#!/usr/bin/env python3
"""
Build all outputs for a job application folder.

Usage:
    python scripts/build_job.py sollicitaties/YYYY-MM-DD_bedrijf_functie/

What it does:
    1. Reads cv_config.yml from the folder (if present)
    2. Generates cv.json  — tailored rxresume JSON, ready to import
    3. Validates cv.json  — fails loud if anything is wrong
    4. Renders brief.pdf  — via quarto render (requires Quarto + XeLaTeX)

Outputs in the job folder:
    cv.json     → import this into rxresume to generate the CV PDF
    brief.pdf   → the cover letter
"""

import copy
import json
import random
import string
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

ROOT = Path(__file__).parent.parent
BASE_JSON = ROOT / "christiaan-verhoef_20260303_1718.json"

# Import shared logic from generate_cv and validate_cv
sys.path.insert(0, str(Path(__file__).parent))
from generate_cv import apply_config, load_base  # noqa: E402
from validate_cv import validate, ERRORS          # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_job.py sollicitaties/YYYY-MM-DD_bedrijf_functie/")
        sys.exit(1)

    job_dir = Path(sys.argv[1]).resolve()
    if not job_dir.is_dir():
        print(f"Not a directory: {job_dir}")
        sys.exit(1)

    cv_config_path = job_dir / "cv_config.yml"
    brief_qmd = job_dir / "brief.qmd"
    cv_json_out = job_dir / "cv.json"

    # ---- 1. Load config ----
    config = {}
    if cv_config_path.exists():
        with open(cv_config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        print(f"Using config: {cv_config_path.relative_to(ROOT)}")
    else:
        print("No cv_config.yml found — using base CV without changes.")

    # ---- 2. Generate cv.json ----
    cv = apply_config(copy.deepcopy(load_base()), config)

    with open(cv_json_out, "w", encoding="utf-8") as f:
        json.dump(cv, f, ensure_ascii=False, indent=2)
    print(f"Generated: {cv_json_out.relative_to(ROOT)}")

    # ---- 3. Validate cv.json ----
    validate(cv)
    if ERRORS:
        print(f"\nVALIDATION FAILED — {len(ERRORS)} error(s):")
        for e in ERRORS:
            print(f"  ✗ {e}")
        sys.exit(1)
    print("Validated: cv.json OK")

    # ---- 4. Render brief.pdf ----
    if not brief_qmd.exists():
        print(f"\nNo brief.qmd found in {job_dir.name} — skipping letter render.")
    else:
        print(f"Rendering: {brief_qmd.relative_to(ROOT)}")
        result = subprocess.run(
            ["quarto", "render", str(brief_qmd)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("\nQuarto render FAILED:")
            print(result.stderr)
            sys.exit(1)

        brief_pdf = job_dir / "brief.pdf"
        if brief_pdf.exists():
            print(f"Rendered: {brief_pdf.relative_to(ROOT)}")
        else:
            print("WARNING: quarto exited 0 but brief.pdf not found.")

    # ---- Done ----
    print()
    print("Done!")
    print(f"  cv.json   → import into rxresume at http://localhost:3000")
    print(f"  brief.pdf → {(job_dir / 'brief.pdf').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
