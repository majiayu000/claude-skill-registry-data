---
name: move-session-log
description: Use when the user asks to relocate or import a session log into the current project, or to make session history and resume follow a renamed project directory in the current tool; not for merely opening or inspecting the current session log.
---

# Relocate Codex session metadata

Import one explicitly identified Codex session into a project, or relocate
metadata after a project-directory rename. Codex stores transcripts globally:
this changes metadata, not their physical project directory. It does not rename
the project, unarchive sessions, merge histories or operate on Claude stores.
Use `open-session-log` for simple inspection. Review, diagnosis and planning
requests remain read-only.

Use the bundled [adapter](scripts/move_session_log.py), its
[single-session importer](scripts/live_import.py), and
[offline safety helper](scripts/migration_safety.py). Do not invent an inline SQL or
transcript-rewrite fallback when the helpers or preflight fail.

## Establish identity and scope

- Resolve the actual active `CODEX_HOME`, defaulting to `~/.codex` only when
  unset. Inspect resolved store identities, not a guessed account or recent file.
  Import requires the exact UUID and one matching `session_meta.payload.id`;
  a filename substring is not identity evidence.
- Resolve the absolute target project; pass `--project` explicitly when it is
  not the shell directory. With no ID the adapter only lists candidates. Choose
  from reliable context or ask one identity question; do not select the newest.
- Rename takes absolute old and new paths, in that order. Mapping is exact, not
  prefix replacement. Report descendant contexts that also need relocation.
- Inventory active `sessions/`, associated `archived_sessions/`, and each
  discovered profile's history, session index and thread database. Discovery
  covers the active home and sibling `.codex*` homes sharing its resolved session
  store, not arbitrarily located profiles. Deduplicate resolved shared files.
  Report absent artifacts as unupdated; do not create a replacement index or
  claim complete coverage from this bounded discovery.

## Preview both modes

Use this skill's resolved directory for `SKILL_DIR`; pass literal quoted
arguments, not paths or IDs interpolated into SQL, Python or shell source.

```bash
python3 "$SKILL_DIR/scripts/move_session_log.py" --dry-run --project "$TARGET_PROJECT" "$SESSION_ID"
python3 "$SKILL_DIR/scripts/move_session_log.py" --dry-run --rename "$OLD_PROJECT" "$NEW_PROJECT"
python3 "$SKILL_DIR/scripts/move_session_log.py" --dry-run --rename-file "$MAPPING_FILE"
```

`--rename-file` renames several projects in one scan of the store. The file
holds one exact `OLD<TAB>NEW` mapping per line; blank lines and `#` comments
are skipped. Sources must be distinct, no path may be both a source and a
destination, and every destination must already exist as a directory. Several
sources may share one destination. Each rollout is read once and every
matching mapping is applied to it under the exact-match rule; history and
index files get one pass each, and each thread database one transaction for
all its rows. The preview and the recovery manifest report counts per mapping
as well as in total. Prefer it to repeated `--rename` runs over a large store.

Validate the selected inventory, JSONL identity and SQLite schemas before
any apply phase. Every mode inspects the thread database through read-only
transactions on the live file and backs it up through SQLite's online backup
API; live WAL and shared-memory bytes are never copied as static inputs. Refuse
malformed/truncated targeted files, identity conflicts, unsupported existing
schemas or unstable inputs. Resolve reversed paths or unexpected scope. Zero
matches do not prove the search was complete.

The database adapter supports the reviewed `state_5.sqlite` thread schema and
known triggers that do not fire on `cwd` updates. Unhandled generations or side effects
refuse before writes. Its database scope is thread `cwd`, not independent project
associations: observed `project_id`, project tables or project roots are reported
as unchanged. Do not claim those associations were migrated.

## Move one closed session while other sessions stay open

Single-session import uses the live-safe path by default. Establish that the
identified session is closed; a user report plus the helper's target-file
writer check supplies this boundary. When accessible, inspect the owning
app-server's `thread/loaded/list` too. Do not resume the target during migration.
The helper refuses the invoking session's ID and any open target-file writer.
An active session must not replace its own append-only transcript: its writer
could continue appending to an unlinked old file.

Unrelated Codex sessions and their database connections may remain open.
The importer uses SQLite transactions to lock and revalidate exact thread rows,
with consistent database backups and a recovery journal. It does not hash live
WAL or shared-memory files as if they were static transcripts. Shared history
and index files that need no change are not replaced or treated as offline
stores. If their selected metadata needs rewriting, their file writer guards
still apply; report the specific blocking file rather than demanding that all
Codex sessions stop.

Apply with a new absolute `--backup-dir` outside Google Drive:

```bash
python3 "$SKILL_DIR/scripts/move_session_log.py" --backup-dir "$NEW_PRIVATE_BACKUP" --project "$TARGET_PROJECT" "$SESSION_ID"
```

Do not kill unrelated sessions, close Emacs, restart Codex or switch accounts
to move a closed session. On a refusal, identify the actual target or input
that failed instead of inferring that the shared database must be closed.

## Bulk rename and explicitly offline import

Bulk `--rename` and `--offline` imports follow the same rule as the live
import: unrelated Codex sessions may stay open. No session may be running
inside a directory being moved, which for a rename means every session whose
rollout records the old project path as its `session_meta` or `turn_context`
`cwd`; those rollouts are rewritten and must have no open writer. The invoking
session must not be one of them. Sessions started elsewhere while the rename
runs are tolerated; one started in the old directory refuses the run. If the
affected sessions cannot be closed within the request, keep the preview and
report that boundary.

Shared `history.jsonl` and `session_index.jsonl` need no quiescence. Open
sessions keep appending to them, so the helper replaces each append-safely:
under an exclusive advisory lock (a zero-byte `.<name>.migration-lock` beside
the file, ordering only our own runs because Codex takes no locks) it re-reads
the file, requires the preflight bytes to still be a prefix, writes the
rewritten prefix followed verbatim by every byte appended since, renames it
into place, and carries over a line that lands in the rename window. A file
truncated or rewritten wholesale refuses with no write to it; the journal
records the re-appended tail. `state_5.sqlite` may stay open in other Codex
processes: the selected exact thread rows are re-checked before every
operation and updated inside `BEGIN IMMEDIATE`, after an online-backup snapshot.

Apply requires `--offline` and a new absolute `--backup-dir` outside Google Drive.
The flag asserts that the affected sessions are closed; it does not stop writers.
The helper revalidates inputs and inspects kernel device/inode records using the
supported Darwin/libproc `lsof` 4.91 format, refusing an open write handle on
any rollout or index it rewrites. Handles on other files, and other Codex or
Claude processes as such, are not refusals. Unrecognized formats or diagnostics
refuse the operation. This can miss processes the OS hides and cannot exclude
future writers; it does not independently establish quiescence.

```bash
python3 "$SKILL_DIR/scripts/move_session_log.py" --offline --backup-dir "$NEW_PRIVATE_BACKUP" --project "$TARGET_PROJECT" "$SESSION_ID"
python3 "$SKILL_DIR/scripts/move_session_log.py" --offline --backup-dir "$NEW_PRIVATE_BACKUP" --rename "$OLD_PROJECT" "$NEW_PROJECT"
python3 "$SKILL_DIR/scripts/move_session_log.py" --offline --backup-dir "$NEW_PRIVATE_BACKUP" --rename-file "$MAPPING_FILE"
```

Choose a durable uniquely named location under a private off-Drive state root.
Protected originals and the recovery journal contain private user history, not
scratch or public repository artifacts. Do not publish or delete them as cleanup.

In either mode, only consumer-relevant `session_meta`/`turn_context` payload `cwd` and supported
top-level history/index metadata are eligible. Import maps the identified
original project to the target, preserving different contexts. SQLite updates
match exact thread IDs, never `rollout_path LIKE` or a nested arbitrary `id`.
Historical tool arguments, results, prose and unrelated records stay unchanged.
Archives remain archived; shell snapshots are not moved.

A rollout may hold several `session_meta` records. Its identity is the first
record; forked and subagent threads copy their ancestors' records behind it,
and Codex 0.129–0.133 re-append the thread's own record with a changed
`memory_mode`. Every `session_meta` `cwd` that exactly equals the original
project is remapped, ancestor copies included; records sharing an `id` must
agree on `cwd`, and a `session_meta` without a canonical `id`, a conflicting
`cwd` for one `id`, or an owning record that is not first is refused.

## Verify the right result

For Agent Log, test `agent-log-resume-session` from the user's rendered log.
Agent Log has its own persistent `agent-log-thread-catalog.json` and rendered
index, separate from Codex's SQLite database and Emacs session buffers. A stale
catalog can send resume back to the original project. Ensure resume resolves
the current project from the exact canonical transcript, refresh Agent Log's
catalog through its own refresh mechanism, and use its rendered-file maintenance
to relocate the indexed Markdown file and any visiting buffer. Keep the
original rendered path available until its resume command has been exercised.
Verify the newly resumed session's ID, restored history and actual directory;
renaming a previously running Codex buffer does not test this entry point.

When the user works in Emacs, relocation includes the buffer associated with
the exact session ID, not just disk metadata or the history picker. Inspect all
Codex buffers, including buffers whose processes have exited, before and after
the operation. Match `codex--app-server-thread-id` or `codex--session-id`; do not
infer identity from the buffer name. A buffer reopened during the operation can
retain the old directory even after the disk migration succeeds.

For an idle live app-server buffer whose persistent metadata is already moved,
send `thread/settings/update` with the exact `threadId` and target `cwd` through
that buffer's existing connection. Check the installed experimental schema and
the response before updating buffer state. Set `default-directory` and
`codex--buffer-directory` to the target, preserve the session ID, and update
`codex--buffer-instance-name` and the buffer name together. If the target's
instance name is occupied, choose a distinct instance such as `moved`; never
replace the other buffer. Do not interrupt an active turn or pretend changing
only the displayed name relocates the running session. Exited matching buffers
still need their directory and name synchronized.

Verify the resulting buffer name, directory, exact session ID and live server
`thread/read` cwd. Verify persistent metadata separately. A passing history
listing alone does not establish that an existing buffer moved.

Inspect exit status and journal; independently read back selected metadata,
exact thread rows and unchanged unrelated records. Compare the actual result
with the preview and explain changed inputs or coverage limits. Repeat a preview
for remaining intended changes: matching counts alone are not proof.

Files and profile-local SQLite transactions are not one atomic transaction. On
failure, stop and inspect completed operations and retained originals. Report
partial application and its recovery path. Do not blindly retry or roll back
over newer state.

The installed app-server interface accepts a `cwd` override for `thread/resume`,
and the Emacs client sends it. That alone does not establish durable relocation
of the original rollout header. Project-filtered listing also uses stored
metadata and can repair it from JSONL; changing only a database row is insufficient
consistency evidence.

Use `end-to-end` when claiming that the actual history/resume consumer now works.
Do not start a live session as part of a dry run or an audit of this skill.
Report the session/project, material outcome and any partial-state, coverage or
live-verification gap briefly.
