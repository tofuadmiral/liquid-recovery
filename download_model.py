import json, time
from pathlib import Path
from huggingface_hub import HfApi, snapshot_download
repo = 'LiquidAI/LFM2.5-2.6B-MLX-4bit'
info = HfApi().model_info(repo)
start = time.perf_counter()
path = snapshot_download(repo, revision=info.sha)
config = json.loads((Path(path)/'config.json').read_text())
manifest = {'repo':repo,'revision':info.sha,'local_path':path,'download_seconds':time.perf_counter()-start,'quantization':config.get('quantization'),'model_type':config.get('model_type')}
Path('results/model.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
