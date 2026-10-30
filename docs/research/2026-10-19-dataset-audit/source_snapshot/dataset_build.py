"""Local UWA production. No hardware, classifier, learned detector or registration."""
from pathlib import Path
import argparse,csv,hashlib,io,json,zipfile
import cv2,numpy as np,yaml
from PIL import Image,ImageDraw

def digest(p):
 with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def targets(cube):
 s=cube.mean((1,2),dtype=np.float64)
 if not np.isfinite(s).all() or s.sum()<=0:raise ValueError("invalid spectrum")
 return s,s/s.sum()
def save(path,cube,meta):
 if path.exists():raise FileExistsError(path)
 s,q=targets(cube)
 np.savez_compressed(path,cube=cube,wavelengths_nm=np.arange(450,651,10),mean_spectrum=s,relative_spectrum=q,
  pseudo_rgb=np.moveaxis(cube[[20,10,0]],0,-1).astype(np.float32)/255,metadata_json=json.dumps(meta))
def write_manifest(path,rows):
 with path.open("w",encoding="utf-8",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def build(root,cfg):
 out=root/cfg["output"];out.mkdir(exist_ok=False)
 (out/"candidates").mkdir();preview=root/"dataset_preview";preview.mkdir(exist_ok=False)
 archive=(root/cfg["archive"]).resolve();assert digest(archive)==cfg["archive_sha256"]
 samples=json.loads((root/cfg["samples_index"]).read_text())
 groups=json.loads((root/cfg["subject_groups"]).read_text())
 mapping={s:split for split,k in [("train","train"),("val","validation"),("test","test")] for s in groups[k+"_subjects"]}
 assert len(mapping)==78 and sum(len(groups[k+"_subjects"]) for k in ["train","validation","test"])==78
 (root/"splits.json").write_text(json.dumps({"rule":"subject disjoint; all sessions/derivatives inherit subject group","subject_to_split":mapping,"acquisition_to_split":{s:mapping[v["subject"]] for s,v in samples.items()}},indent=2))
 rows=[];tiles=[];fingerprints={}
 with zipfile.ZipFile(archive) as z:
  for idx,(sid,spec) in enumerate(samples.items()):
   flags=[];eyes=np.loadtxt(io.BytesIO(z.read(spec["fiducial_member"])))
   if eyes.shape!=(2,2) or not np.isfinite(eyes).all() or (eyes<0).any() or (eyes>=1024).any():raise ValueError("invalid eyes "+sid)
   distance=float(np.linalg.norm(eyes[1]-eyes[0]));side=int(np.ceil(4*distance))
   center=eyes.mean(0)+[0,.5*distance];x,y=np.floor(center-side/2).astype(int)
   # Invalid/clipped proposals are not silently padded or moved.
   if x<0 or y<0 or x+side>1024 or y+side>1024:
    rows.append(dict(sample_id=sid.replace("/","_"),acquisition_id=sid,subject_id=spec["subject"],session_id=spec["session"],split=mapping[spec["subject"]],label="face",path="",status="rejected_crop_boundary",augmentation="none",quality_flags="crop_out_of_bounds",source_sha256=cfg["archive_sha256"],sample_sha256=""))
    continue
   arrays=[];source_hashes=[]
   for band in range(6,27):
    member=f"UWA HSFD V1.1/HyperSpec_Face_Session{spec['session']}/{spec['subject']}/F_{band:02d}.png"
    b=z.read(member);a=cv2.imdecode(np.frombuffer(b,np.uint8),cv2.IMREAD_UNCHANGED)
    assert a.shape==(1024,1024) and a.dtype==np.uint8
    arrays.append(a[y:y+side,x:x+side]);source_hashes.append(hashlib.sha256(b).hexdigest())
   raw=np.stack(arrays);cube=np.stack([cv2.resize(a,(256,256),interpolation=cv2.INTER_AREA) for a in raw.astype(np.float32)])
   limit=(raw==255).mean((1,2));zero=(raw==0).mean((1,2))
   if limit.max()>0:flags.append("source_has_255_review_not_proven_saturation")
   # Diagnostic only: different spectra can change gradients. No warp is applied.
   def edge(a):
    g=cv2.GaussianBlur(a,(5,5),0)
    return cv2.magnitude(cv2.Sobel(g,cv2.CV_32F,1,0),cv2.Sobel(g,cv2.CV_32F,0,1))
   ref=edge(cube[10]);win=cv2.createHanningWindow((256,256),cv2.CV_32F);motion=[]
   for wave,a in zip(cfg["wavelengths_nm"],cube):
    shift,response=cv2.phaseCorrelate(ref.copy(),edge(a),win.copy())
    motion.append({"wavelength_nm":wave,"shift_xy_output_px":list(shift),"response":response})
   if any(np.linalg.norm(m["shift_xy_output_px"])>4 and m["response"]>=.2 for m in motion):flags.append("possible_band_motion")
   if any(m["response"]<.2 for m in motion):flags.append("motion_check_low_confidence")
   key=sid.replace("/","_");fp=hashlib.sha256("".join(source_hashes).encode()).hexdigest()
   if fp in fingerprints:flags.append("duplicate_acquisition_content")
   fingerprints[fp]=sid
   meta=dict(sample_id=key,label="face",label_source="UWA subject and eye annotations; full-face crop pending visual review",subject_id=spec["subject"],session_id=spec["session"],acquisition_id=sid,split=mapping[spec["subject"]],crop_xywh=[int(x),int(y),side,side],output_hw=[256,256],reference_wavelength_nm=550,eyes_source_xy=eyes.tolist(),eyes_output_xy=((eyes-[x,y])*256/side).tolist(),geometry="same crop and INTER_AREA resize for all bands; no registration",wavelengths_nm=cfg["wavelengths_nm"],augmentation=None,quality_flags=flags,source_255_fraction=limit.tolist(),source_zero_fraction=zero.tolist(),motion_diagnostic=motion,source_archive=str(archive),source_sha256=cfg["archive_sha256"],source_band_sha256=source_hashes,semantic_review="pending",radiometric_units="processed UWA DN; not calibrated reflectance",pseudo_rgb="650/550/450 bands; uncalibrated; fixed DN/255")
   file=out/"candidates"/(key+".npz");save(file,cube,meta)
   rows.append(dict(sample_id=key,acquisition_id=sid,subject_id=spec["subject"],session_id=spec["session"],split=mapping[spec["subject"]],label="face",path=str(file.relative_to(root)),status="pending_review",augmentation="none",quality_flags=";".join(flags),source_sha256=cfg["archive_sha256"],sample_sha256=digest(file)))
   tile=Image.new("RGB",(384,148))
   for j,bi in enumerate([0,10,20]):
    pic=Image.fromarray(np.uint8(np.clip(cube[bi],0,255))).resize((128,128))
    tile.paste(pic.convert("RGB"),(j*128,0))
   ImageDraw.Draw(tile).text((3,130),key+" 450/550/650 "+("FLAG" if flags else ""),fill="white")
   tiles.append((key,tile))
   if len(rows)%20==0:print("built",len(rows),flush=True)
 for n,start in enumerate(range(0,len(tiles),24)):
  page=Image.new("RGB",(1536,888))
  for i,(_,tile) in enumerate(tiles[start:start+24]):page.paste(tile,((i%4)*384,(i//4)*148))
  page.save(preview/f"sheet_{n+1:02d}.png")
 (root/"preview_index.json").write_text(json.dumps({f"sheet_{n+1:02d}.png":[k for k,_ in tiles[start:start+24]] for n,start in enumerate(range(0,len(tiles),24))},indent=2))
 write_manifest(root/"dataset_manifest.csv",rows)
 (root/"build_versions.json").write_text(json.dumps({"numpy":np.__version__,"opencv":cv2.__version__,"archive_sha256":digest(archive),"script_sha256":digest(Path(__file__))},indent=2))
 print("base",len(rows),"files",len(tiles),flush=True)

def finalize(root,cfg):
 review=json.loads((root/"review_decisions.json").read_text())
 rows=list(csv.DictReader((root/"dataset_manifest.csv").open(encoding="utf-8")))
 if any(r["augmentation"]!="none" for r in rows):raise ValueError("already finalized")
 dest=root/cfg["output"]/"reviewed";dest.mkdir(exist_ok=False);extra=[]
 for r in rows:
  if not r["path"]:continue
  z=np.load(root/r["path"]);meta=json.loads(str(z["metadata_json"]));cube=z["cube"]
  decision=review["samples"].get(r["sample_id"],"pending")
  meta["semantic_review"]=decision;flags=meta["quality_flags"]
  flags.extend(review.get("additional_quality_flags",{}).get(r["sample_id"],[]))
  r["quality_flags"]=";".join(flags)
  r["status"]="accepted_face" if decision=="full_face_visible" and not flags else "pending_quality_review"
  if decision=="incomplete_or_uncertain":r["status"]="pending_semantic_review"
  meta["quality_status"]=r["status"]
  target=dest/(r["sample_id"]+".npz");save(target,cube,meta)
  r["path"]=str(target.relative_to(root));r["sample_sha256"]=digest(target)
  if r["status"]!="accepted_face" or r["split"]!="train":continue
  seed=int.from_bytes(hashlib.sha256((cfg["augmentation"]["seed_namespace"]+r["acquisition_id"]).encode()).digest()[:4],"little")
  rng=np.random.default_rng(seed);flip=bool(rng.random()<.5);gain=float(rng.uniform(.95,1.05))
  aug=np.ascontiguousarray(cube[:,:,::-1] if flip else cube)*gain
  am=dict(meta);am["sample_id"]=r["sample_id"]+"_aug01";am["augmentation"]={"seed":seed,"parent_acquisition_id":r["acquisition_id"],"parent_sample_id":r["sample_id"],"horizontal_flip":flip,"shared_brightness_scale":gain,"clipping":"none; float32 processed DN"}
  if flip:am["eyes_output_xy"]=[[255-x,y] for x,y in am["eyes_output_xy"]]
  target=dest/(am["sample_id"]+".npz");save(target,aug,am)
  ar=dict(r);ar.update(sample_id=am["sample_id"],path=str(target.relative_to(root)),augmentation=json.dumps(am["augmentation"]),sample_sha256=digest(target));extra.append(ar)
 write_manifest(root/"dataset_manifest.csv",rows+extra)
 print("accepted",sum(r["status"]=="accepted_face" for r in rows),"aug",len(extra),flush=True)
def negatives(root,cfg):
 rows=list(csv.DictReader((root/"dataset_manifest.csv").open(encoding="utf-8")))
 if any(r['label']=='non_face' for r in rows):raise ValueError('negatives already built')
 parents=[r for r in rows if r['status']=='accepted_face' and r['augmentation']=='none']
 reviewed=json.loads((root/'review_decisions.json').read_text()).get('negative_samples',{})
 dest=root/cfg['output']/'non_face';dest.mkdir(exist_ok=False);extra=[];tiles=[]
 with zipfile.ZipFile((root/cfg['archive']).resolve()) as z:
  for r in parents:
   cube=[];hashes=[]
   for band in range(6,27):
    name=f"UWA HSFD V1.1/HyperSpec_Face_Session{r['session_id']}/{r['subject_id']}/F_{band:02d}.png"
    b=z.read(name);a=cv2.imdecode(np.frombuffer(b,np.uint8),cv2.IMREAD_UNCHANGED)
    cube.append(a[768:1024,0:256]);hashes.append(hashlib.sha256(b).hexdigest())
   cube=np.stack(cube).astype(np.float32);flags=[];motion=[]
   for a in cube:
    shift,response=cv2.phaseCorrelate(cube[10].copy(),a.copy(),cv2.createHanningWindow((256,256),cv2.CV_32F))
    motion.append({'shift_xy':list(shift),'response':response})
   if (cube==255).any():flags.append('source_has_255_review_not_proven_saturation')
   if any(np.linalg.norm(m['shift_xy'])>4 and m['response']>=.2 for m in motion):flags.append('possible_band_motion')
   if any(m['response']<.2 for m in motion):flags.append('motion_check_low_confidence')
   key=r['sample_id']+'_nonface'
   if reviewed.get(key)!='no_face_or_face_contour_visible_in_450_550_650_review':flags.append('negative_semantic_review_pending')
   meta=dict(sample_id=key,label='non_face',label_source='agent visual inspection of fixed lower-left ROI at 550nm; endpoint previews retained',subject_id=r['subject_id'],session_id=r['session_id'],acquisition_id=r['acquisition_id'],split=r['split'],crop_xywh=[0,768,256,256],wavelengths_nm=cfg['wavelengths_nm'],augmentation=None,quality_flags=flags,motion_diagnostic=motion,source_band_sha256=hashes,source_sha256=cfg['archive_sha256'],scene_source='shared UWA backdrop and subject clothing; not independent scenes',pseudo_rgb='650/550/450; uncalibrated DN/255',radiometric_units='original UWA DN float32')
   file=dest/(key+'.npz');save(file,cube,meta)
   nr=dict(r);nr.update(sample_id=key,label='non_face',path=str(file.relative_to(root)),status='pending_quality_review' if flags else 'accepted_non_face',quality_flags=';'.join(flags),sample_sha256=digest(file));extra.append(nr)
   tile=Image.new('RGB',(384,148))
   for j,bi in enumerate([0,10,20]):tile.paste(Image.fromarray(cube[bi].astype(np.uint8)).resize((128,128)).convert('RGB'),(128*j,0))
   ImageDraw.Draw(tile).text((0,130),key,fill='white');tiles.append(tile)
 for page,start in enumerate(range(0,len(tiles),24)):
  canvas=Image.new('RGB',(1536,888))
  for i,tile in enumerate(tiles[start:start+24]):canvas.paste(tile,((i%4)*384,(i//4)*148))
  canvas.save(root/f'dataset_preview/nonface_spectral_{page+1}.png')
 write_manifest(root/'dataset_manifest.csv',rows+extra)
 print('negative statuses', {s:sum(r['status']==s for r in extra) for s in {r['status'] for r in extra}},flush=True)
def augment_negatives(root,cfg):
 rows=list(csv.DictReader((root/'dataset_manifest.csv').open(encoding='utf-8')))
 if any(r['label']=='non_face' and r['augmentation']!='none' for r in rows):raise ValueError('already augmented')
 extra=[]
 for r in rows:
  if r['label']!='non_face' or r['status']!='accepted_non_face' or r['split']!='train':continue
  z=np.load(root/r['path']);cube=z['cube'];m=json.loads(str(z['metadata_json']))
  seed=int.from_bytes(hashlib.sha256((cfg['augmentation']['seed_namespace']+r['acquisition_id']).encode()).digest()[:4],'little')
  rng=np.random.default_rng(seed);flip=bool(rng.random()<.5);gain=float(rng.uniform(.95,1.05))
  aug=np.ascontiguousarray(cube[:,:,::-1] if flip else cube)*gain
  m['sample_id']=r['sample_id']+'_aug01';m['augmentation']={'seed':seed,'parent_acquisition_id':r['acquisition_id'],'parent_sample_id':r['sample_id'],'horizontal_flip':flip,'shared_brightness_scale':gain,'clipping':'none; float32 processed DN'}
  path=root/cfg['output']/'non_face'/(m['sample_id']+'.npz');save(path,aug,m)
  ar=dict(r);ar.update(sample_id=m['sample_id'],path=str(path.relative_to(root)),augmentation=json.dumps(m['augmentation']),sample_sha256=digest(path));extra.append(ar)
 write_manifest(root/'dataset_manifest.csv',rows+extra)
 print('negative augmentation',len(extra),flush=True)
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--finalize",action="store_true");ap.add_argument('--negatives',action='store_true');ap.add_argument('--augment-negatives',action='store_true');args=ap.parse_args()
 root=Path(__file__).resolve().parent;cfg=yaml.safe_load((root/"preprocessing_config.yaml").read_text())
 (augment_negatives if args.augment_negatives else negatives if args.negatives else finalize if args.finalize else build)(root,cfg)
