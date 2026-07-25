#!/usr/bin/env python3
import json

from models import Generators, Relations, CheckAbelianThingies
from generate_lean_statements import build_result
from sage_runner import run_check_abelian

JSON_PATH = "groups.json"


def main():
    with open(JSON_PATH) as f:
        items = json.load(f)

    results = []
    for i, item in enumerate(items, start=1):
        thingies = CheckAbelianThingies(
            generators=Generators(names=item["generators"]["names"]),
            relations=Relations(words=item["relations"]["words"]),
        )
        response = run_check_abelian(thingies)
        result = build_result(i, thingies, response)
        results.append(result.model_dump())

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
