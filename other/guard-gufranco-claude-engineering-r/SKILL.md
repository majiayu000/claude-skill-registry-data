---
name: guard
description: Safety mode for risky operations that freezes edits to one directory, warns on destructive commands, and enforces scope.
disable-model-invocation: true
argument-hint: "/guard [directory] | /guard off | /guard status"
allowed-tools: "Bash, Read, Write, Glob, AskUserQuestion"
---

## Overview

Activates multiple safety protections at once to reduce the risk of accidental damage during sensitive operations.

## When to Use

Activate before a sensitive operation where an edit outside one directory or an unconfirmed destructive command would do damage, such as a migration, a production config change, or a bulk rename.

### Arguments

| Invocation | Action |
|-----------|--------|
| `/guard <directory>` | Activate guard mode, freeze edits to the specified directory |
| `/guard` | Activate guard mode for the current project root |
| `/guard off` | Deactivate guard mode, remove all restrictions |
| `/guard status` | Show current guard state |

## Protections

Guard mode enables three protections simultaneously:

| Protection | What it does |
|-----------|-------------|
| **Freeze** | Restricts file edits to the specified directory. Writes to `~/.claude/.freeze-scope` with the frozen path. Enforcement relies on the agent respecting the freeze file. |
| **Careful** | Warns before any destructive command: `rm`, `git reset`, `DROP`, `DELETE`, and patterns covered by the dangerous-command-blocker hook. |
| **Scope** | If a `plan.md` exists in the project's spec folder, compares every file edit against the planned file list. Warns when editing files not in the plan. |

## Process

### Activate

1. **Resolve the directory.** If a directory argument is given, resolve it to an absolute path. If no argument, use the project root from `git rev-parse --show-toplevel`.

2. **Verify the directory exists.** If it does not, abort with an error.

3. **Write the freeze scope.** Create `~/.claude/.freeze-scope` with the absolute path.

4. **Confirm activation.** State the frozen directory path and that edits outside it will be refused. No hook reads the freeze file, so the refusal comes from the agent checking it before every edit.

5. **Check for plan.md.** Search for a spec folder with a `plan.md`:
   - Check `<root>/plans/*/plan.md` in the project workspace, per [`rules/project-workspace.md`](../../rules/project-workspace.md), then the legacy `specs/*/plan.md` and `.claude/specs/*/plan.md`.
   - If found, read the planned file list for scope comparison.
   - If not found, skip scope protection and note it.

6. **Confirm activation.** State:
   - Frozen directory path.
   - Whether scope checking is active.
   - How to deactivate: `/guard off`.

### Deactivate

1. **Remove the freeze scope.** Delete `~/.claude/.freeze-scope` if it exists.

2. **Confirm deactivation.** State that all guard protections are removed.

### Status

1. **Check freeze scope.** Read `~/.claude/.freeze-scope` if it exists.
2. **Check for plan.md.** Search for an active plan.
3. **Report:**

   | Protection | Status |
   |-----------|--------|
   | Freeze | Active: `/path/to/directory` or Inactive |
   | Careful | Active: always on when guard is active |
   | Scope | Active: using `plan.md` at `<plan path>` or Inactive: no plan found |

## Behavior While Active

When guard mode is active, every file edit and destructive command follows these checks:

1. **Before editing a file:**
   - Verify the file path is inside the frozen directory. If not, refuse the edit and state why.
   - If scope checking is active, verify the file is listed in `plan.md`. If not, warn and ask for confirmation before proceeding.

2. **Before running a destructive command:**
   - State the command and its potential impact.
   - Ask for explicit confirmation before executing.
   - Never run destructive commands silently while guard is active.

## Rules

- All three protections are advisory. No hook in [`hooks/`](../../hooks) reads `.freeze-scope`, so freeze holds only because the agent reads the file before every edit and refuses one outside it.
- The `.freeze-scope` file contains exactly one line: the absolute directory path.
- Activating guard a second time with a different directory overwrites the previous freeze scope.
- The freeze file stays on disk across sessions, and a new session does not read it on its own. Run `/guard status` at the start of a session that should honor it.
- Never auto-deactivate guard mode. Only `/guard off` removes the freeze file.
- All paths must be absolute, never relative.

## Common Rationalizations

- "This file sits just outside the frozen directory, and the fix needs it": refuse the edit, state why, and let the user widen the scope with a new `/guard <directory>`.
- "`rm` on a build directory is harmless": guard mode confirms every destructive command. State the command and its impact, then ask.
- "The plan missed this file, but it obviously belongs": an unplanned file gets a warning and a confirmation.
- "Guard was on last session, so it still is": the file may remain, but nothing enforces it until this session reads it. Run `/guard status` first.
- "A relative path is fine here": the freeze file holds one absolute path. Resolve it before writing.

## Red Flags

- Stop and refuse when an edit target resolves outside the path in `~/.claude/.freeze-scope`.
- Stop and ask for confirmation when a command matches `rm`, `git reset`, `DROP`, `DELETE`, or a dangerous-command-blocker pattern.
- Stop and abort activation when the directory argument does not exist.
- Stop and warn when scope checking is active and the edit target is absent from `plan.md`.

## Verification

- After activation, `~/.claude/.freeze-scope` holds exactly one line, an absolute path that exists.
- The activation message names the frozen path, the scope checking state, and `/guard off`.
- `/guard status` prints the three-row protection table matching the freeze file and plan lookup.
- After `/guard off`, `~/.claude/.freeze-scope` is absent.

## Related Skills

- `/investigate --freeze` -- Debugging with freeze protection uses the same mechanism.
- `/plan` -- Creates the `plan.md` that scope checking uses.
- `/ship commit` -- Commit after completing guarded work.
