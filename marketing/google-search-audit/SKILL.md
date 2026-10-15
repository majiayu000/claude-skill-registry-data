---
name: google-search-audit
description: |
  Daily Google Ads Search morning briefing — compares last 3 days vs prior 3 days, segments brand vs non-brand (with different expectations for each), and surfaces specific recommendations across budget, impression share, bid adjustments, search-term waste, and query opportunities. Read-only — produces a CUT / FIX / SCALE recommendations list, never executes mutations. Use as your morning Google Search standup.
---

# Google Ads Search Audit — Morning Briefing (Read-Only)

For the Google Ads account the user names, run a daily Search-campaigns operator pass. Compare **last 3 days vs prior 3 days**. **Read-only — output is recommendations only, no mutations applied.**

If the user didn't name an account, list their connected accounts and ask which one to use.

## Step 1 — Brand vs Non-Brand classification (do first)

For every Search campaign, classify as **Brand** or **Non-Brand** before analyzing. Use campaign name, keyword content, and whether top queries contain the brand name.

| Type | Healthy state | Focus |
|---|---|---|
| **Brand** | IS > 85%, low CPA, query intent clean | Efficiency, waste reduction. Scaling is demand-limited, not budget-limited. |
| **Non-Brand** | Growth runway in IS, CPA at-or-below target | IS growth, budget scaling, volume expansion. |

Surface recommendations against the correct expectation per type.

## Step 2 — Metrics to pull

Per campaign, both 3d windows: CPA vs target, Conversion volume, Search Impression Share, Lost IS (Rank), Lost IS (Budget), Top-of-page rate, Absolute-top %, ROAS, Conversion Value (AOV trend).

## Step 3 — Analysis tasks

### Budget + efficiency
- Campaign with rising CPA + stable/improving IS → **likely demand issue**, recommendation: reassess targeting or pause
- Campaign with low IS + strong CPA → **suggest budget increase** with exact %
- Campaign where CPA improved but ROAS declined → **flag AOV / mix-shift issue**

### Impression share
- `Lost IS (Budget) > 20%` → suggest budget increase, state %
- `Lost IS (Rank) > 20%` → suggest bid adjustment or relevance work

### Search-term waste
- Identify queries spending > 2× target CPA with poor conversion intent
- Suggest exact-match negative keywords (do not add them — recommend only)

### Query-level opportunities
- Identify high-converting queries not yet in exact match
- Suggest exact-match keyword additions

### Alerts
- Flag any sudden drop > 25% in CVR, IS, conversions, or ROAS — surface as "investigate first"

## Output format

Three sections, each a vertical list of recommendation lines:

### 🛑 CUT / WASTE
- `Suggest adding negative exact: "[query]" — spending $X at CPA $Y (3.2× target)`

### 🔧 FIX
- `Suggest bid +15% on [ad group] — Lost IS (Rank) 28%, strong relevance signal`

### 📈 SCALE
- `Suggest budget +20% on [campaign — Non-Brand] — Lost IS (Budget) 35%, CPA 18% under target`

Skip a section entirely if it has no recommendations. End with: `_All recommendations — no changes applied._`
