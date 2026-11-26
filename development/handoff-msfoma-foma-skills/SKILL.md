---
name: handoff
description: >-
  Writes a short session note so the next session resumes in one step. Use when the user says wrap up, done for today, continue later, or start a new session. Not for commits or docs.
license: Apache-2.0
metadata:
  level: "setup"
  uses: ""
  agents: ""
  tokens: "384"
---

Saves the state of the work in a note of at most 20 lines, so a fresh session continues without re-reading the history.

## Steps
1. Gather only from what this session already holds plus `git status --short` and the active plan (`Status:` lines). Read no other files.
2. Write `.scratch/handoff.md` (create the folder; overwrite the old note). The first line is `Next: <the exact first action>`: a command, `file:line`, or the plan task. Then, one line each where it applies: Goal; Done; In progress (and what is broken); Decisions not visible in code (path to the DEC entry if recorded); Don't redo (dead ends); Open questions.
3. Signals, one line each, only when the session had them: a user correction or the same failure twice (`learning`); stray files, `.bak`, scratch or debug leftovers (`tidying`). Name the files; touch nothing.
4. Ensure `.scratch/` is gitignored. If not, say so and ask before editing `.gitignore`.
5. Tell the user to run `/clear` and that the next session prints the `Next:` line by itself while the note is under 24 hours old.

## Rules
- No narration of the session; facts a next session cannot get from the code or git.
- Paths and one-line facts instead of pasted code, logs or diffs.
- Never commit the note, never call `/clear` yourself (a skill cannot).
- Nothing worth saving (clean tree, no plan, nothing open): say so and write no note.

## Report
- Note path, its `Next:` line, signals flagged.
- Not checked: <...>

Next: `/clear`; `/foma-skills:learning` or `/foma-skills:tidying` if flagged.
