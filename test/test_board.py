import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.board import Board
from core.piece import Tetromino


class TestBoard:
    def test_init(self):
        """Test board initialization"""
        board = Board()
        assert len(board.grid) == board.height
        assert len(board.grid[0]) == board.width
        assert board.score == 0
        assert board.lines_cleared == 0
        assert board.level == 1
        assert not board.game_over
        assert board.current_piece is not None
        assert board.next_piece is not None

    def test_is_valid_position(self):
        """Test position validation"""
        board = Board()

        # Force a specific piece and position
        board.current_piece = Tetromino(shape_idx=0)  # I-piece
        board.current_piece.x = 3
        board.current_piece.y = 0

        # Valid position
        assert board.is_valid_position()

        # Invalid position (out of bounds)
        assert not board.is_valid_position(x_offset=-4)  # Too far left
        assert not board.is_valid_position(x_offset=8)  # Too far right
        assert not board.is_valid_position(y_offset=20)  # Too far down

    def test_move_piece(self):
        """Test moving a piece"""
        board = Board()

        # Force a specific piece and position
        board.current_piece = Tetromino(shape_idx=0)  # I-piece
        board.current_piece.x = 3
        board.current_piece.y = 0

        # Move right
        original_x = board.current_piece.x
        board.move_piece(dx=1)
        assert board.current_piece.x == original_x + 1

        # Move left
        board.move_piece(dx=-1)
        assert board.current_piece.x == original_x

        # Move down
        original_y = board.current_piece.y
        board.move_piece(dy=1)
        assert board.current_piece.y == original_y + 1

    def test_rotate_piece(self):
        """Test rotating a piece"""
        board = Board()

        # Force a specific piece and position
        board.current_piece = Tetromino(shape_idx=0)  # I-piece
        board.current_piece.x = 3
        board.current_piece.y = 0

        original_shape = [row[:] for row in board.current_piece.shape]

        # Rotate
        assert board.rotate_piece()
        assert board.current_piece.shape != original_shape

    def test_clear_lines(self):
        """Test clearing completed lines"""
        board = Board()

        # Manually set up a grid with a complete line
        for j in range(board.width):
            board.grid[board.height - 1][j] = 1

        lines_cleared = board.clear_lines()
        assert lines_cleared == 1
        assert board.lines_cleared == 1

        # The bottom row should now be empty
        assert sum(board.grid[board.height - 1]) == 0