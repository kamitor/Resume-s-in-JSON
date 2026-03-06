#!/usr/bin/env python3
"""
Validate tracker.yml schema and data integrity.

Tests:
  1. tracker.yml exists and is valid YAML
  2. Required fields present on every entry
  3. Status values are within the allowed set
  4. IDs are unique
  5. Date fields are valid ISO dates (when not null)
"""

import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
TRACKER = ROOT / "sollicitaties" / "tracker.yml"

REQUIRED_FIELDS = {"id", "bedrijf", "functie", "datum_gevonden", "status"}
VALID_STATUSES = {"concept", "verstuurd", "gesprek", "aangeboden", "afgewezen", "geaccepteerd"}
DATE_FIELDS = {"datum_gevonden", "datum_verstuurd", "gesprek_datum"}

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)
    print(f"  FAIL: {msg}")


def check_date(value: object, label: str) -> None:
    if value is None:
        return
    try:
        date.fromisoformat(str(value))
    except ValueError:
        fail(f"{label} is not a valid ISO date: {value!r}")


print(f"Checking {TRACKER.relative_to(ROOT)} ...")

# 1. File exists and parses
if not TRACKER.exists():
    print(f"FAIL: {TRACKER} not found")
    sys.exit(1)

with open(TRACKER) as f:
    data = yaml.safe_load(f)

if not isinstance(data, dict) or "applications" not in data:
    print("FAIL: tracker.yml must have a top-level 'applications' key")
    sys.exit(1)

applications = data["applications"]
if not isinstance(applications, list):
    print("FAIL: 'applications' must be a list")
    sys.exit(1)

print(f"  Found {len(applications)} application(s)")

# 2-5. Per-entry checks
seen_ids: set[str] = set()
for i, entry in enumerate(applications):
    prefix = f"Entry #{i} (id={entry.get('id', '?')})"

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in entry:
            fail(f"{prefix}: missing required field '{field}'")

    # Unique IDs
    eid = entry.get("id")
    if eid in seen_ids:
        fail(f"{prefix}: duplicate id '{eid}'")
    seen_ids.add(eid)

    # Valid status
    status = entry.get("status")
    if status not in VALID_STATUSES:
        fail(f"{prefix}: invalid status '{status}' (must be one of {sorted(VALID_STATUSES)})")

    # Date fields
    for field in DATE_FIELDS:
        check_date(entry.get(field), f"{prefix}.{field}")

if errors:
    print(f"\n{len(errors)} error(s) found.")
    sys.exit(1)
else:
    print("  All checks passed.")
