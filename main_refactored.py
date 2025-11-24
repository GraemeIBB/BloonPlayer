"""Main entry point for BloonPlayer with refactored architecture.

This demonstrates using the new SOLID-principle-based architecture.
"""
import pyautogui
import time
from placer_refactored import PlacerRefactored


def main():
    """Main entry point."""
    # Activate the game window
    pyautogui.getWindowsWithTitle("BloonsTD6")[0].activate()
    
    # Create placer with refactored architecture
    # Uses dependency injection and follows SOLID principles
    placer = PlacerRefactored(difficulty='easy', map_name='monkey_meadow')
    
    # Main game loop
    while True:
        placer.play()
        print(placer.getMoneyStr())
        print(placer.getMonkeysStr())
        time.sleep(3)


if __name__ == "__main__":
    main()
