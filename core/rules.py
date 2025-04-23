from enum import Enum, auto

class GameMode(Enum):
    NORMAL = auto()
    SPRINT = auto()
    MARATHON = auto()

class Difficulty(Enum):
    EASY = auto()
    NORMAL = auto()
    HARD = auto()

# Scoring system
def calculate_score(lines_cleared, level):
    """Calculate score based on lines cleared and current level"""
    if lines_cleared == 1:
        return 100 * level
    elif lines_cleared == 2:
        return 300 * level
    elif lines_cleared == 3:
        return 500 * level
    elif lines_cleared == 4:
        return 800 * level
    return 0

# Drop speed in seconds based on level
def get_drop_speed(level):
    """Return the drop speed in seconds for a given level"""
    # Formula: 1.0 - (level - 1) * 0.05, minimum 0.05
    speed = 1.0 - (level - 1) * 0.05
    return max(0.05, speed)

# Level progression based on lines cleared
def calculate_level(lines_cleared):
    """Calculate level based on lines cleared"""
    return (lines_cleared // 10) + 1