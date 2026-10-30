from pathlib import Path
import csv,json,hashlib,collections
import numpy as np
p=Path(__file__).resolve().parent
rows=list(csv.DictReader((p/"dataset_manifest.csv").open(encoding="utf-8")))
groups=json.loads((p/"splits.json").read_text())
seen={};counts=collections.Counter();statuses=collections.Counter();flags=collections.Counter()
for r in rows:
 assert groups["subject_to_split"][r["subject_id"]]==r["split"]
 assert groups["acquisition_to_split"][r["acquisition_id"]]==r["split"]
 if r["subject_id"] in seen:assert seen[r["subject_id"]]==r["split"]
 seen[r["subject_id"]]=r["split"];statuses[r["status"]]+=1
 if not r["path"]:continue
 f=p/r["path"]
 with f.open("rb") as stream:assert hashlib.file_digest(stream,"sha256").hexdigest()==r["sample_sha256"]
 z=np.load(f);a=z["cube"];m=json.loads(str(z["metadata_json"]))
 assert a.shape==(21,256,256) and a.dtype==np.float32 and np.isfinite(a).all()
 assert np.array_equal(z["wavelengths_nm"],np.arange(450,651,10))
 assert np.allclose(z["mean_spectrum"],a.mean((1,2),dtype=np.float64),atol=1e-10)
 assert np.allclose(z["relative_spectrum"],z["mean_spectrum"]/z["mean_spectrum"].sum(),atol=1e-12)
 assert np.array_equal(z["pseudo_rgb"],np.moveaxis(a[[20,10,0]],0,-1)/np.float32(255))
 assert m["subject_id"]==r["subject_id"] and m["acquisition_id"]==r["acquisition_id"]
 flags.update(m["quality_flags"])
 if r["augmentation"]!="none":
  assert r["split"]=="train" and r["status"] in ("accepted_face","accepted_non_face")
  am=m["augmentation"];parent=next(v for v in rows if v["sample_id"]==am["parent_sample_id"])
  assert parent["acquisition_id"]==r["acquisition_id"]
  pa=np.load(p/parent["path"])["cube"]
  expected=(pa[:,:,::-1] if am["horizontal_flip"] else pa)*am["shared_brightness_scale"]
  assert np.array_equal(expected,a)
  assert np.allclose(z["relative_spectrum"],np.load(p/parent["path"])["relative_spectrum"],atol=1e-8)
 counts[(r["split"],r["augmentation"]=="none",r["status"])]+=1
summary={"manifest_rows":len(rows),"independent_acquisitions":len({r["acquisition_id"] for r in rows}),"subjects":len(seen),"status_counts":dict(statuses),"counts":[{"split":k[0],"original":k[1],"status":k[2],"n":n} for k,n in counts.items()],"quality_flag_counts_files":dict(flags),"all_file_hashes_targets_shapes_group_checks_pass":True,"non_face_samples":sum(r['label']=='non_face' for r in rows)}
(p/"validation_summary.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
