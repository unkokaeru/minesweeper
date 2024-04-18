"""cell.py: Contains the cell model for Minesweeper."""


class Cell:
    """A cell in the Minesweeper grid."""

    def __init__(
        self, value: int = 0, revealed: bool = False, flagged: bool = False
    ) -> None:
        """
        Initialises the cell.
        :param value: The value of the cell, -1 represents a bomb, 0 represents no bombs, 1-8 represent the number of adjacent bombs.
        :param revealed: The revealed status of the cell.
        :param flagged: The flagged status of the cell.
        :returns: None
        """
        self.value = value
        self.revealed = revealed
        self.flagged = flagged

    def __str__(self) -> str:
        """
        Returns the string representation of the cell.
        :returns: The string representation of the cell.
        """
        return f"Cell(value={self.value}, revealed={self.revealed}, flagged={self.flagged})"

    def __repr__(self) -> str:
        """
        Returns the string representation of the cell.
        :returns: The string representation of the cell.
        """
        return self.__str__()

    def reveal(self) -> None:
        """
        Reveals the cell.
        :returns: None
        """
        self.revealed = True

    def flag(self) -> None:
        """
        Flags the cell.
        :returns: None
        """
        if not self.revealed:
            self.flagged = not self.flagged
