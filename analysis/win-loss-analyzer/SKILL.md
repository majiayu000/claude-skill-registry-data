---
name: win-loss-analyzer
description: Analyze closed deals and lost opportunities for patterns
tags: [analysis, deals, win-loss, strategy]
---

# Win-Loss Analyzer

Analyzes closed-won and closed-lost deals to identify patterns in what drives wins and what causes losses. Produces actionable insights for ICP refinement, messaging adjustments, and process improvements. The output feeds into `icp-builder` for segment validation and `message-generator` for objection handling.

## Prerequisites

- `agency.config.json` in the project root
- Deal data from CRM or user input (minimum 5 deals, ideally 10+)
- Optional: CRM tab access for automated data pull

## Phase 0: Read Config and CRM

1. Read `agency.config.json` from the project root.
2. Extract `icp.segments[]` for segment classification.
3. Extract `services[].name` to categorize deals by service.
4. Extract `crm` config for CRM data access.
5. If CRM is configured, attempt to read closed deals from the pipeline tab:
   - Filter for Status = "WON" or "LOST" or "CLOSED" or "DEAD"
   - Pull all available fields
6. If CRM data is insufficient or unavailable, proceed to manual input in Phase 1.

## Phase 1: Gather Deal Data

For each deal (won or lost), collect:

**Won deals:**
```
DEAL: [Company Name] -- WON
Industry: [industry]
Company Size: [employees]
Decision Maker: [name, title]
Deal Value: [monthly retainer or project value]
Service Sold: [which service(s)]
Source Channel: [how they found us / how we found them]
First Contact Date: [date]
Close Date: [date]
Time to Close: [calculated days]
Key Factors: [why they chose us -- in their words if possible]
Champion: [internal advocate if any]
Competitor Considered: [other agencies they evaluated]
```

**Lost deals:**
```
DEAL: [Company Name] -- LOST
Industry: [industry]
Company Size: [employees]
Decision Maker: [name, title]
Estimated Deal Value: [what the deal would have been]
Service Discussed: [which service(s)]
Source Channel: [how they found us / how we found them]
First Contact Date: [date]
Lost Date: [date]
Stage Lost At: [awareness / demo / proposal / negotiation / verbal yes then ghosted]
Reason for Loss: [price / timing / competitor / internal decision / went dark / not a fit]
Competitor Chosen: [who they went with, if known]
Objections Raised: [what they pushed back on]
Last Communication: [what happened at the end]
```

Ask the user to provide as many deals as possible. Minimum 5 total (mix of won and lost). If they have fewer, note that insights will be directional, not statistically significant.

## Phase 2: Win Analysis

Analyze all won deals for patterns:

**Segment distribution:**
- Count deals per industry, company size range, decision maker title
- Identify the "sweet spot" segment (highest frequency + highest value)

**Channel effectiveness:**
- Win count by acquisition channel (inbound, outbound, referral, platform)
- Average deal value by channel
- Average time to close by channel
- Best channel = highest (win count * avg deal value) / avg time to close

**Service demand:**
- Which services are sold most often?
- Which services command the highest deal value?
- Which services have the fastest close cycle?

**Decision patterns:**
- Average time to close across all won deals
- Fastest close: what made it fast?
- Longest close: what caused the delay?
- Common champion titles (the internal person who pushed the deal)

**Buying trigger analysis:**
- What event preceded first contact? (funding, hiring, competitor move, seasonal, growth milestone)
- Cluster triggers by frequency

**Competitive wins:**
- Which competitors did we beat?
- What was our advantage? (price, expertise, speed, case studies, relationship)

Present findings:
```
WIN ANALYSIS
===
Total won deals: [N]
Total revenue: [sum]
Average deal value: [mean]
Average time to close: [days]

SWEET SPOT SEGMENT:
Industry: [most common]
Company size: [most common range]
Decision maker: [most common title]
Deal value: [average for this segment]

BEST CHANNEL: [channel] -- [N] wins, avg [value], avg [days] to close
MOST SOLD SERVICE: [service] -- [N] deals
FASTEST CLOSE: [days] -- [what made it fast]

TOP BUYING TRIGGERS:
1. [trigger] -- [N] occurrences
2. [trigger] -- [N] occurrences
3. [trigger] -- [N] occurrences

COMPETITIVE EDGE:
- Beat [competitor] [N] times because [reason]
```

## Phase 3: Loss Analysis

Analyze all lost deals for patterns:

**Loss reason distribution:**
```
LOSS REASONS:
1. Price -- [N] deals ([X]%)
2. Timing -- [N] deals ([X]%)
3. Competitor -- [N] deals ([X]%)
4. Internal decision (decided to do in-house) -- [N] deals ([X]%)
5. Went dark (ghosted) -- [N] deals ([X]%)
6. Not a fit -- [N] deals ([X]%)
```

**Stage analysis:**
- At which stage do most deals die?
- Early losses (awareness/demo) = messaging or qualification problem
- Late losses (proposal/negotiation) = pricing, proof, or process problem
- Post-verbal-yes losses = trust or urgency problem

**Competitor losses:**
- Which competitors took deals from us?
- What was their advantage? (price, reputation, feature, location)
- Pattern: are we losing to the same competitor repeatedly?

**Objection inventory:**
- List every objection raised across lost deals
- Rank by frequency
- Note which objections were overcome (in won deals) vs fatal (in lost deals)

**Ghost analysis:**
- How many deals went dark?
- At what stage?
- After how many days of silence?
- Was there a follow-up cadence?

Present findings:
```
LOSS ANALYSIS
===
Total lost deals: [N]
Estimated lost revenue: [sum of estimated values]

PRIMARY LOSS REASON: [reason] -- [N] deals
DEADLIEST STAGE: [stage] -- [X]% of losses happen here
TOP COMPETITOR: [name] -- took [N] deals

UNRESOLVED OBJECTIONS:
1. "[objection]" -- raised [N] times, never overcome
2. "[objection]" -- raised [N] times, overcome in [M] cases
3. "[objection]" -- raised [N] times

GHOST RATE: [X]% of lost deals went dark
Average ghost point: [stage], after [N] days of engagement
```

## Phase 4: Insights

Cross-reference win and loss data to produce actionable insights:

**Win rate by segment:**
```
SEGMENT WIN RATES:
[Segment 1]: [X]% win rate ([won]/[total]) -- avg deal [value]
[Segment 2]: [X]% win rate ([won]/[total]) -- avg deal [value]
[Segment 3]: [X]% win rate ([won]/[total]) -- avg deal [value]
```

**Fastest path to close:**
- The combination of segment + channel + service that closes fastest
- Example: "D2C skincare brands from LinkedIn outreach buying CRO audits close in 12 days on average"

**Risk factors:**
- Deals with [characteristic] have [X]% higher loss rate
- When [objection] is raised and not addressed by [stage], the deal is lost [X]% of the time
- Deals that go silent for > [N] days after [stage] have a [X]% ghost rate

**Revenue concentration risk:**
- What percentage of revenue comes from the top segment?
- Is the pipeline too dependent on one channel or service?

**Recommendations:**

```
RECOMMENDED ACTIONS
===

ICP ADJUSTMENTS:
- Increase priority: [segment] (highest win rate + deal value)
- Decrease priority: [segment] (low win rate, high loss to competitors)
- New segment to test: [based on patterns in won deals that don't fit existing segments]

MESSAGING ADJUSTMENTS:
- Add objection handler for: "[objection]" (raised [N] times, not in current messaging)
- Lead with: [value prop that correlates with wins]
- Stop leading with: [value prop that doesn't correlate]

PROCESS CHANGES:
- Add [touchpoint] at [stage] -- losses spike here
- Follow-up cadence: if silent for [N] days at [stage], trigger [action]
- Qualification criteria: disqualify if [characteristic] (high loss predictor)
- Competitive playbook: when [competitor] is involved, [strategy]

PRICING ADJUSTMENTS:
- [segment] is price-sensitive -- consider [tier/packaging change]
- [segment] pays premium -- raise prices or add premium tier
```

## Phase 5: Output

Return the complete win-loss analysis:

1. **Win analysis report** -- from Phase 2
2. **Loss analysis report** -- from Phase 3
3. **Cross-analysis insights** -- from Phase 4
4. **Actionable recommendations** -- categorized by ICP, messaging, process, pricing
5. **Data quality assessment**:
   ```
   DATA QUALITY:
   Total deals analyzed: [N]
   Won: [N], Lost: [N]
   Confidence level: [high (20+ deals) / medium (10-20) / directional (5-10) / insufficient (<5)]
   Missing data: [fields that were incomplete across deals]
   ```
6. **Recommended next steps**:
   - Update `icp-builder` with segment win rates
   - Update `message-generator` with objection handlers
   - Set up lost deal post-mortem template for future deals
   - Re-run `win-loss-analyzer` quarterly with new data

## Example Usage

Trigger phrases:
- "Analyze our wins and losses"
- "Why are we losing deals?"
- "What's our win rate by segment?"
- "Do a win-loss analysis"
- "Which deals are we winning and why?"

```
User: Why do we keep losing deals at the proposal stage?
Assistant: [gathers deal data, analyzes loss patterns by stage, identifies proposal-stage issues, recommends process and messaging changes]
```

```
User: Analyze our last 10 deals
Assistant: [collects data on all 10, splits into won/lost, runs full analysis, produces report with insights]
```
