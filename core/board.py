import services.config as config
from core.piece import Tetromino
from core.rules import calculate_score


class Board:
    def __init__(self, sounds=None):
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
        self.sounds = sounds or {}
        self.spawn_new_piece()

    def spawn_new_piece(self):
        """Spawns a new piece and checks for game over"""
        if self.next_piece:
            self.current_piece = self.next_piece
        else:
            self.current_piece = Tetromino()

        self.next_piece = Tetromino()

        # Check if any part of the new piece overlaps with existing blocks
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = self.current_piece.x + j
                    y = self.current_piece.y + i

                    # If the cell is within the grid and overlaps with an existing block
                    if 0 <= y < self.height and 0 <= x < self.width and self.grid[y][x]:
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

                    # Check if out of bounds horizontally or at the bottom
                    if x < 0 or x >= self.width or y >= self.height:
                        return False

                    # Check collision with existing pieces (even for cells above the grid)
                    if y >= 0 and y < self.height and x >= 0 and x < self.width and self.grid[y][x]:
                        return False

        return True

    def merge_piece(self):
        """Merge the current piece with the board"""
        if not self.current_piece:
            return False

        # Check if any part of the piece is above the grid
        piece_partly_above_grid = any(self.current_piece.y + i < 0 for i in range(len(self.current_piece.shape)))

        # Merge piece with the board
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    # Only merge cells that are within the grid
                    if 0 <= self.current_piece.y + i < self.height and 0 <= self.current_piece.x + j < self.width:
                        self.grid[self.current_piece.y + i][self.current_piece.x + j] = 1
                        self.colors[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color

        # Clear lines and update scores
        lines_cleared = self.clear_lines()

        # If part of the piece was above the grid, it's likely game over
        if piece_partly_above_grid:
           self.game_over = True
            # DON'T return here, continue to return after the game over check

        # Try to spawn a new piece
        if not self.spawn_new_piece() and not self.game_over:
           self.game_over = True

        return not self.game_over

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

        # Update score based on lines cleared
        if lines_cleared > 0:
            if lines_cleared == 1:
                self.score += 100 * self.level
                if 'line_clear' in self.sounds:
                    self.sounds['line_clear'].play()
            elif lines_cleared == 2:
                self.score += 300 * self.level
                if 'line_clear' in self.sounds:
                    self.sounds['line_clear'].play()
            elif lines_cleared == 3:
                self.score += 500 * self.level
                if 'line_clear' in self.sounds:
                    self.sounds['line_clear'].play()
            elif lines_cleared == 4:
                self.score += 800 * self.level
                if 'tetris' in self.sounds:
                    self.sounds['tetris'].play()

            # Update lines cleared count
            self.lines_cleared += lines_cleared

            # Calculate new level
            new_level = (self.lines_cleared // 10) + 1

            # Check if level has increased
            if new_level > self.level:
                # Level up!
                old_level = self.level
                self.level = new_level

                # Play level up sound
                if 'level_up' in self.sounds:
                    self.sounds['level_up'].play()

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
