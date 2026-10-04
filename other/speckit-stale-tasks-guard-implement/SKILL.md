---
name: speckit-stale-tasks-guard-implement
description: Halt /speckit-implement when spec.md is newer than tasks.md
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: stale-tasks-guard:commands/implement.md
---

## Stale-Tasks Guard (lifecycle hook — before_implement)

The `before_implement` hook invoked this command before the `/speckit-implement` body
runs, so this guard applies no matter which preset owns that body.

Hook targets do not receive the triggering command's `$ARGUMENTS`. This is a best-effort
check, not a tool-enforced gate: look at the arguments the user actually typed on the
`/speckit-implement` invocation still visible earlier in this conversation. If `--force`
appears anywhere in them, log `⚠️ Stale-tasks guard skipped (--force)` and skip the rest
of this section.

1. **Resolve the script path and run it:**
   ```bash
   ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
   SCRIPT="$ROOT/.specify/extensions/stale-tasks-guard/scripts/python/stale_tasks_guard.py"
   if [ -f "$SCRIPT" ]; then
     python3 "$SCRIPT"
     STATUS=$?
   else
     echo "stale-tasks-guard script not found — skipping guard" >&2
     STATUS=0
   fi
   ```

2. **Check `STATUS`:**
   - `0` — not stale, or the guard didn't apply (missing `spec.md`/`tasks.md`, or an
     unresolvable feature directory — either way the script printed why on stderr,
     and this is **not** a staleness signal). Proceed to the implementation loop.
   - `1` — the script printed a `STALE TASKS DETECTED` banner with the delta and next
     steps. Halt immediately, print that banner, and do **not** invoke
     `/speckit-implement`'s body. No implementation code is written until the operator
     reconciles tasks (`/speckit-tasks`) or opts in with `--force`.

The script resolves the feature directory the same way core Spec Kit does (`common.sh`'s
`get_feature_paths()`): the `SPECIFY_FEATURE_DIRECTORY` env var first (an explicit
override, e.g. a temporarily pinned feature), falling back to `SPECIFY_FEATURE` and then the current git branch (`specs/<branch>`).
It then compares each file's last-commit time (falling back to its filesystem mtime only
when the file has uncommitted local changes), not raw mtime — a plain mtime comparison
would be defeated by `git checkout`/clone resetting both files' mtimes to checkout time
in a fresh worktree.

## Failure Policy

- Exit `1` from the script is a hard stop before the implementation loop starts for this
  hook invocation — but the `--force` check above depends on the orchestrating agent
  correctly recalling the original invocation's arguments, since hook targets get no
  `$ARGUMENTS`. Treat it as a strong safeguard, not an unconditional guarantee.
- A skip (exit `0` with an stderr note) is not stale tasks; the core command's existing
  error paths for a missing `spec.md`/`tasks.md`/feature directory are unchanged.