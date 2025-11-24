# Bloom Player

current highest round: 104 - Meadows, easy
notes: mostly wizards

## About

The goal of this project is to facilitate the playing of BTD6 without any human input. This means no scripts, no recorded actions to replicate. I want this to be as dynamic as possible, and indistinguishable from a high level player.

## Architecture

This project has been refactored to follow SOLID principles for better maintainability and extensibility. See [REFACTORING.md](REFACTORING.md) for detailed documentation on the architecture.

### Key Features
- **Modular Design**: Separated concerns into focused components
- **Dependency Injection**: Easy to test and extend
- **Strategy Pattern**: Pluggable game strategies
- **Factory Pattern**: Configurable maps and difficulties
- **Interface-Based**: Easy to mock and test

### Usage
```python
from placer_refactored import PlacerRefactored

# Create placer with configuration
placer = PlacerRefactored(difficulty='easy', map_name='monkey_meadow')

# Play the game
placer.play()
```

## Dependencies

- `pyautogui`: For controlling the mouse and keyboard.
- `pynput`: For listening to keyboard and mouse events.
- `Pillow`: For image processing tasks.
- `imutils`: For more image processing tasks.
- `numpy`: For numerical operations.
- `cv2`: For computer vision tasks.
