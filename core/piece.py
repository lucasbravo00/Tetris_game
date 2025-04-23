import random
import services.config as config
from ui.theme import SHAPE_COLORS


class Tetromino:
    # Shape definitions (matrices)
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 1], [1, 1]],  # O
        [[1, 1, 1], [0, 1, 0]],  # T
        [[1, 1, 1], [1, 0, 0]],  # L
        [[1, 1, 1], [0, 0, 1]],  # J
        [[0, 1, 1], [1, 1, 0]],  # S
        [[1, 1, 0], [0, 1, 1]]  # Z
    ]

    # Names of shapes for reference
    SHAPE_NAMES = ["I", "O", "T", "L", "J", "S", "Z"]

    def __init__(self, shape_idx=None):
        """Initialize a new tetromino with random shape if not specified"""
        if shape_idx is None:
            shape_idx = random.randint(0, len(self.SHAPES) - 1)

        self.shape_idx = shape_idx
        self.shape = [row[:] for row in self.SHAPES[shape_idx]]  # Deep copy
        self.color = SHAPE_COLORS[shape_idx]
        self.x = config.GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = -len(self.shape)  # Start above visible grid
        self.name = self.SHAPE_NAMES[shape_idx]

    def rotate(self):
        """Rotate the piece 90 degrees clockwise"""
        # Special case for O piece (no rotation)
        if self.shape_idx == 1:  # O piece
            return

        # Transpose and reverse rows to rotate 90 degrees clockwise
        self.shape = [list(row) for row in zip(*self.shape[::-1])]