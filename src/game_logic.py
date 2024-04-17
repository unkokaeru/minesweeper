"""Contains the Minesweeper game logic."""

import math
import random
from heapq import heappop, heappush
from logging import Logger
from time import sleep, time
from typing import List

import pygame

from cfg.constants import Constants


class Minesweeper:
    """The Minesweeper game class."""

    def __init__(
        self, logger: Logger, width: int, height: int, difficulty: str
    ) -> None:
        """
        Initialises the Minesweeper game.
        :param logger: The logger object.
        :param width: The width of the grid.
        :param height: The height of the grid.
        :param difficulty: The difficulty of the game.
        :returns: None
        """
        # Initialise the logger
        self.logger = logger

        # Initialise the grid
        self.width = width
        self.height = height
        self.grid = [
            [(0, False, False) for _ in range(self.width)] for _ in range(self.height)
        ]  # -1 represents a bomb, 0 represents no bombs, 1-8 represent the number of adjacent bombs

        # Initialise the number of bombs
        self.difficulty = difficulty
        if difficulty in Constants.DIFFICULTY_PERCENTAGES:
            self.num_bombs = int(
                (Constants.DIFFICULTY_PERCENTAGES[difficulty] / 100)
                * (self.width * self.height)
            )
        else:
            raise ValueError("Invalid difficulty level.")

        # Initialise the number of revealed cells
        self.revealed_count = 0

        # Initialise a timer
        self.start_time = time()

        # Initialise pygame
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.width * Constants.BOX_WIDTH, self.height * Constants.BOX_HEIGHT),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption(Constants.WINDOW_TITLE)
        self.font = pygame.font.Font(None, Constants.FONT_SIZE)

        # Initalise assets
        self.assets = {}
        self._initialise_assets()

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

    def _get_cell_image(
        self, value: int, revealed: bool, flagged: bool
    ) -> pygame.Surface:
        """
        Retrieves the image of a cell in the Minesweeper grid.
        :param value: The value of the cell.
        :param revealed: The revealed status of the cell.
        :param flagged: The flagged status of the cell.
        :returns: The image of the cell.
        """
        if revealed:
            if value == -1:
                return self.assets["image_bomb"]
            elif value == 1:
                return self.assets["image_1"]
            elif value == 2:
                return self.assets["image_2"]
            elif value == 3:
                return self.assets["image_3"]
            elif value == 4:
                return self.assets["image_4"]
            elif value == 5:
                return self.assets["image_5"]
            elif value == 6:
                return self.assets["image_6"]
            elif value == 7:
                return self.assets["image_7"]
            elif value == 8:
                return self.assets["image_8"]
            elif value == 0:
                return self.assets["image_cell"]
        elif not revealed:
            if flagged:
                return self.assets["image_flag"]
            else:
                return self.assets["image_fog_sharp"]

    def _animate_reveal(self, row: int, col: int) -> None:
        """
        Animates the reveal of a cell in the Minesweeper grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: None
        """
        value, revealed, flagged = self.grid[row][col]
        final_image = self._get_cell_image(value, revealed, flagged)
        fading_surface = pygame.Surface((Constants.BOX_WIDTH, Constants.BOX_HEIGHT))
        fading_surface.blit(final_image, (0, 0))

        for alpha in range(0, 255, 15):
            fading_surface.set_alpha(alpha)
            self.screen.blit(
                fading_surface, (col * Constants.BOX_WIDTH, row * Constants.BOX_HEIGHT)
            )
            pygame.display.flip()
            sleep(0.001)

    def _animate_flag(self, row: int, col: int) -> None:
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
                    if self.grid[row + i][col + j][0] == -1:
                        count += 1

        return count

    def _generate_grid(self) -> List[List[str]]:
        """
        Generates a Minesweeper grid.
        :returns: A 2D list representing the grid.
        """
        # Generate bombs
        bomb_positions = random.sample(range(self.width * self.height), self.num_bombs)
        for position in bomb_positions:
            row, col = divmod(position, self.width)
            self.grid[row][col] = (-1, False, False)

        # Generate numbers
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col][0] == -1:
                    continue
                self.grid[row][col] = (
                    self._count_adjacent_bombs(row, col),
                    False,
                    False,
                )

        return self.grid

    def _display_grid(self) -> None:
        """
        Displays the Minesweeper grid using pygame.
        :returns: None
        """
        self.screen.fill(Constants.EMPTY_COLOUR)

        for row in range(self.height):
            for col in range(self.width):
                value, revealed, flagged = self.grid[row][col]
                box_rect = (col * Constants.BOX_WIDTH, row * Constants.BOX_HEIGHT)

                image = self._get_cell_image(value, revealed, flagged)

                self.screen.blit(image, box_rect)

    def _display_basic_grid(self) -> None:
        """
        Displays the Minesweeper grid using pygame. (DEPRECATED)
        :returns: None
        """
        self.screen.fill(Constants.EMPTY_COLOUR)

        for row in range(self.height):
            for col in range(self.width):
                value, revealed, flagged = self.grid[row][col]
                box_rect = (
                    col * Constants.BOX_WIDTH,
                    row * Constants.BOX_HEIGHT,
                    Constants.BOX_WIDTH,
                    Constants.BOX_HEIGHT,
                )

                if revealed:
                    if value == -1:
                        colour = Constants.GAME_OVER_COLOUR
                    elif value > 0:
                        colour = Constants.TEXT_BACKGROUND_COLOUR
                    elif value == 0:
                        colour = Constants.EMPTY_COLOUR
                elif not revealed:
                    colour = Constants.FOG_COLOUR

                if flagged:
                    colour = Constants.TEXT_BACKGROUND_COLOUR

                pygame.draw.rect(self.screen, colour, box_rect, 0)

                if revealed:
                    if value == -1:
                        pygame.draw.circle(
                            self.screen,
                            Constants.TEXT_COLOUR,
                            (
                                col * Constants.BOX_WIDTH + Constants.BOX_WIDTH // 2,
                                row * Constants.BOX_HEIGHT + Constants.BOX_HEIGHT // 2,
                            ),
                            Constants.BOX_WIDTH // 4,
                        )
                    elif value > 0:
                        text = self.font.render(str(value), True, Constants.TEXT_COLOUR)
                        self.screen.blit(
                            text,
                            (
                                col * Constants.BOX_WIDTH
                                + Constants.BOX_WIDTH // 2
                                - text.get_width() // 2,
                                row * Constants.BOX_HEIGHT
                                + Constants.BOX_HEIGHT // 2
                                - text.get_height() // 2,
                            ),
                        )

                if flagged:
                    text = self.font.render("F", True, Constants.TEXT_COLOUR)
                    self.screen.blit(
                        text,
                        (
                            col * Constants.BOX_WIDTH
                            + Constants.BOX_WIDTH // 2
                            - text.get_width() // 2,
                            row * Constants.BOX_HEIGHT
                            + Constants.BOX_HEIGHT // 2
                            - text.get_height() // 2,
                        ),
                    )

    def _reveal_cell(self, start_row: int, start_col: int) -> None:
        """
        Reveals a cell in the Minesweeper grid, recursively revealing adjacent cells if the cell is empty.
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
            if row < 0 or row >= self.height or col < 0 or col >= self.width:
                continue

            # Retrieve the cell value and revealed status
            value, revealed_status, flagged = self.grid[row][col]

            # Stop if the cell is already revealed or flagged
            if revealed_status or flagged:
                continue

            # Mark the cell as revealed
            self.grid[row][col] = (value, True, False)
            self._animate_reveal(row, col)
            self.revealed_count += 1

            # If the cell is a bomb or has adjacent bombs, stop further revealing
            if value != 0:
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

    def _show_game_over_animation(self) -> None:
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

    def _show_game_over(self) -> None:
        """
        Displays the game over screen.
        :returns: None
        """
        self._show_game_over_animation()

        self.screen.fill(Constants.GAME_OVER_COLOUR)
        text = self.font.render("Game Over!", True, Constants.TEXT_COLOUR)
        self.screen.blit(
            text,
            (
                self.width * Constants.BOX_HEIGHT // 2 - text.get_width() // 2,
                self.height * Constants.BOX_WIDTH // 2 - text.get_height() // 2,
            ),
        )

    def _flag_cell(self, row: int, col: int) -> None:
        """
        Flags a cell in the Minesweeper grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :returns: None
        """
        value, revealed, flagged = self.grid[row][col]

        if not revealed:
            self.grid[row][col] = (value, revealed, not flagged)
            self._animate_flag(row, col)

    def _handle_click(self, row: int, col: int, button: int) -> bool:
        """
        Handles a click on the Minesweeper grid.
        :param row: The row of the cell.
        :param col: The column of the cell.
        :param button: The mouse button clicked.
        :returns: True if the game is still running, False otherwise.
        """
        if button == 1:
            if self.grid[row][col][0] == -1 and not self.grid[row][col][2]:
                self._reveal_cell(row, col)
                self._display_grid()
                pygame.display.flip()
                sleep(1)
                self._show_game_over()
                return False
            elif self.grid[row][col][0] == -1 and self.grid[row][col][2]:
                return True
            else:
                self._reveal_cell(row, col)
                return True
        elif button == 3:
            self._flag_cell(row, col)
            return True
        elif button == 2:
            return True

    def _reinitalise_game(self) -> None:
        """
        Reinitialises the game.
        :returns: None
        """
        self.__init__(self.width, self.height, self.difficulty)
        self._generate_grid()

    def _handle_key_press(self, event) -> bool:
        """
        Handles a key press event.
        :param event: The key press event.
        :returns: True if the game is still running, False otherwise.
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
            self._reinitalise_game()
            return True
        elif event.key == pygame.K_r:
            self._reinitalise_game()
            return True
        elif event.key == pygame.K_EQUALS:
            self.width += 1
            self.height += 1
            self._reinitalise_game()
            return True
        elif event.key == pygame.K_MINUS:
            self.width -= 1
            self.height -= 1
            self._reinitalise_game()
            return True
        elif event.key == pygame.K_TAB:
            for row in range(self.height):
                for col in range(self.width):
                    self.grid[row][col] = (self.grid[row][col][0], True, False)
            return True

        return True

    def _handle_event(self, event) -> None:
        """
        Handles a pygame event.
        :param event: The pygame event.
        :returns: None
        """
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            return self._handle_click(
                y // Constants.BOX_HEIGHT, x // Constants.BOX_WIDTH, event.button
            )
        elif event.type == pygame.KEYDOWN:
            return self._handle_key_press(event)

        return True

    def _show_win_animation(self) -> None:
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
                    random.randint(0, self.width * Constants.BOX_WIDTH),
                    random.randint(0, self.height * Constants.BOX_HEIGHT),
                ),
                random.randint(10, 50),
            )
            pygame.display.flip()
            sleep(0.01)

    def _show_win_screen(self) -> bool:
        """
        Displays the win screen.
        :returns: True if the game is still running, False otherwise.
        """
        time_to_complete_raw = time() - self.start_time

        minutes = int(time_to_complete_raw // 60)
        seconds = int(time_to_complete_raw % 60)
        time_to_complete = (
            f"{minutes} minutes and {seconds} seconds"
            if minutes > 0
            else f"{seconds} seconds"
        )

        self._show_win_animation()

        self.screen.fill(Constants.WIN_COLOUR)
        text = self.font.render("You win!", True, Constants.TEXT_COLOUR)
        self.screen.blit(
            text,
            (
                self.width * Constants.BOX_HEIGHT // 2 - text.get_width() // 2,
                self.height * Constants.BOX_WIDTH // 2 - text.get_height() // 2,
            ),
        )
        text = self.font.render(
            f"Time to complete: {time_to_complete}", True, Constants.TEXT_COLOUR
        )
        self.screen.blit(
            text,
            (
                self.width * Constants.BOX_HEIGHT // 2 - text.get_width() // 2,
                self.height * Constants.BOX_WIDTH // 2 + text.get_height(),
            ),
        )

    def play_game(self) -> None:
        """
        Plays the Minesweeper game.
        :returns: None
        """
        self._generate_grid()

        running = True
        while running:
            self._display_grid()

            if self.revealed_count == self.width * self.height - self.num_bombs:
                running = self._show_win_screen()

            for event in pygame.event.get():
                try:
                    running = self._handle_event(event)
                except Exception as e:  # Temporary fix
                    self.logger.exception(e)
                    running = True

            pygame.display.flip()

        sleep(2)
        pygame.quit()
