---
name: ci
description: >-
  Triage the current branch's CI. Find the relevant current-head run, wait if pending, diagnose
  failures without flooding context, compare against main when appropriate, and report or fix. In
  fix mode, push and re-watch until the new current HEAD is green. Never merge.
argument-hint: "[fix] [optional PR number / run id]"
---

Get the current branch's CI green. `$ARGUMENTS`: `fix` applies fixes; explicit PR/run overrides auto-detect.

This skill inherits caller model/effort. Raw logs never enter the calling context.

## Find and watch

- Detect branch/PR and current HEAD SHA.
- Find checks/runs that actually cover that SHA; do not mistake an older green run for current-head coverage.
- Pending ⇒ wait with the shared poller: launch `${CLAUDE_PLUGIN_ROOT}/scripts/ci_poll.sh poll <pr> --repo <the PR's base repository, never a fork's own origin>` as a single token-free `run_in_background` Bash call (it sleeps between checks and exits when nothing is pending); add `--head <SHA>` whenever triage already knows the expected head, so a stale or empty check set cannot read as green. Never hand-write a poller loop. Never poll once per reasoning turn and never self-resume a monitor at a turn-budget boundary; both bleed tokens on a large matrix. Its default 1800s timeout comes from `ci.poll_timeout` — raise it for repos/matrices whose CI routinely runs longer, so a single call spans the wait instead of timing out and bouncing to the parent.

## Diagnose failure

Use `sy:sweep` for large failing logs; it returns failing jobs/tests, a few decisive root-cause lines, and implicated code pointers. If the failure surface is tiny, read the small error region directly. Never page full logs.

Before calling something pre-existing, verify the corresponding latest main job when relevant. Distinguish branch bug, inherited main breakage, flake, resource limit, dependency drift, and infra/auth/network failure.

## Report or fix

- Report: failing job, real error, cause, concrete fix.
- `fix`: apply, run local reproducer/checks, push, and re-watch the **new HEAD** until green.

Return status plus the SHA covered:

```text
CI status: green | fixably-red | blocked
CI_GREEN_SHA: <sha or none>
```

Never merge.

Every subagent dispatch resolves its model from config and passes it as the `Agent` invocation's actual model override, per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`; a nested dispatch inherits nothing and must resolve again.
