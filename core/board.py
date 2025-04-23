import services.config as config
from core.piece import Tetromino
from core.rules import calculate_score


class Board:
    def __init__(self):
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.colors = [[config.BLACK for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.spawn_new_piece()

    def spawn_new_piece(self):
        """Spawns a new piece and checks for game over"""
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = Tetromino()

        self.next_piece = Tetromino()

        # Check if the new piece can be placed
        if not self.is_valid_position():
            self.game_over = True
            return False

        return True

    def is_valid_position(self, piece=None, x_offset=0, y_offset=0):
        """Check if the piece can be placed at the given position"""
        piece = piece or self.current_piece

        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = piece.x + j + x_offset
                    y = piece.y + i + y_offset

                    # Check if out of bounds or collides with another block
                    if (x < 0 or x >= self.width or
                            y >= self.height or
                            (y >= 0 and self.grid[y][x])):
                        return False

        return True

    def merge_piece(self):
        """Merge the current piece with the board"""
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell and self.current_piece.y + i >= 0:
                    self.grid[self.current_piece.y + i][self.current_piece.x + j] = 1
                    self.colors[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

        # Check for completed lines
        lines = self.clear_lines()

        # Update score based on lines cleared
        if lines > 0:
            points = calculate_score(lines, self.level)
            self.score += points
            self.lines_cleared += lines

            # Update level (every 10 lines)
            self.level = (self.lines_cleared // 10) + 1

        # Spawn a new piece
        return self.spawn_new_piece()

    def clear_lines(self):
        """Clear completed lines and return the number of lines cleared"""
        lines_cleared = 0

        for i in range(self.height):
            if all(self.grid[i]):
                lines_cleared += 1

                # Move all lines above down
                for j in range(i, 0, -1):
                    self.grid[j] = self.grid[j - 1][:]
                    self.colors[j] = self.colors[j - 1][:]

                # Clear the top line
                self.grid[0] = [0] * self.width
                self.colors[0] = [config.BLACK] * self.width

        return lines_cleared

    def move_piece(self, dx=0, dy=0):
        """Move the current piece if valid"""
        if self.is_valid_position(x_offset=dx, y_offset=dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_piece(self):
        """Rotate the current piece if valid"""
        original_shape = self.current_piece.shape
        self.current_piece.rotate()

        if not self.is_valid_position():
            # Try wall kicks (adjust x position if rotation puts piece against wall)
            for dx in [-1, 1, -2, 2]:
                if self.is_valid_position(x_offset=dx):
                    self.current_piece.x += dx
                    return True

            # Revert rotation if all wall kicks fail
            self.current_piece.shape = original_shape
            return False

        return True

    def hard_drop(self):
        """Drop the piece to the lowest valid position"""
        drop_distance = 0
        while self.move_piece(dy=1):
            drop_distance += 1

        # Give score for hard drop (2 points per cell dropped)
        self.score += drop_distance * 2

        # Merge the piece with the board
        return self.merge_piece()