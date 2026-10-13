---
name: db
description: "Resolve and load any file or directory the user shares through Dropbox, from the Dropbox root. Use whenever the user invokes /db, including inline forms like '/db foobar/ check its docs' — '/db <path>' always means the Dropbox path <path>. Handles Dropbox sync delay, online-only placeholders, directory settling, and recursive search that a plain ls/Read misses. Covers /db (root listing), /db dirname/, /db path/to/file.png, /db env/ (shared dev credentials), and multiple files at once. /ss is the shorthand for /db screenshots/."
disable-model-invocation: false
argument-hint: "[path/ | path/to/file | file1 file2 | (empty = root listing)]"
allowed-tools: Read, Bash(ls *), Bash(find *), Bash(stat *), Bash(for *), Bash(while *), Bash(head *), Bash(seq *), Bash(sleep *), Bash(printf *), Bash(sort *), Bash(cut *), Bash(cp *), Bash(grep *)
---

# Dropbox path resolver

The user keeps working material in Dropbox and refers to it by path relative to the Dropbox root. `/db foobar/` means "the Dropbox `foobar/` directory".

**Invocation epoch:** !`date +%s`

Keep this as `CUTOFF` — it is the moment the user invoked `/db`, used to reject files that appear afterwards.

## Base directory

`$DROPBOX_ROOT` (set in `.zshrc` for macOS and WSL2; all other `DROPBOX_*` vars derive from it).

If it is unset or missing, stop and say so — do not guess the path. This is the expected state on Claude Code web, where Dropbox is unreachable; report that the file cannot be loaded there rather than substituting something else.

## Resolve the argument

Read [references/resolve.md](references/resolve.md) and apply it with **BASE = `$DROPBOX_ROOT`**. It covers mode resolution order, directory settling, sync-delay retries, placeholder materialization, and type routing — all of which a direct `ls`/`Read` gets wrong on a syncing filesystem.

Two behaviours specific to `/db`:

- **Empty argument** → list the top level of `$DROPBOX_ROOT` (directories only, one level) and ask which one they mean. Do not load anything.
- **Argument under `env/`** → read [references/env-secrets.md](references/env-secrets.md) **before** opening anything. Those files hold dev credentials, and the handling rule there — resolve values inside a single shell command instead of printing them — exists because printing copies them into the transcript and the synced logs.

## Well-known subdirectories

| Path | Contents | Note |
| --- | --- | --- |
| `screenshots/` | Screenshots and ad-hoc shared files | Also reachable as `/ss`, which adds latest-N selection |
| `cclogs/` | Per-repo agent logs, prototypes, artifacts | Also `$DROPBOX_CCLOGS_DIR`, symlinked at `$HOME/cclogs` |
| `env/` | Per-project dev credentials | See [references/env-secrets.md](references/env-secrets.md) |

For `cclogs/`, prefer `$DROPBOX_CCLOGS_DIR` in anything written down — it is the documented handle, and repo-scoped paths under it fold worktrees and numbered sibling clones onto the base repo name.

## Related skills

- `/ss` — same engine, based at `$DROPBOX_SCREENSHOTS_DIR`, plus latest-N screenshot selection
