---
name: hand-off-session
description: >-
  Load this skill when a session's working state must survive into a later one: save writes a
  handoff file, load reads one back and resumes. Trigger on "save where we are", "write a handoff",
  "I'll continue this tomorrow", "load the handoff", "pick this up".
argument-hint: "[save | load [path]]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Hand off session

Save turns this session's working state into one file a later session can resume from cold. Load
reads that file back and continues from it. The file replaces the transcript: everything needed is
in context _now_, and reconstructing it later from a transcript costs far more than writing it.

Pick the mode from `$ARGUMENTS` or the request: `save` when the state must outlive the session,
`load` when a new session starts from one. With no clear mode, saving is the default, because a
spare handoff file costs nothing and a missing one loses the state.

## Save

1. **Leave nothing half-applied.** Finish the edit or command in flight, or revert it and record it
   as open. Do not start new work to make the snapshot look tidier.
2. **Describe the working tree, do not change it.** Commit uncommitted changes only if committing
   was already authorized. Saving a handoff authorizes no commit, stash, or push.
3. **Write the handoff file** to
   `.agents_workspace/handoff/HANDOFF-<YYYYMMDD-HHMM>-<session-id-prefix>.md` in the working
   directory, in the format under Output. Create the directory if needed. Take the timestamp from
   a single `date` call and the session id prefix from the first 8 characters of
   `${CLAUDE_SESSION_ID}`. A caller that passes its own header lines (a usage window, a reason)
   gets them added under the title.
4. **Append one line to the global index** at `~/.claude/handoff/index.md`, creating it if absent:
   `- <YYYY-MM-DD HH:MM> — <cwd> — <branch or "no git"> — <one-line state> — <file path>`.
   The index is what finds the file days later without remembering which directory it was in.
5. **Report the file path and its content** as your message, so the handoff is readable without
   opening the file.

Saving does not end the session. Keep working afterwards if the user asks, and save again later:
each save is a new file, never an edit of an old one.

## Load

1. **Find the file.** Use the path given. Otherwise take the newest `HANDOFF-*.md` in
   `.agents_workspace/handoff/`, and if there is none, the newest index line in
   `~/.claude/handoff/index.md` whose cwd matches. If several plausible files exist and none was
   named, list the newest few with their one-line state and take the newest, saying so.
2. **Read it in full**, then check it against the world before trusting it: the branch exists and
   is checked out, files named under Done exist, `git log` and `git status` match the described
   state. Report every mismatch. The file is a snapshot and the repo may have moved on.
3. **State what you are resuming:** the goal, and the first Open item as the next step.
4. **Continue from the first Open item.** A Decisions pending entry that blocks that step goes to
   the user before any work on it.

## Rules

- Write for a reader with none of this context: exact file paths, branch names, commands. A line
  that only makes sense with the transcript open is a line to rewrite.
- Keep the file a bounded snapshot, short enough to read in full on load, never a log.
- Mark what was validated and what was not. Load treats an unmarked Done item as unverified.
- Resume by loading the file in a fresh session, not by replaying the old one with `--resume`.
  The replay pays again for the context the file exists to compress.

## Output

```markdown
# Handoff — <YYYY-MM-DD HH:MM>

**Repo / branch:** <path> / <branch or "no git">
**Session:** <session-id-prefix>

**Goal** — what this session set out to do:

- <one or two lines>

**Done** — completed and in what state (validated / not validated):

- <item — files touched, what was verified>

**In flight** — the step closed or reverted at the save:

- <state of the working tree, anything half-planned>

**Open** — remaining work, ordered; first item is the next actionable step:

1. <next concrete step, specific enough to execute cold>
2. <...>

**Decisions pending** — forks the user still has to resolve, if any.

**Resume with:** <one line: branch name, command to run, or file to open first>
```
