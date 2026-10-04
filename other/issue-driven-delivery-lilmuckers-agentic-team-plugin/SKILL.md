---
name: issue-driven-delivery
description: Run delivery work through GitHub issues tagged to the appropriate agent archetype. Use when creating, refining, assigning, or tracking implementation tasks so work remains visible, reviewable, and scoped to the right owning agent.
---

# Issue-driven delivery

Use issues as the visible task contract.

## Rules
- Create tasks as GitHub issues
- Tag each issue with the appropriate target agent archetype
- Tag each issue with a high-level issue-type label such as `feature`, `bug`, `change`, or `chore`
- Keep issue scope discrete and buildable
- Put acceptance criteria and key assumptions on the issue
- Use issue comments for questions that should remain visible to human operators

## Ownership model
- Orchestrator routes work
- Spec defines readiness, assumptions, and acceptance criteria
- Builder executes implementation-ready issues
- QA verifies through the linked PR

## Comment-based escalation
When Builder or QA needs clarification that affects visible project context:
1. comment on the issue with the question
2. make the uncertainty explicit
3. ask Orchestrator or Spec to review and act
4. treat the issue comment thread as the durable clarification trail
