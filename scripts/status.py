#!/usr/bin/env python3
"""
Quickly update application status in tracker.yml.

Usage:
    # Update status (and optionally record a date)
    python scripts/status.py 2026-03-03_bedrijf_functie verstuurd
    python scripts/status.py 2026-03-03_bedrijf_functie gesprek --datum 2026-04-01
    python scripts/status.py 2026-03-03_bedrijf_functie verstuurd --notities "Via LinkedIn verstuurd"

    # List all applications
    python scripts/status.py --list

Status transitions:
    concept → verstuurd → gesprek → aangeboden → afgewezen / geaccepteerd

Date fields set automatically per status (unless --datum overrides):
    verstuurd   → datum_verstuurd = today
    gesprek     → gesprek_datum = today
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
TRACKER = ROOT / "sollicitaties" / "tracker.yml"

VALID_STATUSES = ["concept", "verstuurd", "gesprek", "aangeboden", "afgewezen", "geaccepteerd"]

STATUS_DATE_FIELD = {
    "verstuurd": "datum_verstuurd",
    "gesprek": "gesprek_datum",
}

STATUS_COLORS = {
    "concept":      "\033[90m",   # grey
    "verstuurd":    "\033[34m",   # blue
    "gesprek":      "\033[33m",   # yellow
    "aangeboden":   "\033[35m",   # magenta
    "afgewezen":    "\033[31m",   # red
    "geaccepteerd": "\033[32m",   # green
}
RESET = "\033[0m"


def load() -> tuple[dict, list[dict]]:
    if not TRACKER.exists():
        print(f"tracker.yml not found: {TRACKER}", file=sys.stderr)
        sys.exit(1)
    with open(TRACKER) as f:
        data = yaml.safe_load(f) or {}
    return data, data.get("applications", [])


def save(data: dict, applications: list[dict]) -> None:
    data["applications"] = applications
    with open(TRACKER, "w") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def find_entry(applications: list[dict], app_id: str) -> dict | None:
    # Exact match first, then substring
    for a in applications:
        if a["id"] == app_id:
            return a
    matches = [a for a in applications if app_id in a["id"]]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"Ambiguous ID '{app_id}', matches:", file=sys.stderr)
        for m in matches:
            print(f"  {m['id']}", file=sys.stderr)
        sys.exit(1)
    return None


def cmd_list(applications: list[dict]) -> None:
    if not applications:
        print("No applications tracked yet.")
        return
    width = max(len(a["id"]) for a in applications)
    print(f"{'ID':<{width}}  {'Status':<12}  {'Bedrijf'}")
    print("-" * (width + 30))
    for a in sorted(applications, key=lambda x: x.get("datum_gevonden") or ""):
        color = STATUS_COLORS.get(a["status"], "")
        status_str = f"{color}{a['status']:<12}{RESET}"
        bedrijf = a.get("bedrijf") or "—"
        functie = a.get("functie") or "—"
        print(f"{a['id']:<{width}}  {status_str}  {bedrijf} — {functie}")


def cmd_update(applications: list[dict], app_id: str, new_status: str,
               datum: str | None, notities: str | None) -> dict:
    entry = find_entry(applications, app_id)
    if entry is None:
        print(f"No application found for '{app_id}'", file=sys.stderr)
        sys.exit(1)

    old_status = entry["status"]
    entry["status"] = new_status

    # Auto-set date field for this status
    date_field = STATUS_DATE_FIELD.get(new_status)
    if date_field:
        entry[date_field] = datum or str(date.today())

    # Manual notities append
    if notities:
        existing = entry.get("notities") or ""
        entry["notities"] = (existing.strip() + "\n" + notities).strip() if existing else notities

    print(f"{entry['id']}")
    print(f"  {old_status}  →  {STATUS_COLORS.get(new_status,'')}{new_status}{RESET}")
    if date_field:
        print(f"  {date_field}: {entry[date_field]}")
    if notities:
        print(f"  notities: {entry['notities']}")

    return entry


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update application status in tracker.yml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("id", nargs="?", help="Application ID (or substring)")
    parser.add_argument("status", nargs="?", choices=VALID_STATUSES, help="New status")
    parser.add_argument("--datum", help="Date to record (YYYY-MM-DD, default: today)")
    parser.add_argument("--notities", help="Append a note to this application")
    parser.add_argument("--list", "-l", action="store_true", help="List all applications")
    args = parser.parse_args()

    data, applications = load()

    if args.list or (not args.id and not args.status):
        cmd_list(applications)
        return

    if not args.id or not args.status:
        parser.print_help()
        sys.exit(1)

    cmd_update(applications, args.id, args.status, args.datum, args.notities)
    save(data, applications)


if __name__ == "__main__":
    main()
