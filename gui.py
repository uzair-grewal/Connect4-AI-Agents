import tkinter as tk

from engine import ConnectFour


class ConnectFourGUI:
    """A simple Tkinter-based GUI for visualizing the Connect Four engine."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Connect Four")
        self.root.resizable(False, False)

        self.game = ConnectFour()
        self.cells: list[list[tk.Label]] = []

        self.status_var = tk.StringVar(value="Player 1 turn")
        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 12), pady=8)
        self.status_label.grid(row=0, column=0, columnspan=8)

        for col in range(7):
            button = tk.Button(
                root,
                text=str(col + 1),
                width=4,
                height=2,
                command=lambda col=col: self.play(col),
            )
            button.grid(row=1, column=col)

        reset_button = tk.Button(root, text="Restart Game", width=12, command=self.reset_game)
        reset_button.grid(row=1, column=7)

        for row in range(6):
            row_labels: list[tk.Label] = []
            for col in range(7):
                label = tk.Label(root, text="○", font=("Arial", 24), width=3, height=2, bg="white")
                label.grid(row=row + 2, column=col)
                row_labels.append(label)
            self.cells.append(row_labels)

        self.refresh_board()

    def play(self, col: int) -> None:
        """Apply a move for the current player and refresh the visible board."""
        if self.game.is_terminal():
            return

        if col not in self.game.legal_moves():
            self.status_var.set("Illegal move")
            return

        self.game.apply_move(col)
        self.refresh_board()

        winner = self.game.winner()
        if winner is not None:
            self.status_var.set(f"Player {winner} wins!")
        elif self.game.is_draw():
            self.status_var.set("Draw!")
        else:
            self.status_var.set(f"Player {self.game.current_player} turn")

    def reset_game(self) -> None:
        """Start a fresh game and redraw the board."""
        self.game = ConnectFour()
        self.status_var.set("Player 1 turn")
        self.refresh_board()

    def refresh_board(self) -> None:
        """Render the current board state into the Tkinter labels."""
        for board_row in range(6):
            visual_row = 5 - board_row
            for col in range(7):
                cell_value = self.game.board[board_row][col]
                if cell_value == 0:
                    self.cells[visual_row][col].config(text="○", fg="black")
                elif cell_value == 1:
                    self.cells[visual_row][col].config(text="●", fg="red")
                else:
                    self.cells[visual_row][col].config(text="●", fg="yellow")


if __name__ == "__main__":
    root = tk.Tk()
    ConnectFourGUI(root)
    root.mainloop()
