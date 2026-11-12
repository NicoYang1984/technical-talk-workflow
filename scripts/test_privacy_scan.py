"""Tests for simple high-confidence secret scanning."""
import tempfile
import unittest
from pathlib import Path
from privacy_scan import scan


class PrivacyScanTests(unittest.TestCase):
    def test_token(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'doc.md'
            p.write_text('token: ghp_'+'Q'*35,encoding='utf-8')
            self.assertTrue(any(tag=='token_like' for _,_,tag in scan(Path(td))))

    def test_clean(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'doc.md'
            p.write_text('A tiny anonymous tutorial.',encoding='utf-8')
            self.assertEqual(scan(Path(td)), [])


if __name__=='__main__':
    unittest.main()
