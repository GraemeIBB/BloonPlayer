"""Refactored Placer class with backward compatibility."""
import time
from typing import Dict, Tuple
from money_detector import MoneyDetector
from bindings import bindings
from core.game_input import GameInput
from core.tower_manager import TowerManager
from core.cost_calculator import CostCalculator
from core.tower_placer import TowerPlacer
from core.game_controller import GameController
from strategies.random_wizard_strategy import RandomWizardStrategy
from config.config_factory import ConfigFactory


class PlacerRefactored:
    """Refactored Placer class implementing SOLID principles.
    
    This class maintains the same interface as the original Placer class
    but uses composition and dependency injection internally.
    """

    def __init__(self, difficulty: str = 'easy', map_name: str = 'monkey_meadow'):
        """Initialize the refactored placer.
        
        Args:
            difficulty: Game difficulty ('easy', 'medium', 'hard')
            map_name: Map name
        """
        # Create configurations
        # Note: game_config validates difficulty level but is not currently used
        # for other purposes. Kept for future extensibility.
        game_config = ConfigFactory.create_game_config(difficulty, map_name)
        map_config = ConfigFactory.create_map_config(map_name)
        difficulty_config = ConfigFactory.create_difficulty_config(difficulty)
        
        # Create core components
        self.money_detector = MoneyDetector()
        self.game_input = GameInput()
        self.tower_manager = TowerManager(self.money_detector, difficulty_config.costs)
        self.cost_calculator = CostCalculator(difficulty_config.costs)
        
        # Create tower placer
        self.tower_placer = TowerPlacer(
            self.game_input,
            self.tower_manager,
            self.cost_calculator,
            map_config.locations,
            bindings
        )
        
        # Create strategy
        self.strategy = RandomWizardStrategy(
            self.tower_placer,
            self.tower_manager,
            self.cost_calculator
        )
        
        # Create game controller
        self.game_controller = GameController(
            self.tower_placer,
            self.strategy
        )
        
        # Keep references for backward compatibility
        self.monkeys = self.tower_manager.towers
        self.costs = difficulty_config.costs

    def play(self) -> None:
        """Execute one turn of the game."""
        self.game_controller.play_turn()

    def getMonkeysStr(self) -> str:
        """Get string representation of placed monkeys.
        
        Returns:
            String representation of monkeys list
        """
        return str(self.tower_manager.get_towers())

    def getMoneyStr(self) -> str:
        """Get current money amount.
        
        Returns:
            String representation of current money
        """
        return self.tower_manager.get_precise_money()

    def preciseMoney(self) -> str:
        """Get precise money reading (backward compatibility).
        
        Returns:
            String representation of current money
        """
        return self.tower_manager.get_precise_money()

    # Legacy methods for backward compatibility
    def place(self, tower_type: str, location: int) -> None:
        """Place a tower (backward compatibility).
        
        Args:
            tower_type: Type of tower to place
            location: Location index
        """
        self.tower_placer.place_tower(tower_type, location)

    def upgrade(self, monkey_index: int, choice: int) -> None:
        """Upgrade a monkey (backward compatibility).
        
        Args:
            monkey_index: Index of the monkey
            choice: Upgrade path (1, 2, or 3)
        """
        self.tower_placer.upgrade_tower(monkey_index, choice)

    def placeNext(self, tower_type: str) -> int:
        """Place tower at next available location (backward compatibility).
        
        Args:
            tower_type: Type of tower to place
            
        Returns:
            1 if successful, -1 otherwise
        """
        location = self.tower_placer.find_next_available_location()
        if location == -1:
            return -1
        
        success = self.tower_placer.place_tower(tower_type, location)
        return 1 if success else -1

    def placeWizardNext(self) -> None:
        """Place wizard at next available location (backward compatibility)."""
        self.placeNext("wizard_monkey")

    def placeSniper(self) -> None:
        """Place sniper at default location (backward compatibility)."""
        self.tower_placer.place_tower("sniper_monkey", 27)

    def upgradeRandom(self) -> None:
        """Perform random upgrade (backward compatibility)."""
        action_type, params = self.strategy.decide_next_action()
        if action_type == 'upgrade' and params:
            self.tower_placer.upgrade_tower(params['tower_index'], params['path'])
