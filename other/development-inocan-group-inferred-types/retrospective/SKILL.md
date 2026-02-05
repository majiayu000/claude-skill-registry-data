---
name: retrospective
description: Captures learnings from the current session and updates skill files. Use when ending a session, after solving problems, debugging issues, or when the user says "retrospective", "capture learnings", or "what did we learn".
---

# Session Retrospective

You are conducting a retrospective analysis of the current session to extract and persist learnings.

## Process

### 1. Analyze the Session

Review the conversation to identify:
- **Successes**: What approaches worked well
- **Failures**: What didn't work and why
- **Insights**: Non-obvious learnings that would help in future sessions
- **Patterns**: Recurring themes or issues

### 2. Categorize Learnings

Determine which skill domain each learning belongs to:
- **coding-workflow**: Code patterns, debugging, refactoring, best practices
- **infrastructure-debugging**: Dependencies, installation, environment, platform issues
- **cross-domain**: Failures that span multiple areas (log to failures-log)

### 3. Update Skill Files

For each learning, append to the appropriate file:

**For coding learnings**: Update `~/.claude/skills/coding-workflow/learnings.md`
**For infrastructure learnings**: Update `~/.claude/skills/infrastructure-debugging/learnings.md`
**For significant failures**: Also log to `~/.claude/skills/failures-log/failures.md`

### 4. Learning Entry Format

Use this format when adding entries:

```markdown
## [YYYY-MM-DD] - Brief Title

**Context**: What was being done when this was learned
**Outcome**: Success | Failure | Partial
**Insight**: The key takeaway or lesson learned
**Solution** (if applicable): What resolved the issue
**Tags**: #relevant #tags
```

## Guidelines

- Be concise but specific - future you needs to understand the context
- Include error messages or symptoms for failures
- Note platform-specific issues (Windows/Linux/Mac)
- Don't duplicate existing learnings - check first
- Prioritize actionable insights over observations

## After Updating

Summarize to the user:
1. How many learnings were captured
2. Which files were updated
3. Key insights extracted

## Reference Files

When updating, first read the existing content to avoid duplicates:
- [Coding Learnings](~/.claude/skills/coding-workflow/learnings.md)
- [Infrastructure Learnings](~/.claude/skills/infrastructure-debugging/learnings.md)
- [Failures Log](~/.claude/skills/failures-log/failures.md)
