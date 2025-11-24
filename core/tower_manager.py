"""Tower management implementation."""
from typing import List, Dict, Tuple
from interfaces.money_detector import IMoneyDetector


class TowerManager:
    """Manages tower state and operations."""

    def __init__(self, money_detector: IMoneyDetector, costs: Dict[str, int]):
        """Initialize the tower manager.
        
        Args:
            money_detector: Money detection interface
            costs: Dictionary of tower costs
        """
        self.money_detector = money_detector
        self.costs = costs
        self.towers = []  # Format: [type, location, upgrades]

    def add_tower(self, tower_type: str, location: int) -> None:
        """Add a tower to the list.
        
        Args:
            tower_type: Type of tower
            location: Location index
        """
        self.towers.append([tower_type, location, "000"])

    def get_tower(self, index: int) -> List:
        """Get tower at the specified index.
        
        Args:
            index: Tower index
            
        Returns:
            Tower data [type, location, upgrades]
        """
        if 0 <= index < len(self.towers):
            return self.towers[index]
        return None

    def get_towers(self) -> List[List]:
        """Get all towers.
        
        Returns:
            List of all towers
        """
        return self.towers

    def upgrade_tower_state(self, index: int, path: int) -> None:
        """Update tower state after upgrade.
        
        Args:
            index: Tower index
            path: Upgrade path (1, 2, or 3)
        """
        if 0 <= index < len(self.towers):
            tower = self.towers[index]
            upgrades = tower[2]
            path_index = path - 1
            new_value = str(int(upgrades[path_index]) + 1)
            tower[2] = upgrades[:path_index] + new_value + upgrades[path_index + 1:]

    def check_has_tier5(self, tower_type: str, path: int) -> bool:
        """Check if a tier 5 tower exists for the given type and path.
        
        Args:
            tower_type: Type of tower
            path: Upgrade path (1, 2, or 3)
            
        Returns:
            True if tier 5 exists, False otherwise
        """
        path_index = path - 1
        for tower in self.towers:
            if tower[0] == tower_type and tower[2][path_index] == "5":
                return True
        return False

    def can_afford(self, cost: int) -> bool:
        """Check if player can afford a purchase.
        
        Args:
            cost: Cost of the item
            
        Returns:
            True if affordable, False otherwise
        """
        try:
            return int(self.get_precise_money()) >= cost
        except (ValueError, TypeError):
            return False

    def get_precise_money(self) -> str:
        """Get precise money reading.
        
        Returns:
            Money amount as string
        """
        a = self.money_detector.get_money()
        b = self.money_detector.get_money()
        if a == b:
            return a
        else:
            return self.get_precise_money()

    def get_upgrade_cost(self, tower_index: int, path: int) -> int:
        """Get the cost of upgrading a tower.
        
        Args:
            tower_index: Index of the tower
            path: Upgrade path (1, 2, or 3)
            
        Returns:
            Cost of the upgrade, or -1 if invalid
        """
        tower = self.get_tower(tower_index)
        if not tower:
            return -1

        upgrades = tower[2]
        path_index = path - 1
        new_level = int(upgrades[path_index]) + 1

        # Build new upgrade string
        if path == 1:
            new_str = str(new_level) + upgrades[1:]
        elif path == 2:
            new_str = upgrades[0] + str(new_level) + upgrades[2]
        else:  # path == 3
            new_str = upgrades[:2] + str(new_level)

        upgrade_key = tower[0] + new_str
        return self.costs.get(upgrade_key, -1)

    def get_tower_cost(self, tower_type: str) -> int:
        """Get the cost of placing a tower.
        
        Args:
            tower_type: Type of tower
            
        Returns:
            Cost of the tower, or -1 if invalid
        """
        return self.costs.get(tower_type + "000", -1)
