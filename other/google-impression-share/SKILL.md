---
name: google-impression-share
description: |
  Google Ads impression-share analysis to identify missed scaling opportunities and diagnose delivery constraints. Distinguishes Lost-IS (Budget) — addressable with money — from Lost-IS (Rank) — addressable with bids/quality. Disciplined: only recommends scaling on campaigns that are already profitable (≥30 conversions in 30d AND CPA at/below target). Read-only — recommends budgets, bids, holds; never executes. Use weekly or when planning where to deploy more spend.
---

# Google Ads Impression Share Analysis (Read-Only)

For the Google Ads account the user names, analyze impression-share metrics across all active campaigns. **Read-only — recommends only, never adjusts budgets or bids.**

If the user didn't name an account, list their connected accounts and ask which one to use.

## Constraints (do not violate)

- **Only consider campaigns with ≥ 30 conversions in last 30 days.** Below that, the signal is too noisy.
- **Do not recommend budget increases for campaigns with CPA > 1.2× target.** Throwing money at unprofitable campaigns wastes money.
- **Do not recommend bid increases if already above target CPA.** Same logic.
- **Prioritize profitable scaling only.**

## Inputs (per campaign, last 30d)

- Search Impression Share
- Lost IS (Budget)
- Lost IS (Rank)
- Conversion volume + CVR
- CPA vs target
- ROAS
- Current daily budget

## Analysis buckets

### Bucket A — Scaling opportunity (high Lost-IS Budget + strong CPA)
- `Lost IS (Budget) ≥ 20%` AND `CPA ≤ target`
- Recommendation: budget increase. Suggest exact % based on how much budget headroom the IS gap implies.

### Bucket B — Bid / relevance issue (high Lost-IS Rank + good CVR)
- `Lost IS (Rank) ≥ 20%` AND `CVR ≥ campaign median`
- Recommendation: bid adjustment OR ad-strength / quality-score work. Suggest which.

### Bucket C — Overexposure (high IS + poor CPA)
- `Search IS ≥ 75%` AND `CPA > target`
- Recommendation: HOLD. Do not scale. Profitability problem, not a reach problem.

### Bucket D — Healthy (high IS + good CPA)
- `Search IS ≥ 80%` AND `CPA ≤ target`
- Recommendation: monitor. You're maxed out on demand for current keywords; growth requires new keyword expansion or new campaign types.

## Output format

Three sections, each a vertical list:

### 📈 Scale (recommend budget increase)
- `[Campaign] — Lost IS (Budget) 32%, CPA 22% under target. Suggest +30% budget, expected +N conversions/day.`

### 🔧 Fix (recommend bid / quality work)
- `[Campaign] — Lost IS (Rank) 28%, strong CVR. Suggest bid +15% OR ad-copy refresh — ad strength is "Average".`

### 🛑 Hold (no action recommended)
- `[Campaign] — Overexposed (IS 88%, CPA 38% above target). Fix profitability before scaling.`

For each campaign that hits the conversion-volume floor (< 30 conv / 30d), exclude it silently.

End with: `_All recommendations — no budgets or bids changed. Ask explicitly to enact any of these._`
