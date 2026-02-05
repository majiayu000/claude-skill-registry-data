---
name: task-create
description: Create structured task files for planning dev work. Use when user asks to "create a task", "add a task", "plan a task", or needs to document work items. Creates numbered markdown files in docs/planning/tasks/.
---

# Task Create

Create numbered task files following project conventions.

## Workflow

**IMPORTANT:** Use the `aaa` binary directly, NOT `bun --cwd tools run dev`.

1. **Create file**: `aaa task create <kebab-name>` → returns filepath
2. **Write content** using template below
3. **Link to story** if applicable (add `**Story:**` header)

## Template

```markdown
## Task: [Short descriptive name]

**Story:** [story-name](../stories/NNN-story-name.md) *(optional)*

### Goal
[One sentence: what should be true when this is done?]

### Context
[Why this matters. Current state, trigger, constraints, dependencies]

### Plan
1. [First concrete action]
2. [Second action]
3. [Continue as needed]

### Acceptance Criteria
- [ ] [Specific, testable outcome]
- [ ] [Another outcome]

### Test Plan
- [ ] [What tests to add/run]
- [ ] [Manual verification if needed]

### Scope
- **In:** [What this includes]
- **Out:** [What this explicitly excludes]

### Notes
[Optional: Technical considerations, risks, edge cases]
```

## Required Sections

| Section | Purpose |
|---------|---------|
| Goal | One sentence outcome - "what's true when done?" |
| Context | The why: problem, trigger, constraints |
| Plan | Numbered concrete actions |
| Acceptance Criteria | Checkboxes for verification |
| Test Plan | What tests to add/update/run |
| Scope | Explicit In/Out boundaries |

## File Location

- Default: `docs/planning/tasks/NNN-name.md`
- Custom: `aaa task create <name> --dir <path>`
