---
name: travel-research
description: Research and compare destinations with deeper scoring across budget, climate, logistics, activity fit, and seasonal tradeoffs before moving into full trip planning.
version: 1.2.0
---

# Travel Research Skill

## Intent

Use this skill when the user is not ready for a full itinerary yet and needs stronger destination research first. The goal is to compare places honestly, surface tradeoffs early, and identify the best fit before handing off into `travel-planning` or `travel-itinerary`.

## Use When

- The user wants to compare destinations, regions, or trip styles
- A trip idea is still in the research phase and the right destination is not settled
- The user needs deeper analysis of climate, seasonality, training value, crowds, budget, or travel friction
- The best next step is to narrow choices before building a day by day plan

## Do Not Use When

- The destination is already chosen and the user needs a full itinerary
- The request is mainly about booking specific flights, hotels, or transport
- The user wants a finished travel budget and execution plan more than research
- The question is a quick one off logistics check that does not need structured comparison

## Research Priorities

Always judge options against Mick's actual travel preferences:

- solo travel by default
- private rooms only
- BNA as the home airport unless otherwise stated
- value optimized, not backpacker cheap and not luxury
- preference for active trips, endurance anchors, and good photo worthy experiences

Focus on what materially separates one option from another:

- total trip cost and daily spend
- weather and season fit
- live or current flight pricing, weather normals, and crowd levels when available
- event or activity alignment
- transit complexity
- travel friction score across visa effort, flight routing, and in-country transport difficulty
- crowd pressure
- safety and scam friction
- visa or border hassle
- how well the destination fits the stated trip goal

## Workflow

1. Identify the trip goal first.
2. Determine the comparison set:
   - user supplied destinations
   - a region shortlist
   - best fit suggestions if the user only gives goals and constraints
3. Build a direct scorecard for each option.
4. Pull live or current data when the request depends on timing-sensitive facts:
   - flight pricing from available public search results or user-provided fare data
   - weather normals from reliable climate or weather sources
   - crowd levels from seasonality, event calendars, booking pressure, or current travel sources
5. If live data is unavailable, label estimates clearly and explain what source or assumption was used.
6. Calculate a travel friction score for each destination from:
   - visa or entry effort
   - flight routing difficulty from BNA unless another origin is stated
   - in-country transport difficulty
7. Explain the tradeoffs in plain language, not tourism fluff.
8. Call out strong and weak fit areas:
   - budget fit
   - climate fit
   - activity fit
   - logistics fit
   - travel friction fit
   - pace fit
   - value for the stated season
9. Recommend the best option and at least one fallback.
10. State the next practical move:
   - deeper research
   - move into `travel-planning`
   - move into `travel-itinerary`

## Scoring Weight Presets

Different trip types should not weight the scorecard the same way. Apply the preset that matches the trip goal and say which one was used:

| Dimension | Endurance training | Sightseeing | Remote work | Budget recharge |
|---|---:|---:|---:|---:|
| Activity fit | 35% | 15% | 10% | 10% |
| Climate | 25% | 15% | 10% | 20% |
| Budget | 15% | 20% | 20% | 35% |
| Logistics / friction | 15% | 25% | 25% | 20% |
| Value for season | 10% | 25% | 35% | 15% |

For mixed-goal trips, blend the two closest presets and note the blend. The weighted score feeds the Overall column; never let a destination win on vibe while losing on every weighted dimension.

## Comparison History

Treat prior research as reusable instead of rebuilding it:

- when the user references an earlier comparison, ask for or reuse that output as the baseline and only refresh the timing-sensitive columns: flights, crowds, seasonal value
- when producing a substantial comparison, note at the end that the scorecard can be saved to Obsidian or notes for reuse, and offer a compact save format on request
- if a saved comparison is more than a season old, refresh live data before standing behind its recommendation

## Shortlist Handoff

When research concludes, end with a handoff block that `travel-planning` or `travel-itinerary` can consume directly without re-deriving anything:

```text
SHORTLIST HANDOFF
Pick: [destination] | Window: [dates or month] | Style: [trip style preset]
Why it won: [one line]
Locked assumptions: [origin airport, budget band, solo, private rooms]
Carry-forward facts: [flight range found, daily spend estimate, friction score, must-book items]
Next skill: travel-planning [or travel-itinerary if dates and route are already firm]
```

## Comparison Framework

For each destination, check:

- best travel window for the stated goal
- worst travel window and why
- current flight price range or clearly labeled estimate
- weather normals for the target month or season
- crowd level for the target month or season
- likely flight friction from BNA
- local transport simplicity
- visa or entry effort
- travel friction score
- private room lodging value
- food cost and quality
- training or adventure opportunities
- scenic or content capture value
- overtourism pressure
- common traveler mistakes

When relevant, also compare:

- event calendars
- altitude or terrain
- rental car need
- ferry or rail usefulness
- remote work practicality
- carry only practicality

## Output Format

Use this structure for substantial comparison requests:

```text
TRIP GOAL:
[What the user is trying to optimize for]

OPTIONS:
- [Destination A]
- [Destination B]

SCORECARD:
| Destination | Budget | Climate | Activity | Logistics | Value | Overall |
|---|---:|---:|---:|---:|---:|---:|

LIVE DATA SNAPSHOT:
| Destination | Flight Pricing | Weather Normals | Crowd Level | Source / Confidence |
|---|---|---|---|---|
| [Destination A] | [Current range or estimate] | [Temp / rain / season note] | [Low / Medium / High] | [Source or assumption] |
| [Destination B] | [Current range or estimate] | [Temp / rain / season note] | [Low / Medium / High] | [Source or assumption] |

TRAVEL FRICTION:
| Destination | Visa / Entry | Flight Routing | In-Country Transport | Friction Score | Notes |
|---|---:|---:|---:|---:|---|
| [Destination A] | [1-5] | [1-5] | [1-5] | [Avg or weighted score] | [Main friction point] |
| [Destination B] | [1-5] | [1-5] | [1-5] | [Avg or weighted score] | [Main friction point] |

DESTINATION NOTES:
[Destination A]
- Best for:
- Watch for:
- Best season:
- Poor season:
- Estimated daily spend:
- Live data confidence:
- Travel friction:

[Destination B]
- Best for:
- Watch for:
- Best season:
- Poor season:
- Estimated daily spend:

RECOMMENDATION:
[Best choice and why]

RUNNER UP:
[Fallback and why]

NEXT STEP:
[Move into travel-planning or request deeper research on one option]
```

## Constraints

- Do not give generic top ten destination lists
- Make comparisons explicit and decision oriented
- Prefer practical travel friction over postcard descriptions
- Use current sources for flight pricing, weather normals, and crowd levels when the user asks for a live decision or a dated trip window
- Clearly label live data, estimates, assumptions, and stale or unavailable data
- Score travel friction separately from overall appeal so a beautiful destination with hard routing does not look easier than it is
- If the user gives weak input, propose a short relevant comparison set instead of pretending certainty
- Hand off to `travel-planning` once a destination is chosen

## References

- `shared/skill-standard.md`
- `claude/skills/travel-planning/SKILL.md`
- `claude/skills/travel-itinerary/SKILL.md`

## Help And Examples

Use this skill when the user needs to decide where to go before planning the trip in detail.

Minimum useful input:

- a destination shortlist or a trip goal
- rough date window
- budget or style constraints if known

Example prompts:

```text
Use travel-research to compare Madeira, Girona, and Mallorca for a spring cycling trip from BNA.
```

```text
Research the best October solo trip options for hiking, good weather, and strong USD value.
```

```text
Compare Japan and Portugal for a two week active trip with good food, easy logistics, and private room lodging.
```

## Validation Checklist

- The comparison focuses on real tradeoffs instead of generic destination blurbs
- The output reflects Mick's travel constraints and preferences
- The recommendation is clear and justified
- Live data is included or missing live data is clearly labeled
- Travel friction includes visa effort, flight routing, and in-country transport difficulty
- The next step points to planning or itinerary work, not more vague brainstorming
