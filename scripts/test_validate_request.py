"""Tests for request defaults and validation. Uses only Python stdlib."""
import unittest

from validate_request import validate


class TestInputContract(unittest.TestCase):
    def test_one_topic_is_enough_for_provisional_test(self):
        data, errors, assumptions = validate({"topic": "B+ tree", "mode": "test"})
        self.assertFalse(errors)
        self.assertEqual((data["duration_minutes"], data["discussion_minutes"]), (30, 5))
        self.assertIn("audience", assumptions)
        self.assertIn("duration_minutes", assumptions)

    def test_fully_specified_does_not_assume_core(self):
        data, errors, assumptions = validate({"topic": "B+ tree", "audience": {"knows": ["SQL"], "new_to": ["index"]}, "duration_minutes": 45, "discussion_minutes": 10})
        self.assertFalse(errors)
        self.assertNotIn("audience", assumptions)
        self.assertNotIn("duration_minutes", assumptions)
        self.assertEqual(data["duration_minutes"], 45)

    def test_topic_cannot_be_blank(self):
        self.assertTrue(validate({"topic": " "})[1])

    def test_discussion_not_longer_than_talk(self):
        self.assertTrue(validate({"topic": "B+ tree", "duration_minutes": 20, "discussion_minutes": 20})[1])

    def test_unknown_or_wrong_type(self):
        self.assertTrue(validate({"topic": "x", "audience": "everyone"})[1])
        self.assertTrue(validate({"topic": "x", "duration_minutes": True})[1])
        self.assertTrue(validate({"topic": "x", "super_secret_field": "no"})[1])

    def test_recommended_fields(self):
        self.assertFalse(validate({"topic": "Index", "mode": "full", "privacy": "public", "sources": ["public paper"]})[1])


if __name__ == "__main__":
    unittest.main()
