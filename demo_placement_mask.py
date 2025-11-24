"""
Demonstration script for placement mask generation

This script demonstrates how to use the PlacementMask class to find optimal
monkey placement locations on the Monkey Meadow map.
"""

from placement_mask import PlacementMask
from locations import monkey_meadow


def main():
    """Demonstrate placement mask functionality"""
    
    print("=" * 60)
    print("Procedural Placement Mask Generation Demo")
    print("=" * 60)
    print()
    
    # Create a placement mask for Monkey Meadow
    print("Initializing PlacementMask for Monkey Meadow...")
    mask = PlacementMask(map_locations=monkey_meadow)
    print(f"✓ Loaded {len(monkey_meadow)} locations")
    print(f"✓ Using {len(mask.path_segments)} path segments")
    print(f"✓ Distance threshold: {mask.distance_threshold} pixels")
    print()
    
    # Calculate scores for all locations
    print("Calculating placement scores for all locations...")
    all_scores = mask.get_all_location_scores()
    print(f"✓ Calculated scores for {len(all_scores)} locations")
    print()
    
    # Find the best placement locations
    print("Top 10 Best Placement Locations:")
    print("-" * 60)
    best_locations = mask.get_best_locations(count=10)
    
    for rank, (location_id, score) in enumerate(best_locations, 1):
        coords = monkey_meadow[location_id]
        print(f"{rank:2d}. Location {location_id:2d} at {coords}: Score = {score:.4f}")
    print()
    
    # Show locations with zero score (too far from path)
    zero_score_locations = [loc for loc, score in all_scores.items() if score == 0]
    if zero_score_locations:
        print(f"Locations too far from path (score = 0): {sorted(zero_score_locations)}")
    else:
        print("All locations are within range of the path")
    print()
    
    # Demonstrate exclusion feature
    print("Top 5 locations excluding the best 3:")
    print("-" * 60)
    excluded = [loc[0] for loc in best_locations[:3]]
    alternative_locations = mask.get_best_locations(count=5, excluded_locations=excluded)
    
    for rank, (location_id, score) in enumerate(alternative_locations, 1):
        coords = monkey_meadow[location_id]
        print(f"{rank:2d}. Location {location_id:2d} at {coords}: Score = {score:.4f}")
    print()
    
    # Demonstrate threshold tuning
    print("Effect of Distance Threshold:")
    print("-" * 60)
    thresholds = [100, 200, 300, 400]
    for threshold in thresholds:
        mask.set_distance_threshold(threshold)
        scores = mask.get_all_location_scores()
        positive_count = sum(1 for s in scores.values() if s > 0)
        avg_score = sum(scores.values()) / len(scores)
        print(f"Threshold {threshold:3d}px: {positive_count:2d} viable locations, "
              f"avg score = {avg_score:.4f}")
    print()
    
    # Reset to default
    mask.set_distance_threshold(200.0)
    
    # Demonstrate weight tuning
    print("Effect of Distance Weights:")
    print("-" * 60)
    weight_configs = [
        (1.0, 0.1, "Default (high bias to close)"),
        (1.0, 0.5, "Moderate bias"),
        (1.0, 0.9, "Low bias (more uniform)"),
    ]
    
    for min_w, max_w, desc in weight_configs:
        mask.set_weights(min_w, max_w)
        best = mask.get_best_locations(count=3)
        top_score = best[0][1]
        bottom_score = best[2][1]
        print(f"{desc:30s}: Top={top_score:.4f}, 3rd={bottom_score:.4f}, "
              f"Range={top_score-bottom_score:.4f}")
    print()
    
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
