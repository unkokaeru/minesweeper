"""grid.py: Contains the grid model for Minesweeper."""

import random
from logging import Logger
from typing import List

import pygame

from cfg.constants import Constants
from src.models.cell import Cell


class Grid:
    """The Minesweeper grid."""

    def __init__(self, logger: Logger, width: int, height: int) -> None:
        """
        Initialises the grid.
        :param width: The width of the grid.
        :param height: The height of the grid.
        :returns: None
        """
        self.logger = logger

        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        self.revealed_count = 0

        self.assets = {}
        self._initialise_assets()

    def __str__(self) -> str:
        """
        Returns the string representation of the grid.
        :returns: The string representation of the grid.
        """
        return f"Grid(width={self.width}, height={self.height}, grid={self.grid})"

    def __repr__(self) -> str:
        """
        Returns the string representation of the grid.
        :returns: The string representation of the grid.
        """
        return self.__str__()

    def _initialise_assets(self) -> None:
        """
        Initialises the assets for the Minesweeper game.
        :returns: None
        """
        for name, path in Constants.ASSET_PATHS.items():
            try:
                self.assets[name] = pygame.transform.scale(
                    pygame.image.load(path),
                    (Constants.BOX_WIDTH, Constants.BOX_HEIGHT),
                )
            except FileNotFoundError as e:
                self.logger.exception(f"Failed to load {path}: {e}")

    def _count_adjacent_bombs(self, row: int, col: int) -> int:
        """
        Counts the number of adjacent bombs to a cell.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: The number of adjacent bombs.
        """
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i < self.height and 0 <= col + j < self.width:
                    adj_cell = self.get_cell(row + i, col + j)
                    if adj_cell.value == -1:
                        count += 1

        return count

    def get_cell_image(self, cell: Cell) -> pygame.Surface:
        """
        Retrieves the image of a cell in the Minesweeper grid.
        :param cell: The cell object.
        :returns: The image of the cell.
        """
        if cell.revealed:
            if cell.value == -1:
                return self.assets["image_bomb"]
            elif cell.value == 0:
                return self.assets["image_cell"]
            else:
                return self.assets[f"image_{cell.value}"]
        elif not cell.revealed:
            if cell.flagged:
                return self.assets["image_flag"]
            else:
                return self.assets["image_fog_sharp"]

    def get_cell(self, row: int, col: int) -> Cell:
        """
        Retrieves a cell from the grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: The cell object.
        """
        return self.grid[row][col]

    def generate(self, num_bombs: int) -> List[List[str]]:
        """
        Generates a Minesweeper grid.
        :param num_bombs: The number of bombs in the grid.
        :returns: A 2D list representing the grid.
        """
        # Generate bombs
        bomb_positions = random.sample(range(self.width * self.height), num_bombs)
        for position in bomb_positions:
            row, col = divmod(position, self.width)
            cell = self.get_cell(row, col)
            cell.value = -1

        # Generate numbers
        for row in range(self.height):
            for col in range(self.width):
                cell = self.get_cell(row, col)
                if cell.value == -1:
                    continue
                cell.value = self._count_adjacent_bombs(row, col)
