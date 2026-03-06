#!/usr/bin/env python3
"""
Validate profiel.yml — single source of truth for all letters and the CV.

Checks:
  1. File exists and is valid YAML
  2. Required personal fields are present and non-empty
  3. certificeringen_cv: each entry has a non-empty 'title'
  4. certificeringen (short list for badge): non-empty strings
  5. No duplicate titles in certificeringen_cv
  6. Email looks like an email address
  7. Telefoon is non-empty

Usage:
    python scripts/validate_profiel.py
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
PROFIEL = ROOT / "profiel.yml"

REQUIRED_FIELDS = ["naam", "email", "telefoon", "stad"]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"  FAIL: {msg}")


print(f"Checking {PROFIEL.relative_to(ROOT)} ...")

if not PROFIEL.exists():
    print(f"FAIL: {PROFIEL} not found")
    sys.exit(1)

with open(PROFIEL) as f:
    data = yaml.safe_load(f)

if not isinstance(data, dict):
    print("FAIL: profiel.yml must be a YAML mapping")
    sys.exit(1)

# 1. Required personal fields
for field in REQUIRED_FIELDS:
    value = data.get(field)
    if not value or not str(value).strip():
        fail(f"Required field '{field}' is missing or empty")

# 2. Email format
email = data.get("email", "")
if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    fail(f"'email' does not look like a valid address: {email!r}")

# 3. certificeringen_cv
cv_certs = data.get("certificeringen_cv", [])
if not isinstance(cv_certs, list):
    fail("'certificeringen_cv' must be a list")
else:
    titles_seen: set[str] = set()
    for i, cert in enumerate(cv_certs):
        if not isinstance(cert, dict):
            fail(f"certificeringen_cv[{i}] must be a mapping (has 'title', 'issuer', 'date')")
            continue
        title = cert.get("title")
        if not title or not str(title).strip():
            fail(f"certificeringen_cv[{i}] is missing a non-empty 'title'")
            continue
        if title in titles_seen:
            fail(f"Duplicate certification title: {title!r}")
        titles_seen.add(title)

# 4. certificeringen (short badge list)
badge_certs = data.get("certificeringen", [])
if not isinstance(badge_certs, list):
    fail("'certificeringen' must be a list")
else:
    for i, cert in enumerate(badge_certs):
        if not cert or not str(cert).strip():
            fail(f"certificeringen[{i}] is empty")

if errors:
    print(f"\n{len(errors)} error(s) found in profiel.yml.")
    sys.exit(1)
else:
    fields_ok = ", ".join(REQUIRED_FIELDS)
    print(f"  Required fields OK: {fields_ok}")
    print(f"  certificeringen_cv: {len(cv_certs)} entry/entries")
    print(f"  certificeringen (badges): {len(badge_certs)} entry/entries")
    print("  All checks passed.")
