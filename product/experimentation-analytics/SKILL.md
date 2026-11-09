---
name: "experimentation-analytics"
description: "How to read experiment results without fooling yourself. Confidence intervals, p-values, multiple testing, sequential testing, CUPED, heterogeneous treatment effects, ratio metrics, network effects, dashboard reconciliation, and the interpretation failures that produce confidently wrong shipping decisions. Use this skill whenever the user is reading a finished experiment result panel and about to make a ship, kill, or iterate decision, or when an experiment number does not match the dashboard number. Triggers on read experiment results, result panel, ship or kill decision, p-value, confidence interval, statistical significance, multiple testing, peeking, sequential testing, CUPED, variance reduction, heterogeneous treatment effects, ratio metric, network effects, inconclusive test, experiment versus dashboard mismatch. Use `experiment-design` instead when the test has not run yet and the question is hypothesis, sample size, duration, or what to test."
---

# Experimentation Analytics

A data-team-mentor's playbook for interpreting experiment results without fooling yourself.

The result panel is the moment-of-truth for an experiment. The numbers on it determine whether you ship, kill, or iterate. They also expose every shortcut taken in the design phase: an underpowered test produces wide confidence intervals; a peeked test produces a too-narrow p-value; a ratio metric without delta-method correction produces overconfident lift estimates. Most ship-the-wrong-thing decisions trace back to misreading the result panel.

This skill is the discipline that prevents misreading. It assumes the experiment was designed well (see the `experiment-design` skill). It assumes the platform's results panel is technically correct (most modern platforms are; some older ones are not). It assumes you can read a number off a screen. The hard part is knowing what each number actually means and what it does not, and that is what is here.

When to use this skill: any time you are reading an experiment result panel and about to make a ship, kill, or iterate decision.

---

## What this skill is for

This skill covers result interpretation, the statistical concepts that make the numbers trustworthy, and the dashboard reconciliation work that prevents executive-level confusion when the experiment number does not match the BI number. The audience is product managers and data analysts who read experiment results together and need a shared vocabulary that does not paper over the dangerous parts of statistics.

Companion skills cover the adjacent territory. The `experiment-design` skill covers pre-experiment thinking: hypothesis, sample size, MDE, segments, what NOT to test. Read it before designing the test; read this skill when reading the result. The `feature-flagging` skill covers the operational mechanics of flag management, environment promotion, and stale-flag cleanup. Together the three skills span the experimentation lifecycle from intent through interpretation. For platform-specific MCP commands, consult the chosen platform's docs; Statsig, PostHog, Optimizely, GrowthBook, Eppo, Amplitude, and Kameleoon all expose rich analytics surfaces that this skill informs how to read.

---

## Reference files

- [`references/confidence-interval-cheatsheet.md`](references/confidence-interval-cheatsheet.md). How to read a CI, what to ignore, the five decision rules with worked examples for each.
- [`references/p-value-interpretation-guide.md`](references/p-value-interpretation-guide.md). What it means, what people pretend it means, the 0.05 convention, the peeking problem, and the multiple-testing context.
- [`references/statistical-method-reference.md`](references/statistical-method-reference.md). CUPED, the delta method, sequential testing methods (mSPRT, group sequential, anytime-valid), HTE handling, multiple testing corrections, cluster randomization. The technical reference for analysts.
- [`references/dashboard-vs-experiment-reconciliation.md`](references/dashboard-vs-experiment-reconciliation.md). Why the BI number does not match the experiment number, the blended-attribution trap, and how to communicate the difference to non-statistical stakeholders.
- [`references/result-presentation-templates.md`](references/result-presentation-templates.md). Five templates for stakeholder communication: clear win, clear loss, inconclusive (the most common, hardest), mixed (positive primary with ambiguous guardrail), and long-term holdout report.
- [`references/analytics-platform-comparison.md`](references/analytics-platform-comparison.md). Profiles of seven major platforms (Statsig, PostHog, Optimizely, GrowthBook, Eppo, Amplitude, Kameleoon) covering what each exposes, what each hides, and the gotchas in each.
- [`references/common-interpretation-failures.md`](references/common-interpretation-failures.md). Fifteen-plus failure patterns: name, symptom, root cause, fix, prevention.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The result panel: what every modern platform should expose: [method](references/domain-guide.md#the-result-panel-what-every-modern-platform-should-expose).
- Confidence intervals: the most important number: [method](references/domain-guide.md#confidence-intervals-the-most-important-number).
- P-values: what they mean and what they do not: [method](references/domain-guide.md#p-values-what-they-mean-and-what-they-do-not).
- Multiple testing corrections: [method](references/domain-guide.md#multiple-testing-corrections).
- Sequential testing math: [method](references/domain-guide.md#sequential-testing-math).
- CUPED variance reduction: [method](references/domain-guide.md#cuped-variance-reduction).
- Heterogeneous treatment effects (HTE) and segments: [method](references/domain-guide.md#heterogeneous-treatment-effects-hte-and-segments).
- Ratio metrics and the delta method: [method](references/domain-guide.md#ratio-metrics-and-the-delta-method).
- Bayesian vs frequentist results panels: [method](references/domain-guide.md#bayesian-vs-frequentist-results-panels).
- Network effects and SUTVA violation: [method](references/domain-guide.md#network-effects-and-sutva-violation).
- Dashboard metric vs experiment metric reconciliation: [method](references/domain-guide.md#dashboard-metric-vs-experiment-metric-reconciliation).
- Long-term effect estimation: [method](references/domain-guide.md#long-term-effect-estimation).
- Common interpretation failures: [method](references/domain-guide.md#common-interpretation-failures).
- The framework: 14 considerations for trustworthy experiment interpretation: [method](references/domain-guide.md#the-framework-14-considerations-for-trustworthy-experiment-interpretation).
- Closing: the courage to call it inconclusive: [method](references/domain-guide.md#closing-the-courage-to-call-it-inconclusive).
