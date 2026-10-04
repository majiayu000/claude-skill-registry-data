---
name: evo-travel-itinerary-builder
description: Assembles 7-day travel itinerary with route optimization, budget validation, and JSON output.
---
# evo-travel-itinerary-builder
## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-travel-itinerary-builder/scripts')
from utils import (optimize_route, allocate_days_to_cities, validate_budget,
    build_daily_plan, generate_itinerary_json)
route = optimize_route('Minneapolis', ['Cleveland','Columbus','Cincinnati'])
alloc = allocate_days_to_cities(route)
plan, tools = build_daily_plan(alloc, ['American','Mediterranean','Chinese','Italian'])
generate_itinerary_json(plan, tools)
```
