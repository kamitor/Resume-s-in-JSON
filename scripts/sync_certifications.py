#!/usr/bin/env python3
"""
Sync confirmed certifications from profiel.yml into the rxresume base JSON.

Usage: python scripts/sync_certifications.py [--dry-run]

Reads  : profiel.yml           → certificeringen_cv
Writes : christiaan-verhoef_20260303_1718.json  → sections.certifications.items

IDs of existing items are preserved when the title matches (case-insensitive).
New items get a fresh nanoid.
"""

import copy
import json
import random
import string
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
PROFIEL = ROOT / "profiel.yml"
BASE_JSON = ROOT / "christiaan-verhoef_20260303_1718.json"


def nanoid(size: int = 25) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choices(alphabet, k=size))


def main() -> None:
    dry_run = "--dry-run" in sys.argv

    with open(PROFIEL, encoding="utf-8") as f:
        profiel = yaml.safe_load(f)

    certs_yml = profiel.get("certificeringen_cv", [])
    if not certs_yml:
        print("No 'certificeringen_cv' found in profiel.yml. Nothing to sync.")
        sys.exit(0)

    with open(BASE_JSON, encoding="utf-8") as f:
        cv = json.load(f)

    # Build a lookup of existing items by lowercase title for ID preservation
    existing = {
        item["title"].strip().lower(): item
        for item in cv["sections"]["certifications"]["items"]
    }

    new_items = []
    for cert in certs_yml:
        if isinstance(cert, str):
            cert = {"title": cert, "issuer": "", "date": ""}

        title = cert.get("title", "").strip()
        key = title.lower()

        # Preserve existing ID if the cert was already present
        existing_id = existing.get(key, {}).get("id", nanoid())

        new_items.append({
            "id": existing_id,
            "hidden": False,
            "title": title,
            "issuer": cert.get("issuer", ""),
            "date": cert.get("date", ""),
            "website": {"url": "", "label": ""},
            "description": "",
        })

    if dry_run:
        print("DRY RUN — would write these certifications to the JSON:\n")
        for item in new_items:
            issuer = f" ({item['issuer']})" if item["issuer"] else ""
            date = f" [{item['date']}]" if item["date"] else ""
            print(f"  • {item['title']}{issuer}{date}")
        print(f"\nTotal: {len(new_items)} certifications")
        return

    cv["sections"]["certifications"]["items"] = new_items

    with open(BASE_JSON, "w", encoding="utf-8") as f:
        json.dump(cv, f, ensure_ascii=False, indent=2)

    print(f"Synced {len(new_items)} certifications to {BASE_JSON.name}")
    for item in new_items:
        issuer = f" ({item['issuer']})" if item["issuer"] else ""
        print(f"  • {item['title']}{issuer}")

    print(f"\nValidate: python scripts/validate_cv.py {BASE_JSON.name}")


if __name__ == "__main__":
    main()
