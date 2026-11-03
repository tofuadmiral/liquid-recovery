import json,unittest
from copy import deepcopy
from engine import ROOT,PACKAGE,prepare,validate,score,parse_answer,decision,tree

class ContractTests(unittest.TestCase):
 def setUp(self):
  self.case=json.loads((ROOT/'data/dev.json').read_text())[0]
  self.p=prepare(self.case['input'])
 def test_correct_control(self):
  candidate=decision('C_RECIPE',['S0']);out,errors=validate(candidate,self.p)
  self.assertTrue(score(self.case,candidate,self.p,out,errors)['passed'])
 def test_allowed_but_wrong_not_hidden_by_guard(self):
  candidate=decision('C_OBSERVE',['S0']);out,errors=validate(candidate,self.p)
  s=score(self.case,candidate,self.p,out,errors)
  self.assertFalse(s['correct']);self.assertTrue(s['unsupported_check_selection'])
 def test_unknown_action_and_fabricated_reference_rejected(self):
  bad={'action_id':'RESET_PLC','evidence_ids':['X999'],'missing_information':[]}
  out,errors=validate(bad,self.p)
  self.assertEqual(out['action_id'],'E_VALIDATION')
  self.assertIn('unknown_action',errors);self.assertIn('nonexistent_evidence',errors)
 def test_extra_assertion_rejected(self):
  bad={**decision('C_RECIPE',['S0']),'root_cause':'broken_motor'}
  out,errors=validate(bad,self.p)
  self.assertIn('unsupported_fields_or_prose',errors)
  self.assertTrue(score(self.case,bad,self.p,out,errors)['unsupported_assertion'])
 def test_procedure_version_and_exhaustion(self):
  bad=deepcopy(self.p);bad['machine']['software']='unlisted'
  self.assertIn('inapplicable_procedure',validate(decision('C_RECIPE',['S0']),bad)[1])
  bad=deepcopy(self.p);bad['derived']['attempted_check_ids']=['C_RECIPE']
  self.assertIn('exhausted_check',validate(decision('C_RECIPE',['S0']),bad)[1])
 def test_wrong_evidence_does_not_pass(self):
  cand=decision('C_RECIPE',['N0']);out,errors=validate(cand,self.p)
  s=score(self.case,cand,self.p,out,errors)
  self.assertTrue(s['valid_evidence_refs']);self.assertFalse(s['complete_gold_evidence'])
 def test_parser_does_not_use_reasoning_json(self):
  obj,_=parse_answer('thinking {"action_id":"ACT_RESET"}</think>'+json.dumps(decision('C_RECIPE',['S0'])))
  self.assertEqual(obj['action_id'],'C_RECIPE')
  self.assertIsNone(parse_answer('still thinking {"action_id":"C_RECIPE"}')[0])
 def test_negated_attempt_not_treated_as_completed(self):
  p=deepcopy(self.p);p['snapshot'].update(recipe='R17',alarm='SYN-202')
  p['operator']['text']='I have not copied the alarm-detail text yet.'
  self.assertEqual(tree(p)['action_id'],'C_OBSERVE')
 def test_split_integrity_and_evidence(self):
  a=json.loads((ROOT/'data/dev.json').read_text());b=json.loads((ROOT/'data/heldout.json').read_text())
  self.assertEqual((len(a),len(b)),(12,24))
  self.assertFalse({x['group'] for x in a}&{x['group'] for x in b})
  self.assertEqual(len({x['id'] for x in a+b}),36)
  self.assertTrue(all(len([y for y in a+b if y['group']==x['group']])==2 for x in a+b))
  for c in a+b:
   from engine import source_ids
   self.assertTrue(set(c['gold']['required_evidence'])<=source_ids(prepare(c['input'])))
 def test_current_ablation_really_omits_observations(self):
  p=prepare(self.case['input'],False)
  self.assertNotIn('operator',p);self.assertNotIn('history',p);self.assertFalse(p['derived']['history_available'])
if __name__=='__main__':unittest.main()
