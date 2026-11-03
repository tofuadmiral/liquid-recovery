import json,unittest
from copy import deepcopy
from engine import prepare,ROOT
from hybrid_adapter import normalize
class HybridContractTests(unittest.TestCase):
 def setUp(self):self.p=prepare(json.loads((ROOT/'data/dev.json').read_text())[1]['input'])
 def test_unobserved_recipe_is_rejected(self):
  c,_=normalize('{"displayed_recipe":"R888","reported_check_ids":[]}',self.p);self.assertIsNone(c)
 def test_extra_prose_or_fields_rejected(self):
  for raw in ['I recommend a reset.', '{"displayed_recipe":null,"reported_check_ids":[],"reset":true}']:
   c,_=normalize(raw,self.p);self.assertIsNone(c)
 def test_no_observation_keeps_policy_step(self):
  c,_=normalize('{"displayed_recipe":null,"reported_check_ids":[]}',self.p);self.assertEqual(c['action_id'],'C_SETUP')
 def test_conflicting_recipe_requires_both_sources(self):
  self.p['operator']['text']='The screen shows recipe R99.'
  c,_=normalize('{"displayed_recipe":"R99","reported_check_ids":[]}',self.p)
  self.assertEqual(c['action_id'],'Q_CONFLICT');self.assertEqual(set(c['evidence_ids']),{'N0','S0'})
 def test_extracted_observation_cannot_override_version(self):
  self.p['machine']['software']='9.0'
  c,_=normalize('{"displayed_recipe":null,"reported_check_ids":["C_SETUP"]}',self.p);self.assertEqual(c['action_id'],'E_VERSION')
 def test_unknown_and_duplicate_checks_fail_closed(self):
  for checks in [['RESET'],['C_SETUP','C_SETUP']]:
   c,_=normalize(json.dumps({'displayed_recipe':None,'reported_check_ids':checks}),self.p);self.assertIsNone(c)
if __name__=='__main__':unittest.main()
