---
name: handoff
description: 'Writes a handoff file a fresh session loads after /clear, or resumes from one. Use when a hook says a handoff is due, or the user says "write a handoff", "hand off" or "resume from the handoff". Not for saving a note (use memory-note).'
argument-hint: '[resume [path to a .mz/handoff/ file]]'
allowed-tools: Bash(${CLAUDE_PLUGIN_ROOT}/scripts/handoff-facts.sh), Bash(${CLAUDE_PLUGIN_ROOT}/scripts/handoff-facts.sh *), Bash(git log *), Bash(git status *), Read, Write, Edit, AskUserQuestion
---

# Handoff

## Overview

A long session loses detail with every compaction, because each one summarizes a summary. This skill moves the session into a file a fresh session can trust, built from the transcript and git rather than from what the current context still remembers. After the file exists, the user types `/clear`, and this plugin's SessionStart hook loads that terminal's handoff into the new session.

The Stop hook asks for a handoff once the main conversation has been compacted `MZ_HANDOFF_AFTER` times (default 3; `0` turns the nudge off). The user can also ask for one at any time.

## When to Use

- **Write mode** (default): the Stop hook reported that the handoff threshold was reached, or the user asks to write a handoff, hand off, or wrap up for a fresh session.
- **Resume mode** (`resume`): the session-start context names a handoff, or the user asks to resume, continue or pick up from a handoff.

### When NOT to use

- One fact or decision to keep across sessions → memory-note.
- A pipeline run that only needs its own resume → that skill reads its `.mz/task/<task_name>/state.md`. The handoff points at the task dir and never replaces its state.

## Input

`$ARGUMENTS`: empty for write mode, or `resume` followed by an optional handoff path. Anything else → ask via AskUserQuestion which mode was meant.

## Constants

- **FACTS_SCRIPT**: `${CLAUDE_PLUGIN_ROOT}/scripts/handoff-facts.sh`
- **HANDOFF_DIR**: `.mz/handoff/` under the project root
- **MAX_LINES**: 150 (the whole handoff file, frontmatter included)

## Core Process

### Phase Overview

| Phase | Goal                                 | Details      |
| ----- | ------------------------------------ | ------------ |
| W1    | Gather facts                         | Inline below |
| W2    | Write the handoff                    | Inline below |
| W3    | Tell the user to /clear              | Inline below |
| R1    | Pick the handoff                     | Inline below |
| R2    | Check it against git and the old run | Inline below |
| R3    | Claim it and report                  | Inline below |

### Phase W1: Gather Facts

When the hook's message names this session's transcript, run `FACTS_SCRIPT <that path>`. Otherwise run `FACTS_SCRIPT` with no arguments, and it looks the transcript up through `CLAUDE_CODE_SESSION_ID`. It prints:

- a header of `key: value` lines (`handoff_file`, `session_id`, `claude_pid`, `transcript`, `written_at`, `compactions`, `cwd`, `branch`, `head`);
- running tasks, git status, the commits since the session started and the files the session wrote;
- the user's own messages, verbatim, oldest first.

These facts outrank your memory of the session. Where the two disagree, write what the facts say. When the lookup finds no transcript, the output ends with a "Transcript facts unavailable" section instead of the files and messages: take the user's words from the conversation, and still write to `handoff_file`.

### Phase W2: Write the Handoff

Write the file at the header's `handoff_file` path with the Write tool. That path already points at this session's earlier handoff when there is one, so a second run rewrites it in place. Follow the template below, and stay within MAX_LINES.

- **Frontmatter**: copy `session_id`, `claude_pid`, `transcript`, `written_at`, `compactions`, `cwd`, `branch` and `head` from the header. Set `task` to the running task dir, or `none`. Set `status: open`.
- **Goal**: what the user is trying to get done, in one or two lines, plus the criterion that means done.
- **Constraints (verbatim)**: the user's own words that limit how the work is done, quoted from the user-message facts with their time. Don't paraphrase them; summaries lose constraints first.
- **Decisions**: choices made and why. Point at the task's `state.md` or `.mz/journal.md` rather than copying them.
- **Done (verified)**: only items with evidence: a commit from the facts, a path that exists, or a command and the result it gave in this session.
- **Assumed, not verified**: everything you believe is done but can't point to evidence for.
- **Tried and failed**: approaches that didn't work and why, so the next session doesn't repeat them.
- **Next**: one to three concrete steps, the first one doable straight away.
- **Open questions**: what only the user can decide.
- **Files touched**: up to 15 paths from the facts, each with its role.
- **Verify on resume**: the exact commands that prove the current state, with the result expected.

Write `[redacted]` for any secret or `<private>` text in the facts. The task's `state.md` stays the source of truth for a running pipeline; the handoff names it and adds only what it lacks.

```markdown
---
schema: handoff/1
session_id: <from facts>
claude_pid: <from facts>
transcript: <from facts>
written_at: <from facts>
compactions: <from facts>
cwd: <from facts>
branch: <from facts>
head: <from facts>
task: .mz/task/<task_name>/ or none
status: open
---
## Goal

## Constraints (verbatim)
> "<the user's words>" (user, <time>)

## Decisions

## Done (verified)
- <item>. Evidence: <commit | path | `command` → result>

## Assumed, not verified

## Tried and failed

## Next
1. <step>

## Open questions

## Files touched
- <path>: <role>

## Verify on resume
- `<command>` → <expected result>
```

### Phase W3: Tell the User

Tell the user, in one short message: the handoff path, that typing `/clear` starts a fresh session in this terminal which loads it, and that they can edit the file first. Then stop. Don't start new work in the old context.

### Phase R1: Pick the Handoff

Use the path from `$ARGUMENTS`, or else the one the session-start context names. Otherwise read the frontmatter of the files in HANDOFF_DIR, newest first, and keep those with `status: open`. One left → use it. Several → AskUserQuestion with up to four of them, each labeled by path, branch and goal. None → say there is no open handoff and stop.

### Phase R2: Check It Against Git and the Old Run

1. Read the whole handoff.
1. Run `git log --oneline <head>..HEAD` and `git status --short` to see what changed after it was written.
1. If its `transcript` still exists, run `FACTS_SCRIPT --since <written_at> <transcript>`. User messages listed there came after the handoff and override it.
1. Run each "Verify on resume" command. A "Done" item that the results contradict counts as not done.
1. If `task` names a task dir, read its `state.md`. Resuming that pipeline belongs to its own skill, so name the skill and the task dir to the user.

### Phase R3: Claim It and Report

1. Change the handoff's frontmatter line to `status: claimed <CLAUDE_CODE_SESSION_ID>` with Edit, so later sessions don't load it again.
1. Report in at most five lines: the goal, where the work stands, what changed since the handoff, the verify results and the next step.
1. Ask whether to go ahead with the next step.

## Common Rationalizations

| Rationalization                                 | Rebuttal                                                                            |
| ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| "I remember the session well enough"            | after several compactions you remember a summary; the facts script reads the record |
| "paraphrase the constraints, it's shorter"      | constraints are what summaries lose; quote the user                                 |
| "mark it done, I'm fairly sure it works"        | belief without evidence goes under Assumed, or the next session trusts it           |
| "copy the task's state.md into the handoff"     | two copies drift; point at the task dir                                             |
| "carry on with the work after writing the file" | the old context is the problem; the user's /clear is the next step                  |

## Red Flags

- A "Done" line with no commit, path or command result.
- A constraint written in your words instead of the user's.
- A handoff over MAX_LINES, or one that repeats a task's `state.md`.
- Resume mode trusting the file without running its verify commands.
- A secret copied from the user messages into the file.

## Error Handling

- FACTS_SCRIPT exits 1 (`jq` missing, or the transcript you named doesn't exist) → surface its stderr. Write the handoff to `.mz/handoff/<YYYY_MM_DD_HHMM>_<first 8 characters of the session id>.md` from what you can still check (git, task state), and say in the Goal section that the transcript facts were unavailable.
- The handoff path can't be written → surface the error and stop. Don't fall back to a different directory.
- A verify command fails in resume mode → report it as the current state. Don't fix it before the user has seen the report.

## State Management

This skill is single-shot and keeps no `.mz/task/` state. The handoff file is its only artifact. The hooks keep two marker directories, `.mz/handoff/.due/` and `.mz/handoff/.nudged/`, which the skill never touches.
