// Isolated DOM unit tests. No live browser, network, or user computer interaction.
const fs = require('node:fs');
const assert = require('node:assert/strict');
const {JSDOM,VirtualConsole} = require('jsdom');
const html=fs.readFileSync('output/replay.html','utf8');
let errors=[];const log=new VirtualConsole();log.on('jsdomError',e=>errors.push(e.message));
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://synthetic-replay.test/',virtualConsole:log,beforeParse(w){w.scrollTo=()=>{};}});
const w=dom.window,d=w.document;
const el=id=>d.getElementById(id);
let checked=0;
for(const run of Array.from(el('run-select').options).map(o=>o.value)){
 el('run-select').value=run;w.changeRun();
 const cases=Array.from(el('case-select').options).map(o=>o.value);
 for(const id of cases){
  el('case-select').value=id;w.renderReplay();
  const methods=Array.from(el('replay-body').querySelectorAll('.method-grid button')).map(b=>b.getAttribute('onclick').match(/choose\('([^']+)'\)/)[1]);
  for(const method of methods){
   w.choose(method);
   assert.ok(el('replay-body').textContent.includes('MOCK:'));
   assert.ok(el('replay-body').textContent.includes('Original instruction'));
   for(const a of el('replay-body').querySelectorAll('a.ref')){
    assert.ok(d.querySelector(a.getAttribute('href')),`${run}/${id} missing evidence target ${a.hash}`);
   }
   assert.equal(el('replay-body').querySelectorAll('script').length,0,'Evidence must never inject executable markup');
   checked++;
  }
 }
 w.showTab('evaluation');assert.equal(el('evaluation').classList.contains('hide'),false);
 assert.ok(el('evaluation-body').textContent.includes('Failure ledger'));
 w.showTab('protocol');assert.equal(el('protocol').classList.contains('hide'),false);
 w.showTab('replay');assert.equal(el('replay').classList.contains('hide'),false);
}
const before=el('case-select').value;w.adjacent(1);assert.notEqual(el('case-select').value,before);w.adjacent(-1);assert.equal(el('case-select').value,before);
w.recordOutcome();const entries=JSON.parse(w.localStorage.getItem('liquid-replay-demo-outcomes'));
assert.equal(entries.length,1);assert.equal(entries[0].root_cause_confirmed,false);assert.equal(entries[0].synthetic_demo,true);
assert.ok(el('outcome-status').textContent.includes('Saved locally'));
el('outcome-choice').value='service_confirmed_resumption';w.recordOutcome();
const confirmed=JSON.parse(w.localStorage.getItem('liquid-replay-demo-outcomes'))[1];
assert.equal(confirmed.confirmed_by,'service');assert.equal(confirmed.root_cause_confirmed,false);
assert.equal(errors.length,0,errors.join('\n'));
console.log(`Passed ${checked} case/method render combinations, source targets, tabs, case navigation, untrusted text rendering and isolated outcome storage.`);
dom.window.close();
