---
name: handoff
description: Summarize the current session for handing off to another session. Use when the user wants to end the current session and transfer context to a new session.
---

Create a handoff summary to transfer the current session context seamlessly to another session.

## Process

1. **Gather context**:
   - Review conversation history to identify active tasks.
   - Note the current working directory, project context, and any running processes/servers.
   - List uncommitted modified files using `jj diff -s` or `git status`.
   - Capture user preferences, constraints, instructions, and recent debugging state (errors or failures).

2. **Identify command patterns & skills**:
   - Record project-specific commands (build, test, lint, etc.) and custom scripts/aliases.
   - Note custom agent skills used during the session (e.g., `jujutsu`, `clickup`, `context7`).

3. **Determine remaining work**:
   - List incomplete tasks, TODOs, and next steps or planned actions.
   - Identify specific files the next agent should read first and note any blockers/issues.

## Output Format

The handoff file should follow this structure:

```markdown
# Handoff - <Timestamp>

## Current Context

- Working directory: `<path>`
- Project: `<project name and brief description>`
- Uncommitted changes: `<summary of jj diff -s>`

## What We Were Working On

<Summary of the task, feature, bug fix, or investigation in progress>

## Files to Read First

- `<path/to/file1>` - <why it's relevant>
- `<path/to/file2>` - <why it's relevant>

## Key Context & Decisions

- <Important decisions made or context discovered>
- <User constraints or preferences established>
- <Environment state worth preserving (e.g., running dev servers)>

## Recent Errors / Debugging State

- <Exact error message or test failure being investigated, or "None">

## Command Patterns & Skills Used

- `<command>` - <what it's for>
- `<skill-name>` - <custom skills the next agent should be aware of>

## What's Left to Do

- [ ] <Incomplete task 1>
- [ ] <Incomplete task 2>
- [ ] <Next planned step>

## Blockers/Issues

- <Any blockers encountered, or "None">

---
```

## Output Location

Write to `HANDOFF.md` in the current working directory unless the user specifies a different path.

Guidelines:

- Check if the handoff file already exists before writing.
- If updating, preserve existing content and add a new section with the current timestamp.
- Keep summaries concise while ensuring enough context remains for a seamless handoff.
- Never include sensitive information (e.g., passwords, API keys, or tokens).
