#!/usr/bin/env python3
import csv
import subprocess
from generate_lean_statements import generate_statement

CSV_PATH = "groupPresentations.csv"


def run_check_abelian(generators, relations):
    """Run check_abelian.sage and return (order, verdict)."""
    result = subprocess.run(
        ["sage", "check_abelian.sage", generators, relations],
        capture_output=True,
        text=True,
    )

    # last word is verdict.
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
            order, _, verdict = parts
            return order, verdict
    return None, None


def main():
    print("import Mathlib.GroupTheory.PresentedGroup")
    print("import Mathlib.SetTheory.Cardinal.Finite")
    print()

    with open(CSV_PATH) as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        for i, row in enumerate(reader, start=2):
            generators = row[0]
            relations = row[1]

            order, verdict = run_check_abelian(generators, relations)
            if verdict is None:
                print(f"-- Line {i}: could not read Sage output (skipped)")
                print()
                continue

            print(generate_statement(i, generators, relations, order, verdict))
            print()


if __name__ == "__main__":
    main()
