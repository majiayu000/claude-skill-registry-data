---
name: spike-360
description: >
  Interrogate authority before planning a feature, refactor, migration, rewrite,
  backfill, event-sourcing design, dual-write setup, new authoritative store, or
  system-of-record change. Fire whenever a proposal might introduce, move,
  duplicate, or replace authoritative state — or involves event sourcing or
  "event sourced," a "source of truth," "authoritative" data, dual-writes,
  replay, projections, replacing persistence, a new data store, or "design the
  architecture for / rewrite X" — and classify authority before writing any plan
  or reaching for a seam or architecture spike. The five levels: audit-only, read
  projection, dual-written peer, source of truth, replacement runtime; for
  audit-only or read-projection cases, fire just long enough to classify and
  stop, and for dual-written peer and above, require the surface and
  failure-scenario checks first. Triggering is deliberately broad — the skill
  classifies first and stops fast when the level is light. Skip only for a
  localized bugfix with no authority change, or when the authority level is
  already classified, agreed, and its required surface and failure-scenario pass
  is already complete.
---

# Spike 360

Interrogate the premise before you design the architecture.

The failure this prevents: a plan jumps straight to "event-sourced core" and only discovers, three phases in, that "source of truth" changes the entire problem class — new invariants, new failure modes, a migration nobody scoped. The fix is to change the first move from *design the architecture* to *interrogate the premise*.

## Core idea

Before writing any plan, decide **what authority the new system will hold**. That classification — not the design — sets the problem class. Most proposals that sound like "a new system of record" are actually solved by a smaller, lower-authority mechanism — often just a ledger — that the existing source of truth never has to defer to. Find that out first, on purpose, before a single phase or schema is drawn.

## Hard rule

> Classify the authority level before you write any migration plan — and at dual-written peer or above, audit the current read / write / side-effect surfaces before writing it too.

If you catch yourself sketching phases, schemas, or an "event-sourced core" before Gate 2 is answered, stop and answer Gate 2.

## The five gates (in order)

**Gate 1 — Problem narrowing.** What user or business problem actually triggered this? What is the smallest change that solves *only* that? What would be overbuilding?

**Gate 2 — Authority classification (the pivot).** What authority does the new system hold?

- **Audit-only** — it observes; nothing reads it back as truth.
- **Read projection** — a derived view; the old store stays authoritative.
- **Dual-written peer** — written alongside the old store; both claim truth.
- **Source of truth** — other systems now defer to it.
- **Replacement runtime** — it *becomes* the system; the old one is retired.

This ladder is also a reversibility ladder: audit-only and read projection are Easy to undo; dual-written peer, source of truth, and replacement runtime run Costly to One-way door once two systems claim truth or readers depend on the new one. **Those three trigger the heavy checklist (Gates 3-4)** — and a far larger scope than the proposal usually admits. Dual-written peer is in that tier on purpose: two writers means divergence, ordering, and reconciliation risk from day one — one of the most failure-prone designs this skill exists to catch.

**Gate 3 — Current-state audit** (dual-written peer and up). Enumerate, concretely:

- every **reader** and every **writer** of the state being changed
- every **persisted field** and every **external side effect** (emails, webhooks, payments)
- **transient vs resting** state — what is mid-flight vs settled
- **startup / load / backfill** behavior — how state is reconstituted from cold

**Gate 4 — Failure-scenario pass** (dual-written peer and up). For each, does the design survive it?

- crash *before* the write
- crash *after* the write, before the downstream mutation
- crash *after* an external side effect, before the write
- concurrent handlers interleaving across an `await`, async boundary, transaction gap, or retry boundary
- replay from an empty / brand-new log
- replay from a partial or corrupt tail
- legacy import with missing fields
- (dual-written peer) the two stores disagree — which one wins, and when is the divergence detected and reconciled?

**Gate 5 — Stop / Go.**

- If a smaller, lower-authority mechanism solves the Gate 1 problem, **recommend that first** — name it (a ledger, projection, cache, report table, reconciliation view, or no new store at all).
- For a **dual-written peer**, do not approve the path unless the design names the winner rule, drift detection, reconciliation process, ordering key, idempotency boundary, and rollback plan.
- If **source of truth** or replacement runtime is still genuinely wanted, **require explicit approval** and list the new invariants it must guarantee from this day forward.

## Output format

Lead with the authority level — it is the line that must survive skimming, because it decides everything after it. Then add only the gates that change the call. A light classification is a few lines; the heavy checklist (Surfaces / Failure scenarios) appears *only* at dual-written peer and up. Never pad.

**Authority level:** [Audit-only / Read projection / Dual-written peer / Source of truth / Replacement runtime] — [one line: what that means for scope and reversibility].

**Real problem:** [the triggering problem, one sentence] → **Smallest fix:** [the narrowest change that solves only that].

**Overbuild:** [what the current proposal adds beyond the smallest fix — or "none, the proposal is already minimal."]

*Dual-written peer and up only — otherwise omit both blocks:*

**Surfaces at risk:** [the readers / writers / persisted fields / side effects / transient-vs-resting / startup-load-backfill that actually bite — not all of them.]

**Failure scenarios:** [only the ones the design does not yet survive, each with the gap in a phrase. If it survives every applicable scenario, say so.]

**Stop / Go:** [Smallest safe mechanism first, named — ledger, projection, cache, report table, or no new store — or: authority shift approved, with the new invariants listed.]

## How this differs from its siblings

- **take-a-step-back** is the general pre-commit reset ("am I solving the right problem?"). spike-360 is its architecture-specific form: it forces a concrete authority classification and, above a threshold, a failure-scenario pass.
- **blast-radius** sizes a path you have *already chosen*. spike-360 fires earlier and questions whether the path's authority level is even the right one — its verdict can feed straight into blast-radius.
- **recon** — the read-only trace of the current system. spike-360 classifies authority *first*; once the level is settled, recon maps the readers, writers, and contracts the approved shape has to live with, and the plan is written against that map. A light audit-only or read-projection verdict stops spike-360 early but does not excuse the trace: recon still runs if the remaining implementation plan meets its trigger. Gate 3's surfaces pass is the classification-sized sample of that audit, not a replacement for it.
- **phase-0-spike** (an external workflow in `~/.claude/workflows/`, not a skill in this repo) maps seams, contract owners, and rollout invariants *after* you have committed to the refactor — it already assumes a source of truth exists (it asks each analyzer for the "contract owner"). spike-360 runs upstream and decides whether a new source of truth should exist *at all*. Run spike-360 first; only a "source of truth — approved" verdict makes phase-0-spike's seam-mapping worth doing.

## When not to escalate

If Gate 2 lands on audit-only or a read projection that the smallest-fix gate already satisfies, **stop there** — dual-written peer and above do not qualify, since a second writer or a new system of record already carries the heavy invariants. Classify it, say "a ledger or projection is enough — ship it," and skip Gates 3-4 entirely. Running the full crash-replay failure pass on an append-only log nothing reads back is exactly the manufactured gravity this suite warns against. The heavy checklist is *earned* by the authority level, not applied by default.

## Example 1 — source-of-truth creep, caught early

Input: "Let's make the orders subsystem event-sourced so we have a full history and a single source of truth for order state."

Output:

> *Before any event-sourcing design — one classification decides the whole scope here.*
>
> **Authority level:** Source of truth, edging toward replacement runtime — every reader of order state would now defer to the event log, not the orders table. One-way door once they do.
>
> **Real problem:** "We can't tell why an order's status changed." → **Smallest fix:** an append-only `order_events` ledger written beside the existing table for history and audit; the table stays authoritative.
>
> **Overbuild:** Event-sourcing makes the log the source of truth, which drags in replay, projections, and a migration of every reader — none of which the "why did status change?" problem requires.
>
> **Surfaces at risk (if you proceed to source of truth):** every order reader (API, fulfillment, billing), the `status` / `total` persisted fields, the payment-capture side effect, and order-load on startup.
>
> **Failure scenarios not yet survived:** crash after payment capture before the event writes (double-charge on replay); replay from a partial tail (orders resurrect in a stale status).
>
> **Stop / Go:** Ledger first — it solves the stated problem with no new invariants. If a true source-of-truth event log is still wanted, that is a separate, explicitly approved decision that must guarantee idempotent, deduplicated side effects (don't rely on exactly-once external effects — design for at-least-once delivery plus idempotency), deterministic replay, and a backfill for every legacy order. Get that approval *before* any plan is written.

## Example 2 — correctly not escalated

Input: "I want to log every admin permission change to a new table so we have an audit trail."

Output:

> **Authority level:** Audit-only — nothing reads the table back as truth; permissions still live where they live. Easy to undo.
>
> **Real problem:** "We have no record of who changed permissions." → **Smallest fix:** an append-only `permission_audit` row written in the same transaction as the change. That *is* the whole job.
>
> **Overbuild:** none — keep it append-only and resist adding reads against it later. The moment something defers to it for current permission state, re-run this check.
>
> No current-state audit or failure-scenario pass needed: an audit log no one reads back does not carry source-of-truth invariants.

## What success looks like

The operator learns the authority level — and therefore the true scope — in the first line, before a single phase or schema is drawn. A proposal that was about to become an event-sourced rewrite gets resized to a ledger; or, if the larger change is genuinely wanted, it walks in with its new invariants named and approved instead of discovered in phase three.
