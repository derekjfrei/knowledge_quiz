def get_level():
    """Get quiz level from user input with default fallback."""
    level = input("Level (undergrad/grad) [default: undergrad]: ").strip().lower()
    if level not in ("undergrad", "grad"):
        level = "undergrad"
    return level


def get_topic():
    """Get quiz topic from user input with default fallback."""
    topic = input("Enter a quiz topic (press Enter to use 'TCP vs UDP'): ").strip()
    if not topic:
        topic = "TCP vs UDP"
    return topic


def get_difficulty():
    """Get quiz difficulty from user input with default fallback."""
    difficulty = input("Difficulty (easy/medium/hard) [default: medium]: ").strip().lower()
    if difficulty not in ("easy", "medium", "hard"):
        difficulty = "medium"
    return difficulty
