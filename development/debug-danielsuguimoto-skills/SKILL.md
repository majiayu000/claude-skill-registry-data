---
name: debug
description: "Use when a user reports a bug, error, or unexpected behavior and wants it troubleshot and fixed. Interactive: grills the user to clarify the problem, then investigates, plans, and executes the fix."
---

## Required `<project-root>/docs` reads

Read these project-root spec files before investigating the bug (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/bug-trackers.md`
- `<project-root>/docs/code-navigation.md`
- `<project-root>/docs/database-tools.md`
- `<project-root>/docs/doc-lookup.md`
- `<project-root>/docs/memory-providers.md`
- `<project-root>/docs/observability-tools.md`
- `<project-root>/docs/terminal-wrappers.md`
- `<project-root>/docs/terminal-tools.md`

Troubleshoot and fix a user-reported issue. Three phases, each with a grilling section. This skill **executes fixes**; for read-only root-cause reporting use `triage`.

## Tool Agnosticism

Reference `<project-root>/docs` specs, never hardcode tool names: code symbols → `<project-root>/docs/code-navigation.md`, DB → `<project-root>/docs/database-tools.md`, framework docs → `<project-root>/docs/doc-lookup.md`, error logs → `<project-root>/docs/bug-trackers.md`, observability → `<project-root>/docs/observability-tools.md`, terminal → `<project-root>/docs/terminal-wrappers.md`, memory → `<project-root>/docs/memory-providers.md`. Missing spec → fall back to native tools, note the gap.

## Grilling Discipline

Grill before exploring, hypothesizing, or fixing. One question at a time — wait for the answer, never batch. Include a one-line recommended answer. Ground in evidence: if codebase/logs/DB can answer it, investigate first. Cite file:line. Stop when target is met. AFK → proceed with recommended answers, state assumptions.

## Phase 1 — Context Gathering

Don't explore until the symptom is clear.

**1.1 Grill: Clarify the Symptom** — rotate until each settles: Symptom (quote error verbatim) · Expected vs actual · Reproduction (exact steps; no repro → last known-working + what changed) · Environment (version, branch, deployment, data state, feature flags) · Scope (who affected, when started) · Frequency (always, intermittent, load/time-dependent). Store as `<issue-context>`. Still undefined after one round → stop, list unknowns.

**1.2 Gather Evidence** — `<issue-context>` settled, collect don't guess: Reproduce against exact symptom (nearby failure isn't the bug; repro fails → say so, list attempts). Trace code path user action → failure (`<project-root>/docs/code-navigation.md`). Inspect DB when state persists (`<project-root>/docs/database-tools.md`) — live data is ground truth, don't trust seeders/migrations/factories. Pull error logs (`<project-root>/docs/bug-trackers.md`), read full trace. Inspect app runtime (`<project-root>/docs/observability-tools.md`). Check memory for prior pitfalls (`<project-root>/docs/memory-providers.md`). Fetch framework docs when behavior hinges on version/API (`<project-root>/docs/doc-lookup.md`). Store as `<investigation-findings>` with file:line citations.

**Done when:** symptom reproduced or attempted · code path traced · DB verified (when relevant) · traces read in full · context + findings stored.

## Phase 2 — Planning

Strategy before code. Single-hypothesis thinking anchors on the first plausible idea and misses the cause.

**2.1 Grill: Confirm the Strategy** — Hypotheses (present ranked list, ask to confirm/reorder) · Fix approach (minimal patch, refactor, or workaround — recommend one) · Risk tolerance (what must not change — recommend safest boundary) · Test strategy (recommend failing test reproducing the bug). Store as `<plan-decisions>`.

**2.2 Ranked Hypotheses** — Generate 3–5 from `<investigation-findings>`. Each falsifiable: "If `<X>` is the cause, then `<changing Y>` makes the bug disappear." No prediction → vibe, discard. Show ranked list before testing. Don't block if AFK.

**2.3 Test Hypotheses** — Change one variable at a time; each probe maps to a prediction. Tag debug logs with unique prefix `[DEBUG-a4f2]` (cleanup = one grep). Targeted logs at boundaries — never "log everything and grep."

**2.4 Analyze Root Cause** — Synthesize: `<root-cause>`, `<affected-components>`, `<impact-scope>`, `<reproduction-conditions>`, `<potential-fixes>` (ranked).

**Done when:** 3–5 falsifiable hypotheses · winning hypothesis tested, alternatives falsified · root cause/components/scope/conditions stated with evidence · fixes ranked · plan confirmed (or assumptions if AFK) · gaps named.

## Phase 3 — Execution

Minimal, surgical, verified.

**3.1 Grill: Confirm Before Applying** — The fix (chosen `<potential-fixes>` entry + exact files/symbols, cited. Proceed?) · Scope check (what will NOT change) · Rollback (how to undo; keep minimal and isolated). User declines → return to Phase 2. Don't apply unconfirmed fix.

**3.2 Implement** — Write failing test reproducing the bug first (when agreed). Apply minimal change at identified file/symbol/location. Match existing style/naming/error-handling. No comments, no speculative abstractions, no refactors beyond fix. Remove every `[DEBUG-xxxx]` log.

**3.3 Verify** — Run lint + tests. Reproducing test passes, no regression. Reproduce original scenario manually (when feasible) — symptom gone. Confirm no debug instrumentation remains. Store `<validation-results>`, `<validation-passing>`.

**3.4 Present and Stop** — Root cause (one line + citation) · fix applied (one line per change, file:line) · validation status · remaining gaps/risks. STOP. No commit, push, PR, or unsolicited next steps. User invokes `commit-and-push` or `ship-changes` to ship.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "I'll just fix it directly" | Fixing without root cause guarantees recurrence. |
| "The bug is obvious" | Obvious bugs are usually symptoms, not causes. |
| "Debugging takes too long" | Systematic debugging beats trial-and-error. |
| "I don't need to ask the user" | Vague report sent to the wrong target wastes the whole investigation. |
