"""Random wizard strategy implementation."""
import random
from typing import Optional, Tuple, List
from interfaces.strategy import IStrategy
from interfaces.tower_placer import ITowerPlacer
from core.tower_manager import TowerManager
from core.cost_calculator import CostCalculator


class RandomWizardStrategy(IStrategy):
    """Strategy that focuses on wizard monkeys with random upgrades."""

    def __init__(
        self,
        tower_placer: ITowerPlacer,
        tower_manager: TowerManager,
        cost_calculator: CostCalculator,
        initial_sniper_location: int = 27
    ):
        """Initialize the strategy.
        
        Args:
            tower_placer: Tower placement interface
            tower_manager: Tower manager instance
            cost_calculator: Cost calculator instance
            initial_sniper_location: Location for initial sniper placement
        """
        self.tower_placer = tower_placer
        self.tower_manager = tower_manager
        self.cost_calculator = cost_calculator
        self.initial_sniper_location = initial_sniper_location
        self.move_count = 0
        self.max_towers = 14

    def decide_next_action(self) -> Tuple[str, Optional[dict]]:
        """Decide the next action to take.
        
        Returns:
            Tuple of (action_type, action_params)
        """
        # Initial moves - place sniper and wizard
        if self.move_count == 0:
            return ('place', {'tower_type': 'sniper_monkey', 'location': self.initial_sniper_location})
        elif self.move_count == 1:
            return ('place', {'tower_type': 'wizard_monkey', 'next_available': True})

        # Get current tower count
        tower_count = len(self.tower_manager.get_towers())

        # After 14 towers, only upgrade
        if tower_count > self.max_towers:
            return self._decide_upgrade()

        # Determine threshold based on move count
        thresh = 5 if self.move_count < 30 else 3
        choice = random.randint(0, 10)

        if choice > thresh:
            # Upgrade existing tower
            return self._decide_upgrade()
        else:
            # Place new wizard
            return ('place', {'tower_type': 'wizard_monkey', 'next_available': True})

    def _decide_upgrade(self) -> Tuple[str, Optional[dict]]:
        """Decide which tower to upgrade.
        
        Returns:
            Tuple of (action_type, action_params)
        """
        viable_upgrades = self._get_viable_upgrades()
        
        if not viable_upgrades:
            return ('wait', None)

        # Randomly choose an upgrade
        chosen = random.choice(viable_upgrades)
        return ('upgrade', {'tower_index': chosen[0], 'path': chosen[1]})

    def _get_viable_upgrades(self) -> List[Tuple[int, int]]:
        """Get list of viable upgrades.
        
        Returns:
            List of (tower_index, path) tuples
        """
        viable = []
        current_money = int(self.tower_manager.get_precise_money())
        
        for i, tower in enumerate(self.tower_manager.get_towers()):
            tower_type = tower[0]
            upgrades = tower[2]
            
            # Check each path
            for path in [1, 2, 3]:
                # Validate path
                is_valid, _ = self.cost_calculator.validate_upgrade_path(upgrades, path)
                if not is_valid:
                    continue
                
                # Check tier 5 restriction
                path_index = path - 1
                if int(upgrades[path_index]) == 4:
                    if self.tower_manager.check_has_tier5(tower_type, path):
                        continue
                
                # Check affordability
                cost = self.tower_manager.get_upgrade_cost(i, path)
                if cost != -1 and cost <= current_money:
                    viable.append((i, path))
        
        return viable

    def on_tower_placed(self, tower_type: str, location: int) -> None:
        """Callback when a tower is placed.
        
        Args:
            tower_type: Type of tower placed
            location: Location index where tower was placed
        """
        self.move_count += 1

    def on_tower_upgraded(self, tower_index: int, path: int) -> None:
        """Callback when a tower is upgraded.
        
        Args:
            tower_index: Index of the tower that was upgraded
            path: Upgrade path (1, 2, or 3)
        """
        self.move_count += 1
