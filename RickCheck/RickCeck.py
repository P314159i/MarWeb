from flask import Flask, request, render_template_string

app = Flask(__name__)

# ── High-risk drugs (from PDF reference) ──────────────────────────────────────
HIGH_RISK_DRUGS = {
    "chloramphenicol",
    "chloroquine",
    "ciprofloxacin",
    "dapsone",
    "diaphenylsulfone",
    "dimercaprol",
    "doxorubicin",
    "furazolidone",
    "glibenclamide",
    "glucosulfone",
    "glucosulfone sodium",
    "isobutyl nitrite",
    "menadiol sodium sulfate",
    "vitamin k4 sodium sulfate",
    "menadione sodium bisulfite",
    "vitamin k3 sodium bisulfite",
    "mepacrine",
    "quinacrine",
    "mesalazine",
    "5-aminosalicylic acid",
    "paraaminosalicylic acid",
    "metamizole",
    "methylthioninium chloride",
    "methylene blue",
    "nalidixic acid",
    "naphthalene",
    "naphthalin",
    "niridazole",
    "nitrofural",
    "nitrofurazone",
    "nitrofurantoin",
    "o-acetylsalicylic acid",
    "acetylsalicylic acid",
    "asa",
    "oxidase, urate",
    "urate oxidase",
    "pamaquine",
    "phenacetin",
    "acetophenetidin",
    "phenazopyridine",
    "phenylhydrazine",
    "primaquine",
    "probenecid",
    "sulfacetamide",
    "sulfadimidine",
    "sulfafurazole",
    "sulfisoxazole",
    "sulfamethoxazole",
    "sulfanilamide",
    "sulphanilamide",
    "sulfapyridine",
    "sulfasalazine",
    "salazosulfapyridine",
    "salazopyrin",
    "thiazolsulfone",
    "tolonium chloride",
    "toluidine blue",
}

# ── Low-risk drugs (from PDF reference) ───────────────────────────────────────
LOW_RISK_DRUGS = {
    "arginine",
    "ascorbic acid",
    "colchicine",
    "diphenhydramine",
    "dopamine",
    "l-dopa",
    "isoniazid",
    "norfloxacin",
    "para-aminobenzoic acid",
    "4-aminobenzoic acid",
    "paracetamol",
    "acetaminophen",
    "phenylbutazone",
    "phenytoin",
    "phytomenadione",
    "vitamin k1",
    "procainamide",
    "proguanil",
    "chlorguanidine",
    "pyrimethamine",
    "quinidine",
    "quinine",
    "streptomycin",
    "sulfacytine",
    "sulfadiazine",
    "sulfaguanidine",
    "sulfamerazine",
    "sulfamethoxypyridazine",
    "trihexyphenidyl",
    "benzhexol",
    "trimethoprim",
}

# ── HTML template ─────────────────────────────────────────────────────────────
HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>G6PD Drug Risk Checker</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
body {
  font-family: Inter, system-ui, sans-serif;
  background: linear-gradient(135deg,#eef2ff,#f8fafc);
  margin:0;
  padding:40px 16px;
  display:flex;
  justify-content:center;
}

.card {
  width:100%;
  max-width:720px;
  background:white;
  border-radius:20px;
  box-shadow:0 10px 40px rgba(0,0,0,.08);
  padding:36px;
}

h1 {
  font-size:1.6rem;
  margin-bottom:6px;
}

.subtitle {
  color:#64748b;
  font-size:.95rem;
  margin-bottom:28px;
}

label {
  font-weight:600;
  font-size:.9rem;
}

.hint {
  font-size:.8rem;
  color:#94a3b8;
  margin-bottom:8px;
}

textarea {
  width:100%;
  border-radius:12px;
  border:1.5px solid #cbd5e1;
  padding:14px;
  font-size:.95rem;
  resize:vertical;
  transition:.2s;
}

textarea:focus {
  outline:none;
  border-color:#6366f1;
  box-shadow:0 0 0 3px rgba(99,102,241,.15);
}

button {
  margin-top:14px;
  width:100%;
  padding:12px;
  border-radius:12px;
  border:none;
  background:#6366f1;
  color:white;
  font-weight:600;
  font-size:.95rem;
  cursor:pointer;
}

button:hover {
  background:#4f46e5;
}

.results {
  margin-top:32px;
}

.result {
  border-radius:12px;
  padding:14px 16px;
  margin-bottom:10px;
  font-size:.9rem;
}

.high { background:#fef2f2; border-left:5px solid #ef4444; }
.low { background:#fefce8; border-left:5px solid #eab308; }
.unknown { background:#f1f5f9; border-left:5px solid #94a3b8; }

.tag {
  font-size:.7rem;
  font-weight:700;
  padding:3px 7px;
  border-radius:6px;
  margin-right:6px;
}

.high .tag { background:#fee2e2; color:#b91c1c; }
.low .tag { background:#fef9c3; color:#92400e; }
.unknown .tag { background:#e2e8f0; color:#475569; }

.footer {
  margin-top:28px;
  font-size:.75rem;
  text-align:center;
  color:#94a3b8;
}
</style>
</head>

<body>
<div class="card">

<h1>G6PD Drug Risk Checker</h1>
<p class="subtitle">Assess medication safety for patients with G6PD deficiency.</p>

<form method="post">
<label>Patient Medications</label>
<p class="hint">Comma separated — e.g. primaquine, paracetamol</p>
<textarea name="drugs" rows="4" placeholder="Enter medications...">{{ drugs or "" }}</textarea>
<button type="submit">Check Risk</button>
</form>

{% if results is not none %}
<div class="results">

{% if not results %}
<p class="hint">No drugs entered.</p>
{% else %}

{% for item in results %}
<div class="result {{ item.risk|lower }}">
<span class="tag">
{% if item.risk == "HIGH" %}HIGH
{% elif item.risk == "LOW" %}LOW
{% else %}UNKNOWN
{% endif %}
</span>
<strong>{{ item.name }}</strong>
</div>
{% endfor %}

{% endif %}
</div>
{% endif %}

<div class="footer">
Informational use only. Always verify clinically.
</div>

</div>
</body>
</html>
"""


def normalize_name(name: str) -> str:
    """Lowercase and strip spaces for matching."""
    return name.strip().lower()


@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    drugs_text = ""

    if request.method == "POST":
        drugs_text = request.form.get("drugs", "")
        raw_drugs = [d for d in drugs_text.split(",") if d.strip()]
        results = []

        for d in raw_drugs:
            norm = normalize_name(d)
            display_name = d.strip()

            if norm in HIGH_RISK_DRUGS:
                results.append({"name": display_name, "risk": "HIGH"})
            elif norm in LOW_RISK_DRUGS:
                results.append({"name": display_name, "risk": "LOW"})
            else:
                results.append({"name": display_name, "risk": "UNKNOWN"})

        if not raw_drugs:
            results = []

    return render_template_string(HTML_FORM, results=results, drugs=drugs_text)


if __name__ == "__main__":
    app.run(debug=True)
