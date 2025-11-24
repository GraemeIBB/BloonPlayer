"""
Procedural Placement Mask Generation Module

This module provides functionality to generate placement masks that evaluate
viable locations for monkey placement based on proximity to bloon path segments.
"""

import math
from typing import List, Tuple, Dict, Optional


class PlacementMask:
    """
    Generates and evaluates placement masks for monkey towers based on their
    proximity to bloon path segments.
    """
    
    def __init__(self, map_locations: Dict[int, Tuple[int, int]], 
                 path_segments: Optional[List[Tuple[Tuple[int, int], Tuple[int, int]]]] = None,
                 distance_threshold: float = 200.0,
                 min_distance_weight: float = 1.0,
                 max_distance_weight: float = 0.1):
        """
        Initialize the PlacementMask generator.
        
        Args:
            map_locations: Dictionary mapping location IDs to (x, y) coordinates
            path_segments: List of line segments representing the bloon path as 
                         ((x1, y1), (x2, y2)) tuples. If None, will use default for map.
            distance_threshold: Maximum distance to consider path segments (pixels)
            min_distance_weight: Weight for closest path segment (default 1.0)
            max_distance_weight: Weight for farthest path segment within threshold (default 0.1)
        """
        self.map_locations = map_locations
        self.path_segments = path_segments if path_segments else self._get_default_path_segments()
        self.distance_threshold = distance_threshold
        self.min_distance_weight = min_distance_weight
        self.max_distance_weight = max_distance_weight
        
        # Cache for calculated scores
        self._score_cache: Dict[int, float] = {}
    
    def _get_default_path_segments(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Returns default path segments for Monkey Meadow map.
        This represents the general path that bloons travel.
        
        Returns:
            List of line segments as ((x1, y1), (x2, y2)) tuples
        """
        # Monkey Meadow path - approximated from typical gameplay
        # Path goes from left to right with some curves
        return [
            ((50, 400), (200, 400)),      # Entry from left
            ((200, 400), (350, 450)),     # Slight curve down
            ((350, 450), (500, 500)),     # Continue down
            ((500, 500), (650, 550)),     # More right
            ((650, 550), (800, 500)),     # Curve up
            ((800, 500), (950, 450)),     # Continue curve
            ((950, 450), (1100, 450)),    # Straighten out
            ((1100, 450), (1250, 450)),   # Continue right
            ((1250, 450), (1400, 450)),   # Exit to right
        ]
    
    def _point_to_segment_distance(self, point: Tuple[int, int], 
                                   segment: Tuple[Tuple[int, int], Tuple[int, int]]) -> float:
        """
        Calculate the shortest distance from a point to a line segment.
        
        Args:
            point: (x, y) coordinates of the point
            segment: Line segment as ((x1, y1), (x2, y2))
            
        Returns:
            Minimum distance from point to segment
        """
        px, py = point
        (x1, y1), (x2, y2) = segment
        
        # Vector from segment start to point
        dx = x2 - x1
        dy = y2 - y1
        
        # Handle degenerate segment (point)
        if dx == 0 and dy == 0:
            return math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
        
        # Calculate parameter t for closest point on line
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        
        # Calculate closest point on segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        # Return distance to closest point
        return math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)
    
    def calculate_location_score(self, location_id: int) -> float:
        """
        Calculate the placement value score for a given location.
        
        Score is based on proximity to path segments within the distance threshold.
        Closer segments contribute more to the score, with weights scaled by distance.
        
        Args:
            location_id: The location ID to evaluate
            
        Returns:
            Placement score (higher is better). Returns 0 if location doesn't exist
            or is too far from all path segments.
        """
        # Check cache first
        if location_id in self._score_cache:
            return self._score_cache[location_id]
        
        # Get location coordinates
        if location_id not in self.map_locations:
            return 0.0
        
        location = self.map_locations[location_id]
        
        # Calculate distances to all path segments
        segment_distances = []
        for segment in self.path_segments:
            distance = self._point_to_segment_distance(location, segment)
            if distance <= self.distance_threshold:
                segment_distances.append(distance)
        
        # If no segments within threshold, score is 0
        if not segment_distances:
            self._score_cache[location_id] = 0.0
            return 0.0
        
        # Calculate score based on weighted sum of inverse distances
        # Closer segments contribute more to the score
        total_score = 0.0
        for distance in segment_distances:
            # Normalize distance to [0, 1] range within threshold
            normalized_distance = distance / self.distance_threshold
            
            # Calculate weight (inverse relationship - closer is better)
            # Weight ranges from min_distance_weight (distance=0) to max_distance_weight (distance=threshold)
            weight = self.max_distance_weight + (self.min_distance_weight - self.max_distance_weight) * (1 - normalized_distance)
            
            # Add weighted contribution (inverse of distance)
            # Using 1/(distance+1) to avoid division by zero
            contribution = weight / (distance + 1)
            total_score += contribution
        
        self._score_cache[location_id] = total_score
        return total_score
    
    def get_all_location_scores(self) -> Dict[int, float]:
        """
        Calculate placement scores for all locations on the map.
        
        Returns:
            Dictionary mapping location IDs to their placement scores
        """
        scores = {}
        for location_id in self.map_locations.keys():
            scores[location_id] = self.calculate_location_score(location_id)
        return scores
    
    def get_best_locations(self, count: int = 5, 
                          excluded_locations: Optional[List[int]] = None) -> List[Tuple[int, float]]:
        """
        Get the best placement locations sorted by score.
        
        Args:
            count: Number of top locations to return
            excluded_locations: List of location IDs to exclude from results
            
        Returns:
            List of (location_id, score) tuples sorted by score (highest first)
        """
        excluded = set(excluded_locations) if excluded_locations else set()
        
        # Calculate scores for all locations
        all_scores = self.get_all_location_scores()
        
        # Filter out excluded locations
        filtered_scores = {loc: score for loc, score in all_scores.items() 
                          if loc not in excluded}
        
        # Sort by score (descending) and return top count
        sorted_locations = sorted(filtered_scores.items(), 
                                 key=lambda x: x[1], 
                                 reverse=True)
        
        return sorted_locations[:count]
    
    def clear_cache(self):
        """Clear the score cache. Useful when parameters change."""
        self._score_cache.clear()
    
    def set_distance_threshold(self, threshold: float):
        """Update the distance threshold and clear cache."""
        self.distance_threshold = threshold
        self.clear_cache()
    
    def set_weights(self, min_weight: float, max_weight: float):
        """Update the distance weights and clear cache."""
        self.min_distance_weight = min_weight
        self.max_distance_weight = max_weight
        self.clear_cache()
