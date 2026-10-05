---
name: investment-thesis-tracker
description: Create and maintain an append-only investment thesis with original evidence cutoff, what is priced in, falsifiable pillars, KPIs, catalysts, valuation and entry gates, risks, kill/add/trim/exit criteria, review dates, and evidence-delta updates. Use to monitor a holding or prior recommendation, prepare earnings reviews, or for Turkish intents such as “yatırım tezimi kaydet/takip et”, “bu hisseyi bundan sonra izle”, “tez bozuldu mu”, “hangi şartta artır/sat”, “önceki analizle ne değişti”. Separate company quality, security readiness, and portfolio action; never rewrite the original thesis with hindsight.
---

# Investment Thesis Tracker

Own the durable decision record across time. Use current evidence for every review and keep the baseline immutable.

Read [references/thesis-schema.md](references/thesis-schema.md). Use `$finance-evidence-guard` for claim updates, `$probabilistic-market-forecast` for forecast revisions, `$portfolio-risk-and-sizing` for action size and `$investment-red-team` when the thesis or action is consequential.

## Create the baseline

1. Resolve exact instrument, venue, currency, decision horizon, portfolio role and evidence cutoff.
2. Record what the market appears to price in and the differentiated thesis/variant view.
3. Define a small set of falsifiable pillars. Give each an observable KPI, expected path, source, review cadence and failure condition.
4. Record dated catalysts and what should happen if the thesis is right or wrong.
5. Separate business value/quality, security valuation/readiness and portfolio action/size.
6. Define price/valuation entry gates, add/trim/exit rules, hard thesis-kill criteria and the next scheduled review.
7. Store source links, assumptions, contradictions and confidence ceiling. Hash or otherwise preserve the baseline when the host supports it.

## Review the thesis

1. Preserve the original record and append a timestamped update.
2. Classify each new item as confirming, contradicting, neutral, resolved or still missing.
3. Compare actual KPI/catalyst path with the frozen expectation and explain material deltas.
4. Recompute valuation/forecast and identify whether the change came from evidence, price, time decay, portfolio constraints or an earlier analytical error.
5. Return separate statuses:
   - Company thesis: `INTACT / WEAKENED / BROKEN / IMPROVED`
   - Security readiness: `ATTRACTIVE / FAIR / EXPENSIVE / WAIT / INVALID`
   - Portfolio action: `ADD / HOLD / TRIM / EXIT / WATCH / NO ACTION`
6. State the next observable trigger and review date.

## Hard rules

- Never overwrite the original thesis, probability, target or kill criteria.
- Never treat price movement alone as proof that the thesis was right or wrong.
- Never move a kill criterion after it occurs without labeling a new thesis.
- Never confuse an excellent company with an attractive security at the current price.
- Never let sunk research effort or an existing position raise confidence.

## Output

Lead with the three separate statuses and evidence cutoff. Then show baseline versus current evidence, pillar/KPI table, catalyst progress, valuation/forecast delta, triggered rules, portfolio implication, contradictions, next review and confidence.
