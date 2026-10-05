---
name: slice-land
description: >
  Verify a finished slice is actually ready to land (tests green, DoD ticked,
  deviation log present, STATUS=DONE) and emit a deterministic landing
  checklist for either direct merge-to-main or PR-shaped integration. Use
  when the user says "land this slice", "merge back to main", "ready to
  ship", "create a PR for this slice", "close out the slice", or "slice is
  done — what now". Use `prepare` to emit a readiness report; use
  `execute --mode direct` to also run the merge sequence; use
  `execute --mode pr` to push the branch and open the PR.
user-invocable: true
---

> Spec 007 created this skill from scratch. The deterministic readiness
> checks + report generation live in `land.py`; this SKILL.md drives the
> judgment layer (when to invoke, how to interpret blockers, what mode to
> pick).

## What this skill does

Closes the worktree-drift gap: every slice in jig today commits to a
worktree branch and stays there until a human remembers to merge. The
skill provides a deterministic landing path:

- **Verify** the slice is actually done — STATUS=DONE in spec.md, full
  test suite green, deviation log section present, DoD checkboxes all
  ticked.
- **Emit** a structured markdown report with five readiness checks
  (STATUS=DONE, tests green, deviation log present, DoD ticked, and the
  Class-A cross-ref backstop — spec 112: refuse when the slice/ADR is already
  integrated on `origin/main`, `JIG_CROSSREF_GATE=0` to bypass) and
  (in `--mode direct` or `--mode pr`) a Next-steps section of suggested
  git commands.

`prepare` is **non-destructive on git state**: it may read branch state and
fetch `origin/main` to surface a branch-freshness warning, but it never
switches branches, merges, pushes, or removes worktrees.  `execute --mode
direct` runs the destructive merge sequence by pushing the current branch to
`origin/main`, then fast-forwards the canonical local `main` worktree to
`origin/main` or reports why local sync was skipped (slice 007-02 + 081-01);
`execute --mode pr` runs the destructive push + PR-open sequence (slice
007-03).  `git worktree remove` and `gh pr merge` are never executed — both
stay user-driven post-landing suggestions.

## How to use

### Run the readiness check

```bash
python3 "${PLUGIN_ROOT}/skills/slice-land/land.py" prepare \
  <path-to-spec.md> <slice-fragment> [--mode {direct,pr}]
```

- `spec.md` — path to the spec file (e.g. `docs/specs/007-slice-land/spec.md`).
- `<slice-fragment>` — case-insensitive substring against `## Slice X — Y`
  headings. Same lenient match as `workflow.py transition`.
- `--mode` — optional. Without it, only the readiness check runs.
  - `direct` — for solo / merge-to-main projects. Suggested commands:
    push the branch to `origin/main`, then fast-forward local `main` to
    `origin/main` when a clean canonical `main` worktree exists.
  - `pr` — for team / PR-shaped flows. Suggested commands: `git push -u
    origin <branch> && gh pr create --body-file <path>`. A PR body is
    written to `/tmp/jig-slice-<NNN-NN>-pr-body.md` containing the
    slice's ACs and a deviation-log excerpt.

### Run the merge sequence (execute --mode direct)

After `prepare` confirms the slice is ready, `execute --mode direct`
runs the direct landing sequence:

```bash
python3 "${PLUGIN_ROOT}/skills/slice-land/land.py" execute \
  --mode direct <path-to-spec.md> <slice-fragment> [--dry-run]
```

- `--dry-run` — print the git commands that would run without executing
  them. Use this for a final sanity check before committing.
- Without `--dry-run` — runs `git push origin <branch>:main` from the
  current worktree after the fast-forward guard passes, then fetches and
  fast-forwards the canonical local worktree checked out at
  `refs/heads/main` to `origin/main` when that worktree exists and is
  clean. The caller's feature/detached worktree is not switched to `main`.
  Stops and reports if the authoritative push fails. If the post-push
  local sync cannot run because `main` is missing, dirty, locked, diverged,
  or unavailable, the report says
  `local main sync skipped: <reason>` while preserving the successful
  authoritative push. Never runs `git worktree remove` (printed as a
  post-landing suggestion only).

**Safety guards** (checked before any git mutation):
- Refuses if current branch is `main` or `master`.
- Refuses if `main` has diverged (fast-forward not possible).

### Open the PR (execute --mode pr)

For PR-shaped flows, `execute --mode pr` pushes the branch and opens
the PR via the GitHub CLI:

```bash
python3 "${PLUGIN_ROOT}/skills/slice-land/land.py" execute \
  --mode pr <path-to-spec.md> <slice-fragment> [--dry-run]
```

- `--dry-run` — print the commands that would run, write the PR body
  file for inspection, but do NOT push or open the PR.
- Without `--dry-run` — runs `git push -u origin <branch>` followed by
  `gh pr create --title "<title>" --body-file <body-path>`.  Stops if
  push fails (gh is NOT called after push failure).  Title shape is
  `feat(<scope>): <subject>`: scope comes from a single `skill:`
  frontmatter value or falls back to the spec directory slug, and subject
  drops the numeric slice prefix so the PR-title workflow accepts it.
- Push runs from the **current worktree** (not the main worktree root,
  since the feature branch is checked out here).
- Never runs `gh pr merge` (printed as a post-landing suggestion only).
- Local `main` sync is pending until the PR actually merges. PR mode never
  claims local `main` was updated before `origin/main` moves.

**Safety guards** (checked before any subprocess mutation):
- Refuses if current branch is `main` or `master`.
- Refuses if `gh` CLI is not on PATH (install instructions printed).
- Refuses if `origin` does not point at github.com (HTTPS or SSH form).

### Exit codes

- `0` — all five readiness checks pass; the slice is ready to land
  (for `prepare`) or was merged successfully (for `execute`).
- `1` — at least one check failed, a safety guard fired, or a git
  command failed (the report still emits; the user sees what's wrong).
- `2` — user error (missing spec, ambiguous fragment, invalid `--mode`).

### Test-check warnings

If `tdd.py run` returns exit 2 (no test runner detected at the target),
the readiness report marks the Tests row as a `[?]` warning rather
than a `[ ]` blocker. Rationale: some slices are doc-only and have no
executable tests — those slices should still be landable. Exit 1 from
`tdd.py run` (red tests) IS a blocker.

### Close-out (post-DONE) subsection

Slices often include items that can only be completed AFTER the
`RECONCILED → DONE` transition — e.g. `workflow.py status-board` regen
(which reads the updated STATUS marker) skills-table
promotion (which advertises the slice as done). These items create a
chicken-and-egg if they live in the DoD: `slice-land` requires DoD =
N/N before blessing landing, but the user uses slice-land's blessing as
the cue to commit + flip to DONE.

**Convention (spec 009 / slice 009-01):** put post-DONE items in a
subsection headed `### Close-out (post-DONE)` inside the slice, after
the DoD checklist and before the slice's `---` separator. `slice-land`'s
`check_dod` recognizes the heading and excludes its checkboxes from the
count. Anything between `**DoD:**` and `### Close-out` is DoD-counted;
anything after isn't.

Example:

```markdown
## Slice 009-01 — close-out-section-recognition

**STATUS: DONE**

...

**DoD:**
- [x] All ACs pass; full suite green.
- [x] Reviewed by `reviewer` subagent.
- [x] Deviation log produced.
- [x] Reconciliation review pass.

### Close-out (post-DONE)

- [ ] `docs/specs/README.md` regenerated by `workflow.py status-board`
      AFTER the DONE transition.
- [ ] `AGENTS.md` skills-table update.
```

The heading is case-insensitive (matches `Close-out`, `Closeout`, `close
out`, etc.) and requires H3 (`###`) — H2/H4 don't delimit, to avoid
accidentally matching unrelated content.

If no `### Close-out` heading exists in the slice, `check_dod`
behavior is unchanged (counts all boxes in the slice section).

## When to invoke

Auto-trigger phrases: "land this slice", "merge back to main", "ready
to ship", "create a PR for this slice", "close out the slice", "slice
is done — what now".

Typical session flow:

1. Slice transitions to `DONE` via `workflow.py transition`.
2. Deviation log is written under the slice heading.
3. DoD checkboxes get ticked.
4. Run `land.py prepare ... --mode direct` (or `--mode pr`).
5. Copy-paste the suggested commands.

## End-to-end example

```bash
# 1. Verify readiness — no merge command yet.
python3 .../land.py prepare docs/specs/007-slice-land/spec.md "007-01"

# 2. Get the direct-merge recipe.
python3 .../land.py prepare docs/specs/007-slice-land/spec.md "007-01" --mode direct

# Expected output (when all five checks pass):
#
#   # Landing readiness — slice 007-01 — land-prepare
#
#   ## Readiness checks
#
#   - [x] Status: DONE
#   - [x] Tests: green (`tdd.py run` exit 0)
#   - [x] Deviation log: present
#   - [x] DoD: 9/9 boxes ticked
#   - [x] Cross-ref state: not already integrated on origin/main
#
#   ## Next steps (mode: direct)
#
#   Run via `execute --mode direct` so `origin/main` is updated from
#   this branch, then the canonical local `main` worktree is
#   fast-forwarded as housekeeping when it is available and clean:
#
#       git push origin claude/eager-zhukovsky-34ebb0:main
#       git fetch origin main
#       git merge --ff-only origin/main
#       git worktree remove .codex/worktrees/eager-zhukovsky-34ebb0
```

## Gotchas

- **`prepare` is non-destructive; `execute` IS destructive.**
  `prepare` only writes the PR body file (mode=pr); it never runs
  `git checkout`, `git merge`, `git push`, `git worktree remove`, or
  `gh pr create`.  `execute --mode direct` runs the push/sync sequence
  as an authoritative push to `origin/main` and reports the post-push local
  sync result (007-02 / 081-01); `execute --mode pr` runs push + gh pr
  create (007-03) and reports local sync as pending on merge.
  Use `--dry-run` for a non-destructive preview of either execute mode.
- **Test-check target = `land.py`'s cwd.** The helper invokes
  `tdd.py run` against the current working directory by default. If
  the slice changes a deep subdir (e.g. `skills/foo/`), run `land.py`
  from `skills/foo/` (or pass it as cwd) to keep the test run focused.
  Running from the project root re-tests the whole suite — slower but
  also more honest.
- **Substring fragment matching is identical to `workflow.py`.** A
  fragment like `007-01` matches `## Slice 007-01 — land-prepare`.
  Ambiguous fragments (multiple matches) refuse with exit 2.
- **PR body file path is predictable** (`/tmp/jig-slice-NNN-NN-pr-body.md`)
  so callers can read / edit the body before `gh pr create`. Re-running
  `--mode pr` overwrites the same file — idempotent.
- **The Test plan section in the PR body uses generic `[x]` lines.**
  The helper does not detect per-AC test counts — that would require
  the AC-coverage mapping deferred to slice 006-02. The generated
  checkboxes are placeholders; tighten the PR body manually before
  `gh pr create` if you want specific counts.
- **Branch detection requires being inside a git repo.** Outside one
  (e.g. running against a synthetic spec in `/tmp`), the helper
  degrades to the literal placeholder `<BRANCH>` in the suggested
  commands. Edit by hand before running.
- **Deviation log detection is heading-based.** The helper looks for
  `### Deviation log` (or a variant like `### Deviation log (after
  reconciliation)`) within the slice section. Missing heading → blocker,
  even if the slice has reconciliation content under another heading.
  Convention: every Done slice gets the explicit subsection.

## Relationship to other skills

- **`spec-workflow`** owns the lifecycle state transitions
  (`workflow.py transition`). `slice-land` runs AFTER the final DONE
  transition; the two skills cleanly compose.
- **`independent-review`** runs BEFORE `slice-land` — review verdicts
  must be `pass` and reconciliation review must be done before the
  slice goes DONE. Once the slice is DONE, `slice-land` checks
  readiness and emits the landing recipe.
- **`tdd-loop`** is the helper `slice-land` shells out to for the
  test check. The test-check normalization (green / red / warn) maps
  directly to `tdd.py run`'s exit code 0 / 1 / 2.
- **`adr-workflow`** is orthogonal — ADRs may or may not be written
  during reconciliation. `slice-land` doesn't gate on ADR presence.

## Out of scope for slice 007-03

- `scaffold.json` `integration: "direct" | "pr"` field (slice 007-04
  remains deferred — the `--mode` flag is sufficient for manual
  invocations).
- Multi-slice batch landing (single slice at a time is the right
  audit-trail granularity).
- Interactive confirm-before-push prompt — `--dry-run` is the
  preview mechanism instead.  Use `--dry-run`, inspect the PR body,
  then re-run without `--dry-run`.
- JIRA / Linear ticketing integration, Slack notifications,
  auto-drafting ADRs from the deviation log.
- GitHub Enterprise (self-hosted) — the `_check_github_remote`
  substring match requires `github.com` literally.  Self-hosted GHE
  users will need a future extension or local override.
