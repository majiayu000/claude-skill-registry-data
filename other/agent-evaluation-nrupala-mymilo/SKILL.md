---
name: agent-evaluation
description: Measure agents before trusting them — task suites, regression gates, calibrated judging, scorecards.
version: 1
triggers: evaluate an agent, agent scorecard, agent regression, test an agent, agent benchmarks
category: How Milo works
blurb: Measure an agent before trusting it, with task suites, regression gates and scorecards.
archetype: knowledge
example: Build a scorecard to evaluate whether this agent is actually improving.
---

# Agent Evaluation

Agent changes (model, prompt, tools, context) are behavior changes. Measure them like code: task suites, regression gates, honest scorecards.

## When to use
- Changing any model, prompt, tool set, or retrieval context for an agent.
- Deciding between agents for a role ("is the new model actually better here?").
- Turning an incident into a permanent regression test.

## Method
1. **Task suites**: golden tasks per capability with acceptance criteria — success definition, allowed cost, allowed latency, safety constraints. Version them with the agent.
2. **Reproducible runs**: pin model versions, seeds/temperatures, tool states, fixtures; run the same suite per candidate; store raw transcripts.
3. **Judging carefully**: deterministic checks first (did it do the thing?); LLM-judges only when calibrated against human labels, blinded, with position bias controls. The model under test never judges itself uncalibrated.
4. **Regression gates**: eval suite runs before merging agent changes; regressions block until explained (accepted trade-offs are written, not vibes).
5. **Beyond accuracy**: track steps-to-completion, cost, latency, refusal/error rates, safety violations, and "silent wrongness" (confident bad output) — the metrics that hurt in production.
6. **Incident replay**: every production misbehavior becomes a named test case (like bug→regression for code).
7. **Scorecards**: publish a compact table per run (task, pass, cost, notes) — honest comparisons beat leaderboards.
8. **Watch benchmark hygiene**: contamination (tasks leaking into training), variance across runs (run N times, report spread), and drift (re-baseline after model updates).

## Quality gates
- [ ] Suite versioned, criteria written before running.
- [ ] Every agent-affecting change gated on an eval run.
- [ ] Judges calibrated or replaced by deterministic checks.
- [ ] Incidents replayed as tests; scorecards stored.

## Red lines
- No "feels better" promotion for agent changes; no cherry-picked runs; no uncalibrated self-judging.

## Related
`testing-strategy` · `poc-validation` · `agent-safety-guardrails` (adversarial cases).
