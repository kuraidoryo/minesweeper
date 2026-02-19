# Minesweeper

Welcome to Minesweeper! 💣

A classic Minesweeper game written in Python using the `curses` library. It supports both English and Polish (EN/PL) languages.

## How to Play

- **Move the Cursor**: Use the **WASD** keys to move the cursor (up, down, left, right).
- **Reveal a Cell**: Press **E** to reveal a cell.
- **Place/Remove Flag**: Press **F** to place or remove a flag on a cell.
- **Avoid Mines**: Don't reveal cells with mines!
- **Pause/Leave Game**: Press **P** to pause the game, or **Q** to quit to the main menu.

## Features

- Language switching between English and Polish
- First reveal is always safe (mines are placed after first click)
- Flood fill algorithm for revealing empty areas
- Flag counter to track remaining mines
- Real-time timer
- High score persistence (best time saved locally)
- Pause and resume functionality
- Dynamic board sizing based on terminal size

## Prerequisites

1. Python 3.10 or higher is recommended (for `match`-case syntax support)
2. `curses` library (comes pre-installed with Python on Linux/Mac. For Windows, install `windows-curses`):
   ```bash
   pip install windows-curses
   ```

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/kuraidoryo/minesweeper.git
   ```
2. Navigate to the project folder:
   ```bash
   cd minesweeper
   ```
3. Run the game:
   ```bash
   python minesweeper.py
   ```

---

**Enjoy the Game and Have Fun! 💣**

## Author

Developed by Kuraidoryo ✨
