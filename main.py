"""A simple Minesweeper program"""

from src.game_logic import Minesweeper
from src.log_manager import get_logger

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
"""


def main() -> None:
    """
    A simple Minesweeper program.
    :returns: None
    """
    logger = get_logger()

    minesweeper = Minesweeper(
        logger, 10, 10, "easy"
    )  # 10x10 grid, easy difficulty - default

    minesweeper.play_game()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        get_logger.info("Program terminated by user.")
