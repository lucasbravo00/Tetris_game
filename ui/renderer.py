import pygame
from enum import Enum, auto
from core.board import Board
import services.config as config
from ui.widgets import InputBox, Menu


class GameStates(Enum):
    TITLE = auto()
    NAME_ENTRY = auto()
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    HIGH_SCORES = auto()
    CONFIRM_NAME = auto()


class GameState:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def enter(self):
        """Called when entering this state"""
        pass

    def exit(self):
        """Called when exiting this state"""
        pass

    def handle_event(self, event):
        """Handle pygame events"""
        pass

    def update(self):
        """Update game logic"""
        pass

    def render(self):
        """Render the state"""
        pass


class TitleState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)

    def enter(self):
        # Start playing title music
        self.state_manager.audio_manager.play_music('title')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state_manager.change_state(GameStates.NAME_ENTRY)

    def render(self):
        self.state_manager.renderer.render_title_screen()


class NameEntryState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.input_box = InputBox(
            config.SCREEN_WIDTH // 2 - 100,
            config.SCREEN_HEIGHT // 2,
            200, 40
        )

    def handle_event(self, event):
        result = self.input_box.handle_event(event)
        if result == "ENTER" and self.input_box.text:
            self.state_manager.player_name = self.input_box.text
            self.state_manager.change_state(GameStates.MAIN_MENU)

    def update(self):
        self.input_box.update()

    def render(self):
        self.state_manager.renderer.render_name_entry(self.input_box)


class MainMenuState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.menu = Menu([
            "Start Game",
            "High Scores",
            "Exit"
        ])

    def handle_event(self, event):
        selection = self.menu.handle_event(event)
        if selection == "Start Game":
            self.state_manager.change_state(GameStates.PLAYING)
        elif selection == "High Scores":
            self.state_manager.change_state(GameStates.HIGH_SCORES)
        elif selection == "Exit":
            pygame.quit()
            exit()

    def render(self):
        self.state_manager.renderer.render_main_menu(self.menu)


class PlayingState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.board = None
        self.fall_time = 0
        self.last_time = 0
        self.key_repeat = {
            pygame.K_LEFT: {"pressed": False, "time": 0},
            pygame.K_RIGHT: {"pressed": False, "time": 0},
            pygame.K_DOWN: {"pressed": False, "time": 0}
        }

    def enter(self):
        """Called when entering playing state"""
        # Only create a new board if we don't have one yet
        if self.board is None:
            self.board = Board()
            self.fall_time = 0
            self.last_time = pygame.time.get_ticks()

            # Start playing game music
            self.state_manager.audio_manager.play_music('game')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state_manager.change_state(GameStates.PAUSED)
            elif event.key == pygame.K_UP:
                if self.board.rotate_piece():
                    self.state_manager.audio_manager.play_sound('rotate')
            elif event.key == pygame.K_SPACE:
                if self.board.hard_drop():
                    self.state_manager.audio_manager.play_sound('drop')
                else:
                    self.state_manager.audio_manager.play_sound('game_over')
                    self.state_manager.change_state(GameStates.GAME_OVER)

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        self.fall_time += delta_time

        # Handle key repeats for smoother movement
        keys = pygame.key.get_pressed()
        self._handle_key_repeats(keys, current_time)

        # Check for game over
        if self.board.game_over:
            self.state_manager.final_score = self.board.score
            self.state_manager.change_state(GameStates.GAME_OVER)
            return

        # Automatic falling
        drop_speed = config.get_drop_speed(self.board.level)
        if self.fall_time >= drop_speed:
            if not self.board.move_piece(dy=1):
                # Piece hit bottom, merge with board
                if not self.board.merge_piece():
                    self.state_manager.audio_manager.play_sound('game_over')
                    self.state_manager.change_state(GameStates.GAME_OVER)
            self.fall_time = 0

    def _handle_key_repeats(self, keys, current_time):
        # Handle left key
        if keys[pygame.K_LEFT]:
            if not self.key_repeat[pygame.K_LEFT]["pressed"]:
                self.board.move_piece(dx=-1)
                self.key_repeat[pygame.K_LEFT]["pressed"] = True
                self.key_repeat[pygame.K_LEFT]["time"] = current_time
            elif current_time - self.key_repeat[pygame.K_LEFT]["time"] > config.KEY_REPEAT_DELAY:
                if (current_time - self.key_repeat[pygame.K_LEFT][
                    "time"] - config.KEY_REPEAT_DELAY) % config.KEY_REPEAT_INTERVAL < 20:
                    self.board.move_piece(dx=-1)
        else:
            self.key_repeat[pygame.K_LEFT]["pressed"] = False

        # Handle right key
        if keys[pygame.K_RIGHT]:
            if not self.key_repeat[pygame.K_RIGHT]["pressed"]:
                self.board.move_piece(dx=1)
                self.key_repeat[pygame.K_RIGHT]["pressed"] = True
                self.key_repeat[pygame.K_RIGHT]["time"] = current_time
            elif current_time - self.key_repeat[pygame.K_RIGHT]["time"] > config.KEY_REPEAT_DELAY:
                if (current_time - self.key_repeat[pygame.K_RIGHT][
                    "time"] - config.KEY_REPEAT_DELAY) % config.KEY_REPEAT_INTERVAL < 20:
                    self.board.move_piece(dx=1)
        else:
            self.key_repeat[pygame.K_RIGHT]["pressed"] = False

        # Handle down key (soft drop)
        if keys[pygame.K_DOWN]:
            if not self.key_repeat[pygame.K_DOWN]["pressed"]:
                if not self.board.move_piece(dy=1):
                    if not self.board.merge_piece():
                        self.state_manager.audio_manager.play_sound('game_over')
                        self.state_manager.change_state(GameStates.GAME_OVER)
                self.key_repeat[pygame.K_DOWN]["pressed"] = True
                self.key_repeat[pygame.K_DOWN]["time"] = current_time
            elif current_time - self.key_repeat[pygame.K_DOWN]["time"] > config.KEY_REPEAT_DELAY:
                if (current_time - self.key_repeat[pygame.K_DOWN][
                    "time"] - config.KEY_REPEAT_DELAY) % config.KEY_REPEAT_INTERVAL < 20:
                    if not self.board.move_piece(dy=1):
                        if not self.board.merge_piece():
                            self.state_manager.audio_manager.play_sound('game_over')
                            self.state_manager.change_state(GameStates.GAME_OVER)
        else:
            self.key_repeat[pygame.K_DOWN]["pressed"] = False

    def render(self):
        self.state_manager.renderer.render_game(self.board)


class PausedState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.menu = Menu([
            "Resume",
            "Restart",
            "Main Menu"
        ])
        # Create a cached surface for the pause screen
        self.cached_screen = None

    def enter(self):
        # Pause music
        self.state_manager.audio_manager.pause_music()

        # Create the cached screen
        self._create_cached_screen()

    def _create_cached_screen(self):
        """Create a cached version of the pause screen to prevent flickering"""
        # First render the game in the background
        playing_state = self.state_manager.states[GameStates.PLAYING]
        self.state_manager.renderer.render_game(playing_state.board)

        # Create a copy of the current screen
        self.cached_screen = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.cached_screen.blit(self.state_manager.renderer.screen, (0, 0))

        # Add a semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Transparent black
        self.cached_screen.blit(overlay, (0, 0))

        # Draw pause text and initial menu state
        font = pygame.font.SysFont(None, 60)
        pause_text = font.render("PAUSED", True, config.WHITE)
        text_rect = pause_text.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 4))
        self.cached_screen.blit(pause_text, text_rect)

    def exit(self):
        # Resume music
        self.state_manager.audio_manager.unpause_music()
        self.cached_screen = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state_manager.change_state(GameStates.PLAYING, False)
                return

        # Call menu.handle_event and capture the selection
        selection = self.menu.handle_event(event)

        if selection == "Resume":
            self.state_manager.change_state(GameStates.PLAYING, False)
        elif selection == "Restart":
            self.state_manager.change_state(GameStates.PLAYING, True)
        elif selection == "Main Menu":
            self.state_manager.change_state(GameStates.MAIN_MENU)

    def render(self):
        # Use the cached background to avoid re-rendering the game
        if self.cached_screen:
            self.state_manager.renderer.screen.blit(self.cached_screen, (0, 0))

        # Just draw the menu on top (which could change as user navigates)
        self.menu.draw(self.state_manager.renderer.screen, config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2)

        pygame.display.update()


class GameOverState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.show_high_scores = False

    def enter(self):
        # Save the high score
        self.state_manager.audio_manager.play_sound('game_over')
        self.state_manager.audio_manager.stop_music()
        self.high_scores = self.state_manager.high_score_manager.save_score(
            self.state_manager.final_score,
            self.state_manager.player_name
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.show_high_scores:
                if event.key == pygame.K_RETURN:
                    self.state_manager.change_state(GameStates.CONFIRM_NAME)
                elif event.key == pygame.K_ESCAPE:
                    self.state_manager.change_state(GameStates.MAIN_MENU)
                elif event.key == pygame.K_h:
                    self.show_high_scores = True
            else:
                if event.key == pygame.K_b:
                    self.show_high_scores = False
                elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    if event.key == pygame.K_RETURN:
                        self.state_manager.change_state(GameStates.CONFIRM_NAME)
                    else:
                        self.state_manager.change_state(GameStates.MAIN_MENU)

    def render(self):
        self.state_manager.renderer.render_game_over(
            self.state_manager.final_score,
            self.state_manager.player_name,
            self.high_scores,
            self.show_high_scores
        )


class HighScoresState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)

    def enter(self):
        self.high_scores = self.state_manager.high_score_manager.load_scores()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_b):
                self.state_manager.change_state(GameStates.MAIN_MENU)

    def render(self):
        self.state_manager.renderer.render_high_scores(self.high_scores)


class ConfirmNameState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                self.state_manager.change_state(GameStates.PLAYING, reset=True)
            elif event.key == pygame.K_n:
                self.state_manager.change_state(GameStates.NAME_ENTRY)
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(GameStates.MAIN_MENU)

    def render(self):
        self.state_manager.renderer.render_confirm_name(self.state_manager.player_name)


class GameStateManager:
    def __init__(self, renderer, audio_manager, high_score_manager):
        self.renderer = renderer
        self.audio_manager = audio_manager
        self.high_score_manager = high_score_manager
        self.player_name = "Player"
        self.final_score = 0

        # Initialize all states
        self.states = {
            GameStates.TITLE: TitleState(self),
            GameStates.NAME_ENTRY: NameEntryState(self),
            GameStates.MAIN_MENU: MainMenuState(self),
            GameStates.PLAYING: PlayingState(self),
            GameStates.PAUSED: PausedState(self),
            GameStates.GAME_OVER: GameOverState(self),
            GameStates.HIGH_SCORES: HighScoresState(self),
            GameStates.CONFIRM_NAME: ConfirmNameState(self)
        }

        # Set initial state
        self.current_state = self.states[GameStates.TITLE]
        self.current_state.enter()

    def change_state(self, new_state_type, reset=False):
        """Change to a new game state"""
        # Exit current state
        self.current_state.exit()

        print(f"Changing state to {new_state_type}, reset={reset}")  # Debug log

        # If state is PLAYING and needs to be reset, recreate it
        if new_state_type == GameStates.PLAYING and reset:
            print("Resetting playing state")  # Debug
            self.states[GameStates.PLAYING] = PlayingState(self)

        # Set new state
        self.current_state = self.states[new_state_type]

        # Enter new state
        self.current_state.enter()

    def handle_event(self, event):
        self.current_state.handle_event(event)

    def update(self):
        self.current_state.update()

    def render(self):
        self.current_state.render()
