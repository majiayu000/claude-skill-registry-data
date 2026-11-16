---
name: design-interview
description: Clarify an ambiguous feature or product idea before committing to a design. Use when multiple plausible interpretations or trade-offs materially affect implementation.
---

# Design Interview

Help the user make the important decisions; do not turn every request into a lengthy interview.

1. Restate the goal in concrete user-visible terms and identify what is already known.
2. Ask one focused question at a time, starting with the decision that most changes scope or architecture.
3. Explore the primary user, core workflow, success criteria, constraints, edge cases, and what is explicitly out of scope.
4. Offer a small number of meaningfully different approaches with trade-offs. Include the simplest viable option.
5. Challenge contradictions, hidden assumptions, and features that do not support the goal. Explain why rather than merely disagreeing.
6. Stop when the remaining uncertainty can safely be handled as an implementation detail.

Deliver a concise decision record: problem, user/workflow, agreed behavior, non-goals, constraints, unresolved questions, and acceptance criteria. Do not begin implementation until the decisions that affect it are settled or the user explicitly asks for a best-effort assumption.
