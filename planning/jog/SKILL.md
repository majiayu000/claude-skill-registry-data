---
name: jog
description: Immediate serial task queue execution engine and conversational capture skill. Use when an operator wants to queue, prioritize, inspect, or execute a sequence of tasks one at a time today without marathon wave planning or concurrency overhead. Re-uses the Releases SQLite DB, driver lock, Marathon's reviewed one-phase executor (default since GH-280), and swarm-preflight.
---

# /jog — Serial Immediate-Queue Execution Engine

`jog` manages a serial queue of tasks for immediate execution today. It provides conversational task intake and runs tasks one by one with zero concurrency overhead, using `releases.db` (`jog_queue` table), the outer `relay-driver.lock`, and `swarm-preflight`. Since the GH-280 recalibration, per-task execution defaults to Marathon's reviewed one-phase driver (`--executor marathon`); `--executor relay` keeps the legacy single-phase `relay-drive` path as the documented rollback during a bounded compatibility window.

## Conversational Triggers

When the operator speaks naturally:
- `"jog GH-123"`:
  1. Validates the issue via `gh issue view 123`.
  2. Ensures a capture doc exists (in `PROJECT/1-INBOX/` or `PROJECT/2-WORKING/`).
  3. Ensures the issue is parked in the roadmap ledger (`releases roadmap add`).
  4. Enqueues the issue into `jog_queue` (`releases jog add GH-123`).
  5. Echoes: `jog: enqueued GH-123 at position N`.

- `"jog task above"`:
  1. Extracts the immediate task/bug discussion from recent context.
  2. Creates the tracking GitHub issue via `gh issue create` (issue-first SOP).
  3. Writes the initial capture doc to `PROJECT/1-INBOX/GH-<num>-<title>.md`.
  4. Parks the issue in the roadmap ledger (`releases roadmap add`).
  5. Enqueues into `jog_queue` (`releases jog add <num>`).
  6. Confirms the newly created issue number and queue position with the operator.

## CLI Commands

All commands run through `python3 utils/py/releases_app.py jog <subcommand>` (or `releases jog <subcommand>` when aliased):

```text
releases jog add <GH-NUM|doc-path> [--pos N] [--dry-run]
    Enqueue a task at the end of the queue (or at a specific position).

releases jog list [--all] [--json]
    Display active queue items (or all historical items with --all).

releases jog bump <GH-NUM>
    Move an active task to position 1 (head of line). Refuses terminal rows.

releases jog drop <GH-NUM> --reason "<text>" [--force]
    Mark a task as dropped with an auditable reason. Refuses already-completed items without --force.

releases jog retry <GH-NUM>
    Reset a failed, parked, or dropped task back to pending.

releases jog skip <GH-NUM> [--reason "<text>"]
    Park the current head task and advance to the next item.

releases jog clear
    Archive completed/dropped/parked terminal items.

releases jog to-marathon
    Export active jog items to marathon format.

releases jog resume <GH-NUM>
    Reconcile durable Marathon state for an item (spends no token).

releases jog retry-gate <GH-NUM>
    Re-run ONLY the gate against the same head SHA (no builder turn).

releases jog retry-build <GH-NUM>
    Fresh Marathon attempt on a fresh execution id (history preserved).

releases jog land <GH-NUM> [--pr N]
    Verify merged delivery against GitHub truth, complete the row, delegate lifecycle to wave_reconcile.

releases jog reconcile <GH-NUM>
    Idempotent replay entry for jog land (same verification and steps).

releases jog run [--executor relay|marathon] [--reviewer <agent>] [--builder agy|codex|aider] [--auto-merge] [--max-tasks N] [--simulate] [--dry-run]
    Execute the serial jog runner loop. Default executor is marathon (GH-280); --reviewer is
    required (builder and reviewer must differ). --executor relay selects the legacy rollback
    path during its compatibility window.
```

## Runner Execution Lifecycle (`jog run`)

1. **Outer Driver Lock & Hermetic Dry-Run:**
   - `--dry-run`: Hermetic simulation with zero locks and zero mutations (leaves queue and DB untouched).
   - Real run: Acquires `relay-driver.lock` via `rtl.driver_lock_path()`, sets `RELAY_DRIVER_LOCKED=1`, and registers a clean exit handler. Concurrently running marathons or relays in the same clone are safely excluded (GH-42 / GH-354).

2. **Receipt-Backed State Transitions:**
   Every runner transition (lease acquisition, status changes, orphan reconciliation) goes strictly through `perform_write` in `releases_app.py`, ensuring full journal, receipt-chain, and dump integrity. `lease_pid` is excluded from the committed `releases.sql` dump to eliminate merge conflicts.

3. **Startup Lease Reconciliation:**
   Inspects `jog_queue` for orphaned `running` rows (dead `lease_pid`). Resets them to `pending` (or `parked` if `attempt_count >= 3`).

4. **Fire-Time Promotion & Probe Linting:**
   If a task's capture doc is in `PROJECT/1-INBOX/`, `jog run` promotes it to `PROJECT/2-WORKING/`, formats the status table, and lints its `fix_probes`:
   - Rejects trivial or dummy probe patterns (e.g. `exit 0`, `true`).
   - Requires referenced probe scripts/globs to resolve to actual files.
   - In interactive mode, prompts operator to approve drafted probes before running preflight.
   - In unattended mode, unreviewed auto-scaffolding without verified probes is parked with `unreviewed-probe-contract` to prevent false-green runs.

5. **Swarm Preflight:**
   Runs `swarm-preflight --gh-issue <n>`:
   - `ready` (exit 0) -> fires the executor (Marathon one-phase drive by default).
   - `already-landed` (exit 4) -> marks `completed` with auto-drop receipt.
   - `not-ready` -> marks `parked`, records error, and prompts operator.

6. **Marathon Executor Dispatch (default; GH-280):**
   Per-task execution is delegated to Marathon's reviewed one-phase driver: Jog validates the
   preflight packet's `marathon-invocation@1` contract, invokes the drive, and projects the
   validated `marathon-drive/result@1` receipt. Attempts, review, gates, branch/commit, and PR
   identity are Marathon-owned; Jog records a receipt-backed projection, never a guess. Builder
   and reviewer are separated: `--builder` defaults to the cost-blind lanes (`agy`; `codex`/`aider`
   selectable) while `--reviewer <agent>` is required, must differ from the builder, and has no
   silent default. `--executor relay` keeps the legacy single-phase `relay-drive.sh` dispatch as
   the explicit rollback path during a documented compatibility window; it will be removed in its
   own dedicated commit one release cycle after the flip — do not build new usage on it.

7. **Receipt-Backed Landing & `--auto-merge`:**
   A row is never marked `completed` on a self-report. `jog land` verifies GitHub truth first —
   merged state, merge-SHA reachability, PR identity (repo, base, head, head SHA), and qualifying
   gate evidence — then completes the row and delegates issue closure, doc promotion, and
   dashboard refresh to `wave_reconcile`.
   - **Default (Interactive):** Pauses at each landing boundary for human confirmation. On confirm: merges PR into `development` and re-anchors the checkout. On decline: marks row `parked` (`awaiting-landing`) so unmerged tasks are never misrepresented as `completed`.
   - **Unattended without `--auto-merge`:** Parks row as `parked` (`awaiting-landing (unattended run without --auto-merge)`) and halts advance.
   - **`--auto-merge` (verified, GH-300):** Verifies GitHub truth against the receipt BEFORE merging — the PR must still be OPEN on the receipt's base/head/head SHA in this repo with the gate green on that head — and refuses (parking the row) instead of merging blind; on pass, merges into `development` and re-anchors the checkout before advancing.

8. **Teardown Cleanliness:**
   Verifies clean worktree disposal, clean working tree status, and gate receipts between serial items.
   At campaign end, point the operator at `/merge-cleanup` to retire the task clone (GH-690).

## Recovery Verbs

After an interrupted or failed item, pick the verb that matches what actually needs redoing:

- `jog resume <GH-NUM>` — the crash/restart remedy: reconciles the durable Marathon state and
  re-projects a valid terminal receipt without spending a token (parks instead of silently
  re-firing when state is missing or contradictory).
- `jog retry-gate <GH-NUM>` — the "approved relay, red gate" remedy: re-runs ONLY the gate against
  the same head SHA with no builder turn, for failures fixed outside the build (e.g. operator
  intake-hygiene fixes).
- `jog retry-build <GH-NUM>` — the real rebuild: a fresh Marathon attempt on a fresh execution id
  when the build itself must be redone; all prior Tick history and execution records are preserved.
