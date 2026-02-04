---
name: concise-commit
description: Craft concise commit messages with technical precision
---

# Concise Commit Messages

## Core Rules

- Subject line: 50 characters max
- Imperative mood: "Add feature" not "Added feature"
- Present tense: "Fix bug" not "Fixed bug"
- Capitalize first word, no period at end
- Body (optional): Explain WHY, use bullets, 72 chars/line

## Format

**Subject line:**
```
<verb> <what> [context]
```

**With body (if needed):**
```
<subject line>

- Why this change matters
- Key impact or constraint
- Related context
```

## Action Verbs

**Specific (use these):**
- `add` - new feature, file, dependency
- `remove` - delete code, dependency, file
- `fix` - bug, error, regression
- `refactor` - restructure without changing behavior
- `extract` - pull out logic to separate unit
- `update` - modify existing (when more specific verb doesn't fit)

**Vague (avoid):**
- change, modify, adjust, tweak, improve

## Examples

**Good:**
```
Add user authentication module
Fix null pointer in payment processor
Refactor database queries to use connection pool
Extract validation logic to separate validator class
```

**Bad:**
```
Updated the code to make it better
Fixed some bugs and added new stuff
Changes to improve performance and fix issues
Added a new feature that allows users to authenticate
```

## Anti-patterns

❌ Paragraphs - use bullets instead
❌ Past tense - "Added" → "Add"
❌ Vague verbs - "Update" → "Extract/Refactor/Fix"
❌ Implementation details - focus on WHAT and WHY, not HOW
❌ Multiple unrelated changes - split into separate commits
