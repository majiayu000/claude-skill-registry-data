---
name: review-fix
description: 'Applies saved code-review findings and updates artifact status. Use when fixing a review file, applying severity-filtered findings, or tracking review fixes as Fixed or Failed.'
argument-hint: '[--parallel | --team] [--severity <level>] [--no-worktree] [--dry-run] <path/to/review.md | pr-number | blank>'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Agent
  - AskUserQuestion
  - TaskCreate
  - TaskGet
  - TaskList
  - TaskUpdate
  - SendMessage
  - Bash(ls:*)
  - Bash(cat:*)
  - Bash(test:*)
  - Bash(find:*)
  - Bash(mkdir:*)
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pnpm:*)
  - Bash(yarn:*)
  - Bash(bun:*)
  - Bash(npx:*)
  - Bash(cargo:*)
  - Bash(go:*)
  - Bash(pytest:*)
  - Bash(python:*)
  - Bash(python3:*)
  - Bash(make:*)
---

# Review Fix

Apply fixes for saved `/ycc:code-review` artifacts: filter findings, group
into dependency-safe batches, dispatch `ycc:review-fixer` agents, update the
artifact's Status fields in place, write a fix report. Adapted from
PRPs-agentic-eng by Wirasm. The artifact is the source of truth; never modify
a finding's `Suggested fix` — mark it `Failed` and let the human decide.

Input: `$ARGUMENTS`.

## Phase 0 — DETECT

Extract flags from `$ARGUMENTS` before treating the remainder as the input:

| Flag                 | Effect                                                                                                                             |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `--parallel`         | Standalone `ycc:review-fixer` sub-agents in parallel per batch; fail-stop between batches                                          |
| `--team`             | Claude Code only; same fan-out via implicit agent team (flat task graph, per-batch spawn + shutdown)                               |
| `--severity <level>` | Minimum severity: CRITICAL/HIGH/MEDIUM/LOW; default HIGH                                                                           |
| `--dry-run`          | Print the fix plan and stop. No dispatch, no file changes. With `--team` also print team name and per-batch roster (no tool calls) |
| `--worktree`         | Legacy no-op; worktree mode is default (auto-detect from artifact)                                                                 |
| `--no-worktree`      | Apply fixes directly in current working tree                                                                                       |

Strip these flags from `$ARGUMENTS` and set `PARALLEL_MODE`, `AGENT_TEAM_MODE`, `MIN_SEVERITY`, `DRY_RUN`, and `WORKTREE_MODE=true` unless `--no-worktree` is present. The remaining text is the input selector.

**Questions:** class `failure-recovery` (Path B/C between-batch failure): headless (no question tool or chat turn), stop, preserve completed fixes, and print the failing batch plus the resume command; class `clarify` (blank input): headless, print the resolved artifact path and stop. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

**Validation**:

- Both `--parallel` and `--team`:
  `--parallel and --team are mutually exclusive. Pick one.`
- `--team` without `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`:
  `--team requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1. Use --parallel instead, or set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in your Claude Code settings if you intentionally want agent-team dispatch.`
- `--team` in Cursor/Codex bundles: use `--parallel` instead.

Input resolution — artifact lives on the PR branch in the worktree's
`docs/prps/reviews/`; fall back to main repo's. Path ending `.md` → as-is;
digits → `docs/prps/reviews/pr-<N>-review.md`; blank → latest by mtime in
current worktree, then main repo; prompt user to confirm.

Error paths:

- Nothing found: `Error: No review artifact found.` + `Run /ycc:code-review first to produce a review artifact.`
- Missing explicit path: `Error: review file not found: <path>`
- Unparseable: stop with
  `Error: Review file has no parseable findings or is not in the expected format.`
  - `See ${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-artifact-format.md`.
- No Open findings: stop with Fixed/Failed counts, `Nothing to do.`

Package manager detection (`TYPECHECK_CMD`, `TEST_CMD`):

| File                | Type-check                                                                     | Tests           |
| ------------------- | ------------------------------------------------------------------------------ | --------------- |
| `bun.lockb`         | `bun run typecheck`                                                            | `bun test`      |
| `pnpm-lock.yaml`    | `pnpm typecheck` / `pnpm tsc`                                                  | `pnpm test`     |
| `yarn.lock`         | `yarn typecheck`                                                               | `yarn test`     |
| `package-lock.json` | `npx tsc --noEmit`                                                             | `npm test`      |
| `Cargo.toml`        | `cargo check`                                                                  | `cargo test`    |
| `go.mod`            | `go vet ./...`                                                                 | `go test ./...` |
| `pyproject.toml`    | `pytest` (`python3 -m mypy <paths>` only when mypy is configured with targets) | `pytest`        |

## Phase 1 — LOAD

Parse artifact per finding schema and status rules:

`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/review-artifact-format.md`

Build an in-memory list of `Finding` objects with fields:

- `id` (e.g., `F042`)
- `severity` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`)
- `file`
- `line`
- `description`
- `status`
- `category`
- `suggested_fix`

If every finding already has `Status: Fixed` or `Status: Failed`, stop with:

```
All findings in this review have already been processed.
  Fixed:  N
  Failed: M
Nothing to do.
```

**CHECKPOINT**: Review loaded. All findings parsed. At least one `Status: Open` finding exists.

Finding missing Status → treat as Open, warn:
`Warning: Finding F### has no Status field. Treating as Open.` +
`Fix the source review file format — see review-artifact-format.md (shared reference above).`

Scan for `^## Worktree Setup`:

- Present → `WORKTREE_ACTIVE=true` (artifact declaration wins). Capture
  `PARENT_PATH` (parent worktree, `- **Parent**: <path> (branch: <branch>)`)
  and `PARENT_BRANCH`. Missing directory:
  `Error: parent worktree <path> is declared in the review artifact but does not exist.` +
  `Re-run /ycc:code-review --worktree <N> to recreate it, then retry.`
- Absent + `WORKTREE_MODE=false` → `WORKTREE_ACTIVE=false`; continue.
- Absent + forced `--worktree`: for `pr-<N>-review.md` resolve PR head and run
  `setup-worktree.sh parent <repo> pr-<N> --base-ref <head>`. For
  `local-*-review.md`: `Error: --worktree cannot be force-applied to a local review artifact that was produced without worktree isolation. Re-run /ycc:code-review --worktree to regenerate.`

## Phase 2 — FILTER

In order, tracking drops: (a) keep `Status: Open` only; (b) severity ≥
`MIN_SEVERITY` (CRITICAL > HIGH > MEDIUM > LOW); (c) drop empty
`Suggested fix`; (d) drop findings whose file is missing (`test -f`).

Print filter summary (Total/Already Fixed/Already Failed/Below threshold/No
suggested fix/Missing files/Eligible). `M == 0` → `No eligible findings to fix.`

## Phase 3 — PLAN

Read the batching contract before building batches:

`${CLAUDE_PLUGIN_ROOT}/skills/review-fix/references/plan.md`

Post the plan as a `Fix Plan:` block (counts M/G/B/W, per-batch listing with
IDs, `file:line`, severity and file counts). Worktree mode prints the
plan summary with severity batches from that reference. `--dry-run` with
`--worktree` prints that summary and exits; all batches would run inside the
parent worktree at `$PARENT_PATH`.

### Dry-run gate

If `DRY_RUN=true` and `AGENT_TEAM_MODE=false`, stop here. Print a reminder:

```
Dry run complete. To apply fixes, re-run without --dry-run:
  /ycc:review-fix $REVIEW_FILE [--parallel | --team] [--severity <level>]
```

If `DRY_RUN=true` and `AGENT_TEAM_MODE=true`, defer the final exit to Phase 4 C.2 so the team name and per-batch teammate roster can be printed alongside the fix plan. Do NOT proceed to any team/task/agent tool calls.

**CHECKPOINT**: Plan built. Batches computed. User has seen the plan.

## Phase 4 — EXECUTE

Read fixer prompt contract, Path B/C fan-out and failure handling:

`${CLAUDE_PLUGIN_ROOT}/skills/review-fix/references/fixer-dispatch.md`

Branch based on `PARALLEL_MODE` and `AGENT_TEAM_MODE`:

| Flags             | Path                                               |
| ----------------- | -------------------------------------------------- |
| Neither set       | **Path A** — sequential execution (default)        |
| `PARALLEL_MODE`   | **Path B** — parallel standalone sub-agent batches |
| `AGENT_TEAM_MODE` | **Path C** — agent-team batch execution            |

### Worktree-mode lifecycle (`WORKTREE_ACTIVE=true`)

Read when `WORKTREE_ACTIVE=true`: the "Worktree-mode lifecycle" section of
`${CLAUDE_PLUGIN_ROOT}/skills/review-fix/references/plan.md` and
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/worktree-strategy.md` §1.
All batches run inside
`$PARENT_PATH`; validation per batch:

```bash
( cd "$PARENT_PATH" && $TYPECHECK_CMD ) && ( cd "$PARENT_PATH" && $TEST_CMD )
```

One-time parent setup only when forced and not yet ensured.

Status updates in place via `Edit` after each agent returns: Fixed on
`STATUS: Fixed`, Failed on `STATUS: Failed`. Track per-batch todos. In Path B/C,
between-batch validation failure stops and asks for the path-specific choices
in fixer-dispatch.md. Path A continues; no stop-and-ask gate.

## Phase 5 — VERIFY

Run `$TYPECHECK_CMD` and `$TEST_CMD`; record pass/fail. Diagnostic only — no
rollback; user decides.

## Phase 6 — REPORT

Read report template and worktree summary:

`${CLAUDE_PLUGIN_ROOT}/skills/review-fix/references/fix-report.md`

Write to `docs/prps/reviews/fixes/<source-name>-fixes.md` under the active
checkout root. In worktree mode, stage and commit the report alongside fix
commits and push. GitHub-only: detect forge first (see
`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/forge-detection.md`); on
non-GitHub providers skip commit/push with notice
`PR posting is GitHub-only on provider <provider>; fixes applied locally — commit and push them yourself.` and `REPORT_COMMITTED: n/a`.

## Phase 7 — OUTPUT

Start the output with this literal heading:

```markdown
## Review Fixes Complete
```

Report source path, report path, mode, eligible/fixed/failed/skipped/open
counts, updated statuses, validation results, next steps
(`/ycc:code-review <target>` re-review, `/ycc:git-workflow --commit`).

Print under `### Goal Signals (machine-readable — printed verbatim for /goal)`,
as the last lines, one `KEY: PASS|FAIL` per line (always include the value):

```
PLAN_VALID: <PASS|FAIL>
REVIEW_UPDATED: <PASS|FAIL>
REPORT_CREATED: <PASS|FAIL>
VALIDATION_RUN: <PASS|FAIL>
REPORT_COMMITTED: <PASS|FAIL|n/a>
```

PASS only when the criterion holds: plan respects same-file sequentialization;
every attempted finding's Status updated in the source artifact; report
written under `docs/prps/reviews/fixes/`; Phase 5 completed (even if checks
failed); report committed and pushed (worktree mode; `n/a` in `--no-worktree`).
Also print an `Open remaining: <M - X - Y>` line.

## Edge cases

- Stale line numbers (file changed since review) → fixer returns Failed;
  note `stale line — file modified since review`.
- Interrupted runs resume cleanly: statuses update incrementally; re-runs skip
  Fixed/Failed.
- No recursive new-finding scan; re-run `/ycc:code-review` after fixes.

## /goal pairing

Done signal: `Open remaining: 0` plus all five Goal Signals printed. Failed
findings are terminal (never re-dispatched); when `Fixed + Failed == Eligible`
the pipeline is complete. Before relying on a `/goal` loop, read:

`${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/goal-pairing.md`
