from __future__ import annotations

from agents.base_agent import Agent
from engine import ConnectFour


class RuleBasedAgent(Agent):
    """Rule-based agent scaffold for Connect Four."""

    def choose_move(self, game: ConnectFour) -> int:
        """TODO: Choose a move by applying the assignment's rule order."""
        raise NotImplementedError

    def _find_winning_move(self, game: ConnectFour) -> int:
        """TODO: Find a legal move that immediately wins for the current player."""
        raise NotImplementedError

    def _find_blocking_move(self, game: ConnectFour) -> int:
        """TODO: Find a legal move that blocks the opponent's immediate win."""
        raise NotImplementedError

    def _prefer_central(self, game: ConnectFour) -> int:
        """TODO: Prefer central columns when no stronger rule applies."""
        raise NotImplementedError

    def _extend_longest_line(self, game: ConnectFour) -> int:
        """TODO: Extend the current player's longest line in a legal move."""
        raise NotImplementedError
