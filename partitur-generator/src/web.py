from __future__ import annotations

import base64
from pathlib import Path
from types import SimpleNamespace
from typing import Dict

# from flask
from flask import Flask, request, render_template_string, send_from_directory

from utils.text_parser import parse_text
from score.generator import ScoreGenerator, MUSIC21_AVAILABLE

BASE_DIR = Path(__file__).resolve().parents[2]
app = Flask(__name__, static_folder=str(BASE_DIR / "docs"))

# directory for generated files
OUTPUT_DIR = Path(__file__).resolve().parent / "generated"
OUTPUT_DIR.mkdir(exist_ok=True)

PAGE_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Partitur Generator</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <script src="{{ url_for('static', filename='script.js') }}" defer></script>
</head>
<body>
  <div class="container">
    <h1>Partitur Generator</h1>
    <form method="post">
      <textarea name="description" rows="4" placeholder="Beschreibungstext eingeben" required></textarea>
      <div class="instrument-list">
        {% for inst in instruments %}
          <label><input type="checkbox" name="instruments" value="{{ inst }}" {% if inst in selected_instruments %}checked{% endif %}> {{ inst.title() }}</label>
        {% endfor %}
      </div>
      <button type="submit">Generieren</button>
    </form>
    {% if result %}
      <h2>Kompositionsübersicht</h2>
      <p><strong>Stimmung:</strong> {{ result.mood }}</p>
      {% for instrument, data in result.outputs.items() %}
        <div class="sheet">
          <h3>{{ instrument.title() }}</h3>
          {% if data.image %}
            <img src="data:image/png;base64,{{ data.image }}" alt="Notenblatt von {{ instrument }}"/>
          {% else %}
            <p>{{ data.notes }}</p>
          {% endif %}
          {% if data.pdf %}
            <p><a href="/download/{{ data.pdf }}">PDF herunterladen</a></p>
          {% endif %}
        </div>
      {% endfor %}
    {% endif %}
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    generator = ScoreGenerator()
    all_instruments = list(generator.INSTRUMENT_CLASSES.keys()) or ["piano", "violin", "flute", "guitar", "bass", "drums"]
    selected_instruments = []

    if request.method == "POST":
        description = request.form.get("description", "")
        parsed = parse_text(description)
        selected_instruments = request.form.getlist("instruments") or parsed.get("instruments", [])
        parsed["instruments"] = selected_instruments

        scores = generator.generate_score(parsed)
        outputs: Dict[str, Dict[str, str | None]] = {}
        for instrument, part in scores.items():
            data: Dict[str, str | None] = {"pdf": None, "image": None, "notes": None}
            if MUSIC21_AVAILABLE:
                try:
                    pdf_path = OUTPUT_DIR / f"{instrument}.pdf"
                    part.write("musicxml.pdf", fp=str(pdf_path))
                    data["pdf"] = pdf_path.name
                    png_path = OUTPUT_DIR / f"{instrument}.png"
                    part.write("musicxml.png", fp=str(png_path))
                    with open(png_path, "rb") as img:
                        data["image"] = base64.b64encode(img.read()).decode("ascii")
                except Exception:
                    data["notes"] = " ".join(n.nameWithOctave for n in part.notes)
            else:  # pragma: no cover - fallback when music21 missing
                data["notes"] = part
            outputs[instrument] = data

        result = SimpleNamespace(
            mood=parsed["mood"],
            outputs=outputs,
        )

    return render_template_string(
        PAGE_TEMPLATE,
        result=result,
        instruments=all_instruments,
        selected_instruments=selected_instruments,
    )


@app.route("/download/<path:filename>")
def download(filename: str):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run()
