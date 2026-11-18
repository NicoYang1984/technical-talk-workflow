"""Minimal tests for check_alignment.py. Uses standard library."""
import json
import tempfile
import unittest
from pathlib import Path
from check_alignment import check

class AlignmentTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)
        self.outline = self.root / 'outline.json'
        self.projection = self.root / 'projection.md'
        self.notes = self.root / 'speaker_notes.md'
        self.data = {
            'title': 'Example', 'duration_minutes': 12, 'talk_minutes': 10,
            'discussion_minutes': 2,
            'sections': [
                {'id': 'P00', 'title': '开场', 'minutes': 2},
                {'id': 'P01', 'title': '核心原理', 'minutes': 8},
            ]
        }
        self.outline.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')
        self.projection.write_text('# Talk\n## 开场\n## 核心原理\n', encoding='utf-8')
        self.notes.write_text('# Notes\n## 开场\n## 核心原理\n', encoding='utf-8')

    def test_valid(self):
        self.assertEqual(check(self.outline, self.projection, self.notes), [])

    def test_discussion_node(self):
        self.data['sections'].append({'id': 'P02', 'title': '讨论', 'kind': 'discussion', 'minutes': 2})
        self.outline.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')
        self.projection.write_text('## 开场\n## 核心原理\n## 讨论\n', encoding='utf-8')
        self.notes.write_text('## 开场\n## 核心原理\n## 讨论\n', encoding='utf-8')
        self.assertEqual(check(self.outline, self.projection, self.notes), [])

    def test_mismatch_title(self):
        self.notes.write_text('## 开场\n## 别的标题\n', encoding='utf-8')
        self.assertTrue(any('expected' in s for s in check(self.outline, self.projection, self.notes)))

    def test_mismatch_time(self):
        self.data['sections'][1]['minutes'] = 7
        self.outline.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')
        self.assertTrue(any('minutes sum' in s for s in check(self.outline, self.projection, self.notes)))

    def test_duplicate_title(self):
        self.projection.write_text('## 开场\n## 开场\n', encoding='utf-8')
        self.assertTrue(any('duplicate' in s for s in check(self.outline, self.projection, self.notes)))

    def test_legacy_headings_still_valid(self):
        self.projection.write_text('# Talk\n## [P00] 开场\n## [P01] 核心原理\n', encoding='utf-8')
        self.notes.write_text('# Notes\n## [P00] 开场\n## [P01] 核心原理\n', encoding='utf-8')
        self.assertEqual(check(self.outline, self.projection, self.notes), [])

    def test_mixed_headings_still_valid(self):
        self.notes.write_text('## [P00] 开场\n## 核心原理\n', encoding='utf-8')
        self.assertEqual(check(self.outline, self.projection, self.notes), [])

    def test_hidden_heading_in_fenced_code(self):
        self.notes.write_text('## 开场\n\x60\x60\x60md\n## Fake Heading\n\x60\x60\x60\n## 核心原理\n', encoding='utf-8')
        self.assertEqual(check(self.outline, self.projection, self.notes), [])

    def test_appendix_not_counted(self):
        self.notes.write_text('## 开场\n## 核心原理\n## Appendix\n### More\n', encoding='utf-8')
        self.assertEqual(check(self.outline, self.projection, self.notes), [])

    def test_changed_order_fails(self):
        self.notes.write_text('## 核心原理\n## 开场\n', encoding='utf-8')
        self.assertTrue(any('expected title' in s for s in check(self.outline, self.projection, self.notes)))

if __name__ == '__main__':
    unittest.main()
