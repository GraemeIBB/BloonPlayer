"""Interface for tower placement operations."""
from abc import ABC, abstractmethod
from typing import List, Optional


class ITowerPlacer(ABC):
    """Interface for tower placement and management."""

    @abstractmethod
    def place_tower(self, tower_type: str, location: int) -> bool:
        """Place a tower at the specified location.
        
        Args:
            tower_type: Type of tower to place (e.g., 'wizard_monkey')
            location: Location index on the map
            
        Returns:
            True if tower was placed successfully, False otherwise
        """
        pass

    @abstractmethod
    def upgrade_tower(self, tower_index: int, path: int) -> bool:
        """Upgrade a tower on a specific path.
        
        Args:
            tower_index: Index of the tower in the tower list
            path: Upgrade path (1, 2, or 3)
            
        Returns:
            True if upgrade was successful, False otherwise
        """
        pass

    @abstractmethod
    def get_towers(self) -> List[List]:
        """Get the list of placed towers.
        
        Returns:
            List of towers in format [type, location, upgrades]
        """
        pass

    @abstractmethod
    def can_afford(self, cost: int) -> bool:
        """Check if player can afford a purchase.
        
        Args:
            cost: Cost of the item
            
        Returns:
            True if affordable, False otherwise
        """
        pass
