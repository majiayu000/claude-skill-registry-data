---
name: eos-fix-drain
description: Run the dogfood-agent fix drain end-to-end with the pre-flight + post-revert safety gates that `apps/extension/dev/fix-agent` itself doesn't enforce. Use when the user says "drain the fix queue", "run the fix drain", "process pending fix-prompts", "fix-drain", or wants to apply N queued fixes overnight / in one batch. Wraps `POST /dogfood-agent/api/fix-drain/start` with the invariants documented in `docs/fix-agent.md` — refuses to launch on dirty state, verifies main is linear + free of orphan branches after each revert, surfaces 529/interrupt fallout for manual triage. NOT for queueing the fix-prompts (use eos-usecase-audit or the dogfood agent) and NOT for reviewing what a drained fix changed (use eos-agent-diff-review).
---

# EmptyOS Fix Drain

Operational runner for the dogfood-agent → fix-agent → sandbox verify → revert loop. The HTTP endpoint (`POST /dogfood-agent/api/fix-drain/start`) is fast but lossy — it launches the loop and trusts the operator to have checked everything else. This skill is the checked path.

Read `docs/fix-agent.md` once for the contract; this skill is the runner that enforces it.

## When to use

- "Run the fix drain" / "drain the queue" / "process pending fixes"
- Multiple fix-prompts queued in `data/apps/dogfood-agent/fix-prompts/` ready to apply
- Overnight batch of friction fixes after a dogfood-agent cron run
- After a stuck drain — rerun with this skill to surface what got left behind

## When NOT to use

- Single fix being iterated manually via `/fix-agent/` UI — that flow is one-click Apply, no skill needed
- The fix-prompt queue is empty (`ls data/apps/dogfood-agent/fix-prompts/*.md`) — surface that and stop
- `:9000` or `:9001` daemon unreachable — drain crashes on first call; fix daemons first
- A previous drain left `orchestrator_dirty: true` and `:9000` hasn't been restarted yet — restart first, then drain

## Pre-flight gates (refuse if any fail)

Run these checks before calling `start`. Bail with a clear diagnosis on the first failure — never proceed past a failed gate.

### 1. Working tree clean on main

```bash
git status --short
git rev-parse --abbrev-ref HEAD
```

Refuse if:
- Working tree has uncommitted changes (drain carries them into every fix's worktree via `git checkout -B <branch> main`)
- HEAD is not on `main` (`api_run_merge` will refuse anyway)

Surface the dirty files and ask the user to commit/stash before draining.

### 2. No orphan fix branches

```bash
git branch --list 'fix/*'
```

Refuse if any exist — they're leftovers from a previous crashed drain. Ask before deleting: each branch may represent a fix worth recovering. Safe path: surface the list, let the user `git branch -D` what they don't want.

### 3. No leftover worktree state

```bash
git -C .claude/worktrees/fix-agent status --short 2>/dev/null
git -C .claude/worktrees/fix-agent rev-parse --abbrev-ref HEAD 2>/dev/null
```

If the worktree directory exists but isn't on a `fix/*` branch (or doesn't exist as a worktree at all), fix-agent's reset cycle will recreate it cleanly — no action needed. Don't `git worktree remove` unless the path is corrupt.

### 4. Both daemons reachable

```bash
curl -fsS http://127.0.0.1:9000/api/health
curl -fsS http://127.0.0.1:9001/api/health
```

Refuse on either failure. `:9000` runs fix-agent; `:9001` is the verify sandbox. Don't try to restart them from this skill — daemon handling rule (`.claude/rules/daemon-handling.md`) forbids it.

### 5. orchestrator_dirty flag clear

```bash
cat data/apps/dogfood-agent/fix-drain.json | python -c "import sys, json; s = json.load(sys.stdin); print('DIRTY' if s.get('orchestrator_dirty') else 'clean')"
```

If `DIRTY`, the previous drain merged a fix that touched orchestrator code (drain.py, fix-agent's app.py, etc.). `:9000` is running stale code. **Refuse and tell the user to `restart.bat`.** After restart, the flag is cleared on next drain start.

### 6. Queue has at least one entry and one known-verifiable scenario

```bash
ls data/apps/dogfood-agent/fix-prompts/*.md 2>/dev/null | wc -l
```

If zero, stop. If non-zero, **strongly recommend** a single pre-flight verify before launching the full drain (per `feedback_drain_preflight_verify` memory — stashed WIP can split contracts across HEAD↔stash and make every verify a no-op):

> Before draining N fixes, run one verify against HEAD: pick the most recent pending fix, invoke `api_run` + `api_run_merge` + `api_run_verify` manually, confirm `verified`. If that one fails, the whole batch will fail — abort and investigate verify infrastructure first.

If the user skips this, note it in the launch announcement so it's clear what wasn't checked.

## Launch

Once all gates pass:

```bash
curl -X POST http://127.0.0.1:9000/dogfood-agent/api/fix-drain/start \
  -H 'Content-Type: application/json' \
  -d '{"max_fixes": <N>, "per_fix_timeout_s": 1500}'
```

Defaults: `max_fixes=5`, `per_fix_timeout_s=1500` (25 min). Cap `max_fixes` at 10 unless the user explicitly asks for more — a runaway loop is exactly what the kill-switch is for, but small batches make triage easier.

Announce to user: which `max_fixes`, which queued fix-prompts will run (`ls fix-prompts/*.md | head -N`), expected wall-clock (`N * (~5min code + ~3min verify)`).

## During the drain — what to monitor

The drain runs in the background; you don't need to poll continuously. Use `ScheduleWakeup` if checking back after a long wait — match the delay to expected duration of remaining fixes (e.g. 5 fixes × ~8 min = ~2400s, schedule for ~half that).

When you do check:

```bash
curl -s http://127.0.0.1:9000/dogfood-agent/api/fix-drain/status
```

Watch for:

- `result: "halted_orchestrator_dirty"` — a merged fix touched drain code; halt is correct, restart needed before next drain
- `result: "stopped_by_user"` — operator set `active: false`
- `result: "crashed"` — exception during `_drain_queue`; check `history[0].error`. **In-flight fix's state must be triaged manually** (see post-drain checks)
- High `stuck_count` relative to `applied_count` — verify infrastructure or fix quality issue; investigate before re-draining

## Post-drain invariants (verify after every drain)

These are the checks `api_run_revert` does NOT do. Run them after the drain reports `result != "in_progress"`.

### 1. Main is linear (no true merge commits introduced)

```bash
git log --merges main --since="$(date -d '4 hours ago' --iso=seconds)" 2>/dev/null || \
  git log --merges -n 50 main
```

Expected: **no output** (or only pre-drain merges). `--ff-only` should guarantee this; the check catches any case where the invariant breaks.

If a merge commit exists post-drain: surface immediately. Something bypassed `api_run_merge`'s ff-only gate (a manual `git merge`, a force-push, a config change). Don't auto-revert; the user investigates.

### 2. Every revert commit pairs with its target

```bash
git log --grep='^Revert ' --since="$(date -d '4 hours ago' --iso=seconds)" --format='%H %s'
```

For each revert, the original commit should be visible in `git log` before it. If a `Revert "X"` appears with no `X` ancestor, history was rewritten — investigate.

### 3. No leftover fix branches from this drain

```bash
git branch --list 'fix/*'
```

Successful merges leave branches in place by design. After a drain, expect one branch per `applied_count + stuck_count` entry. Optional cleanup (ask user first):

```bash
git branch --merged main | grep '^  fix/' | xargs git branch -d  # only fully-merged
```

Never `-D` (force-delete) automatically — a branch failing `-d` is an unmerged branch with potentially recoverable work.

### 4. Drain state recorded in history

```bash
cat data/apps/dogfood-agent/fix-drain.json | python -c "import sys, json; s = json.load(sys.stdin); h = s['history'][0]; print(json.dumps({k: h[k] for k in ['result','applied_count','stuck_count','finished']}, indent=2))"
```

Confirm `active: false` (drain finished) and `current: null`. If `active: true` after the drain should have ended, the `finally` block didn't run — investigate the daemon log.

### 5. Restart needed?

Any applied fix that touched daemon-loaded Python (`apps/**/*.py`, `plugins/**/*.py`, `emptyos/**/*.py`) needs a `:9000` restart to take effect. Surface the list:

```bash
git log main --since="$(date -d '4 hours ago' --iso=seconds)" --name-only --pretty=format: | \
  grep -E '^(apps|plugins|emptyos)/.+\.py$' | sort -u
```

If non-empty, tell the user to run `restart.bat`. Don't run it from a Claude tool — daemon-handling rule forbids it.

## When something fails mid-drain

The three failure windows (per `docs/fix-agent.md`):

1. **claude-cli phase fails** — fix-agent records `error`/`timeout`/`no-changes`. Branch may have partial edits; next iteration's reset wipes them. **Main untouched.** Drain continues with next pending.
2. **Merged but verify didn't kick off** — rare race; merge commit on main, no verify attempted. Drain marks `stuck` and proceeds. **Manual revert needed.** Surface in post-drain triage.
3. **Verify polled past timeout OR returned `target_fixed: false`** — drain auto-reverts (`drain.py:408-414`). Verify the revert landed cleanly per post-drain check #1.

If the drain itself crashed (`result: "crashed"`):
- Read `history[0].steps[-1]` to find the last step that ran
- Inspect that step's `run_id`'s status via `GET /fix-agent/api/runs/<run_id>`
- If status is `merged` or `verifying` and no revert recorded, decide: revert manually (`POST /fix-agent/api/runs/<run_id>/revert`) or accept the commit if it looks clean

## Stop signal (mid-drain abort)

```bash
curl -X POST http://127.0.0.1:9000/dogfood-agent/api/fix-drain/stop
```

This sets `active: false`. **The current iteration completes** (no mid-run interrupt) — including any in-flight verify and any revert it triggers. The loop checks the flag at iteration start (`drain.py:294-297`) and exits cleanly on the next boundary.

If the user wants harder abort: there isn't one. Killing the daemon (which they should NOT do) leaves whatever state the in-flight call was in. Tell them to wait for the current iteration.

## Anti-patterns to refuse

- **Skipping pre-flight gates** — "just run it, it's fine" is how stashed WIP makes every verify a no-op. The gates take 30 seconds; refusing to skip them is the value of this skill.
- **`max_fixes > 20`** — bigger batches mean bigger blast radius if verify infra is broken. Recommend splitting.
- **Running drain while the user is actively editing** — every drained fix could merge code that conflicts with their unsaved work. Check for active git activity (look at `git diff` line count or recently-modified files in `apps/`); surface and ask.
- **Bypassing post-drain checks** — the whole point of this skill is the checks. If skipping, just call the endpoint directly.

## Cross-references

- `docs/fix-agent.md` — full operational contract: worktree semantics, merge gates, revert mechanics, failure modes
- `.claude/rules/test-fix-verify-loop.md` — architectural shape
- `.claude/rules/daemon-handling.md` — why this skill never restarts daemons
- `apps/extension/dev/fix-agent/app.py:347-507` — merge, verify, revert handlers
- `apps/extension/dev/dogfood-agent/drain.py:266-436` — the `_drain_queue` loop
- Memory `feedback_drain_preflight_verify` — the lesson behind pre-flight gate #6
