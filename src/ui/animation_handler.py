"""animation_handler.py: Contains the animation handler for Minesweeper."""

import random
from time import sleep

import pygame

from cfg.constants import Constants
from src.models.grid import Grid


class AnimationHandler:
    """The animation handler for the Minesweeper game."""

    def __init__(self, grid: Grid, screen: pygame.Surface, assets: dict) -> None:
        """
        Initialises the animation handler.
        :param grid: The Minesweeper grid object.
        :param screen: The pygame screen object.
        :param assets: The assets for the Minesweeper game.
        :returns: None
        """
        self.grid = grid
        self.screen = screen
        self.assets = assets

    def reveal(self, row: int, col: int) -> None:
        """
        Animates the reveal of a cell in the Minesweeper grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: None
        """
        cell = self.grid.get_cell(row, col)
        final_image = self.grid.get_cell_image(cell)
        fading_surface = pygame.Surface((Constants.BOX_WIDTH, Constants.BOX_HEIGHT))
        fading_surface.blit(final_image, (0, 0))

        for alpha in range(0, 255, 15):
            fading_surface.set_alpha(alpha)
            self.screen.blit(
                fading_surface, (col * Constants.BOX_WIDTH, row * Constants.BOX_HEIGHT)
            )
            pygame.display.flip()
            sleep(0.001)

    def flag(self, row: int, col: int) -> None:
        """
        Animates the flagging of a cell in the Minesweeper grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: None
        """
        positions = [
            (Constants.BOX_WIDTH * 0.9, Constants.BOX_HEIGHT * 0.9),
            (Constants.BOX_WIDTH, Constants.BOX_HEIGHT),
            (Constants.BOX_WIDTH * 0.9, Constants.BOX_HEIGHT * 0.9),
        ]

        for position in positions:
            temp_image = self.assets["image_flag"].copy()
            image = pygame.transform.scale(
                temp_image, (int(position[0]), int(position[1]))
            )
            self.screen.blit(
                image,
                (
                    col * Constants.BOX_WIDTH
                    + (Constants.BOX_WIDTH - position[0]) // 2,
                    row * Constants.BOX_HEIGHT
                    + (Constants.BOX_HEIGHT - position[1]) // 2,
                ),
            )
            pygame.display.flip()
            sleep(0.1)

    def game_over(self) -> None:
        """
        Displays the game over animation.
        :returns: None
        """
        for i in range(5):
            self.screen.fill(Constants.GAME_OVER_COLOUR)
            pygame.display.flip()
            sleep(0.1)
            self.screen.fill(Constants.EMPTY_COLOUR)
            pygame.display.flip()
            sleep(0.1)

    def win(self) -> None:
        """
        Displays the win animation.
        :returns: None
        """
        for _ in range(100):
            colour = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            pygame.draw.circle(
                self.screen,
                colour,
                (
                    random.randint(0, self.grid.width * Constants.BOX_WIDTH),
                    random.randint(0, self.grid.height * Constants.BOX_HEIGHT),
                ),
                random.randint(10, 50),
            )
            pygame.display.flip()
            sleep(0.01)
