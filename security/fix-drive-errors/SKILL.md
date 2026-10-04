---
name: fix-drive-errors
description: Use when Google Drive reports sync errors, a symlink or generated directory exists under ~/My Drive, or a Google Docs pointer fails to upload from the synced personal-account root.
---

# Fix Google Drive sync errors

## Scope and evidence

An audit, inventory, or diagnosis request is read-only: inspecting the panel may
open/close its error window, but does not authorize file repairs or restarting
Drive. For a fix request, repair only evidenced causes within the requested
scope. Moving or trashing synced files can propagate to the cloud and other
devices; confirm that the exact action is authorized before doing it.

Treat the current, fully paginated panel as evidence of what Drive reports, not
proof of a file's identity or cause. Rows may survive after an offender disappears.
Establish the displayed Drive account and its configured sync root before
attributing rows or a clean panel to that root. The helper does not bind these
identities itself. Preserve duplicate rows and their order.

## Read and inventory

Start with the error panel and basename candidates:

    ~/My\ Drive/dotfiles/bin/drive-errors list

`list` opens the error summary's View button and reads every page. The currently
supported exact reason strings are `Can’t upload some Google files` and
`Can’t upload some files`. They are categories, not diagnoses: investigate
corrupt/unsupported Google-native pointers, account mismatches, symlinks, or
other causes using the actual evidence. A traversal failure, changed count,
unknown category, inaccessible panel, or unsupported UI is incomplete evidence,
never a clean result. Inspect the native panel directly if the reader refuses;
do not weaken its checks to obtain a zero count.

Check the helper environment. `DRIVE_ERRORS_PANEL_FIXTURE` selects simulated
input and cannot verify live Drive; use a live invocation without that override.
`DRIVE_ERRORS_DRIVE_ROOT` selects the candidate-search root only, not the UI
account. Record the root actually searched and any unreadable/unavailable
subtrees. The reader currently recognizes the English `Up to date` clean marker;
a different locale or layout needs direct inspection.

Use `drive-errors locate` when a broader filesystem inventory is in scope
(the default command runs both modes). It walks the selected root without
following directory symlinks. It lists symlinks and directories matching seven
generated-state names: `node_modules`, `__pycache__`, `.pytest_cache`, `.venv`,
`venv`, `.next`, and `.ruff_cache`. This is a heuristic, not exhaustive
generated-state detection or proof of disposability. Archive directories are
walked; archive-file contents are not inspected.

A basename match is only a candidate, not `LIVE`/`STALE` proof. Resolve its exact
path, file type, contents, account, and creation workflow before any mutation.
Zero matches means none were found in the traversed scope, not that the row is
stale. Active repositories belong under `~/repos`; dotfiles remains the sole
repository under Drive, which also contains notes, archives, and retained git
metadata. Do not treat the whole root as disposable development state.

## Repair the evidenced cause

Before each change, inspect the exact source and destination, preserve unrelated
or concurrent changes, and identify consumers. Keep enough recoverable evidence
outside Drive to restore the affected state. Do not copy secret-bearing or
private external content into a synced/public location while materializing a
link; follow the secrets context before handling credentials.

- For an offending symlink, inspect the link itself and its resolved target
  separately. Materialize only bounded, small, static data whose contents and
  destination are appropriate; do not recursively follow unknown links. Move
  required dependencies/build state outside Drive and update every affected
  consumer. Do not replace the link with another Drive-hosted symlink.
- For generated directories, verify what created them and whether they contain
  unique state. Keep dependencies, environments, caches, builds, and worktrees
  outside Drive. Preserve required contents and metadata during relocation,
  then run the actual consumer against its new location. Trash only an inspected
  exact target with deletion authority; trashing a symlink must not trash its
  target. A familiar basename alone never authorizes removal.
- For a rejected Google-native pointer, inspect its metadata without rewriting
  it. `doc_id` and `email` are clues, not proof of document type, ownership, or
  current account access. Use the mapped Google tools and explicit account from
  `claude/context/service-access.md` and `claude/context/google-services.md`
  to verify the original document and cause. Read the secrets context first if
  credential handling becomes necessary. Do not treat every Google-file error
  as an Epoch `.gdoc`.

### Epoch Google Docs pointer replacement

Use this route only for a verified Google Docs document intended to open in
Epoch and an authorized replacement of its rejected personal-root pointer.
It does not support Sheets, Slides, or another account.

1. Preserve the exact document ID and original pointer bytes/identity. Inspect
   the destination and existing trusted `epoch-doc:` handler/profile route;
   do not install/rebind handlers, alter Chrome aliases, change sharing, or
   duplicate the cloud document as an implicit repair.
2. Run `epoch-doc-link create DOC_ID PATH.url` with literal, quoted arguments.
   It creates a regular Internet Shortcut containing
   `epoch-doc:///document/DOC_ID`, not a plain HTTPS shortcut. An identical
   existing file is reusable; a conflicting destination must be preserved.
3. Verify the actual saved `.url` opening route through the OS handler into the
   configured Epoch Chrome profile, and observe the correct document and
   account. `epoch-doc-link open` takes the custom URI, not the file path;
   invoking it directly bypasses the file/handler route. A zero exit status,
   login page, or profile label alone does not prove successful document access.
   Use `end-to-end` for this live acceptance, within the authorized scope.
4. Only after that check, recheck that the original pointer is unchanged and
   trash it if deletion was authorized. Preserve it if verification is blocked
   or it changed. Verify the replacement syncs if cloud availability is part
   of the requirement; local creation alone does not establish that.

Google documents pointer corruption and unsupported desktop copying as other
possible causes; its generic recovery actions do not override this skill's
preservation and authorization limits. See
[Google's troubleshooting guide](https://support.google.com/drive/answer/2565956?co=GENIE.Platform%3DDesktop&hl=en).

## Clear and verify

After authorized repairs, allow a bounded settling period and inspect current
transfers and unsynced state. Do not wait indefinitely for `Sync completed` or
require an error-free state before refreshing stale errors. If a normal restart
is needed and within repair scope, first establish that interrupting transfers
is safe, then quit via Drive's menu and relaunch normally. Do not force-kill it.
If it cannot settle or quit safely, report that boundary without restart loops.

Rerun a live `drive-errors list`, re-establish the same account/root, and verify
the complete current panel plus the repaired consumer/document behavior.
A lower count, basename inventory, or fixture run is insufficient. Diagnose any
remaining exact rows; if there is no identified candidate, keep the name and
reason unresolved rather than mutating an unrelated file. Report only what was
observed, including any material live-verification gap.

## Hard limits

1. Never disconnect/reconnect the account or remove/re-add the sync root. A past
   reconnection re-uploaded thousands of files into the wrong cloud folder.
2. Never write, delete, or rename DriveFS internal databases under
   `~/Library/Application Support/Google/DriveFS`. Read-only diagnosis is fine.
3. Never create a symlink, dependency tree, cache, virtual environment, build
   output, or worktree under `~/My Drive`.
