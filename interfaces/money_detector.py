"""Interface for money detection."""
from abc import ABC, abstractmethod


class IMoneyDetector(ABC):
    """Interface for detecting available money in the game."""

    @abstractmethod
    def get_money(self) -> str:
        """Get the current money amount as a string.
        
        Returns:
            String representation of the current money
        """
        pass
