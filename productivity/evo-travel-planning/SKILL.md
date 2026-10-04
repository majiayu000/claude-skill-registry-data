---
name: evo-travel-planning
description: Build multi-day travel itineraries from structured databases (cities, accommodations, restaurants, attractions, driving distances) with robust constraint validation, budget tracking, and pet-friendly filtering.
---

# evo-travel-planning

## Purpose
Build multi-day travel itineraries from structured CSV/text databases covering cities, accommodations, restaurants, attractions, and driving distances. Handles complex constraints including pet-friendly accommodations, cuisine preferences, budget limits, multi-city routing, and transportation restrictions.

## Key Rules
1. All data must come from database files in `/app/data/` — never use LLM memory for POIs.
2. **Pet-friendly accommodations**: `house_rules` column must NOT contain "No pets" (use `na=False` to handle NaN safely per Pandas 2.0.3 best practices).
3. Output accommodation field MUST contain "Pet-friendly" prefix when pet-friendly is required.
4. Cuisine coverage verified from restaurant `Cuisines` field, not restaurant names.
5. All 5 tool names must appear in `tool_called`: `search_cities`, `search_accommodations`, `search_restaurants`, `search_attractions`, `search_driving_distance`.
6. Attractions separated by semicolons with trailing semicolon (e.g., `"Attraction A;Attraction B;"`).
7. Transportation format: `"Self-driving: from A to B"` or `"-"` for same-city days.
8. `current_city`: city name for same-city days, or `"from A to B"` for transit days.
9. Budget validation: accommodations are per-night, meals are per-person, transportation is per-trip.
10. Uses `pd.concat()` instead of deprecated `DataFrame.append()` (removed in Pandas 2.0).

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-travel-planning/scripts')
from utils import (
    search_cities, search_accommodations, search_restaurants,
    search_attractions, search_driving_distance,
    format_accommodation_name, format_attractions,
    build_itinerary, save_itinerary, validate_budget,
    optimize_route, allocate_days_to_cities,
    get_cheapest_accommodation, get_restaurants_by_cuisines
)

# 1. Search Ohio cities
ohio_cities = search_cities(state='Ohio')

# 2. Optimize route from origin through destination cities
route = optimize_route('Minneapolis', ['Cleveland', 'Columbus', 'Cincinnati'])

# 3. Allocate days across cities
allocation = allocate_days_to_cities(route, total_days=7)

# 4. Find pet-friendly accommodations
accomm = search_accommodations(city='Cleveland', pet_friendly=True, min_occupancy=2)

# 5. Find cheapest pet-friendly accommodation
cheapest = get_cheapest_accommodation(city='Cleveland', pet_friendly=True, min_occupancy=2)

# 6. Find restaurants by multiple cuisines
restaurants = get_restaurants_by_cuisines(city='Cleveland',
    cuisines=['American', 'Mediterranean', 'Chinese', 'Italian'])

# 7. Get attractions
attractions = search_attractions(city='Cleveland')

# 8. Check driving distance/cost
dist = search_driving_distance(origin='Minneapolis', destination='Cleveland')

# 9. Validate budget
budget_result = validate_budget(
    accommodation_costs=[{'price': 80, 'nights': 2}],
    meal_costs=[15, 20, 25],
    transport_costs=[50],
    num_travelers=2,
    budget=5100
)

# 10. Build and save
itinerary = build_itinerary(plan_days, tools_used)
save_itinerary(itinerary)
```