import sys
from utils.text_parser import parse_text
from score.generator import MUSIC21_AVAILABLE, ScoreGenerator


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <description_text>")
        return

    description = " ".join(sys.argv[1:])
    parsed_data = parse_text(description)

    score_generator = ScoreGenerator()
    scores = score_generator.generate_score(parsed_data)

    print("Composition overview:")
    print(f"  Mood: {parsed_data['mood']}")
    print(f"  Instruments: {', '.join(parsed_data['instruments'])}")

    for instrument, part in scores.items():
        if MUSIC21_AVAILABLE:
            filename = f"{instrument}.musicxml"
            part.write("musicxml", fp=filename)
            notes = " ".join(n.nameWithOctave for n in part.notes)
            print(f"\n{instrument.title()} part -> {filename}\nNotes: {notes}")
        else:
            print(f"\n{instrument.title()} notes: {part}")


if __name__ == "__main__":
    main()