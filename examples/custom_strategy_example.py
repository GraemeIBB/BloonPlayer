"""Example: Creating a custom strategy.

This example demonstrates how to extend the system with a new strategy
following the Open/Closed Principle.
"""
from typing import Optional, Tuple, List
from interfaces.strategy import IStrategy
from interfaces.tower_placer import ITowerPlacer
from core.tower_manager import TowerManager
from core.cost_calculator import CostCalculator


class DartMonkeyStrategy(IStrategy):
    """Simple strategy that focuses on dart monkeys."""

    def __init__(
        self,
        tower_placer: ITowerPlacer,
        tower_manager: TowerManager,
        cost_calculator: CostCalculator
    ):
        """Initialize the strategy.
        
        Args:
            tower_placer: Tower placement interface
            tower_manager: Tower manager instance
            cost_calculator: Cost calculator instance
        """
        self.tower_placer = tower_placer
        self.tower_manager = tower_manager
        self.cost_calculator = cost_calculator
        self.move_count = 0

    def decide_next_action(self) -> Tuple[str, Optional[dict]]:
        """Decide the next action to take.
        
        Returns:
            Tuple of (action_type, action_params)
        """
        tower_count = len(self.tower_manager.get_towers())
        
        # Place dart monkeys until we have 5
        if tower_count < 5:
            return ('place', {'tower_type': 'dart_monkey', 'next_available': True})
        
        # After 5 towers, focus on upgrades
        return self._decide_upgrade()

    def _decide_upgrade(self) -> Tuple[str, Optional[dict]]:
        """Decide which tower to upgrade.
        
        Returns:
            Tuple of (action_type, action_params)
        """
        current_money = int(self.tower_manager.get_precise_money())
        
        # Prioritize upgrading path 1 (top path)
        for i, tower in enumerate(self.tower_manager.get_towers()):
            if tower[0] == 'dart_monkey':
                upgrades = tower[2]
                
                # Try to upgrade path 1
                if int(upgrades[0]) < 5:
                    is_valid, _ = self.cost_calculator.validate_upgrade_path(upgrades, 1)
                    if is_valid:
                        cost = self.tower_manager.get_upgrade_cost(i, 1)
                        if cost != -1 and cost <= current_money:
                            return ('upgrade', {'tower_index': i, 'path': 1})
        
        return ('wait', None)

    def on_tower_placed(self, tower_type: str, location: int) -> None:
        """Callback when a tower is placed."""
        self.move_count += 1

    def on_tower_upgraded(self, tower_index: int, path: int) -> None:
        """Callback when a tower is upgraded."""
        self.move_count += 1


def create_custom_game():
    """Example of creating a game with a custom strategy."""
    from money_detector import MoneyDetector
    from bindings import bindings
    from core.game_input import GameInput
    from core.tower_manager import TowerManager
    from core.cost_calculator import CostCalculator
    from core.tower_placer import TowerPlacer
    from core.game_controller import GameController
    from config.config_factory import ConfigFactory
    
    # Create configurations
    map_config = ConfigFactory.create_map_config('monkey_meadow')
    difficulty_config = ConfigFactory.create_difficulty_config('easy')
    
    # Create core components
    money_detector = MoneyDetector()
    game_input = GameInput()
    tower_manager = TowerManager(money_detector, difficulty_config.costs)
    cost_calculator = CostCalculator(difficulty_config.costs)
    
    # Create tower placer
    tower_placer = TowerPlacer(
        game_input,
        tower_manager,
        cost_calculator,
        map_config.locations,
        bindings
    )
    
    # Create custom strategy
    strategy = DartMonkeyStrategy(
        tower_placer,
        tower_manager,
        cost_calculator
    )
    
    # Create game controller
    game_controller = GameController(tower_placer, strategy)
    
    return game_controller


if __name__ == "__main__":
    print("This is an example file demonstrating custom strategy creation.")
    print("See the DartMonkeyStrategy class for implementation details.")
