---
name: plan-mode-clarify
description: Clarify an ambiguous request. Use when missing meaning, scope, or success criteria changes the next step; ask only what context cannot resolve.
license: MIT
---

# Clarify

Resolve the ambiguity that matters to the next decision. Do not turn a small request into an interview.

1. Read the request, history, and project instructions. Separate requirements from inference. Identify ambiguities whose answers change scope, behavior, or result.
2. Resolve what you can from existing evidence. For each remaining ambiguity, name the competing interpretations and the consequence of choosing each. Do not ask about preferences that can be decided safely during the work.
3. Ask the fewest targeted questions needed to proceed. Offer concrete options when useful. Continue independent read-only work while waiting.
4. Return a brief working interpretation: goal, constraints, success criteria, resolved assumptions, and the questions still blocking a choice. Stop once the next action can be chosen without inventing a requirement.

Clarification does not authorize implementation or expand the user's scope. If no material ambiguity remains, state the working interpretation and proceed with the task the user actually requested.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
