#!/usr/bin/env python3

from models import CheckAbelianThingies, CheckAbelianResponse, GroupResult


def word_to_lean(word, gen_map):
    n = len(gen_map)
    parts = []
    for term in word.split('*'):
        term = term.strip()
        if not term:
            continue
        if '^' in term:
            gen, exp = term.split('^')
        else:
            gen, exp = term, ''
        gen = gen.strip()
        if gen not in gen_map:
            continue
        if parts:
            parts.append(' * ')
        idx = gen_map[gen]
        if exp == '':
            parts.append(f'FreeGroup.of ({idx} : Fin {n})')
        else:
            parts.append(f'(FreeGroup.of ({idx} : Fin {n}) ^ ({exp} : ℤ))')
    return ''.join(parts) if parts else None


def generate_statement(line_num, thingies: CheckAbelianThingies, response: CheckAbelianResponse):
    names = thingies.generators.names
    n = len(names)
    gen_map = {name: idx for idx, name in enumerate(names)}

    lean_rels = []
    for word in thingies.relations.words:
        lean_r = word_to_lean(word, gen_map)
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

    if response.abelian == 'yes':
        lines.append(f'theorem group_{line_num}_abelian :')
        lines.append(f'  ∀ x y : PresentedGroup rels_{line_num}, x * y = y * x := by')
        lines.append('  sorry')
    else:
        lines.append(f'theorem group_{line_num}_not_abelian :')
        lines.append(f'  ∃ x y : PresentedGroup rels_{line_num}, x * y ≠ y * x := by')
        lines.append('  sorry')

    return '\n'.join(lines)


def build_result(index, thingies: CheckAbelianThingies, response: CheckAbelianResponse | None) -> GroupResult:
    if response is None:
        return GroupResult(
            index=index,
            generators=thingies.generators,
            relations=thingies.relations,
            order=None,
            abelian=None,
            status="error",
            lean_code=None,
        )

    if response.abelian == '?':
        return GroupResult(
            index=index,
            generators=thingies.generators,
            relations=thingies.relations,
            order=response.order,
            abelian=response.abelian,
            status="timeout",
            lean_code=None,
        )

    if response.order == 'timeout' or 'Infinity' in response.order:
        return GroupResult(
            index=index,
            generators=thingies.generators,
            relations=thingies.relations,
            order=response.order,
            abelian=response.abelian,
            status="skipped",
            lean_code=None,
        )

    lean_code = generate_statement(index, thingies, response)
    return GroupResult(
        index=index,
        generators=thingies.generators,
        relations=thingies.relations,
        order=response.order,
        abelian=response.abelian,
        status="ok",
        lean_code=lean_code,
    )
