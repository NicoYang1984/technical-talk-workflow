"""Tests for content, media and speaking-time audits; standard library only."""
import json
import tempfile
import unittest
from pathlib import Path
from audit_talk import audit


class AuditTalkTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.o = self.root / 'outline.json'
        self.p = self.root / 'projection.md'
        self.n = self.root / 'speaker_notes.md'
        self.v = self.root / 'visuals.json'
        self.data = {
            'duration_minutes': 10, 'talk_minutes': 8, 'discussion_minutes': 2,
            'sections': [
                {'id': 'P00', 'title': 'Mechanism', 'minutes': 8, 'visual_id': 'flow',
                 'anchors': {'projection': ['A=B'], 'notes': ['A=B']}},
                {'id': 'P01', 'title': 'Discussion', 'kind': 'discussion', 'minutes': 2,
                 'anchors': {'both': ['question']}}
            ]}
        self.o.write_text(json.dumps(self.data), encoding='utf-8')
        self.p.write_text('## [P00] Mechanism\nA=B\n## [P01] Discussion\nquestion\n',encoding='utf-8')
        self.n.write_text('## [P00] Mechanism\nA=B\n## [P01] Discussion\nquestion\n',encoding='utf-8')
        (self.root/'flow.mmd').write_text('flowchart LR\nA-->B\n',encoding='utf-8')
        (self.root/'flow.txt').write_text('A -> B',encoding='utf-8')
        self.v.write_text(json.dumps({'visuals':[{'id':'flow','source_path':'flow.mmd',
                           'fallback_path':'flow.txt','rendered_ok':True}]}),encoding='utf-8')

    def test_all_pass(self):
        self.assertEqual(audit(self.o,self.p,self.n,self.v), ([],[]))

    def test_anchor_missing(self):
        self.n.write_text(self.n.read_text().replace('A=B','C=D'),encoding='utf-8')
        errors,_ = audit(self.o,self.p,self.n,self.v)
        self.assertTrue(any('missing exact anchor' in e for e in errors))

    def test_missing_media(self):
        (self.root/'flow.txt').unlink()
        errors,_ = audit(self.o,self.p,self.n,self.v)
        self.assertTrue(any('fallback_path not found' in e for e in errors))

    def test_pace_warning(self):
        a='<!-- SPOKEN START -->'+'大家好我们开始讲清楚这个问题'*250+'<!-- SPOKEN END -->'
        self.n.write_text('## [P00] Mechanism\nA=B\n'+a+'\n## [P01] Discussion\nquestion',encoding='utf-8')
        errors,warnings = audit(self.o,self.p,self.n,self.v)
        self.assertEqual(errors, [])
        self.assertTrue(any('may run long' in s for s in warnings))


if __name__=='__main__':
    unittest.main()
