---
name: planning-spec
description: Use when a discussed feature or change must be written up as a spec, with agreed test seams, Rails boundaries, and out-of-scope items, and published through the planning tracker, without re-interviewing the user.
license: MIT
---

# Planning Spec

## Purpose

Turn what the conversation and the repository already establish into a spec that an agent or a person can implement without re-deriving the decisions. Synthesize; do not interview. If decisions are missing, stop and run `planning-interview` first.

## Activate when

- the user asks for a spec, PRD, or write-up of a discussed feature
- a `planning-interview` or `planning-wayfinder` effort reached its destination and the result must be specified
- `planning-tickets` needs a spec to slice and none exists

## Repository inspection

- read the glossary and decision records so the spec uses the project's terms and respects recorded decisions;
- inspect the models, schema, routes, jobs, and tests the feature touches;
- identify the owning skill for each touched boundary (route with `skill-manifest.yml` and `router/ROUTING.md`) and read its `## <Domain> changes` contract;
- find prior art for tests of the same kind: request, model, job, or system tests;
- for each touched boundary, find its direct callers and indirect readers (other models, jobs, serializers, other services) and check whether existing tests already cover them.

## Decision rules

1. **Check completeness first.** List the decisions the spec needs. If any is unresolved, name it and hand back to `planning-interview` instead of guessing.
2. **Agree the test seams before writing.** Prefer existing seams and the highest seam that still gives a precise signal; propose new seams only where none fits, as few as possible. Confirm them with the user when available.
3. **Write for behavior, not files.** Describe modules, interfaces, schema changes, and contracts. Leave out file paths and code, which go stale; the exception is a snippet, such as a schema or state table, that states a decision more precisely than prose.
4. **Name the Rails boundaries.** For each touched boundary, name the owning skill, and include the data impact: migrations, backfills, and constraints that change.
5. **Name the regression surface.** For each touched boundary, list what depends on it and whether existing tests already cover that dependent; an uncovered dependent goes in the spec's Notes as a gap to close, not an assumption that it is safe.
6. **Publish through `planning-tracker`** as a `kind: spec` item with the `ready-for-agent` label, after resolving the backend and confirming any remote write.

## Spec template

```markdown
## Problem
What the user faces today, from their point of view.

## Solution
What changes for them, from their point of view.

## User stories
1. As a <actor>, I want <capability>, so that <benefit>.
(Cover every actor and edge case the conversation raised.)

## Decisions
- Modules and interfaces to add or change, and what each hides.
- Schema changes, migrations, backfills, and new constraints.
- API or event contracts.
- Owning skills: <boundary> → <skill>, with any change-contract rules that shape the work.

## Test seams
- The agreed seams, the behavior each proves, and prior art in this repository.

## Out of scope
- What this spec deliberately does not cover.

## Notes
- Open risks, rollout order, references to decision records, and the regression surface: dependents of each touched boundary that existing tests do not yet cover.
```

## Critical invariants

- Never invent a decision to fill a gap in the spec; hand the gap back to `planning-interview`.
- Never publish before the backend is resolved and any remote write is confirmed.
- Test seams are agreed, not assumed; a spec without them is incomplete.
- Never mark a touched boundary's dependents as safe without checking their existing test coverage.

## Reference example

```markdown
## Decisions
- Refund gains line-level entries: a new RefundLine (refund_id, invoice_line_id,
  amount_cents, tax_cents); refunds.amount_cents becomes the sum of its lines.
- Migration adds refund_lines with foreign keys and a unique index on
  (refund_id, invoice_line_id); no backfill, because existing refunds are full-invoice.
- Owning skills: persistence → rails-active-record; constraints → rails-database-engineering;
  permission to refund → rails-authorization.

## Test seams
- POST /refunds request test: creates a partial refund and returns 422 for over-refunds
  (prior art: test/integration/refunds_test.rb).
- Refund#issue! model test: tax per line is preserved for partial refunds.

## Notes
- Regression surface: InvoiceExport reads refunds.amount_cents directly and has
  no test for a refund with multiple lines; add that case before shipping.
```

## Agent review checklist

- [ ] every needed decision is present, or the gap was handed back
- [ ] test seams agreed and listed with prior art
- [ ] owning skills and data impact named for each boundary
- [ ] regression surface named for each boundary, with uncovered dependents listed in Notes
- [ ] no file paths or code except decision-bearing snippets
- [ ] out-of-scope list present
- [ ] published through the resolved tracker backend

## Failure modes

- re-interviewing the user on decisions already made in the conversation
- filling missing decisions with plausible guesses
- a spec that lists files to edit instead of behavior and contracts
- omitting migrations, backfills, or constraints from a data-changing feature
- assuming a boundary's dependents are safe without checking their test coverage
- publishing to GitHub without confirmation

## Verification

Read the published spec back from the tracker. Check that each user story is covered by a decision and that each decision is proved at an agreed test seam.

## Source foundation

Adapted, in this repository's words and with Rails boundaries and data impact added, from the `to-spec` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock). Publishing goes through this repository's backend-neutral `planning-tracker`.
