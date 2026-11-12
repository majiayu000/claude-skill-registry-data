---
name: plan-status
description: Report measured open, done, and blocked counts from the project's active plan and backlog, then list the open decisions as numbered A/B/C questions with a recommended option, answerable in one line. Read-only. Use when the user asks where the work stands or what is left, for example "what is the status", "what is left", "show the plan status", "where do we stand".
license: MIT
compatibility: "Claude Code"
---

# Plan status

Read-only: never edit a plan, backlog, or any other file, and never run a test or build to get a number.

## 1. Find the sources

- Plans: the `*.md` files directly in the planning location the project's `AGENTS.md` or `CLAUDE.md` declares, otherwise `docs/plans/`, not its subdirectories (`approved/`, `lanes/`). The files the `Backlog:` line names are not plans. The active plan is the most recently updated one whose task is not done (not marked done in its status section); list the other not-done plans by name.
- Backlog: a `Backlog: <todo path>, <done path>` line in the project's `AGENTS.md` or `CLAUDE.md`, otherwise `TODO.md` and `TODO-done.md`. A missing backlog is `none found`, not an error.
- If no plan exists, say so and report the backlog alone.

## 2. Count

Count, do not estimate. State the rule you used in the output.

- **Done:** `- [x]` items, or steps the plan's status section names as done.
- **Blocked:** open plan items or steps that say `blocked` (any case) or use a `[!]` or `[-]` box. Name each with its blocker. A backlog item's `Blocked by:` line does not count here; it decides ready or waiting below.
- **Open:** every other `- [ ]` item or step. Blocked items are not counted again as open.
- A plan line that only links a backlog ID (`- FEAT-03: …`) is counted in the backlog, not again in the plan.
- A plan without checkboxes: count its steps (`### Step …` or numbered step headings) and classify each from the plan's own status text; a step with no status is open.
- Backlog: open items per `P0`–`P3` section in the todo file; items in the done file. Count each open item in exactly one bucket, first match wins: **orphaned** (an `Owner` dated more than 7 days ago), **waiting** (a `Blocked by` ID still open), **claimed** (any other `Owner`), **ready** (the rest). The four add up to the open count. Name each orphaned item with its owner.

## 3. Decisions

Collect the questions the plan leaves open (an open-questions section, `Q`/`D` items without an outcome, open items that wait on the user). Keep the plan's IDs; otherwise number them 1, 2, 3. Give each two or three lettered options with a one-line consequence and mark one as recommended with the reason. At most five questions; the most blocking first.

## 4. Output

```
Plan: docs/plans/2026-10-14-search-index.md (rule: checkboxes)
Done 3 · Open 2 · Blocked 1
Blocked: "Deploy to staging" — waits on database credentials
Backlog: TODO.md — P0 0 · P1 2 · P2 4 · P3 1; done 9 · ready 4 · waiting 2 · claimed 0 · orphaned 1
Orphaned: SEC-04 — Owner .worktrees/sec-04 (2026-10-02)
Next: "Add the reindex command"

1. Index storage? A) SQLite (recommended: no new service) B) Postgres C) in memory
2. Ship before the reindex command? A) yes B) no (recommended: the index goes stale)

Reply like "1A 2B".
```

Without open decisions, end with the next action instead of questions.
