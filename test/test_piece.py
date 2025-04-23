import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.piece import Tetromino


class TestTetromino:
    def test_init(self):
        """Test tetromino initialization with specific shape"""
        piece = Tetromino(shape_idx=0)  # I-piece
        assert piece.shape_idx == 0
        assert piece.name == "I"
        assert len(piece.shape) == 1  # I-piece has 1 row
        assert len(piece.shape[0]) == 4  # I-piece has 4 columns

    def test_rotate_i_piece(self):
        """Test rotating I-piece"""
        piece = Tetromino(shape_idx=0)  # I-piece
        original_shape = [row[:] for row in piece.shape]  # Deep copy

        # Rotate once (90 degrees)
        piece.rotate()
        assert len(piece.shape) == 4  # Should now have 4 rows
        assert len(piece.shape[0]) == 1  # Should now have 1 column

        # Rotate again (180 degrees from original)
        piece.rotate()
        assert len(piece.shape) == 1  # Should be back to 1 row
        assert len(piece.shape[0]) == 4  # Should be back to 4 columns

        # Rotate twice more to complete full rotation
        piece.rotate()
        piece.rotate()

        # Should be back to original shape
        assert piece.shape == original_shape

    def test_rotate_o_piece(self):
        """Test rotating O-piece (should not change)"""
        piece = Tetromino(shape_idx=1)  # O-piece
        original_shape = [row[:] for row in piece.shape]  # Deep copy

        # Rotate
        piece.rotate()

        # Should be unchanged
        assert piece.shape == original_shape