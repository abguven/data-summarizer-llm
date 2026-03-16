#!/usr/bin/env python3
"""
Functional tests for data-summarizer output.

Validates that generated Markdown summaries contain the correct values
for known input files in tests/data/.

Usage:
    python tests/test_output.py <output_dir>
"""

import os
import sys


def check(failures: list, label: str, content: str, expected: str):
    if expected in content:
        print(f"  ✅ {label}")
    else:
        print(f"  ❌ {label} — expected: '{expected}'")
        failures.append(label)


def load_file(path: str) -> str:
    if not os.path.exists(path):
        print(f"❌ Missing output file: {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_csv(output_dir: str, failures: list):
    content = load_file(os.path.join(output_dir, "SUMMARY_sample.csv.md"))
    print("\n[sample.csv]")

    # Structure
    check(failures, "5 rows detected",         content, "**Rows:** 5")
    check(failures, "5 columns detected",      content, "**Columns:** 5")

    # Columns present
    check(failures, "column 'name' present",   content, "| name |")
    check(failures, "column 'age' present",    content, "| age |")
    check(failures, "column 'city' present",   content, "| city |")
    check(failures, "column 'salary' present", content, "| salary |")

    # Numeric stats for 'age' (Eve is null → 4 values: 25, 28, 30, 35)
    check(failures, "age min = 25.00",         content, "Min:25.00")
    check(failures, "age max = 35.00",         content, "Max:35.00")
    check(failures, "age avg = 29.50",         content, "Avg:29.50")

    # Numeric stats for 'salary' (Bob is null → 4 values)
    check(failures, "salary min = 38500.75",   content, "Min:38500.75")
    check(failures, "salary max = 62000.00",   content, "Max:62000.00")

    # Missing values
    check(failures, "age missing = 20.0%",     content, "20.0%")
    check(failures, "salary missing = 20.0%",  content, "20.0%")

    # ASCII histogram generated for numeric columns
    check(failures, "histogram present",       content, "Dist:")


def test_json(output_dir: str, failures: list):
    content = load_file(os.path.join(output_dir, "SUMMARY_sample.json.md"))
    print("\n[sample.json]")

    # Structure
    check(failures, "4 rows detected",            content, "**Rows:** 4")
    check(failures, "4 columns detected",         content, "**Columns:** 4")

    # Columns present
    check(failures, "column 'product' present",   content, "| product |")
    check(failures, "column 'category' present",  content, "| category |")
    check(failures, "column 'price' present",     content, "| price |")
    check(failures, "column 'stock' present",     content, "| stock |")

    # Numeric stats for 'price' (no nulls → 4 values: 8.99, 12.50, 29.99, 49.99)
    check(failures, "price min = 8.99",            content, "Min:8.99")
    check(failures, "price max = 49.99",           content, "Max:49.99")
    check(failures, "price avg = 25.37",           content, "Avg:25.37")

    # Numeric stats for 'stock' (Widget B is null → 3 values: 75, 150, 300)
    check(failures, "stock min = 75.00",           content, "Min:75.00")
    check(failures, "stock max = 300.00",          content, "Max:300.00")

    # Missing values (1 null out of 4 rows)
    check(failures, "stock missing = 25.0%",       content, "25.0%")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    failures = []

    test_csv(output_dir, failures)
    test_json(output_dir, failures)

    print(f"\n{'─' * 40}")
    if failures:
        print(f"❌ {len(failures)} test(s) failed: {', '.join(failures)}")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
