---
name: handoff
description: Generate a structured handoff for agent or session transitions.
version: 0.1.0
execution-mode: side_effecting
argument-hint: "\"<TARGET_AGENT>\" [context]"
category: fleet-ops
status: candidate
---
# Handoff Command

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=handoff] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

Generate a structured handoff document when transitioning work between agents or sessions.

## Usage

```bash
[handoff]                        # Handoff for current session (generic)
[handoff] "kimi"                 # Handoff targeted at Kimi
[handoff] "ide-sonnet" "cost adapter wiring"  # Handoff to IDE with context
```

## When to Use

- Switching from Claude Code to IDE (Sonnet/Cursor)
- Handing work to Kimi for bold generation
- Ending a session with unfinished work
- Passing context to Codex for verification
- Any agent transition where context would be lost

## Evidence Gathering

Before writing the handoff, gather:

1. `git log --oneline -10` -- recent commits
2. `git status --short --untracked-files=all` -- tracked and untracked work
3. `git diff --stat` and `git diff --cached --stat` -- tracked unstaged/staged scope
4. Explicit untracked artifact receipt for any `??` files or directories: `wc -l <file>` or `find <dir> -type f | wc -l`
5. Recent bus entries from the canonical bus reader for the host, not a stale local TSV mirror
6. Any failing tests or CI status

`git diff --stat` omits untracked files. Do not describe handoff scope from diff
stat alone when `git status` shows `??` entries.

## Output Format

```
HANDOFF: <from> -> <to> | <YYYYMMDD-HHMMZ>
═══════════════════════════════════════════

## What Was Done
- <completed item with commit hash or evidence>
- <completed item with commit hash or evidence>

## What's Left
- [ ] <remaining task 1>
- [ ] <remaining task 2>

## Key Files Touched
- `example.py.py` -- <what changed>
- `output/target.py` -- <what changed>

## Branch (mandatory if not on main)
If any artifact is on a non-main branch, include:
```
Branch: <branch-name>
```
The next session can checkout in one step: `git checkout <branch-name>`.
Omit this field only if all work is on `main`.
(Origin: 2026-08-13 — prior session wasted multiple tool calls locating
OQ4 because it was on branch `docs/devin/omni-meta-proposals`, not main.
The summary mentioned the file path but not the branch.)

## Gotchas & Context
- <thing the next agent needs to know>
- <constraint, workaround, or trap to avoid>

## Test Status
- Tests: <passing/failing count>
- CI: <green/red/pending>

## Entry Points
- Start here: `<primary file or command>`
- Smoke test: `<command to verify things work>`
```

## Constraints

- DO NOT fabricate commit hashes, file paths, or test counts. Verify before citing.
- DO NOT omit known failures or blockers -- the receiving agent needs the full picture.
- DO NOT include secrets, tokens, or credentials in handoff documents.
- Keep it concise. The handoff should be scannable in 30 seconds.
- Always post a summary to the coordination bus after generating.

## Bus Integration

```
<timestamp_utc>	<from_agent>	<to_agent>	STATUS	HANDOFF: <1-line summary>
```

## Skill Chains

### Mandatory

- None — handoff is a transition artifact. Evidence gathering (step 1) is the built-in check.

### Advisory

- **Before handoff**: `[session-metrics]` (capture metrics for the handoff)
- **After handoff**: `[end-session]` (if ending session), `[bus]` (STATUS post)
- **For cross-agent**: `[delegate]` (prepare task for delegation with guardrails)

## Authority

- **T1 (TRUSTED)**: May run without restriction
- **T2 (Active/High)**: May run without restriction (read-only — gathers evidence, writes handoff doc)
- **T3 (Medium)**: May run without restriction (read-only transition artifact)
- **T4 (Probationary)**: May run (read-only — no destructive actions)
- **Operator**: Override any restriction
