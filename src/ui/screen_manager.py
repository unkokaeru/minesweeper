"""screen_manager.py: Contains the screen manager for Minesweeper."""

from time import time

import pygame

from cfg.constants import Constants
from src.models.grid import Grid
from src.ui.animation_handler import AnimationHandler


class ScreenManager:
    """The screen manager for the Minesweeper game."""

    def __init__(
        self, grid: Grid, screen: pygame.Surface, animation_handler: AnimationHandler
    ) -> None:
        """
        Initialises the screen manager.
        :param grid: The Minesweeper grid object.
        :param screen: The pygame screen object.
        :returns: None
        """
        self.grid = grid
        self.screen = screen
        self.animation_handler = animation_handler

        self.font = pygame.font.Font(None, Constants.FONT_SIZE)

    def show_game_over(self) -> None:
        """
        Displays the game over screen.
        :returns: None
        """
        self.animation_handler.game_over()

        self.screen.fill(Constants.GAME_OVER_COLOUR)
        text = self.font.render("Game Over!", True, Constants.TEXT_COLOUR)
        self.screen.blit(
            text,
            (
                self.grid.width * Constants.BOX_HEIGHT // 2 - text.get_width() // 2,
                self.grid.height * Constants.BOX_WIDTH // 2 - text.get_height() // 2,
            ),
        )

    def show_win(self, start_time: float) -> bool:
        """
        Displays the win screen.
        :returns: True if the game is still running, False otherwise.
        """
        time_to_complete_raw = time() - start_time

        minutes = int(time_to_complete_raw // 60)
        seconds = int(time_to_complete_raw % 60)
        time_to_complete = (
            f"{minutes} minutes and {seconds} seconds"
            if minutes > 0
            else f"{seconds} seconds"
        )

        self.animation_handler.win()

        self.screen.fill(Constants.WIN_COLOUR)
        text = self.font.render("You win!", True, Constants.TEXT_COLOUR)
        self.screen.blit(
            text,
            (
                self.grid.width * Constants.BOX_HEIGHT // 2 - text.get_width() // 2,
                self.grid.height * Constants.BOX_WIDTH // 2 - text.get_height() // 2,
            ),
        )
        text = self.font.render(
            f"Time to complete: {time_to_complete}", True, Constants.TEXT_COLOUR
        )
        self.screen.blit(
            text,
            (
                self.grid.width * Constants.BOX_HEIGHT // 2 - text.get_width() // 2,
                self.grid.height * Constants.BOX_WIDTH // 2 + text.get_height(),
            ),
        )

    def display(self) -> None:
        """
        Displays the Minesweeper grid using pygame.
        :returns: None
        """
        self.screen.fill(Constants.EMPTY_COLOUR)

        for row in range(self.grid.height):
            for col in range(self.grid.width):
                cell = self.grid.get_cell(row, col)
                box_rect = (col * Constants.BOX_WIDTH, row * Constants.BOX_HEIGHT)

                image = self.grid.get_cell_image(cell)

                self.screen.blit(image, box_rect)
