import pygame
import services.config as config
from ui.theme import COLORS, FONTS


class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def _draw_text(self, text, size, x, y, color=COLORS['WHITE'], centered=True):
        """Helper function to draw text on screen"""
        font = pygame.font.SysFont(FONTS['main'], size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if centered:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)

        self.screen.blit(text_surface, text_rect)

        return text_rect

    def render_title_screen(self):
        """Render the title screen"""
        self.screen.fill(COLORS['BLACK'])

        # Draw title
        self._draw_text("TETRIS", 80, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4, COLORS['CYAN'])

        # Draw instructions
        self._draw_text("Press ENTER to Start", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2,
                        COLORS['WHITE'])

        pygame.display.update()

    def render_name_entry(self, input_box):
        """Render the name entry screen"""
        self.screen.fill(COLORS['BLACK'])

        # Draw title
        self._draw_text("ENTER YOUR NAME", 40, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4, COLORS['CYAN'])

        # Draw input box
        input_box.draw(self.screen)

        # Draw instructions
        self._draw_text("Press ENTER when done", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 3 // 4,
                        COLORS['WHITE'])

        pygame.display.update()

    def render_main_menu(self, menu):
        """Render the main menu"""
        self.screen.fill(COLORS['BLACK'])

        # Draw title
        self._draw_text("TETRIS", 80, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4, COLORS['CYAN'])

        # Draw menu
        menu.draw(self.screen, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        pygame.display.update()

    def render_game(self, board):
        """Render the game board and current piece"""
        self.screen.fill(config.BLACK)

        # Draw the grid
        for i in range(board.height):
            for j in range(board.width):
                if board.grid[i][j]:
                    pygame.draw.rect(
                        self.screen,
                        board.colors[i][j],
                        [j * config.BLOCK_SIZE, i * config.BLOCK_SIZE, config.BLOCK_SIZE, config.BLOCK_SIZE]
                    )
                    pygame.draw.rect(
                        self.screen,
                        config.WHITE,
                        [j * config.BLOCK_SIZE, i * config.BLOCK_SIZE, config.BLOCK_SIZE, config.BLOCK_SIZE],
                        1
                    )

        # Draw a separation line between game board and UI area
        pygame.draw.line(
            self.screen,
            config.WHITE,
            (board.width * config.BLOCK_SIZE, 0),
            (board.width * config.BLOCK_SIZE, config.SCREEN_HEIGHT),
            2
        )

        # Draw the current piece
        self._draw_tetromino(board.current_piece)

        # Draw next piece preview
        self._draw_next_piece(board.next_piece)

        # Draw the score information
        self._draw_text(f"Score: {board.score}", 30, config.SCREEN_WIDTH - 100, 30, config.WHITE, centered=False)
        self._draw_text(f"Level: {board.level}", 30, config.SCREEN_WIDTH - 100, 60, config.WHITE, centered=False)
        self._draw_text(f"Lines: {board.lines_cleared}", 30, config.SCREEN_WIDTH - 100, 90, config.WHITE,
                        centered=False)

        pygame.display.update()

    def render_game_over(self, score, player_name, high_scores, show_high_scores=False):
        """Render the game over screen"""
        self.screen.fill(config.BLACK)

        if not show_high_scores:
            # Draw game over message
            self._draw_text("GAME OVER", 60, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4, config.RED)

            # Draw final score with player name
            self._draw_text(f"{player_name}: {score} pts", 35, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 40,
                            config.WHITE)

            # Draw options
            self._draw_text("Press H to view High Scores", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 20,
                            config.CYAN)
            self._draw_text("Press ENTER to Play Again", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 80,
                            config.WHITE)
            self._draw_text("Press ESC to Quit", 25, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 120,
                            config.WHITE)
        else:
            # Draw high scores screen
            self._draw_text("HIGH SCORES", 50, config.SCREEN_WIDTH // 2, 50, config.YELLOW)

            # Check if this score is a new high score (in top 3)
            is_new_high_score = False
            for i, hs in enumerate(high_scores[:3]):
                if hs['score'] == score and hs['name'] == player_name and i < 3:
                    is_new_high_score = True

            if is_new_high_score:
                self._draw_text("NEW HIGH SCORE!", 35, config.SCREEN_WIDTH // 2, 100, config.GREEN)

            # Display top scores (maximum 8 to fit on screen)
            start_y = 150
            for i, hs in enumerate(high_scores[:8]):
                color = config.CYAN if hs['score'] == score and hs['name'] == player_name else config.WHITE
                self._draw_text(f"{i + 1}. {hs['name']}: {hs['score']} pts",
                                25, config.SCREEN_WIDTH // 2, start_y + i * 35, color)

            # Back button
            self._draw_text("Press B to go Back", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50, config.WHITE)

        pygame.display.update()

    def render_confirm_name(self, player_name):
        """Render the name confirmation screen"""
        self.screen.fill(config.BLACK)

        self._draw_text(f"Current Name: {player_name}", 40, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 3,
                        config.WHITE)
        self._draw_text("Keep this name?", 35, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2, config.CYAN)
        self._draw_text("Y - Yes", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 2 // 3, config.WHITE)
        self._draw_text("N - No", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 2 // 3 + 40, config.WHITE)

        pygame.display.update()

    def _draw_tetromino(self, tetromino):
        """Draw a tetromino on the screen"""
        for i, row in enumerate(tetromino.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        tetromino.color,
                        [(tetromino.x + j) * config.BLOCK_SIZE, (tetromino.y + i) * config.BLOCK_SIZE,
                         config.BLOCK_SIZE, config.BLOCK_SIZE]
                    )
                    pygame.draw.rect(
                        self.screen,
                        COLORS['WHITE'],
                        [(tetromino.x + j) * config.BLOCK_SIZE, (tetromino.y + i) * config.BLOCK_SIZE,
                         config.BLOCK_SIZE, config.BLOCK_SIZE],
                        1
                    )

    def _draw_next_piece(self, next_piece):
        """Draw the next piece preview"""
        # Draw preview box
        preview_x = config.SCREEN_WIDTH - 160
        preview_y = 200

        # Draw "Next" text
        self._draw_text("Next:", 30, preview_x, preview_y - 30, COLORS['WHITE'], centered=False)

        # Draw box outline
        box_size = 140
        pygame.draw.rect(self.screen, COLORS['WHITE'],
                         [preview_x, preview_y, box_size, box_size], 1)

        # Calculate center position for the piece
        offset_x = preview_x + box_size // 2 - (len(next_piece.shape[0]) * config.BLOCK_SIZE) // 2
        offset_y = preview_y + box_size // 2 - (len(next_piece.shape) * config.BLOCK_SIZE) // 2

        # Draw next piece
        for i, row in enumerate(next_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        next_piece.color,
                        [offset_x + j * config.BLOCK_SIZE, offset_y + i * config.BLOCK_SIZE,
                         config.BLOCK_SIZE, config.BLOCK_SIZE]
                    )
                    pygame.draw.rect(
                        self.screen,
                        COLORS['WHITE'],
                        [offset_x + j * config.BLOCK_SIZE, offset_y + i * config.BLOCK_SIZE,
                         config.BLOCK_SIZE, config.BLOCK_SIZE],
                        1
                    )

                def render_pause_menu(self, menu):
                    """Render the pause menu overlay"""
                    # Create a semi-transparent overlay
                    overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))  # Transparent black
                    self.screen.blit(overlay, (0, 0))

                    # Draw pause text
                    self._draw_text("PAUSED", 60, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4, COLORS['WHITE'])

                    # Draw menu
                    menu.draw(self.screen, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

                    pygame.display.update()

                def render_game_over(self, score, player_name, high_scores, show_high_scores):
                    """Render the game over screen"""
                    self.screen.fill(COLORS['BLACK'])

                    if not show_high_scores:
                        # Draw game over message
                        self._draw_text("GAME OVER", 60, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4,
                                        COLORS['RED'])

                        # Draw final score with player name
                        self._draw_text(f"{player_name}: {score} pts", 35, config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT // 2 - 40, COLORS['WHITE'])

                        # Draw options
                        self._draw_text("Press H to view High Scores", 30, config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT // 2 + 20, COLORS['CYAN'])
                        self._draw_text("Press ENTER to Play Again", 30, config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT // 2 + 80, COLORS['WHITE'])
                        self._draw_text("Press ESC to Quit", 25, config.SCREEN_WIDTH // 2,
                                        config.SCREEN_HEIGHT // 2 + 120, COLORS['WHITE'])
                    else:
                        # Draw high scores screen
                        self._draw_text("HIGH SCORES", 50, config.SCREEN_WIDTH // 2, 50, COLORS['YELLOW'])

                        # Check if this score is a new high score (in top 3)
                        is_new_high_score = False
                        for i, hs in enumerate(high_scores[:3]):
                            if hs['score'] == score and hs['name'] == player_name and i < 3:
                                is_new_high_score = True

                        if is_new_high_score:
                            self._draw_text("NEW HIGH SCORE!", 35, config.SCREEN_WIDTH // 2, 100, COLORS['GREEN'])

                        # Display top scores (maximum 8 to fit on screen)
                        start_y = 150
                        for i, hs in enumerate(high_scores[:8]):
                            color = COLORS['CYAN'] if hs['score'] == score and hs['name'] == player_name else COLORS[
                                'WHITE']
                            self._draw_text(f"{i + 1}. {hs['name']}: {hs['score']} pts",
                                            25, config.SCREEN_WIDTH // 2, start_y + i * 35, color)

                        # Back button
                        self._draw_text("Press B to go Back", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50,
                                        COLORS['WHITE'])

                    pygame.display.update()

                def render_high_scores(self, high_scores):
                    """Render the high scores screen"""
                    self.screen.fill(COLORS['BLACK'])

                    # Draw title
                    self._draw_text("HIGH SCORES", 50, config.SCREEN_WIDTH // 2, 50, COLORS['YELLOW'])

                    # Display scores
                    start_y = 150
                    if high_scores:
                        for i, hs in enumerate(high_scores[:10]):
                            self._draw_text(f"{i + 1}. {hs['name']}: {hs['score']} pts",
                                            25, config.SCREEN_WIDTH // 2, start_y + i * 35, COLORS['WHITE'])
                    else:
                        self._draw_text("No high scores yet!", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2,
                                        COLORS['WHITE'])

                    # Back button
                    self._draw_text("Press any key to return", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50,
                                    COLORS['WHITE'])

                    pygame.display.update()

                def render_confirm_name(self, player_name):
                    """Render the name confirmation screen"""
                    self.screen.fill(COLORS['BLACK'])

                    self._draw_text(f"Current Name: {player_name}", 40, config.SCREEN_WIDTH // 2,
                                    config.SCREEN_HEIGHT // 3, COLORS['WHITE'])
                    self._draw_text("Keep this name?", 35, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2,
                                    COLORS['CYAN'])
                    self._draw_text("Y - Yes", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 2 // 3,
                                    COLORS['WHITE'])
                    self._draw_text("N - No", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT * 2 // 3 + 40,
                                    COLORS['WHITE'])

                    pygame.display.update()

    def render_high_scores(self, high_scores):
        """Render the high scores screen"""
        self.screen.fill(config.BLACK)

        # Draw title
        self._draw_text("HIGH SCORES", 50, config.SCREEN_WIDTH // 2, 50, config.YELLOW)

        # Display scores
        start_y = 150
        if high_scores:
            for i, hs in enumerate(high_scores[:10]):
                self._draw_text(f"{i + 1}. {hs['name']}: {hs['score']} pts",
                                25, config.SCREEN_WIDTH // 2, start_y + i * 35, config.WHITE)
        else:
            self._draw_text("No high scores yet!", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2,
                            config.WHITE)

        # Back button
        self._draw_text("Press ENTER to return", 30, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50,
                        config.WHITE)

        pygame.display.update()

    def render_pause_menu(self, menu):
        """Render the pause menu overlay"""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Transparent black
        self.screen.blit(overlay, (0, 0))

        # Draw pause text
        self._draw_text("PAUSED", 60, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4, config.WHITE)

        # Draw menu
        menu.draw(self.screen, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        pygame.display.update()
