#!/usr/bin/env python3
"""
Generate a job-tailored Reactive Resume JSON from the base CV and a job config YAML.

Usage:
    python scripts/generate_cv.py job_config.yml [--output output.json]

The base CV is always christiaan-verhoef_20260303_1718.json
The job config controls what to show, hide, reorder, or rewrite.
"""

import copy
import json
import random
import string
import sys
from pathlib import Path
import argparse

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

BASE_JSON = Path(__file__).parent.parent / "christiaan-verhoef_20260303_1718.json"


def nanoid(size: int = 25) -> str:
    """Generate a nanoid-style alphanumeric ID matching rxresume's format."""
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choices(alphabet, k=size))


def load_base() -> dict:
    with open(BASE_JSON, encoding="utf-8") as f:
        return json.load(f)


def apply_config(cv: dict, config: dict) -> dict:
    """Apply job config overrides to the base CV."""

    # --- basics ---
    if headline := config.get("headline"):
        cv["basics"]["headline"] = headline

    # --- summary ---
    if summary := config.get("summary"):
        # Accept plain text or HTML; wrap plain text in <p> tags
        if not summary.strip().startswith("<"):
            summary = "<p>" + "</p><p>".join(summary.strip().split("\n\n")) + "</p>"
        cv["summary"]["content"] = summary

    # --- hide experience items by company name ---
    if hide_companies := config.get("hide_experience", []):
        hide_lower = [h.lower() for h in hide_companies]
        for item in cv["sections"]["experience"]["items"]:
            if item.get("company", "").lower() in hide_lower:
                item["hidden"] = True

    # --- show only specific experience items (hides all others) ---
    if show_companies := config.get("show_experience", []):
        show_lower = [s.lower() for s in show_companies]
        for item in cv["sections"]["experience"]["items"]:
            item["hidden"] = item.get("company", "").lower() not in show_lower

    # --- reorder skills: listed skills go first, rest follow ---
    if priority_skills := config.get("priority_skills", []):
        priority_lower = [s.lower() for s in priority_skills]
        skills = cv["sections"]["skills"]["items"]
        ordered = sorted(
            skills,
            key=lambda s: priority_lower.index(s["name"].strip().lower())
            if s["name"].strip().lower() in priority_lower
            else len(priority_lower) + 1,
        )
        cv["sections"]["skills"]["items"] = ordered

    # --- hide skills by name ---
    if hide_skills := config.get("hide_skills", []):
        hide_lower = [h.lower() for h in hide_skills]
        for item in cv["sections"]["skills"]["items"]:
            if item["name"].strip().lower() in hide_lower:
                item["hidden"] = True

    # --- override certifications (replaces the certifications section entirely) ---
    if certs := config.get("certifications", []):
        cv["sections"]["certifications"]["items"] = [
            {
                "id": nanoid(),
                "hidden": False,
                "title": cert if isinstance(cert, str) else cert.get("title", ""),
                "issuer": cert.get("issuer", "") if isinstance(cert, dict) else "",
                "date": cert.get("date", "") if isinstance(cert, dict) else "",
                "website": {"url": "", "label": ""},
                "description": "",
            }
            for cert in certs
        ]

    # --- hide project items by name ---
    if hide_projects := config.get("hide_projects", []):
        hide_lower = [h.lower() for h in hide_projects]
        for item in cv["sections"]["projects"]["items"]:
            if item.get("name", "").lower() in hide_lower:
                item["hidden"] = True

    # --- show only specific projects ---
    if show_projects := config.get("show_projects", []):
        show_lower = [s.lower() for s in show_projects]
        for item in cv["sections"]["projects"]["items"]:
            item["hidden"] = item.get("name", "").lower() not in show_lower

    # --- metadata overrides ---
    if template := config.get("template"):
        cv["metadata"]["template"] = template

    return cv


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a tailored rxresume JSON.")
    parser.add_argument("config", help="Path to job config YAML file")
    parser.add_argument("--output", "-o", help="Output JSON path (default: stdout)")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    cv = load_base()
    cv = apply_config(copy.deepcopy(cv), config)

    output = json.dumps(cv, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Written to {args.output}")
        print(f"Validate with: python scripts/validate_cv.py {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
