aiproverP1.1

## Workflow: Group Presentations → Lean Statements

### Pipeline

1. **`check_abelian.sage`** — Takes one group (generators and relations as two args), computes `|G|`, `|G^ab|`, and the abelian, prints: `order ab_order verdict`
2. **`generate_lean_statements.py`** — Turns a group's sage result into a Lean 4 statement string, and packages everything into a `GroupResult` (see `models.py`)
3. **`main.py`** — Orchestrator: opens `groups.json`, loops, runs `check_abelian.sage`, and prints one JSON array of results

### Input format (`groups.json`)

A JSON array where each item describes one group:

```json
{
  "generators": {"names": ["a", "b"]},
  "relations": {"words": ["a^2", "b^2", "a*b*a^-1*b^-1"]}
}
```

### Usage

```bash
# Run the loop 
python3 main.py        # or: ./run_pipeline.sh

# Check a single group directly:
sage check_abelian.sage "a,b,c,d" "c^-2*b^-2"
```

### Output (JSON, printed to terminal)

One JSON object per group, in a JSON array:

```json
{
  "index": 1,
  "generators": {"names": ["a", "b"]},
  "relations": {"words": ["a^2", "b^2", "a*b*a^-1*b^-1"]},
  "order": "4",
  "abelian": "yes",
  "status": "ok",
  "lean_code": "def rels_1 : Set (FreeGroup (Fin 2)) := ..."
}
```

`status` is one of:
- `ok` — `lean_code` has the Lean statement
- `skipped` — non-finite order, needs manual review
- `timeout` — Sage timed out before finishing
- `error` — could not read Sage's output at all

### Encoding

- Generators: `Fin n` indexed by the order they appear in `names`
- Relations: `c^-2*b^-2` → Lean `(FreeGroup.of (2 : Fin 4) ^ (-2 : ℤ)) * (FreeGroup.of (1 : Fin 4) ^ (-2 : ℤ))`
- Theorems: `sorry` placeholders for you to prove later

