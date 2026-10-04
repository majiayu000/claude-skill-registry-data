---
name: ci-watch
description: Inspect current CI state, identify the first real blocker, separate required failures from noise, and monitor until checks settle. Use when checks are failing, flaky, or blocking a merge.
triggers:
  - ci watch
  - failing checks
  - check the pipeline
  - ci blocker
  - checks failing
---

# ci-watch

Use for broken checks, flaky tests, or merge-blocking pipeline noise.

## Phases

### Phase 1 — Triage
1. Identify the active PR or HEAD commit.
2. List non-passing checks.
3. Separate required failures from advisory noise.

Read PR state: `gh pr view N --json mergeable,mergeStateStatus,reviewDecision,statusCheckRollup`

### Phase 2 — Diagnose
4. Inspect the first failing required job deeply (logs, not just the summary line).
5. Name the smallest fix — or the exact reason the failure is pre-existing / unrelated to the current change.

### Phase 3 — Fix or Monitor
6. If fixable: apply smallest fix, push, watch checks settle.
7. If not fixable now: document the blocker and surface it as output.
8. For checks that take >1 min to settle: use a Monitor until-loop rather than busy-waiting.

## Output

```
BLOCKED — <job name>: <one-line cause>
  Fix: <smallest concrete action>
  Blocks shipping: yes / no

CLEAR — all required checks green
```

## Reconciliation

```
CI WATCH — <PR/SHA>

Phase 1 Triage:   N failing checks (<X> required, <Y> advisory) ✅
Phase 2 Diagnose: root cause: <description> ✅
Phase 3 Fix:      <action taken> | (blocked: <reason>) ✅

Result: RESOLVED | BLOCKED (requires: <what unblocks it>)
```

## PR state machine

| mergeable / state | Action |
|---|---|
| `MERGEABLE` + `CLEAN` | proceed to merge |
| `MERGEABLE` + `UNSTABLE` | non-required check failing; poll required-only checks |
| `MERGEABLE` + `BEHIND` | `gh pr update-branch` or local rebase + force-push |
| `MERGEABLE` + `BLOCKED` | check `reviewDecision` and branch protection |
| `CONFLICTING` + `DIRTY` | local rebase first; if GH disagrees → webhook desync, close+recreate |
| `UNKNOWN` + `UNKNOWN` | wait 15s, recheck; if STILL UNKNOWN try `gh pr merge` directly |

## Common gotchas

- `UNKNOWN` often means the PR was already merged in another window.
- `mergeStateStatus: BLOCKED` with no failing checks = review or branch protection.
- PR head SHA disagrees with `git ls-remote` = webhook desync. Close + recreate.
