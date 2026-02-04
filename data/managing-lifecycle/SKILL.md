---
name: managing-lifecycle
description: GitHub Issue CRUD and state management. TRIGGERS - create issue, close issue, update issue, bulk process issues.
---

# Issue Lifecycle Operations

**Capability:** Complete CRUD operations for GitHub Issues and PRs

**When to use:** Creating, reading, updating, deleting, commenting on issues/PRs

---

## Create Operations

### Create Issue

```bash
# Basic creation
gh issue create --title "Bug: Login fails" --body "Steps to reproduce..."

# With labels and assignee
gh issue create \
  --title "Feature: Add dark mode" \
  --body "User requested dark mode support" \
  --label feature,ui \
  --assignee username

# From file
gh issue create --title "API Documentation" --body-file doc.md

# Interactive mode
gh issue create
```

### Create with Template

```bash
# Knowledge base entry
gh issue create \
  --repo terrylica/claude-code-skills-github-issues \
  --title "Claude Code: Using Plan Mode" \
  --label claude-code,tips,how-to \
  --body-file tip.md
```

---

## Read Operations

### View Issue

```bash
# Web view
gh issue view 123 --web

# Terminal view
gh issue view 123

# JSON output (21 fields available)
gh issue view 123 --json title,body,state,labels,assignees,createdAt
```

### List Issues

```bash
# List open issues
gh issue list

# Filter by assignee
gh issue list --assignee @me

# Filter by label
gh issue list --label bug --state open

# Limit results
gh issue list --limit 50
```

---

## Update Operations

### Modify Issue

```bash
# Update title
gh issue edit 123 --title "New title"

# Update body
gh issue edit 123 --body "Updated description"

# Add labels
gh issue edit 123 --add-label priority:high,bug

# Remove labels
gh issue edit 123 --remove-label wontfix

# Change assignee
gh issue edit 123 --add-assignee username
```

### State Management

```bash
# Close issue
gh issue close 123

# Close with comment
gh issue close 123 --comment "Fixed in commit abc123"

# Reopen issue
gh issue reopen 123

# Mark as resolved
gh issue close 123 --reason completed

# Mark as won't fix
gh issue close 123 --reason "not planned"
```

---

## Comment Operations

```bash
# Add comment
gh issue comment 123 --body "Thanks for reporting this!"

# Comment from file
gh issue comment 123 --body-file response.md

# Edit comment (requires comment ID)
gh api repos/owner/repo/issues/comments/COMMENT_ID \
  --method PATCH \
  --field body="Updated comment"
```

---

## Delete Operations

```bash
# Delete issue (careful - permanent!)
gh issue delete 123

# Delete with confirmation skip
gh issue delete 123 --yes

# Note: Prefer closing over deleting for audit trail
```

---

## Batch Operations

### Close Multiple Issues

```bash
# Close all issues with specific label
gh issue list --label wontfix --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --reason "not planned"

# Close old issues
gh search issues "is:open created:<2024-01-01" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {}
```

### Bulk Label Updates

```bash
# Add label to multiple issues
for issue in 101 102 103; do
  gh issue edit $issue --add-label priority:high
done
```

---

## Common Workflows

### Knowledge Base Entry Workflow

```bash
# 1. Create issue with content
gh issue create --title "Tip: Git worktrees" --body-file tip.md

# 2. Add labels
gh issue edit 1 --add-label git,tips,how-to

# 3. Verify created
gh issue view 1
```

### Issue Triage Workflow

```bash
# 1. List new issues
gh issue list --label needs-triage

# 2. Review and categorize
gh issue edit 123 --add-label bug --remove-label needs-triage

# 3. Assign if needed
gh issue edit 123 --add-assignee dev-team
```

---

## JSON Output Fields (21 available)

**Core:** number, title, body, state, url
**Metadata:** labels, assignees, milestone, projectCards
**Timestamps:** createdAt, updatedAt, closedAt
**Engagement:** comments, reactions
**Users:** author, participants
**Full list:** `gh issue view --help`

---

## Best Practices

1. **Prefer closing over deleting** - Maintains audit trail
2. **Use labels for organization** - Better than comments
3. **Atomic updates** - One change per command for clarity
4. **JSON for automation** - Script with `--json` and `--jq`
5. **Batch carefully** - Test on single issue first

---

**Empirical Testing:** 200+ test cases covering all CRUD operations

**Full Operational Guide:** [AI_AGENT_OPERATIONAL_GUIDE.md](/docs/guides/AI_AGENT_OPERATIONAL_GUIDE.md)
