---
name: session-log
description: Summarize the current session's files changed, tests run, commits, and decisions as handoff or standup notes.
disable-model-invocation: true
argument-hint: "/session-log | /session-log export"
allowed-tools: "Read, Bash, Write, Skill"
sensitive: true
---

## Overview

Session activity logger that builds a summary of what happened in the current session. Useful for handoff between developers, standup preparation, and session documentation.

## When to Use

- Handing the work to another developer at the end of a session.
- Preparing standup notes from what the session actually changed.
- Recording what a long session did before the context is cleared.

For resumable working state, use `/checkpoint save`; for corrections that change how the assistant works, use `/retro`.

## Invocation

| Invocation | Action |
|-----------|--------|
| `/session-log` | Display session summary in the conversation |
| `/session-log export` | Export session summary as a markdown file |

---

## Steps

1. **Gather git activity.** Collect commits made during this session:
   - Run `git log --oneline --since="<session start or today>"` to find recent commits.
   - If no commits exist since today, check the last 24 hours.
   - For each commit: hash, message, files changed.

2. **Gather file changes.** Identify all files modified in the session:
   - Run `git diff --name-status` for uncommitted changes.
   - Run `git diff --cached --name-status` for staged changes.
   - Categorize: added, modified, deleted, renamed.

3. **Gather test activity.** Check if tests were run during the session:
   - Look for test output in the conversation history.
   - Summarize: test suite name, pass/fail counts, coverage if reported.

4. **Gather decisions.** Scan the conversation for decisions made during the session:
   - Architecture choices.
   - Trade-offs discussed and resolved.
   - Scope changes agreed upon.
   - Rejected approaches with reasons.

5. **Identify next steps.** Based on the session context:
   - What remains unfinished?
   - What follow-up tasks were identified?
   - What blockers exist?

6. **Format the output.** Compile into a structured summary.

### Output

```
## Session Log

**Date:** <timestamp GMT>
**Duration:** <approximate>
**Branch:** <current branch>

### Commits
| Hash | Message |
|------|---------|
| <short hash> | <commit message> |

### Files Changed
| Status | File |
|--------|------|
| M | <path> |
| A | <path> |
| D | <path> |

### Tests
| Suite | Passed | Failed | Coverage |
|-------|--------|--------|----------|
| <name> | <count> | <count> | <percentage or N/A> |

### Decisions
1. <Decision made and rationale>
2. <Decision made and rationale>

### Next Steps
- [ ] <Remaining task>
- [ ] <Follow-up identified>
- [ ] <Blocker to resolve>
```

### Export mode

When `/session-log export` is invoked:
- Inside a git repository, write the output to `session-log-<YYYY-MM-DD-HHMM>.md` in the project workspace, per [`rules/project-workspace.md`](../../rules/project-workspace.md). Resolve the workspace root with [`hooks/_lib/project_workspace.py`](../../hooks/_lib/project_workspace.py) the same way [`/checkpoint`](../checkpoint/SKILL.md) does, never by guessing:

  ```bash
  python3 -c 'import sys,pathlib; sys.path.insert(0, str(pathlib.Path.home()/".claude/hooks")); from _lib import project_workspace as pw; top = pw.toplevel(pathlib.Path.cwd()); print(top / pw.resolve_root(top))'
  ```

- Outside a git repository, write it to the scratchpad directory.
- The workspace is excluded through `.git/info/exclude`, so the export stays out of commits and the project's own files stay untouched.
- Confirm the file path after writing.

## Durable Facts

This skill runs only when the user invokes it. While building the log, route each finding by what it is:

| Finding | Destination |
|---------|-------------|
| Task state, open decisions, next steps | The log itself. When the work resumes in a later session, offer to call the Skill tool with `checkpoint` and the argument `save` |
| A fact a future session needs, such as a gotcha with no trace in code or a decision with lasting effect | Call the Skill tool with `brain` and the argument `capture`, once per fact, after the user approves the list |
| A correction to how the assistant works | Name it in the log and suggest `/retro`, which routes it to a rule, a skill, or the vault |

Never write `MEMORY.md` or any memory file. The memory directory is compiled from the vault, per the Knowledge Single Source of Truth section of [`CLAUDE.md`](../../CLAUDE.md). When `SECOND_BRAIN_VAULT` does not resolve to a directory, list the durable facts under a `Worth keeping` heading in the log and tell the user that no vault is configured to hold them.

## Rules

- All timestamps in GMT.
- Do not fabricate session activity. Only include what actually happened based on git history and conversation context.
- Decisions must reflect what was actually discussed, not inferred preferences.
- Keep each section concise. The reader needs a quick overview, not a transcript.
- If no activity exists in a section, state "None this session" instead of omitting the section.

## Common Rationalizations

- "The tests probably ran, so list them as passing": a test row needs output from this conversation. With no output, the Tests section says "None this session".
- "The project root is the obvious place for the export": the root belongs to the project. The export goes to the resolved workspace, which git ignores locally.
- "This fact is worth remembering, so write it to memory": memory is compiled from the vault. Route the fact through `brain` capture, or list it under `Worth keeping` when no vault exists.
- "The decision was implied, so record it": the Decisions section holds only what the conversation settled out loud.

## Red Flags

- Stop and drop the row when a commit, test result, or decision has no source in `git log` or the conversation.
- Stop and resolve the workspace with the helper when the export path you are about to write is the repository root or a tracked directory.
- Stop and ask for approval of the fact list before the first `brain` capture call.
- Stop and convert to GMT when a timestamp carries a local offset.

## Verification

- Every commit hash in the log appears in `git log` output from this session.
- Every section is present, with "None this session" where it is empty.
- An export lands under the resolved workspace root or the scratchpad directory, and `git status --short` does not list it.
- No file in the memory directory was written.

## Related skills

- `/retro` -- Deeper retrospective that persists learnings as config.
- `/checkpoint` -- Save working state for cross-session resumption.
- [`/morning`](../morning/SKILL.md) -- Start-of-day sweep of pending work across every git account.
- `/ship commit` -- Commit changes identified in the session log.
