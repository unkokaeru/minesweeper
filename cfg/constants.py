"""Contains the constants for Minesweeper."""


class Constants:
    """Stores the constants for Minesweeper."""

    def __init__(self):
        """Initializes the constants."""
        # Colors
        self.TEXT_COLOUR = (214, 214, 214)
        self.TEXT_BACKGROUND_COLOUR = (51, 51, 51)
        self.EMPTY_COLOUR = (51, 51, 51)
        self.FOG_COLOUR = (242, 129, 35)
        self.WIN_COLOUR = (93, 162, 113)
        self.GAME_OVER_COLOUR = (200, 70, 48)

        # Font size
        self.FONT_SIZE = 30

        # Window title
        self.WINDOW_TITLE = "Minesweeper"

        # Box dimensions
        self.BOX_WIDTH = 50
        self.BOX_HEIGHT = 50

        # Bomb percentages
        self.DIFFICULTY_PERCENTAGES = {
            "beginner": 5,
            "easy": 10,
            "medium": 15,
            "hard": 20,
            "expert": 25,
        }
