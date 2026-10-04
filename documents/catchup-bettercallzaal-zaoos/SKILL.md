---
name: catchup
description: Use when starting a new session, after /clear, or when context is lost and you need to understand current work state
disable-model-invocation: true
---

# Catchup — Quick Context Restore

Fast session start. Gather state, detect in-progress work, report concisely.

## Context to Gather

Run ALL of these:

```
Git branch:          !`git branch --show-current`
Git status:          !`git status --short`
Recent commits:      !`git log --oneline -5`
Uncommitted diff:    !`git diff --stat`
Staged diff:         !`git diff --cached --stat`
Untracked files:     !`git ls-files --others --exclude-standard`
```

Then detect in-progress work — this step is MANDATORY:

1. **Read diffs** (not full files): run `git diff` and `git diff --cached` to understand what changed
2. **Scan for TODOs**: in every file listed by `git status`, search for `TODO|FIXME|HACK|XXX|WIP` and record the file path + comment text
3. **Check for plan files**: look in `.superpowers/plans/` and `docs/superpowers/plans/` — if any exist, read them

## Output Format

Respond with EXACTLY these 4 sections. Total output MUST be under 500 words — aim for 200-400.

### Branch
State the current git branch name. Note if ahead/behind remote.

### Modified Files
List every file from `git status` with its path. Use a bullet list. Group by status (modified/staged/untracked) only if 10+ files; otherwise flat list is fine.

### In-Progress Work
This section is MANDATORY — never skip it, never leave it empty. Based on diffs and TODO scan:
- Summarize what was being worked on (1-2 sentences max)
- List any `TODO`, `FIXME`, `HACK`, `XXX`, or `WIP` comments found, with file path and comment text
- If a plan file exists, state its goal in one line
- If working tree is clean and no TODOs found, write exactly: "Clean working tree — no in-progress work detected."

### Suggested Next Steps
1-3 bullet points. Infer from the changes and TODOs what to do next.

## Rules

- Read-only — never modify files
- Read diffs, not full file contents
- Do NOT narrate commit history beyond the 5-line `git log` output
- Every file path from `git status` MUST appear in the Modified Files section
- The In-Progress Work section MUST contain concrete TODO/WIP findings or an explicit "none" statement
