---
name: checkpoint
description: Save and resume working state across sessions, with subcommands save, resume, and list. Captures git state, decisions made, remaining work, and modified files so a new session can pick up where the last one left off. Use when user says "checkpoint", "save progress", "save state", "resume", "pick up where I left off", or wants to preserve session context. For git commits, use /ship commit; for retrospectives, use /retro; for planning, use /plan.
argument-hint: "/checkpoint save [purpose] | /checkpoint resume [id] | /checkpoint list"
allowed-tools: "Read, Write, Bash, Glob, Agent, AskUserQuestion"
---

## Overview

Persist working state to disk so a future session can restore full context without the user re-explaining everything.

## Subcommand Routing

| Invocation | Action |
|-----------|--------|
| `/checkpoint save` | Capture current state to a checkpoint file |
| `/checkpoint save <purpose>` | Capture state tailored to what the next session will be used for |
| `/checkpoint resume` | Restore context from the most recent checkpoint |
| `/checkpoint resume <id>` | Restore context from a specific checkpoint |
| `/checkpoint list` | Show all available checkpoints |
| `/checkpoint` | Default to `save` |

## When to Use

Decide at a phase boundary, the point where one chunk of work such as an interview, an implementation, or a QA pass is done. Mid-phase there is nothing to decide: continue, or hand the remaining work to subagents. Work the questions in order; the first yes wins.

1. **Continue?** Yes when the next phase needs this session as a primary source, as implementation needs the interview that preceded it, or when enough context is left for the next phase to fit. Continuing loses nothing, so rule it out first.
2. **`/clear`?** Yes when everything in the session, the exploration, the decisions, and the dead ends, is irrelevant to what comes next. Clearing a relevant session loses the reasoning behind the work, and reading the diff back does not recover it.
3. **`/checkpoint save`?** Yes when the state has to travel: a fresh session will pick it up, the work moves to another directory, repository, or harness, a colleague takes it over, or a side task found mid-phase is forked off without derailing the current one.
4. **Subagent?** Yes when the task is scoped tightly enough to run unattended, such as a review of a finished diff. Spawn it with the Agent tool and keep this session untouched.
5. **`/compact`.** The default, reached last: relevant context, same place, and the user stays in the loop. Pass an instruction naming the next phase, such as `/compact we are about to QA the importer`, so the summary keeps what that phase needs.

Every option except continuing turns the session into a summary of itself, which is lossy. Pay that loss only when staying costs more than it saves.

## Storage

Inside a git repository, the checkpoint is the project workspace's `PROMPT.md`, per [`rules/project-workspace.md`](../../rules/project-workspace.md). Resolve the workspace root with [`hooks/_lib/project_workspace.py`](../../hooks/_lib/project_workspace.py), never by guessing:

```bash
python3 -c 'import sys,pathlib; sys.path.insert(0, str(pathlib.Path.home()/".claude/hooks")); from _lib import project_workspace as pw; top = pw.toplevel(pathlib.Path.cwd()); print(top / pw.resolve_root(top))'
```

The file is overwritten in place on every save. Outside a git repository, checkpoints go to `~/.claude/checkpoints/<YYYYMMDD-HHmmss>.md`. Files already in `~/.claude/checkpoints/` stay readable by `resume` and `list`.

## Process

### Save

1. **Gather git state.** Run these in parallel:
   - `git branch --show-current` to capture the active branch.
   - `git log --oneline -5` to capture recent commits.
   - `git status --short` to capture uncommitted changes.
   - `git diff --stat` to capture the scope of modifications.

2. **Gather session context.** When a purpose argument was given, it names what the next session will do; keep what that work needs and drop the rest. From the current conversation, extract:
   - The current task description.
   - Decisions made during the session, with rationale.
   - Files modified or created.
   - Files read that are relevant to the task.
   - Any blockers or open questions.
   - Next steps remaining.

3. **Write the checkpoint file.** Inside a repository, write `<root>/PROMPT.md` with the required sections and template from [`standards/project-workspace.md`](../../standards/project-workspace.md): identity with a README pointer, read first, hard constraints, dated state, numbered next steps, decided against. Carry the decisions, modified files, blockers, and suggested skills gathered above into those sections. When a purpose was given, state it at the top and order the next steps around it. Outside a repository, create `~/.claude/checkpoints/<YYYYMMDD-HHmmss>.md`, named by the GMT save time so a filename sort is a time sort, with this structure:

   ```markdown
   # Checkpoint: <YYYYMMDD-HHmmss>

   **Saved:** <GMT timestamp>
   **Branch:** <branch name>
   **Project:** <repo root path>
   **Purpose:** <what the next session will be used for, when given>

   ## Task

   <current task description>

   ## Decisions

   - <decision 1>: <rationale>
   - <decision 2>: <rationale>

   ## Modified Files

   - <file path 1>
   - <file path 2>

   ## Recent Commits

   <output of git log --oneline -5>

   ## Uncommitted Changes

   <output of git status --short>

   ## Next Steps

   1. <remaining step 1>
   2. <remaining step 2>

   ## Blockers

   - <blocker or open question, if any>

   ## Suggested skills

   - <skill 1> -- <why the resuming agent should consider it>
   - <skill 2> -- <why>
   ```

   Reference other artifacts instead of copying them: a commit by SHA, a spec, plan, or ADR by path, a pull request or issue by URL. The checkpoint carries what no artifact holds, meaning the reasoning, the open questions, and the next step.

4. **Redact sensitive content.** Before writing the file, scan every section for sensitive material and replace with a `[REDACTED:<reason>]` token. Patterns to redact:
   - API keys, tokens, bearer credentials. Heuristics: high-entropy strings 32 chars or more, strings prefixed with `sk_`, `pk_`, `ghp_`, `Bearer `, `AKIA`.
   - Passwords, private keys, certificates. Patterns: `-----BEGIN`, `password=`, `pwd=`, `secret=`.
   - PII: email addresses, phone numbers, national identifiers, full names tied to non-public records.
   - Internal hostnames, internal URLs such as `*.internal`, `*.corp`, or `*.lan`, and IP addresses in RFC 1918 ranges when paired with a service name.
   The token must name the reason so a human reading the checkpoint can decide whether to fetch the real value: `[REDACTED:api-key]`, `[REDACTED:email]`.

5. **Pick suggested skills.** Choose 2 to 5 skills the resuming agent should consider, ranked by likely value. Examples: `/plan` if there is an open spec, `/test` if there are unrun tests, `/ship pr` if the work is ready to land, `/investigate` if a blocker is a bug.

6. **Confirm.** State the checkpoint ID and file path to the user.

### Resume

1. **Find the checkpoint.** If no ID is given and the workspace holds `PROMPT.md`, read it. Otherwise use the most recent file in `~/.claude/checkpoints/` sorted by filename. If an ID is given, read that specific file.

2. **Read the checkpoint file.** Parse all sections.

3. **Verify the environment.** Run these in parallel:
   - `git branch --show-current` to confirm the branch matches.
   - `git status --short` to see if files have changed since the checkpoint.
   - Verify the project directory matches.

4. **Output the context.** Present the full checkpoint contents to re-ground the session:
   - State the task.
   - List decisions already made.
   - List modified files.
   - State remaining next steps.
   - Flag any discrepancies between the checkpoint and the current git state.

5. **Proceed.** Ask the user which next step to start with, or continue from the first remaining step if the instruction is clear.

### List

1. **Read the checkpoints.** List the workspace `PROMPT.md` first when it exists, then all `.md` files in `~/.claude/checkpoints/`, sorted by name descending.

2. **Display a summary table:**

   | ID | Saved | Branch | Task |
   |----|-------|--------|------|

   Extract the branch and task from each file's header section.

## Rules

- Checkpoints are informational snapshots, not git operations. They never commit, stash, or modify the working tree.
- Timestamps use GMT, never local timezone.
- The checkpoint file must be self-contained for orientation. A reader with no prior context must understand the full state from the file alone, following SHAs, paths, and URLs for the detail those artifacts already hold.
- On resume, if the branch has diverged significantly from the checkpoint, warn the user before proceeding.
- Keep every checkpoint file. Only the user deletes one, by hand.
- Create the `~/.claude/checkpoints/` directory if it does not exist.
- Never stage or commit `PROMPT.md`. The workspace is excluded through `.git/info/exclude`, and [`hooks/project-workspace.py`](../../hooks/project-workspace.py) blocks a forced add.

## Common Rationalizations

- "The diff shows what I did, so the checkpoint can be short": the diff holds no rationale, no rejected options, and no next step. Write the decisions and the numbered next steps.
- "Pasting the spec into the checkpoint keeps it self-contained": a pasted copy drifts from the source. Reference it by path, SHA, or URL.
- "The token is needed to resume, so leave it in": the checkpoint is plain text on disk. Write `[REDACTED:<reason>]` and name where the real value lives.
- "Saving is always the safe choice": every save turns the session into a lossy summary. Work the When to Use questions first; continuing loses nothing.
- "The branch on resume is close enough": a mismatch means the next steps may target code that moved. Flag the discrepancy before proceeding.

## Red Flags

- Stop and redact when any section matches a pattern from step 4 of Save, such as `ghp_`, `-----BEGIN`, or an email address.
- Stop and warn the user when `git branch --show-current` on resume differs from the checkpoint's branch.
- Stop and resolve the workspace root with the helper script when about to write `PROMPT.md` to a guessed path.
- Stop and unstage when `git status` shows `PROMPT.md` staged.

## Verification

- The file exists at the confirmed path: `<root>/PROMPT.md` inside a repository, `~/.claude/checkpoints/<YYYYMMDD-HHmmss>.md` outside one.
- The file carries a GMT timestamp, the branch, numbered next steps, and 2 to 5 suggested skills.
- A scan of the file for `sk_`, `ghp_`, `AKIA`, `Bearer `, and `-----BEGIN` finds nothing outside `[REDACTED:...]` tokens.
- `git status --short` lists the same files before and after the save, and `PROMPT.md` is absent from it.
- On resume, every discrepancy between the checkpoint and the current git state is stated in the output.

## Related Skills

- `/ship commit` -- Commit changes after resuming and completing work.
- `/retro` -- Run a retrospective after a multi-session task.
- `/plan` -- Create a plan before starting work that checkpoints can reference.
