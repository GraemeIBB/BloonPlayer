"""Interface for game input handling."""
from abc import ABC, abstractmethod
from typing import Tuple


class IGameInput(ABC):
    """Interface for handling game input operations."""

    @abstractmethod
    def press_key(self, key: str) -> None:
        """Press a keyboard key.
        
        Args:
            key: The key to press
        """
        pass

    @abstractmethod
    def click(self, position: Tuple[int, int] = None) -> None:
        """Click the mouse at the current or specified position.
        
        Args:
            position: Optional (x, y) position to click at
        """
        pass

    @abstractmethod
    def move_to(self, position: Tuple[int, int], duration: float = 0.5) -> None:
        """Move the mouse to a position.
        
        Args:
            position: (x, y) position to move to
            duration: Time in seconds to take for the movement
        """
        pass
