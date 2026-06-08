aiproverP1.1

## Workflow: Group Presentations → Lean Statements

### Pipeline

1. **`check_abelian.sage`** — Takes one group (generators and relations as two args), computes `|G|`, `|G^ab|`, and the abelian, prints: `order ab_order verdict`
2. **`generate_lean_statements.py`** — Turns group verdict into a Lean 4 statement string
3. **`main.py`** — Orchestrator: opens CSV, loops, runs `check_abelian.sage`, and prints the Lean statements

### Usage

```bash
# Run the loop 
python3 main.py        # or: ./run_pipeline.sh

# Check a single group directly:
sage check_abelian.sage "a,b,c,d" "c^-2*b^-2"
```

### Output (to terminal)

- One `def rels_N : Set (FreeGroup (Fin n))` + `theorem group_N_abelian`/`group_N_not_abelian` per finite group
- Skips timeouts and infinite-order groups (printed as comments needing manual review)

### Encoding

- Generators: `Fin n` indexed by CSV column order (a=0, b=1, c=2, d=3)
- Relations: CSV `c^-2*b^-2` → Lean `(FreeGroup.of (2 : Fin 4) ^ (-2 : ℤ)) * (FreeGroup.of (1 : Fin 4) ^ (-2 : ℤ))`
- Theorems: `sorry` placeholders for you to prove later
