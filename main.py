#!/usr/bin/env python3
import json
import os

from models import Generators, Relations, CheckAbelianThingies, CheckAbelianResponse
from generate_lean_statements import generate_statement

JSON_PATH = "groupPresentations.json"


def run_check_abelian(thingies: CheckAbelianThingies) -> CheckAbelianResponse | None:
    sage = os.environ.get("SAGE_PATH", "sage")
    generators_str = ",".join(thingies.generators.names)
    relations_str = ",".join(thingies.relations.expressions)
    command = f'{sage} check_abelian.sage "{generators_str}" "{relations_str}"'
    output = os.popen(command).read()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
            return CheckAbelianResponse(order=parts[0], abelian=parts[2])
    return None


def main():
    print("import Mathlib.GroupTheory.PresentedGroup")
    print("import Mathlib.SetTheory.Cardinal.Finite")
    print()

    with open(JSON_PATH) as f:
        items = json.load(f)

    for i, item in enumerate(items, start=1):
        thingies = CheckAbelianThingies(
            generators=Generators(names=item["generators"]["names"]),
            relations=Relations(expressions=item["relations"]["expressions"]),
        )
        response = run_check_abelian(thingies)
        if response is None:
            print(f"-- Line {i}: could not read Sage output (skipped)")
            print()
            continue

        print(generate_statement(i, thingies, response))
        print()


if __name__ == "__main__":
    main()


# --- OLD CSV-BASED CODE (commented out) ---
#
# import csv
# CSV_PATH = "groupPresentations.csv"
#
# def run_check_abelian(generators, relations):
#     sage = os.environ.get("SAGE_PATH", "sage")
#     command = f'{sage} check_abelian.sage "{generators}" "{relations}"'
#     output = os.popen(command).read()
#     for line in output.splitlines():
#         parts = line.split()
#         if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
#             order, _, verdict = parts
#             return order, verdict
#     return None, None
#
# def main():
#     print("import Mathlib.GroupTheory.PresentedGroup")
#     print("import Mathlib.SetTheory.Cardinal.Finite")
#     print()
#     with open(CSV_PATH) as f:
#         reader = csv.reader(f)
#         next(reader)
#         for i, row in enumerate(reader, start=2):
#             generators = row[0]
#             relations = row[1]
#             order, verdict = run_check_abelian(generators, relations)
#             if verdict is None:
#                 print(f"-- Line {i}: could not read Sage output (skipped)")
#                 print()
#                 continue
#             print(generate_statement(i, generators, relations, order, verdict))
#             print()
