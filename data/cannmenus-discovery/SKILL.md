---
name: CannMenus Discovery
description: Search cannabis products, menus, and retailers via CannMenus API.
---

# CannMenus Discovery Skill

## Capabilities
You can search the live inventory of dispensaries across the US.
- `searchProducts`: Find specific products (by query, category, price) nearby or globally.
- `findRetailers`: Locate dispensaries in a specific area.

## Usage Guidelines
1. **Location Aware**: Always try to filter by location (`near=` or `lat/lng`) if the user provides one.
2. **Pricing**: Use `price_min` and `price_max` to help users find deals.
3. **Availability**: Results represent a "snapshot" of the menu.

## When NOT to use
- Do not use for "Effect" or "Flavor" searching unless the keyword is part of the product name.
