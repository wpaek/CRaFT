import os

from models import CheckAbelianThingies, CheckAbelianResponse, word


def word_to_text(one_word: word) -> str:
    pieces = []
    for name, exponent in one_word:
        pieces.append(f"{name}^{exponent}")
    return "*".join(pieces)


def text_to_order(text: str) -> int | None:
    if text.isdigit() and int(text) > 0:
        return int(text)
    return None


def text_to_abelian(text: str) -> bool | None:
    if text == "yes":
        return True
    if text == "no":
        return False
    return None


def run_check_abelian(thingies: CheckAbelianThingies) -> CheckAbelianResponse | None:
    sage = os.environ.get("SAGE_PATH", "sage")
    generators_str = ",".join(thingies.generators.names)
    relation_texts = []
    for one_word in thingies.relations.words:
        relation_texts.append(word_to_text(one_word))
    relations_str = ",".join(relation_texts)
    command = f'{sage} check_abelian.sage "{generators_str}" "{relations_str}"'
    output = os.popen(command).read()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
            return CheckAbelianResponse(
                order=text_to_order(parts[0]),
                abelian=text_to_abelian(parts[2]),
            )
    return None
