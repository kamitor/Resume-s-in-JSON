#!/usr/bin/env python3
"""
Import a CV JSON into a local Reactive Resume instance.

Usage:
    python scripts/rxresume_import.py [path/to/cv.json]

Defaults to christiaan-verhoef_20260303_1718.json if no path given.

Requires a running rxresume instance at http://localhost:3000.
Set RXRESUME_EMAIL and RXRESUME_PASSWORD env vars, or use defaults below.
Start rxresume with: ./rxresume.sh up

After import, the CV is available at http://localhost:3000/dashboard
"""

import http.cookiejar
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
BASE_JSON = ROOT / "christiaan-verhoef_20260303_1718.json"

RXRESUME_URL = os.environ.get("RXRESUME_URL", "http://localhost:3000")
EMAIL = os.environ.get("RXRESUME_EMAIL", "christiaan@localhost.dev")
PASSWORD = os.environ.get("RXRESUME_PASSWORD", "CareerOS2026")


def make_opener() -> urllib.request.OpenerDirector:
    jar = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def sign_in(opener: urllib.request.OpenerDirector) -> str:
    data = json.dumps({"email": EMAIL, "password": PASSWORD}).encode()
    req = urllib.request.Request(
        f"{RXRESUME_URL}/api/auth/sign-in/email",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with opener.open(req) as resp:
            body = json.loads(resp.read())
            return body["token"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 401:
            print("Sign-in failed (wrong email/password).")
            print("Register a new account first or check your credentials.")
            sys.exit(1)
        if "FAILED_TO_CREATE_USER" in body or "not found" in body.lower():
            print("Account not found. Register first:")
            print(f"  python scripts/rxresume_register.py")
        print(f"Sign-in error {e.code}: {body[:200]}")
        sys.exit(1)


def sign_up(opener: urllib.request.OpenerDirector) -> str:
    """Register a new account if needed."""
    data = json.dumps({
        "name": "Christiaan Verhoef",
        "username": "christiaan",
        "email": EMAIL,
        "password": PASSWORD,
    }).encode()
    req = urllib.request.Request(
        f"{RXRESUME_URL}/api/auth/sign-up/email",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with opener.open(req) as resp:
            body = json.loads(resp.read())
            print(f"Registered: {EMAIL}")
            return body["token"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already" in body.lower() or "exists" in body.lower():
            print(f"Account {EMAIL} already exists — signing in.")
            return sign_in(opener)
        print(f"Registration error {e.code}: {body[:200]}")
        sys.exit(1)


def import_resume(opener: urllib.request.OpenerDirector, token: str, cv_path: Path) -> str:
    cv_data = json.loads(cv_path.read_text(encoding="utf-8"))
    payload = json.dumps({"json": {"data": cv_data}}).encode()
    req = urllib.request.Request(
        f"{RXRESUME_URL}/api/rpc/resume/import",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with opener.open(req) as resp:
            body = json.loads(resp.read())
            # Returns {"json": "<uuid>"}
            return body.get("json", body) if isinstance(body, dict) else str(body)
    except urllib.error.HTTPError as e:
        print(f"Import error {e.code}: {e.read().decode()[:300]}")
        sys.exit(1)


def check_health() -> None:
    try:
        with urllib.request.urlopen(f"{RXRESUME_URL}/api/health", timeout=5) as resp:
            data = json.loads(resp.read())
            if data.get("status") != "healthy":
                print(f"rxresume is not healthy: {data.get('status')}")
                sys.exit(1)
    except Exception:
        print(f"Cannot reach rxresume at {RXRESUME_URL}")
        print("Start it with: ./rxresume.sh up")
        sys.exit(1)


def main() -> None:
    cv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE_JSON

    if not cv_path.exists():
        print(f"File not found: {cv_path}")
        sys.exit(1)

    print(f"Checking rxresume at {RXRESUME_URL} ...")
    check_health()
    print("  rxresume is healthy")

    opener = make_opener()

    # Try sign-in first; register if account doesn't exist yet
    try:
        token = sign_in(opener)
    except SystemExit:
        print(f"Trying to register {EMAIL} ...")
        token = sign_up(opener)

    print(f"Authenticated as {EMAIL}")

    print(f"Importing: {cv_path.name} ...")
    resume_id = import_resume(opener, token, cv_path)

    print(f"\nImported successfully!")
    print(f"  Resume ID : {resume_id}")
    print(f"  Open in   : {RXRESUME_URL}/dashboard")
    print(f"  Builder   : {RXRESUME_URL}/builder/{resume_id}")


if __name__ == "__main__":
    main()
