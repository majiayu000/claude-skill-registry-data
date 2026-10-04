---
name: extract-design-rationale
description: "Extract defensible design rationale from project notes, logs, specifications, research, and artifacts. Use when a case study shows what was built but not why, needs a constraint-alternatives-decision matrix, must explain rejected options and trade-offs, or needs to connect a UI, product, system, or AI-agent decision to evidence and measurable consequences."
---

# Extract Design Rationale

Turn implementation history into a decision argument. Read `references/rationale-matrix.md`.

## Workflow

1. Inventory candidate decisions in the supplied evidence.
2. Keep only decisions that changed user outcomes, system behavior, risk, cost, delivery, or learning.
3. For each decision, extract:
   - the constraint or problem;
   - the tension between competing goals;
   - the alternatives genuinely considered;
   - why each alternative was rejected or deferred;
   - the final decision and owner;
   - the evidence available at decision time;
   - the observed consequence or metric.
4. Separate contemporary evidence from hindsight.
5. Mark absent alternatives, rationale, ownership, or outcomes as evidence gaps.
6. Rank the records by narrative importance.

Do not invent alternatives to make a decision look rigorous. Do not convert a team decision into sole-designer ownership. Do not claim business alignment without a named goal, constraint, or metric.

## Output

Return:

1. a one-sentence decision thesis;
2. a ranked shortlist of pivotal decisions;
3. one rationale matrix per decision;
4. the strongest visual or artifact to pair with each record;
5. unresolved evidence gaps.

## Example

Input:

```text
Users missed background-agent failures. We considered persistent alerts, a blocking
modal, and an activity timeline. Support logs showed most failures were recoverable.
We shipped the timeline plus a thresholded alert; failed-task recovery rose from 62%
to 84% in the beta.
```

Expected outcome: a matrix naming failure visibility as the constraint, the modal and persistent-alert trade-offs, the selected timeline-plus-threshold model, the support-log evidence, and the 62%→84% recovery result.
