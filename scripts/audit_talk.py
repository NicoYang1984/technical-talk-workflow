#!/usr/bin/env python3
"""Audit content anchors, local visuals, and obviously risky speaking-time estimates.

Usage:
  python scripts/audit_talk.py --outline outline.json --projection projection.md --notes speaker_notes.md [--visuals visuals.json]

This is a conservative lint, NOT semantic proof or a substitute for viewing the PDF.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from check_alignment import headings, check as check_alignment

SPOKEN = re.compile(r"<!--\s*SPOKEN START\s*-->(.*?)<!--\s*SPOKEN END\s*-->", re.DOTALL | re.IGNORECASE)
CJK = re.compile(r"[\u3400-\u9fff]")


def split_sections(path: Path, expected_sections: list[dict]) -> dict[str, str]:
    """Map visible natural headings to internal outline IDs by validated order."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    entries = headings(path)
    result: dict[str, str] = {}
    for idx, (_, _title, line_number) in enumerate(entries[:len(expected_sections)]):
        end = entries[idx + 1][2] - 1 if idx + 1 < len(entries) else len(lines)
        result[expected_sections[idx]["id"]] = "\n".join(lines[line_number:end])
    return result


def audit(outline: Path, projection: Path, notes: Path, visuals: Path | None = None,
          cjk_chars_per_minute: int = 220, warning_threshold: float = 1.5) -> tuple[list[str], list[str]]:
    errors = check_alignment(outline, projection, notes)
    warnings = []
    if errors:
        return errors, warnings

    data = json.loads(outline.read_text(encoding="utf-8-sig"))
    projected = split_sections(projection, data["sections"])
    spoken = split_sections(notes, data["sections"])
    manifest_by_id: dict[str, dict] = {}
    if visuals:
        media = json.loads(visuals.read_text(encoding="utf-8-sig"))
        entries = media.get("visuals", [])
        if not isinstance(entries, list):
            errors.append("visuals.json: 'visuals' must be a list")
        else:
            for v in entries:
                if not isinstance(v, dict) or not v.get("id"):
                    errors.append("visuals.json: each entry requires a nonempty 'id'")
                    continue
                if v["id"] in manifest_by_id:
                    errors.append(f"visuals.json: duplicate id '{v['id']}'")
                manifest_by_id[v["id"]] = v
                for key in ["source_path", "fallback_path"]:
                    loc = v.get(key)
                    if not loc:
                        errors.append(f"visual {v['id']}: missing {key}")
                    elif not (visuals.parent / str(loc)).is_file():
                        errors.append(f"visual {v['id']}: {key} not found at '{loc}'")
                if not v.get("rendered_ok", False):
                    warnings.append(f"visual {v['id']}: final rendered appearance not yet verified")

    for section in data["sections"]:
        sid = section["id"]
        a = section.get("anchors", {})
        if not isinstance(a, dict):
            errors.append(f"{sid}: anchors must be an object")
            a = {}
        for side, text in (("projection", projected.get(sid, "")), ("notes", spoken.get(sid, ""))):
            anchors = a.get(side, []) + a.get("both", [])
            if not isinstance(anchors, list):
                errors.append(f"{sid}: anchors.{side} must be a list")
                continue
            for anchor in anchors:
                if not isinstance(anchor, str) or not anchor.strip():
                    errors.append(f"{sid}: empty/non-string anchor for {side}")
                elif anchor not in text:
                    errors.append(f"{sid}: {side} missing exact anchor {anchor!r}")
        vi = section.get("visual_id")
        if vi and visuals and vi not in manifest_by_id:
            errors.append(f"{sid}: visual_id '{vi}' is not in the manifest")
        if section.get("deep_dive") and float(section.get("minutes", 0)) < 4:
            warnings.append(f"{sid}: deep_dive planned for <4 minutes, rehearse its actual duration")

        # Only count explicitly delimited words actually intended to be spoken.
        passages = SPOKEN.findall(spoken.get(sid, ""))
        if passages:
            cjk_count = len(CJK.findall(" ".join(passages)))
            budget = float(section.get("minutes", 0)) * cjk_chars_per_minute
            if cjk_count > budget * warning_threshold:
                warnings.append(
                    f"{sid}: {cjk_count} CJK speaking chars vs ~{budget:.0f} budget; "
                    "may run long (excludes math/interaction overhead)"
                )

    return errors, warnings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--outline", type=Path, required=True)
    ap.add_argument("--projection", type=Path, required=True)
    ap.add_argument("--notes", type=Path, required=True)
    ap.add_argument("--visuals", type=Path)
    ap.add_argument("--cjk-chars-per-minute", type=int, default=220)
    ap.add_argument("--warning-threshold", type=float, default=1.5)
    ap.add_argument("--strict-warnings", action="store_true")
    args = ap.parse_args(argv)
    try:
        errors, warnings = audit(args.outline, args.projection, args.notes,
                                  args.visuals, args.cjk_chars_per_minute,
                                  args.warning_threshold)
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as ex:
        print("ERROR:", ex, file=sys.stderr)
        return 2
    for item in errors:
        print("ERROR:", item, file=sys.stderr)
    for item in warnings:
        print("WARN:", item)
    if errors or (args.strict_warnings and warnings):
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: no structural/content errors ({len(warnings)} advisory warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
