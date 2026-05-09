#!/usr/bin/env python3
"""Compute lightweight summary statistics for the APPRISE audit file."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def print_counts(frame: pd.DataFrame, column: str) -> None:
    if column not in frame.columns:
        return
    print(f"\n{column}")
    print(frame[column].fillna("<missing>").value_counts().to_string())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, default=Path("audit.csv"))
    args = parser.parse_args()

    frame = pd.read_csv(args.audit)
    print(f"rows: {len(frame)}")
    print(f"columns: {', '.join(frame.columns)}")

    for column in ["app", "persona", "label", "verdict", "quality", "aligned"]:
        print_counts(frame, column)

    numeric_columns = frame.select_dtypes(include="number").columns
    if len(numeric_columns):
        print("\nNumeric summary")
        print(frame[numeric_columns].describe().to_string())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

