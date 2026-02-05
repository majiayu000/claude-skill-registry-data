---
name: pr-feedback
description: This skill should be used for integrating PR review comments back into devloop plan, parsing review feedback, addressing reviewer concerns
whenToUse: PR has review comments, feedback to address, review iterations, changes requested, responding to reviewers
whenNotToUse: No open PR, PR already merged, creating new PR
seeAlso:
  - skill: git-workflows
    when: git operations and PR strategy
  - skill: plan-management
    when: updating plan with new tasks
---

# PR Feedback Integration

Parse PR review comments and integrate actionable items into the devloop plan.

## When to Use

- PR has review comments or change requests
- Reviewer requested changes
- Need to track which feedback has been addressed
- Iterating on PR after initial review

## Fetching PR Feedback

**Get PR details with comments:**

```bash
# View PR with all comments
gh pr view --json number,title,body,comments,reviews,reviewDecision

# Get review comments (inline code comments)
gh api repos/{owner}/{repo}/pulls/{number}/comments

# Get PR conversation comments
gh api repos/{owner}/{repo}/issues/{number}/comments
```

**Key fields to extract:**

| Field | Purpose |
|-------|---------|
| `reviewDecision` | APPROVED, CHANGES_REQUESTED, REVIEW_REQUIRED |
| `reviews` | List of reviews with state and body |
| `comments` | Conversation comments |

## Parsing Feedback

**Categorize feedback:**

| Type | Description |
|------|-------------|
| **Blocker** | Must fix before merge |
| **Suggestion** | Should consider |
| **Question** | Needs response |
| **Nitpick** | Nice to have |

**Identify actionable items:**

Look for patterns:
- "Please..." / "Could you..." → Action request
- "This should..." / "Consider..." → Suggestion
- "Why..." / "What if..." → Question
- "Nit:" / "Minor:" → Low priority

## Adding to Plan

**Create PR Feedback section in plan:**

```markdown
## PR Feedback

PR #123 - Review by @reviewer (CHANGES_REQUESTED)

### Blockers
- [ ] [PR-123-1] Fix null handling in parseConfig (@reviewer)
- [ ] [PR-123-2] Add tests for edge cases (@reviewer)

### Suggestions
- [ ] [PR-123-3] Consider caching config (@reviewer)

### Questions
- [ ] [PR-123-4] Respond: Why not use existing parser? (@reviewer)
```

**Task ID format:** `[PR-{number}-{item}]`

## Tracking Resolution

When addressing feedback:

1. Make the fix
2. Mark task complete in plan
3. Reply to the comment on GitHub
4. Push changes

**Reply template:**

```bash
gh pr comment {number} --body "Addressed in commit {sha}:
- Fixed null handling
- Added edge case tests"
```

## Example Workflow

```bash
# 1. Check PR status
gh pr view --json reviewDecision,reviews

# 2. If changes requested, get details
gh pr view --comments

# 3. Parse into plan tasks (manual or use /devloop:pr-feedback)

# 4. Work through feedback tasks

# 5. Push and reply
git push
gh pr comment --body "Ready for re-review"
```

## Integration with /devloop:pr-feedback

The `/devloop:pr-feedback` command automates:

1. Fetching current PR comments
2. Parsing actionable items
3. Presenting to user for selection
4. Adding selected items to plan
5. Updating Progress Log

## Best Practices

- Address blockers first
- Reply to each comment when resolved
- Push frequently during feedback iteration
- Re-request review when ready
