import pygame
import sys
from core.state import GameState, GameStateManager
from ui.renderer import Renderer
from services.audio import AudioManager
from services.highscores import HighScoreManager
import services.config as config


def main():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()

    # Create the screen
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    # Initialize services
    audio_manager = AudioManager()
    high_score_manager = HighScoreManager()

    # Initialize renderer
    renderer = Renderer(screen)

    # Initialize game state manager
    state_manager = GameStateManager(renderer, audio_manager, high_score_manager)

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pass event to current state
            state_manager.handle_event(event)

        # Update current state
        state_manager.update()

        # Render current state
        state_manager.render()

        # Cap the frame rate
        clock.tick(config.FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()