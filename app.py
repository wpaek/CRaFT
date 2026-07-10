import csv
import io
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

from generate_lean_statements import generate_statement

app = FastAPI()


def run_check_abelian(generators, relations):
    sage = "/home/pk/miniforge3/envs/sage/bin/sage"
    command = f'{sage} check_abelian.sage "{generators}" "{relations}"'
    output = os.popen(command).read()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
            order, _, verdict = parts
            return order, verdict
    return None, None


FORM_HTML = """
<!DOCTYPE html>
<html>
<head><title>CRaFT</title></head>
<body>
  <h1>IN: .CSV  OUT: Lean</h1>
  <form id="f">
    <input type="file" name="file" accept=".csv" required>
    <button type="submit">Generate</button>
  </form>
  <pre id="out"></pre>
  <script>
    document.getElementById('f').onsubmit = async function(e) {
      e.preventDefault();
      const out = document.getElementById('out');
      out.textContent = '';
      const body = new FormData(this);
      const res = await fetch('/generate', {method: 'POST', body});
      const reader = res.body.getReader();
      const dec = new TextDecoder();
      while (true) {
        const {done, value} = await reader.read();
        if (done) break;
        out.textContent += dec.decode(value);
      }
    };
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return FORM_HTML


@app.post("/generate")
def generate(file: UploadFile = File(...)):
    raw = file.file.read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(raw)))
    rows = rows[1:]

    def stream():
        yield "import Mathlib.GroupTheory.PresentedGroup\nimport Mathlib.SetTheory.Cardinal.Finite\n\n"
        for i, row in enumerate(rows, start=2):
            generators = row[0]
            relations = row[1]
            order, verdict = run_check_abelian(generators, relations)
            if verdict is None:
                yield f"-- Line {i}: could not read Sage output (skipped)\n\n"
            else:
                yield generate_statement(i, generators, relations, order, verdict) + "\n\n"

    return StreamingResponse(stream(), media_type="text/plain")
