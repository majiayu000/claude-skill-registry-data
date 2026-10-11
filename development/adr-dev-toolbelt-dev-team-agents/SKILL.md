---
name: adr
description: Architecture Decision Records — MADR format.
---

# Architecture Decision Records (ADR)

ADRs document significant architectural decisions — the context, what was decided, why, and what was considered and rejected.

## File Location

```
docs/development/adrs/
  0001-database-choice.md
  0002-api-design-approach.md
  0003-authentication-strategy.md
```

## MADR Format

```markdown
# [Short title of the decision]

**Status**: [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Date**: YYYY-MM-DD
**Deciders**: [names or roles involved]

## Context

[Describe the issue motivating this decision, including forces at play: technical, political, social, project constraints. Be factual — no judgment yet.]

## Decision

[State the decision in active voice: "We will use X because..."]

## Rationale

[Explain why this option was chosen over the alternatives. Link to evidence, benchmarks, or constraints that drove the decision.]

## Alternatives Considered

### Option A — [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

### Option B — [Name]
- **Pros**: ...
- **Cons**: ...
- **Why rejected**: ...

## Consequences

**Positive**: [What becomes easier or possible]
**Negative**: [What becomes harder, what debt is accepted]
**Risks**: [What could go wrong, and how to mitigate]
```

## Check Before Creating

**Before creating anything**, list the existing ADR titles and check whether the decision is already covered:

```bash
bash .dev-team-agents/scripts/new-adr.sh --list
```

`--list` prints the titles and creates nothing. Use it rather than a glob of your own: ADR filenames exist under two schemes (the historical `adr-NNN-slug.md` and the current `NNNN-slug.md`), the script is the single place that knows both, and a hand-written glob that matched only the historical one is exactly why this check silently returned an empty list for every ADR that existed.

- **Same decision, not yet decided** (still `Proposed`, or genuinely still open) → edit that file, do not create a new one.
- **Same decision, already `Accepted`, and this is a reversal** → create a new ADR, then set the old one's status to `Superseded by ADR-XXX` and link forward.
- **Related but distinct decision** (e.g. this one narrows or extends an existing ADR without reversing it) → create a new ADR and cross-reference the related one in `## Context`.
- **Genuinely new topic** → create a new ADR.

This check applies regardless of which command or agent triggers ADR creation (`/devteam:adr`, `/devteam:learn`, `software-architect` acting on the CLAUDE.md trigger) — each is a separate entry point into the same registry, and none of them can see what another already wrote without this step.

## Creating an ADR

Use the script to auto-number and scaffold the file — it also prints existing ADR titles as a mechanical reminder of the check above:

```bash
bash .dev-team-agents/scripts/new-adr.sh "title of the decision"
```

This creates `docs/development/adrs/NNNN-title-slug.md` — four digits, no `adr-` prefix — with the MADR template pre-filled. Fill in the generated file and change the status from `Proposed` to `Accepted`.

## When to Write an ADR

Write an ADR when the decision:
- Is hard to reverse (database engine, auth strategy, monolith vs microservices)
- Affects multiple components or teams
- Has non-obvious reasoning that future developers will question
- Involves a significant tradeoff

Skip ADRs for: library versions, code style rules, trivial configuration.

## Status Lifecycle

`Proposed` → `Accepted` → (if superseded) `Deprecated` / `Superseded by ADR-XXX`

When superseding an ADR, update the old one's status and link to the new one.

## Tips

- Keep it short — 1-2 pages max
- Write it at decision time, not after implementation
- "We will" not "We should" — ADRs record decisions, not recommendations
- Link ADRs from `CLAUDE.md` or `development/architecture.md` so they're discoverable
