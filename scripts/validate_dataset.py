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

TRIPLET_COLUMNS = [
    "query_review_id",
    "positive_issue_id",
    "negative_issue_id",
    "negative_type",
]

NEGATIVE_TYPES = {"within_app", "cross_app"}


def load_jsonl_by_id(path: Path, id_field: str) -> tuple[dict[str, dict], int, list[str]]:
    records: dict[str, dict] = {}
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
                continue
            record_id = value.get(id_field)
            if not record_id:
                errors.append(f"{path.name}:{line_number}: missing {id_field}")
                continue
            if record_id in records:
                errors.append(f"{path.name}:{line_number}: duplicate {id_field}={record_id}")
                continue
            records[str(record_id)] = value
    return records, count, errors


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


def load_triplets(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    triplets: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != TRIPLET_COLUMNS:
            errors.append(f"{path.name}: expected columns {TRIPLET_COLUMNS}, found {reader.fieldnames}")
            return triplets, errors
        for line_number, row in enumerate(reader, start=2):
            if row.keys() != set(TRIPLET_COLUMNS):
                errors.append(f"{path.name}:{line_number}: malformed row")
                continue
            triplets.append({column: (row.get(column) or "") for column in TRIPLET_COLUMNS})
    return triplets, errors


def count_csv_data_rows(path: Path) -> tuple[int, list[str]]:
    total_rows, errors = count_delimited(path, ",")
    return max(total_rows - 1, 0), errors


def check_review_links(reviews: dict[str, dict], issues: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for review_id, review in reviews.items():
        issue_id = review.get("issue_id")
        if not issue_id:
            errors.append(f"reviews.jsonl:{review_id}: missing issue_id")
        elif str(issue_id) not in issues:
            errors.append(f"reviews.jsonl:{review_id}: issue_id={issue_id} not found in issues")
    return errors


def check_triplets(triplets: list[dict[str, str]], reviews: dict[str, dict], issues: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for index, triplet in enumerate(triplets, start=2):
        query_review_id = triplet["query_review_id"]
        positive_issue_id = triplet["positive_issue_id"]
        negative_issue_id = triplet["negative_issue_id"]
        negative_type = triplet["negative_type"]

        review = reviews.get(query_review_id)
        positive_issue = issues.get(positive_issue_id)
        negative_issue = issues.get(negative_issue_id)

        if review is None:
            errors.append(f"triplets.tsv:{index}: query_review_id={query_review_id} not found in reviews")
        if positive_issue is None:
            errors.append(f"triplets.tsv:{index}: positive_issue_id={positive_issue_id} not found in issues")
        if negative_issue is None:
            errors.append(f"triplets.tsv:{index}: negative_issue_id={negative_issue_id} not found in issues")
        if positive_issue_id == negative_issue_id:
            errors.append(f"triplets.tsv:{index}: positive_issue_id equals negative_issue_id ({positive_issue_id})")
        if negative_type not in NEGATIVE_TYPES:
            errors.append(f"triplets.tsv:{index}: invalid negative_type={negative_type}")

        if review is not None and str(review.get("issue_id")) != positive_issue_id:
            errors.append(
                f"triplets.tsv:{index}: positive_issue_id={positive_issue_id} does not match "
                f"review {query_review_id} source issue_id={review.get('issue_id')}"
            )

        if positive_issue is None or negative_issue is None or negative_type not in NEGATIVE_TYPES:
            continue

        positive_app = positive_issue.get("app")
        negative_app = negative_issue.get("app")
        if negative_type == "within_app" and positive_app != negative_app:
            errors.append(
                f"triplets.tsv:{index}: within_app negative has different apps "
                f"positive={positive_app}, negative={negative_app}"
            )
        if negative_type == "cross_app" and positive_app == negative_app:
            errors.append(
                f"triplets.tsv:{index}: cross_app negative has same app positive={positive_app}, negative={negative_app}"
            )
    return errors


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
    counts: dict[str, int] = {}

    paths = {label: data_dir / filename for label, filename in EXPECTED_FILES.items()}
    for filename, path in ((filename, data_dir / filename) for filename in EXPECTED_FILES.values()):
        if not path.exists():
            failures.append(f"missing {filename}")

    issues: dict[str, dict] = {}
    reviews: dict[str, dict] = {}
    triplets: list[dict[str, str]] = []

    if not failures:
        issues, counts["issues"], errors = load_jsonl_by_id(paths["issues"], "issue_id")
        failures.extend(errors)

        reviews, counts["reviews"], errors = load_jsonl_by_id(paths["reviews"], "review_id")
        failures.extend(errors)
        failures.extend(check_review_links(reviews, issues))

        triplets, errors = load_triplets(paths["triplets"])
        counts["triplets"] = len(triplets)
        failures.extend(errors)
        failures.extend(check_triplets(triplets, reviews, issues))

        counts["audit"], errors = count_csv_data_rows(paths["audit"])
        failures.extend(errors)

    for label in EXPECTED_FILES:
        if label in counts:
            print(f"{label}: {counts[label]} rows")

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
