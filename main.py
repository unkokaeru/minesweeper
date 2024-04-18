"""main.py: Contains the main function for Minesweeper."""

from src.logging.log_manager import get_logger
from src.models.game_state import GameState

"""
TODO:
- Responsive Design (adjust to screen size) - resize all grid elements
- Game Statistics (real-time) - time taken, number of moves, bombs left, etc.
- High Scores
- Game Settings and Controls - difficulty, sound, controls
    (keyboard selection vs mouse selection), etc.
- Sound Effects - bomb explosion, flag placement, etc.
- Background Music - self-produced
- Interactive Tutorial - how to play Minesweeper
- Recreate the README.md - how to run the game, how to play Minesweeper
"""


def main() -> None:
    """A simple Minesweeper program."""
    logger = get_logger()

    minesweeper = GameState(logger)

    minesweeper.play()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program terminated by user.")
