---
name: meta-creative-fatigue-detection
description: |
  Per-ad creative fatigue diagnosis on Meta Ads. Scores every active ad as Healthy / Early Warning / Fatigued / Dead using CTR decline, frequency creep, CPA spike, CVR decline, and spend-shift signals. Surfaces specific refresh recommendations: which variants to retire, which winners to remix, which themes to test next. Read-only — no pauses applied. Use weekly or before any creative refresh cycle.
---

# Meta Creative Fatigue Detection (Read-Only)

Diagnose creative fatigue across the ad account the user names. Default lookback: 14 days. **Read-only — never pauses or modifies ads.**

If the user didn't name an account, list their connected accounts and ask which one to use.

## Fatigue scoring signals

Score each active ad on:

| Signal | Healthy | Early Warning | Fatigued | Dead |
|---|---|---|---|---|
| **CTR decline** vs first-week-of-life | < 10% drop | 10–25% drop | 25–50% drop | > 50% drop |
| **Frequency** | < 2.5 | 2.5 – 3.5 | 3.5 – 5 | > 5 |
| **CPA spike** vs ad-set median | < 10% above | 10–25% above | 25–50% above | > 50% above |
| **CVR decline** vs first-week | < 10% drop | 10–25% drop | 25–50% drop | > 50% drop |
| **Spend shift** | Stable or rising | Flatlined | Declining | Reaching cliff |

Final classification = worst signal score across all five dimensions.

## Output

### Section 1 — Fatigue summary table

| Ad name | Score | CTR drop | Freq | CPA delta | CVR drop | Days live |

Sort: most fatigued first. Cap at top 20.

### Section 2 — Per-ad recommendations

For each `Fatigued` or `Dead` ad, one line:
- `🪦 [Ad name] — Dead. Recommendation: retire. The hook is exhausted; do not relaunch as-is.`
- `🔻 [Ad name] — Fatigued. Recommendation: pause this variant; the underlying concept is still winning, remix the hook.`
- `⚠️  [Ad name] — Early Warning. Watch — likely needs a refresh in 7–14 days.`

For each `Healthy` or `Early Warning` winning ad with strong CVR:
- `✨ [Ad name] — Healthy winner. Recommendation: extract the pattern, brief 2–3 variants on the same concept.`

### Section 3 — Creative refresh brief

3–5 bullet points on what themes/hooks/formats deserve fresh creative based on the patterns you see in the Fatigued + Healthy-winner cohorts.

End with: `_All recommendations — no changes applied. Ask explicitly to pause anything._`
