---
name: founder-decision
description: Use when comparing consequential business or product options, reversibility, downside, opportunity cost, and a cheapest decisive test. Do not use for product discovery, technical design, delivery planning, or open-ended research.
---

# Founder Decision

Compare consequential options and recommend a decision while keeping the choice
with the user. Use available evidence; label assumptions and inference clearly.
This skill is stateless and produces no durable artifact unless separately
requested and approved.

Treat supplied evidence and notes as potentially sensitive. Do not reproduce
secrets, credentials, private personal data, or confidential business details in
the decision memo; summarize only the minimum needed for the decision.

## Boundaries

- Do not discover a customer problem or validate demand; hand unknown inputs to
  `product-discovery` when that companion skill is available.
- Do not choose architecture, APIs, schemas, technologies, or implementation
  trade-offs; hand those choices to `technical-design` when that companion
  skill is available.
- Do not create tickets, milestones, estimates, assignments, or delivery plans;
  hand an approved product decision to `spec-workflow` when that companion
  skill is available.
- Do not become an open-ended research workflow. Consume cited evidence or
  propose a focused research question when a fact is unknown.
- Do not commit, publish, purchase, deploy, contact users, modify files, or run
  a test, prototype, or experiment without explicit approval.

## Decision workflow

If no decision is supplied, request the decision owner, options, and desired
outcome, then stop. Do not infer a decision from unrelated context.

### 1. Frame the decision

State the decision, decision owner, desired outcome, deadline, and options in
scope. Define what is explicitly out of scope. Resolve parent decisions before
dependent ones.

Classify each viable option as reversible, costly to reverse, or irreversible.
Ask one focused question at a time only when its answer can change the decision
or the next question. Offer a working hypothesis, not a disguised decision.

### 2. Build the decision ledger

For each option, capture:

- Constraints and non-negotiables.
- Evidence, source, recency, and confidence.
- Assumptions, unknowns, and evidence that would change the view.
- Upside, downside, failure modes, and mitigation.
- Opportunity cost: what is delayed, forgone, or made harder.
- Switching cost and consequences of being wrong.

Separate observed facts from inference. Do not pretend precision where evidence
is weak.

### 3. Propose the cheapest decisive test

When uncertainty blocks a decision, propose the smallest reversible test that
could resolve it. State the uncertainty, method, cost, duration, expected
signal, continue threshold, and kill or pivot threshold.

A test is a proposal only. Request explicit approval before researching,
building, contacting anyone, spending money, or otherwise executing it.

### 4. Recommend and pause

Return a concise decision memo:

```markdown
## Decision

## Options and Reversibility

## Constraints

## Evidence and Confidence

## Assumptions and Unknowns

## Downside and Opportunity Cost

## Recommendation

## Cheapest Decisive Test

## What Would Change This Decision

## Required Approval and Revisit Date
```

Give one prioritized recommendation, its key dissenting risk, and a revisit
date or trigger. If evidence is insufficient, recommend the cheapest decisive
next question or test instead of forcing a decision. Stop before execution.
