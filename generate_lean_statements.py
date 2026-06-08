#!/usr/bin/env python3
import re

def csv_word_to_lean(word, gen_map):
    word = word.strip()
    if not word:
        return None
    
    tokens = re.findall(r'([a-z])(?:\^(-?\d+))?|\*', word)
    parts = []
    for i, token in enumerate(tokens):
        if isinstance(token, str) and token == '*':
            continue
        elif isinstance(token, tuple):
            gen, exp = token
            if not gen:
                continue
            if gen not in gen_map:
                continue
            
            if parts:
                parts.append(' * ')
            
            idx = gen_map[gen]
            if exp == '':
                parts.append(f'FreeGroup.of ({idx} : Fin {len(gen_map)})')
            else:
                parts.append(f'(FreeGroup.of ({idx} : Fin {len(gen_map)}) ^ ({exp} : ℤ))')
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
    gens = generators.split(',')
    n = len(gens)
    gen_map = {g.strip(): idx for idx, g in enumerate(gens)}
    lean_rels = parse_relations(relations, gen_map)

    # skip cases we can't trust
    if verdict == '?':
        return f'-- Line {line_num}: Timeout (skipped)'

    if order == 'timeout' or 'Infinity' in order:
        return f'-- Line {line_num}: Non-finite order (needs manual review)'

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
