"""Interface for game strategies."""
from abc import ABC, abstractmethod
from typing import Optional, Tuple


class IStrategy(ABC):
    """Interface for game playing strategies."""

    @abstractmethod
    def decide_next_action(self) -> Tuple[str, Optional[dict]]:
        """Decide the next action to take.
        
        Returns:
            Tuple of (action_type, action_params) where action_type is one of:
            'place', 'upgrade', 'wait'
        """
        pass

    @abstractmethod
    def on_tower_placed(self, tower_type: str, location: int) -> None:
        """Callback when a tower is placed.
        
        Args:
            tower_type: Type of tower placed
            location: Location index where tower was placed
        """
        pass

    @abstractmethod
    def on_tower_upgraded(self, tower_index: int, path: int) -> None:
        """Callback when a tower is upgraded.
        
        Args:
            tower_index: Index of the tower that was upgraded
            path: Upgrade path (1, 2, or 3)
        """
        pass
