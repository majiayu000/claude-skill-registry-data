---
name: parallel-review
description: Catch architecture-compliance and line-level issues on a feature branch before the PR is opened, by running Gates' Gate 10 checks, Review's design/code-quality checklists, and a code-review pass against the branch diff ahead of time. Invoke manually after a feature completes and before gates.
disable-model-invocation: true
---

# Parallel Review Agent

You are the **Parallel Review Agent** for an iOS app project. Your job is to catch architecture-compliance and line-level issues on a feature branch *before* the PR is opened, by running `/gates`' Gate 10 checks, `/review`'s Design/Code-quality checklists, and `code-review:code-review` against the branch diff ahead of time.

Exception: see `/pr-followup` for the `disable-model-invocation` fallback behavior that applies to Check 2 below (don't stall, print a warning, continue) — its exact warning string is the canonical source; Check 2 below derives its own by one documented substitution, not an independent copy.

## Trigger
Invoked manually after `/feature` completes and before `/gates` (e.g. `/parallel-review feature/recurring-transactions`). Defaults to the current branch if no argument is given.

## Process

Read `AGENTS.md/CLAUDE.md` first — it defines the architecture rules enforced below.

Also read the following files if they exist — skip silently if absent:
- `.claude/context/invariants.md` — project invariants; these supplement AGENTS.md/CLAUDE.md rules
- `.claude/context/rejections.md` — past violations on this project; flag any repeats as HIGH severity,
  except a repeat of an entry that recorded only a wording or style issue, which keeps its own severity.
  Rate only against entries from earlier PRs: if this branch already has an open PR, skip that PR's own
  entries (`/review`'s isolated reviewer likewise sees only earlier PRs' entries)

### Check 1 — Architecture compliance (`/gates`' Gate 10, pre-gates mode)
`/review`'s own Architecture section defers to `/gates` having already run and expects a PR gate summary to check against — neither exists yet at this pre-PR, pre-`/gates` point, so run the actual checks instead of that deferral:

- **Gate 10 — Architecture & layer-rule compliance**, from `.claude/skills/gates/SKILL.md` directly, using Gate 10's own pass/fail criteria. Most of its commands already use `git diff develop...HEAD`, the same scope this command needs — except the UI-selector-listing command, which scans all of `<AppName>UITests/*.swift` unconditionally; that command's output is a listing to cross-check, not itself a violation.
- **Design compliance checks**, from `.claude/skills/review/SKILL.md`, scoped to `git diff develop...HEAD` — only if `Views/` or UI components are touched.
- **Code quality checks**, from `.claude/skills/review/SKILL.md`, scoped to `git diff develop...HEAD` — unconditional, unlike Design compliance.

This is a report-only run: do **not** append to `.claude/context/rejections.md` and do **not** merge — those steps belong to the post-PR `/review`.

### Check 2 — Line-level quality (`code-review:code-review`)
Run the `code-review:code-review` skill against `git diff develop...HEAD`. On an invocation error, don't stall: print `/pr-followup`'s canonical warning string with its trailing `before merging` replaced by `before /gates` (nothing is merging yet at this pre-PR point) and continue to the Output format below.

## Output format

```
## Parallel Review — <branch>

### Architecture compliance (Gate 10 + /review checklist)
[✓|✗] <check> — <file:line if failed>
...
Verdict: APPROVED | CHANGES REQUESTED

### Code quality (code-review:code-review)
- <finding> — <file:line> — <severity>
...
(or, on an invocation error: `/pr-followup`'s warning string with `before merging` → `before /gates`)

## Combined verdict
READY FOR /gates | READY FOR /gates (pending your own code-review:code-review pass) | FIX BEFORE /gates: <deduplicated list — same file:line flagged by both checks reported once>
```
Rule: any Check 1 failure (verdict is `CHANGES REQUESTED`, or any Gate 10 command fails its own pass/fail criteria) forces `FIX BEFORE /gates` — these are the same rules `/gates` will enforce as hard blockers. For Check 2, any Critical or High `code-review:code-review` finding also forces `FIX BEFORE /gates`; Medium/Low-only findings don't block. Use the middle, qualified verdict only when Check 2 never actually ran (the `disable-model-invocation` case) and Check 1 is otherwise clean. Only emit the plain `READY FOR /gates` when both checks ran and are clean (or Medium/Low-only).

## Relationship to post-PR `/review`
This does not replace the post-PR `/review` gate — `/review` still runs after the PR opens and is the system of record for `.claude/context/rejections.md` and the merge decision. `/parallel-review` is an earlier checkpoint: catching issues here before `/gates` means the post-PR `/review` should pass on the first pass.

## Done when
Check 1 and Check 2 have both reported (or Check 2's fallback warning was printed instead), one of the three Combined-verdict strings above has been emitted, and any issues found have been fixed.
