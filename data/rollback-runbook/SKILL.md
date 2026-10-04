---
name: rollback-runbook
category: release
description: Use before and after calling rollback_release - what a rollback restores per delivery mode, when a schema change makes a code rollback unsafe, how to work and report manual_steps, and what to do when rollback_release refuses
source: ankane/strong_migrations (MIT), wshobson/agents (MIT), adapted
---

# Rollback runbook

`rollback_release` always reverts the release's task merge commits on the default branch and pushes that revert — production can never ship the bad change again, whatever else happens. What restores the RUNNING service depends on the component's delivery mode:

- **`dispatch`** — the previous good release's commit is tagged and the deploy workflow is dispatched at it (`Mechanism: workflow_dispatch`). No previous release: it dispatches at the revert commit instead.
- **`on_merge`** — the revert push itself is the redeploy (`Mechanism: revert_push`); there is nothing else to trigger.
- **`batch`** (desktop, mobile) — nothing is redeployed. `Status` goes straight to `rolled_back`: a published desktop build or a store build cannot be unpublished by reverting a git commit, so there is no redeploy for `watch_release` to follow. See `batch-artifact-verification` for the yank step.

For `dispatch`/`on_merge`, `Status` becomes `rolling_back` and you are expected to call `watch_release` again to follow the redeploy through to `rolled_back`.

## Before you roll back: check what schema the release changed

A code revert is not automatically safe. For each task in `release.tasks`, `get_task_pull_request({ task_id, include_diff: false })` to list files, then look for migration paths: `migrations/`, `db/migrate/`, `prisma/migrations/`, `alembic/versions/`, `V*__*.sql`, `*.up.sql`. Read the up file (`get_task_pull_request` with the diff, or `read_file`) for any match.

- **Additive** — `CREATE TABLE`/`CREATE INDEX`, `ADD COLUMN` that is nullable or has a constant default: reverting the code is safe. The previous version simply ignores the new objects — **leave the schema in place**; do not drop what the forward migration added.
- **Destructive or renaming** — `DROP COLUMN`/`DROP TABLE`, `RENAME COLUMN`/`RENAME TABLE`, `ALTER COLUMN TYPE`, `SET NOT NULL` on an existing column: the previous version may not run against this schema at all. If the task's `rollback_plan` covers it, follow the plan exactly. Otherwise do **not** call `rollback_release` — comment the evidence plus "a code rollback would run the previous version against a schema it does not know — needs a human: forward fix or a down-migration first", and stop.

This is the parallel-change pattern (DORA): decouple a database change from the application change that depends on it, so either one can revert on its own. A migration that only adds is reversible by the code revert alone; one that removes or reshapes is not, unless a plan already accounted for it.

## What a revert cannot undo

`git revert` undoes code. It does not:

- reverse a database migration,
- turn a feature flag back off,
- purge a CDN or cache,
- roll back a third-party configuration change,
- un-send a webhook, an email, or anything else the code triggered while it ran.

`rollback.manual_steps` is exactly this list, built from each rolled-back task's own `rollback_plan`/`before_deploy`/`after_deploy` fields — the developer who made the change is the only one who knew which of these applied.

## Batch releases add one more, first

For a `batch` release, `manual_steps` puts one entry ahead of the tasks' own: unpublish or halt the artifact the revert cannot touch. See `batch-artifact-verification` for the exact commands. Treat it like any other manual step: perform it if you can, report it if you cannot, and put it first in your report — it is the step that actually stops the bad build reaching more users, not the code revert.

## Work through it

1. Read every item in `manual_steps`.
2. Perform every one you can with the tools you have — most manual steps are outside this system's reach (a third-party console, a human-run command) and are for a human; `release-terminal-scope` names the one write you may make yourself.
3. Say explicitly, on the card, which ones you performed and which you could not, and who has to finish them.

✅ "Reverted the code (revert `a1b2c3d`). Left for a human: migration 043 added `tasks.priority` (`NOT NULL DEFAULT 'medium'`); the previous version ignores it, so it stays — dropping it would discard values written since the deploy. T-12's `after_deploy` enabled flag `new_pricing`: turn it off in the flag console. T-14 recorded no rollback plan."

❌ "Rolled back; the column added by migration 042 needs a human to drop it." — additive columns are not dropped; see "Before you roll back" above.

A rollback reported as complete when half of it was not is worse than one that admits what it did not do — the next release will ship on top of whatever was left half-undone.

## No plan recorded

If a rolled-back task recorded no rollback plan at all, say that too. The absence is a finding for whoever reviews this release next, not something to paper over with "nothing else to do here".

## When rollback_release refuses

Do not retry — a refusal here is final the same way a merge refusal is (`board_rollback_release_refused`):

- **Too old** (more than 24h since it was released) or **a newer release already shipped** — production now runs something newer than what you'd be rolling back to. One comment saying so, and that this needs a forward fix as a new task (a human or PM call), then stop.
- **A newer release is open** — resolve that one first; leave this one alone.
- **`verifying` or `deploying`** — the sweeper will hand it back to you at the right moment; stop and let it.
