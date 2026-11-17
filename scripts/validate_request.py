#!/usr/bin/env python3
"""Lightweight input validator (standard library only). Prints explicitly assumed defaults.

Usage: python scripts/validate_request.py assets/talk-request-minimal.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULTS = {
    "mode": "full",
    "audience": {"role": "software/ML engineering audience (assumed)", "knows": ["basic programming"], "new_to": ["the requested topic"]},
    "duration_minutes": 30,
    "discussion_minutes": 5,
    "learning_outcome": "Explain one mechanism, trace one example, name one trade-off",
    "delivery_platform": "Markdown",
    "depth": "intro-to-engineering",
    "language": "zh-CN",
    "offline_required": True,
    "demo_available": False,
    "privacy": "private",
}
VALID_MODES = {"outline", "test", "full", "repair"}
VALID_DEPTHS = {"intro", "intro-to-engineering", "deep-dive"}
VALID_PRIVACY = {"private", "internal", "public"}
KNOWN_KEYS = set(DEFAULTS) | {"topic", "sources", "focus", "excluded_topics"}


def validate(request: dict) -> tuple[dict, list[str], list[str]]:
    if not isinstance(request, dict):
        return {}, ["Request must be a JSON object"], []
    errors: list[str] = []
    assumed: list[str] = []
    extra = sorted(set(request) - KNOWN_KEYS)
    if extra:
        errors.append("Unknown fields: " + ", ".join(extra))
    topic = request.get("topic")
    if not isinstance(topic, str) or not topic.strip():
        errors.append("A non-empty topic is required")
    payload = dict(request)
    for key, default in DEFAULTS.items():
        if key not in payload:
            payload[key] = default
            assumed.append(key)
    for key, allowed in [("mode", VALID_MODES), ("depth", VALID_DEPTHS), ("privacy", VALID_PRIVACY)]:
        if not isinstance(payload.get(key), str) or payload[key] not in allowed:
            errors.append(f"Invalid {key}: {payload.get(key)!r}")
    for key, min_v, max_v in [("duration_minutes", 10, 240), ("discussion_minutes", 0, 120)]:
        value = payload.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or not min_v <= value <= max_v:
            errors.append(f"{key} must be integer in [{min_v}, {max_v}]")
    if isinstance(payload.get("duration_minutes"), int) and isinstance(payload.get("discussion_minutes"), int):
        if payload["discussion_minutes"] >= payload["duration_minutes"]:
            errors.append("discussion_minutes must be less than duration_minutes")
    audience = payload.get("audience")
    if not isinstance(audience, dict):
        errors.append("audience must be an object")
    else:
        for key in ("knows", "new_to"):
            if key in audience and (not isinstance(audience[key], list) or any(not isinstance(x, str) for x in audience[key])):
                errors.append(f"audience.{key} must be a list of strings")
        if "role" in audience and not isinstance(audience["role"], str):
            errors.append("audience.role must be a string")
    for key in ("sources", "focus", "excluded_topics"):
        val = payload.get(key, [])
        if not isinstance(val, list) or any(not isinstance(v, str) for v in val):
            errors.append(f"{key} must be a list of strings")
    for key in ("learning_outcome", "delivery_platform", "language"):
        if not isinstance(payload.get(key), str):
            errors.append(f"{key} must be a string")
    for key in ("demo_available", "offline_required"):
        if not isinstance(payload.get(key), bool):
            errors.append(f"{key} must be boolean")
    if not errors:
        payload["topic"] = payload["topic"].strip()
    return payload, errors, assumed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("--strict", action="store_true", help="reject missing recommended audience/duration")
    args = parser.parse_args()
    try:
        obj = json.loads(args.request.read_text(encoding="utf-8"))
    except (OSError, ValueError) as err:
        print("ERROR:", err)
        return 2
    payload, errors, assumptions = validate(obj)
    if args.strict and {"audience", "duration_minutes"}.intersection(assumptions):
        errors.append("--strict requires audience and duration_minutes")
    if errors:
        print("FAIL:", "; ".join(errors))
        return 1
    print("PASS:", payload["topic"])
    print(f"TALK: {payload['duration_minutes']} min incl {payload['discussion_minutes']} min discussion; mode={payload['mode']}")
    if assumptions:
        print("ASSUMED DEFAULTS:", ", ".join(assumptions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
