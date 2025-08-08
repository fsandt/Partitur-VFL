from types import SimpleNamespace
from flask import Flask, request, render_template_string

from utils.text_parser import parse_text
from score.generator import ScoreGenerator, MUSIC21_AVAILABLE

app = Flask(__name__)

PAGE_TEMPLATE = """
<!doctype html>
<title>Partitur Generator</title>
<h1>Partitur Generator</h1>
<form method="post">
  <textarea name="description" rows="4" cols="50" placeholder="Enter description" required></textarea><br/>
  <button type="submit">Generate</button>
</form>
{% if result %}
  <h2>Composition Overview</h2>
  <p><strong>Mood:</strong> {{ result.mood }}</p>
  <p><strong>Instruments:</strong> {{ result.instruments|join(', ') }}</p>
  {% for instrument, notes in result.notes.items() %}
    <h3>{{ instrument.title() }}</h3>
    <p>{{ notes }}</p>
  {% endfor %}
{% endif %}
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        description = request.form.get("description", "")
        parsed = parse_text(description)
        generator = ScoreGenerator()
        scores = generator.generate_score(parsed)
        notes: dict[str, str] = {}
        for instrument, part in scores.items():
            if MUSIC21_AVAILABLE:
                notes[instrument] = " ".join(n.nameWithOctave for n in part.notes)
            else:
                notes[instrument] = part
        result = SimpleNamespace(
            mood=parsed["mood"],
            instruments=parsed["instruments"],
            notes=notes,
        )
    return render_template_string(PAGE_TEMPLATE, result=result)


if __name__ == "__main__":
    app.run()
