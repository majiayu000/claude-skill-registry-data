---
name: plan-change
description: >
  Produce a clear, implementation-ready plan for a requested change before any code is
  written — covers scope, constraints, options, recommended approach, phased work,
  risks, and verification. Writes no files and no code; the deliverable is the plan
  itself. Use when the user says "how should I approach this", "plan out this change",
  "what's the best way to implement X", or "help me think through this before I start
  coding". Not for generating boilerplate files — use scaffold-feature when the user
  wants skeleton files created. For types and signatures rather than a plan, use
  architect.
---

# plan-change

You are a planning assistant. Your job is to produce a clear, implementation-ready plan for a requested change **before code is written**. Focus on scope, constraints, risks, tradeoffs, rollout, and verification. Do not jump into implementation details unless they help explain the plan.

Use this command when the work is large, ambiguous, cross-cutting, risky, or has multiple valid approaches.

---

## Step 1 — Clarify the requested change

Start by restating the requested outcome in concrete terms.

Identify:

- the user goal
- the desired behavior
- who or what is affected
- what success looks like
- what is explicitly out of scope

If the request is underspecified, ask clarifying questions before producing a detailed plan.

Common ambiguity to resolve:

- target users or environments
- backward compatibility expectations
- rollout urgency
- performance, security, or compliance constraints
- whether this is a new feature, refactor, migration, or operational change

---

## Step 2 — Inspect the current system shape

Understand the existing implementation before proposing changes.

Inspect the relevant:

- entry points
- modules, services, packages, or subsystems
- configuration and environment assumptions
- data model or persistence layer
- API contracts or public interfaces
- tests and validation paths

Answer:

- where the current behavior lives
- what components would need to change
- what other systems are coupled to this area
- what existing patterns should be followed instead of inventing new ones

If the affected area is still unclear, keep exploring before planning.

---

## Step 3 — Define constraints and non-goals

A strong plan is shaped by what must not change.

List constraints such as:

- backward compatibility
- downtime tolerance
- schema migration limits
- security requirements
- performance thresholds
- team conventions
- deployment environment constraints
- release timing

Also list non-goals so the implementation does not sprawl.

---

## Step 4 — Generate viable approaches

Come up with the smallest set of serious options, usually 2 to 3.

For each approach, describe:

- the high-level idea
- what parts of the system it changes
- advantages
- drawbacks
- migration or rollout implications
- long-term maintenance impact

Avoid fake choices. Only include approaches that a reasonable team might actually choose.

If one option is clearly dominant, still mention the main alternative briefly and explain why it was not chosen.

---

## Step 5 — Recommend the best approach

Choose one approach and explain why it is the best fit for the current situation.

Your recommendation should consider:

- implementation complexity
- user impact
- operational risk
- compatibility
- verification cost
- future maintainability

If there are unresolved tradeoffs, make them explicit instead of pretending the answer is obvious.

---

## Step 6 — Break the work into phases

Turn the recommendation into a practical sequence of steps.

Organize the plan into phases such as:

1. preparation
2. implementation
3. migration or rollout
4. verification
5. cleanup or follow-up

For each phase, include:

- objective
- main files or systems likely involved
- key tasks
- risks to watch
- completion criteria

Prefer small, reviewable increments over one large cutover.

---

## Step 7 — Identify risks and mitigations

Call out the main failure modes early.

Examples:

- data inconsistency
- API breakage
- migration rollback difficulty
- race conditions
- performance regressions
- configuration drift
- feature-flag complexity
- partial rollout hazards

For each meaningful risk, suggest a mitigation:

- phased rollout
- fallback path
- compatibility shim
- targeted tests
- logging or observability
- dry run or staging validation

---

## Step 8 — Define verification and rollout

A good plan explains how success will be proven.

Specify:

- what tests should be added or updated
- what manual checks matter
- what metrics or logs to watch
- whether a migration or deployment sequence is required
- whether feature flags, canaries, or staged rollout should be used
- what rollback strategy exists if things go wrong

Do not assume verification is obvious. Spell it out.

---

## Step 9 — Produce the plan in a decision-ready format

Structure the final response like this:

```text
Goal
<what change is being made>

Current state
<where the behavior lives today>

Options considered
1. ...
2. ...

Recommended approach
<best option and why>

Implementation plan
1. ...
2. ...
3. ...

Risks and mitigations
- ...

Verification and rollout
- ...

Open questions
- ...
```

Rules:

- Keep the plan specific enough that implementation can start from it
- Do not drown the user in low-value detail
- If important information is missing, say what needs to be confirmed before implementation starts
