import os
from pathlib import Path

# Colors definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)

# Tetromino colors
SHAPE_COLORS = [
    CYAN,     # I
    YELLOW,   # O
    PURPLE,   # T
    ORANGE,   # L
    BLUE,     # J
    GREEN,    # S
    RED       # Z
]

# Default configuration
# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)  # Extra space for UI
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
HIGH_SCORES_FILE = os.path.join(BASE_DIR, 'data', 'high_scores.json')

# Game settings
FPS = 60
MAX_HIGH_SCORES = 10
SOUND_VOLUME = 0.6
MUSIC_VOLUME = 0.5

# Key repeat settings
KEY_REPEAT_DELAY = 200  # milliseconds before first repeat
KEY_REPEAT_INTERVAL = 70  # milliseconds between repeats

# Create necessary directories
os.makedirs(os.path.dirname(HIGH_SCORES_FILE), exist_ok=True)
os.makedirs(os.path.join(ASSETS_DIR, 'sounds'), exist_ok=True)
os.makedirs(os.path.join(ASSETS_DIR, 'music'), exist_ok=True)

# Helper functions
def get_drop_speed(level):
    """Return the drop speed in seconds for a given level"""
    # Formula: 1.0 - (level - 1) * 0.05, minimum 0.05
    speed = 1.0 - (level - 1) * 0.05
    return max(0.05, speed)