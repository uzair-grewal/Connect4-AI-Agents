from __future__ import annotations

import random
from typing import Optional

from agents.base_agent import Agent
from engine import ConnectFour


class RuleBasedAgent(Agent):
    """Rule-based agent driven by prioritized rules."""

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize the agent with an optional RNG seed for reproducibility."""
        self.seed = seed
        self.rng = random.Random(seed)

    def choose_move(self, game: ConnectFour) -> int:
        """Apply rules in priority order, with tie-breaking using random selection."""
        legal_moves = game.legal_moves()

        winning_moves = self._find_winning_moves(game, legal_moves)
        if winning_moves:
            return self.rng.choice(winning_moves)

        blocking_moves = self._find_blocking_moves(game, legal_moves)
        if blocking_moves:
            return self.rng.choice(blocking_moves)

        central_moves = self._prefer_central_moves(game, legal_moves)
        if central_moves:
            return self.rng.choice(central_moves)

        extension_moves = self._extend_longest_line_moves(game, legal_moves)
        if extension_moves:
            return self.rng.choice(extension_moves)

        return self.rng.choice(legal_moves)

    def _find_winning_moves(self, game: ConnectFour, legal_moves: list[int]) -> list[int]:
        """Find legal moves that immediately win for the current player."""
        winning = []
        for col in legal_moves:
            game_copy = game.copy()
            game_copy.apply_move(col)
            if game_copy.winner() == game.current_player:
                winning.append(col)
        return winning

    def _find_blocking_moves(self, game: ConnectFour, legal_moves: list[int]) -> list[int]:
        """Find legal moves that block the opponent's immediate winning move."""
        opponent = 3 - game.current_player
        blocking = []

        for col in legal_moves:
            game_copy = game.copy()
            game_copy.apply_move(col)
            opponent_opp_moves = game_copy.legal_moves()

            for opp_col in opponent_opp_moves:
                game_copy2 = game_copy.copy()
                game_copy2.apply_move(opp_col)
                if game_copy2.winner() == opponent:
                    blocking.append(col)
                    break

        return blocking

    def _prefer_central_moves(self, game: ConnectFour, legal_moves: list[int]) -> list[int]:
        """Return the most central legal moves."""
        center = 3
        if not legal_moves:
            return []

        min_distance = min(abs(col - center) for col in legal_moves)
        return [col for col in legal_moves if abs(col - center) == min_distance]

    def _extend_longest_line_moves(self, game: ConnectFour, legal_moves: list[int]) -> list[int]:
        """Find moves that extend the player's longest line or create threats."""
        player = game.current_player
        best_score = -1
        best_moves = []

        for col in legal_moves:
            game_copy = game.copy()
            game_copy.apply_move(col)
            score = self._score_board_state(game_copy, player)

            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)

        return best_moves if best_moves else legal_moves

    def _score_board_state(self, game: ConnectFour, player: int) -> int:
        """Score a board state based on the player's line extensions."""
        score = 0
        opponent = 3 - player

        for row in range(game.ROWS):
            for col in range(game.COLS):
                if game.board[row][col] == player:
                    score += self._count_consecutive(game, row, col, player, 0, 1)
                    score += self._count_consecutive(game, row, col, player, 1, 0)
                    score += self._count_consecutive(game, row, col, player, 1, 1)
                    score += self._count_consecutive(game, row, col, player, 1, -1)
                elif game.board[row][col] == opponent:
                    score -= self._count_consecutive(game, row, col, opponent, 0, 1) // 2
                    score -= self._count_consecutive(game, row, col, opponent, 1, 0) // 2
                    score -= self._count_consecutive(game, row, col, opponent, 1, 1) // 2
                    score -= self._count_consecutive(game, row, col, opponent, 1, -1) // 2

        return score

    def _count_consecutive(self, game: ConnectFour, row: int, col: int, player: int, delta_row: int, delta_col: int) -> int:
        """Count consecutive discs in a direction from a starting position."""
        count = 1
        for direction in (1, -1):
            next_row = row + direction * delta_row
            next_col = col + direction * delta_col
            while 0 <= next_row < game.ROWS and 0 <= next_col < game.COLS and game.board[next_row][next_col] == player:
                count += 1
                next_row += direction * delta_row
                next_col += direction * delta_col
        return count

