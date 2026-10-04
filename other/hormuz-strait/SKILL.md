---
name: hormuz-strait
description: >
  Check the live status of the Strait of Hormuz from the Hormuz Strait Monitor
  dashboard: open, restricted, or closed status, tanker transits vs normal, stranded
  vessels, Brent price impact, war-risk insurance levels, cargo throughput, tanker
  freight rates, diplomatic developments, and global trade impact. Use this skill
  whenever the user asks about the Strait of Hormuz or the Persian Gulf in the context
  of oil, shipping, or geopolitical risk — whether Hormuz is open, chokepoint or
  transit disruption, Gulf tanker traffic, war-risk premiums, Middle East shipping
  routes, or energy supply-chain risk.
---

# Hormuz Strait Monitor Skill

Fetches real-time status of the Strait of Hormuz from the [Hormuz Strait Monitor](https://hormuzstraitmonitor.com) dashboard API. Covers shipping transits, oil prices, stranded vessels, insurance risk, diplomatic status, global trade impact, and crisis timeline.

**This skill is read-only.** It fetches public dashboard data — no authentication required.

---

## Step 1: Fetch Dashboard Data

Use `curl` to fetch the dashboard API:

```bash
curl -s https://hormuzstraitmonitor.com/api/dashboard
```

Parse the JSON response. The API returns `{ "success": true, "data": { ... }, "timestamp": "..." }`.

If `success` is `false` or the request fails, inform the user the monitor is temporarily unavailable and suggest checking https://hormuzstraitmonitor.com directly.

---

## Step 2: Identify What the User Needs

Match the user's request to the relevant data sections. If the user asks for a general status update, present all sections. If they ask about something specific, focus on the relevant section(s).

| User Request | Data Section | Key Fields |
|---|---|---|
| General status / "is Hormuz open?" | `straitStatus` | `status`, `since`, `description` |
| Ship traffic / transit count | `shipCount` | `currentTransits`, `last24h`, `normalDaily`, `percentOfNormal` |
| Oil price impact | `oilPrice` | `brentPrice`, `change24h`, `changePercent24h`, `sparkline` |
| Stranded / stuck vessels | `strandedVessels` | `total`, `tankers`, `bulk`, `other`, `changeToday` |
| Insurance / war risk | `insurance` | `level`, `warRiskPercent`, `normalPercent`, `multiplier` |
| Cargo throughput | `throughput` | `todayDWT`, `averageDWT`, `percentOfNormal`, `last7Days` |
| Diplomatic situation | `diplomacy` | `status`, `headline`, `parties`, `summary` |
| Global trade impact | `globalTradeImpact` | `percentOfWorldOilAtRisk`, `estimatedDailyCostBillions`, `affectedRegions`, `lngImpact`, `alternativeRoutes`, `supplyChainImpact` |
| Crisis timeline / events | `crisisTimeline` | `events[]` with `date`, `type`, `title`, `description` |
| Tanker freight rates / VLCC rates | `tankerRates` | `currentRate`, `preCrisisRate`, `changePercent`, `route`, `vesselType`, `trend`, `unit` |
| Latest news | `news` | `title`, `source`, `url`, `publishedAt`, `description` |

---

## Step 3: Present the Data

Format the results clearly for financial research. Adapt the presentation based on what the user asked for.

### General status briefing (default)

When the user asks for a general update, cover these sections — a line each while shipping is operating normally, more depth wherever there is active disruption:

1. **Strait Status** — lead with the current status (e.g., "OPEN", "RESTRICTED", "CLOSED"), how long it's been in that state, and the description
2. **Ship Traffic** — current transits, last 24h count, and percent of normal
3. **Oil Price** — Brent price with 24h change
4. **Stranded Vessels** — total count broken down by type, with today's change
5. **Insurance Risk** — risk level, war risk premium percentage, and multiplier vs. normal
6. **Cargo Throughput** — today's DWT vs. average, percent of normal
7. **Diplomatic Status** — current status, headline, and brief summary
8. **Global Trade Impact** — percent of world oil at risk, estimated daily cost, and top affected regions
9. **Tanker Freight Rates** — current VLCC rate on the benchmark route vs. pre-crisis baseline, with trend direction

### Formatting guidelines

- Use tables for structured data (vessel counts, affected regions, alternative routes)
- Highlight abnormal values — if `percentOfNormal` is below 80% or above 120%, call it out
- For `oilPrice.sparkline`, describe the trend (rising, falling, stable) rather than listing raw numbers
- For `throughput.last7Days`, describe the trend direction
- Show `lastUpdated` timestamp so the user knows data freshness
- For news items, include the source and link
- For crisis timeline events, present chronologically with event type labels

### Risk assessment

Based on the data, provide a brief risk assessment. `insurance.level` values come back uppercase:

| Insurance Level | Interpretation |
|---|---|
| `NORMAL` | No elevated risk — shipping operating normally |
| `ELEVATED` | Some disruption concerns — monitor closely |
| `HIGH` | Significant risk — active disruption or credible threat |
| `CRITICAL` | Severe disruption — major impact on global oil supply |
| `EXTREME` | Effective closure — war risk premiums at multi-decade highs, most commercial traffic halted |

If the strait status is anything other than fully open, highlight:
- The estimated daily cost to global trade
- Which regions are most affected and their oil dependency
- Available alternative routes with additional transit days and cost
- LNG impact if applicable
- SPR (Strategic Petroleum Reserve) status in days

---

## Step 4: Respond to the User

- Lead with the most important information: strait status and any active disruption
- Include data freshness (`lastUpdated` timestamp)
- If the situation is elevated or worse, proactively include the global trade impact summary
- Keep the response concise for routine "all clear" statuses; expand for active incidents
- Add a disclaimer: data is sourced from Hormuz Strait Monitor and may have delays

---

## Reference Files

- `references/api_schema.md` — Complete API response schema with field descriptions and data types

Read the reference file when you need exact field names or data type details.
