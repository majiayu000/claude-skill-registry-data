---
name: codex-project-transfer
description: Check and save a project's native Codex chats locally, or upload, download, and synchronize them, only when the user explicitly asks; diagnose session-transfer problems. Use for project-scoped Codex session transfer and sync, not ordinary code commits or ChatGPT web history.
---

# Codex Project Transfer

Operate the bundled tool for the user. Run commands yourself and report the result; do not turn routine setup or diagnosis into a CLI tutorial.

## Runtime and installation

All installed files must live inside the skill's own directory: `SKILL.md`, UI metadata, launcher and installer scripts, Python source, supporting docs, license, and `.venv`. Do not install a thin wrapper pointing to an external clone, use an external runtime directory, or create symlinks to the source repository.

For a source checkout or native plugin bundle, if this skill directory does not yet contain `src/codex_project_transfer`, locate the repository two directories above it and run that repository's `scripts/install.py` with an available Python 3.10+ (`python3` on macOS/Linux, `py -3` on Windows). The installer copies the complete bundle into the selected `CODEX_HOME/skills/codex-project-transfer`, creates `.venv` there, and returns the installed skill path. Use that returned directory for every subsequent command. `--skills-dir` supports an explicitly chosen destination. Existing unrelated skills are preserved.

The installer also creates `bin/cpt` (POSIX) or `bin/cpt.cmd` (Windows) inside the skill, bound to its local venv. When the user wants a bare terminal command on POSIX, pass `--link-dir` with their user PATH directory (commonly `~/.local/bin`); only a symlink lives outside the skill. On Windows, add the returned `command_directory` to PATH. Inspect `command_on_path` before saying the bare command is available. Preserve unrelated existing commands.

The installation is independent of the download/clone directory, which can be removed afterward. Do not copy the source `.venv`; create a fresh one on the receiving device. Tell the user to open a new chat for discovery. Installing this skill does not install a marketplace or transfer project sessions.

For an installed skill, the stable entry point is its own `scripts/cpt.py`. It uses `.venv` and source within that same skill directory, without global pip installation, pipx, environment activation, or PATH changes. Its bundled `scripts/install.py` can install another complete copy if explicitly requested.

In the commands below, `RUN` means the available Python plus the absolute path to this skill's `scripts/cpt.py`, passed as separate, correctly quoted arguments. Never invoke an arbitrary `cpt` from PATH. The optional project path follows the command and defaults to the current directory:

```text
RUN COMMAND [PROJECT] [--home CODEX_HOME] [--provider PROVIDER_ID] ...
```

## Set up a project

1. Resolve the project with `git rev-parse --show-toplevel`; inspect local CPT settings and remotes without contacting the network. Run `RUN --version` to check the local runtime.
2. Run `RUN init PROJECT` to prepare the local store without saving sessions. Add `--remote REMOTE` only when the user has selected an upload/download destination. This remembers the destination, but does not fetch or upload. If none is selected, finish local setup and ask for a destination only when a transfer is requested.
3. Run `status` and report setup status. Do not run `sync`, `upload`, `download`, native reconciliation, or a full export merely to finish installation.
4. No hooks or trust review are needed. Report setup completion and wait for a user-requested check, save, or transfer.

There are no hooks or automatic saves. Codex retains its own normal history; this plugin snapshots it into the project only on an explicit check/save/upload/sync request. No startup or shutdown export, Git-event import, background polling, or automatic retry is installed. A configured remote is a destination, not authorization to initiate transfers on later turns. Do not schedule or launch a watcher.

## User-requested operations

| User intent | Action |
|---|---|
| Check and save project sessions | `check` (export plus local status; no network/import) |
| Save this project's chats locally | `export` |
| Upload this project's chats | `upload`, then inspect the returned JSON |
| Download / restore from the other device | `download`, then inspect the returned JSON |
| Synchronize both directions now | `sync`, then inspect the returned JSON |
| Import files already in this repository | `import` (local only) |
| Preview a local import | `import --dry-run` |
| Check transfer health | `status` only; do not contact the remote |
| Imported files are not visible | `reconcile`, inspect `verified` and warnings |

Perform remote operations only in response to the user's upload, download, or sync request. Reuse an already authorized destination; if missing, ask before transferring. Keep the directions distinct: `download` never uploads or exports local sessions. `upload` reads and merges the remote first to avoid overwriting other devices' histories, but does not import anything into the local Codex home. `sync` is one explicit round trip, not an ongoing service.

On failure, preserve snapshots, report the error, and stop. Do not silently start polling or schedule future retries. A successful exit code alone is not proof of complete transfer: inspect errors, warnings, pending updates, conflicts, and native verification in the JSON result.

## History completeness

Export includes the storage ancestors required by paginated forks, including needed prefixes from outside the project. Native logical session IDs and physical history version IDs are distinct; the tool resolves original/version files and saves stable independent ancestry snapshots. Inspect `dependencies` in the export result.

Missing/cyclic/truncated ancestry stops export before new snapshots are written. An export-stage missing source requires the named native file from the correct Codex home, original device, or backup; repeating export cannot recreate it. If the user accepts a partial save, use `--skip-incomplete` on `export`, `check`, `upload`, or `sync`. Report every `skipped` ID and reason, warnings, and exit code 2 as partial completion. Do not silently enable this option or delete existing archive entries; it does not repair an already incomplete archive. Import-stage missing ancestry requires a complete archive from the source. Never remove `history_base`, fabricate missing turns, or report metadata/list visibility alone as successful restoration.

Import validates the entire archive before writing sessions and recalculates history byte bounds after path/provider adaptation. Reconciliation prepares required ancestor projections with a short-lived native process, with hooks disabled and no model turn. Inspect `prepared_dependencies`, `verified`, and warnings. A nonzero exit can mean files were preserved but verification or an update is incomplete.

## Titles and desktop visibility

Export saves UI names and updates later generated or renamed titles; inspect `titles_updated`. Import/reconcile applies and verifies titles for new and unchanged chats; inspect `native.titles_restored`. `--no-reconcile` defers title restoration too. To repair a title missing from an earlier snapshot, export again on the source and import the updated archive; restarting alone cannot recover a name absent from the archive.

An already-open desktop client may retain its chat-list cache after native discovery. Report `native.ui_refresh` and tell the user to refresh the list or restart the client manually if chats or titles remain absent. Never claim `native.verified` proves that the current GUI refreshed. Do not automatically quit/restart the app, control its UI, or create refresh hooks/background jobs. The refresh hint alone is informational, not an import failure.

## Destination provider

New native sessions are bound to the receiving project's effective `model_provider`, resolved through Codex `config/read`. Both the header and replayed thread settings bind to the destination provider and project paths. The archive keeps its provider provenance and historical message text. Do not copy credentials or provider endpoints from the sending machine.

If the user runs a profile or override that differs from the configuration visible to the tool, use `--provider PROVIDER_ID` with the subcommand, with the provider ID they selected. The ID is a provider configuration key, not a model name. If automatic resolution fails, report the error and obtain an explicit choice; do not silently fall back to the sender's provider. `--no-reconcile` skips discovery only; configuration resolution still occurs unless `--provider` is supplied.

Inspect `provider`, `provider_adapted`, and native `verified`/warnings in the result. Verification uses the destination-provider list and the actual thread metadata. This applies to newly imported sessions; existing native session prefixes retain their routing. Unchanged IDs are also verified; copying files or matching IDs is not enough to prove readability. Do not add database patches or migration procedures for previously registered sessions.

## Existing sessions and conflicts

Multiple native files with one session ID are not automatically separate conversations. CPT uses Codex's matching registered `rollout_path` when available and reports it in `selected_rollouts`; inactive files are preserved. If no matching registry entry exists and the files diverge, stop and inspect the reported candidate paths. Do not choose by size/mtime or delete duplicate files to suppress the error.

Imports do not overwrite already-open chats. `pending` means newer history is saved but not applied. Tell the user to close Codex/ChatGPT/VS Code first; after that, `import --update-existing` can apply the already-downloaded fast-forwards locally. An agent inside the active client cannot truthfully promise to close itself and finish the operation. If a user needs to finish outside the client, provide the exact local-venv command for `run PROJECT -- resume --all`, with real paths, as the necessary handoff. This command only imports already-saved local history and launches Codex. It does not save on startup/exit or fetch/upload.

For a divergent continuation, inspect `status` and preserve both histories. Use `fork PROJECT SESSION_ID CONFLICT_SHA256` followed by `import` when the user wants both branches available independently. Never splice JSONL records, force-push the session branch, overwrite SQLite, or use a code reset to fix chat sync.

## Evidence boundaries

Native CLI/app-server legacy and paginated restoration have been tested on macOS with Codex 0.155.1. Desktop/VS Code GUI continuation and Windows/Linux runtime validation remain separate checks. `reconcile` verifies discovery, not a new model answer. Paginated item projection may populate only after native resume. Code, external attachments, credentials, and running processes are not transferred.

Read `docs/design.md` inside the installed skill directory only when debugging storage, transport, or compatibility. Keep technical implementation details out of routine user instructions.
