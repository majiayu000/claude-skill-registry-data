---
name: domain-modeling
description: Use when a project needs shared terminology, glossary updates, ADRs, clearer domain language, or when user language conflicts with existing code, ticket, board, project, workflow, or CONTEXT.md terms.
---

# Domain Modeling

Use this to keep the project language sharp while planning or implementing.

## Workflow

1. Look for `CONTEXT.md`, `CONTEXT-MAP.md`, and nearby ADRs.
2. When a term is fuzzy, propose one canonical term and test it with a concrete scenario.
3. When user language conflicts with code or docs, surface the conflict and resolve it before implementation.
4. Update the glossary only when a term is settled.
5. Create an ADR only when the choice is hard to reverse, surprising without context, and the result of a real tradeoff.

## DecisionsAI Fit

- Use board/ticket/workflow names as evidence, not as the glossary by themselves.
- Keep glossary entries free of implementation detail.
- Put implementation decisions in ADRs or workflow artifacts, not in `CONTEXT.md`.
- Prefer project memory sync when the active workflow needs the term later.
