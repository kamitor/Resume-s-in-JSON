#!/usr/bin/env python3
"""
Create a new job application folder with all template files.

Usage:
    python scripts/new_job.py YYYY-MM-DD_bedrijfsnaam_functie

Example:
    python scripts/new_job.py 2026-03-15_acme_innovatiemanager

Creates:
    sollicitaties/2026-03-15_acme_innovatiemanager/
        brief.qmd       — copy of _template/brief.qmd
        vacature.md     — copy of _template/vacature.md
        cv_config.yml   — copy of _template/cv_config.yml
"""

import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
TEMPLATE = ROOT / "sollicitaties" / "_template"
SOLLICITATIES = ROOT / "sollicitaties"
TRACKER = SOLLICITATIES / "tracker.yml"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/new_job.py YYYY-MM-DD_bedrijfsnaam_functie")
        print(f"Example: python scripts/new_job.py {date.today()}_bedrijf_functie")
        sys.exit(1)

    name = sys.argv[1].strip().rstrip("/")
    target = SOLLICITATIES / name

    if target.exists():
        print(f"Folder already exists: {target}")
        sys.exit(1)

    target.mkdir(parents=True)

    for fname in ("brief.qmd", "vacature.md", "cv_config.yml"):
        src = TEMPLATE / fname
        if src.exists():
            shutil.copy2(src, target / fname)

    _append_tracker(name)

    print(f"Created: {target.relative_to(ROOT)}/")
    print()
    print("Next steps:")
    print(f"  1. Fill in sollicitaties/{name}/vacature.md")
    print(f"  2. Fill in sollicitaties/{name}/brief.qmd  (bedrijf, functie, datum, brief tekst)")
    print(f"  3. Adjust sollicitaties/{name}/cv_config.yml  (optioneel)")
    print(f"  4. python scripts/build_job.py sollicitaties/{name}/")


def _append_tracker(name: str) -> None:
    """Append a concept entry to tracker.yml for the new application."""
    entry = {
        "id": name,
        "bedrijf": "",
        "functie": "",
        "datum_gevonden": str(date.today()),
        "datum_verstuurd": None,
        "salaris_range": None,
        "status": "concept",
        "gesprek_datum": None,
        "notities": "",
    }

    if TRACKER.exists():
        with open(TRACKER) as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    applications = data.get("applications", [])
    ids = [a.get("id") for a in applications]
    if name in ids:
        return  # already present

    applications.append(entry)
    data["applications"] = applications

    with open(TRACKER, "w") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"Tracker: added '{name}' to {TRACKER.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
