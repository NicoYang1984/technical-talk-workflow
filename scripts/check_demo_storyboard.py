#!/usr/bin/env python3
"""Validate a step-by-step demo storyboard and its static fallback file.

Examples:
  python scripts/check_demo_storyboard.py assets/demo-storyboard-template.json --allow-template
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

LEVELS = {"illustrative", "derived", "source-backed", "measured"}
REQUIRED = ["demo_id", "section_id", "question", "input_state", "change_one_thing", "predict", "steps", "reveal", "mechanism", "boundary", "fallback", "evidence_level"]


def check_storyboard(path: Path, allow_template: bool = False) -> list[str]:
    try:
        d = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return [f"Cannot load storyboard: {exc}"]
    if not isinstance(d, dict):
        return ["Story board must be a JSON object"]
    errors: list[str] = []
    for field in REQUIRED:
        if not d.get(field):
            errors.append(f"Missing {field}")
    if d.get("evidence_level") not in LEVELS:
        errors.append("evidence_level must be illustrative, derived, source-backed, or measured")
    if not isinstance(d.get("input_state"), dict):
        errors.append("input_state must be an object")
    steps = d.get("steps")
    if not isinstance(steps, list) or len(steps) < 2:
        errors.append("steps must have at least two frames")
    else:
        for i, st in enumerate(steps):
            if not isinstance(st, dict) or not all(st.get(k) for k in ["highlight", "narration", "expected_state"]):
                errors.append(f"step {i+1} requires highlight, narration and expected_state")
    fallback = d.get("fallback")
    if isinstance(fallback, str) and fallback and not allow_template and not (path.parent / fallback).is_file():
        errors.append(f"Fallback missing: {fallback}")
    if d.get("evidence_level") == "measured" and not d.get("measurement_source"):
        errors.append("Measured demos must include measurement_source")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("storyboard", type=Path)
    p.add_argument("--allow-template", action="store_true")
    a = p.parse_args()
    errors = check_storyboard(a.storyboard, a.allow_template)
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: storyboard fields and fallback checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
