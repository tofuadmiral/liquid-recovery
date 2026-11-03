// Isolated functional tests of the recorded terminal demo.
const fs=require('node:fs'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom');
const html=fs.readFileSync(process.env.REPLAY_HTML||'output/replay.html','utf8');
let errors=[];const log=new VirtualConsole();log.on('jsdomError',e=>errors.push(e.message));
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://synthetic-replay.test/',virtualConsole:log,beforeParse(w){w.scrollTo=()=>{};}});
const w=dom.window,d=w.document,el=id=>d.getElementById(id);
assert.equal(el('story').classList.contains('hide'),false);
assert.equal(el('case-select').options.length,24);
assert.equal(el('method-select').options.length,3);
assert.equal(html.includes('Built for an honest product decision'),false);
assert.equal(html.includes('hold the LFM product bet'),false);
let checked=0;
for(const id of Array.from(el('case-select').options).map(x=>x.value)){
 el('case-select').value=id;w.renderReplay();
 for(const method of Array.from(el('method-select').options).map(x=>x.value)){
  w.choose(method);assert.ok(el('replay-body').textContent.includes('MOCK:'));
  assert.ok(el('replay-body').textContent.includes('Original instruction'));
  for(const a of el('replay-body').querySelectorAll('a.ref'))assert.ok(d.querySelector(a.hash),`${id}/${method} missing ${a.hash}`);
  assert.equal(el('replay-body').querySelectorAll('script').length,0);
  checked++;
 }
}
w.setStoryStep(3);assert.equal(el('story-source').textContent,'F01a ↗');assert.match(el('story-instruction-text').textContent,/setup-checklist/);assert.equal(el('machine-checks').textContent,'1');
w.setStoryStep(4);assert.equal(el('machine-checks').textContent,'2');assert.equal(el('story-source').textContent,'F01b ↗');
w.setStoryStep(5);assert.match(el('story-instruction-text').textContent,/alarm-detail/);assert.equal(el('story-next').disabled,true);
w.setStoryStep(0);assert.equal(el('story-prev').disabled,true);w.toggleStory();assert.equal(el('play-btn').getAttribute('aria-pressed'),'true');w.showTab('replay');assert.equal(el('play-btn').getAttribute('aria-pressed'),'false');
w.openStoryCase();assert.equal(el('case-select').value,'F01a');
const before=el('case-select').value;w.adjacent(1);assert.notEqual(el('case-select').value,before);w.adjacent(-1);assert.equal(el('case-select').value,before);
w.revealEvidence();assert.equal(el('evidence-details').open,true);
w.showTab('evaluation');assert.equal(el('evaluation').classList.contains('hide'),false);assert.match(el('evaluation-body').textContent,/Rules with history/);assert.match(el('evaluation-body').textContent,/Every case and result/);
w.showTab('replay');w.recordOutcome();let entry=JSON.parse(w.localStorage.getItem('liquid-replay-demo-outcomes'))[0];assert.equal(entry.synthetic_demo,true);assert.equal(entry.root_cause_confirmed,false);
el('outcome-choice').value='service_confirmed_resumption';w.recordOutcome();entry=JSON.parse(w.localStorage.getItem('liquid-replay-demo-outcomes'))[1];assert.equal(entry.confirmed_by,'service');assert.equal(entry.root_cause_confirmed,false);
assert.equal(errors.length,0,errors.join('\n'));
console.log(`Passed ${checked} case and method combinations, all story states, playback controls, evidence targets, tabs, untrusted text rendering and local outcome storage.`);
dom.window.close();
