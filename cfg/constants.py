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

        # Asset paths
        self.ASSET_PATHS = {
            "image_1": "assets/1.png",
            "image_2": "assets/2.png",
            "image_3": "assets/3.png",
            "image_4": "assets/4.png",
            "image_5": "assets/5.png",
            "image_6": "assets/6.png",
            "image_7": "assets/7.png",
            "image_8": "assets/8.png",
            "image_bomb": "assets/bomb.png",
            "image_flag": "assets/flag.png",
            "image_fog_round": "assets/fog_rounded.png",
            "image_fog_sharp": "assets/fog_sharp.png",
            "image_cell": "assets/cell.png",
        }
