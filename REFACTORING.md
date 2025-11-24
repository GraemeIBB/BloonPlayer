# BloonPlayer Refactoring Documentation

## Overview

This document explains the refactoring work done to implement SOLID principles in the BloonPlayer project. The refactoring improves code maintainability, extensibility, and testability while maintaining backward compatibility.

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)

**Before:** The `Placer` class had multiple responsibilities:
- Tower placement
- Tower upgrades
- Money detection
- Game strategy
- Input handling
- State management

**After:** Responsibilities are separated into focused classes:
- `GameInput`: Handles keyboard and mouse input
- `MoneyDetector`: Detects available money
- `TowerManager`: Manages tower state
- `CostCalculator`: Validates costs and affordability
- `TowerPlacer`: Handles tower placement operations
- `RandomWizardStrategy`: Makes strategic decisions
- `GameController`: Orchestrates game flow

### Open/Closed Principle (OCP)

**Before:** Hard-coded difficulty levels and strategies made extension difficult.

**After:**
- Abstract interfaces (`IStrategy`, `IGameInput`, `IMoneyDetector`, `ITowerPlacer`) allow new implementations without modifying existing code
- `ConfigFactory` allows registration of new maps and difficulties
- Strategy pattern enables adding new game strategies

### Liskov Substitution Principle (LSP)

**After:** All implementations follow their interface contracts:
- `GameInput` implements `IGameInput`
- `MoneyDetector` implements `IMoneyDetector`
- `TowerPlacer` implements `ITowerPlacer`
- `RandomWizardStrategy` implements `IStrategy`

Any class implementing these interfaces can be substituted without breaking functionality.

### Interface Segregation Principle (ISP)

**After:** Interfaces are focused and specific:
- `IGameInput`: Only input-related methods
- `IMoneyDetector`: Only money detection
- `ITowerPlacer`: Only tower placement/upgrade operations
- `IStrategy`: Only strategy decision methods

Classes only depend on the interfaces they use.

### Dependency Inversion Principle (DIP)

**Before:** Direct dependencies on concrete implementations.

**After:**
- High-level `GameController` depends on abstractions (`IStrategy`, `ITowerPlacer`)
- `TowerPlacer` depends on abstractions (`IGameInput`, `TowerManager`)
- Dependencies are injected through constructors
- Easy to mock for testing

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      PlacerRefactored                        │
│              (Backward Compatible Wrapper)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Uses
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      GameController                          │
│                 (Orchestrates Game Flow)                     │
└─────────────────────────────────────────────────────────────┘
                    │                    │
         ┌──────────┴──────────┐        │
         │                     │        │
         ↓                     ↓        ↓
┌─────────────────┐   ┌──────────────────┐
│   IStrategy     │   │  ITowerPlacer    │
│   (Interface)   │   │   (Interface)    │
└─────────────────┘   └──────────────────┘
         │                     │
         ↓                     ↓
┌─────────────────┐   ┌──────────────────┐
│ RandomWizard    │   │  TowerPlacer     │
│   Strategy      │   │                  │
└─────────────────┘   └──────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ↓               ↓               ↓
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │ IGameInput   │ │TowerManager  │ │CostCalculator│
      │ (Interface)  │ │              │ │              │
      └──────────────┘ └──────────────┘ └──────────────┘
              │               │
              ↓               ↓
      ┌──────────────┐ ┌──────────────┐
      │  GameInput   │ │IMoneyDetector│
      │              │ │ (Interface)  │
      └──────────────┘ └──────────────┘
                              │
                              ↓
                      ┌──────────────┐
                      │MoneyDetector │
                      │              │
                      └──────────────┘
```

## Key Components

### Interfaces (`interfaces/`)

- **IGameInput**: Interface for game input operations (keyboard, mouse)
- **IMoneyDetector**: Interface for money detection
- **IStrategy**: Interface for game strategies
- **ITowerPlacer**: Interface for tower placement and management

### Core Components (`core/`)

- **GameInput**: Concrete implementation of game input
- **TowerManager**: Manages tower state and operations
- **CostCalculator**: Calculates and validates costs
- **TowerPlacer**: Implements tower placement logic
- **GameController**: Main orchestrator for game flow

### Strategies (`strategies/`)

- **RandomWizardStrategy**: Strategy focusing on wizard monkeys with random upgrades
- Easy to add new strategies by implementing `IStrategy`

### Configuration (`config/`)

- **GameConfig**: Configuration for game setup
- **MapConfig**: Configuration for maps
- **DifficultyConfig**: Configuration for difficulty settings
- **ConfigFactory**: Factory for creating configurations

## Usage

### Using the Refactored Architecture

```python
from placer_refactored import PlacerRefactored

# Create placer with dependency injection
placer = PlacerRefactored(difficulty='easy', map_name='monkey_meadow')

# Use the same interface as before
placer.play()
print(placer.getMoneyStr())
print(placer.getMonkeysStr())
```

### Extending with a Custom Strategy

```python
from interfaces.strategy import IStrategy

class MyCustomStrategy(IStrategy):
    def decide_next_action(self):
        # Your custom logic here
        return ('place', {'tower_type': 'dart_monkey', 'location': 1})
    
    def on_tower_placed(self, tower_type, location):
        pass
    
    def on_tower_upgraded(self, tower_index, path):
        pass

# Use it
from core.game_controller import GameController
controller = GameController(tower_placer, MyCustomStrategy(...))
```

### Adding a New Map

```python
from config.config_factory import ConfigFactory

new_map_locations = {
    1: (100, 200),
    2: (150, 250),
    # ... more locations
}

ConfigFactory.register_map('my_new_map', new_map_locations)

# Use it
placer = PlacerRefactored(difficulty='easy', map_name='my_new_map')
```

## Benefits

1. **Maintainability**: Each class has a single, well-defined responsibility
2. **Extensibility**: New strategies, maps, and difficulties can be added without modifying existing code
3. **Testability**: Components can be tested in isolation with mock dependencies
4. **Reusability**: Core components can be reused in different contexts
5. **Backward Compatibility**: Original code still works via `PlacerRefactored` wrapper

## Migration Guide

The refactored code is fully backward compatible. Existing code using the `Placer` class can gradually migrate:

1. **No changes needed**: Use `PlacerRefactored` as a drop-in replacement for `Placer`
2. **Gradual adoption**: Start using specific components as needed
3. **Full migration**: Build custom configurations using the factory pattern

## Future Enhancements

The refactored architecture makes these enhancements easier:

1. **Multiple Strategies**: Easy to implement and switch between different strategies
2. **AI/ML Integration**: Strategy interface perfect for ML-based decision making
3. **Unit Testing**: All components can be tested with mocks
4. **Configuration Files**: Load maps and costs from JSON/YAML files
5. **Performance Monitoring**: Add decorators for timing and logging
6. **Replay System**: Record and replay actions using the strategy pattern
