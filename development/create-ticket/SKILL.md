---
name: create-ticket
description: Creates GitHub issues to capture work that needs to be done. Records intent with context about the codebase, not implementation plans. Use when the user wants to track work, create a ticket, log a task, or says "we want to do X" or "we need to X".
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# Create Ticket

## Purpose

Capture intent for future work. This is NOT about planning implementation - it's about recording WHAT needs doing and WHY, with enough context to understand the task later.

## Workflow

### Step 1: Verify Environment

Check we have a GitHub remote and are on a clean, up-to-date main/master:

```bash
git remote -v
git status
git fetch origin
git rev-parse --abbrev-ref HEAD
git status -uno
```

**STOP if:**
- No remote exists → "This skill requires a GitHub remote. Please add one with `git remote add origin <url>` first."
- Not on main/master → "Please switch to main/master first: `git checkout main`"
- Uncommitted changes → "Please commit or stash your changes first."
- Behind remote → "Please pull latest changes: `git pull`"

### Step 2: Understand the Request

Listen to what the user wants to do. Ask clarifying questions if needed:
- What's the goal?
- Why is this needed?
- Any constraints or requirements?

Keep questions minimal - don't over-engineer the discovery.

### Step 3: Assess Scope

Decide if this is:
- **Single task** - one coherent piece of work
- **Multiple tasks** - should be split into separate issues

If splitting, create separate issues for each logical unit of work.

### Step 4: Gather Context

Briefly explore the codebase to understand:
- What currently exists that's relevant
- Where the change would likely happen
- Any related code or patterns

This context goes INTO the issue - you're not planning, just documenting what exists.

### Step 5: Create GitHub Issue

```bash
gh issue create --title "<title>" --body "$(cat <<'EOF'
## Summary

<One paragraph describing what needs to be done and why>

## Context

<What currently exists that's relevant - files, patterns, related code>

## Notes

<Any constraints, requirements, or considerations>
EOF
)"
```

### Step 6: Report Back

Tell the user:
- What issue(s) were created
- GitHub issue URL(s)
- Brief summary of what was captured

## Ticket Writing Guidelines

**DO**:
- Describe the intent clearly
- Include relevant context about existing code
- Note any constraints mentioned by user
- Keep it concise but complete

**DON'T**:
- Write implementation plans
- Include step-by-step instructions
- Estimate time or effort
- Make architectural decisions

## Example Ticket

```markdown
# Add rate limiting to API endpoints

## Summary

API endpoints currently have no rate limiting, making them vulnerable to abuse. Need to add rate limiting to protect the service.

## Context

- API routes defined in `src/api/routes.py`
- Currently using FastAPI with no middleware for rate limiting
- Redis is already available in the stack (`src/services/redis.py`)

## Notes

- User mentioned starting with a simple per-IP limit
- Should be configurable per-endpoint
```

## Checklist

- [ ] Verify GitHub remote exists and on clean, up-to-date main/master
- [ ] Understand what user wants to do
- [ ] Ask clarifying questions if needed
- [ ] Assess if single or multiple issues
- [ ] Explore codebase for relevant context
- [ ] Create GitHub issue(s)
- [ ] Report back with issue URL(s)
