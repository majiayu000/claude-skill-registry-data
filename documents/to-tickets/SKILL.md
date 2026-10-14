---
name: plan-mode-to-tickets
description: Break an approved epic, spec, PRD, or plan into executable tickets. Use when the user needs small deliverable slices with explicit acceptance criteria and real blocking dependencies.
license: MIT
---

# To Tickets

Make **tickets** a contributor can pick up and verify without reconstructing the conversation.

1. Read the source and relevant repo context. Extract outcomes and constraints. Mark unapproved assumptions as open decisions.
2. Slice by demonstrable behavior or necessary enabling change, not arbitrary layers. Keep each ticket small enough for one focused pass. For cross-cutting migrations, use an expand, migrate, contract sequence that keeps intermediate states workable.
3. Give every ticket a clear title, source/parent reference, delivered behavior, scope boundary, acceptance criteria, verification method, and only the blockers that genuinely prevent starting it. State “none” when it can start now. Include a separate decision ticket only if its answer blocks implementation.
4. Check every source requirement: no omitted outcome, duplicate ticket, circular dependency, or acceptance criterion dependent on unstated work. Show dependency order and startable tickets.

Deliver ticket drafts for review. Each is ready when its result is observable and blockers are explicit. Create or update tracker issues only with user authorization.

Record this output in `docs/plans/` per the [doc system](../references/doc-system.md), delegating the write to a subagent.
