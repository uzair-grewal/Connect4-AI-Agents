from __future__ import annotations

import random
from typing import Optional

from agents.base_agent import Agent
from engine import ConnectFour


class RandomAgent(Agent):
    """Randomly chooses a legal move for the current board state."""

    def __init__(self, seed: Optional[int] = None) -> None:
        """Initialize the agent with an optional RNG seed for reproducibility."""
        self.seed = seed
        self.rng = random.Random(seed)

    def choose_move(self, game: ConnectFour) -> int:
        """Select a uniformly random legal move and return its column index."""
        legal_moves = game.legal_moves()
        return self.rng.choice(legal_moves)
