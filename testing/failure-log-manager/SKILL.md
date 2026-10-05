---
name: failure-log-manager
description: This skill should be used when the user asks to "log a failure", "remember this mistake", "add to failure log", "what mistakes to avoid", "check failure log", or when a mistake is detected that should be recorded for future reference. Manages persistent failure memory.
---

# Failure Log Manager

Manages the persistent failure log at `.claude/failure-log.local.md` to prevent repeating mistakes across sessions.

## Activation Triggers

This skill activates when:
- User asks to log a mistake or failure
- A pattern violation or error is detected
- User wants to review known mistakes
- Adding, viewing, or managing failure entries

## File Location

```
.claude/failure-log.local.md
```

This file is project-specific and should be in `.gitignore`.

## File Format

```markdown
---
enabled: true
last_updated: 2026-01-01T10:30:00Z
---

# Failure Log

## Pattern Mistakes

### [YYYY-MM-DD] Brief title
**Context:** What was being done
**Mistake:** What went wrong
**Correct:** What should be done instead
**Category:** imports|security|testing|architecture|conventions

## Failed Approaches

### [YYYY-MM-DD] Brief title
**Context:** What was being attempted
**What failed:** Why the approach didn't work
**Better approach:** What works instead
**Category:** imports|security|testing|architecture|conventions
```

## Categories

| Category | Description | Examples |
|----------|-------------|----------|
| `imports` | Wrong import patterns | Relative imports, missing aliases |
| `security` | Missing security checks | No permission classes, exposed secrets |
| `testing` | Wrong test approaches | unittest vs pytest, missing fixtures |
| `architecture` | Structural mistakes | Wrong file locations, missing layers |
| `conventions` | Code style violations | Naming, formatting, patterns |

## Adding Failures

### Pattern Mistake Entry

For recurring pattern violations:

```markdown
### [2026-01-01] Wrong import pattern in Django
**Context:** Writing user service
**Mistake:** Used `from users.models import User` instead of alias pattern
**Correct:** Use `import users.models as _users_models`
**Category:** imports
```

### Failed Approach Entry

For approaches that don't work:

```markdown
### [2026-01-01] Tried unittest instead of pytest
**Context:** Writing tests for user service
**What failed:** unittest assertions don't integrate with Django fixtures
**Better approach:** Use pytest with factory_boy for test data
**Category:** testing
```

## Reading Failures

To check the failure log:

1. Read `.claude/failure-log.local.md`
2. Parse entries under each section
3. Use category to filter relevant failures
4. Apply lessons to current task

## Creating Initial Log

If no failure log exists, create with template:

```markdown
---
enabled: true
last_updated: CURRENT_ISO_TIMESTAMP
---

# Failure Log

This log tracks mistakes to prevent repeating them across sessions.

## Pattern Mistakes

_No pattern mistakes logged yet._

## Failed Approaches

_No failed approaches logged yet._
```

## Updating Log

When adding a new failure:

1. Read existing file
2. Update `last_updated` in frontmatter
3. Add new entry under appropriate section (Pattern Mistakes or Failed Approaches)
4. Maintain chronological order (newest first)
5. Write updated file

## Best Practices

### What to Log

Log failures that are:
- Likely to recur (pattern-based mistakes)
- Non-obvious (not caught by linting)
- Project-specific (conventions unique to codebase)
- Costly to repeat (security, architecture)

### What NOT to Log

Skip failures that are:
- One-time typos
- Already caught by linting/tests
- Generic programming errors
- Not actionable

### Entry Quality

Each entry must have:
- Clear date for context
- Specific mistake description
- Actionable correct approach
- Appropriate category

## Integration with Hooks

The `UserPromptSubmit` hook automatically injects a condensed summary of failures into context. The summary includes:
- Total failure count
- One-line summary per failure
- Reference to full log file

This ensures failures are always visible without overwhelming context.
