---
name: codex-local-cleanup
description: Safely inspect, clean, and repair local Codex Desktop project and thread state under $CODEX_HOME or ~/.codex when removed projects, deleted workspace paths, archived threads, failed thread archive operations, or mobile-visible sidebar entries remain; use current local-project metadata and the App Server thread API first, back up before writes, preserve active projects/projectless chats/current thread by default, and reserve direct SQLite repair for verified fallback cases.
---

# Codex Local Cleanup

Clean or repair local Codex Desktop project and thread state without touching user source projects.

## Safety Rules

- Treat `~/.codex` as live application state. Keep the first pass read-only.
- Require an explicit target set and create a backup before any write.
- Never delete or rewrite `auth.json`, `installation_id`, `skills/`, `plugins/`, `automations/`, `.sandbox-secrets/`, or user source projects.
- Never clean the current thread. If its ID cannot be identified reliably, stop before writes.
- Never archive-repair the current thread. Require its resolved ID before applying a repair to another thread.
- Preserve projectless/general chats unless the user explicitly includes them.
- Preserve automation threads and automation-run state unless the user explicitly targets a removed automation and its runs.
- Prefer the Desktop **Remove** action for a project first. Use this workflow when the project or its threads remain visible after removal and refresh/restart.
- Prefer supported App Server lifecycle methods over direct session-file or SQLite edits.
- For a failed archive request, retry the supported thread archive method and verify both active and archived lists before considering direct repair.
- Do not expose secrets from historical titles, previews, prompts, paths, or backups.
- Before deleting rollout files, resolve and verify every path is below `~/.codex/sessions` or `~/.codex/archived_sessions`.

## Cleanup Modes

Keep these scopes separate:

- **Visibility cleanup**: stale project definitions, assignments, sidebar state, and selected project threads. Use this by default.
- **Archive cleanup**: archived threads selected by the user. Do not infer consent from a visibility-cleanup request.
- **Archive repair**: move one explicitly identified, non-current active thread into the archive after the supported archive method fails. Preserve the conversation and do not treat this as deletion.
- **Storage cleanup**: diagnostic logs, old backups, and database compaction. Run only when the user asks to reclaim space.
- **Repair fallback**: direct JSONL or SQLite repair after the supported API is unavailable, fails, or leaves a proven orphan.

## Current Data Model

Inspect local files only. Discover versions and schemas instead of assuming fixed filenames or tables.

- `.codex-global-state.json` and `.bak`:
  - Current project definitions: `local-projects`, whose entries contain `id`, `name`, and one or more `rootPaths`.
  - Current project visibility/order: `project-order`, `pinned-project-ids`, `selected-project`, and `active-workspace-roots`.
  - Current thread mapping: `thread-project-assignments`, including `projectId`, `projectKind`, `cwd`, optional `path`, and `pendingCoreUpdate`.
  - Projectless state: `projectless-thread-ids`, `thread-projectless-output-directories`, and `thread-workspace-root-hints`.
  - UI state under `electron-persisted-atom-state`, including thread descriptions, unread IDs, client IDs, browser/workspace state, and project ordering.
  - Legacy compatibility keys: `electron-saved-workspace-roots` and `electron-workspace-root-labels`.
- Top-level `state_*.sqlite`: authoritative current thread metadata. Compare successful `_sqlx_migrations`, modification time, columns, and rollout coverage before selecting a DB. Older Windows rows may store `rollout_path` with a `\\?\` prefix that must be normalized for filesystem access.
- `sessions/**/rollout-*.jsonl` and `archived_sessions/rollout-*.jsonl`: persisted active and archived threads.
- `sqlite/codex-dev.db`: Desktop-derived catalog state such as `local_thread_catalog` and sync metadata. Treat it as a verification/reconciliation cache, not the primary deletion source.
- Legacy `sqlite/state_*.sqlite` and `sqlite/logs_*.sqlite`: inspect only for migration residue or a mobile-visible orphan absent from current state.
- `session_index.jsonl`: compatibility index. Never use it as the authoritative thread inventory.
- `logs_*.sqlite`: diagnostics. Exclude from visibility cleanup unless a target-specific residual is proven; include in storage cleanup only with user consent.
- `goals_*.sqlite` and `memories_*.sqlite`: separate thread-related state. Do not touch them unless rows are proven orphaned and the user requested complete residual cleanup.
- `sqlite/codex-dev.db` automation and inbox tables: preserve rows linked to `thread_source = automation` unless the automation itself is an explicit cleanup target.
- `config.toml`: trusted project roots.

## Classification

Build the active project set in this order:

1. Read `local-projects` and index entries by project ID.
2. Build visible project IDs from `project-order`, `pinned-project-ids`, and `selected-project`; preserve every matching `local-projects` entry.
3. Preserve `active-workspace-roots`, even during a partially completed project migration.
4. Build active roots from every `rootPaths` item of preserved projects. Support multi-folder projects.
5. Use `electron-saved-workspace-roots` only as a fallback when the current project keys are absent. Do not union stale legacy roots into an otherwise valid current project set.

Preserve by default:

- The current thread.
- Threads assigned by `thread-project-assignments` to a preserved project ID.
- Threads whose normalized `cwd` is equal to or below an active root when no reliable assignment exists.
- Projectless/general chats and their projectless output/hint records.
- Automation threads and runs, including archived runs, unless explicitly selected with their owning automation.
- Generated Codex workspaces and worktrees tied to a preserved project.
- Subagent threads unless their root parent is selected and the user accepts App Server descendant deletion.
- Archived threads belonging to preserved projects unless archive cleanup was requested.

Treat as candidates, not automatic deletions:

- A `thread-project-assignments` entry whose `projectId` is absent from `local-projects` and which is not projectless or current.
- A project entry absent from visible order/pinned/selected state after the Desktop **Remove** flow, when the user confirms it should no longer exist.
- A non-projectless thread assigned to a removed project.
- A non-projectless thread with no current assignment whose normalized `cwd` is outside all active roots.
- A thread whose `cwd` no longer exists, unless it belongs to a preserved project, remote project, worktree, or generated workspace.
- A legacy-state row or catalog entry only when the authoritative current thread list no longer contains it.
- A dead `config.toml` project trust block.

If a Desktop project name differs from a raw folder name on mobile, compare `local-projects.name` and legacy labels. Treat a valid project-ID/root match as a display-sync problem, not a deletion target.

For Windows paths, normalize `\\?\` prefixes, separators, trailing separators, and case. Compare `root == cwd` or `cwd.startswith(root + "\\")`; do not rely on mixed-form `commonpath` results.

## Failed Archive Repair

When the user supplies a thread ID that remains active after an archive request, read [references/archive-repair.md](references/archive-repair.md) and keep this path separate from cleanup or deletion.

1. Resolve the target and current thread IDs with the available app context.
2. Retry the supported archive operation and re-list active and archived threads.
3. If the supported operation fails and the target still has one verified active database row plus an existing rollout below `sessions`, run `scripts/repair_thread_archive.py` without `--apply`.
4. Review its selected database, source, destination, size, hash, and path-prefix decision.
5. Run the same command with `--apply` only for the confirmed target. The helper creates its own timestamped backup before changing state.
6. Verify the app lists and read recent archived turns. Do not report success from SQLite state alone.

Stop instead of improvising if the helper reports an ambiguous database, missing rollout, path escape, mismatched destination, current-thread target, or unsupported schema. The helper intentionally leaves global UI state, compatibility indexes, diagnostics, goals, memories, project assignments, and derived catalogs unchanged.

## Workflow

1. Record the installed Desktop and CLI versions and locate `CODEX_HOME`.
2. Try the supported UI path first: remove the stale project in Desktop, refresh or restart Desktop, and reconnect Remote/mobile when practical.
3. Read current global project state and the selected top-level state DB in read-only mode. Page through App Server `thread/list` when available, including active and archived threads.
4. Print a concise candidate report with project ID status, assignment status, cwd existence, archived state, descendant count, and preservation reason. Redact sensitive titles and paths.
5. Resolve the current thread ID and remove it from the candidate set. Stop if it cannot be resolved safely.
6. Confirm the requested cleanup mode and exact target set. A request for active-project cleanup does not authorize archive or storage cleanup.
7. Create a timestamped backup under the current workspace `work/` directory containing:
   - target and preservation manifests
   - consistent SQLite backups using `sqlite3.Connection.backup`
   - copies of global state, its `.bak`, `session_index.jsonl`, and `config.toml`
   - selected rollout files
   - pre-cleanup byte sizes
8. For selected persisted threads, prefer a callable Codex thread-delete tool. Otherwise use the official App Server JSON-RPC `thread/delete` method after the `initialize`/`initialized` handshake.
   - Delete only root target IDs because App Server also deletes spawned descendants.
   - Tell the user the descendant count before deletion.
   - Treat a missing rollout as already deleted only when the App Server reports success.
9. After successful thread deletion, update only stale Desktop project and assignment state tied to confirmed targets:
   - `local-projects`, `project-order`, `pinned-project-ids`, `selected-project`, `thread-project-assignments`, and `active-workspace-roots`
   - matching projectless/output/hint, queued-follow-up, permission, unread, client-ID, description, browser-tab, workspace-state, and project-order UI entries
   - legacy saved-root/label keys only when they refer to the same confirmed removed project
10. Do not remove `codex-writing-block-deleted-thread-v1:*` or other unknown tombstone-like keys without proving their semantics. Do not directly edit `local_thread_catalog` during the normal path; allow Desktop to reconcile it.
11. Remove dead `config.toml` trust blocks only when their normalized path is confirmed outside active projects and the requested scope includes trust cleanup.
12. Use direct repair only for residual targets that remain after the supported path:
   - inspect `sqlite_master` and foreign keys before choosing tables
   - remove rows only from tables that exist and reference the selected thread IDs
   - delete validated rollout files and compatibility-index entries
   - include legacy state only when it contains the proven residual
   - exclude logs, goals, memories, and the derived catalog unless separately justified by the requested mode
   - exclude automation and inbox tables unless a removed automation is an explicit target
13. Avoid checkpoint, `VACUUM`, or large log deletes while the DB is busy. Run compaction only for an explicit storage cleanup and report lock failures honestly.
14. Record post-cleanup sizes and verify before reporting success.

## Verification

- Run `PRAGMA integrity_check` for every modified SQLite DB.
- For archive repair, confirm the ID is absent from the active app list, present exactly once in the archived list, and readable with its conversation intact.
- For archive repair, confirm the active rollout is absent, the archived rollout exists with the verified hash, and the current state row has `archived = 1`, a non-null `archived_at`, and the archived path.
- Confirm removed IDs are absent from App Server `thread/list` and `thread/read`, including archived results.
- Confirm selected rollout files are absent and preserved rollout files still exist.
- Confirm removed IDs are absent from the current state DB and any included legacy DB.
- Confirm removed project IDs and assignments are absent from current global state while preserved project IDs, `rootPaths`, names, projectless records, and the current thread remain.
- Confirm automation threads, automation runs, and their owning automation definitions remain unchanged unless explicitly selected.
- Confirm `local_thread_catalog` reconciles without the removed IDs; report a catalog-only residual instead of editing it silently.
- Treat `session_index.jsonl` as a compatibility check only.
- Verify `config.toml` trust blocks only for the requested scope.
- When Remote/mobile is involved, ask the user to reconnect or refresh and distinguish local verification from device UI verification.

## Size Accounting

- Report directly reclaimed bytes from files that no longer exist.
- Report SQLite file-size deltas only when measured. If pages remain allocated, report deleted row counts instead of reclaimed bytes.
- Report backup size separately and calculate net disk change only when both sides are known.
- Explain that visibility cleanup may reclaim little space because logs and compaction are separate.

## Reporting

Report in Korean unless the user asks otherwise. Include the cleanup or repair mode, target and descendant counts, API versus fallback path, files/DBs touched, backup directory, size accounting, verification results, and known residuals. Archive repair normally reclaims no space because it moves the rollout while retaining a backup. Keep sensitive historical content redacted.
