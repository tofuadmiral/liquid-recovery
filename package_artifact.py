"""Curate public source and the single portable replay bundle. No private notes or weights."""
from pathlib import Path
import hashlib,json,zipfile,shutil,re
from engine import ROOT
from evaluate import verify_freeze
from evaluate_hybrid import verify_freeze as verify_hybrid
verify_freeze();verify_hybrid()
files=[]
for name in ['README.md','EVIDENCE.md','.gitignore','vercel.json','engine.py','evaluate.py','evaluate_corrected.py','evaluate_direct_corrected.py','evaluate_hybrid.py','correction_adapter.py','direct_correction_adapter.py','hybrid_adapter.py','reproduce.py','download_model.py','make_scenarios.py','make_correction_cases.py','build_artifact.py','build_memo.py','artifact.template.html','summarize_results.py','summarize_hybrid.py','reconstruct_prompts.py','requirements.lock','package.json','package-lock.json','package_artifact.py','correction_probe.py','correction_probe_b.py','correction_probe_c.py','correction_probe_tools.py','hybrid_probe.py']:
 p=ROOT/name
 if p.exists():files.append(p)
for folder in ['data','prompts','tests','docs','site']:
 files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in str(p))
for name in ['dev-v1','dev-v2','heldout-final','correction-dev','hybrid-dev','hybrid-dev-v2','hybrid-final']:
 files.extend(p for p in (ROOT/'results'/name).rglob('*') if p.is_file() and '__pycache__' not in str(p))
for p in (ROOT/'results').iterdir():
 if p.is_file() and p.name not in {'finalization.log'} and p.suffix in {'.json','.md','.log'}:files.append(p)
for name in ['output/replay.html','output/memo.md','output/pdf/liquid-recovery-memo.pdf']:
 files.append(ROOT/name)
archive=ROOT/'output/liquid-recovery-artifact.zip'
public=ROOT.parent/'liquid-recovery-public';public.mkdir(exist_ok=True)
manifest={}
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(set(files)):
  name=str(p.relative_to(ROOT));data=p.read_bytes()
  if name=='results/model.json':
   obj=json.loads(data);obj.pop('local_path',None);data=(json.dumps(obj,indent=2)+'\n').encode()
  if p.suffix in {'.json','.jsonl','.md','.log','.py','.html'}:
   text=data.decode()
   assert not re.search(r'/Users/[^/]+/(?:vaults|\.cache)/',text), f'Private path in {name}'
  manifest[name]=hashlib.sha256(data).hexdigest();z.writestr(name,data)
  dest=public/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 z.writestr('MANIFEST.sha256.json',json.dumps(manifest,indent=2)+'\n')
(public/'MANIFEST.sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert all(hashlib.sha256(z.read(n)).hexdigest()==sha for n,sha in manifest.items())
print(f'Curated {len(manifest)} public files and verified {archive.stat().st_size:,} byte archive.')
