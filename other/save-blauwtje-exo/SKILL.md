---
name: save
description: "Writes a handoff file for unfinished work and reads it back in a fresh session. Use when the user asks to save, pause or hand off this session, or to continue from a saved handoff ('continue where I left off'). Not for finished work."
argument-hint: "[what the next session must not lose]"
metadata:
  author: exo
  tags: [handoff, session, resume]
---

# Save

## Purpose

Freeze what this session knows and the next one cannot rebuild. Point to files and commands, never paste the transcript, a diff or a log, because the fresh session would pay again for that context.

## Prerequisites

`node` and `git`.

## Instructions

### Before writing

- Finish or undo the step in progress and start no new work.
- On a plan's run branch, commit nothing: run `node "${CLAUDE_SKILL_DIR}/scripts/handoff.mjs" path` first, create its parent folder, save the partial work of the task in progress with `git diff > <handoff path with .md replaced by -task<n>.patch>` and list the patch under Progress.
- On any other non-default branch, commit every uncommitted edit as one `chore: wip <topic>` commit, and say in its body if the tree is broken.
- On the default branch, leave edits uncommitted and list them under Progress.

### Write the file

1. Run `node "${CLAUDE_SKILL_DIR}/scripts/handoff.mjs" path` for the location, create its parent directories, and write the file whole, replacing an older handoff.
2. Run `node "${CLAUDE_SKILL_DIR}/scripts/handoff.mjs" facts` and copy its `Written:` line and its path lists into the file. Write plain words in the user's language, with these sections in order:
   - One line on where the work stands and the first thing to do next, then the `Written:` line.
   - `## Goal`: what the work is for, and what it will not do.
   - `## Progress`: from `git status --short`, not memory. Open with the plan path and task number when a plan runs. List what is committed, then every uncommitted path in full, because a next session that cannot tell them apart discards working-tree edits. Add each decision as "<decision>, decided by <the user or this session>".
   - `## Evidence`: what is proven, as claim, command and result, and what is unproven, with what is open and who can answer.
   - `## Ruled out`: each approach already tried and dropped, one line each with why it failed.
   - `## Next step`: the first action, then each later step with its full command. For a run, say how to wait, what to do on failure and where to stop.
3. End the turn by naming the written path and telling the user to run `/clear`, then say "continue from the handoff". Continue no work.

### Continue from a handoff

When the user asks to continue saved work, run `node "${CLAUDE_SKILL_DIR}/scripts/handoff.mjs" path`, read the file it prints, run `node "${CLAUDE_SKILL_DIR}/scripts/handoff.mjs" stale`, then this text once: "Diff the work this handoff records as done against the work it still lists as next or open, name the resume point, and repeat no step it records as proven. Verify an inherited claim against the real artifact before building on it: a prior session's report is not the proof. Name what handoff.mjs stale lists as changed since, before relying on a claim." With no file there, say which branch has none and write nothing.

## Examples

The user says "save this, I continue tomorrow" on branch `feature-x`. The skill commits the edits as `chore: wip <topic>`, writes the handoff and ends with:

```
Saved to <handoff path>. Run /clear, then say "continue from the handoff".
```

## Limitations

- Push nothing and open no pull request.

## Troubleshooting

| Error | Cause | Solution |
| --- | --- | --- |
| No file at the printed handoff path | Nothing was saved on this branch | Say which branch has none and write nothing. |
| `git diff > <patch>` fails | The parent folder of the handoff path does not exist | Create the parent folder, then rerun the command. |
| The handoff names a commit that is not `git log -1` | Work continued after the `Written` date | Name what changed since before relying on a claim. |

## Available Scripts

| Script | Purpose | Arguments |
| --- | --- | --- |
| `handoff.mjs` | Prints where the handoff of the current branch sits | `path, facts or stale, each with [--cwd <dir>]` |
