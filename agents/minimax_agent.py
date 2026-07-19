from __future__ import annotations

import random
from typing import Optional

from agents.base_agent import Agent
from engine import ConnectFour


class MinimaxAgent(Agent):
    """Minimax-based agent for Connect Four with heuristic evaluation."""

    def __init__(self, depth: int = 4, seed: Optional[int] = None) -> None:
        """Initialize the agent with a search depth and optional RNG seed."""
        self.depth = depth
        self.seed = seed
        self.rng = random.Random(seed)

    def choose_move(self, game: ConnectFour) -> int:
        """Use minimax search to select the best legal move."""
        self.agent_player = game.current_player
        legal_moves = game.legal_moves()
        best_value = float('-inf')
        best_moves = []

        for col in legal_moves:
            game_copy = game.copy()
            game_copy.apply_move(col)
            value = self._minimax(game_copy, self.depth - 1)

            if value > best_value:
                best_value = value
                best_moves = [col]
            elif value == best_value:
                best_moves.append(col)

        return self.rng.choice(best_moves)

    def _minimax(self, game: ConnectFour, depth: int) -> float:
        """Implement minimax search."""
        if game.is_terminal():
            winner = game.winner()
            if winner == self.agent_player:
                return 10000
            elif winner is not None:
                return -10000
            else:
                return 0

        if depth == 0:
            return self._evaluate(game)

        legal_moves = game.legal_moves()

        if game.current_player == self.agent_player:
            max_value = float('-inf')
            for col in legal_moves:
                game_copy = game.copy()
                game_copy.apply_move(col)
                value = self._minimax(game_copy, depth - 1)
                max_value = max(max_value, value)
            return max_value
        else:
            min_value = float('inf')
            for col in legal_moves:
                game_copy = game.copy()
                game_copy.apply_move(col)
                value = self._minimax(game_copy, depth - 1)
                min_value = min(min_value, value)
            return min_value

    def _evaluate(self, game: ConnectFour) -> float:
        """Evaluate a non-terminal position using windowed scoring from agent's perspective."""
        opponent = 3 - self.agent_player
        score = 0

        score += self._score_windows(game, self.agent_player) * 100
        score -= self._score_windows(game, opponent) * 100
        score += self._score_center_control(game, self.agent_player) * 10
        score -= self._score_center_control(game, opponent) * 10

        return score

    def _score_windows(self, game: ConnectFour, player: int) -> float:
        """Score all 4-windows for a player."""
        score = 0
        opponent = 3 - player

        for row in range(game.ROWS):
            for col in range(game.COLS - 3):
                window = [game.board[row][col + i] for i in range(4)]
                player_count = window.count(player)
                opponent_count = window.count(opponent)

                if opponent_count == 0:
                    if player_count == 3:
                        score += 50
                    elif player_count == 2:
                        score += 10
                    elif player_count == 1:
                        score += 1

        for col in range(game.COLS):
            for row in range(game.ROWS - 3):
                window = [game.board[row + i][col] for i in range(4)]
                player_count = window.count(player)
                opponent_count = window.count(opponent)

                if opponent_count == 0:
                    if player_count == 3:
                        score += 50
                    elif player_count == 2:
                        score += 10
                    elif player_count == 1:
                        score += 1

        for row in range(game.ROWS - 3):
            for col in range(game.COLS - 3):
                window = [game.board[row + i][col + i] for i in range(4)]
                player_count = window.count(player)
                opponent_count = window.count(opponent)

                if opponent_count == 0:
                    if player_count == 3:
                        score += 50
                    elif player_count == 2:
                        score += 10
                    elif player_count == 1:
                        score += 1

        for row in range(game.ROWS - 3):
            for col in range(3, game.COLS):
                window = [game.board[row + i][col - i] for i in range(4)]
                player_count = window.count(player)
                opponent_count = window.count(opponent)

                if opponent_count == 0:
                    if player_count == 3:
                        score += 50
                    elif player_count == 2:
                        score += 10
                    elif player_count == 1:
                        score += 1

        return score

    def _score_center_control(self, game: ConnectFour, player: int) -> float:
        """Score the player's control of center columns."""
        center_col = 3
        score = 0

        for row in range(game.ROWS):
            if game.board[row][center_col] == player:
                score += 3
            for offset in [1, 2, 3]:
                if center_col - offset >= 0 and game.board[row][center_col - offset] == player:
                    score += (4 - offset)
                if center_col + offset < game.COLS and game.board[row][center_col + offset] == player:
                    score += (4 - offset)

        return score
