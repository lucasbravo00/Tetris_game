import pygame
import os
import services.config as config


class AudioManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()

        # Sound dictionaries
        self.sounds = {}
        self.music = {}

        # Load audio files
        self._load_sounds()
        self._load_music()

    def _load_sounds(self):
        """Load sound effects"""
        try:
            # Create assets directory if it doesn't exist
            if not os.path.exists(config.ASSETS_DIR):
                os.makedirs(config.ASSETS_DIR)
                print(f"Created '{config.ASSETS_DIR}' directory. Please add sound files.")
                return

            # Define sound files to load
            sound_files = {
                'line_clear': 'line_clear.wav',
                'rotate': 'rotate.wav',
                'drop': 'drop.wav',
                'game_over': 'game_over.wav',
                'tetris': 'tetris.wav',  # Special sound for 4 lines
                'level_up': 'level_up.wav',
                'menu_select': 'menu_select.wav',
                'menu_move': 'menu_move.wav'
            }

            # Load each sound file if it exists
            for sound_name, file_name in sound_files.items():
                file_path = os.path.join(config.ASSETS_DIR, 'sounds', file_name)
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    self.sounds[sound_name].set_volume(config.SOUND_VOLUME)
                else:
                    print(f"Sound file not found: {file_path}")

        except pygame.error as e:
            print(f"Error loading sounds: {e}")

    def _load_music(self):
        """Load music tracks"""
        try:
            # Define music files to load
            music_files = {
                'title': 'title_theme.mp3',
                'game': 'game_theme.mp3',
                'high_score': 'high_score_theme.mp3'
            }

            # Store paths for music files
            for music_name, file_name in music_files.items():
                file_path = os.path.join(config.ASSETS_DIR, 'music', file_name)
                if os.path.exists(file_path):
                    self.music[music_name] = file_path
                else:
                    print(f"Music file not found: {file_path}")

        except Exception as e:
            print(f"Error loading music paths: {e}")

    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found")

    def play_music(self, music_name):
        """Play a music track with looping"""
        if music_name in self.music:
            try:
                pygame.mixer.music.load(self.music[music_name])
                pygame.mixer.music.set_volume(config.MUSIC_VOLUME)
                pygame.mixer.music.play(-1)  # -1 for infinite loop
            except pygame.error as e:
                print(f"Error playing music '{music_name}': {e}")
        else:
            print(f"Music '{music_name}' not found")

    def stop_music(self):
        """Stop the currently playing music"""
        pygame.mixer.music.stop()

    def pause_music(self):
        """Pause the currently playing music"""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """Unpause the currently playing music"""
        pygame.mixer.music.unpause()

    def set_sound_volume(self, volume):
        """Set the volume for all sound effects"""
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def set_music_volume(self, volume):
        """Set the volume for music"""
        pygame.mixer.music.set_volume(volume)