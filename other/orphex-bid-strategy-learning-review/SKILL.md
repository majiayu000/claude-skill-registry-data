---
name: orphex-bid-strategy-learning-review
description: "Review Google Ads bidding goals, reported learning status, conversion delay, and delivery constraints before proposing strategy or target changes."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Bid Strategy & Learning Review

Review the fit between the user's business goal, biddable conversion signal, actual strategy, and observed delivery. Preserve current platform strategy names; label changes do not establish behavior changes.

## Assess the supplied strategy

Establish the primary versus secondary conversion goals, value definition, conversion/import delay, strategy scope (campaign/portfolio), target and average target over the interval, budgets, status reason, eligibility, and change dates. Distinguish a missing goal or import problem from a restrictive target, capped spend, policy/eligibility issue, or ordinary reporting delay. Compare mature equal-length intervals; do not treat recent incomplete conversions as deterioration.

Read the actual strategy status and its reason. A strategy/composition or goal change can require calibration; a target edit does not universally reset Smart Bidding learning. Do not recommend a fixed percentage step, conversion threshold, or universal waiting period as a rule. Use the supplied reporting cycle, platform guidance for the actual strategy, and the account's business constraints. A target CPA is not a per-conversion ceiling; target ROAS and attributed values are not profit.

Rank constraints using observed evidence. Historical average CPA/ROAS and target simulators have different meanings; simulator outputs are modeled scenarios with stated dates/scope, not guarantees. Recommend a target change only when its objective, bound, feasibility, and monitoring condition are supported. If goals or measurement are unreliable, resolve that before economically interpreting bidding performance.

## Deliver a decision

Report strategy fit, actual status, mature metrics, supported constraints, unknowns, and a review point after conversions/imports mature. Keep strategy, target, and goal changes as proposals unless the specific changes and account write path are authorized. Preserve prior settings for a requested rollback; do not switch goals merely to collect more events.

## Official references

- [Google Smart Bidding learning and target changes](https://support.google.com/google-ads/answer/10970825?hl=en)
- [Google learning status reasons](https://support.google.com/google-ads/answer/13020501?hl=en)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
