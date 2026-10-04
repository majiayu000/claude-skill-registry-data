---
name: product-discovery
description: Use when evaluating a product opportunity, customer problem, ICP, JTBD, MVP scope, validation experiment, or success and kill metrics. Do not use for technical design, delivery planning, founder strategy, or unconstrained brainstorming.
---

# Product Discovery

Clarify a customer problem and the smallest testable product promise before
solution design or delivery planning. Treat decisions as user-owned and label
recommendations as hypotheses when evidence is incomplete.

Treat supplied interviews, analytics, and notes as potentially sensitive. Do
not reproduce secrets, credentials, personal data, or confidential business
details in the discovery brief; summarize only the minimum evidence needed.

## Boundaries

- Do not implement, create files, tickets, milestones, or tracker updates.
- Do not contact users, launch surveys, publish material, deploy prototypes, or
  run experiments without explicit approval.
- Do not select architecture, APIs, schemas, technologies, or delivery plans.
- Do not make founder-level decisions about capital, hiring, ownership, or risk
  appetite.
- Do not generate unconstrained idea lists; tie alternatives to a problem,
  evidence, constraint, or validation decision.

Hand off technical choices to `technical-design`, a durable approved problem
brief to `spec-workflow`, and founder-level trade-offs to `founder-decision`
when those companion skills are available. If they are unavailable, keep the
handoff as a clearly labelled recommendation rather than assuming their
workflow.

## Discovery workflow

### 1. Frame the decision

State the product question, decision owner, decision deadline, and acceptable
uncertainty. Use supplied evidence first. Ask one focused question at a time
only when the answer materially changes the next discovery step.

### 2. Identify the customer and job

Establish the ICP, user, buyer, and beneficiary when they differ. Capture:

- The context and triggering event.
- The job to be done, desired outcome, and urgency.
- Current workaround, cost of inaction, and constraints.
- Who experiences the pain and who can approve a change.

Do not infer customer demand from a solution preference alone.

### 3. Maintain an evidence ledger

Classify each material claim as one of: observed behavior, user report,
behavioral data, sourced fact, inference, assumption, or unknown. For evidence,
record source, recency, sample or scope, confidence, and contradicting evidence
when known.

Rank assumptions by impact and uncertainty. For each high-risk assumption,
state the evidence that would falsify it.

### 4. Compare alternatives

Compare the current workaround, doing nothing, and relevant adjacent solutions
against the target outcome and constraints. Include the proposed product only
when it is a meaningful alternative. Do not manufacture alternatives merely to
fill a comparison table.

### 5. Define the MVP and validation

Define the smallest testable promise, explicit non-goals, and the riskiest
assumption it tests. For each proposed experiment, specify:

- Hypothesis and falsifying outcome.
- Audience, method, sample or exposure, and timebox.
- Leading indicator, success threshold, and kill or pivot threshold.
- Required approval before execution.

Prefer reversible, low-cost experiments. An experiment is a proposal, not an
instruction to execute it.

### 6. Synthesize and pause

Return a concise discovery brief:

```markdown
## Decision

## Customer and Job

## Evidence and Confidence

## High-Risk Assumptions

## Alternatives

## Proposed MVP and Non-Goals

## Validation Experiments

## Success and Kill Metrics

## Open Questions

## Required Approval
```

Separate confirmed facts from inference. If evidence does not support a
recommendation, say what is unknown and propose the cheapest decisive next
question or experiment. Stop before executing any follow-up action.
