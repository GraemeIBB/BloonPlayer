"""Tower placement implementation."""
from typing import List, Dict, Tuple
from pynput.keyboard import Key
from interfaces.tower_placer import ITowerPlacer
from interfaces.game_input import IGameInput
from core.tower_manager import TowerManager
from core.cost_calculator import CostCalculator


class TowerPlacer(ITowerPlacer):
    """Concrete implementation of tower placement."""

    def __init__(
        self,
        game_input: IGameInput,
        tower_manager: TowerManager,
        cost_calculator: CostCalculator,
        map_locations: Dict[int, Tuple[int, int]],
        key_bindings: Dict[str, str]
    ):
        """Initialize the tower placer.
        
        Args:
            game_input: Game input interface
            tower_manager: Tower manager instance
            cost_calculator: Cost calculator instance
            map_locations: Map location coordinates
            key_bindings: Key bindings for towers and actions
        """
        self.game_input = game_input
        self.tower_manager = tower_manager
        self.cost_calculator = cost_calculator
        self.map_locations = map_locations
        self.key_bindings = key_bindings

    def place_tower(self, tower_type: str, location: int) -> bool:
        """Place a tower at the specified location.
        
        Args:
            tower_type: Type of tower to place (e.g., 'wizard_monkey')
            location: Location index on the map
            
        Returns:
            True if tower was placed successfully, False otherwise
        """
        # Check if location is already occupied
        for tower in self.tower_manager.get_towers():
            if tower[1] == location:
                return False

        # Check if we can afford it
        cost = self.tower_manager.get_tower_cost(tower_type)
        if cost == -1 or not self.tower_manager.can_afford(cost):
            return False

        # Check if location exists
        if location not in self.map_locations:
            return False

        # Get key binding
        key = self.key_bindings.get(tower_type)
        if not key:
            return False

        # Place the tower
        position = self.map_locations[location]
        self.game_input.move_to(position)
        self.game_input.press_key(key)
        self.game_input.click()

        # Add to tower list
        self.tower_manager.add_tower(tower_type, location)
        return True

    def upgrade_tower(self, tower_index: int, path: int) -> bool:
        """Upgrade a tower on a specific path.
        
        Args:
            tower_index: Index of the tower in the tower list
            path: Upgrade path (1, 2, or 3)
            
        Returns:
            True if upgrade was successful, False otherwise
        """
        tower = self.tower_manager.get_tower(tower_index)
        if not tower:
            return False

        # Validate upgrade path
        is_valid, _ = self.cost_calculator.validate_upgrade_path(tower[2], path)
        if not is_valid:
            return False

        # Check for tier 5 restriction
        path_index = path - 1
        if int(tower[2][path_index]) == 4:
            if self.tower_manager.check_has_tier5(tower[0], path):
                return False

        # Check if we can afford it
        cost = self.tower_manager.get_upgrade_cost(tower_index, path)
        if cost == -1 or not self.tower_manager.can_afford(cost):
            return False

        # Get upgrade key binding
        upgrade_keys = {
            1: self.key_bindings.get('upgrade_path_1'),
            2: self.key_bindings.get('upgrade_path_2'),
            3: self.key_bindings.get('upgrade_path_3')
        }
        keybind = upgrade_keys.get(path)
        if not keybind:
            return False

        # Perform upgrade
        location = tower[1]
        position = self.map_locations.get(location)
        if not position:
            return False

        self.game_input.move_to(position)
        self.game_input.click()
        self.game_input.press_key(keybind)
        self.game_input.press_key(Key.esc)

        # Update tower state
        self.tower_manager.upgrade_tower_state(tower_index, path)
        return True

    def get_towers(self) -> List[List]:
        """Get the list of placed towers.
        
        Returns:
            List of towers in format [type, location, upgrades]
        """
        return self.tower_manager.get_towers()

    def can_afford(self, cost: int) -> bool:
        """Check if player can afford a purchase.
        
        Args:
            cost: Cost of the item
            
        Returns:
            True if affordable, False otherwise
        """
        return self.tower_manager.can_afford(cost)

    def find_next_available_location(self) -> int:
        """Find the next available location on the map.
        
        Returns:
            Location index, or -1 if no locations available
        """
        occupied = {tower[1] for tower in self.tower_manager.get_towers()}
        available = set(self.map_locations.keys()) - occupied
        
        if not available:
            return -1
        
        return min(available)
