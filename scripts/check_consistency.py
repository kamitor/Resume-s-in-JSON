#!/usr/bin/env python3
"""
Cross-check sollicitaties/ folders against tracker.yml.

Reports:
  - Application folders with no tracker entry
  - Tracker entries with no matching folder
  - Application folders missing required files (brief.qmd, vacature.md)

Usage:
    python scripts/check_consistency.py [--fix]

  --fix   Auto-add missing tracker entries (status: concept) for folders
          that exist but are not yet tracked. Does not delete entries.

Exit code: 0 = all OK, 1 = issues found.
"""

import sys
import argparse
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
SOLLICITATIES = ROOT / "sollicitaties"
TRACKER = SOLLICITATIES / "tracker.yml"
REQUIRED_FILES = ["brief.qmd", "vacature.md"]
IGNORE_DIRS = {"_template"}


def load_tracker() -> tuple[dict, list[dict]]:
    if not TRACKER.exists():
        return {}, []
    with open(TRACKER) as f:
        data = yaml.safe_load(f) or {}
    return data, data.get("applications", [])


def get_application_folders() -> list[Path]:
    return sorted(
        d for d in SOLLICITATIES.iterdir()
        if d.is_dir() and d.name not in IGNORE_DIRS and not d.name.startswith(".")
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-check tracker.yml vs sollicitaties/ folders")
    parser.add_argument("--fix", action="store_true", help="Auto-add missing tracker entries")
    args = parser.parse_args()

    data, applications = load_tracker()
    folders = get_application_folders()

    tracked_ids = {a["id"] for a in applications}
    folder_names = {f.name for f in folders}

    issues: list[str] = []
    warnings: list[str] = []

    # 1. Folders not in tracker
    untracked = folder_names - tracked_ids
    for name in sorted(untracked):
        issues.append(f"Folder not in tracker: sollicitaties/{name}/")

    # 2. Tracker entries with no folder
    orphaned = tracked_ids - folder_names
    for eid in sorted(orphaned):
        issues.append(f"Tracker entry has no folder: {eid}")

    # 3. Required files per folder
    for folder in folders:
        for fname in REQUIRED_FILES:
            if not (folder / fname).exists():
                warnings.append(f"Missing {fname}: sollicitaties/{folder.name}/")

    # Print results
    print(f"Folders found:  {len(folders)}")
    print(f"Tracker entries: {len(applications)}")
    print()

    if not issues and not warnings:
        print("All OK — tracker and folders are in sync.")
        return 0

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
        print()

    if issues:
        print(f"ISSUES ({len(issues)}):")
        for issue in issues:
            print(f"  x {issue}")
        print()

    # Auto-fix: add missing tracker entries for untracked folders
    if args.fix and untracked:
        for name in sorted(untracked):
            new_entry = {
                "id": name,
                "bedrijf": "",
                "functie": "",
                "datum_gevonden": str(date.today()),
                "datum_verstuurd": None,
                "salaris_range": None,
                "status": "concept",
                "gesprek_datum": None,
                "notities": "Auto-added by check_consistency.py",
            }
            applications.append(new_entry)
            print(f"  Added tracker entry: {name}")

        data["applications"] = applications
        with open(TRACKER, "w") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        print(f"\ntracker.yml updated ({len(untracked)} entr(y/ies) added).")

        # Only orphaned entries (no folder) are still real issues
        return 1 if orphaned else 0

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
