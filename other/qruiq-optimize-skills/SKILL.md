---
name: qruiq-optimize-skills
description: |
  Summarize the current session's execution history, analyze which skills were used and how,
  then propose optimizations to those skill definitions. All changes must be confirmed by the
  user before writing to files.
  Use when asked to "optimize skills", "improve skills", "review skills", "refine skills",
  or "总结优化 skills".
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# qruiq-optimize-skills

Analyze the current conversation to understand which skills were invoked, how they performed,
and propose concrete improvements — but **never write changes without user approval**.

## Steps

**Execute all steps directly. Do not list as TODOs.**

### 1. Summarize session execution history

Review the current conversation context and summarize:
- Which skills were invoked (in order)
- What parameters were used
- What succeeded, what failed, and any friction points
- Any steps that were skipped, repeated, or manually corrected by the user

Present the summary to the user in a clear table or list.

### 2. Read the relevant skill definitions

For each skill identified in step 1, read its `SKILL.md`:

```
~/.qruiq/skills/skills/<skill-name>/SKILL.md
```

Also scan for any template files or supporting assets in the skill directory.

### 3. Identify optimization opportunities

Analyze each skill definition against the session history and look for:
- **Missing steps**: actions that had to be done manually but should be in the skill
- **Incorrect or outdated instructions**: steps that produced errors or needed adjustment
- **Unclear parameters**: parameters that caused confusion or were missing
- **Redundant steps**: steps that are no longer needed or can be combined
- **Better defaults**: values that could be pre-filled or inferred
- **Missing error handling**: foreseeable failures that should be addressed
- **Description/trigger improvements**: better trigger phrases or descriptions

### 4. Present proposed changes to the user

For **each** skill that has proposed changes, present a clear diff-style summary:

```
## <skill-name>

### Change 1: <short description>
- Before: <current text>
- After: <proposed text>
- Reason: <why this improves the skill>

### Change 2: ...
```

Then ask the user: **"确认以上变更？可以逐条确认或全部接受/拒绝。"**

### 5. Apply confirmed changes only

- Only write changes the user has explicitly approved
- For each approved change, edit the corresponding `SKILL.md` (or template files)
- After all edits, show a final summary of what was changed

## Rules

- **NEVER** write to any skill file without explicit user confirmation
- Present all changes as before/after comparisons so the user can review
- If no optimizations are found, say so — do not invent unnecessary changes
- Keep skill definitions concise; do not over-engineer
- Preserve the existing frontmatter format (`name`, `description`, `allowed-tools`)
