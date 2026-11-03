---
name: understand
description: >
  Build a complete mental model of a codebase, module, or feature before any change is discussed.
  Use whenever the user says "understand the codebase", "first understand", "first of all understand",
  "explore the code", "how does X work", "understand @path fully", or opens a session by pointing at
  a module or directory. Read-only: this skill never edits, never plans changes, never proposes fixes.
  It produces a compact mental model — purpose, file map, state machine, event flow, schedule hooks —
  and ends ready for change requests. Always run this before planning any modification.
---

# Understand — Module Mental Model

You are building the mental model a veteran engineer forms before touching code. Read deeply, report compactly. **No edits. No fix proposals. No plans.**

## Phase 1 — Locate Boundaries

Identify what "the module" is:

1. If given a path, list its full tree (`Glob` on `<path>/**/*`).
2. Find its namespace root and every sub-folder (slices, sub-features).
3. Note sibling modules it might touch — you will trace those edges in Phase 3.

## Phase 2 — Read the Core

Read in this order; skip nothing that exists:

1. **Entry points** — controllers, route registrations, scheduled jobs, webhook handlers, console commands. Grep route files and scheduler files for the module's class names.
2. **Models & schema** — every model the module touches: fillable, casts, relations, scopes. Then the migrations that shaped those tables.
3. **Domain services** — the classes doing the real work. Read them fully, not just signatures.
4. **Events & listeners** — every event the module fires or consumes; read each listener's `handle()`.
5. **Jobs** — what dispatches them (event, scheduler, chain, batch) and what they delegate to.
6. **UI surface** — views/components rendering this module's data.
7. **Tests** — scan test names for the behavior contract; note what is covered and what is not.
8. **Config** — module config files, env variables, feature flags, kill-switches.

## Phase 3 — Trace the Flow

Assemble the journey of one record through the module:

- **Trigger** → what starts the flow (user action, schedule, event, webhook).
- **State machine** → every status/stage field: which class writes each value, which class consumes it.
- **Events out / events in** → what other modules learn from this one, and vice versa.
- **Schedule hooks** → every scheduler entry with cadence and the job it fires.
- **Failure paths** → retries, circuit breakers, error states, idempotency guards.

## Output Contract

Report exactly these sections, in this order, compact:

1. **Purpose** — one sentence.
2. **File map** — tree of slices/files with a half-line role each.
3. **State machine** — table: status value → written by → consumed by.
4. **Flow** — the trigger-to-completion journey as a short numbered list.
5. **Events & schedules** — what fires, when, who listens.
6. **Test coverage** — what the suite proves; visible gaps (facts only, no fix proposals).
7. **Open questions** — anything ambiguous that a change request would need answered.

End with: **"Mental model ready. What do you want to change?"**

## Hard Rules

- Read files fully before summarizing them — never infer behavior from a name.
- Never conclude behavior from a controller alone; read the service it delegates to.
- No edits, no refactor suggestions, no "improvements noticed" — this skill only maps what exists.
