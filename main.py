#!/usr/bin/env python3
import csv
import os
from generate_lean_statements import generate_statement

CSV_PATH = "groupPresentations.csv"


def run_check_abelian(generators, relations):
    """Run check_abelian.sage and return (order, verdict)."""
    sage = "/home/pk/miniforge3/envs/sage/bin/sage"
    command = f'{sage} check_abelian.sage "{generators}" "{relations}"'
    output = os.popen(command).read()

    # last word is verdict.
    for line in output.splitlines():
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
