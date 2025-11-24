"""Game controller implementation."""
import time
from typing import Dict, Tuple
from interfaces.strategy import IStrategy
from interfaces.tower_placer import ITowerPlacer


class GameController:
    """Main game controller that orchestrates the game playing."""

    def __init__(
        self,
        tower_placer: ITowerPlacer,
        strategy: IStrategy
    ):
        """Initialize the game controller.
        
        Args:
            tower_placer: Tower placement interface
            strategy: Game strategy interface
        """
        self.tower_placer = tower_placer
        self.strategy = strategy

    def execute_action(self, action_type: str, params: dict) -> bool:
        """Execute a game action.
        
        Args:
            action_type: Type of action ('place', 'upgrade', 'wait')
            params: Action parameters
            
        Returns:
            True if action was successful, False otherwise
        """
        if action_type == 'place':
            return self._execute_place(params)
        elif action_type == 'upgrade':
            return self._execute_upgrade(params)
        elif action_type == 'wait':
            return True
        return False

    def _execute_place(self, params: dict) -> bool:
        """Execute a tower placement action.
        
        Args:
            params: Placement parameters
            
        Returns:
            True if successful, False otherwise
        """
        tower_type = params.get('tower_type')
        if not tower_type:
            return False

        # Check if we need to find next available location
        if params.get('next_available', False):
            location = self.tower_placer.find_next_available_location()
            if location == -1:
                return False
        else:
            location = params.get('location')
            if location is None:
                return False

        success = self.tower_placer.place_tower(tower_type, location)
        if success:
            self.strategy.on_tower_placed(tower_type, location)
        return success

    def _execute_upgrade(self, params: dict) -> bool:
        """Execute a tower upgrade action.
        
        Args:
            params: Upgrade parameters
            
        Returns:
            True if successful, False otherwise
        """
        tower_index = params.get('tower_index')
        path = params.get('path')
        
        if tower_index is None or path is None:
            return False

        success = self.tower_placer.upgrade_tower(tower_index, path)
        if success:
            self.strategy.on_tower_upgraded(tower_index, path)
        return success

    def play_turn(self) -> None:
        """Execute one turn of the game."""
        action_type, params = self.strategy.decide_next_action()
        self.execute_action(action_type, params)

    def get_status(self) -> Dict:
        """Get current game status.
        
        Returns:
            Dictionary with status information
        """
        towers = self.tower_placer.get_towers()
        return {
            'tower_count': len(towers),
            'towers': towers
        }
