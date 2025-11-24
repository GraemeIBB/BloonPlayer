"""Cost calculation utilities."""
from typing import Dict, List, Tuple


class CostCalculator:
    """Calculates and validates costs for towers and upgrades."""

    def __init__(self, costs: Dict[str, int]):
        """Initialize the cost calculator.
        
        Args:
            costs: Dictionary of tower costs
        """
        self.costs = costs

    def get_base_towers(self) -> List[str]:
        """Get list of base tower types (ending in 000).
        
        Returns:
            List of base tower keys
        """
        return [key for key in self.costs.keys() if key.endswith("000")]

    def validate_upgrade_path(self, current_upgrades: str, path: int) -> Tuple[bool, str]:
        """Validate if an upgrade path is available.
        
        Args:
            current_upgrades: Current upgrade string (e.g., "320")
            path: Upgrade path to check (1, 2, or 3)
            
        Returns:
            Tuple of (is_valid, reason)
        """
        path1, path2, path3 = int(current_upgrades[0]), int(current_upgrades[1]), int(current_upgrades[2])
        paths = [path1, path2, path3]
        path_index = path - 1

        # Check if already at max level
        if paths[path_index] >= 5:
            return False, "Already at max level"

        # Count how many paths are selected (> 0)
        selected_paths = [i for i, p in enumerate(paths) if p > 0]

        # If two paths are selected
        if len(selected_paths) == 2:
            # Can't upgrade the unselected path
            if path_index not in selected_paths:
                return False, "Cannot upgrade third path when two are selected"

            # If one path is >= 3 and the other is 2, can't upgrade the 2
            for i in selected_paths:
                other = [p for p in selected_paths if p != i][0]
                if paths[i] >= 3 and paths[other] == 2 and path_index == other:
                    return False, "Cannot upgrade past 2 when another path is >= 3"

        return True, ""

    def get_affordable_towers(self, current_money: int) -> List[str]:
        """Get list of towers that can be afforded.
        
        Args:
            current_money: Current available money
            
        Returns:
            List of affordable tower types (without "000")
        """
        affordable = []
        for key, cost in self.costs.items():
            if key.endswith("000") and cost <= current_money:
                affordable.append(key[:-3])
        return affordable

    def get_affordable_upgrades(self, tower_type: str, current_upgrades: str, current_money: int) -> List[int]:
        """Get list of affordable upgrade paths for a tower.
        
        Args:
            tower_type: Type of the tower
            current_upgrades: Current upgrade string
            current_money: Current available money
            
        Returns:
            List of affordable path numbers
        """
        affordable = []
        for path in [1, 2, 3]:
            is_valid, _ = self.validate_upgrade_path(current_upgrades, path)
            if not is_valid:
                continue

            # Build upgrade key
            path_index = path - 1
            new_level = str(int(current_upgrades[path_index]) + 1)
            if path == 1:
                new_str = new_level + current_upgrades[1:]
            elif path == 2:
                new_str = current_upgrades[0] + new_level + current_upgrades[2]
            else:  # path == 3
                new_str = current_upgrades[:2] + new_level

            upgrade_key = tower_type + new_str
            cost = self.costs.get(upgrade_key, float('inf'))
            if cost <= current_money:
                affordable.append(path)

        return affordable
