from __future__ import annotations

from agents.base_agent import Agent
from engine import ConnectFour


class RandomAgent(Agent):
    """Randomly chooses a legal move for the current board state."""

    def choose_move(self, game: ConnectFour) -> int:
        """TODO: Select a uniformly random legal move and return its column index."""
        raise NotImplementedError
