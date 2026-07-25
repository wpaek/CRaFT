import os

from models import CheckAbelianThingies, CheckAbelianResponse


def run_check_abelian(thingies: CheckAbelianThingies) -> CheckAbelianResponse | None:
    sage = os.environ.get("SAGE_PATH", "sage")
    generators_str = ",".join(thingies.generators.names)
    relations_str = ",".join(thingies.relations.words)
    command = f'{sage} check_abelian.sage "{generators_str}" "{relations_str}"'
    output = os.popen(command).read()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
            return CheckAbelianResponse(order=parts[0], abelian=parts[2])
    return None
