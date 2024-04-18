"""game_state.py: Contains the game state for Minesweeper."""

from logging import Logger
from time import sleep, time

import pygame

from cfg.constants import Constants
from src.logic.game_logic import GameLogic
from src.handlers.event_handlers import KeyEventHandler, MouseEventHandler
from src.models.grid import Grid
from src.ui.animation_handler import AnimationHandler
from src.ui.screen_manager import ScreenManager


class GameState:
    """The game state for the Minesweeper game."""

    def __init__(
        self,
        logger: Logger,
        width: int = 10,
        height: int = 10,
        difficulty: str = "easy",
    ) -> None:
        """
        Initialises the game state.
        :param logger: The logger object.
        :param width: The width of the grid.
        :param height: The height of the grid.
        :param difficulty: The difficulty of the game.
        :returns: None
        """
        self.logger = logger
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.grid = Grid(logger, width, height)

        self._init_bomb_num()
        self._init_pygame()
        self.grid.generate(self.num_bombs)
        self.animation_handler = AnimationHandler(
            self.grid, self.screen, self.grid.assets
        )
        self.screen_manager = ScreenManager(
            self.grid, self.screen, self.animation_handler
        )
        self.game_logic = GameLogic(
            self.grid, self.animation_handler, self.screen_manager
        )
        self.mouse_event_handler = MouseEventHandler(
            self.grid, self.game_logic, self.screen_manager
        )
        self.key_event_handler = KeyEventHandler(self.grid, self.game_logic)

        self.start_time = time()

    def _init_bomb_num(self) -> None:
        """
        Initialises the number of bombs based on the difficulty level.
        :returns: None
        """
        if self.difficulty in Constants.DIFFICULTY_PERCENTAGES:
            self.num_bombs = int(
                (Constants.DIFFICULTY_PERCENTAGES[self.difficulty] / 100)
                * (self.grid.width * self.grid.height)
            )
        else:
            raise ValueError("Invalid difficulty level.")

    def _init_pygame(self) -> None:
        """
        Initialises the pygame window.
        :returns: None
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            (
                self.grid.width * Constants.BOX_WIDTH,
                self.grid.height * Constants.BOX_HEIGHT,
            ),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption(Constants.WINDOW_TITLE)

    def _reinitialise(self) -> None:
        """
        Reinitialises the game.
        :returns: None
        """
        self.__init__(self.logger, self.grid.width, self.grid.height, self.difficulty)

    def _handle_event(self, event) -> bool:
        """
        Handles a pygame event.
        :param event: The pygame event.
        :returns: True if the game is still running, False otherwise.
        """
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            return self.mouse_event_handler.click(
                y // Constants.BOX_HEIGHT, x // Constants.BOX_WIDTH, event.button
            )
        elif event.type == pygame.KEYDOWN:
            if self.key_event_handler.key_press(event):
                self.game_state = self._reinitialise()
            return True

        return True

    def play(self) -> None:
        """
        Plays the Minesweeper game.
        :returns: None
        """
        running = True

        while running:
            self.screen_manager.display()

            if (
                self.grid.revealed_count
                == self.grid.width * self.grid.height - self.num_bombs
            ):
                running = self.screen_manager.show_win(self.start_time)

            for event in pygame.event.get():
                try:
                    running = self._handle_event(event)
                except Exception as e:  # Temporary fix
                    self.logger.exception(e)
                    running = True

            pygame.display.flip()

        sleep(2)
        pygame.quit()
