---
name: goal-and-constraints
description: Use at the very start of any new product, feature, project, or decision, before brainstorming, speccing (OpenSpec), or building (Superpowers). Runs a short interview to name the user, their need, and the product context; the goal as a measurable objective function (outcome, not output); the data and evals it depends on; the single top constraint or bottleneck (discovered, not assumed); and the four product risks (value, usability, feasibility, viability), then produces a one-page Goal and Constraint Brief. Use when the user starts scoping something new, asks to define the goal, asks what the constraint or bottleneck is, or runs /goal-discover.
---

# Goal and Constraints

The Why layer of the native-agentic lifecycle: **GOAL (why), then OpenSpec (what), then Superpowers (how).** Expert teams already spec and build well. This skill adds the step before both: name the goal and the one constraint (the bottleneck), so the spec and the build aim at the right target.

Run this before brainstorming, speccing, or building anything new, whether a product, a feature, a project, or a decision. It works at any altitude: frame a whole product's goal, or one effort's goal that ladders up to it.

## What to do

Interview the user briefly (one question at a time is fine), then write a one-page **Goal and Constraint Brief** using `references/brief-template.md`. Ask:

1. **Who, plus context and intent.** Who is this for (the user or customer, and their context)? What product or system does this serve, what state is it in today, and what is the intent: the change in behavior or outcome you are trying to create? Keep it light here; the full personas and behaviors are the `product-model-canvas` skill.
2. **Need.** What unserved need or job-to-be-done are we serving, and what is the real problem (the need behind the need), not the solution that was asked for?
3. **Goal.** What outcome are we really after (for a product: adoption, retention, revenue; for internal work: throughput, cost, time saved), not output (stories, PRs, features shipped)? Push for a measurable objective function, a number, not a vague aim, and how we will know we hit it (the success metric).
4. **Data and evals (AI-native).** What data does this depend on? What do you already have that is proprietary, curated, or labeled; what is missing; and what is the ground truth or eval set that will prove it works? In native-agentic work the data and evals are often both the constraint and the moat, and they become the Learn-phase reinforcement learning environment. Keep this light for non-AI work. (Name the eval set here; the full Eval Plan is the `eval-driven-development` skill.)
5. **Constraint or bottleneck (discover it, do not assume it).** The user often will not know the bottleneck. Guide discovery: map the flow of work from the need to the goal; find where it waits, piles up, or is blocked; classify it (physical, policy, market, or knowledge; data readiness is a common one in AI-native work); if only symptoms show, ask why a few times to reach the core problem; then validate ("if this one thing were removed, would we hit the goal?"). Name the single constraint.
6. **Alignment.** How does this goal ladder up to the product, team, or org goal? Which higher priority does it serve? If it serves none, surface that.
7. **Scope, and right-size the solution.** What is in, and what is explicitly out? Then ask whether this needs an agent at all: does a single prompt or a plain workflow clear the constraint? Prefer the simplest thing that works, and add agentic complexity only when the constraint demands it.
8. **Risks and confidence.** For each of value, usability, feasibility, viability, how confident are you (low, moderate, or high), and why? The lowest-confidence one is your riskiest assumption, and it is what to validate first. Scale this to the effort: a small internal task can collapse to just the riskiest assumption.

Fill the template, save it as `goal-brief.md` in the working project, and show it to the user.

## When to go deeper

If the problem is complex, the constraint is unclear, or the stakes are high, offer the deep pass: read `references/five-focusing-steps.md` and walk Goldratt's Five Focusing Steps, then record the result in the Brief. Do not run the deep pass by default; the lean interview is enough for most work.

## Self-check before you finish

Check the Brief against this rubric, and fix anything that fails:

- The goal is measurable (there is a number or a clear, testable outcome).
- The goal is concrete enough to write at least one pass/fail eval task for it; if you cannot, it is not ready to spec (the full Eval Plan is the `eval-driven-development` skill).
- The solution is right-sized: a prompt or a workflow was considered before an agent, and the chosen complexity is justified by the constraint.
- The top constraint (bottleneck) is a single thing, not a list.
- The need behind the need is distinct from the asked-for solution.
- For AI-native work, the data and evals are named: what exists, what is missing, and the ground truth or eval set that proves it works.
- The alignment ladders up to a higher goal (or the misalignment is called out).
- The four product risks are rated (value, usability, feasibility, viability), and the riskiest assumption is named.
- The user (who), the product context, and the need are named, and the constraint was discovered (flow of work mapped and validated), not assumed.

## The constraint moves

This is dynamic. Break a constraint and a new one appears elsewhere (that is why the deep pass ends with *repeat*). Do not assume last cycle's constraint still holds: re-run this pass at the start of each cycle, and balance the effort to the *current* constraint rather than optimizing every dimension at once. The Brief is a living artifact, revisited, not written once.

## Phase state (for the GOAL status-line HUD)

If the user runs the GOAL status-line HUD (`docs/statusline.md`), keep it in sync. At the start of this pass, create or update `.goal/state.json` in the working project:

```json
{ "phase": "Discover", "project": "<the project folder name>" }
```

When you hand off to the next phase (Specify / OpenSpec), set `phase` to `Specify`. It is a small, harmless file; if the user has not set up the HUD, it simply sits unused.

## Hand off

The Brief is the input to the rest of the lifecycle: it feeds OpenSpec (the What) and Superpowers (the How). Point the user there next.

See `references/examples/` for two worked examples in different domains: `manufacturing-brain.md` (a factory) and `agentic-triage.md` (an AI-native multi-agent product). The same constraint logic runs both.
