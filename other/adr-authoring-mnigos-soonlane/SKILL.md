---
name: adr-authoring
description: Creates or updates Soonlane architecture decision records under docs/decisions. Use when the user asks for an ADR, decision record, architecture decision, accepted/proposed decision, or when domain-model work produces a hard-to-reverse architectural trade-off.
---

# ADR Authoring

Use ADRs for durable architecture decisions, not routine implementation notes.

## Related Skills

- Use `domain-model` first for module ownership, Effect layering, package boundaries or language-heavy decisions.
- Update `UBIQUITOUS_LANGUAGE.md` (see `domain-model/GLOSSARY-FORMAT.md`) when the ADR introduces or changes domain terms.
- Use `.agents/skills/domain-model/ADR-FORMAT.md` for the ADR format.

## When An ADR Qualifies

Create or update an ADR only when all are true:

- The decision is hard to reverse.
- The decision would be surprising without context.
- The decision involved a real trade-off.

## Flow

1. Read existing ADRs in `docs/decisions`.
2. Read `.agents/skills/domain-model/ADR-FORMAT.md`.
3. Read `.agents/skills/domain-model/CONTEXT-FORMAT.md` when the ADR touches context boundaries.
4. Read `UBIQUITOUS_LANGUAGE.md`, `PRODUCT.md`, `ARCHITECTURE.md` and code patterns relevant to the decision.
5. If `CONTEXT-MAP.md` exists, read it and the relevant context docs it points to.
6. Choose the next number by scanning all `docs/decisions/*.md` files and parsing the leading ADR number.
7. Use `docs/decisions/NNNN-short-slug.md`.
8. Match the existing repo style: title, status, date, context, decision, consequences, and related links when useful.
9. Link to `UBIQUITOUS_LANGUAGE.md` instead of duplicating large term tables.
10. Mark new ADRs `Proposed` unless the user says the decision is accepted.
11. Add the ADR to the decision table in `ARCHITECTURE.md`.

## Rules

- Keep ADRs concise but complete enough for a future agent to understand why.
- Record rejected alternatives when they would otherwise be suggested again.
- Include concrete dates, PRs and affected modules or packages when they clarify scope.
- Use `docs/decisions`, not generic `docs/adr`.
- Decisions already recorded in `PRODUCT.md` are final; an ADR may cite them but never reopens them.
- Do not create GitHub issues from an ADR unless the user asks.
- Do not commit ADR changes unless explicitly asked.
