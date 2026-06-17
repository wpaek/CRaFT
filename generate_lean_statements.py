#!/usr/bin/env python3

def csv_word_to_lean(word, gen_map):
    word = word.strip()
    if not word:
        return None

    n = len(gen_map)
    parts = []
    # a word is terms joined by '*', e.g. "c^-2*b^-2"
    for term in word.split('*'):
        term = term.strip()
        if not term:
            continue

        # a term is a generator with an optional "^exponent"
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
    return ''.join(parts)

def parse_relations(rel_str, gen_map):
    if not rel_str.strip():
        return []
    rels = rel_str.split(',')
    lean_rels = []
    for r in rels:
        lean_r = csv_word_to_lean(r, gen_map)
        if lean_r:
            lean_rels.append(lean_r)
    return lean_rels

def generate_statement(line_num, generators, relations, order, verdict):
    """Build the Lean statement for one group as a string."""
    # skip cases we can't trust
    if verdict == '?':
        return f'-- Line {line_num}: Timeout (skipped)'

    if order == 'timeout' or 'Infinity' in order:
        return f'-- Line {line_num}: Non-finite order (needs manual review)'

    gens = generators.split(',')
    n = len(gens)
    gen_map = {g.strip(): idx for idx, g in enumerate(gens)}
    lean_rels = parse_relations(relations, gen_map)

    lines = []
    lines.append(f'-- Line {line_num}: generators={generators}, order={order}, abelian={verdict}')
    lines.append(f'def rels_{line_num} : Set (FreeGroup (Fin {n})) :=')
    if lean_rels:
        lines.append('  {' + ',\n   '.join(lean_rels) + '}')
    else:
        lines.append('  ∅')
    lines.append('')

    if verdict == 'yes':
        lines.append(f'theorem group_{line_num}_abelian :')
        lines.append(f'  ∀ x y : PresentedGroup rels_{line_num}, x * y = y * x := by')
        lines.append('  sorry')
    else:
        lines.append(f'theorem group_{line_num}_not_abelian :')
        lines.append(f'  ∃ x y : PresentedGroup rels_{line_num}, x * y ≠ y * x := by')
        lines.append('  sorry')

    return '\n'.join(lines)
