---
name: evo-travel-data-search
description: Query travel CSV datasets with filtering for pet-friendly, cuisine, city, state, budget.
---
# evo-travel-data-search
## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-travel-data-search/scripts')
from utils import (search_cities, search_accommodations, search_restaurants,
    search_attractions, search_transportation, search_distance)
cities = search_cities('Ohio')
hotels = search_accommodations('Cleveland', pet_friendly=True)
rests = search_restaurants('Cleveland', cuisine='Italian')
attractions = search_attractions('Cleveland')
dist = search_distance('Minneapolis', 'Cleveland')
```
