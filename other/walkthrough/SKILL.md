---
name: walkthrough
description: Autonomous maintenance walkthrough — baseline, spec drift (via surveyor), coverage, docs, and a prioritized recommendations list. Applies safe (Quick-Path) fixes; routes anything bigger to recommendations for review. The maintain-mode counterpart to homeowner (build mode).
version: 1.0
---

## Contract terms — read first

Before anything else, read your slice of the Plumbline contract at **`${CLAUDE_PLUGIN_ROOT}/terms/walkthrough.md`** — generated from the root `TERMS.md`, it holds every shared token, status line, and file-naming pattern this skill reads or writes. Reproduce them **verbatim**. **If you cannot load it, stop and report; do not guess the contract.**

---

## When to use this skill
When you want to spend a session improving a project without manual oversight.
Run `/walkthrough` and walk away. It ends with safe fixes applied and a prioritized list of everything else for you to approve.

---

## Setup

Before starting, identify:
1. **Project root** — the folder being walked
2. **Test command** and **run/demo command** — from the project's CLAUDE.md
3. **Specs folder** — `Planning/specs/` (the convention; fall back to `docs/specs/` if that's what the project uses)
4. **Output folder** — `Plumbline/walkthrough/` in the project root (create it if missing). Both this run's files land here, dated.

---

## Rules
- **No check-ins.** Do not ask for permission. Anything you cannot safely do autonomously goes to Recommendations.
- **Spec is truth.** If code disagrees with the spec, the spec wins.
- **Autonomy is fenced by the Change rules in CLAUDE.md (Quick Path / Full Path).** Apply **Quick-Path** changes yourself (no new/removed files, no schema change, no core-logic change, nothing that needs a decision doc). **One explicit file-creation exception: new *test* files are Quick-Path** — adding a test for existing behavior changes nothing a future reader needs explained. Anything that is **Full-Path** — schema, core logic, new/renamed non-test files, decisions worth recording — goes to **Recommendations**, not applied. Do not author decision docs unattended.
- **Run the test command after every change.** If a change breaks tests and you can't fix it within the Quick-Path fence, revert it and log to Recommendations.
- **Log everything** to `Plumbline/walkthrough/WalkthroughLog_YYYY-MM-DD_HH-MM.md` as you go.
- **Commit nothing.** Leave all changes uncommitted for review.

---

## Execution Order

### Phase 1 — Baseline
1. Run any health scripts the project has (check `tools/` if it exists).
2. Run the test command. Log pass/fail.
3. If specs carry "Done when" items, run **inspector** to learn what is actually *proven*, not just what compiles. **Spawn it as a separate subagent** — inspector's value depends on fresh eyes, and running it inline in this session defeats that. Log the result it reports back. If inspector returns **`BLOCKED`** (the run/demo command won't launch — nothing can be verified), log that as "no runtime baseline" and carry it to Recommendations as a HIGH item; do not treat a `BLOCKED` as a proof result, and don't try to fix the launch yourself if it's Full-Path.
4. Record all of this as the baseline in WalkthroughLog.

### Phase 2 — Spec drift
Run the **surveyor** skill to detect drift — do not reimplement detection here. Then act on its report:
- **Drift, Quick-Path fix:** correct the code to match the spec, run tests, log it.
- **Drift, Full-Path fix:** log to Recommendations (do not apply).
- **Unimplemented / Undocumented / Untested automated criteria:** log to Recommendations with priority. (Adding a missing test is Quick-Path — you may do it in Phase 3.)

### Phase 3 — Test coverage
1. Identify code paths with no coverage (core logic, edge cases, integration seams), plus any `[automated]` Done-when items surveyor flagged as having no backing test.
2. Add tests for them — adding tests is Quick-Path. Run the full suite after.

### Phase 4 — Documentation
Improve project docs for clarity: `CLAUDE.md`, `CONTEXT.md` / `REFERENCES.md`. Remove redundancy and stale info; make file maps scannable.

**Walk test — judge the contract as an agent with no memory would:**
1. From `CLAUDE.md` plus at most two more reads, can you answer *where am I* and *where do I go for task X* (find the current spec, its blueprint, the latest inspection)?
2. Can you state build status purely by scanning `Plumbline/` and the blueprint's checkboxes — no prose summary required?
3. Is `CLAUDE.md` carrying content that belongs in a spec, reference, or decision doc? Move the payload to its home and leave a pointer (a doc edit — Quick-Path).
4. Is any fact stated in two places? Pick one home; link from the other.

A walk-test failure that needs files moved or renamed is Full-Path — route it to Recommendations rather than fixing structure unattended.
- **Do not edit skill files or other tooling.** If a skill or tool should change, write it to Recommendations — walkthrough does not rewrite its own machinery unattended.
- **Never fill a `[pending — architect]` contract field.** If `CLAUDE.md`'s Stack or Commands are still placeholders, that's not a doc cleanup — it's drift (architect should have filled them at the first spec). Route it to **Recommendations** ("contract Stack/Commands never filled — run architect"); do not fabricate the stack or a run command yourself.

### Phase 5 — Tools
Look for repeatable tasks worth a helper script (health checks, cross-reference validators). If you write one, create `tools/` lazily at that point (it is not pre-created). A new tool script is Full-Path — propose it in Recommendations first unless it is a trivial, self-contained check.

### Phase 6 — Recommendations
1. **Read the deviation history first** — `Plumbline/deviations/` across all past builds. The
   builder model varies run to run, so don't tune grain to a model — read the trends as
   *plan-quality* signals:
   - **Dense trivial deviations** (renames, file moves, tactic swaps) → blueprints are
     constraining tactics that don't affect outcomes; recommend foreman pin what matters
     (names, interfaces, behavior) and leave tactics free.
   - **Repeated Stucks / ambiguity stops** → steps keep leaving addresses or details thin;
     call out what foreman keeps under-specifying.
   - A handful of meaningful deviations is healthy — only flag a *pattern*.
2. Compile everything deferred into a prioritized list (format below).

---

## Log Format (Plumbline/walkthrough/WalkthroughLog_YYYY-MM-DD_HH-MM.md)

```
## Phase N — Title

### [sequence] Action taken
- **Area:** file or module
- **Finding:** what was found
- **Action:** what was done (or "DEFERRED — Full-Path, see Recommendations")
- **Tests:** pass/fail after change
```

---

## Recommendations Format (Plumbline/walkthrough/Recommendations_YYYY-MM-DD_HH-MM.md)

```
## Priority: HIGH / MEDIUM / LOW

### Title
- **Area:** file or module
- **What:** description of change
- **Why:** rationale
- **Effort:** small / medium / large
- **Path:** Quick / Full
- **Spec affected:** which spec, if any
```
