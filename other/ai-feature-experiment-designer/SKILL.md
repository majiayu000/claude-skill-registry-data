---
name: ai-feature-experiment-designer
description: "Designs A/B tests for non-deterministic Artificial Intelligence (AI) features: an offline-evaluation gate, variance-aware sample sizing, a primary metric with guardrails for cost per task, latency, and override rate, novelty-effect handling, and pre-registered ship / iterate / kill decision rules. Use when testing a new model, prompt, or agent behavior in production; comparing two Large Language Model (LLM) providers or versions; deciding whether an AI feature actually moves a business metric; or an online test result contradicts offline evaluations."
---

# AI Feature Experiment Designer

> The same input can produce different outputs, costs, and latencies - an AI experiment has to measure all three before it declares a winner.

## What this skill is

An experiment-design workflow for features whose behavior is stochastic and whose quality, cost, and speed move together. It pairs offline evaluations (cheap, fast, controlled) with online A/B tests (real users, real outcomes), sizes samples for the extra variance that model outputs add, and pre-registers guardrails so a variant that lifts engagement while doubling inference cost or eroding trust does not ship by accident.

## What it solves

- Shipping a new prompt or model because offline evaluation scores rose, with no evidence users or revenue benefit
- Underpowered tests that read noise from output variance as a win
- Variants that win the primary metric while silently raising cost per task or latency
- Novelty spikes in the first week mistaken for durable lift
- Peeking at results daily and stopping the test at the first significant reading
- Metrics such as thumbs-up rate that are biased by who chooses to rate

## When to invoke

- Swapping or upgrading the model behind a production feature
- Testing prompt, retrieval, or agent-planning changes with real users
- Launching an AI feature and needing proof of incremental business impact
- Choosing between providers on quality, cost, and latency together
- Reconciling an online result that disagrees with offline evaluations

## Phase 1: Frame the hypothesis and unit

| Field | Example |
|-------|---------|
| Change | New retrieval step plus updated system prompt |
| Hypothesis | Raises task success because answers cite the customer's own documents |
| Unit of randomization | User or account (not request - avoids one user seeing both variants) |
| Population | Active users who trigger the feature at least once in the window |
| Exposure point | First time the feature is invoked after assignment |

Randomize by user or account whenever the experience accumulates (memory, history, learned preferences). Request-level randomization is acceptable only for stateless, single-turn features.

## Phase 2: Offline evaluation gate

Run before any traffic is exposed.

| Check | Pass condition |
|-------|----------------|
| Task-quality evaluation | Variant is not worse than control on a held-out set of 200+ realistic tasks, scored by rubric or graded model with human spot checks |
| Regression suite | No new failures on known critical cases |
| Safety and policy | No increase in policy violations on adversarial prompts |
| Cost and latency | Projected cost per task and 95th percentile (p95) latency within guardrail budgets |

Offline evaluation decides whether a variant is safe to test. It does not decide whether to ship.

## Phase 3: Metric stack

| Role | Metric | Notes |
|------|--------|-------|
| Primary | Task success rate, accepted-output rate, or downstream conversion | One metric, tied to user or business value |
| Secondary | Retention of feature users at day 7 and 28, tasks per user | Directional support |
| Guardrail: cost | Inference cost per successful task | Includes retries and tool calls |
| Guardrail: speed | p95 time to first token and to complete answer | |
| Guardrail: trust | Override rate (user edits, regenerates, or discards output), complaint rate | |
| Guardrail: safety | Flagged outputs per 1,000 tasks | |

Prefer behavioral signals (accepted, edited, copied, regenerated) over voluntary ratings, which suffer from selection bias.

## Phase 4: Variance-aware sample sizing

Model outputs add within-user variance, so use the observed variance of the primary metric from the current production feature, not textbook values.

```
n per arm = 2 x (z_alpha/2 + z_beta)^2 x sigma^2 / MDE^2
```

- z_alpha/2 = 1.96 for 95% confidence; z_beta = 0.84 for 80% power
- sigma^2 = per-user variance of the primary metric (for a rate p, use p x (1 - p) adjusted by the design effect below)
- MDE = Minimum Detectable Effect, stated in absolute terms

When randomizing by user but measuring per task, inflate for clustering:

```
Design effect = 1 + (m - 1) x ICC
```

where m is the average tasks per user and ICC is the Intra-Class Correlation of the metric within users. Multiply n by the design effect. Use Controlled-experiment Using Pre-Experiment Data (CUPED) variance reduction with a pre-period covariate when available.

## Phase 5: Duration and novelty handling

- Run at least 2 full weekly cycles, and longer if the feature is used weekly rather than daily
- Plot the treatment effect by day since first exposure; if it decays, report the stabilized effect from weeks 2 onward
- Hold out a small long-term control (for example 5%) for major AI changes to measure durable impact over 4-8 weeks
- Freeze the model version and prompt for both arms during the test; a silent provider update invalidates the comparison

## Phase 6: Pre-registered decision rules

| Outcome | Decision |
|---------|----------|
| Primary significant and positive, all guardrails within limits | Ship |
| Primary positive, one guardrail breached (for example cost per task +25%) | Iterate on cost or latency, re-test |
| Primary flat, guardrails improved (cheaper or faster at same quality) | Ship as an efficiency win |
| Primary flat, guardrails flat or worse | Kill or return to offline work |
| Primary negative or safety guardrail breached | Kill and run a post-mortem |

Set guardrail limits numerically before launch (for example: cost per successful task no more than +10%, p95 latency no more than +500 milliseconds, override rate no more than +2 points). Use a sequential testing method if the team will look before the planned end.

## Phase 7: Readout

Report the effect with confidence intervals, the guardrail table, the novelty curve, segment cuts (new versus existing users, heavy versus light users, task type), and the offline-to-online agreement: did offline evaluation predict the online result? Track that agreement over time to learn how much to trust offline evaluations.

## Output

- Experiment brief: hypothesis, unit, population, exposure point
- Offline evaluation gate results
- Metric stack with numeric guardrail limits
- Sample size calculation including design effect and planned duration
- Pre-registered decision table
- Readout template with novelty curve and offline-to-online agreement

## Operating rules

**Always**
- Gate every online test behind an offline evaluation pass
- Include cost per successful task and p95 latency as guardrails
- Randomize at the user or account level for stateful features
- Pin model and prompt versions for the whole test window
- Write decision rules before the test starts

**Never**
- Ship on offline evaluation scores alone
- Use voluntary thumbs-up rate as the primary metric
- Stop the test early at the first significant reading without a sequential method
- Compare variants measured in different weeks or on different model versions
- Report a first-week lift as durable without checking the novelty curve
