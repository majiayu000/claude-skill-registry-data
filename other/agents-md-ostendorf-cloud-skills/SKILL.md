---
name: agents-md
description: "What a root AGENTS.md holds, where the rest of a repository's agent knowledge goes, and the line limits a check enforces. Use when writing, trimming or reviewing an AGENTS.md or a CLAUDE.md."
---

# AGENTS.md

A root `AGENTS.md` holds only what almost every task in the repository needs.

## When to use

- Creating an `AGENTS.md` for a repository.
- Adding a rule, a command or a note to an existing one.
- The file grew, or the size check warns.

## Rules

### Why it stays short

- The root file loads in full into every session and every subagent in the repository.
- Every line is paid for in every request. A line only one directory needs does not belong there.
- The baseline already applies. The file never repeats it.

### What belongs in the root file

- Purpose: what the repository is, in a few lines.
- Layout: the main directories, one line each.
- Commands: the ones that verify a change and start the work, such as `task setup` and
  `task check`.
- Hard constraints: what breaks if ignored, specific to this repository.
- `## Deviations` from the baseline, one line each with the reason. See `repo-conventions`.

### Where the rest goes

- Knowledge tied to one directory: a nested `AGENTS.md` in that directory.
- A `CLAUDE.md` next to each nested `AGENTS.md`, holding only `@AGENTS.md`.
- A nested file loads on demand, once a file below its directory is read. Verified in one run,
  see ADR 0009.
- Background, history and reasons: a file under `docs/`, with a one line pointer in `AGENTS.md`.
- A decision worth keeping: an ADR. See `adr`.
- What the code, the config or `task --list` already shows: nowhere.

### Limits

- Root `AGENTS.md`: 150 lines at most.
- Nested `AGENTS.md`: 100 lines at most.
- Over the limit means move content out, not squeeze lines together.
- Move in this order: a nested file, then `docs/`, then delete.

### The check

- The check is the task `lint:agents-md`, defined once in the shared workflows repository.
- A repository includes that shared task and runs it locally and in CI.
- It has two modes: `warn` prints the files over the limit, `fail` also exits non zero.
- The limits are inputs of the check, defaulting to 150 and 100.
- CI runs the included task with `--yes` or `--trusted-hosts`, because a remote include needs
  trust. Task loads the include on every call, so every `task` call in CI passes the flag.
- Pin the include by tag and checksum. The tag and the checksum move by hand together.
- Set the mode once as a root `vars` entry in `Taskfile.yaml`, so a local run and CI agree.

### Rollout

- A repository above the limit starts in `warn` mode.
- Its own issue shrinks the file, then the mode turns to `fail`.
- A repository within the limits starts in `fail` mode.

## Guardrails

- Root file at most 150 lines, nested files at most 100.
- No content the baseline already states.
- No content the code or `task --list` shows.
- Every nested `AGENTS.md` has a `CLAUDE.md` holding `@AGENTS.md` next to it.
- Every `docs/` page the file relies on has a one line pointer.
- Never turn the check off to pass. Move the content.

## References

- `repo-conventions` for the required files and `## Deviations`.
- `adr` for recording a decision.
- `docs/adr/0009-agents-md-stays-short.md` in the skills repository for the limits and the
  probe results.
