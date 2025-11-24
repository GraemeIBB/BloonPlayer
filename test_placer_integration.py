"""
Integration test for PlacementMask with Placer class
"""

import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock the external dependencies before importing placer
sys.modules['pyautogui'] = MagicMock()
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['money_detector'] = MagicMock()

from placer import Placer


class TestPlacerIntegration(unittest.TestCase):
    """Test integration of PlacementMask with Placer"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Placer should now work with mocked dependencies
        self.placer = Placer()
    
    def test_placement_mask_initialized(self):
        """Test that placement mask is initialized in Placer"""
        self.assertIsNotNone(self.placer.placement_mask)
        self.assertGreater(len(self.placer.placement_mask.map_locations), 0)
    
    def test_get_best_available_location_empty(self):
        """Test getting best location when no monkeys placed"""
        location = self.placer.getBestAvailableLocation()
        
        self.assertIsNotNone(location)
        self.assertIn(location, self.placer.map)
    
    def test_get_best_available_location_with_monkeys(self):
        """Test getting best location with some positions occupied"""
        # Simulate placing some monkeys
        self.placer.monkeys = [
            ["wizard_monkey", 9, "000"],   # Location 9 (best location)
            ["wizard_monkey", 11, "000"],  # Location 11 (second best)
        ]
        
        location = self.placer.getBestAvailableLocation()
        
        # Should not return occupied locations
        self.assertIsNotNone(location)
        self.assertNotIn(location, [9, 11])
        self.assertIn(location, self.placer.map)
    
    def test_get_best_available_location_all_occupied(self):
        """Test behavior when all top locations are occupied"""
        # Get all locations
        all_locations = list(self.placer.map.keys())
        
        # Occupy all but one location
        self.placer.monkeys = [
            ["wizard_monkey", loc, "000"] for loc in all_locations[:-1]
        ]
        
        location = self.placer.getBestAvailableLocation()
        
        # Should return the last available location
        self.assertIsNotNone(location)
        self.assertEqual(location, all_locations[-1])
    
    def test_place_strategic_mocked(self):
        """Test placeStrategic method (mocked to avoid game interaction)"""
        # Mock the place method to avoid actual game interaction
        self.placer.place = MagicMock()
        
        result = self.placer.placeStrategic("wizard_monkey")
        
        self.assertEqual(result, 1)
        self.placer.place.assert_called_once()
        
        # Verify it called place with a valid location
        call_args = self.placer.place.call_args
        self.assertEqual(call_args[0][0], "wizard_monkey")
        self.assertIn(call_args[0][1], self.placer.map)
    
    def test_place_strategic_no_locations(self):
        """Test placeStrategic when no locations available"""
        # Occupy all locations
        all_locations = list(self.placer.map.keys())
        self.placer.monkeys = [
            ["wizard_monkey", loc, "000"] for loc in all_locations
        ]
        
        self.placer.place = MagicMock()
        
        result = self.placer.placeStrategic("wizard_monkey")
        
        self.assertEqual(result, -1)
        self.placer.place.assert_not_called()


if __name__ == '__main__':
    unittest.main()
