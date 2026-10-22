---
name: travel-planning
version: 1.2.0
description: Plan trips, build itineraries, research destinations, estimate budgets, and organize logistics for Mick's travel. Always trigger immediately when the user mentions planning a trip, asks about flights, hotels, itineraries, destinations, or uses phrases like "trip to", "travel to", "planning a visit", "what should I do in", "how do I get to", "how much will this cost", or references any upcoming travel. Also trigger when the user mentions specific destinations, asks about visa requirements, crossing borders, ferry routes, or comparing travel options. This skill encodes Mick's full travel preferences and constraints so outputs are personalized from the first message — never produce generic travel advice.
---

# Travel Planning Skill

## Intent

Plan solo travel with destination fit, logistics, budget, preferences, booking triage, and itinerary handoff.

## Use When

- The user explicitly asks for `travel-planning`.
- The request matches the triggers or workflow described below.
- The task benefits from a reusable, structured output instead of a one-off answer.

## Do Not Use When

- Do not use for live booking, legal visa advice, medical travel advice, or broad research better handled by travel-research.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

## Workflow

1. Identify the exact task and available source material.
2. Apply the domain rules and output format in this skill.
3. State assumptions, uncertainty, and missing inputs clearly.
4. Return the requested artifact, recommendation, or review in a practical format.
5. Check the result against the validation checklist before finishing.

Produces personalized, opinionated travel plans for Mick Pletcher. Every output should reflect his specific constraints and preferences — never produce generic tourist recommendations.

---

## Who This Is For

**Mick Pletcher** — Automation Engineer, endurance athlete, and adventure traveler based in Nashville, TN. Visited 33+ countries, targeting 50. Summited Kilimanjaro. Background in competitive cycling and triathlon. Pursues geographic arbitrage and early retirement.

**Travel style: Solo by default.** All itineraries, budgets, and logistics are planned for one person unless Mick explicitly states otherwise. Do not suggest group tours, couples packages, or shared activities framed for multiple people. When Mick mentions a travel companion for a specific trip, note it and adjust accordingly but do not assume it carries over to other trips.

---

## Hard Constraints (Never Violate)

| Constraint | Rule |
|---|---|
| Accommodation | **Private rooms only** — no dorms, no shared baths |
| Home Airport | **BNA (Nashville)** — all flights route through BNA unless Mick specifies otherwise |
| Budget mindset | Value-optimized, not budget-backpacker and not luxury — target the best experience per dollar |
| Activities | Anchor the trip around an **endurance or adventure activity** when one is available (cycling, hiking, running events, climbing, skydiving, etc.) |
| Geographic arbitrage | Flag when a destination offers strong USD value — eating, accommodation, transport costs |

---

## Travel Preferences

**Accommodation style**: Boutique hotels, guesthouses, locally-owned properties. Avoid large chain hotels unless price/location is overwhelming.

**Pace**: Active and structured, not leisurely. Mick covers a lot of ground. Plan for full days.

**Food**: Street food and local spots over tourist restaurants. No dietary restrictions.

**Transport**: Train or ferry over flying when it's feasible and interesting. Renting a car is fine for rural/off-grid destinations.

**Experiences over things**: Prioritize events, physical challenges, cultural immersion over museums and shopping.

**Social media documentation**: Mick documents trips publicly on Facebook and X — good photo/video opportunities matter.

---

## What Claude Should Do When This Skill Triggers

### 1. Identify the trip type

Determine whether this is:
- **Event-anchored** (Tour de France, Running of the Bulls, a race, a summit attempt) — build the itinerary around the event dates, work outward
- **Destination-driven** (exploring a country or region) — anchor around an endurance activity if one fits
- **Logistics query** (flights, visas, border crossings, ferries) — answer precisely and completely
- **Comparison query** (choosing between destinations or trip styles) — score options against budget, training goals, climate, interests, and trip friction

Also infer the best trip style preset when the user does not name one:
- **Endurance travel** — training camps, races, mountain routes, trail access, recovery support
- **Sightseeing** — landmark density, walkability, culture, food, and easy logistics
- **Remote work** — Wi-Fi reliability, workspace fit, quiet lodging, time-zone practicality
- **Minimalist carry-only** — light packing, laundry access, transit simplicity, compact gear needs

### 2. Build the itinerary structure

For multi-city trips, produce a day-by-day breakdown:
- City/location per day
- Accommodation type and price range (in USD)
- Key activities (endurance anchor highlighted)
- Meals worth noting
- Transport between cities with method, duration, and cost
- Any booking lead time warnings (events, permits, popular routes)

When the request is still in the planning phase, separate what should be locked in now from what can wait:
- **Book now** — flights, event entries, permits, high-demand lodging, rental cars, or transit that sells out
- **Research later** — restaurants, optional excursions, backup stops, and lower-risk local details

If the user asks for a finished itinerary or is ready to move from planning into execution, hand off into a day-by-day itinerary structure directly instead of repeating abstract planning notes.

### 3. Budget estimate

Always produce a trip total with a per-day breakdown:
- Flights (BNA routing, round trip)
- Accommodation (nightly rate × nights)
- Food (realistic daily spend for the destination)
- Transport (intercity + local)
- Activities and entrance fees
- Buffer (10%)

Flag when a destination has strong USD purchasing power.

For destination comparison requests, also provide a simple scorecard that covers:
- Budget fit
- Training fit
- Climate fit
- Interest fit
- Transit simplicity
- Overall recommendation

### Airfare timing guidance

When flights are part of the plan, say whether to book now or watch, and why:

- international flights from BNA: typically best 2 to 5 months out; book sooner for peak season or event-anchored dates that will not move
- domestic flights: typically best 1 to 3 months out
- event-anchored trips: book as soon as dates are fixed; fare risk outweighs the chance of a dip when an event drives demand
- flexible destination-driven trips: watching for 2 to 3 weeks is reasonable; name the fare level that should trigger booking, such as "under $750 round trip, take it"

Keep the advice directional and dated; do not present fare predictions as certainties.

### Calendar matching

When the trip window is flexible, align the destination to Mick's training and event calendar instead of treating dates as fixed:

- check whether the destination has a race, gran fondo, climbing season, or cycling window that overlaps the candidate dates and could anchor the trip
- avoid scheduling hard adventure trips inside the final build weeks before a target race back home; flag the conflict instead of silently planning around it
- when two destinations score similarly, the one whose best season matches an open block in the calendar wins
- state which calendar assumption was used so Mick can correct it

### Accommodation placement

When recommending where to stay in a city, rank neighborhoods rather than just naming hotels:

- **transit access**: walkable to a rail or metro stop that reaches the airport and the day-trip launch points
- **training access**: runnable streets or waterfront, ride routes out of town without 30 minutes of traffic, or gym access on recovery days
- **workability**: reliable Wi-Fi and quiet at night when the trip includes remote work days

Name 2 to 3 candidate neighborhoods with a one-line tradeoff each, then suggest lodging inside the winner consistent with the boutique, private-room constraints.

### 4. Logistics flags

Proactively surface:
- Visa requirements for US passport holders
- Booking windows (what needs to be reserved months ahead)
- Peak season/crowd warnings
- Ferry or border crossing logistics
- Phone/SIM recommendations
- Currency situation

Also include planning risk notes when relevant:
- Transit complexity
- Safety or scam pressure
- Visa friction
- Overpacked itinerary risk
- Seasonal crowd or pricing pressure

Add seasonal guidance that states when the destination is:
- Great value
- Crowded
- Expensive
- Poor value for Mick's stated goals

Add packing and gear suggestions tied to the trip style. Focus on what changes because of the trip, not a generic packing list.

---

## Active Trip Context

When Mick mentions a specific upcoming trip, load the relevant reference file if one exists. For trips without a reference file, research inline and apply all hard constraints and preferences.

Current reference files:
- `references/europe-2026.md` — Summer 2026 Spain / Morocco / Portugal trip
- `references/colorado-2026.md` — Summer 2026 Colorado 14ers + Theodore Roosevelt NP

For any new destination not covered by a reference file, proceed using the hard constraints and preferences defined above. Do not treat this skill as limited to documented trips.

---

## Output Format

### For full itinerary requests:
```
TRIP: [Name / Dates]
TRIP STYLE: [Endurance / Sightseeing / Remote Work / Minimalist Carry-Only / Mixed]
TOTAL BUDGET ESTIMATE: $X,XXX

BOOK NOW:
- [critical reservations]

RESEARCH LATER:
- [lower urgency items]

DAY-BY-DAY:
Day 1 – [City]: ...
Day 2 – [City]: ...

BUDGET BREAKDOWN:
- Flights (BNA → X → BNA): $
- Accommodation (X nights): $
- Food (avg $/day × days): $
- Transport: $
- Activities: $
- Buffer (10%): $
TOTAL: $

LOGISTICS FLAGS:
- [Visa / booking windows / warnings]

RISK NOTES:
- [Transit / safety / visa / pacing / crowd notes]

PACKING AND GEAR:
- [Trip specific gear, clothing, or carry strategy]
```

### For single-destination or activity queries:
Answer directly and concisely. No need for full itinerary format unless asked.

### For budget comparisons:
Side-by-side table with per-day costs and totals.

### For destination comparison requests:
Use this structure:
```
DESTINATION COMPARISON

OPTIONS:
- [Destination A]
- [Destination B]

SCORECARD:
| Destination | Budget | Training | Climate | Interests | Transit | Overall |
|---|---:|---:|---:|---:|---:|---:|

SEASONAL NOTES:
- [Best window, crowd risk, value window]

BOOK NOW VS RESEARCH LATER:
- [Urgent items]
- [Deferred items]

RECOMMENDATION:
- [Best fit and why]

NEXT STEP:
- [Move into day-by-day itinerary planning or deeper research]
```

---

## Reference Files

- `references/europe-2026.md` — Detailed research notes for the Spain/Morocco/Portugal summer trip
- `references/colorado-2026.md` — Summit profiles, trailhead logistics, permit info

Load the relevant reference file when working on a specific trip. For new destinations not covered, research inline.

## Quality Checks

Before finalizing a planning response:
- Make sure trip style guidance actually matches the user goal instead of defaulting to generic travel advice.
- Check whether the destination is being judged against budget, training goals, climate, and interests when options are compared.
- Separate urgent booking actions from lower urgency research when the trip is not fully locked in yet.
- Call out seasonal value, crowd pressure, and obvious trip friction instead of leaving them implicit.
- Add trip-specific packing or gear notes only when they materially affect the plan.
- If enough planning detail exists, offer or produce a day-by-day itinerary next so the workflow can move directly into `travel-itinerary`.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A destination idea, date range, and the kind of trip you want.

Example prompts:

- `Use travel-planning to compare two solo trip options for budget, logistics, and training value.`
- `Plan a trip to Morocco from BNA with an active itinerary and realistic budget.`
- `Show me the fastest example prompt for using this skill to start trip planning.`

