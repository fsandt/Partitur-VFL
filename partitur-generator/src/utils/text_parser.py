def parse_text(description):
    """
    Parses the input description text to extract relevant information for score generation.
    
    Args:
        description (str): The input description text.

    Returns:
        dict: A dictionary containing extracted information such as mood, instruments, and themes.
    """
    description = description.lower()

    moods = {
        "happy": ["happy", "joyful", "cheerful", "gl\u00fccklich"],
        "sad": ["sad", "melancholy", "down", "traurig"],
        "energetic": ["energetic", "fast", "aggressive", "energie"],
        "calm": ["calm", "peaceful", "serene", "ruhig"]
    }
    instruments = ["piano", "violin", "drums", "flute", "guitar", "bass"]

    selected_mood = "neutral"
    for mood, keywords in moods.items():
        if any(keyword in description for keyword in keywords):
            selected_mood = mood
            break

    selected_instruments = [inst for inst in instruments if inst in description]
    if not selected_instruments:
        selected_instruments = ["piano", "violin"]

    extracted_data = {
        "mood": selected_mood,
        "instruments": selected_instruments,
        "themes": []
    }

    return extracted_data