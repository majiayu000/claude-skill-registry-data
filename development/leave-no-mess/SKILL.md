---
name: leave-no-mess
description: Clean up a session's side effects — background processes and ports, temp files, debug scaffolding, seeded test data, stashes, config and env changes — and name what has to stay. Use before the final report on any task that started servers or watchers, wrote scratch or repro files, added logging or debug output, seeded databases, registered webhooks or test accounts, or changed configs, env vars, or branches. Not for reviewing the intended diff itself.
---

# leave-no-mess

Weak cleanup looks like: reporting "done" with a dev server still holding :3000, a `repro.py` in the repo root, and `console.log('HERE')` in three files. Strong cleanup leaves the workspace as you found it plus the intended diff, and names anything that had to stay. The task isn't the diff alone; it's the diff plus a workspace in the state you found it.

## Sweep, in this order

1. **Processes and ports.** List background tasks you started this session (the harness's task list, plus `ps` / `Get-Process` for anything a script spawned) and stop each one — dev servers, watchers, containers, tunnels. Confirm the port is free afterwards (`lsof -i :<port>` / `netstat -ano | findstr :<port>`). A zombie from your session is the "port already in use" mystery in the user's next one.
2. **Scaffolding in the diff.** Read `git diff` hunk by hunk (see workmanship): debug prints, log-level flips, hardcoded test values, commented-out experiments, `TODO(remove)`, skipped or `.only` tests, timeouts you shortened. Everything left should be the change, not the process of finding it.
3. **Files you created.** `git status --porcelain`: every untracked path is yours to classify — deliberate artifact (keep) or repro script / downloaded sample / generated fixture (delete, or move to the scratchpad). Also check ignored locations you wrote to (`git status --ignored`: build dirs, caches, `.env.local`).
4. **State you changed outside the repo.** Undo: seeded or mutated rows in a shared database, edited local or global configs, env vars exported for one run, git stashes you created, feature flags toggled, test users / webhooks / sandbox records registered against real services. External artifacts especially — nobody else knows they exist.
5. **Working-tree position.** Same branch you started on unless moving it was the task; nothing of the user's left stashed; no half-applied migration.

## What stays, and how to say so

- **Deliberate artifacts are not mess** — the new fixture, the added script, the updated lockfile. The test is intent: did the task need this to exist afterward, or did *you* need it during?
- **What you can't or shouldn't clean, report explicitly**, one "Left in place:" line each: `dev server on :3000 for your review (stop with ...)`, `migration 0042 applied to local db`, `cache in .next/ will rebuild`. A named leftover is a handoff; an unnamed one is a mess.

## Exit check

Before the final report: `git status` shows only intended changes; every process you spawned is stopped or listed under "Left in place"; every external test artifact is deleted or listed. If any item is unverified, say so rather than assume.
