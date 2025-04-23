# Colors definition
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'CYAN': (0, 255, 255),
    'BLUE': (0, 0, 255),
    'ORANGE': (255, 165, 0),
    'YELLOW': (255, 255, 0),
    'GREEN': (0, 255, 0),
    'PURPLE': (128, 0, 128),
    'RED': (255, 0, 0),
    'DARK_GRAY': (50, 50, 50),
    'LIGHT_GRAY': (200, 200, 200)
}

# Tetromino colors
SHAPE_COLORS = [
    COLORS['CYAN'],     # I
    COLORS['YELLOW'],   # O
    COLORS['PURPLE'],   # T
    COLORS['ORANGE'],   # L
    COLORS['BLUE'],     # J
    COLORS['GREEN'],    # S
    COLORS['RED']       # Z
]

# Fonts
FONTS = {
    'main': None,  # Default system font
    'title': None  # Default system font
}

# UI theme settings
UI_THEME = {
    'background': COLORS['BLACK'],
    'text': COLORS['WHITE'],
    'highlight': COLORS['CYAN'],
    'border': COLORS['WHITE'],
    'button': COLORS['DARK_GRAY'],
    'button_hover': COLORS['LIGHT_GRAY']
}