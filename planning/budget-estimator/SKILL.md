---
name: budget-estimator
description: "Generates a structured production budget estimate for a specific project element or an entire short-form production, broken down by standard industry cost categories."
status: stable
category: pre-production
subcategory:
version: 1.0
eval_score: 4.2
tags: [budget, pre-production, planning, finance, production]
---
# Budget estimator

## What this skill does
Generates a structured production budget estimate for a specific project element or an entire short-form production, broken down by standard industry cost categories.

## When to use this skill
- You are preparing a budget for a pitch deck or funding application and need realistic line items
- A commissioner or funder has asked for a cost breakdown and you need a starting framework
- You want to sanity-check your own budget against industry norms before submitting
- You are comparing production approaches (studio vs. location, in-house vs. freelance) and need cost estimates for each

## What you need to provide
**Required:**
- Project type (documentary, short film, podcast series, corporate video, etc.)
- Duration or scope (e.g., "6 × 30-minute episodes" or "one 90-second brand video")
- Key production elements (number of shoot days, locations, crew size, talent, post-production needs)
- Territory or market (costs vary dramatically between countries and cities)

**Optional:**
- Known fixed costs (e.g., "archive licensing budget is capped at €5,000")
- Format constraints (e.g., "4K delivery required" or "must include subtitles in three languages")
- Whether this is for internal planning or external submission (affects level of detail)

## How the Assistant Approaches This
1. Identifies the production type and maps it to standard budget categories (development, pre-production, production, post-production, delivery, overheads, contingency)
2. Estimates realistic cost ranges for each line item based on the territory, scale, and format specified
3. Flags assumptions made (day rates, equipment costs, post-production timelines) so you can adjust with real quotes
4. Adds a contingency line (typically 10% for controlled productions, 15–20% for location-heavy or international work)
5. Notes which line items are most likely to be challenged by funders or commissioners

## Output format
A structured budget table with:
- Category headings (development, pre-production, production, post-production, delivery, overheads, contingency)
- Line items with unit cost, quantity, and subtotal
- Notes column explaining assumptions
- Summary totals per category and grand total
- A short "budget notes" section flagging the three biggest cost risks

Currency matches the territory specified. Estimates given as ranges where exact costs depend on quotes.

## Quality criteria
- [ ] Every line item has a unit cost, quantity, and subtotal — no lump sums without explanation
- [ ] Assumptions are stated explicitly (e.g., "camera operator day rate estimated at €450/day based on Western European freelance market")
- [ ] Contingency is included and justified
- [ ] The budget is structured so a funder or commissioner can read it without explanation
- [ ] Cost ranges are realistic for the specified territory and market

## Example

### Input
Project: 3-part documentary series (3 × 45 minutes) about urban farming initiatives across three European cities. Production includes interviews, observational shooting, some aerial drone footage, and archival material. Budget territory: Germany/Western Europe. This is for a public broadcaster funding application.

### Output

**Budget estimate — Urban farming documentary series (3 × 45 min)**

| Category | Line item | Unit cost | Qty | Subtotal | Notes |
|----------|-----------|-----------|-----|----------|-------|
| **Development** | | | | **€18,500** | |
| | Research & development | €3,000 | 1 | €3,000 | Desktop research, contributor identification |
| | Location scouting (3 cities) | €2,500 | 3 | €7,500 | Travel + 2 days per city |
| | Development producer | €4,000 | 1 | €4,000 | 10 days @ €400/day |
| | Rights research | €2,000 | 1 | €2,000 | Archive pre-clearance |
| | Legal (option agreements) | €2,000 | 1 | €2,000 | Contributor agreements |
| **Pre-production** | | | | **€14,000** | |
| | Producer (prep) | €400/day | 15 | €6,000 | Schedule, logistics, permits |
| | Director (prep) | €450/day | 10 | €4,500 | Treatment refinement, shot planning |
| | Travel & accommodation (recce) | €1,500 | 2 | €3,000 | 2 recce trips |
| | Insurance | €500 | 1 | €500 | Production insurance |
| **Production** | | | | **€89,400** | |
| | Director | €450/day | 30 | €13,500 | 10 shoot days × 3 episodes |
| | Camera operator | €450/day | 30 | €13,500 | |
| | Sound recordist | €350/day | 30 | €10,500 | |
| | Producer (shoot) | €400/day | 36 | €14,400 | Including travel days |
| | Drone operator + equipment | €1,200/day | 6 | €7,200 | 2 days per city |
| | Camera kit rental | €300/day | 30 | €9,000 | 4K documentary kit |
| | Sound kit rental | €100/day | 30 | €3,000 | |
| | Travel (crew, 3 cities) | €3,000 | 3 | €9,000 | Flights + ground transport |
| | Accommodation | €120/night | 75 | €9,000 | 3 crew × 25 nights |
| | Per diems | €30/day | 120 | €3,600 | 4 crew × 30 days |
| | Miscellaneous production | €700 | 1 | €700 | Parking, consumables, contingency items |
| **Post-production** | | | | **€52,500** | |
| | Editor | €400/day | 60 | €24,000 | 20 days per episode |
| | Edit suite rental | €150/day | 60 | €9,000 | Or license fee if in-house |
| | Director (post) | €450/day | 15 | €6,750 | 5 days per episode |
| | Composer / music licensing | €3,000 | 3 | €9,000 | Per episode |
| | Sound mix | €1,500 | 3 | €4,500 | Per episode |
| | Grade / online | €2,500 | 3 | €7,500 | Per episode |
| | Archive licensing | €5,000 | 1 | €5,000 | Estimated; depends on sources |
| | Graphics / titles | €2,000 | 1 | €2,000 | Series package |
| **Delivery** | | | | **€7,500** | |
| | Subtitling (3 languages) | €1,500 | 3 | €4,500 | DE, EN, FR |
| | Delivery masters | €1,000 | 3 | €3,000 | Broadcaster specs |
| **Overheads** | | | | **€9,100** | |
| | Production office | €500/month | 8 | €4,000 | 8-month production period |
| | Communication / admin | €300/month | 8 | €2,400 | |
| | Accounting | €2,700 | 1 | €2,700 | Production accounting |
| **Contingency** | | | | **€19,100** | |
| | 10% of total | | | €19,100 | Standard for controlled European doc production |

**Grand total: €210,100**

**Budget notes:**
1. **Archive licensing is the wildcard.** €5,000 is a placeholder. If the series uses significant broadcast archive, this could triple. Get clearance quotes early.
2. **Drone costs assume local operators in each city.** Flying your own drone internationally adds permit complexity and may require local co-pilots. Budget could rise by €2,000–4,000 if permits are difficult.
3. **Music licensing vs. original score.** The €9,000/episode estimate covers a modest original score. Library music would reduce this to €1,500–2,500/episode but limits exclusivity.

## Known limitations
- All costs are estimates based on typical Western European rates. Actual costs depend on specific quotes, crew availability, and market conditions at time of production.
- Does not account for co-production financing structures, tax incentives, or regional fund requirements that may affect budget presentation.
- Cannot predict archive licensing costs without knowing specific sources. Always get quotes before committing a figure to a funder.
- Day rates vary significantly even within the same market. These estimates assume mid-range freelancers, not top-tier specialists.

## Related skills
- [pitch-treatment-writer](../../tv-documentary/development/pitch-treatment-writer/SKILL.md)
- [grant-proposal-writer](../../tv-documentary/business/grant-proposal-writer/SKILL.md)
- [grant-narrative-writer](../../media-business/funding/grant-narrative-writer/SKILL.md)
