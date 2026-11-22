---
name: grill-with-docs
description: Stress-test a Yuzu plan against the repo's domain language, code, CONTEXT.md, and ADRs while updating docs as decisions crystallize. Use when the user says `/grill-with-docs`, asks to grill a design with docs, wants decision interrogation, or needs ADR-adjacent planning.
---

# Grill With Docs

Interrogate one decision at a time. Ask a question, provide your recommended answer, and wait for feedback. If the answer can be discovered from the codebase or docs, inspect them instead of asking.

## Inputs

Read lazily:

- `CONTEXT.md` for glossary and domain boundaries.
- `docs/adr/` for existing architectural decisions relevant to the topic.
- Code and docs that implement or describe the plan's domain.

Create files lazily only when there is something real to record.

## During The Session

- Challenge terms that conflict with `CONTEXT.md`.
- Replace vague terms with canonical Yuzu terms.
- Use concrete scenarios that stress boundary cases, permissions, failure modes, and operator-visible behavior.
- Cross-check claims against code when feasible.
- Update `CONTEXT.md` inline when a domain term is resolved.

## CONTEXT.md Format

Keep terms domain-level, not implementation trivia:

```markdown
## Term

Definition in Yuzu language.

- Related concepts: ...
- Avoid saying: ...
```

## ADR Rule

Offer an ADR only when all are true:

- hard to reverse
- surprising without context
- a real trade-off among credible alternatives

ADRs live in `docs/adr/` and are numbered `0001-short-title.md`, `0002-short-title.md`, etc. Use this shape:

```markdown
# ADR-NNNN: Title

## Status

Accepted

## Context

## Decision

## Consequences
```

There is no separate `/adr` workflow initially; this skill is the ADR-adjacent workflow.
