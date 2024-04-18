"""game_logic.py: Contains the game logic for Minesweeper."""

import math
from heapq import heappop, heappush

from src.models.grid import Grid
from src.ui.animation_handler import AnimationHandler
from src.ui.screen_manager import ScreenManager


class GameLogic:
    """The game logic for the Minesweeper game."""

    def __init__(
        self,
        grid: Grid,
        animation_handler: AnimationHandler,
        screen_manager: ScreenManager,
    ) -> None:
        """
        Initialises the game logic.
        :param grid: The Minesweeper grid object.
        :param animation_handler: The animation handler object.
        :param screen_manager: The screen manager object.
        :returns: None
        """
        self.grid = grid
        self.animation_handler = animation_handler
        self.screen_manager = screen_manager

    def reveal_cells(self, start_row: int, start_col: int) -> None:
        """
        Reveals cells in the Minesweeper grid.
        :param revealed_count: The number of cells revealed.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: None
        """
        # Use a priority queue to sort cells by their distance from the initial click
        priority_queue = []
        heappush(priority_queue, (0, start_row, start_col))  # (distance, row, col)

        revealed = set()  # To avoid re-adding the same cell

        while priority_queue:
            distance, row, col = heappop(priority_queue)

            # Ensure the cell indices are within grid boundaries
            if row < 0 or row >= self.grid.height or col < 0 or col >= self.grid.width:
                continue

            # Retrieve the cell value and revealed status
            cell = self.grid.get_cell(row, col)

            # Stop if the cell is already revealed or flagged
            if cell.revealed or cell.flagged:
                continue

            # Mark the cell as revealed
            cell.reveal()
            self.animation_handler.reveal(row, col)

            # Increment the number of revealed cells
            self.grid.revealed_count += 1

            # If the cell is a bomb or has adjacent bombs, stop further revealing
            if cell.value != 0:
                continue

            # Add all adjacent cells to the queue, prioritized by their distance from the click
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_row, new_col = row + i, col + j
                    if (
                        (new_row, new_col) not in revealed and i != 0 or j != 0
                    ):  # Skip the current cell
                        revealed.add((new_row, new_col))
                        dist = math.sqrt(
                            (new_row - start_row) ** 2 + (new_col - start_col) ** 2
                        )
                        heappush(priority_queue, (dist, new_row, new_col))

    def flag_cell(self, row: int, col: int) -> None:
        """
        Flags a cell in the Minesweeper grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: None
        """
        cell = self.grid.get_cell(row, col)

        if not cell.revealed:
            cell.flag()
            self.animation_handler.flag(row, col)
