---
name: planning-tickets
description: Use when a spec, plan, or conversation must be broken into tracer-bullet tickets, each a vertical slice that fits one agent session, with explicit blocking edges, published through the planning tracker.
license: MIT
---

# Planning Tickets

## Purpose

Break agreed work into **tickets**: vertical slices that each cut a narrow but complete path through every layer they touch, can be verified on their own, and fit in one fresh agent session. Every ticket declares the tickets that **block** it, so the frontier of startable work is always computable.

## Activate when

- a spec or plan is ready to implement and is larger than one session
- the user asks for tickets, issues, a breakdown, or a work plan
- a wide refactor such as a column rename must be sequenced safely

## Repository inspection

- read the spec (from the tracker or a path the user gave) and the conversation;
- read the glossary and decision records so tickets use the project's terms;
- inspect the code each slice touches, and look for **prefactoring** that would make the change easy;
- check how the repository runs migrations and deploys, since that decides how schema changes are split.

## Decision rules

1. **Slice vertically.** A Rails slice usually runs from migration and model through route, controller or job, and view or API, to its tests. It is demoable or verifiable alone. Never ship one layer across all features as a ticket.
2. **Prefactor first.** If a refactor would make the change easy, make it the first ticket and block the feature slices on it.
3. **Size each ticket to one fresh session.** Split any ticket that needs more context than one session holds.
4. **Wire blocking edges honestly.** A ticket is blocked only by tickets that truly gate it. Tickets with no blockers start immediately.
5. **Sequence wide refactors as expand–contract.** When one mechanical change fans across the codebase (renaming a column, changing a shared interface), no vertical slice can land green. Instead:
   - **expand**: add the new form beside the old (a new column written alongside the old one, or a new method delegating to the old);
   - **migrate**: move callers in batches sized by blast radius (per engine, directory, or model family), each batch its own ticket blocked by the expand;
   - **contract**: remove the old form in a final ticket blocked by every batch.
   For schema changes, keep each deploy compatible with the running code, following `rails-database-engineering`.
6. **Quiz the user on the breakdown** before publishing: granularity, blocking edges, and any merges or splits. Iterate until they approve.
7. **Publish through `planning-tracker`** in dependency order (blockers first), then wire blocking edges, with the `ready-for-agent` label. Never close or rewrite the parent spec.

## Ticket template

```markdown
## What to build
The end-to-end behavior this ticket makes work, from the user's point of view.

## Acceptance criteria
- [ ] Observable behavior 1, proved at <agreed test seam>
- [ ] Observable behavior 2

## Blocked by
- <ticket title, linked>, or "None; can start immediately"
```

Leave out file paths and code; they go stale. Keep a snippet only when it states a decision more precisely than prose.

## Critical invariants

- Every ticket is a vertical slice, except the explicit expand, migrate, and contract steps of a wide refactor.
- Every blocking edge points to an existing ticket, and the graph has no cycles; validate local trackers with the tracker script.
- No ticket is published before the user approves the breakdown.

## Reference example

Tickets for "rename `invoices.total` to `invoices.total_cents`" and "partial refunds":

```text
1. Add invoices.total_cents written alongside total          Blocked by: none           (expand)
2. Read total_cents in billing models and serializers        Blocked by: 1              (migrate)
3. Read total_cents in reports and exports                   Blocked by: 1              (migrate)
4. Drop invoices.total                                       Blocked by: 2, 3           (contract)
5. Support staff refund selected invoice lines (end to end)  Blocked by: 2
6. Over-refund attempts are rejected with a clear 422        Blocked by: 5
```

Frontier after publishing: ticket 1 only.

## Agent review checklist

- [ ] every ticket is a vertical slice or an explicit expand/migrate/contract step
- [ ] prefactoring sequenced first where it helps
- [ ] each ticket fits one session and has checkable acceptance criteria
- [ ] blocking edges are real, present, and acyclic
- [ ] user approved the breakdown before publishing
- [ ] published in dependency order through the resolved backend

## Failure modes

- horizontal tickets such as "all migrations" or "all controllers"
- a wide rename as one ticket that breaks every caller at once
- blocking edges added "to be safe", which starve the frontier
- tickets too large for one session, or with acceptance criteria nobody can check
- publishing before the user reviewed the breakdown

## Verification

After publishing, compute the frontier (for local Markdown, `ruby scripts/tracker.rb frontier --root <root> --parent <spec id>` from the `planning-tracker` skill) and confirm it lists exactly the tickets meant to start first.

## Source foundation

Adapted, in this repository's words and with Rails slices and schema expand–contract, from the `to-tickets` skill in https://github.com/mattpocock/skills (MIT License, Copyright (c) 2026 Matt Pocock). Publishing goes through this repository's backend-neutral `planning-tracker`.
