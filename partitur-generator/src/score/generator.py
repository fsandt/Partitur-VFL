"""Utility module for constructing simple scores.

The implementation prefers :mod:`music21` for generating proper MusicXML
output.  If the library is not available, a lightweight text based
representation of the notes is returned instead so that the rest of the
application can still run.
"""

from typing import Dict, List

try:  # pragma: no cover - handled gracefully when dependency missing
    from music21 import instrument as m21instrument
    from music21 import note, stream
    MUSIC21_AVAILABLE = True
except ModuleNotFoundError:  # pragma: no cover
    m21instrument = None  # type: ignore
    note = stream = None  # type: ignore
    MUSIC21_AVAILABLE = False


class ScoreGenerator:
    """Create instrument parts based on parsed description data.

    The generator uses a few predefined pitch patterns for different moods.
    For each requested instrument a :class:`music21.stream.Part` is created and
    filled with notes from the pattern that matches the mood.  The returned
    dictionary maps instrument names to their respective streams.
    """

    MOOD_PATTERNS: Dict[str, List[str]] = {
        "happy": ["C5", "E5", "G5", "C6"],
        "sad": ["A4", "C5", "E5", "A5"],
        "energetic": ["C5", "D5", "E5", "G5", "A5", "C6"],
        "calm": ["C4", "E4", "G4", "E4"],
        "neutral": ["C4", "D4", "E4", "F4"],
    }

    if MUSIC21_AVAILABLE:
        INSTRUMENT_CLASSES = {
            "piano": m21instrument.Piano,
            "violin": m21instrument.Violin,
            "flute": m21instrument.Flute,
            "guitar": m21instrument.Guitar,
            "bass": m21instrument.Bass,
            "drums": m21instrument.Percussion,
        }
    else:
        INSTRUMENT_CLASSES = {}

    def generate_score(self, parsed_data: Dict[str, List[str]]) -> Dict[str, object]:
        """Generate score parts for each instrument described in ``parsed_data``.

        Args:
            parsed_data: Data returned by :func:`utils.text_parser.parse_text`.

        Returns:
            Dictionary mapping instrument names to ``music21`` parts (if the
            library is available) or simple strings of note names otherwise.
        """

        mood = parsed_data.get("mood", "neutral")
        instruments = parsed_data.get("instruments", [])
        pattern = self.MOOD_PATTERNS.get(mood, self.MOOD_PATTERNS["neutral"])

        scores: Dict[str, object] = {}
        for inst_name in instruments:
            if MUSIC21_AVAILABLE:
                part = stream.Part()
                inst_class = self.INSTRUMENT_CLASSES.get(inst_name, m21instrument.Instrument)
                part.insert(0, inst_class())
                for pitch in pattern:
                    part.append(note.Note(pitch))
                scores[inst_name] = part
            else:  # pragma: no cover - fallback when music21 missing
                scores[inst_name] = " ".join(pattern)

        return scores

