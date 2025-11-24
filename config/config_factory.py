"""Configuration factory for creating game configurations."""
from typing import Dict, Tuple
from config.game_config import GameConfig, MapConfig, DifficultyConfig
from tower_costs import easy, medium, hard
from locations import monkey_meadow


class ConfigFactory:
    """Factory for creating game configurations."""
    
    _difficulty_configs = {
        'easy': easy,
        'medium': medium,
        'hard': hard
    }
    
    _map_configs = {
        'monkey_meadow': monkey_meadow
    }
    
    @classmethod
    def create_game_config(cls, difficulty: str, map_name: str) -> GameConfig:
        """Create a game configuration.
        
        Args:
            difficulty: Difficulty level ('easy', 'medium', 'hard')
            map_name: Map name
            
        Returns:
            GameConfig instance
        """
        return GameConfig(difficulty=difficulty, map_name=map_name)
    
    @classmethod
    def create_map_config(cls, map_name: str) -> MapConfig:
        """Create a map configuration.
        
        Args:
            map_name: Map name
            
        Returns:
            MapConfig instance
        """
        locations = cls._map_configs.get(map_name, {})
        return MapConfig(name=map_name, locations=locations)
    
    @classmethod
    def create_difficulty_config(cls, difficulty: str) -> DifficultyConfig:
        """Create a difficulty configuration.
        
        Args:
            difficulty: Difficulty level
            
        Returns:
            DifficultyConfig instance
        """
        costs = cls._difficulty_configs.get(difficulty, {})
        return DifficultyConfig(name=difficulty, costs=costs)
    
    @classmethod
    def register_map(cls, name: str, locations: Dict[int, Tuple[int, int]]) -> None:
        """Register a new map configuration.
        
        Args:
            name: Map name
            locations: Location coordinates
        """
        cls._map_configs[name] = locations
    
    @classmethod
    def register_difficulty(cls, name: str, costs: Dict[str, int]) -> None:
        """Register a new difficulty configuration.
        
        Args:
            name: Difficulty name
            costs: Tower costs dictionary
        """
        cls._difficulty_configs[name] = costs
