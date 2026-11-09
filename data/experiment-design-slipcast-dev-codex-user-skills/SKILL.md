---
name: "experiment-design"
description: "A discipline for designing experiments (A/B tests, multivariate, holdouts) so the results actually answer the question you asked. Hypothesis writing, sample size, duration, segment analysis, running discipline, matching a result to a pre-committed decision rule, and the common failure modes that produce confidently wrong shipping decisions. Use this skill whenever the user is planning a test that has not run yet: framing a hypothesis, sizing the sample, setting duration, choosing guardrails, or deciding whether something is worth testing at all. Triggers on design an experiment, experiment plan, A/B test, split test, multivariate test, holdout, experiment hypothesis, sample size, minimum detectable effect, MDE, test duration, guardrail metric, no peeking, pre-committed decision rule, is this worth testing. Use `experimentation-analytics` instead when the test has already run and the question is how to read the result panel."
---

# Experiment Design

A senior product manager's playbook for running experiments that produce trustworthy decisions.

The default state of experimentation in most companies is sloppy. PMs run tests against vague hypotheses, look at results too early, ignore guardrails, stratify into noise, and ship features whose lift is mostly measurement error. The cost is real: ship the wrong thing, kill the right thing, learn the wrong lesson, repeat.

This skill is the discipline that prevents most of those mistakes. It assumes you have a working experimentation platform (Statsig, PostHog, GrowthBook, Optimizely, Amplitude, Eppo, Kameleoon; the platform does not matter for the principles). It assumes you have product-design and engineering pipelines that can deliver real treatment changes. The hard part is the thinking, and that is what is here.

When to use this skill: any time you are about to design or interpret an experiment. Read the relevant section before you start, not after the test is running.

---

## What this skill covers

The skill spans the full experiment lifecycle. Pre-experiment readiness (is this thing even worth testing). Hypothesis design (cause, effect, magnitude, mechanism). Sample size and minimum detectable effect (do you have enough traffic to learn anything). Duration (how long is long enough, when does the cycle bias the result). Running discipline (no peeking, guardrails, sequential testing). Interpretation (the three buckets and the inconclusive case). Decision-making (matching the result to a pre-committed rule).

The skill does not cover feature flag operational mechanics; those live in the `feature-flagging` skill, which handles flag taxonomy, environment management, and stale-flag cleanup as a separate discipline. The skill does not cover statistical analysis depth; for delta methods, variance reduction techniques like CUPED, and Bayesian alternatives, see the `experimentation-analytics` skill. The skill does not cover platform-specific tooling; for MCP commands, auth models, and platform-specific configuration, consult the chosen platform's official documentation. This skill produces the experiment design; the platform implements it.

For the orchestration layer above (which experiments to run, in what order, with what cadence), see the forthcoming `experimentation-platform-orchestrator` skill. That skill schedules; this skill designs.

---

## If required data is unavailable

This skill's output depends on data, measurements, or tool results it cannot generate on its own. When a required input, tool, or data source is unavailable or unverifiable, the sanctioned output is the deliverable with the gap stated: what was needed, what was actually obtained or verified, and which parts of the output are affected. Fabricating, estimating, or interpolating a required number to complete the deliverable is never sanctioned. A stated gap is a complete answer.

---

## Reference files

- [`references/hypothesis-templates.md`](references/hypothesis-templates.md). Concrete formats for writing hypotheses that pass the cause-effect-magnitude-mechanism test, with worked examples across conversion, engagement, revenue, retention, and funnel-step metric types.
- [`references/sample-size-tables.md`](references/sample-size-tables.md). Pre-calculated sample size tables for the most common conversion-rate experiments, with how-to-use guidance and the common pitfalls in sample-size planning.
- [`references/common-failures.md`](references/common-failures.md). Fifteen anti-patterns that produce wrong shipping decisions, each with symptom, root cause, fix, and prevention.
- [`references/results-interpretation-checklist.md`](references/results-interpretation-checklist.md). Step-by-step checklist for reading results, the three-bucket decision matrix (win, loss, inconclusive), and the post-launch monitoring discipline.
- [`references/platform-comparison.md`](references/platform-comparison.md). Profiles of the major experimentation platforms (Statsig, PostHog, GrowthBook, Optimizely, Amplitude, Eppo, Kameleoon) with strengths, gotchas, and a decision matrix for choosing.
- [`references/pre-experiment-readiness-checklist.md`](references/pre-experiment-readiness-checklist.md). Ten-item go/no-go checklist run through before launch.
- [`references/post-experiment-decision-framework.md`](references/post-experiment-decision-framework.md). The moment-of-decision framework: confirm pre-commitment, apply rule mechanically, route to ship/kill/inconclusive paths, write the post-mortem within a week.

---


## Conditional methods

Before applying a method below, read its linked section. For a narrow task select only relevant methods; for a full audit/design use the framework and relevant failure patterns. Existing references remain available for deeper details.

- The framework: 12 considerations for trustworthy experiment results: [method](references/domain-guide.md#the-framework-12-considerations-for-trustworthy-experiment-results).
- Hypothesis discipline: [method](references/domain-guide.md#hypothesis-discipline).
- Sample size and minimum detectable effect: [method](references/domain-guide.md#sample-size-and-minimum-detectable-effect).
- Test duration: [method](references/domain-guide.md#test-duration).
- What NOT to A/B test: [method](references/domain-guide.md#what-not-to-ab-test).
- Segment analysis: [method](references/domain-guide.md#segment-analysis).
- Interaction effects: [method](references/domain-guide.md#interaction-effects).
- Ratio metrics and the delta method: [method](references/domain-guide.md#ratio-metrics-and-the-delta-method).
- Network effects and two-sided markets: [method](references/domain-guide.md#network-effects-and-two-sided-markets).
- Sequential testing and the peeking problem: [method](references/domain-guide.md#sequential-testing-and-the-peeking-problem).
- Pre-commitment vs p-hacking: [method](references/domain-guide.md#pre-commitment-vs-p-hacking).
- Reading results and making the call: [method](references/domain-guide.md#reading-results-and-making-the-call).
- Common failures and fixes: [method](references/domain-guide.md#common-failures-and-fixes).
- Closing: when in doubt: [method](references/domain-guide.md#closing-when-in-doubt).
