from __future__ import annotations

from typing import List, Optional, Tuple


class ConnectFour:
    """A simple Connect Four game engine for AI assignments.

    The board is represented as a 6x7 grid where row 0 is the bottom row.
    Cells contain 0 for empty, 1 for player 1, and 2 for player 2.
    """

    ROWS = 6
    COLS = 7

    def __init__(self) -> None:
        """Initialize an empty game board and set the first player to move."""
        self.board: List[List[int]] = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player: int = 1
        self.last_move: Optional[Tuple[int, int]] = None

    def legal_moves(self) -> List[int]:
        """Return the indices of columns that still have space for a disc."""
        return [col for col in range(self.COLS) if self.board[self.ROWS - 1][col] == 0]

    def apply_move(self, col: int) -> None:
        """Drop the current player's disc into the lowest empty row of a column.

        Args:
            col: The zero-based column index to play in.

        Raises:
            ValueError: If the requested column is already full.
        """
        if not 0 <= col < self.COLS:
            raise ValueError("Column index out of range")
        if self.board[self.ROWS - 1][col] != 0:
            raise ValueError("Column is full")

        for row in range(self.ROWS):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.last_move = (row, col)
                break

        self.current_player = 3 - self.current_player

    def undo_move(self) -> None:
        """Undo the most recently applied move and restore the game state."""
        if self.last_move is None:
            raise ValueError("No move to undo")

        row, col = self.last_move
        if self.board[row][col] == 0:
            raise ValueError("Last move was already undone")

        self.board[row][col] = 0
        self.current_player = 3 - self.current_player
        self.last_move = None

    def winner(self) -> Optional[int]:
        """Return 1 or 2 if a player has four discs in a row, else None."""
        for row in range(self.ROWS):
            for col in range(self.COLS):
                player = self.board[row][col]
                if player == 0:
                    continue

                if self._count_consecutive(row, col, player, 0, 1) >= 4:
                    return player
                if self._count_consecutive(row, col, player, 1, 0) >= 4:
                    return player
                if self._count_consecutive(row, col, player, 1, 1) >= 4:
                    return player
                if self._count_consecutive(row, col, player, 1, -1) >= 4:
                    return player

        return None

    def is_terminal(self) -> bool:
        """Return True when the game is over because of a win or a draw."""
        return self.winner() is not None or self.is_draw()

    def is_draw(self) -> bool:
        """Return True when the board is full and no player has won."""
        if self.winner() is not None:
            return False
        return all(self.board[row][col] != 0 for row in range(self.ROWS) for col in range(self.COLS))

    def copy(self) -> "ConnectFour":
        """Return a deep copy of the current game state."""
        new_game = ConnectFour()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        if self.last_move is not None:
            new_game.last_move = (self.last_move[0], self.last_move[1])
        return new_game

    def render(self) -> str:
        """Return a simple text-based rendering of the board."""
        rows: List[str] = []
        for row in range(self.ROWS - 1, -1, -1):
            rendered_row = []
            for col in range(self.COLS):
                cell = self.board[row][col]
                if cell == 0:
                    rendered_row.append('.')
                elif cell == 1:
                    rendered_row.append('X')
                else:
                    rendered_row.append('O')
            rows.append(''.join(rendered_row))
        rows.append(''.join(str(col) for col in range(self.COLS)))
        return '\n'.join(rows)

    def __str__(self) -> str:
        """Return the board rendering for display in a text UI."""
        return self.render()

    def _count_consecutive(self, row: int, col: int, player: int, delta_row: int, delta_col: int) -> int:
        """Count how many same-player discs appear in a line from a start cell."""
        count = 1
        for direction in (1, -1):
            next_row = row + direction * delta_row
            next_col = col + direction * delta_col
            while 0 <= next_row < self.ROWS and 0 <= next_col < self.COLS and self.board[next_row][next_col] == player:
                count += 1
                next_row += direction * delta_row
                next_col += direction * delta_col
        return count


if __name__ == "__main__":
    game = ConnectFour()
    for move in [0, 6, 1, 5, 2, 4, 3]:
        game.apply_move(move)

    print(game)
    print("winner:", game.winner())
    print("terminal:", game.is_terminal())
