---
name: gh-issue-templates
description: Standardized GitHub issue templates for bugs, features, and tasks. Provides title formats, body structure, and required sections. Use when creating issues to ensure consistency. Includes copy-paste templates in templates/ directory.
---

# Issue Templates

Standardized formats for creating GitHub issues with consistent structure.

## Quick Reference

| Type | Title Prefix | Key Sections |
|------|--------------|--------------|
| Bug | `bug:` | Describe, Expected, Steps, Environment |
| Feature | `feat:` | Problem, Solution, Alternatives, Acceptance |
| Task | `task:` or `chore:` | Description, Checklist, Context |

## Bug Report Format

**Title:** `bug: <short description>`

**Body:**
```markdown
## Describe the bug
<!-- What happened? -->

## Expected behavior
<!-- What should have happened? -->

## Steps to reproduce
1.
2.
3.

## Environment
- OS:
- Version:
- Relevant config:

## Logs/Screenshots
<!-- If applicable -->
```

### Bug Examples

**Good:**
- `bug: login fails with expired OAuth token`
- `bug: dashboard crashes when filter is empty`

**Bad:**
- `bug: it's broken`
- `bug: doesn't work`

## Feature Request Format

**Title:** `feat: <short description>`

**Body:**
```markdown
## Problem
<!-- What problem does this solve? -->

## Proposed solution
<!-- How should it work? -->

## Alternatives considered
<!-- Other approaches you thought of -->

## Acceptance criteria
<!-- How do we know it's done? -->
- [ ] Criterion 1
- [ ] Criterion 2
```

### Feature Examples

**Good:**
- `feat: add CSV export for reports`
- `feat: support dark mode in settings`

**Bad:**
- `feat: make it better`
- `feat: new feature`

## Task Format

**Title:** `task: <short description>` or `chore: <short description>`

Use `task:` for project work, `chore:` for maintenance/deps/infra.

**Body:**
```markdown
## Description
<!-- What needs to be done? -->

## Checklist
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Context
<!-- Why is this needed? -->
```

### Task Examples

**Good:**
- `task: set up CI pipeline`
- `chore: upgrade React to v19`
- `chore: update dependencies`

**Bad:**
- `task: do the thing`
- `chore: stuff`

## Template Selection Guide

```
Is something broken?
  YES → Bug Report
  NO  → Continue

Is this new functionality?
  YES → Feature Request
  NO  → Continue

Is this maintenance/infrastructure?
  YES → Task (chore:)
  NO  → Task (task:)
```

## Template Files

See `templates/` for copy-paste ready files:
- `bug.md` - Bug report template
- `feature.md` - Feature request template
- `task.md` - Task/chore template

## Integration with Other Components

### After Creating Issue
After using this skill to create an issue, use:
- **gh-issue-triage** skill to apply appropriate labels and priority
- **gh-wrangler** agent to create the issue via gh CLI

### Workflow
1. Use **gh-issue-templates** (this skill) to format the issue
2. Use **gh-issue-triage** to determine labels and priority
3. Use **gh-wrangler** to create the issue with `gh issue create`
4. Use **gh-issue-lifecycle** to manage state transitions

## Related

- Skill: `gh-issue-triage` - Labeling and prioritization rules
- Skill: `gh-issue-lifecycle` - State transitions and linking
- Agent: `gh-wrangler` - Interactive issue management
