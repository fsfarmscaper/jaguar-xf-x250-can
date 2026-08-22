#!/usr/bin/env python3
import sys
import subprocess
from pathlib import Path


def validate_file(file_path: str) -> bool:
    """
    Uses cantools CLI equivalent behavior to validate DBC.
    Mirrors: python -m cantools dump <file>
    """
    try:
        result = subprocess.run(
            ["python", "-m", "cantools", "dump", file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"\n❌ DBC validation failed: {file_path}")
            print(result.stderr.strip())
            return False

        print(f"✔ Valid DBC: {file_path}")
        return True

    except Exception as e:
        print(f"\n❌ Exception while validating {file_path}: {e}")
        return False


def main():
    files = sys.argv[1:]

    if not files:
        print("No DBC files provided")
        return 0

    all_ok = True

    for f in files:
        path = Path(f)
        if not path.exists():
            print(f"⚠ File not found: {f}")
            all_ok = False
            continue

        if not validate_file(str(path)):
            all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())