from __future__ import annotations

from abc import ABC, abstractmethod

from engine import ConnectFour


class Agent(ABC):
    """Abstract base class for Connect Four agents."""

    @abstractmethod
    def choose_move(self, game: ConnectFour) -> int:
        """Return a legal column index for the current board state."""
        raise NotImplementedError
