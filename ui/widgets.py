import pygame
import services.config as config
from ui.theme import COLORS, FONTS


class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLORS['WHITE']
        self.text = text
        self.font = pygame.font.SysFont(FONTS['main'], 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True
        self.cursor_visible = True
        self.last_cursor_update = pygame.time.get_ticks()
        self.cursor_blink_time = 500  # milliseconds

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return "ENTER"
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 15 and (event.unicode.isalnum() or event.unicode.isspace()):
                    self.text += event.unicode

                # Reset cursor blink timer on any key press
                self.cursor_visible = True
                self.last_cursor_update = pygame.time.get_ticks()

                # Re-render the text
                self.txt_surface = self.font.render(self.text, True, self.color)

        return None

    def update(self):
        # Update cursor visibility
        current_time = pygame.time.get_ticks()
        if current_time - self.last_cursor_update > self.cursor_blink_time:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_update = current_time

        # Resize the box if the text is too long
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Draw the input box
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Draw the current text
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

        # Draw the cursor
        if self.active and self.cursor_visible:
            cursor_pos = self.rect.x + 5 + self.txt_surface.get_width()
            pygame.draw.line(screen, self.color,
                             (cursor_pos, self.rect.y + 5),
                             (cursor_pos, self.rect.y + self.rect.h - 5), 2)


class Menu:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.font = pygame.font.SysFont(FONTS['main'], 30)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
                return None
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
                return None
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]

        return None

    def draw(self, screen, x, y):
        for i, option in enumerate(self.options):
            color = COLORS['CYAN'] if i == self.selected else COLORS['WHITE']
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(x, y + i * 40))
            screen.blit(text, rect)