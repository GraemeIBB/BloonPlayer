# Procedural Placement Mask Generation

## Overview

The Procedural Placement Mask Generation system provides an automated way to evaluate and select optimal monkey tower placement locations on Bloons TD6 maps. It uses proximity to the bloon path to score locations, helping the automation make more strategic placement decisions.

## How It Works

### Core Concept

The placement mask system evaluates each potential monkey placement location based on its proximity to the path that bloons travel along. Locations closer to the path are scored higher since towers there can attack bloons for a longer duration.

### Scoring Algorithm

1. **Path Segments**: The bloon path is represented as a series of line segments
2. **Distance Calculation**: For each location, the system calculates the minimum distance to each path segment
3. **Threshold Filtering**: Only path segments within a configurable threshold distance are considered
4. **Weighted Scoring**: Closer segments contribute more to the score, with weights scaled inversely to distance
5. **Final Score**: The location's score is the sum of all weighted contributions

### Formula

For a location `L` and path segments `S1, S2, ..., Sn`:

```
score(L) = Σ [weight(distance(L, Si)) / (distance(L, Si) + 1)]
```

Where:
- `distance(L, Si)` is the shortest distance from location L to segment Si
- `weight(d)` scales linearly from `min_weight` (d=0) to `max_weight` (d=threshold)
- Only segments where `distance(L, Si) <= threshold` are included

## Usage

### Basic Usage

```python
from placement_mask import PlacementMask
from locations import monkey_meadow

# Create a placement mask
mask = PlacementMask(map_locations=monkey_meadow)

# Get the best placement locations
best_locations = mask.get_best_locations(count=10)

for location_id, score in best_locations:
    print(f"Location {location_id}: Score {score}")
```

### Integration with Placer

```python
from placer import Placer

placer = Placer()

# The placement mask is automatically initialized
# Use strategic placement
placer.placeStrategic("wizard_monkey")

# Or get the best available location manually
best_location = placer.getBestAvailableLocation()
if best_location:
    placer.place("dart_monkey", best_location)
```

### Advanced Configuration

```python
# Custom path segments
custom_path = [
    ((0, 100), (500, 100)),
    ((500, 100), (500, 500)),
]

# Custom parameters
mask = PlacementMask(
    map_locations=monkey_meadow,
    path_segments=custom_path,
    distance_threshold=300.0,  # Larger search radius
    min_distance_weight=2.0,   # Higher weight for close segments
    max_distance_weight=0.2    # Lower weight for far segments
)

# Excluding specific locations
occupied_locations = [1, 2, 3]
best = mask.get_best_locations(
    count=5,
    excluded_locations=occupied_locations
)
```

## Configuration Parameters

### `distance_threshold` (default: 200.0)
- Maximum distance (in pixels) to consider a path segment relevant
- Larger values consider more of the path but may dilute the scoring
- Smaller values focus on locations very close to the path
- **Effect**: With threshold=100, only 8 locations are viable; with threshold=400, 26 locations are viable

### `min_distance_weight` (default: 1.0)
- Weight applied to the closest point on the path
- Higher values increase the importance of being very close to the path
- **Effect**: Amplifies score differences between locations

### `max_distance_weight` (default: 0.1)
- Weight applied to segments at the threshold distance
- Lower values reduce the importance of far segments
- **Effect**: Creates stronger bias toward locations close to the path

## API Reference

### PlacementMask Class

#### `__init__(map_locations, path_segments=None, distance_threshold=200.0, min_distance_weight=1.0, max_distance_weight=0.1)`
Initialize the placement mask.

**Parameters:**
- `map_locations`: Dictionary mapping location IDs to (x, y) coordinates
- `path_segments`: List of line segments as ((x1, y1), (x2, y2)) tuples (optional)
- `distance_threshold`: Maximum distance to consider path segments
- `min_distance_weight`: Weight for closest path segment
- `max_distance_weight`: Weight for farthest path segment within threshold

#### `calculate_location_score(location_id) -> float`
Calculate the placement value score for a specific location.

**Returns:** Placement score (higher is better), or 0 if location doesn't exist or is too far from path

#### `get_all_location_scores() -> Dict[int, float]`
Calculate placement scores for all locations on the map.

**Returns:** Dictionary mapping location IDs to their placement scores

#### `get_best_locations(count=5, excluded_locations=None) -> List[Tuple[int, float]]`
Get the best placement locations sorted by score.

**Parameters:**
- `count`: Number of top locations to return
- `excluded_locations`: List of location IDs to exclude from results

**Returns:** List of (location_id, score) tuples sorted by score (highest first)

#### `set_distance_threshold(threshold)`
Update the distance threshold and clear the cache.

#### `set_weights(min_weight, max_weight)`
Update the distance weights and clear the cache.

#### `clear_cache()`
Clear the score cache. Useful when parameters change.

### Placer Integration Methods

#### `getBestAvailableLocation(count=5) -> Optional[int]`
Get the best available placement location, excluding occupied positions.

**Parameters:**
- `count`: Number of top locations to consider

**Returns:** Best available location ID, or None if no locations available

#### `placeStrategic(type) -> int`
Place a monkey at the best strategic location based on placement mask.

**Parameters:**
- `type`: Type of monkey to place (e.g., "wizard_monkey")

**Returns:** 1 if placed successfully, -1 otherwise

## Testing

The implementation includes comprehensive test coverage:

### Unit Tests (`test_placement_mask.py`)
- Distance calculation accuracy
- Score calculation and caching
- Parameter tuning effects
- Integration with Monkey Meadow map data
- **Result**: 15 tests, all passing

### Integration Tests (`test_placer_integration.py`)
- PlacementMask initialization in Placer
- Best location selection with occupied positions
- Strategic placement functionality
- **Result**: 6 tests, all passing

Run tests with:
```bash
python3 -m unittest discover -s . -p "test_*.py" -v
```

## Demo

A demonstration script is provided to show the placement mask in action:

```bash
python3 demo_placement_mask.py
```

This will display:
- Top 10 best placement locations for Monkey Meadow
- Locations too far from the path
- Effect of threshold tuning
- Effect of weight tuning
- Alternative locations with exclusions

## Example Output

For Monkey Meadow with default settings:

```
Top 10 Best Placement Locations:
 1. Location  9 at (648, 531): Score = 0.1007
 2. Location 11 at (932, 438): Score = 0.0947
 3. Location 20 at (1144, 431): Score = 0.0671
 4. Location  3 at (253, 350): Score = 0.0227
 5. Location  1 at (133, 350): Score = 0.0226
```

These locations are strategically positioned near the bloon path for optimal tower effectiveness.

## Performance

- **Caching**: Scores are cached to avoid redundant calculations
- **Complexity**: O(n×m) where n = locations, m = path segments
- **Typical Performance**: <1ms to score all 27 Monkey Meadow locations

## Future Enhancements

Potential improvements:
1. **Range-based scoring**: Factor in tower attack range
2. **Multi-path support**: Handle maps with multiple parallel paths
3. **Coverage optimization**: Avoid placing too many towers in the same area
4. **Tower-specific scoring**: Different evaluation for different tower types
5. **Dynamic path learning**: Learn actual bloon paths from gameplay

## Contributing

When adding new maps:
1. Define the map's location coordinates in `locations.py`
2. Create corresponding path segments in PlacementMask
3. Run tests to validate scoring
4. Tune threshold and weights as needed for the specific map

## License

This is part of the BloonPlayer project. See main repository for license information.
