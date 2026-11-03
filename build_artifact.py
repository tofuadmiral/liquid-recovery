from pathlib import Path
import json
from engine import ROOT,PACKAGE
runs={}
for name in ('dev-v1','dev-v2','heldout-final','correction-dev','hybrid-dev','hybrid-dev-v2','hybrid-final'):
 d=ROOT/'results'/name
 if (d/'summary.json').exists():
  runs[name]={'summary':json.loads((d/'summary.json').read_text()),'metadata':json.loads((d/'metadata.json').read_text()),'rows':[json.loads(x) for x in (d/'rows.jsonl').read_text().splitlines()]}
payload={'cases':sum([json.loads((ROOT/f'data/{s}.json').read_text()) for s in ('dev','heldout','correction-heldout')],[]),'package':PACKAGE,'runs':runs}
template=(ROOT/'artifact.template.html').read_text()
output=template.replace('__PAYLOAD__',json.dumps(payload).replace('</','<\\/'))
(ROOT/'output/replay.html').write_text(output.replace('href="memo.pdf"','href="pdf/liquid-recovery-memo.pdf"'))
(ROOT/'site').mkdir(exist_ok=True)
(ROOT/'site/index.html').write_text(output)
print('Built standalone output/replay.html:',len(output),'bytes')
