"""Recover exact input prompts for timed out calls without rerunning inference.
Checks byte equality against every completed call first. Generated output from
killed workers cannot be recovered and is not fabricated.
"""
import json
from pathlib import Path
from transformers import AutoTokenizer
from engine import ROOT,prepare
from evaluate import messages,verify_freeze
verify_freeze()
m=json.loads((ROOT/'results/model.json').read_text())
tok=AutoTokenizer.from_pretrained(m['local_path'],trust_remote_code=False,local_files_only=True)
cases={c['id']:c for c in json.loads((ROOT/'data/heldout.json').read_text())}
rows=[json.loads(x) for x in (ROOT/'results/heldout-final/rows.jsonl').read_text().splitlines()]
verified=0;recovered=[]
for r in rows:
 if not r['method'].startswith('lfm'):continue
 prompt=tok.apply_chat_template(messages(prepare(cases[r['case_id']]['input'],r['method']=='lfm_full')),tokenize=False,add_generation_prompt=True)
 if 'rendered_prompt' in r['runtime']:
  assert prompt==r['runtime']['rendered_prompt'],r['case_id'];verified+=1
 elif r['runtime']['timeout']:
  recovered.append({'case_id':r['case_id'],'method':r['method'],'rendered_prompt':prompt,'prompt_tokens':len(tok.encode(prompt)),'provenance':'Reconstructed after evaluation from frozen code/data and pinned tokenizer. Completed-call prompts were checked for exact equality. Partial generated output is unavailable.'})
assert verified>0
(ROOT/'results/heldout-final/reconstructed-timeout-prompts.json').write_text(json.dumps({'completed_prompts_verified':verified,'timeout_prompts':recovered},indent=2)+'\n')
print('Verified',verified,'completed prompts; reconstructed',len(recovered),'timeout inputs without inference.')
