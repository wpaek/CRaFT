import json
import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

from models import Generators, Relations, CheckAbelianThingies, CheckAbelianResponse
from generate_lean_statements import generate_statement

app = FastAPI()


def run_check_abelian(thingies: CheckAbelianThingies) -> CheckAbelianResponse | None:
    sage = os.environ.get("SAGE_PATH", "sage")
    generators_str = ",".join(thingies.generators.names)
    relations_str = ",".join(thingies.relations.expressions)
    command = f'{sage} check_abelian.sage "{generators_str}" "{relations_str}"'
    output = os.popen(command).read()
    for line in output.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
            return CheckAbelianResponse(order=parts[0], abelian=parts[2])
    return None


FORM_HTML = """
<!DOCTYPE html>
<html>
<head><title>CRaFT</title></head>
<body>
  <h1>IN: .JSON  OUT: Lean</h1>
  <form id="f">
    <input type="file" name="file" accept=".json" required>
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
    items = json.loads(raw)

    def stream():
        yield "import Mathlib.GroupTheory.PresentedGroup\nimport Mathlib.SetTheory.Cardinal.Finite\n\n"
        for i, item in enumerate(items, start=1):
            thingies = CheckAbelianThingies(
                generators=Generators(names=item["generators"]["names"]),
                relations=Relations(expressions=item["relations"]["expressions"]),
            )
            response = run_check_abelian(thingies)
            if response is None:
                yield f"-- Line {i}: could not read Sage output (skipped)\n\n"
            else:
                yield generate_statement(i, thingies, response) + "\n\n"

    return StreamingResponse(stream(), media_type="text/plain")


# --- OLD CSV-BASED CODE (commented out) ---
#
# import csv
# import io
#
# def run_check_abelian(generators, relations):
#     sage = os.environ.get("SAGE_PATH", "sage")
#     command = f'{sage} check_abelian.sage "{generators}" "{relations}"'
#     output = os.popen(command).read()
#     for line in output.splitlines():
#         parts = line.split()
#         if len(parts) == 3 and parts[2] in ("yes", "no", "?"):
#             order, _, verdict = parts
#             return order, verdict
#     return None, None
#
# @app.post("/generate")
# def generate(file: UploadFile = File(...)):
#     raw = file.file.read().decode("utf-8")
#     rows = list(csv.reader(io.StringIO(raw)))
#     rows = rows[1:]
#     def stream():
#         yield "import Mathlib.GroupTheory.PresentedGroup\nimport Mathlib.SetTheory.Cardinal.Finite\n\n"
#         for i, row in enumerate(rows, start=2):
#             generators = row[0]
#             relations = row[1]
#             order, verdict = run_check_abelian(generators, relations)
#             if verdict is None:
#                 yield f"-- Line {i}: could not read Sage output (skipped)\n\n"
#             else:
#                 yield generate_statement(i, generators, relations, order, verdict) + "\n\n"
#     return StreamingResponse(stream(), media_type="text/plain")
