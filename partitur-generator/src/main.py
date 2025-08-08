import sys
from utils.text_parser import parse_text
from score.generator import ScoreGenerator

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <description_text>")
        return

    description = sys.argv[1]
    parsed_data = parse_text(description)
    
    score_generator = ScoreGenerator()
    scores = score_generator.generate_score(parsed_data)

    for instrument, score in scores.items():
        print(f"Score for {instrument}:")
        print(score)

if __name__ == "__main__":
    main()