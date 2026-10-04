---
name: ln-handoff
description: "Capture volatile session state into a structured handoff document before context is lost. Use when ending a session, switching threads, approaching context limits, or at any juncture the user chooses."
argument-hint: "[optional: path for handoff file, default `HANDOFF.md`]"
---

# Ln Handoff

Capture what lives in chat but not on disk. Git can reconstruct file changes. But a half-formed scope card, a spike 60% through its investigation, a plan discussion that hasn't hit `memory/PLAN.md` — those are gone on compaction.

The handoff must let a new thread act immediately without asking clarifying questions.

`HANDOFF.md` is derivative and temporary. It is never canonical planning state: durable truth belongs in `memory/SPEC.md` and `memory/PLAN.md`, prepared multi-card execution queues may live temporarily in `memory/CARDS.md`, and retired history belongs only in `docs/archive/PLAN_HISTORY.md`.

Default to one `HANDOFF.md` at the workspace root. Overwrite or replace the prior handoff; do not create numbered handoff archives, breadcrumb files, or completion tombstones without explicit permission.

## Procedure

### 1. Identify phase

Which `ln-*` skill was most recently active? Where in the flow is the work?

```
grill → spec → plan → [design] → [oracles] → scope → [spike] → build → review → [refactor] → [sync]
```

Be precise about state:

- **Last completed skill**: which skill finished most recently, and what did it produce?
- **Current skill**: what is executing right now? (Often `ln-handoff` itself — say so.)
- **Completion state** of each: not started / in progress / done.

### 2. Capture in-flight state

This is the critical step. Scan the conversation for volatile artifacts — information discussed but **not yet persisted to disk**:

- **Scope cards** from `ln-scope` — target behavior, boundary crossings, acceptance criteria
- **Queued scope cards** already persisted in `memory/CARDS.md` — capture only what is still volatile about them: which card is next, whether the queue is still valid, and any card-level corrections that have not been written back yet
- **Plan drafts** from `ln-plan` — slice lists, ordering decisions, dependency reasoning not yet in `memory/PLAN.md`
- **Design outputs** from `ln-design` — alternative module shapes considered, the chosen shape, and rejected tradeoffs
- **Oracle design outputs** from `ln-oracles` — O/R/C assessment, selected oracle families, per-frontier or per-slice verification approaches, acknowledged blind spots, and whether verification design is complete / pending / stale relative to the code
- **Spike state** from `ln-spike` — the question, what was tried, partial findings, verdict if reached
- **Review findings** from `ln-review` — **ALL findings, not just the one being acted on.** Review debt is critical context. Name every finding, its status (addressed / in-progress / deferred), and any remaining implications. A fresh thread that only knows about the active finding will lose track of deferred review debt.
- **Refactor state** from `ln-refactor` — commit sequence, target structure, and any constraints on safe ordering
- **Grill insights** from `ln-grill` — constraints surfaced, decisions reached
- **Decisions and assumptions** discussed but not yet in `memory/SPEC.md`
- **Evidence that informed diagnoses** — concrete proof points (API responses, test output, log lines, specific data) that caused the investigation to shift direction or a hypothesis to be confirmed/rejected. Without this, a new thread inherits conclusions but not the reasoning, and may re-investigate or contradict settled evidence.
- **Failed attempts or dead ends** that affect what to try next
- **Pending canonical reconciliation** — if a build, spike, or refactor changed reality but the follow-up `memory/SPEC.md` / `memory/PLAN.md` update has not happened yet, capture exactly what still must be reconciled

Reproduce these with full fidelity — preserve the structure (scope card format, spike verdict format, etc.), not just a summary. The natural failure mode is to capture what you're actively working on and drop everything else. Resist this: scan the **entire** conversation, not just the recent context.

### 3. Snapshot persisted state

What IS on disk:

- **Git**: branch, recent commits (last 3-5), dirty/staged files
- **Test status**: run the verification command if fast (<30s), otherwise note last known status
- **Artifacts**: which of `memory/SPEC.md`, `memory/PLAN.md` exist? Are they current relative to what was discussed in conversation, or stale?
- **Derivative queues**: does `memory/CARDS.md` exist, and if so, is it still the live execution queue or already stale?
- **Mini-sync triggers**: did manual verification happen, did frontier status change, or did residual risk surface without a doc update? If yes, name the exact drift the next thread must reconcile.

### 4. Produce handoff

Write structured markdown following the [handoff template](assets/handoff-template.md).

Write to the path given as argument, or `HANDOFF.md` at the nearest workspace root. In a monorepo, this is the workspace (package) the session was working in — not the repository root. Determine the workspace from the files touched during the session: look for the nearest `package.json`, `Cargo.toml`, `go.mod`, or similar project marker up from the most-edited files.

Prefer overwriting the existing handoff instead of inventing a new filename.

### 5. Verify

- Does every in-flight artifact from step 2 appear in the handoff? **Count them.** If step 2 found N items, the handoff must contain N items.
- Are ALL review findings named — not just the active one? Is deferred review debt explicit?
- Is diagnostic evidence preserved — not just conclusions, but the proof points that justified them?
- Is the handoff carrying only still-volatile state? If something is durable and settled, it belongs in `memory/SPEC.md` or `memory/PLAN.md`, not here.
- Could a new thread read this file and know what to do first without asking?
- Is the resume prompt copy-pasteable?

## Constraints

- **Write the file to disk.** Chat-only output defeats the purpose.
- **In-flight state over persisted state.** Persisted state can be re-read; in-flight state cannot be re-derived. Weight accordingly.
- **Preserve structure, don't summarize.** A half-done scope card should appear as a scope card, not a paragraph.
- **Volatile transfer only.** `HANDOFF.md` is not an archive, history sink, or substitute for canonical reconciliation.
- **No new work.** The handoff captures state — it does not advance the plan, fix bugs, or make decisions.
