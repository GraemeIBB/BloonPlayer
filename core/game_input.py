"""Game input implementation."""
import time
import pyautogui
from pynput.keyboard import Key, Controller
from typing import Tuple, Optional
from interfaces.game_input import IGameInput


class GameInput(IGameInput):
    """Concrete implementation of game input handling."""

    def __init__(self):
        """Initialize the game input handler."""
        self.keyboard = Controller()

    def press_key(self, key: str) -> None:
        """Press a keyboard key.
        
        Args:
            key: The key to press
        """
        # Handle special keys
        if key == Key.esc or isinstance(key, Key):
            actual_key = key
        else:
            actual_key = key
            
        self.keyboard.press(actual_key)
        time.sleep(0.1)
        self.keyboard.release(actual_key)
        time.sleep(0.1)

    def click(self, position: Optional[Tuple[int, int]] = None) -> None:
        """Click the mouse at the current or specified position.
        
        Args:
            position: Optional (x, y) position to click at
        """
        if position:
            pyautogui.click(position)
        else:
            pyautogui.click()

    def move_to(self, position: Tuple[int, int], duration: float = 0.5) -> None:
        """Move the mouse to a position.
        
        Args:
            position: (x, y) position to move to
            duration: Time in seconds to take for the movement
        """
        pyautogui.moveTo(position, duration=duration)
