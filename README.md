# Tetris Game

## Overview
This is a Python implementation of the classic game Tetris using the Pygame library. The main objective of this project was to practice implementing the Model-View-Controller (MVC) architecture in a game development context. The clean MVC structure separates game logic (Model), visuals (View), and user input handling (Controller), making the code more maintainable, extensible, and easier to understand.

## Features
- Classic Tetris gameplay with all 7 standard tetrominoes (I, O, T, L, J, S, Z)
- Progressive difficulty - game speed increases with each level
- Scoring system based on line clears
- High score tracking with player names
- Pause functionality
- Preview of the next piece

## Controls
- **Left/Right Arrow Keys**: Move the current piece horizontally
- **Down Arrow Key**: Soft drop (accelerate piece downward)
- **Up Arrow Key**: Rotate the current piece clockwise
- **Space Bar**: Hard drop (immediately place the piece at the lowest possible position)
- **P Key**: Pause/unpause the game

## Game Rules
- Each cleared line awards points:
  - 1 line: 100 points × current level
  - 2 lines: 300 points × current level
  - 3 lines: 500 points × current level
  - 4 lines: 800 points × current level (Tetris)
- Every 10 lines cleared increases the level by 1
- Each level increases the falling speed of the pieces
- The game ends when a new piece cannot be placed on the board

## Requirements
- Python 3.x
- Pygame library

## Installation
1. Make sure you have Python 3 installed on your system
2. Install Pygame using pip:
   ```
   pip install pygame
   ```
3. Clone or download this repository

## Project Structure
The game follows the MVC architecture:

```
tetris/
├── main.py              # Entry-point, owns pygame window & main loop
├── core/
│   ├── board.py         # Board (grid, line-clearing, collision)
│   ├── piece.py         # Tetromino dataclass + rotation logic
│   ├── rules.py         # Score table, speed curve, enums
│   └── state.py         # Finite-state machine (Start, Playing, GameOver, etc.)
├── ui/
│   ├── renderer.py      # Knows how to draw Board & texts on a surface
│   ├── widgets.py       # Menus, blinking cursor, etc.
│   └── theme.py         # Colours & fonts in one place
├── services/
│   ├── audio.py         # Music + SFX, thin wrapper over pygame.mixer
│   ├── highscores.py    # CRUD on JSON, injected into GameOver screen
│   └── config.py        # Configuration settings
└── assets/              # Sound effects and music files
    ├── sounds/
    └── music/
```

## How to Run
Execute the main.py file:
```
python main.py
```

## Credits
This game was developed as an educational project to demonstrate game development concepts and proper software architecture principles in Python.

## License
This project is released under the MIT License.
