---
name: implement-ticket
description: Implements a planned GitHub issue by following the implementation plan. Takes a GitHub issue number. Use when the user wants to implement a ticket, work on an issue, or says "implement ticket X" or "do issue #Y".
user-invocable: true
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# Implement Ticket

## Purpose

Execute the implementation plan for a ticket. Follow the plan step by step, then close the ticket when done.

## Prerequisites

The ticket MUST have an implementation plan. If no plan exists, tell the user to run `/plan-ticket` first.

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

If not clear, ask which ticket to implement.

### Step 3: Setup Working Branch

**Ask the user:** "Do you want to use a worktree (allows parallel work on other tickets) or branch in place?"

#### Option A: Worktree (recommended for parallel work)

Use the `/worktree create <branch-name>` skill to create an isolated working directory.

Benefits:
- Can work on multiple tickets simultaneously
- Main repo stays on main/master
- Easy to context-switch between tickets

**Branch name format:** `<issue-number>-<short-description>`
e.g., `12-add-rate-limiting`

#### Option B: Branch in place

Standard approach, switches the current repo to a new branch:

```bash
git checkout main && git pull
git checkout -b <branch-name>
```

Only proceed once in a clean, ticket-specific environment.

### Step 4: Read Ticket and Plan

```bash
gh issue view <number> --comments
```

Extract:
- The original intent (Summary section)
- The implementation plan (Steps)
- The success criteria

If no implementation plan exists, STOP and tell user to run `/plan-ticket` first.

### Step 5: Execute the Plan

Work through each step in the plan:

1. Read the step
2. Implement it
3. Verify it works
4. Move to next step

Use the TodoWrite tool to track progress through the steps.

If you hit a blocker:
- Ask the user how to proceed
- Document the issue
- Don't skip steps without user approval

### Step 6: Verify Success Criteria

Go through each success criterion and verify it's met:
- Run tests if mentioned
- Check behaviour manually if needed
- Confirm each criterion is satisfied

### Step 7: Create PR

Commit and push (already on ticket branch from Step 3):

```bash
git add .
git commit -m "<summary of changes>"
git push -u origin HEAD
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary

<Brief summary of what was done>

Closes #<issue-number>
EOF
)"
```

The `Closes #<number>` will auto-close the issue when PR is merged.

### Step 8: Request Review

Tell the user:
- What was implemented
- Any deviations from the plan
- PR URL

Ask them to review and merge the PR. Wait for their confirmation that it's been merged.

### Step 9: Clean Up (if using worktree)

Once the user says the PR is ready to clean up:

1. **Verify PR is merged**
   ```bash
   gh pr view <pr-number> --json state,mergedAt
   ```

   **STOP if PR is not merged.** Tell the user the PR is still open and ask if they want to wait or cancel cleanup.

2. **Return to main repo**
   ```bash
   cd <main-repo-path>
   git fetch origin
   git checkout main && git pull
   ```

3. **Remove the worktree**
   Use `/worktree clean <branch-name>` to remove the worktree and delete the branch.

4. **Confirm cleanup**
   Report that the worktree has been removed and the ticket workflow is complete.

## Guidelines

**DO**:
- Follow the plan in order
- Verify each step works before moving on
- Ask if something is unclear or blocked
- Run tests frequently
- Commit logical chunks of work

**DON'T**:
- Implement on main/master branch
- Implement on another ticket's branch
- Start work with uncommitted changes
- Skip steps without asking
- Deviate significantly from the plan without discussing
- Leave tests failing
- Create PR if success criteria aren't met

## Handling Issues

**Plan step is unclear:**
Ask the user for clarification before proceeding.

**Step doesn't work as expected:**
Debug and fix if straightforward, otherwise ask user.

**Plan is missing something:**
Point it out, ask if you should add it or proceed without.

**Tests fail:**
Fix them before continuing. If you can't, ask user.

## Checklist

- [ ] Verify GitHub remote exists and on clean, up-to-date main/master
- [ ] Identify which issue to implement
- [ ] Ask user: worktree or branch in place?
- [ ] Setup working environment (worktree or branch)
- [ ] Read issue and extract plan
- [ ] Verify plan exists (if not, stop)
- [ ] Execute each step in order
- [ ] Verify all success criteria
- [ ] Create PR with "Closes #X"
- [ ] Request review from user
- [ ] Wait for user to confirm ready for cleanup
- [ ] Verify PR is merged before cleanup
- [ ] Clean up worktree (if used)
