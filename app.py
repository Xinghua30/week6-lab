from flask import Flask, jsonify, render_template_string, request

from duckfine import DuckFine

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/fine")
def fine():
    days = request.args.get("days", type=int)
    deluxe = request.args.get("deluxe", "0") in ("1", "true")
    if days is None:
        return jsonify(error="days must be a whole number"), 400
    try:
        fee = DuckFine("quote").charge(days, deluxe=deluxe)
    except ValueError as error:
        return jsonify(error=str(error)), 400
    return jsonify(days_late=days, deluxe=deluxe, fee=fee)


PAGE = """<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>QuackLoan fine checker - Version B</title>
<style>
  body { font: 18px system-ui, sans-serif; background: #eaf2ff; color: #17345d;
         max-width: 560px; margin: 60px auto; padding: 24px; }
  main { background: white; padding: 32px; border-radius: 20px;
         box-shadow: 0 12px 40px #17345d18; }
  .version { display: inline-block; background: #dbe8ff; padding: 6px 12px;
             border-radius: 20px; font-weight: 700; }
  h1 { margin-bottom: 8px; }
  form { display: grid; gap: 18px; margin-top: 28px; }
  input[type=number] { display: block; box-sizing: border-box; width: 100%;
                       font: inherit; padding: 12px; margin-top: 8px;
                       border: 1px solid #9fb6d9; border-radius: 8px; }
  button { font: inherit; font-weight: 700; background: #245fc7; color: white;
           border: 0; border-radius: 8px; padding: 14px; cursor: pointer; }
  [role=status] { background: #e7f6ee; color: #125735; padding: 16px;
                  border-radius: 8px; font-weight: 700; }
</style>
<main>
<span class="version">Version B</span>
<h1>QuackLoan fine checker</h1>
<p>A fresh look for your next duck return.</p>
<form>
  <label>Days late <input name="days" type="number" min="0"
    value="{{ days if days is not none else '' }}"></label>
  <label><input name="deluxe" type="checkbox" value="1"
    {% if deluxe %}checked{% endif %}>
    Deluxe duck</label>
  <button>Check fine</button>
</form>
{% if fee is not none %}
<p role="status">Your fine is ${{ "%.2f" % fee }}</p>
{% endif %}
</main>
</html>
"""


@app.get("/")
def checker():
    days = request.args.get("days", type=int)
    deluxe = request.args.get("deluxe") == "1"
    fee = None
    if days is not None and days >= 0:
        fee = DuckFine("quote").charge(days, deluxe=deluxe)
    return render_template_string(PAGE, fee=fee, days=days, deluxe=deluxe)
