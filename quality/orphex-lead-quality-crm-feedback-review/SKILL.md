---
name: orphex-lead-quality-crm-feedback-review
description: "Compare campaign lead cost with matched CRM qualification and sales outcomes, accounting for cohort maturity, stage definitions, and join coverage."
license: MIT
metadata:
  version: "2.0.1"
---

# Orphex Lead Quality & CRM Feedback Review

Assess whether acquisition produces the business's defined qualified leads, opportunities, and customers. Analyze the supplied CRM evidence without converting unmatched outcomes into failures or successes.

Unequal coverage may distort a comparison, but it does not establish that any portion of an observed rate or cost gap is a coverage artifact. Do not describe the gap as partly driven by observing less of a cohort without actual missing-outcome evidence; all unmatched leads could have no qualifying outcome. State the possible bias and unknown contribution consistently. When applicable, show the full-cohort outcome bounds and the corresponding cost-per-outcome range from known versus maximally qualifying unmatched leads, rather than causally explaining the observed cost difference from coverage alone.

## Establish the cohort and join

Use lead-created or another explicitly supplied acquisition cohort, with campaign scope, spend, attribution rule, stage definitions, snapshot time, follow-up horizon, currency, and unique identity/count rules. Distinguish unique source leads from fractional platform attribution credits; the latter cannot be used as a person-matching denominator. Use aggregate evidence or authorized pseudonymous joins. Do not request raw emails, phone numbers, or upload identities just to run this analysis.

Validate deduplication, one-to-many opportunity/customer relationships, reopened/lost statuses, and stage nesting. Calculate join coverage = unique matched origin leads / eligible unique origin leads. Then report qualified / matched, won / matched, and observed qualified or won / all origin leads separately. Unmatched leads have unknown downstream outcomes; matched-only rates can be selection-biased. Do not extrapolate their rate to the full cohort without an explicit supported missingness model.

Join coverage measures how much of the cohort is observed, not the direction or magnitude of selection bias. Do not claim that a coverage gap drives most of a quality difference without supporting evidence. Higher or equal coverage does not make missing outcomes ignorable or matched cohorts exchangeable, and no universal coverage cutoff establishes an actionable winner. After a revised join, recompute observed denominators, rates, and worst-case bounds for unmatched outcomes; recheck stage definitions and follow-up comparability. Scope any ranking to the exact metric: disjoint valid worst-case bounds can establish a full-cohort qualification-rate ordering without a missingness model, but not a cost, marginal-return, or budget winner. If those bounds overlap, keep that ordering unresolved unless additional evidence or a justified missingness model supports it; a maintained matched-only rate is not proof of cohort superiority.

Align cohorts by the same elapsed follow-up and stage snapshot, not only the same calendar week. Recent leads can remain unresolved. Use cohort acquisition spend for observed cost per qualified/won outcome; report incomplete coverage, delayed stages, and current snapshot effects. Closed-won value, recognized revenue, cash collected, and contribution are different metrics. Zero won counts give an unavailable cost per won, not zero.

## Recommend a feedback improvement

Prioritize definition, identity, coverage, and import-lag gaps before shifting budget or bidding goals. If an offline/enhanced conversion path is requested, verify current consent, supported identifiers, deduplication, timestamps, goal mapping, and authorized write scope. Deliver the cohort table, observed economics, coverage/maturity limitations, and a bounded next reconciliation or experiment. A matched attribution relation is not causal acquisition lift.

## Official reference

- [Google enhanced conversions for leads](https://support.google.com/google-ads/answer/15713840?hl=en)

## Portable inputs and examples

- Read [the input contract](references/input-contract.md) when mapping a new export or checking the example's scope and definitions. Copy [the header-only CSV template](assets/input-template.csv) when preparing data; equivalent supplied exports remain acceptable.
- Read [the reusable business context](references/business-context.md) only for business facts or constraints this task needs. Reuse user-supplied facts with their source/date; the template contains no default targets.
- Inspect [the complete fictional input](assets/example-input.csv) with [its example output](references/example-output.md) when learning the output and calculation boundaries. Never use fictional values for a real account.

State whether the result is complete, partial, or blocked for the requested decision. Link material findings to actual supplied rows/sources and separate observed metrics, hypotheses, and estimates. Lead with a short business conclusion, then evidence, uncertainty, and the next measurable check. A data export or installed skill does not authorize account changes.

For the supported arithmetic only, optionally run [the bundled calculator](scripts/marketing_math.py) with Python 3: `python3 scripts/marketing_math.py weighted-ratio < calculation.json`. Read its input mapping in the input contract before preparing JSON. It reads JSON, not CSV directly. If Python or the requested method is unavailable, show a reproducible alternative calculation or mark it unsupported; do not report an uncomputed result as verified.
