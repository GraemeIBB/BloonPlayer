"""Game configuration."""
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class GameConfig:
    """Configuration for game setup."""
    
    difficulty: str
    map_name: str
    
    def __post_init__(self):
        """Validate configuration."""
        valid_difficulties = ['easy', 'medium', 'hard']
        if self.difficulty not in valid_difficulties:
            raise ValueError(f"Difficulty must be one of {valid_difficulties}")


@dataclass
class MapConfig:
    """Configuration for a game map."""
    
    name: str
    locations: Dict[int, Tuple[int, int]]
    
    def get_location(self, index: int) -> Tuple[int, int]:
        """Get location coordinates by index.
        
        Args:
            index: Location index
            
        Returns:
            (x, y) coordinates
        """
        return self.locations.get(index)


@dataclass
class DifficultyConfig:
    """Configuration for difficulty settings."""
    
    name: str
    costs: Dict[str, int]
    
    def get_cost(self, key: str) -> int:
        """Get cost for a tower or upgrade.
        
        Args:
            key: Tower/upgrade key
            
        Returns:
            Cost value, or -1 if not found
        """
        return self.costs.get(key, -1)
