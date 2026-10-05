---
name: reason-from-reality
description: Turn a learning, planning, assessment, or improvement request into an evidence-grounded loop of observable targets, uncertainty, action, measurement, and belief updates. Use for long-horizon change or decisions under uncertainty; do not load for a simple fact, rewrite, translation, or routine task without evidence and re-testing.
---

# Reason From Reality

Convert attractive explanations into a small, falsifiable loop. Let observed performance, practical results, and re-tests update the plan.

## Trigger boundary

Load this Skill for long-term learning, exam preparation, skill diagnosis, planning, reflective review, habit or process improvement, and decisions where evidence may overturn the first explanation. Do not load it for an isolated definition, one-time fact lookup, translation, copy edit, or routine task with no meaningful measurement or update.

## The operating stance

- Define an observable target, not a slogan such as “mastery” or “be more disciplined.”
- Separate `FACT`, `JUDGMENT`, `ACTION`, `VALIDATION`, and `UNKNOWN` in the reasoning and output.
- Treat every explanation as a hypothesis with supporting, weakening, and falsifying evidence.
- Prefer repeated representative performance, delayed retrieval, transfer, and process traces over confidence, intention, or generic advice.
- Choose the smallest high-value experiment; change one major variable when attribution matters.
- Preserve conditions that affect interpretation: task type, difficulty, time limit, tools, environment, fatigue, stakes, and prior preparation.
- Do not promise a score, rank, diagnosis, or certainty that the evidence cannot support.

For the detailed definition and boundaries of the civilization-level core, read [canonical-civilization-core.md](references/canonical-civilization-core.md). It is a testable integration of principles, not authority worship.

## Core loop

Run this loop in order, skipping only a step supported by reliable evidence:

```text
Goal → reality → gap → main bottleneck → action
→ measure → delayed/transfer re-test → update
```

1. **Define the target behavior.** Name the task, condition, time window, and success criterion.
2. **Build an evidence ledger.** Record the claim, source, conditions, confidence, and what could weaken it. Use [evidence-and-decision-loop.md](references/evidence-and-decision-loop.md).
3. **Diagnose the first bottleneck.** Distinguish exposure, understanding, retrieval, procedure, transfer, retention, environment, and motivation/energy instead of collapsing them into “ability.”
4. **Choose one action or experiment.** Make it concrete, observable, and small enough to complete.
5. **Measure under comparable conditions.** Use an immediate check plus a delayed or transfer check when the target is durable performance.
6. **Update or switch.** Continue when the leading judgment survives evidence; revise when evidence conflicts; stop or escalate when risk or uncertainty crosses the boundary.

## Learning-specific distinctions

Do not treat these as interchangeable:

```text
Exposure → explanation → cue-free retrieval → procedure
→ transfer to a changed surface → delayed retention
```

AI may explain, generate practice, check work, and schedule a re-test. It must not substitute for the user's own retrieval, derivation, writing, problem solving, or programming when those capabilities are the target. Read [learning-transfer-and-retention.md](references/learning-transfer-and-retention.md) when designing a study loop.

## Safety and uncertainty

Use generic roles and minimum necessary data. Keep old and new evidence conflicts visible. For medical, legal, crisis, high-stakes financial, admission, employment, or personal-safety questions, stop ordinary optimization and follow [safety-and-domain-boundaries.md](references/safety-and-domain-boundaries.md). A confident tone is never evidence.

## Required output

```text
Target outcome:
Facts and conditions:
Leading judgment + confidence:
Bottleneck / competing explanations:
Next action or experiment:
Measure + re-test date:
Update / switch rule:
Unknowns and limits:
```

For a short review, use:

```text
Observed → inferred → do next → measure → update if...
```

## Composition

- Pair with `run-autonomous-workpacks` when the loop should run as a bounded work package.
- Pair with `trace-feature-chain` when the evidence problem is a software or release chain; trace the first mismatch first, then decide and update.
- Do not load all three for a simple syntax fix, translation, rewrite, or isolated factual answer.
