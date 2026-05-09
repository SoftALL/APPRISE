#!/usr/bin/env python3
"""Validate APPRISE dataset files and optionally write small sample files."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


EXPECTED_FILES = {
    "issues": "issues.jsonl",
    "reviews": "reviews.jsonl",
    "triplets": "triplets.tsv",
    "audit": "audit.csv",
}

SAMPLE_NAMES = {
    "issues.jsonl": "sample_issues.jsonl",
    "reviews.jsonl": "sample_reviews.jsonl",
    "triplets.tsv": "sample_triplets.tsv",
    "audit.csv": "sample_audit.csv",
}


def read_jsonl(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            count += 1
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}:{line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(value, dict):
                errors.append(f"{path.name}:{line_number}: expected object")
    return count, errors


def count_delimited(path: Path, delimiter: str) -> tuple[int, list[str]]:
    errors: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        rows = list(reader)
    if not rows:
        return 0, [f"{path.name}: file is empty"]
    width = len(rows[0])
    for index, row in enumerate(rows[1:], start=2):
        if len(row) != width:
            errors.append(f"{path.name}:{index}: expected {width} columns, found {len(row)}")
    return len(rows), errors


def write_samples(data_dir: Path, sample_dir: Path, sample_size: int) -> None:
    sample_dir.mkdir(parents=True, exist_ok=True)
    for source_name, sample_name in SAMPLE_NAMES.items():
        source = data_dir / source_name
        target = sample_dir / sample_name
        if not source.exists():
            print(f"skip sample: missing {source}")
            continue
        with source.open("r", encoding="utf-8", newline="") as src, target.open(
            "w", encoding="utf-8", newline=""
        ) as dst:
            for index, line in enumerate(src):
                if index >= sample_size:
                    break
                dst.write(line)
        print(f"wrote {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("."), help="Directory with APPRISE files.")
    parser.add_argument("--write-samples", type=Path, help="Directory where sample files should be written.")
    parser.add_argument("--sample-size", type=int, default=20, help="Number of rows to write per sample file.")
    args = parser.parse_args()

    data_dir = args.data_dir.resolve()
    failures: list[str] = []

    for label, filename in EXPECTED_FILES.items():
        path = data_dir / filename
        if not path.exists():
            failures.append(f"missing {filename}")
            continue
        if path.suffix == ".jsonl":
            count, errors = read_jsonl(path)
        elif path.suffix == ".tsv":
            count, errors = count_delimited(path, "\t")
        else:
            count, errors = count_delimited(path, ",")
        print(f"{label}: {count} rows")
        failures.extend(errors)

    if args.write_samples:
        write_samples(data_dir, args.write_samples, args.sample_size)

    if failures:
        print("\nValidation issues:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

