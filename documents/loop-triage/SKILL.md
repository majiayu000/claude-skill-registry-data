---
name: loop-triage
description: >
  L1 daily loop triage for the orchestrator template. Cache is king: load manifest + lean cache
  before any source or gh deep-dive. Synthesise priorities into STATE.md and reports/loops/.
  Report-only; no auto-fix. Use on schedule or /loop-triage.
argument-hint: "Optional focus, e.g. 'PRs', 'workflows', 'TODO carry'"
user-invocable: true
disable-model-invocation: false
---

# Loop Triage (L1, cache-first)

**Cache is king.** This loop does not explore the codebase. It reads cached knowledge and minimal host snapshots.

## Mandatory load order (do not skip)

1. `.github/project-manifest.yaml` or `.claude/project-manifest.yaml` — `paths`, `token_policy`, `loop_policy`
2. `LOOP.md` — confirm level **L1** for this run
3. `loop-budget.md` — respect max cache files and zero source files at L1
4. `STATE.md` — resume open queue; do not duplicate done items
5. `docs/codebase/README.md` + `docs/codebase/.codebase-scan.txt` — staleness only
6. **≤3 targeted sections** from `docs/codebase/CONCERNS.md`, `ARCHITECTURE.md`, or `CONVENTIONS.md` (grep headings; no full-file read unless small)
7. Latest `TODO/*.md` — open items in ≤5 bullets
8. `.grok/memories/INDEX.md` — ≤2 memories if relevant

## Optional host snapshot (after cache only)

Only if needed for the report; cap at 3 commands:

- `git branch --show-current` + `git status --short`
- `gh pr list --limit 5` (if `gh` available)
- `gh run list --limit 3` (if `gh` available)

Do **not** run grep/find across source trees at L1.

## Produce (L1)

1. Write `reports/loops/YYYY-MM-DD-triage.md` with:
   - **Cache cited:** list every file/section used
   - **Priorities:** ≤5 bullets from cache + TODO
   - **Risks:** numbered CONCERNS items touched
   - **Host snapshot:** branch, open PRs (if fetched)
   - **Next:** 1–3 human actions (no auto-fix)
2. Update `STATE.md` — Cache used, Open/Done, Last session
3. Append one row to `loop-run-log.md`
4. Stay ≤120 words in the executive summary at top of report

## Chain verifier

Invoke `/loop-verifier` on the report artifact before marking run complete.

## Anti-patterns

- Reading `app/`, `src/`, or large trees before cache load
- Auto-commits, auto-PRs, or fixes at L1
- Pasting large cache paragraphs into the report (cite by section only)