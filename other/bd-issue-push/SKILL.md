---
name: "bd-issue-push"
description: "Create a bead (task) in the current repository using beads (`bd`). Beads keeps its database in the main repo checkout and its tracked `issues.jsonl` o"
---

# bd-issue-push command

Apply this command workflow. Treat any text after its invocation as the command input.

Create a bead (task) in the current repository using beads (`bd`). Beads keeps its database in the main repo checkout and its tracked `issues.jsonl` on `main`; `bd sync` persists new beads to git so they are visible on all machines. Run this from the main checkout on `main` (not inside a worktree).

## Input

$ARGUMENTS

## Steps

1. Verify that `.beads/` exists in the repository root. If not, initialize beads and persist it:
   ```bash
   bd init
   bd sync   # commits and pushes the tracked .beads/ files
   ```

2. **Search for ripple effects.** Before drafting the bead, identify every file and field that the change touches — not just the primary target. The executor will do exactly what the bead says and nothing else, so anything omitted will be missed.
   - Read the files involved to understand their structure.
   - `grep` for identifiers, names, or values being added, changed, renamed, or deleted. Search the full project, not just the obvious files.
   - For each hit, note the file path, the field or line, and what needs to change.
   - Check for status fields, summary fields, titles, index entries, cross-reference IDs, and out_of_scope references — these are the most commonly missed.

3. Draft a concise title and well-structured description.
   - Include a "Files to Create/Modify" section listing every file. Under each file, list the specific fields or lines to change.
   - Include an `Estimated LOC:` line for code tasks.

4. Create the bead:
   ```bash
   bd create "<title>"
   ```
   Capture the bead ID from the output.

5. Persist the new bead so it is visible on all machines:
   ```bash
   bd sync   # flushes the database to issues.jsonl and commits/pushes it
   ```
   (`bd sync` is the beads-native way to persist the tracker; do not hand-commit
   `.beads/` — confirm the subcommand with `bd sync --help`.)

6. Report the bead ID and title.
