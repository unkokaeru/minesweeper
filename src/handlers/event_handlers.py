"""event_handlers.py: Contains the event handlers for Minesweeper."""

from time import sleep

import pygame

from src.logic.game_logic import GameLogic
from src.models.grid import Grid
from src.ui.screen_manager import ScreenManager


class MouseEventHandler:
    """The mouse event handler for the Minesweeper game."""

    def __init__(
        self, grid: Grid, game_logic: GameLogic, screen_manager: ScreenManager
    ) -> None:
        """
        Initialises the mouse event handler.
        :param grid: The Minesweeper grid object.
        :param game_logic: The game logic object.
        :returns: None
        """
        self.grid = grid
        self.game_logic = game_logic
        self.screen_manager = screen_manager

    def click(self, row: int, col: int, button: int) -> bool:
        """
        Handles a click on the Minesweeper grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :param button: The mouse button clicked.
        :returns: True if the game is still running, False otherwise.
        """
        cell = self.grid.get_cell(row, col)

        if button == 1:
            if cell.value == -1 and not cell.flagged:
                self.game_logic.reveal_cells(row, col)
                self.screen_manager.display()
                pygame.display.flip()
                sleep(1)
                self.screen_manager.show_game_over()
                return False
            elif cell.value == -1 and cell.flagged:
                return True
            else:
                self.game_logic.reveal_cells(row, col)
                return True
        elif button == 3:
            self.game_logic.flag_cell(row, col)
            return True
        elif button == 2:
            return True


class KeyEventHandler:
    """The key event handler for the Minesweeper game."""

    def __init__(self, grid: Grid, game_logic: GameLogic) -> None:
        """
        Initialises the key event handler.
        :param grid: The Minesweeper grid object.
        :param game_logic: The game logic object.
        :returns: None
        """
        self.grid = grid
        self.game_logic = game_logic

    def key_press(self, event) -> bool:
        """
        Handles a key press event.
        :param event: The key press event.
        :returns: True if reinitialisation is required, False otherwise.
        """
        DIFFICULTY_MAP = {
            pygame.K_1: "beginner",
            pygame.K_2: "easy",
            pygame.K_3: "medium",
            pygame.K_4: "hard",
            pygame.K_5: "expert",
        }

        if event.key in DIFFICULTY_MAP:
            self.difficulty = DIFFICULTY_MAP[event.key]
            return True
        elif event.key == pygame.K_r:
            return True
        elif event.key == pygame.K_EQUALS:
            self.grid.width += 1
            self.grid.height += 1
            return True
        elif event.key == pygame.K_MINUS:
            self.grid.width -= 1
            self.grid.height -= 1
            return True
        elif event.key == pygame.K_TAB:
            for row in range(self.grid.height):
                for col in range(self.grid.width):
                    cell = self.grid.get_cell(row, col)
                    cell.reveal()
            return False

        return False
