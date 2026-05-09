#!/usr/bin/env python3
"""Mine simple lexical hard negatives for APPRISE issue-review pairs."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(text) if len(token) > 2}


def load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def text_for(record: dict, fields: list[str]) -> str:
    return " ".join(str(record.get(field, "")) for field in fields)


def score(issue_terms: set[str], review_terms: set[str], idf: Counter[str]) -> float:
    if not issue_terms or not review_terms:
        return 0.0
    overlap = issue_terms & review_terms
    weighted_overlap = sum(idf[term] for term in overlap)
    normalizer = math.sqrt(sum(idf[term] for term in issue_terms) * sum(idf[term] for term in review_terms))
    return weighted_overlap / normalizer if normalizer else 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issues", type=Path, required=True)
    parser.add_argument("--reviews", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    issues = load_jsonl(args.issues)
    reviews = load_jsonl(args.reviews)
    issue_fields = ["title", "body", "description", "app"]
    review_fields = ["review", "text", "body", "app"]

    review_terms = [tokens(text_for(review, review_fields)) for review in reviews]
    document_frequency: Counter[str] = Counter()
    for terms in review_terms:
        document_frequency.update(terms)

    total_reviews = max(len(reviews), 1)
    idf = Counter(
        {term: math.log((1 + total_reviews) / (1 + frequency)) + 1 for term, frequency in document_frequency.items()}
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        handle.write("issue_index\treview_index\tscore\n")
        for issue_index, issue in enumerate(issues):
            issue_terms = tokens(text_for(issue, issue_fields))
            ranked = sorted(
                (
                    (score(issue_terms, terms, idf), review_index)
                    for review_index, terms in enumerate(review_terms)
                ),
                reverse=True,
            )
            for similarity, review_index in ranked[: args.top_k]:
                handle.write(f"{issue_index}\t{review_index}\t{similarity:.6f}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

