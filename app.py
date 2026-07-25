import json

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

from models import Generators, Relations, CheckAbelianThingies
from generate_lean_statements import build_result
from sage_runner import run_check_abelian

app = FastAPI()


FORM_HTML = """
<!DOCTYPE html>
<html>
<head><title>CRaFT</title></head>
<body>
  <h1>IN: .JSON  OUT: JSON</h1>
  <form id="f">
    <input type="file" name="file" accept=".json" required>
    <button type="submit">Generate</button>
  </form>
  <pre id="out"></pre>
  <script>
    document.getElementById('f').onsubmit = async function(e) {
      e.preventDefault();
      const out = document.getElementById('out');
      out.textContent = 'working...';
      const body = new FormData(this);
      const res = await fetch('/generate', {method: 'POST', body});
      const data = await res.json();
      out.textContent = JSON.stringify(data, null, 2);
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

    results = []
    for i, item in enumerate(items, start=1):
        thingies = CheckAbelianThingies(
            generators=Generators(names=item["generators"]["names"]),
            relations=Relations(words=item["relations"]["words"]),
        )
        response = run_check_abelian(thingies)
        result = build_result(i, thingies, response)
        results.append(result.model_dump())

    return results
