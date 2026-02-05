---
name: "architecture-decision-review"
description: "Framework for evaluating architectural decisions and generating high-quality Architecture Decision Records (ADRs)."
---

# Architecture Decision Review & ADR Generator

## Purpose

Use this skill to:

- Evaluate proposed architectural choices in a structured way.
- Make trade-offs explicit and reviewable.
- Generate clear, maintainable Architecture Decision Records (ADRs).
- Prevent “mystery decisions” and institutional memory loss.

---

## When to Use

- New services, major components, or infrastructure patterns.
- Significant changes to data models, consistency guarantees, or integration patterns.
- New technology adoption (frameworks, databases, messaging systems).
- Reversals of prior decisions (deprecating or replacing an approach).

---

## Decision Review Workflow

1. **Clarify the problem and context**
   - What exact problem is this decision trying to solve?
   - What constraints exist: latency, throughput, reliability, cost, compliance, team expertise, deadlines?
   - What is explicitly **out of scope** for this decision?

2. **Enumerate meaningful alternatives**
   - List at least 2–3 viable options, including “do nothing” or “minimal change”.
   - For each, summarize how it would address the problem.

3. **Assess options against quality attributes**
   For each option, evaluate:

   - Reliability and availability
   - Performance and scalability
   - Security and compliance
   - Operability (monitoring, debugging, deployment)
   - Developer experience and velocity
   - Cost (short-term and long-term)
   - Risk and reversibility

4. **Identify risks and unknowns**
   - What assumptions are you making?
   - What proof (spikes, benchmarks, prior art) would de-risk the choice?
   - What is the blast radius if the decision is wrong?

5. **Make the decision explicit**
   - Choose one option (or combination).
   - Capture rationale: why this over the others?
   - Capture expected lifetime: is this a tactical or strategic decision?

6. **Define follow-ups and guardrails**
   - What needs to be monitored to validate the decision?
   - What metrics or events would trigger reconsideration?
   - What migration or rollback path exists?

---

## ADR Template

When generating an ADR, use this structure:

```text
ADR-XXX: <Short, imperative title>
Status
Proposed | Accepted | Deprecated | Superseded by ADR-YYY

Context
Problem we are solving.

Background and existing constraints.

Relevant historical context or prior ADRs.

Decision
The choice we are making.

Scope and boundaries.

Key assumptions.

Consequences
Positive
Benefits and why they matter.

Negative / Risks
Costs, trade-offs, and potential pitfalls.

New failure modes introduced.

Alternatives Considered
Option A: summary + why rejected.

Option B: summary + why rejected.

“Do nothing”: impact of not changing.

Implementation Notes
High-level integration points and interfaces.

Migration or rollout strategy.

Monitoring, observability, and testing considerations.

Follow-ups
Experiments, spikes, or measurements to run.

Triggers for re-evaluating this decision.
```

## Review Heuristics

Use these questions to sanity-check decisions:

- Is this **as simple as possible**, but not simpler, for current requirements?
- Is the decision **reversible**? If not, are we appropriately cautious?
- Are we solving today’s problem or an imagined future one?
- Will future engineers understand and respect this decision just from the ADR?

---

## Examples of Good Prompts

- “Use the architecture decision review framework to evaluate these two options and generate an ADR.”
- “Given this design doc, produce an ADR that captures the main decision and trade-offs.”
- “Compare microservice vs. modular monolith for this case using the framework, then recommend one and draft an ADR.”
