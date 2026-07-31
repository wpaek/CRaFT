#!/usr/bin/env python3

from models import CheckAbelianThingies, CheckAbelianResponse, GroupResult, word


def word_to_lean(one_word: word, gen_map: dict[str, int]) -> str | None:
    n = len(gen_map)
    parts = []
    for name, exponent in one_word:
        if name not in gen_map:
            continue
        idx = gen_map[name]
        parts.append(f'(FreeGroup.of ({idx} : Fin {n}) ^ ({exponent} : ℤ))')
    if not parts:
        return None
    return ' * '.join(parts)


def generate_statement(line_num, thingies: CheckAbelianThingies, response: CheckAbelianResponse):
    names = thingies.generators.names
    n = len(names)
    gen_map = {name: idx for idx, name in enumerate(names)}

    lean_rels = []
    for one_word in thingies.relations.words:
        lean_r = word_to_lean(one_word, gen_map)
        if lean_r:
            lean_rels.append(lean_r)

    lines = []
    lines.append(f'-- Line {line_num}: generators={names}, order={response.order}, abelian={response.abelian}')
    lines.append(f'def rels_{line_num} : Set (FreeGroup (Fin {n})) :=')
    if lean_rels:
        lines.append('  {' + ',\n   '.join(lean_rels) + '}')
    else:
        lines.append('  ∅')
    lines.append('')

    if response.abelian:
        lines.append(f'theorem group_{line_num}_abelian :')
        lines.append(f'  ∀ x y : PresentedGroup rels_{line_num}, x * y = y * x := by')
        lines.append('  sorry')
    else:
        lines.append(f'theorem group_{line_num}_not_abelian :')
        lines.append(f'  ∃ x y : PresentedGroup rels_{line_num}, x * y ≠ y * x := by')
        lines.append('  sorry')

    return '\n'.join(lines)


def build_result(index, thingies: CheckAbelianThingies, response: CheckAbelianResponse | None) -> GroupResult:
    result = GroupResult(
        index=index,
        generators=thingies.generators,
        relations=thingies.relations,
        order=None,
        abelian=None,
        status="error",
        lean_code=None,
    )

    if response is None:
        return result

    result.order = response.order
    result.abelian = response.abelian

    if response.abelian is None:
        result.status = "timeout"
    elif response.order is None:
        result.status = "skipped"
    else:
        result.status = "ok"
        result.lean_code = generate_statement(index, thingies, response)

    return result
