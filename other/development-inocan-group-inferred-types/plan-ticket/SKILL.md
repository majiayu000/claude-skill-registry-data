---
name: plan-ticket
description: Creates an implementation plan for an existing GitHub issue and adds it as a comment. Takes a GitHub issue number. Use when the user wants to plan a ticket, plan an issue, or says "plan ticket X" or "how should we implement issue #Y".
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob, AskUserQuestion
---

# Plan Ticket

## Purpose

Create a clear implementation plan for an existing ticket. The plan should be detailed enough that success is obvious, but NOT include source code.

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

### Step 2: Identify the Ticket

User will provide a GitHub issue number (e.g., `#12` or `12`).

If not clear, ask which ticket to plan.

### Step 3: Read the Ticket

```bash
gh issue view <number>
```

Understand:
- What needs to be done
- Why it's needed
- Any constraints or notes

### Step 4: Explore the Codebase

Investigate thoroughly to understand:
- Where changes need to happen
- What patterns exist that should be followed
- What dependencies or related code is involved
- Any potential complications

### Step 5: Create the Plan

Write a plan that:
- Lists concrete steps in order
- Names specific files/modules that will be touched
- Describes what each step accomplishes
- Makes success criteria obvious

**Plan format:**

```markdown
## Implementation Plan

### Steps

1. **<Action>** - <What this accomplishes>
   - Files: `path/to/file.py`
   - <Brief description of the change>

2. **<Action>** - <What this accomplishes>
   - Files: `path/to/other.py`
   - <Brief description of the change>

...

### Success Criteria

- [ ] <Observable outcome 1>
- [ ] <Observable outcome 2>
- [ ] <Observable outcome 3>
```

### Step 6: Add Plan to Issue

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Implementation Plan

...plan content...
EOF
)"
```

### Step 7: Report Back

Tell the user the plan has been added and summarise the key steps.

## Plan Writing Guidelines

**DO**:
- Be specific about which files/modules are involved
- Describe what each step achieves
- Make steps atomic and ordered
- Include clear success criteria
- Follow existing patterns in the codebase

**DON'T**:
- Include source code or code snippets
- Over-detail obvious steps
- Include time estimates
- Make it longer than necessary

## Example Plan

```markdown
## Implementation Plan

### Steps

1. **Add rate limiter middleware** - Provides reusable rate limiting logic
   - Files: `src/middleware/rate_limit.py`
   - Create middleware using existing Redis connection
   - Follow pattern from `src/middleware/auth.py`

2. **Configure limits per endpoint** - Allows different limits for different routes
   - Files: `src/config/rate_limits.py`
   - Define default and per-route limits

3. **Apply middleware to API router** - Activates rate limiting
   - Files: `src/api/routes.py`
   - Add middleware to FastAPI app

4. **Add tests** - Verifies rate limiting works correctly
   - Files: `tests/test_rate_limit.py`
   - Test limit enforcement and reset behaviour

### Success Criteria

- [ ] Requests beyond limit return 429 status
- [ ] Limits reset after configured window
- [ ] Different endpoints can have different limits
- [ ] Tests pass
```

## Checklist

- [ ] Verify GitHub remote exists and on clean, up-to-date main/master
- [ ] Identify which issue to plan
- [ ] Read and understand the issue
- [ ] Explore codebase for relevant context
- [ ] Write implementation steps
- [ ] Define success criteria
- [ ] Add plan as comment on issue
- [ ] Report back to user
