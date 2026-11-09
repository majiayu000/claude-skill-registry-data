---
name: "ads-performance-analytics"
description: "How to read paid media dashboards without fooling yourself. Attribution models, platform reporting quirks, multi-platform reconciliation, ROAS vs LTV horizon traps, statistical noise in performance metrics, incrementality testing, and the failure modes that produce expensive lessons. Triggers on read paid media dashboard, attribution analysis, ROAS vs LTV, multi-platform reconciliation, ad incrementality, geo holdout, conversion lift study, ghost bidding, paid media reporting, board-deck paid media metrics, blended CAC, MMM, MTA, last-click attribution. Also triggers when a marketer is about to scale, kill, or rebudget a campaign based on platform metrics, or when reconciling platform reports against warehouse revenue."
---

# Ads Performance Analytics

A data-team-mentor's playbook for interpreting paid media dashboards without fooling yourself.

The dashboard is the moment of truth for paid media decisions. The numbers on it determine whether you scale, hold, or kill. They also expose every platform's self-attribution bias, every modeled-conversion shortcut, every cross-platform double-count. Most "scale this campaign" decisions trace back to misreading the dashboard.

This skill is the discipline that prevents misreading. It assumes the campaign was strategically sound (see `paid-media-strategy`). It assumes the creative was tested properly (see `ads-creative-development`). The hard part is knowing what each number actually means, what it does not, and how to reconcile platform-reported metrics with the truth in your warehouse.

When to use this skill: any time you are about to scale, kill, or rebudget a campaign based on platform metrics; reconciling platform reports with revenue data; evaluating an agency's reporting; or building a paid media dashboard that will not lie to you.

---

## What this skill is for

This skill spans paid media result interpretation. It does not cover paid media strategy (use `paid-media-strategy`), creative production (use `ads-creative-development`), or platform-specific tooling (covered in the integrations microsites). Pair this skill with the relevant integrations microsite for platform-specific MCP commands and example prompts.

The audience is a marketer, growth analyst, agency analyst, or founder evaluating paid media reports. The voice is patient and clinical. There is no "trust the platform's number" or "ignore the platform entirely." Both are wrong. The discipline is knowing which numbers from which platform mean what, and what to reconcile against to make the actual decision.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/metric-definitions-glossary.md`](references/metric-definitions-glossary.md) - CTR, CPC, CPM, CPA, ROAS, LTV, AOV, frequency, reach, impressions, conversion window, view-through, modeled conversion, blended CAC, MER.
- [`references/attribution-model-comparison.md`](references/attribution-model-comparison.md) - Last-click, first-click, linear, time-decay, U-shaped, DDA, MMM. Decision matrix by business stage.
- [`references/platform-reporting-quirks.md`](references/platform-reporting-quirks.md) - Google PMax black box, Meta iOS impact and Conversions API, LinkedIn 30-day click defaults, TikTok video-completion attribution, programmatic viewability gates.
- [`references/incrementality-testing-playbook.md`](references/incrementality-testing-playbook.md) - Geo holdout, Conversion Lift and Experiments, PSA tests, switchback designs. Setup, duration, analysis pattern, expected incremental rates.
- [`references/dashboard-reconciliation-patterns.md`](references/dashboard-reconciliation-patterns.md) - Warehouse as canonical, platform as in-flight signal, blended CAC formula, board-deck patterns, reconciliation cadence.
- [`references/cohort-analysis-templates.md`](references/cohort-analysis-templates.md) - By acquisition month, channel, and campaign. Retention curves, when to act on cohort signals.
- [`references/common-interpretation-failures.md`](references/common-interpretation-failures.md) - Twelve failure patterns with symptom, root cause, fix, prevention.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The result panel: what every paid media platform should expose: [method](references/domain-guide.md#the-result-panel-what-every-paid-media-platform-should-expose).
- Platform-reported vs reality: [method](references/domain-guide.md#platform-reported-vs-reality).
- Attribution models in practice: [method](references/domain-guide.md#attribution-models-in-practice).
- Multi-platform reconciliation: [method](references/domain-guide.md#multi-platform-reconciliation).
- ROAS vs LTV: the time horizon trap: [method](references/domain-guide.md#roas-vs-ltv-the-time-horizon-trap).
- Cohort analysis vs daily metrics: [method](references/domain-guide.md#cohort-analysis-vs-daily-metrics).
- Statistical noise in performance metrics: [method](references/domain-guide.md#statistical-noise-in-performance-metrics).
- Incrementality testing: [method](references/domain-guide.md#incrementality-testing).
- Geo experiments and holdouts: [method](references/domain-guide.md#geo-experiments-and-holdouts).
- Platform self-attribution bias: [method](references/domain-guide.md#platform-self-attribution-bias).
- Common interpretation failures: [method](references/domain-guide.md#common-interpretation-failures).
- The framework: 12 considerations for trustworthy paid media interpretation: [method](references/domain-guide.md#the-framework-12-considerations-for-trustworthy-paid-media-interpretation).
- Closing: the courage to call it incremental zero: [method](references/domain-guide.md#closing-the-courage-to-call-it-incremental-zero).
