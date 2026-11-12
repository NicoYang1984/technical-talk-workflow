#!/usr/bin/env python3
"""Conservative pre-publication secret/PII pattern scan (not a complete DLP tool)."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

PATTERNS = {
    "token_like": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{28,}|github_pat_[A-Za-z0-9_]{35,}|sk-[A-Za-z0-9_-]{24,}|AKIA[0-9A-Z]{16})\b"),
    "private_key_marker": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential_assignment": re.compile(r"(?:password|access[_-]?key[_-]?secret|api[_-]?key|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_!-]{12,}", re.IGNORECASE),
}
TEXT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".csv", ".sh", ".toml"}
IGNORED = {".git", "__pycache__", ".venv", "node_modules", ".pytest_cache"}


def scan(root: Path) -> list[tuple[str, int, str]]:
    findings = []
    sources = [root] if root.is_file() else sorted(root.rglob("*"))
    for p in sources:
        if not p.is_file() or p.suffix not in TEXT_EXTENSIONS or any(x in IGNORED for x in p.parts):
            continue
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except (UnicodeError, OSError):
            continue
        for line_no, line in enumerate(lines, 1):
            for name, regex in PATTERNS.items():
                if regex.search(line):
                    findings.append((str(p.relative_to(root) if root.is_dir() else p.name), line_no, name))
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path, help="File or repository folder")
    a = ap.parse_args(argv)
    if not a.path.exists():
        print("ERROR: path not found", file=sys.stderr)
        return 2
    issues = scan(a.path)
    for p, line, name in issues:
        print(f"RISK: {p}:{line} [{name}] (value not printed)")
    print(f"Scan finished: {len(issues)} potential secret(s). Manual privacy/copyright review is still required.")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
