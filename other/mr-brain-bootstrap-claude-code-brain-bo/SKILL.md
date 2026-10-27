---
name: mr
description: Generate a PR/MR description after the review passes. Use after /review confirms the code is ready to merge. Reads claude/templates.md for the required format.
---

# MR/PR Description Skill

Generate a structured pull request description.

## Prerequisites
- `/review` MUST pass (verdict: PASS, confidence ≥ 95) before generating a PR description
- All tests must be green
- No blocking issues from the review

## Protocol

### 1. Verify prerequisites
```bash
# Confirm tests pass
# (use the test command from claude/build.md)
```
If tests fail: STOP. Fix before generating the PR description.

### 2. Read the PR template
Read `claude/templates.md` — the required PR/MR format for this project.

### 3. Gather the diff
```bash
git --no-pager diff main...HEAD --stat | head -50
git --no-pager log main...HEAD --oneline | head -20
```

### 4. Read the linked ticket (if any)
If a ticket number is referenced, extract the requirements from it.

### 5. Generate the PR description

Use the template from `claude/templates.md`. If no template exists, use this default:

```markdown
## What
<One paragraph: what does this change do and why?>

## Why
<One paragraph: what problem does this solve? Link to ticket.>

## How
<Bullet list: key implementation decisions and approach>

## Testing
<What was tested? How? Test commands run + results>

## Checklist
- [ ] Tests pass
- [ ] No new warnings
- [ ] Documentation updated (if applicable)
- [ ] Breaking changes documented (if applicable)
```

### 6. Present to user
Show the PR description and proposed `git push` command. Wait for confirmation before pushing.

## Rules
- NEVER generate a PR description before review passes
- NEVER include implementation details that would confuse reviewers
- NEVER push without explicit user confirmation
