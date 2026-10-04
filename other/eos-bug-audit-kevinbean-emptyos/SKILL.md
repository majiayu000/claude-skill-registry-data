---
name: eos-bug-audit
description: Hunt correctness/concurrency bugs in EmptyOS the way an external auditor would — run the deterministic static scanners, triage findings with false-positive discipline, do a browser UI walk, fix at root cause, and live-verify the riskiest fixes on a leased sandbox (never on :9000). Use when the user says "audit", "audit for bugs", "find bugs", "check the system for bugs", "work as an auditor", or wants a correctness/robustness sweep. The two high-yield bug classes are sync-in-async event-loop wedges (daemon freeze) and vault read-modify-write races (silent data loss). NOT for architecture/wiring review (use eos-architecture-review), changed-code quality review (use eos-simplify), security posture (use eos-security-review), UI design (use eos-page-design-review / eos-design-system-audit), or KB note↔calculator/reference consistency (use eos-kb-audit).
---

# EmptyOS Bug Audit

Find and fix real correctness bugs — not style, not feature gaps. The two veins
that pay out in this codebase (proven across a 19-fix audit run):

1. **Sync-in-async event-loop wedges** — a blocking call (`subprocess`/`requests`/
   `urlopen`/`time.sleep`/sqlite) on the event loop freezes the *whole daemon* for
   its duration. Caught the `/topology` git freeze, capture/promote/drain stalls.
2. **Vault read-modify-write races** — `read(X)` → mutate → `write(X)` on a shared
   file with no `write_lock` silently drops a concurrent writer's change. Caught
   capture / canvas-node / expense-row data loss.

Everything else (contract drift, input-coercion 500s, swallowed exceptions) is
mostly **noise floor** here — the codebase is well-validated. Don't manufacture
fixes from it.

## The loop (run phases in order; stop when the well is dry)

### 0. Read the prior backlog FIRST (loop memory — load-bearing)
This skill is built to be re-run (`/loop`, `/schedule`). Before scanning, read
`data/audit-loop/backlog.md` if it exists — it carries prior FIXED / WONTFIX /
DEFER findings + rejected false-positives. Two reasons it's load-bearing:
- **Don't re-litigate** settled FPs/deferrals. Wasted tokens, and the codebase
  converges fast — a prior run may have already swept everything, so a fresh
  cold scan mostly reproduces known-noise.
- **Deferrals are where the next bug hides.** The highest-yield move on a re-run
  is to re-examine the prior run's "per-entity / low-concurrency" deferrals
  against the *actual* write target — a shared file mislabelled "per-entity" is
  exactly the missed-bug shape (the 2026-06-16 shared-inbox `add_task_to_project`
  race was found this way, after a 21-iteration prior run had deferred it).
- **Run the partial-lock discriminator per APP DIRECTORY, never per file.** The
  discriminator: does this app have `write_lock`/`note_lock` writers of a note AND
  an unlocked writer of the same note? >0 locks + an unlocked writer = a real
  partial-lock bug (the lock is false safety). 0 locks anywhere = consistently
  unlocked per-entity = defer. Apps are multi-module now, so a per-*file* grep
  reports 0 locks for a sibling module and the file reads as benign — that is how
  the 2026-07-18 publish hole (scheduling.py locked; media.py's 4 writers unlocked,
  so a scheduled release's `publish: true` was silently clobbered and the post
  never went live) survived FIVE runs classified as safe. Count over the whole app
  dir: `grep -rc "write_lock\|note_lock" apps/<track>/<app>/*.py`.

If no backlog exists, this is a first run — proceed to phase 1.

### 1. Baseline (cheap, offline)
- `python -m pytest tests/ -k "sdk or unit" -q` — pure-logic layer (~1900 tests).
- `curl -s :9000/api/health` + verb-drift sweep `GET /agent/api/verbs/sweep?load=1`
  (needs `Authorization: Bearer <auth_token>` from `emptyos.toml [network]`).
- HTTP page-load smoke: fetch every `/{app}/` (`GET :9000/api/apps` for the list),
  flag non-200 / Traceback bodies. 180+/181 should be clean.

### 2. Run the deterministic scanners (the durable, graduated checks)
```
python scripts/preflight.py --scope always,vault   # runs the registry below
python scripts/check-asyncio-blocking.py            # 4 rules; see blocking-in-async
python scripts/check-vault-rmw-race.py              # shared-file RMW races
```
- `check-asyncio-blocking.py` rule **blocking-in-async** = direct + intra-file
  transitive blocking primitive reached from an `async def`. ADVISORY.
- `check-vault-rmw-race.py` = read→write on the same path with no lock. Recognizes
  `write_lock`, `note_lock`, and any `*_lock` helper that RETURNS one (apps wrap a
  canonical key that way — `task._file_lock` borrows the projects lock). Tolerance is
  FUNCTION-scoped, so an unlocked sibling of a locked writer is still flagged — do not
  widen it to file scope or the partial-lock vein goes dark. ADVISORY (per-entity files
  are benign; shared-file writers are the real ones). Both directions are pinned by
  `tests/test_unit_check_vault_rmw_race.py`.
- **Prefer `self.note_lock(path)` for a vault note**, not `write_lock`: it is
  kernel-wide (shared across app *instances*) and normalizes abs/rel spellings, so it
  excludes writers `write_lock` would miss. Don't hand-roll a per-app lock helper for
  a note — that primitive already exists.
- These graduated from one-off scans (audits.md). To add a class, extend the
  scanner, don't re-roll a throwaway.

### 3. Triage — FALSE-POSITIVE DISCIPLINE (the load-bearing step)
A prior agent reported **5 settings + 30 CLI + 376 coercion = 37 false positives**.
Before fixing ANYTHING:
- **Verify both sides yourself against committed `HEAD`** (`git show HEAD:<file>`),
  never trust a sub-agent's grep. (audits.md)
- **Run the heuristic against 3 known-healthy targets** (hub/task/journal). Anything
  that fires on healthy code is noise — tune or drop it.
- **Skip files with uncommitted edits** (`git status --short`) — they're likely a
  parallel session's in-progress work; editing them collides. Audit committed code.
- **Severity = does it hurt in NORMAL use?** all-users-every-action (capture,
  /topology) >> explicit-dev-operation, low-concurrency (fix-agent, model-bench).
  Document-and-defer the latter; don't mass-edit working dev tools for marginal gain.

### 4. Fix at root cause (debugging.md)
- Wedge fix: `x = await asyncio.to_thread(blocking_fn, ...)`. For a sync helper
  chain, wrap at the async caller (or add an `async def *_async` wrapper).
- Race fix: `async with self.write_lock(f"<ns>:{key}"):` around read→mutate→write;
  **emit stays OUTSIDE the lock** (handler recursion would deadlock). Reference:
  journal `_daily_lock`, quick-action capture lock.
- **DEADLOCK CHECK before locking**: a lock is only safe if the locked methods
  don't call each other with the same key (`asyncio.Lock` is not reentrant).
  expense `set_field` called the locked `add()` → had to inline a non-locking leaf
  (`_append_row`) instead. Verify the call graph first.
- Write a failing test first where practical (`tests/test_unit_*.py`), then fix.

### 5. Verify
- Offline: `python -m py_compile <file>` + the new/existing unit tests.
- Live (for kernel/runtime/core fixes): **lease a sandbox**, never touch :9000.
  `POST :9000/sandbox/api/lease` → it boots fresh from the working tree (picks up
  edits) → probe `<host>` → `DELETE .../lease/{id}`. For a race fix, fire ~10
  concurrent writes and confirm all persisted. For a wedge fix, run the heavy op
  and confirm `/api/health` stays responsive (sub-second) concurrently — that
  *is* the proof the loop didn't freeze. See `.claude/rules/sandbox-driven-testing.md`.

### 6. Record
Keep a running backlog (e.g. `data/audit-loop/backlog.md`): findings, status
(NEW/FIXED/WONTFIX/DEFER), verification, and FPs rejected (so the next run doesn't
re-litigate them — this is what phase 0 reads). **Append a new dated section per
run; never overwrite** — the carried history is what makes the loop compound
instead of restarting from a cold scan each time.

## Hard rules
- **Never restart/kill :9000 or :9001, never touch `data/*.db`** (daemon-handling.md).
  Verify Python fixes on a leased sandbox; ask the user to `restart.bat` for :9000.
- **Never `git add -A` / commit** unless asked — keep audit fixes separate from any
  parallel-session changes. When you do commit, commit by **explicit pathspec**
  (`git commit -- <paths>`), never a bare `git commit` even after `git add <paths>`:
  a parallel session can stage its *own* files between your `add` and `commit`, and
  a pathspec-less commit sweeps them in. Verify `git show HEAD --stat` lists only
  your files afterward; if not, `git reset --soft HEAD~1` and re-commit with the
  pathspec.
- **Don't write test fixtures into the real vault** — concurrency/write tests run on
  the sandbox (its own throwaway vault), not :9000.

## Cross-references
- `scripts/check-asyncio-blocking.py`, `scripts/check-vault-rmw-race.py`,
  `scripts/check_call_app_declared.py` — the graduated scanners (in `scripts/preflight.py`).
- `.claude/rules/audits.md` — FP discipline + graduation; `.claude/rules/debugging.md`
  — root-cause + the async-wedge catalog; `.claude/rules/sandbox-driven-testing.md`
  — the lease/verify loop; `.claude/rules/daemon-handling.md` — hands off :9000.
- CLAUDE.md § Development Gotchas — vault RMW race; § async-wedge catalog.
