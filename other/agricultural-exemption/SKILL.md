---
name: agricultural-exemption
description: |
  Use this skill when the user asks about the agricultural exemption from Hours of Service (HOS) rules under 49 CFR 395.1(k) — what qualifies as agricultural commodity, the 150-air-mile radius rule, state-declared planting/harvest seasons, livestock hauling specifics, and how to document operations under the exemption. Cite 49 CFR 395.1(k) and 49 USC 5117.
---

# Agricultural Exemption from HOS — 49 CFR 395.1(k)

The agricultural exemption is one of the most misunderstood HOS rules. Many operators think they qualify; many actually don't. This skill walks through the exact requirements.

## The exemption (49 CFR 395.1(k)(1))

During state-declared planting and harvesting periods, drivers transporting **agricultural commodities** are EXEMPT from ALL of these HOS rules:

- 11-hour driving limit
- 14-hour on-duty window
- 30-minute break requirement
- 60/70 hour cumulative limit
- ELD requirement (since they're exempt from RODS)

ONLY when they are operating within a **150-air-mile radius** of the source of the commodity.

## Who qualifies

A driver may use the exemption when ALL of:

1. Operating during a state-declared **planting or harvest season**
2. Transporting an **agricultural commodity** (defined below)
3. Operating within a **150-air-mile radius** of the source of the commodity
4. For livestock specifically: 150-air-mile radius can extend to **150 air miles from the destination too**

## Definitions (49 CFR 395.2)

**Agricultural commodity** includes:

- **Crops** — grain, fruits, vegetables, hay, straw
- **Livestock** — cattle, swine, sheep, horses, poultry
- **Bees** — for pollination or honey production
- **Aquatic animals** — fish, shellfish for aquaculture
- **Forest products** — but NOT lumber (raw logs OK; finished lumber NOT exempt)
- **Insects** — for pollination or pest control
- **Other ag products** — when defined by state agriculture commissioner

**NOT covered:**
- Processed foods (e.g., cooked grain → cereal box)
- Fertilizer or feed (going TO the farm — this is a separate exemption under 395.1(k)(2))
- Lumber, milled wood
- Pre-loaded packaged consumer goods

## What "state-declared season" means

Each state's agriculture commissioner (or equivalent) declares the start and end of:

- **Planting season** (often March-June, varies by crop + state)
- **Harvest season** (often July-November, varies)

State declarations are typically published on the state Department of Agriculture website. Operating outside the declared window = no exemption applies.

If a state doesn't issue a formal declaration, the exemption defaults to a year-round window for hauling agricultural commodities within that state's borders (50 states have at least basic ag operation exemptions).

## The 150-air-mile radius

**Air-mile** (NOT road mile) is the straight-line distance from point A to point B. A truck that drives 200 road miles but only 130 air miles is still within the 150-air-mile radius.

The radius is measured:

- **For non-livestock:** From the SOURCE of the commodity (farm, grain elevator, packing facility)
- **For livestock (cattle, swine, sheep, horses, poultry):** From the source OR the destination (whichever you're returning from, more permissive)

Once a driver leaves the 150-air-mile radius, the full HOS rules apply for that entire trip and the driver must have valid logs / be using an ELD.

## How to document

If you use the exemption, document:

- The commodity type
- State-declared season dates (screenshot of state declaration)
- Source location (with GPS coordinates if possible)
- Each trip's start point + end point + air-mile distance
- A "Notice of Agricultural Exemption" letter to the driver explaining when it applies (best practice; not federally required)

Auditors at roadside or compliance review will ask for this documentation.

## Common mistakes

1. **Operating the exemption year-round** when state's declared season is, e.g., March-October. Off-season hauls require full HOS compliance.
2. **Operating beyond 150 air miles** and claiming the exemption. The exemption is radius-limited; one mile beyond = no exemption.
3. **Hauling processed/finished products** (e.g., flour, packaged grain, dairy cartons) and claiming ag exemption. Those are NOT agricultural commodities — they're consumer goods.
4. **Mixed loads** — if a truck hauls a mix of ag commodities + non-ag commodities, the exemption may not apply. Treat the entire load as non-ag if any non-ag is included.
5. **Not documenting season declarations.** If a roadside inspector asks, you need the state declaration on hand.

## Livestock-specific provisions

Livestock hauling gets additional flexibility:

- 150-air-mile radius from EITHER source OR destination
- Some states have "livestock-specific" extensions during certain conditions (drought relief, wildfire evacuation)
- During a federally-declared emergency (e.g., disease outbreak requiring quarantine), USDA may grant temporary exemptions

## Fuel + feed exemption (49 CFR 395.1(k)(2))

A separate exemption: drivers hauling **fuel or feed TO the farm** during planting/harvest may be exempt from 11/14-hour HOS rules within 150 air miles. This applies to suppliers, not farmers' own trucks.

## CMV operations beyond agriculture

If your fleet does:

- Ag commodity hauling (in season, within radius) → exempt
- Non-ag freight (off season OR outside radius OR non-ag commodity) → full HOS

You can mix operations but each individual trip is evaluated independently.

## ELD specifics

Drivers using the ag exemption don't need to use an ELD for ag-exempt trips. They DO need ELD for any non-ag trips. Most carriers configure their ELD to support "exempt" annotations so drivers can log the exemption while still using the device.

## State quirks

Some states have nuances:
- **California** — additional ag-specific provisions for "California Driver Exemption" applies to in-state hauls of small-volume ag goods
- **Texas** — broad ag interpretation; lots of intrastate exemption
- **Florida** — citrus + sugar season-specific
- **Iowa** — long planting/harvest windows due to corn + soybean dominance

Check your state department of agriculture for specifics.

## Where this fits in X3

If a carrier indicates "agricultural" in their operation profile, X3's `hos-eld.html` adds an "Ag Exemption" duty status option. The agent-driver-reminders agent skips HOS-related reminders during state-declared seasons for ag-only drivers. Mike Perry has a written ag-exemption FAQ available on request.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=agricultural-exemption

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
