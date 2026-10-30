from pathlib import Path
import csv,json
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
p=Path(__file__).resolve().parent
rows=list(csv.DictReader((p/"dataset_manifest.csv").open()))
face={r["acquisition_id"]:r for r in rows if r["status"]=="accepted_face" and r["augmentation"]=="none"}
neg={r["acquisition_id"]:r for r in rows if r["status"]=="accepted_non_face" and r['augmentation']=='none'}
pairs=sorted(face.keys()&neg.keys());use=[r for sid in pairs for r in [neg[sid],face[sid]]]
X=np.stack([np.load(p/r["path"])["mean_spectrum"] for r in use]);y=np.array([r["label"]=="face" for r in use],dtype=float)
groups=np.array([r["split"] for r in use]);results={};predictions=[]
for name,x in [("spectrum_raw_dn",X),("spectrum_sum1",X/X.sum(1,keepdims=True)),("three_band_proxy_raw",X[:,[20,10,0]]),("three_band_proxy_sum1",X[:,[20,10,0]]/X[:,[20,10,0]].sum(1,keepdims=True))]:
 train=groups=="train";mu=x[train].mean(0);sd=x[train].std(0);sd[sd<1e-12]=1
 x=(x-mu)/sd;x=np.column_stack([np.ones(len(x)),x]);xt=x[train];yt=y[train];lam=.01
 def fun(b):
  z=xt@b
  return np.mean(np.logaddexp(0,z)-yt*z)+lam/2*np.dot(b[1:],b[1:])
 def jac(b):
  return xt.T@(expit(xt@b)-yt)/len(yt)+lam*np.r_[0,b[1:]]
 fit=minimize(fun,np.zeros(x.shape[1]),jac=jac,method="L-BFGS-B",options={"maxiter":1000,"gtol":1e-8})
 assert fit.success,fit.message
 metrics={}
 for split in ["val","test"]:
  mask=groups==split;truth=y[mask].astype(int);prob=expit(x[mask]@fit.x);pred=(prob>=.5).astype(int)
  cm=np.zeros((2,2),int)
  for a,b in zip(truth,pred):cm[a,b]+=1
  recall=np.diag(cm)/cm.sum(1);f1=2*np.diag(cm)/(cm.sum(0)+cm.sum(1))
  metrics[split]={"n":len(truth),"balanced_accuracy":float(recall.mean()),"macro_f1":float(f1.mean()),"confusion_matrix_true_rows_pred_cols":cm.tolist()}
  for r,t,pr,sc in zip([r for r,m in zip(use,mask) if m],truth,pred,prob):predictions.append(dict(model=name,split=split,sample_id=r["sample_id"],truth=int(t),prediction=int(pr),probability=float(sc),error=bool(t!=pr)))
 results[name]={"solver":"scipy.optimize L-BFGS-B, fixed L2 lambda=.01, no tuning, train-only standardization","converged":bool(fit.success),"metrics":metrics,"coefficients_standardized":fit.x.tolist()}
(p/"oracle_results.json").write_text(json.dumps(results,indent=2))
(p/"oracle_predictions.json").write_text(json.dumps(predictions,indent=2))
(p/"oracle_sample_ids.json").write_text(json.dumps({"paired_acquisitions":pairs,"sample_ids":[r["sample_id"] for r in use],"counts":{s:sum(r["split"]==s for r in use) for s in ["train","val","test"]},"augmentation_used":False,"matched_true_RGB_available":False},indent=2))
print(json.dumps({n:r["metrics"] for n,r in results.items()},indent=2))
print("counts",{s:int(sum(groups==s)) for s in ["train","val","test"]})
