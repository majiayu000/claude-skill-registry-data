---
name: decision-log
description: Maintain durable records of consequential decisions with context, owner, options, evidence, rationale, consequences, dependencies, and revisit conditions.
---
# Decision Log

Use when a decision will affect multiple teams, future work, commitments, architecture, policy, budget, or operating assumptions.

## Procedure
1. State the decision in one clear sentence and identify the accountable decision owner.
2. Record the context and problem being resolved, including relevant constraints and commitments.
3. Capture the material options considered and the evidence or assumptions that shaped the choice.
4. Record the rationale, including tradeoffs and what was deliberately not optimized.
5. Note consequences, follow-up actions, affected owners, dependencies, and any compatibility or migration impact.
6. Distinguish facts available at decision time from forecasts or judgment.
7. Define revisit triggers such as new evidence, threshold changes, deadlines, incidents, or invalidated assumptions.
8. Link durable artifacts such as specs, ADRs, plans, contracts, research, or task records rather than relying on chat transcripts.

## Decision rules
- A log records decisions, not every conversation.
- Avoid rewriting history when a decision changes; supersede the earlier entry and preserve why.
- The owner of the professional decision should remain visible.
- Confidential material should be referenced or summarized according to access policy.

## Quality gate
A future collaborator can understand what was decided, why it was reasonable with the evidence then available, who owned it, what changed because of it, and what conditions should cause the decision to be reconsidered.