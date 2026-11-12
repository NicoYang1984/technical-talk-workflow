#!/usr/bin/env python3
"""Check that a talk's projection and speaker notes share outline IDs/titles/order.

Usage:
    python check_alignment.py --outline outline.json --projection projection.md --notes speaker_notes.md

Standard library only. Exit 0 on structural alignment, 1 on failure.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^\s{0,3}#{1,6}\s+\[(P\d{2,3})\]\s*(.*?)\s*$")


def headings(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    result = []
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        match = HEADING.match(line)
        if match:
            result.append((match.group(1), match.group(2).strip(), number))
    return result


def check(outline: Path, projection: Path, notes: Path):
    errors = []
    data = json.loads(outline.read_text(encoding="utf-8-sig"))
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        return ["outline.json requires a nonempty 'sections' list"]

    expected = []
    times = 0.0
    talk_times = 0.0
    discussion_times = 0.0
    tagged_discussion = False
    for idx, s in enumerate(sections):
        ident = str(s.get("id", ""))
        title = str(s.get("title", "")).strip()
        if not re.fullmatch(r"P\d{2,3}", ident):
            errors.append(f"outline section {idx}: invalid id {ident!r}")
        if not title:
            errors.append(f"outline section {idx}: empty title")
        try:
            minutes = float(s.get("minutes", 0))
            if minutes <= 0:
                raise ValueError
        except (ValueError, TypeError):
            errors.append(f"outline section {idx}: minutes must be > 0")
            minutes = 0
        times += minutes
        kind = s.get("kind", "talk")
        if kind == "discussion":
            tagged_discussion = True
            discussion_times += minutes
        elif kind == "talk":
            talk_times += minutes
        else:
            errors.append(f"outline section {idx}: kind must be talk or discussion")
        expected.append((ident, title))

    if len(set(x[0] for x in expected)) != len(expected):
        errors.append("outline contains duplicate section ids")
    for label, path in [("projection", projection), ("speaker notes", notes)]:
        actual = headings(path)
        ids = [x[0] for x in actual]
        if len(ids) != len(set(ids)):
            errors.append(f"{label}: duplicate section ids")
        if len(actual) != len(expected):
            errors.append(f"{label}: found {len(actual)} sections, expected {len(expected)}")
        for index in range(max(len(expected), len(actual))):
            if index >= len(expected):
                errors.append(f"{label}: unexpected section {actual[index][0]} at line {actual[index][2]}")
                continue
            if index >= len(actual):
                errors.append(f"{label}: missing {expected[index][0]} {expected[index][1]!r}")
                continue
            id_found, title_found, line = actual[index]
            id_exp, title_exp = expected[index]
            if (id_found, title_found) != (id_exp, title_exp):
                errors.append(
                    f"{label} line {line}: expected '[{id_exp}] {title_exp}', "
                    f"found '[{id_found}] {title_found}'"
                )

    talk = data.get("talk_minutes")
    duration = data.get("duration_minutes")
    discussion = data.get("discussion_minutes", 0)
    try:
        talk = float(talk)
        duration = float(duration)
        discussion = float(discussion)
    except (ValueError, TypeError):
        errors.append("outline must provide numeric talk_minutes, duration_minutes and discussion_minutes")
    else:
        if tagged_discussion:
            if abs(talk_times - talk) > 0.01:
                errors.append(f"talk section minutes sum to {talk_times:g}, but talk_minutes={talk:g}")
            if abs(discussion_times - discussion) > 0.01:
                errors.append(f"discussion section minutes sum to {discussion_times:g}, but discussion_minutes={discussion:g}")
            if abs(times - duration) > 0.01:
                errors.append(f"all section minutes sum to {times:g}, but duration_minutes={duration:g}")
        else:
            if abs(times - talk) > 0.01:
                errors.append(f"section minutes sum to {times:g}, but talk_minutes={talk:g}")
        if abs((talk + discussion) - duration) > 0.01:
            errors.append(f"talk+discussion={talk + discussion:g}, but duration_minutes={duration:g}")
    return errors


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outline", type=Path, required=True)
    p.add_argument("--projection", type=Path, required=True)
    p.add_argument("--notes", type=Path, required=True)
    a = p.parse_args(argv)
    try:
        errors = check(a.outline, a.projection, a.notes)
    except (OSError, json.JSONDecodeError) as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        print(f"Alignment failed ({len(errors)} issue(s)).", file=sys.stderr)
        return 1
    print("PASS: projection, speaker notes, and outline have identical section IDs/titles/order and valid time budgets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
