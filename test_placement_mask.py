"""
Test suite for placement_mask module
"""

import unittest
from placement_mask import PlacementMask


class TestPlacementMask(unittest.TestCase):
    """Test cases for PlacementMask class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Simple test map with 5 locations
        self.test_map = {
            1: (100, 100),
            2: (200, 200),
            3: (300, 300),
            4: (400, 400),
            5: (500, 500),
        }
        
        # Simple path segments
        self.test_path = [
            ((0, 200), (600, 200)),    # Horizontal line through middle
        ]
        
        self.mask = PlacementMask(
            map_locations=self.test_map,
            path_segments=self.test_path,
            distance_threshold=200.0
        )
    
    def test_initialization(self):
        """Test PlacementMask initialization"""
        self.assertEqual(self.mask.map_locations, self.test_map)
        self.assertEqual(self.mask.path_segments, self.test_path)
        self.assertEqual(self.mask.distance_threshold, 200.0)
    
    def test_point_to_segment_distance(self):
        """Test distance calculation from point to segment"""
        # Point directly on the segment
        segment = ((0, 0), (100, 0))
        point = (50, 0)
        distance = self.mask._point_to_segment_distance(point, segment)
        self.assertAlmostEqual(distance, 0.0, places=2)
        
        # Point perpendicular to segment
        point = (50, 50)
        distance = self.mask._point_to_segment_distance(point, segment)
        self.assertAlmostEqual(distance, 50.0, places=2)
        
        # Point beyond segment end
        point = (150, 0)
        distance = self.mask._point_to_segment_distance(point, segment)
        self.assertAlmostEqual(distance, 50.0, places=2)
    
    def test_calculate_location_score(self):
        """Test location score calculation"""
        # Location 2 is at (200, 200), exactly on the path (y=200)
        score_2 = self.mask.calculate_location_score(2)
        self.assertGreater(score_2, 0, "Location on path should have positive score")
        
        # Location 5 is at (500, 500), farther from path
        score_5 = self.mask.calculate_location_score(5)
        
        # Location closer to path should have higher score
        self.assertGreater(score_2, score_5, "Closer location should score higher")
    
    def test_calculate_location_score_invalid(self):
        """Test score calculation for invalid location"""
        score = self.mask.calculate_location_score(999)
        self.assertEqual(score, 0.0, "Invalid location should return 0")
    
    def test_get_all_location_scores(self):
        """Test getting scores for all locations"""
        scores = self.mask.get_all_location_scores()
        
        self.assertEqual(len(scores), len(self.test_map))
        for loc_id in self.test_map.keys():
            self.assertIn(loc_id, scores)
            self.assertGreaterEqual(scores[loc_id], 0)
    
    def test_get_best_locations(self):
        """Test getting best placement locations"""
        best = self.mask.get_best_locations(count=3)
        
        self.assertEqual(len(best), 3)
        # Results should be sorted by score (descending)
        self.assertGreaterEqual(best[0][1], best[1][1])
        self.assertGreaterEqual(best[1][1], best[2][1])
    
    def test_get_best_locations_with_exclusions(self):
        """Test getting best locations with exclusions"""
        all_best = self.mask.get_best_locations(count=5)
        top_location = all_best[0][0]
        
        # Exclude the top location
        best_excluded = self.mask.get_best_locations(count=5, excluded_locations=[top_location])
        
        # The excluded location should not appear in results
        excluded_ids = [loc[0] for loc in best_excluded]
        self.assertNotIn(top_location, excluded_ids)
    
    def test_score_caching(self):
        """Test that scores are cached properly"""
        score_1 = self.mask.calculate_location_score(1)
        
        # Second call should use cache
        score_2 = self.mask.calculate_location_score(1)
        self.assertEqual(score_1, score_2)
        
        # Check cache was populated
        self.assertIn(1, self.mask._score_cache)
    
    def test_clear_cache(self):
        """Test cache clearing"""
        self.mask.calculate_location_score(1)
        self.assertGreater(len(self.mask._score_cache), 0)
        
        self.mask.clear_cache()
        self.assertEqual(len(self.mask._score_cache), 0)
    
    def test_set_distance_threshold(self):
        """Test updating distance threshold clears cache"""
        self.mask.calculate_location_score(1)
        original_score = self.mask._score_cache[1]
        
        self.mask.set_distance_threshold(100.0)
        self.assertEqual(self.mask.distance_threshold, 100.0)
        self.assertEqual(len(self.mask._score_cache), 0)
    
    def test_set_weights(self):
        """Test updating weights clears cache"""
        self.mask.calculate_location_score(1)
        
        self.mask.set_weights(2.0, 0.5)
        self.assertEqual(self.mask.min_distance_weight, 2.0)
        self.assertEqual(self.mask.max_distance_weight, 0.5)
        self.assertEqual(len(self.mask._score_cache), 0)
    
    def test_distance_threshold_filtering(self):
        """Test that locations beyond threshold get zero score"""
        # Create a mask with very small threshold
        small_threshold_mask = PlacementMask(
            map_locations=self.test_map,
            path_segments=self.test_path,
            distance_threshold=10.0  # Very small threshold
        )
        
        # Location 5 is at (500, 500), 300 pixels from path
        # With threshold of 10, it should score 0
        score = small_threshold_mask.calculate_location_score(5)
        self.assertEqual(score, 0.0, "Location beyond threshold should score 0")


class TestPlacementMaskWithMonkeyMeadow(unittest.TestCase):
    """Test PlacementMask with actual Monkey Meadow data"""
    
    def setUp(self):
        """Set up with actual monkey meadow locations"""
        from locations import monkey_meadow
        self.mask = PlacementMask(map_locations=monkey_meadow)
    
    def test_monkey_meadow_initialization(self):
        """Test that monkey meadow mask initializes correctly"""
        self.assertIsNotNone(self.mask.map_locations)
        self.assertGreater(len(self.mask.map_locations), 0)
        self.assertIsNotNone(self.mask.path_segments)
        self.assertGreater(len(self.mask.path_segments), 0)
    
    def test_monkey_meadow_all_scores(self):
        """Test scoring all monkey meadow locations"""
        scores = self.mask.get_all_location_scores()
        
        # Should have score for each location
        self.assertEqual(len(scores), len(self.mask.map_locations))
        
        # At least some locations should have positive scores
        positive_scores = [s for s in scores.values() if s > 0]
        self.assertGreater(len(positive_scores), 0)
    
    def test_monkey_meadow_best_locations(self):
        """Test getting best locations on monkey meadow"""
        best = self.mask.get_best_locations(count=10)
        
        self.assertEqual(len(best), 10)
        # All should have location IDs and scores
        for loc_id, score in best:
            self.assertIn(loc_id, self.mask.map_locations)
            self.assertGreaterEqual(score, 0)


if __name__ == '__main__':
    unittest.main()
