"""Materialize the exact saved checkpoint revision on another Mac."""
import argparse,json
from pathlib import Path
from huggingface_hub import snapshot_download
p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');args=p.parse_args()
if args.prepare:
 f=Path(__file__).resolve().parent/'results/model.json';m=json.loads(f.read_text())
 m['local_path']=snapshot_download(m['repo'],revision=m['revision'])
 f.write_text(json.dumps(m,indent=2)+'\n')
 print('Pinned checkpoint ready:',m['revision'])
