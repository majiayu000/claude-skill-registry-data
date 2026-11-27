---
name: agnos-init
description: "AGNOS process initialisation skill. Adds AGNOS to a project by completing its CLAUDE.md and AGENTS.md with one delimited block and creating its agnos-process/ folders, without touching what the developer wrote. USE FOR: adding AGNOS to a new or existing repository, updating the block after AGNOS changes, or whenever agnos-index reports that agnos-process/ is missing."
argument-hint: "<project folder>"
---

<!-- RQ-INI-001 to RQ-INI-006, RQ-INI-009, RQ-PLG-004, RQ-PLG-018, RQ-PLG-020, RQ-PLG-021 / ADR-INI-001 (DEC-INI-001 to DEC-INI-003), ADR-PLG-001 (DEC-PLG-003), ADR-PLG-003 (DEC-PLG-013, DEC-PLG-015, DEC-PLG-016) -->
# AGNOS Init

A script does all the work, so that the same call always gives the same files: do not write or edit
the block yourself. `<skill-folder>` is the folder holding this file. <!-- RQ-PLG-005 -->

## Procedure

1. Take the project folder from the user, by default the current folder.
2. Run the script matching the platform:

   | Platform | Command |
   |---|---|
   | Windows | `powershell -NoProfile -File <skill-folder>/scripts/init.ps1 -Target <project>` |
   | Linux / macOS | `bash <skill-folder>/scripts/init.sh --target <project>` |

   Use `powershell` (Windows PowerShell 5.1), never `pwsh`: PowerShell 7 is not guaranteed to be installed.

3. Check the exit code:
   - `0`: done. Report each line to the user, then give them two separate steps: first, close this conversation and open a new conversation in the tool, so that it reads the block; then, in that new conversation, ask the agent to start an AGNOS session. Name `agnos-process/AGNOS-GETTING-STARTED.md` as the guide to read meanwhile. <!-- RQ-PLG-020, RQ-PLG-021, RQ-PLG-033 / DEC-PLG-015, DEC-PLG-016, DEC-PLG-026 -->
   - `1`: error, nothing written. Report the message. For a damaged block, the user repairs its lines: do not guess its limits.

## What it does

| State of `CLAUDE.md` or `AGENTS.md` | Action | Reported |
|---|---|---|
| Absent | Creates it with the block alone | `created` |
| Without a block | Adds the block at the end | `added` |
| With a block that differs | Replaces only the block | `updated` |
| With the same block | Writes nothing | `unchanged` |
| With a damaged block | Stops before any write, naming the file | Exit 1 |

Every byte outside the block is preserved, and the block takes the file's line ending. It also creates
each folder of `agnos-process/` that is absent, with a `readme.md` saying what it holds, and writes into `agnos-process/` the
user's guide `AGNOS-GETTING-STARTED.md` and `VERSION.txt`, the AGNOS version installed: both are AGNOS's, rewritten whole from their
templates and reported `created`, `updated` or `unchanged`. A root `AGNOS-GETTING-STARTED.md` whose first line is AGNOS's, written by
a former init, is removed and reported `moved`; any other root file of that name stays. <!-- RQ-PLG-021, RQ-PLG-033 / DEC-PLG-016, DEC-PLG-026 -->
It adds `agnos-process/_sessionstate/session.yaml` to the project's `.gitignore`, created if absent, only when git's rules do not
ignore it yet (outside a git repository, when no line of `.gitignore` is that path), reported `created`, `added` or `unchanged`. It
never untracks a file already committed. <!-- RQ-INI-016 / DEC-INI-012 -->
It changes nothing else in the project.

A project initialised before holds its artifacts in `process/`: when `process/INDEX.idx.md` exists and `agnos-process/` does not, the
script renames the folder to `agnos-process/` and its index to `process.idx.md`, with `git mv` when git tracks them so that their
history follows, and reports `moved`. A `process/` without that index is not AGNOS's and is left untouched. When both folders
exist, it stops before any write, exit 1, naming both: the user keeps one. <!-- RQ-PLG-038 / DEC-PLG-031 -->

To update a project after AGNOS changes, call it again.

## Layout

| Path | Role |
|---|---|
| `scripts/init.ps1`, `scripts/init.sh` | The two versions, giving the same bytes |
| `assets/templates/` | One block, `agnos.block.md`, written as it is into both entry-point files <!-- RQ-INI-019 -->, one `readme.md` per process folder, and the guide `AGNOS-GETTING-STARTED.md` |
