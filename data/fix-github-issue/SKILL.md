---
name: fix-github-issue
description: Load a GitHub issue, create an isolated worktree, plan the implementation, and submit a PR. Use when asked to fix, implement, or work on a GitHub issue by number. Requires the gh CLI to be authenticated.
triggers:
  - "fix issue #"
  - "implement issue"
  - "work on issue"
  - "resolve issue"
prerequisites:
  - gh (GitHub CLI, authenticated)
  - git
arguments:
  - name: ISSUE_NUMBER
    required: true
    description: The GitHub issue number to work on
---

# Fix GitHub Issue

Plan, implement, and submit a PR for a GitHub issue using git worktrees for isolation.

**Codex note:** This skill references Claude Code subagents (`Task(...)`). In Codex, run the equivalent steps with tool calls (for example `functions.shell_command` and `multi_tool_use.parallel`) or run them sequentially. See [`../../COMPATIBILITY.md`](../../COMPATIBILITY.md).

## Phase 1: Plan

### 1. Set up worktree

Before anything else, create an isolated worktree for this issue:

```bash
scripts/setup-worktree.sh $ISSUE_NUMBER
```

This will:
- Validate prerequisites (gh auth, git repo, origin remote)
- Checkout main and pull latest changes
- Create a new worktree at `.worktrees/issue-$ISSUE_NUMBER`
- Create and checkout a branch `issue-$ISSUE_NUMBER`
- Output the path to cd into

All subsequent work happens in the worktree, keeping your main repo clean.

**Options:**
- `--no-worktree`: Work directly on a branch without creating a worktree (useful for simple changes)

**Note:** The script auto-adds `.worktrees/` to `.gitignore`.

**If setup fails:**
- "Not in a git repository": Run from within a git repo
- "gh not authenticated": Run `gh auth login`
- "No origin remote": Add one with `git remote add origin <url>`
- "Uncommitted changes": Commit or stash your changes first
- "Could not fast-forward": Your local main has diverged; resolve manually

### 2. Load issue context

```bash
scripts/load-issue.sh $ISSUE_NUMBER
```

Fetches issue details, comments, labels, and related PRs.

From the output, identify:
- Main objective from the issue description
- Clarifications, constraints, or scope changes from comments
- Proposed solutions or implementation hints from the author or maintainers
- Any blockers, dependencies, or related issues mentioned

### 3. Explore the codebase

Locate affected files and review current implementation. Identify integration points, dependencies, and side effects.

### 4. Create plan

Analyse the issue and produce a plan using [templates/plan.md](templates/plan.md):

- Summary, root cause analysis, implementation steps
- Testing approach, risks, complexity assessment

**Example plan output:**

```markdown
# Plan: Fix null pointer in user service

**Issue:** #123 - https://github.com/org/repo/issues/123

## Summary
User service crashes when processing requests with missing optional fields.

## Analysis
The `processUser` function at `src/services/user.ts:45` accesses `user.profile.name`
without checking if `profile` exists. This was introduced in commit abc123.

## Implementation Plan
1. Add null check for `user.profile` in `processUser`
2. Add fallback default values for optional fields
3. Add unit test for the null case

## Testing/Validation
- [ ] Unit test: processUser with null profile
- [ ] Unit test: processUser with partial profile
- [ ] Integration test: API endpoint with minimal payload

## Risks/Edge Cases
- Other callers may rely on the exception being thrown
- Profile field is used in 3 other places (checked: all safe)

## Complexity
**Low** - Single file change with clear fix
```

### 5. Handling complex issues

**Issues with dependencies:**
- Check if blocking issues are resolved
- Note dependencies in your plan
- Consider implementing in phases

**Issues with multiple related issues:**
- Reference related issues in the plan
- Coordinate if changes overlap
- Consider whether to batch or separate PRs

### 6. Confirm before implementing

Ask: "Would you like me to start working on this now?"

Wait for confirmation.

---

## Phase 2: Implement

Write the code changes as planned. Test locally.

Follow the repository's coding standards and conventions.

---

## Phase 3: Submit

### 1. Commit changes

From the worktree (already on the correct branch):

```bash
git add -A
git commit -m "Brief description

Closes #$ISSUE_NUMBER"
```

### 2. Push and create PR

```bash
git push -u origin HEAD
gh pr create --title "Brief description" --body-file templates/pr-body.md
```

Or use the automated script:

```bash
scripts/create-pr.sh $ISSUE_NUMBER "Brief description"
```

### 3. Verify linking

Confirm the PR shows `Closes #N` and the issue appears in the Development sidebar.

---

## Quick Reference

| Keyword | Effect |
|---------|--------|
| `Closes #N` | Links PR and closes issue on merge |
| `Fixes #N` | Same as Closes |
| `Resolves #N` | Same as Closes |
| `Ref #N` | Links without closing |

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/setup-worktree.sh` | Pulls main, creates worktree and branch |
| `scripts/load-issue.sh` | Fetches issue details, comments, and related PRs |
| `scripts/create-pr.sh` | Commits, pushes, and opens PR |

## Subagent Usage

Use subagents to offload codebase exploration from the main context.

### Phase 1: Explore Agent for Codebase Analysis

After loading issue context, launch an Explore agent to find relevant files without bloating main context:

```
Launch Explore agent:
"Find all files related to issue #{number}: {issue_title}

Issue description:
{issue_body}

Search for:
1. Files explicitly mentioned in the issue
2. Files matching keywords from the issue title and body
3. Similar existing implementations (if this is a new feature)
4. Test files that cover the affected areas
5. Configuration files that might need updates
6. Related type definitions or interfaces

For each relevant file found:
- Explain why it's relevant
- Note the key functions/classes to modify
- Identify integration points with other code

Return:
- List of affected files with explanations
- Existing patterns to follow
- Test files to update or add
- Potential side effects to consider"
```

**Benefits:**
- Codebase exploration stays out of main context
- Agent can do thorough search without token pressure
- Main context receives concise summary of findings

### Phase 1: Plan Agent for Implementation Design

After exploration, optionally launch a Plan agent for complex issues:

```
Launch Plan agent:
"Design implementation for issue #{number}: {issue_title}

Context from exploration:
{exploration_results}

Issue requirements:
{issue_body}

Create a detailed implementation plan covering:
1. Root cause analysis (for bugs) or feature breakdown (for features)
2. Step-by-step implementation order
3. Testing approach
4. Risks and edge cases
5. Complexity assessment"
```

**When to use Plan agent:**
- Complex issues requiring architectural decisions
- Issues touching > 5 files
- Features with multiple valid approaches

### Phase 3: Background PR Creation (Optional)

For straightforward PRs, create in background while reporting to user:

```
Launch background agent:
"Create PR for issue #{number}.
Branch: {branch_name}
Title: {pr_title}
Body: {pr_body}

Steps:
1. git push -u origin HEAD
2. gh pr create --title '...' --body '...'
3. Return PR URL"
```

User sees immediate confirmation while PR creates in background.

**When to use subagents:**
- Issue mentions multiple files or areas: Use Explore agent
- Complex architectural issue: Use Plan agent
- User wants quick feedback: Use background PR creation

**When to skip subagents:**
- Issue clearly specifies exact file and change needed
- Single-line fix or typo correction
- You already know the codebase well from context

## Related Skills

- [cleanup-issue](../cleanup-issue/SKILL.md): Clean up after PR is merged
- [pr-feedback-workflow](../pr-feedback-workflow/SKILL.md): Address review comments on the PR
