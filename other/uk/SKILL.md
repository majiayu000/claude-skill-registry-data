---
name: United Kingdom
slug: uk
version: 1.0.0
description: Plan United Kingdom trips with nation-specific routing, ETA-aware entry rules, rail-road tradeoffs, and practical local logistics.
homepage: https://clawic.com/skills/uk
changelog: Initial release with verified UK entry rules, nation-level routing, and practical rail-road travel logistics.
metadata:
  clawdbot:
    emoji: 🇬🇧
    requires:
      bins: []
      config:
      - ~/Clawic/data/uk/
    os:
    - linux
    - darwin
    - win32
    displayName: United Kingdom
---

## When to Use

User is planning a United Kingdom trip and needs practical guidance beyond generic London tips: entry requirements, England-Scotland-Wales-Northern Ireland routing, rail versus car decisions, seasonality, costs, and on-the-ground execution.

## Architecture

Memory lives in `~/Clawic/data/uk/`. If `~/Clawic/data/uk/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/Clawic/data/uk/
└── memory.md     # Trip context and evolving constraints
```

## Data Storage

- `~/Clawic/data/uk/memory.md` stores durable trip context, route decisions, constraints, and reservation timing for future United Kingdom planning.
- No other local files are required unless the user chooses to create their own planning documents.

## Quick Reference

Use this map to load only the UK subtopic that changes the decision in front of you.

| Topic | File |
|-------|------|
| Setup flow | `setup.md` |
| Memory schema | `memory-template.md` |
| **Entry and Compliance** | |
| ETA, visa, passport, border logic | `entry-and-documents.md` |
| Customs, food, cash, duty context | `customs-and-border.md` |
| **Planning Backbone** | |
| Regions and route selection | `regions.md` |
| Sample itineraries | `itineraries.md` |
| Accommodation strategy | `accommodation.md` |
| Budget planning | `budget-and-costs.md` |
| Cards, cash, and tipping | `payments-and-tipping.md` |
| **Transport** | |
| Rail, flights, ferries, urban transit | `transport-domestic.md` |
| Driving and road-trip strategy | `road-trips-and-driving.md` |
| **Place Logic** | |
| London playbook | `london.md` |
| South England and Cotswolds playbook | `south-england-and-cotswolds.md` |
| North England and Lake District playbook | `north-england-and-lake-district.md` |
| Scotland playbook | `scotland.md` |
| Wales playbook | `wales.md` |
| Northern Ireland playbook | `northern-ireland.md` |
| Heritage and castle strategy | `heritage-and-castles.md` |
| **Lifestyle and Execution** | |
| Food by region and meal style | `food-guide.md` |
| Nightlife strategy by destination type | `nightlife.md` |
| Traveling with children | `family-travel.md` |
| Accessibility strategy | `accessibility.md` |
| **Safety and Conditions** | |
| Emergencies, disruptions, health basics | `safety-and-emergencies.md` |
| Seasonality and weather planning | `weather-and-seasonality.md` |
| **Tools** | |
| Connectivity and practical apps | `telecoms-and-apps.md` |
| Official source map | `sources.md` |

## Core Rules

### 1. Route by Nation and Corridor, Not by Checklist
Keep one macro-cluster per week: London plus South England, North England plus Scotland, or one nation-focused loop. UK rail and road networks are strong, but packing all four nations into a short trip still degrades quality.

### 2. Confirm Entry Logic Before Booking Non-Refundables
Use `entry-and-documents.md` first: ETA versus visa, passport validity, border flow, and any Ireland or Northern Ireland crossover complexity.

### 3. Match Transport to Geography
Always offer at least two movement models:
- Rail-first for London, major English cities, and Edinburgh/Glasgow corridors
- Car-first for Cotswolds, Cornwall, Highlands, Snowdonia, or coastal-rural loops

### 4. Distinguish Great Britain from Northern Ireland
Do not collapse the whole UK into one operating pattern. Payments, transport, geography, and cross-border considerations differ when Northern Ireland is involved.

### 5. Budget for the Real Total
Price the full trip, not the room headline:
- Rail yield pricing and advance-fare risk
- Hotel breakfast, parking, and city-centre premiums
- London transit and airport transfer costs
- National trust, castle, and parking day spend

### 6. Make Every Plan Season-Aware
Use `weather-and-seasonality.md` before promising island hops, Highlands driving, coastal hikes, or festival-heavy city weekends. Rain, wind, short winter daylight, and bank-holiday crowding materially shape good routes.

### 7. Deliver Actionable Plans
Every final output should include:
- Base strategy by city or region
- Day-by-day flow with realistic transfer windows
- Reservation deadlines
- Rain or disruption backup options
- Safety and emergency quick notes

## Common Traps

- Treating the UK as "London plus a few easy day trips" and missing nation-level tradeoffs.
- Combining London, Edinburgh, Highlands, Wales, and Belfast in one short trip.
- Renting a car for London-centred itineraries where rail and transit are superior.
- Assuming Ireland and Northern Ireland entry rules are interchangeable.
- Forgetting that rail fares can rise sharply without advance booking.
- Underestimating how much rain, wind, or short daylight can cut outdoor-heavy plans.
- Tipping or tax assumptions copied from the United States instead of UK norms.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/Clawic/data/uk/`

**This skill does NOT:** Access files outside `~/Clawic/data/uk/` or make network requests.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `travel` - General trip planning and itinerary structure
- `booking` - Reservation workflow and confirmation hygiene
- `car-rental` - Better rural and multi-stop rental strategy
- `food` - Deeper restaurant and cuisine planning
- `english` - Language help for bookings, menus, and service interactions

## Feedback

- If useful, star it: https://clawic.com/skills/uk
- Latest version: https://clawic.com/skills/uk
