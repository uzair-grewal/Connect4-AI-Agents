from __future__ import annotations

from typing import Optional

from agents.base_agent import Agent
from engine import ConnectFour


class MinimaxAgent(Agent):
    """Minimax-based agent scaffold for Connect Four."""

    def __init__(self, depth: int = 4, seed: Optional[int] = None) -> None:
        """Initialize the agent with a search depth and optional RNG seed."""
        self.depth = depth
        self.seed = seed

    def choose_move(self, game: ConnectFour) -> int:
        """TODO: Use minimax search to select the best legal move."""
        raise NotImplementedError

    def _minimax(self, game: ConnectFour, depth: int, maximizing_player: bool) -> float:
        """TODO: Implement the minimax search for the current position."""
        raise NotImplementedError

    def _evaluate(self, game: ConnectFour) -> float:
        """TODO: Implement a heuristic evaluation for non-terminal positions."""
        raise NotImplementedError
