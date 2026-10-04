---
name: save-session
description: Use when the user invokes it to save an unfinished session's state for a fresh session after a clear. Not for a plan another executor runs, which spec owns, or finished work, which the commit and pull request record.
argument-hint: "[what the next session must not lose]"
disable-model-invocation: true
---

# Handoff

Freeze what this session knows and the next one cannot rebuild. The enemy is the handoff that pastes the transcript back, so the fresh session pays again for the context the clear just bought. The overcorrection is a page of headlines naming no file, no command and no next step, leaving the reader to rediscover the work.

## Before writing

- Take no irreversible action to pause: no pull request and no push unless one was already out.
- Stop at a safe boundary: finish the current atomic step or back it out, and start nothing new.
- On a branch other than the repository's default, commit every uncommitted edit as one `wip:` commit first.
- Say in that commit's body when the tree is broken.
- On the default branch, leave the edits uncommitted and list them under `## Current state`.
- Preserve verbatim any artefact the user explicitly asked to survive the clear, such as a question list or a checklist.

## Pointers, not content

- Name a path, a command, an issue number or a line range in each section, and stop there.
- Paste no diff, no file body and no log, because the reader can open them and pasting spends the context the clear freed.
- Of an error, paste only its failing lines.
- Quote a value only when it exists nowhere on disk, such as a number from a run that was not logged.

## Where it goes

1. Read the location, never guess it: `node "${CLAUDE_SKILL_DIR}/scripts/handoff.mjs" path` prints it, the same file `hooks/session-start.mjs` points a resuming session at.
2. A branch name holding `/` makes a nested path: create the parent directories first.
3. Write the file whole, replacing any handoff already at that path: the state it held is what this clear discards.

## What it holds

The first line under the H1 is `Written: <YYYY-MM-DD>, HEAD <short commit>, branch <name>`, the commit from `git rev-parse --short HEAD`.

Then these sections, in this order, each left out when the session has nothing true to put in it:

- `## Goal`: what the work is for, in one or two sentences, and what it will not do.
- `## Current state`: what exists and works now, and what is half-built, each named by file.
- `## Decisions`: one line each, `<decision>, decided by <the user | this session>`.
- `## Files touched`: path, then one clause of what changed there.
- `## Proven`: one line per claim, `<claim>: <the command that proved it>, <its result>`.
- `## Next step`: exactly one action, the first thing the fresh session does.
- `## Open questions`: what is unresolved, and who can answer it.
- `## Resume`: never left out, unlike the sections above it.

In those sections:

- Record a decision the user made as theirs, in their wording, never as a shared one.
- When a plan is running and `<plan stem>-decisions.md` sits beside it, carry its lines into `## Decisions` unchanged.
- Put a claim no command proved under `## Open questions`, not `## Proven`.
- Read `## Current state` from `git status --short`, not from memory.
- List which changes are committed, then every uncommitted path in full, because a next session that cannot see the difference treats working-tree edits as saved and discards them.
- When the session was running a plan, open `## Current state` with the plan path and the number of the task in progress.

## Resume

Copy this paragraph into `## Resume` exactly, so the session that reads the note inherits the rule without reading this skill:

```text
Diff what `## Proven` and `## Files touched` already cover against what `## Next step` and `## Open questions` still need, name the resume point, and repeat no step `## Proven` already covers. Verify an inherited claim against the real artifact before building on it — a prior session's report is not the proof.
```

## References

| File | Read it when |
|---|---|
| `references/reconstructing-without-a-note.md` | Save-session itself starts without a note and must rebuild context before saving. |

## Judgment

- A file read this session outranks memory of it: confirm a path, a branch and a commit with a command before writing it down.
- A short handoff that is true outranks a full one that guesses; what the session does not know goes under `## Open questions`.
- The turn ends by naming the written path and saying to run `/clear`. Nothing else is written, and no work continues after it.
