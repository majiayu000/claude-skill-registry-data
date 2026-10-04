---
name: wiki-first-product-management
description: Manage product definition, solution design, architecture, assumptions, and project-level documentation in the GitHub wiki first. Use when defining or refining project goals, architecture, scope, assumptions, decision records, or documentation that should remain visible to human operators and delivery agents.
---

# Wiki-first product management

Use the GitHub wiki as the durable home for project definition.

## Put in the wiki
- product definition
- solution design
- architecture and tradeoffs
- project-level assumptions and rationale
- decision records and clarifications
- project goals and non-goals

## Do not leave only in chat
If a human operator or later agent would need it, write it into the wiki or linkable repo docs.

## Spec ownership
- Spec owns project-level assumptions
- Spec keeps wiki content aligned with the intended product and the merged codebase
- Builder should escalate project-wide ambiguity instead of inventing product truth

## Minimum documentation habit
When a decision changes behavior, scope, or architecture:
1. update the relevant wiki page
2. link the page from the relevant issue or PR
3. summarize the change for reviewers
