---
name: lead-scorer
description: Score raw leads as HOT/WARM/COOL based on config-driven weights from agency.config.json
tags: [scoring, lead-qualification, prioritization]
---

# Lead Scorer

Scores inbound or scraped leads using a multi-factor algorithm. All weights, thresholds, and bonuses are read from `agency.config.json` so the scoring adapts to any agency without code changes.

## Prerequisites

- `agency.config.json` exists at the repo root with a `scoring` section containing: `platform_weights`, `hiring_signals`, `budget_tiers`, `recency_bonuses`, `market_boosts`, `thresholds`
- `icp` section with `primary_keywords`, `secondary_keywords`, `intent_keywords`, `negative_keywords`
- Lead data in structured format (JSON object or array)

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract:
   - `scoring.platform_weights` -- map of platform name to base score
   - `scoring.hiring_signals` -- array of phrases that indicate active hiring/buying
   - `scoring.budget_tiers` -- array of `{min, points}` sorted descending by `min`
   - `scoring.recency_bonuses` -- map of time window to bonus points (e.g., `"24h": 15`)
   - `scoring.market_boosts` -- map of market/country to bonus points
   - `scoring.contact_surface_bonus` -- bonus points for multi-channel reachability
   - `scoring.thresholds` -- `{hot, warm}` cutoffs
   - `icp.primary_keywords` -- high-relevance service keywords (+10 each match)
   - `icp.secondary_keywords` -- medium-relevance keywords (+5 each match)
   - `icp.intent_keywords` -- buying-intent phrases (+10 each match)
   - `icp.negative_keywords` -- disqualifiers (score = 0, immediately reject)
   - `outreach.daily_targets` -- { company_leads: 5, gig_leads: 20, total: 25 }
   - `outreach.geo_split` -- { international_pct: 75, india_pct: 25 }
3. Accept the lead(s) to score. Each lead should have as many of these fields as available:
   - `title` -- the post/gig/job title or subject line
   - `description` -- the full text body
   - `platform` -- where the lead was found
   - `budget` -- numeric budget amount (if available)
   - `currency` -- budget currency
   - `posted_at` -- ISO timestamp or relative time string
   - `country` -- country of the lead or company
   - `url` -- source URL
   - `lead_type` -- "gig" or "company" (from signal-scanner classification)
   - `geo_bucket` -- "international" or "india" (from signal-scanner)

## Phase 1: Negative Keyword Check

For each lead, scan `title` and `description` against every entry in `icp.negative_keywords` (case-insensitive substring match).

- If ANY negative keyword matches: **score = 0**, tier = `REJECTED`, skip all remaining phases for this lead.

## Phase 1.5: Lead Type Awareness

Apply different scoring standards based on `lead_type`:

### Company Leads (target: 5/day)
- Apply FULL scoring algorithm (all phases below)
- Extremely high quality bar: only HOT leads pass
- Company leads must score >= thresholds.hot to be included

### Gig Leads (target: 20/day)
- Apply simplified scoring: platform base + keyword match + budget + recency
- Skip hiring signal bonus (gigs ARE the hiring signal)
- Higher volume: HOT threshold is sufficient
- Must have clear buying signal and budget to qualify

## Phase 2: Platform Base Score

Look up `lead.platform` in `scoring.platform_weights`.

- If the platform exists in the map: `base_score = platform_weights[platform]`
- If the platform is not in the map: `base_score = 10` (default floor)

## Phase 3: Keyword Match Scoring

Combine `title` + `description` into a single lowercase text blob. For each keyword list, count distinct keyword matches (not occurrences):

- **Primary keywords**: For each match, add +10 points. Cap at 3 matches (max +30).
- **Secondary keywords**: For each match, add +5 points. Cap at 3 matches (max +15).
- **Intent keywords**: For each match, add +10 points. Cap at 2 matches (max +20).

`keyword_score = primary_points + secondary_points + intent_points`

## Phase 4: Hiring Signal Bonus

Scan the text blob against `scoring.hiring_signals` (case-insensitive).

- If ANY hiring signal matches: add +20 points (one-time bonus, not per-match).
- **Note**: For gig leads (`lead_type == "gig"`), skip this phase. Gigs ARE the hiring signal, so the bonus is already baked into the platform base score.

## Phase 5: Budget Tier Scoring

If `lead.budget` is a number > 0:

- Iterate `scoring.budget_tiers` from highest `min` to lowest.
- The first tier where `lead.budget >= tier.min` gives `budget_points = tier.points`.
- If no budget data: `budget_points = 0`.

## Phase 6: Recency Bonus

Calculate the age of the lead from `lead.posted_at` relative to now.

- If age <= 24 hours: add `scoring.recency_bonuses["24h"]` points
- Else if age <= 48 hours: add `scoring.recency_bonuses["48h"]` points
- Else if age <= 72 hours: add `scoring.recency_bonuses["72h"]` points
- Else: 0 points

If `posted_at` is not available: 0 points.

## Phase 7: Market Boost

Look up `lead.country` in `scoring.market_boosts` (case-insensitive, also check common abbreviations like "US" for "United States").

- If found: add the boost points.
- If not found: 0 points.

## Phase 7.5: Contact Surface Bonus

If the lead includes a `contact_surfaces` object:
- `channel_count >= 3`: add `scoring.contact_surface_bonus.channels_3_plus` points (default 15)
- `channel_count == 2`: add `scoring.contact_surface_bonus.channels_2` points (default 5)
- `channel_count <= 1` or missing: 0 points

This bonus rewards leads reachable through multiple channels, enabling the full multi-channel outreach cadence.

## Phase 8: Final Score and Tier Assignment

```
total_score = base_score + keyword_score + hiring_bonus + budget_points + recency_bonus + market_boost + surface_bonus
```

Assign tier using `scoring.thresholds`:
- `total_score >= thresholds.hot` => **HOT**
- `total_score >= thresholds.warm` => **WARM**
- `total_score < thresholds.warm` => **COOL**

## Phase 8.5: Geo Split Enforcement

After scoring all leads, enforce the 75/25 geo split from config:

1. Separate scored leads into two pools: international and india
2. Target: ~75% international (~19 of 25 leads), ~25% India (~6 of 25 leads)
3. Within each pool, rank by score descending
4. Select top N from each pool to hit the target split
5. If one pool is short, allow the other pool to fill remaining slots

For company leads specifically (5/day target):
- ~4 international, ~1 India

For gig leads (20/day target):
- ~15 international, ~5 India

Flag any lead that was excluded due to geo split enforcement:
`"excluded_reason": "geo_split_cap_reached"`

## Phase 9: Output

Return a JSON array of scored leads:

```json
[
  {
    "url": "https://...",
    "platform": "Freelancer",
    "title": "Need Shopify developer for store redesign",
    "score": 75,
    "tier": "HOT",
    "lead_type": "gig",
    "geo_bucket": "international",
    "breakdown": {
      "platform_base": 45,
      "keyword_matches": {
        "primary": ["shopify developer", "shopify redesign"],
        "secondary": ["ecommerce redesign"],
        "intent": ["need a developer"]
      },
      "keyword_score": 30,
      "hiring_signal": true,
      "hiring_bonus": 20,
      "budget_points": 0,
      "recency_bonus": 0,
      "market_boost": 0,
      "surface_bonus": 15,
      "channel_count": 4
    },
    "reject_reason": null
  }
]
```

For rejected leads, include `"reject_reason": "Matched negative keyword: 'i am a shopify developer'"` and `"tier": "REJECTED"`.

## Phase 10: Log

If the CRM is configured, write scored leads to the CRM using the `crm-writer` skill. Log: url, platform, title, score, tier, lead_type, geo_bucket, scored_at timestamp.

Summary format:

```
Scored {N} leads:
- HOT: {count}, WARM: {count}, COOL: {count}, REJECTED: {count}
Geo split: X% international, Y% India (target: 75/25)
Lead mix: N company leads, N gig leads (target: 5/20)
```

## Example Usage

Trigger phrases:
- "Score these leads"
- "Qualify this lead list"
- "Run lead scoring on these results"
- "Which of these leads are hot?"

```
User: Score these leads from today's signal scan
Assistant: [reads agency.config.json, applies scoring algorithm with lead type awareness and geo split enforcement, returns sorted JSON with HOT leads first]
```
