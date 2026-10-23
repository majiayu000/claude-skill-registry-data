---
name: git-sync
persona: main-session
description: Run the guarded repository sync ritual; commit-time hooks enforce the cheap gates and the pre-push hook runs gz check.
category: agent-operations
lifecycle_state: active
disable-model-invocation: true
owner: gzkit-governance
last_reviewed: 2026-10-22
metadata:
  skill-version: "1.4.4"
model: haiku
---

# SKILL.md

## Git Sync

Run the guarded repository sync ritual with lint/test gates.

## Trigger

- User asks to "git sync" or "push with guards"
- End-of-task reconciliation before handoff
- Branch drift recovery after remote updates

## Behavior

Use the `gz git-sync` command flow (dry-run first, then apply as requested).

## Prerequisites

- Repository is initialized with `gz init`
- Current directory is a git worktree

## Steps

1. Preview planned actions:
   `uv run gz git-sync`
2. Execute the standard ritual:
   `uv run gz git-sync --apply`
3. Explicit redundant-gate invocation (edge cases only, e.g. verifying
   pre-commit config drift):
   `uv run gz git-sync --apply --lint --test`

> Both dry-run and apply mode run `git fetch --prune <remote>` before
> reading `ahead`/`behind`, so divergence numbers always reflect current
> remote state — no separate pre-fetch needed (GHI #343). When the
> network is unreachable the dry-run reports the fetch failure as a
> warning and proceeds with cached refs; apply-mode treats it as a
> blocker.

> The pre-commit hook runs the CHEAP gates on every commit — ruff, ty,
> the complexity ceiling, complexipy, gitleaks, authorship. It does NOT run the unit
> suite: `unittest` is declared `stages: [manual]` in
> `.pre-commit-config.yaml` and fires only on demand
> (`pre-commit run unittest --hook-stage manual`). The tests a change
> touches reach a push through the separate `gz-check-pre-push` hook, which
> runs `gz check --reuse-verified`; the whole unit tier runs in CI
> (GHI #1191). `--lint` and `--test` re-run those gates at
> the `gz` level — redundant for the normal ritual and multi-minute pain.
> Defaults were flipped to `False` to match this reality (airlineops
> parity evolution).

## Examples

### Example 1

**Input**: "git sync"

**Output**: Runs `uv run gz git-sync --apply` (or dry-run first if safety confirmation is needed). Pre-commit hook handles lint/test automatically.

## Append-only JSONL conflicts

The runtime appends to `.gzkit/ledger.jsonl` (and `agent-insights.jsonl`,
`corpus/*.jsonl`) during every session, so two clones in flight conflict over
disjoint tail additions. `uv run gz git-sync --apply` registers a git merge
driver — `uv run gz ledger merge-driver` — that reconciles them as a
**timestamp-ordered union**. Registration is idempotent and per-clone, because
git reads a driver command from local config, which cannot be committed.

**Never hand-edit `.gzkit/ledger.jsonl` to clear a conflict.** That is the
action `AGENTS.md` § Behavior Rules prohibits (the ledger is written only through `gz` commands), and the driver exists so you do not
have to. If the driver exits 1, a side did more than add rows — an ancestor row
was edited or removed, a row carries no sortable `ts`, or the ancestor was
already out of ts order — and it left the conflict for you deliberately. An
addition never lands there, wherever in the file it sits (GHI #1075). Resolve as
a timestamp-ordered union; never append one side to the other, which is what
git's built-in `merge=union` would do and why it is not used here (the ledger is
strictly ts-ordered — `gz validate --ledger`).

## Constraints

- Never use force push in this routine.
- Resolve blockers (divergence, lint/test failures) before retrying.
- Use `uv run` invocation style for project commands.

## Common Rationalizations

These thoughts mean STOP — you are about to push without the guards:

| Thought | Reality |
|---------|---------|
| "Force push, it's just my branch" | The constraint is explicit: never use force push in this routine. "Just my branch" still rewrites history and can desync local clones. Resolve divergence the long way. |
| "Lint is failing on something cosmetic — ship it" | The lint/test gates exist because cosmetic failures often hide real ones. The whole point of the ritual is that you don't get to triage at sync time. Fix or revert. |
| "I'll skip `--lint --test` to be quick" | The bare `--apply` exists for git-only operations. Skipping the quality gates on a code change is the failure mode the ritual was designed to prevent. |
| "Divergence with remote — just rebase and force" | Investigate first. Divergence may mean another agent or another machine pushed work you don't have. Force-pushing destroys it. |
| "Dry-run looks fine, no need to actually run --apply" | Dry-run shows the plan; apply executes it. Walking away after dry-run leaves the local tree out of sync, which the next session inherits. |
| "Pre-commit hook failed — `--no-verify` it" | Hooks are part of the contract. Skipping them with `--no-verify` is the same anti-pattern as skipping `--lint --test`. Diagnose, don't bypass. |
| "I'll commit and sync separately" | The ritual includes the sync step deliberately. Committing without syncing leaves the branch behind on the remote, which is exactly the divergence trap. |

## Red Flags

- Force push appearing anywhere in the routine
- `--no-verify` used on the commit
- Lint or test failures bypassed instead of fixed
- Divergence resolved by reset/force instead of investigation
- Dry-run run without follow-through apply
- Sync run on a tree with uncommitted control-surface drift

> Two hooks are the mandatory gate: the commit-time cheap gates
> (ruff + ty + the complexity gates + guards) and the pre-push `gz check`, which runs every
> validator and the tests the change touches. The whole unit suite runs in
> CI on every code push. Explicit `--lint --test` flags are
> redundant for the normal ritual (see Steps § 3). Omitting them is not a
> red flag — skipping either hook via `--no-verify` is.

## Related Skills

- `lint`
- `test`
- `format`
