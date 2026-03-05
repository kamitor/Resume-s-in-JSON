#!/usr/bin/env python3
"""
Validate a Reactive Resume JSON file against the required schema.
Usage: python scripts/validate_cv.py path/to/resume.json
"""

import json
import sys
from typing import Any

ERRORS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def check_website(obj: Any, path: str) -> None:
    if not isinstance(obj, dict):
        err(f"{path}: must be an object, got {type(obj).__name__}")
        return
    if "url" not in obj:
        err(f"{path}: missing 'url'")
    if "label" not in obj:
        err(f"{path}: missing 'label'")


def check_id(item: Any, path: str) -> None:
    if "id" not in item:
        err(f"{path}: missing 'id'")
    elif not isinstance(item["id"], str) or len(item["id"]) < 10:
        err(f"{path}.id: must be a non-empty string (nanoid format), got '{item['id']}'")


def check_section(section: Any, name: str) -> None:
    path = f"sections.{name}"
    if not isinstance(section, dict):
        err(f"{path}: must be an object")
        return
    for field in ("title", "columns", "hidden", "items"):
        if field not in section:
            err(f"{path}: missing '{field}'")
    if "items" in section and not isinstance(section["items"], list):
        err(f"{path}.items: must be an array")


def check_experience_item(item: Any, idx: int) -> None:
    path = f"sections.experience.items[{idx}]"
    check_id(item, path)
    for field in ("hidden", "company", "position", "location", "period", "description"):
        if field not in item:
            err(f"{path}: missing '{field}'")
    if "website" in item:
        check_website(item["website"], f"{path}.website")


def check_education_item(item: Any, idx: int) -> None:
    path = f"sections.education.items[{idx}]"
    check_id(item, path)
    for field in ("hidden", "school", "degree", "area", "grade", "location", "period", "description"):
        if field not in item:
            err(f"{path}: missing '{field}'")
    if "website" in item:
        check_website(item["website"], f"{path}.website")


def check_skill_item(item: Any, idx: int) -> None:
    path = f"sections.skills.items[{idx}]"
    check_id(item, path)
    for field in ("hidden", "name", "proficiency", "level", "keywords"):
        if field not in item:
            err(f"{path}: missing '{field}'")
    if "level" in item and not isinstance(item["level"], (int, float)):
        err(f"{path}.level: must be a number (0-5), got '{item['level']}'")
    if "keywords" in item and not isinstance(item["keywords"], list):
        err(f"{path}.keywords: must be an array")


def check_certification_item(item: Any, idx: int) -> None:
    path = f"sections.certifications.items[{idx}]"
    check_id(item, path)
    # Common GPT mistake: using 'name' instead of 'title'
    if "name" in item and "title" not in item:
        err(f"{path}: has 'name' but certifications use 'title' — rename it")
    for field in ("hidden", "title", "issuer", "date", "description"):
        if field not in item:
            err(f"{path}: missing '{field}'")
    if "website" in item:
        check_website(item["website"], f"{path}.website")


def check_language_item(item: Any, idx: int) -> None:
    path = f"sections.languages.items[{idx}]"
    check_id(item, path)
    for field in ("hidden", "language", "fluency", "level"):
        if field not in item:
            err(f"{path}: missing '{field}'")


def check_interest_item(item: Any, idx: int) -> None:
    path = f"sections.interests.items[{idx}]"
    check_id(item, path)
    for field in ("hidden", "name", "keywords"):
        if field not in item:
            err(f"{path}: missing '{field}'")
    if "keywords" in item and not isinstance(item["keywords"], list):
        err(f"{path}.keywords: must be an array")


def check_project_item(item: Any, idx: int) -> None:
    path = f"sections.projects.items[{idx}]"
    check_id(item, path)
    for field in ("hidden", "name", "period", "description"):
        if field not in item:
            err(f"{path}: missing '{field}'")
    if "website" in item:
        check_website(item["website"], f"{path}.website")


SECTION_CHECKERS = {
    "experience": check_experience_item,
    "education": check_education_item,
    "skills": check_skill_item,
    "certifications": check_certification_item,
    "languages": check_language_item,
    "interests": check_interest_item,
    "projects": check_project_item,
}


def validate(data: Any) -> None:
    if not isinstance(data, dict):
        err("Root: must be a JSON object")
        return

    # Top-level keys
    for key in ("picture", "basics", "summary", "sections", "customSections", "metadata"):
        if key not in data:
            err(f"Root: missing top-level key '{key}'")

    # customSections must be array
    if "customSections" in data and not isinstance(data["customSections"], list):
        err("customSections: must be an array (even if empty: [])")

    # basics
    if "basics" in data:
        b = data["basics"]
        for field in ("name", "headline", "email", "phone", "location", "website", "customFields"):
            if field not in b:
                err(f"basics: missing '{field}'")
        if "website" in b:
            check_website(b["website"], "basics.website")
        if "customFields" in b and not isinstance(b["customFields"], list):
            err("basics.customFields: must be an array")

    # summary
    if "summary" in data:
        s = data["summary"]
        for field in ("title", "columns", "hidden", "content"):
            if field not in s:
                err(f"summary: missing '{field}'")

    # sections
    if "sections" in data:
        sections = data["sections"]
        if not isinstance(sections, dict):
            err("sections: must be an object")
        else:
            required_sections = [
                "profiles", "experience", "education", "projects",
                "skills", "languages", "interests", "awards",
                "certifications", "publications", "volunteer", "references"
            ]
            for sec in required_sections:
                if sec not in sections:
                    err(f"sections: missing section '{sec}'")

            for sec_name, checker in SECTION_CHECKERS.items():
                if sec_name in sections:
                    check_section(sections[sec_name], sec_name)
                    items = sections[sec_name].get("items", [])
                    if isinstance(items, list):
                        for i, item in enumerate(items):
                            checker(item, i)

    # metadata
    if "metadata" in data:
        m = data["metadata"]
        for field in ("template", "layout", "css", "page", "design", "typography"):
            if field not in m:
                err(f"metadata: missing '{field}'")
        if "page" in m:
            for field in ("format", "marginX", "marginY"):
                if field not in m["page"]:
                    err(f"metadata.page: missing '{field}'")
        if "design" in m and "colors" in m["design"]:
            for field in ("primary", "text", "background"):
                if field not in m["design"]["colors"]:
                    err(f"metadata.design.colors: missing '{field}'")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_cv.py path/to/resume.json")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"INVALID JSON: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(1)

    validate(data)

    if ERRORS:
        print(f"FAILED — {len(ERRORS)} error(s) found:\n")
        for e in ERRORS:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("OK — JSON is valid and ready to import into Reactive Resume.")


if __name__ == "__main__":
    main()
