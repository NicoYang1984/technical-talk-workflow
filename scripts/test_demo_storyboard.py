"""Demo storyboard contract tests, stdlib only."""
import json
import tempfile
import unittest
from pathlib import Path
from check_demo_storyboard import check_storyboard


class DemoStoryboardTests(unittest.TestCase):
    def setUp(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.root = Path(td.name)
        self.data = {
            "demo_id": "a", "section_id": "P02", "question": "What changes?",
            "input_state": {"same": "x"}, "change_one_thing": "strategy",
            "predict": "Which output?", "steps": [
                {"step": 1, "highlight": "a", "narration": "Look", "expected_state": "0"},
                {"step": 2, "highlight": "b", "narration": "Compute", "expected_state": "1"}],
            "reveal": "1", "mechanism": "calculation", "boundary": "illustrative only",
            "fallback": "still.txt", "evidence_level": "illustrative"}
        (self.root / "still.txt").write_text("still", encoding="utf-8")

    def _write(self):
        p = self.root / "demo.json"
        p.write_text(json.dumps(self.data), encoding="utf-8")
        return p

    def test_valid(self):
        self.assertFalse(check_storyboard(self._write()))

    def test_requires_fallback(self):
        self.data["fallback"] = "missing.png"
        self.assertTrue(any("Fallback missing" in s for s in check_storyboard(self._write())))

    def test_single_frame_not_enough(self):
        self.data["steps"] = self.data["steps"][:1]
        self.assertTrue(any("at least two" in s for s in check_storyboard(self._write())))

    def test_measurements_need_source(self):
        self.data["evidence_level"] = "measured"
        self.assertTrue(any("measurement_source" in s for s in check_storyboard(self._write())))


if __name__ == "__main__":
    unittest.main()
