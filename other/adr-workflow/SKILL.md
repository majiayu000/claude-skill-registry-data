---
name: adr-workflow
description: Use when any schema, behavioral, or architectural change is proposed or requested in Athena — new tables, migrations, new endpoints or modes, retrieval-shape changes, new external dependencies or data sources — BEFORE writing any implementation or migration code.
---

# ADR Workflow

## Overview

House rule (CLAUDE.md, non-negotiable): **ADR before migration.** Any schema,
behavioral, or architectural change starts with a draft ADR in Nygard format
in `docs/decisions/`, gets a review pass, is accepted, then implemented.
Never write a migration — or any database/financial-API code — without an
accepted ADR. Several ADRs state this explicitly: "per house rules none may
be written before this ADR is accepted."

## Process

1. **Draft** — next sequential number, file
   `docs/decisions/NNNN-short-kebab-title.md`, `**Status:** Draft`.
   Read the two or three most recent ADRs first (0010, 0011, 0012) and mirror
   their structure and register.
2. **Review pass** — the draft gets a genuine review (ADR-0012's review lives
   in `0012-compare-mode-REVIEW.md`; findings were folded back into the ADR).
   Review findings can be wrong — the maintainer overrides with reasoning.
3. **Accept** — status flips to Accepted in its own `docs(adr): accept …`
   commit before implementation starts.
4. **Implement** — build only what the ADR decided; out-of-scope items wait
   for their own ADR.

## Template (mirrors ADR-0009/0010/0011/0012)

```markdown
# NNNN — Title: What Is Decided, Stated Plainly

**Status:** Draft | Accepted

## Context

Why now, grounded in observed facts (live-validation findings, commit refs,
prior-ADR gates) — not speculation. Name the constraint that drives the
design (e.g. cost, auditability). Cite prior ADRs by number and section.

## Decision

1. **First decision, bold thesis sentence.** Elaboration, including the
   rejected alternative and why it lost.
2. **Second decision.** …
   (Number every decision; later ADRs cite them as "ADR-NNNN §2".)

**Out of scope** (future work, each its own decision): named items, so the
current silence is chosen, not accidental.

## Compliance and Validation   ← include when guarantees need checking

What must be TRUE for the guarantees to hold, and how each is checked —
structural assertions preferred over output-scanning tests.

## Consequences

- **Changes:** what the system gains/alters.
- **Unchanged:** guarantees explicitly NOT reopened (list prior-ADR
  guarantees that carry over).
- **Risk accepted:** named trade-offs, with the remedy stated.
- **Build sequencing:** first increment and what deliberately waits.
```

## Red flags — stop and draft the ADR

- "It's a small migration, I'll write the ADR after."
- "The ADR obviously would be accepted."
- "This is just adding a column/field/endpoint."
- Writing `alembic revision` with no Accepted ADR covering it.

All of these mean: no implementation until an accepted ADR exists.
