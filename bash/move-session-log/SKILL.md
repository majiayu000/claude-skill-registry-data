---
name: move-session-log
description: Use when the user asks to relocate or import a session log into the current project, or to make session history and resume follow a renamed project directory in the current tool; not for merely opening or inspecting the current session log.
argument-hint: "<session-id> | --rename <old-project-path> <new-project-path>"
---

# Move Claude session history

Relocate one explicitly identified Claude Code session, or its history after a
project-directory rename. This does not rename the project itself, merge stores,
or authorize changes to Codex sessions. Simple inspection belongs to
`open-session-log`. A review, diagnosis or planning request remains read-only.

Use the bundled [adapter](scripts/move_session_log.py) and its
[safety helper](scripts/migration_safety.py). Do not substitute inline `mv`,
truncating JSON rewrites, or another account's store if the helpers fail.

## Establish identity and scope

- Identify the actual account/configuration directory and target project from
  reliable context. The adapter honors `CLAUDE_CONFIG_DIR`; otherwise it uses
  `~/.claude`. Inspect resolved symlink destinations, not a guessed profile.
  Discovery is limited to that configuration root. Sibling/custom profiles'
  separate histories are not inventoried, even when their projects store is
  shared. Report this boundary and absent history stores as unupdated.
- Import requires the exact UUID and matching transcript metadata. Pass an
  explicit absolute `--project` when the shell directory is not the target.
  With no ID the adapter only lists candidates; select from established context
  or ask one concise question. Do not import the newest candidate automatically.
- Rename takes absolute old and new paths, in that order. It relocates history,
  not the filesystem project. Claude's encoded paths are lossy: different
  projects can share a bucket. Refuse ambiguous/mixed origins, unknown root
  artifacts or destination collisions instead of merging or overwriting.
- Inventory the exact transcript, recursively nested sidecars, selected history
  records and resolved shared files. Only supported `subagents/agent-*.jsonl`
  sidecars contain routing metadata; tool results and `agent-*.meta.json`
  remain opaque regardless of extension. Verify existing destination ownership
  before importing. A later different `cwd` does not by itself establish
  another originating project.
- Rename also accepts the legacy flat layout, `<bucket>/subagents/agent-*.jsonl`
  (with `.meta.json` beside it) and `<bucket>/tool-results/*`, written by
  Claude Code up to about 2.1.8x. Such root sidecars belong to the bucket they
  sit in and name their session themselves; the live binary routes them by
  bucket and `sessionId`, never by `cwd`, and in real buckets their `cwd`
  records a resolved or since-renamed directory. They move with the bucket
  with only exact-match `cwd` fields rewritten, including when their owning
  transcript has been cleaned up (a sidecar-only bucket). Orphans add no
  history rewrites. The preview reports their count and how many lack a
  transcript; a bucket holding only `tool-results/` is refused for lack of any
  session identity. Single-session import does not move root sidecars.

- `--rename-history OLD NEW` rewrites prompt-history entries whose project is
  exactly OLD, with or without a `sessionId`, once no OLD bucket remains.
  It covers history left behind by transcripts that no longer exist.

## Preview both modes

Use this skill's resolved directory for `SKILL_DIR`. Pass literal quoted
arguments, never paths interpolated into Python or shell source.

```bash
python3 "$SKILL_DIR/scripts/move_session_log.py" --dry-run --project "$TARGET_PROJECT" "$SESSION_ID"
python3 "$SKILL_DIR/scripts/move_session_log.py" --dry-run --rename "$OLD_PROJECT" "$NEW_PROJECT"
```

Review every selected identity, store, destination and proposed count. Resolve
unknown ownership, malformed inputs, unexpected symlinks, conflicting metadata,
reversed paths or unexpectedly broad scope before writing. Dry-run is a preview
of observed inputs, not a reservation or proof that a later plan is identical.

## Apply with the affected sessions closed

Unrelated Claude sessions may stay open, in any directory and any profile,
throughout preview and apply. The quiescence rule is narrower: no session may
be running inside a directory whose bucket this operation moves or rewrites.
For a rename that is every session of the old project (and, when the bucket
already sits at the new encoded name, every session of the new project); for
an import it is the identified session only. Their transcripts and sidecars
must have no open writer. The invoking session must not be one of them: an
active session cannot safely replace or relocate its own append-only
transcript. Do not kill sessions, close Emacs, restart applications or switch
accounts to satisfy this; if the affected sessions cannot be closed within the
request, preserve the preview and report that boundary.

Shared `history.jsonl` needs no quiescence. Every open session appends to it,
so the helper replaces it append-safely: under an exclusive advisory lock (a
zero-byte `.history.jsonl.migration-lock` beside it, which orders only our own
runs because Claude Code takes no locks) it re-reads the file, requires the
bytes captured at preflight to still be a prefix, writes the rewritten prefix
followed verbatim by every byte appended since, renames the result into place,
and carries over a line that lands in the rename window. A history that was
truncated or rewritten wholesale refuses with no write to it. The journal
records the re-appended tail length and keeps the tail bytes beside the
originals. Transcripts already owned by a session in the destination project
are read the same way: their appends are tolerated, their rewrite is refused.

Apply requires `--offline` and an explicit, new absolute `--backup-dir` outside
Google Drive. The flag asserts that the affected sessions are closed; it does
not stop writers. The helper revalidates captured inputs and inspects kernel
device/inode records using the supported Darwin/libproc `lsof` 4.91 format,
refusing an open write handle on any file it moves or rewrites, including the
history file at the moment of its replacement. Handles on other files, and
other Claude or Codex processes as such, are not refusals. Unrecognized formats
or diagnostics refuse the operation. This inspection can miss processes the OS
hides and cannot exclude future writers; it does not establish quiescence.

The paired Codex skill applies the same rule to rollouts, its shared JSONL
indexes and its SQLite thread database, with runtime-specific mechanisms. The
Codex workflow also verifies the exact session's Emacs buffer and live working
directory; a migrated history index does not rename an existing buffer. Agent
Log keeps a separate catalog and rendered index. When it is the resume entry
point, verify its actual `agent-log-resume-session` command from the user's
rendered log and reconcile the rendered artifact through Agent Log itself.

```bash
python3 "$SKILL_DIR/scripts/move_session_log.py" --offline --backup-dir "$NEW_PRIVATE_BACKUP" --project "$TARGET_PROJECT" "$SESSION_ID"
python3 "$SKILL_DIR/scripts/move_session_log.py" --offline --backup-dir "$NEW_PRIVATE_BACKUP" --rename "$OLD_PROJECT" "$NEW_PROJECT"
```

Choose a durable uniquely named location under a private off-Drive state root.
Protected originals and a recovery journal are created before writes. They
contain private history, not disposable scratch: do not publish, commit or
delete them as cleanup. Follow secret-handling rules when settings are in scope.

Only known top-level runtime path metadata and selected history ownership fields
change. Mapping is exact origin-to-target: unrelated and descendant directories
are preserved, not flattened or prefix-replaced. Report remaining descendant
contexts when relevant. Historical tool arguments, results, prose and untouched
JSONL records remain unchanged.

Project settings in `.claude.json` remain untouched by default: they can contain
trust, tool permissions and MCP approvals. Only a separately explicit request
to carry settings to the same verified renamed project permits
`--migrate-project-settings` on both preview and apply. Relocating history alone
does not grant that authority. Existing destination settings are not merged.
Claude Code rewrites this file wholesale, so it is not append-safe: it stays
byte-pinned, its rewrite is applied before any transcript or history change,
and a concurrent settings write by any open session refuses the whole run
before those changes. Retry, or close the sessions, only for this option.

## Verify and recover honestly

Check exit status and journal, then independently inspect exact destination
layout, source disposition, metadata and preservation of unrelated records and
symlink identities. A repeated preview should show no remaining intended
metadata changes; explain unsupported contexts or missing stores instead of
calling counts complete coverage.

Per-file replacement is not one transaction across every transcript, move and
history file. On failure, stop and inspect completed operations and retained
originals. Do not blindly retry, roll back over newer state or claim that failure
changed nothing.

Use `end-to-end` for a claim that actual project-filtered history/resume now works.
Offline fixtures or metadata counts do not establish live resume behavior. Report
the relocated identity, meaningful result and material recovery/verification gaps.
