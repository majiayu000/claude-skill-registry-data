---
name: issue-management
description: Work with GitHub issues - create, list, update, comment, and search issues using gh CLI
---
# GitHub Issue Management Skill

This skill provides comprehensive issue management operations including creating, listing, updating, and commenting on GitHub issues.

## Available Operations

### 1. Create Issue
Create a new issue in a repository with title, body, labels, and assignees.

### 2. List Issues
List issues with various filters (state, labels, assignee, etc.).

### 3. Get Issue
Retrieve details of a specific issue.

### 4. Update Issue
Update issue properties like title, body, state, labels, or assignees.

### 5. Add Comment
Add a comment to an existing issue.

### 6. Search Issues
Search for issues across repositories.

## Usage Examples

### Create a New Issue

**Basic issue:**
```bash
gh issue create --repo owner/repo-name --title "Bug: Login not working" --body "Users cannot log in with valid credentials"
```

**Issue with labels:**
```bash
gh issue create --repo owner/repo-name \
  --title "Feature: Add dark mode" \
  --body "Add dark mode support to the application" \
  --label "enhancement" \
  --label "ui"
```

**Issue with assignee:**
```bash
gh issue create --repo owner/repo-name \
  --title "Fix memory leak" \
  --body "Memory usage increases over time" \
  --label "bug" \
  --assignee username
```

**Interactive mode:**
```bash
gh issue create --repo owner/repo-name
# Follow the prompts to enter title and body
```

**From template:**
```bash
gh issue create --repo owner/repo-name --template bug_report.md
```

### List Issues

**List all open issues:**
```bash
gh issue list --repo owner/repo-name
```

**List all issues (including closed):**
```bash
gh issue list --repo owner/repo-name --state all
```

**Filter by label:**
```bash
gh issue list --repo owner/repo-name --label bug
```

**Multiple labels (AND):**
```bash
gh issue list --repo owner/repo-name --label bug --label critical
```

**Filter by assignee:**
```bash
gh issue list --repo owner/repo-name --assignee username
```

**Filter by author:**
```bash
gh issue list --repo owner/repo-name --author username
```

**Limit results:**
```bash
gh issue list --repo owner/repo-name --limit 50
```

**Custom output format:**
```bash
gh issue list --repo owner/repo-name --json number,title,state,labels --jq '.[] | "\(.number): \(.title)"'
```

### Get Issue Details

**View issue in terminal:**
```bash
gh issue view 123 --repo owner/repo-name
```

**View with comments:**
```bash
gh issue view 123 --repo owner/repo-name --comments
```

**View in browser:**
```bash
gh issue view 123 --repo owner/repo-name --web
```

**JSON output:**
```bash
gh issue view 123 --repo owner/repo-name --json number,title,body,state,labels,assignees,createdAt
```

### Update an Issue

**Change issue state to closed:**
```bash
gh issue close 123 --repo owner/repo-name
```

**Close with comment:**
```bash
gh issue close 123 --repo owner/repo-name --comment "Fixed in PR #456"
```

**Reopen issue:**
```bash
gh issue reopen 123 --repo owner/repo-name
```

**Edit issue title and body:**
```bash
gh issue edit 123 --repo owner/repo-name \
  --title "Updated title" \
  --body "Updated description"
```

**Add labels:**
```bash
gh issue edit 123 --repo owner/repo-name --add-label "needs-triage"
```

**Remove labels:**
```bash
gh issue edit 123 --repo owner/repo-name --remove-label "needs-triage"
```

**Add assignees:**
```bash
gh issue edit 123 --repo owner/repo-name --add-assignee user1,user2
```

**Remove assignees:**
```bash
gh issue edit 123 --repo owner/repo-name --remove-assignee user1
```

**Interactive edit:**
```bash
gh issue edit 123 --repo owner/repo-name
```

### Add Comment to Issue

**Add simple comment:**
```bash
gh issue comment 123 --repo owner/repo-name --body "This is my comment"
```

**Add multi-line comment:**
```bash
gh issue comment 123 --repo owner/repo-name --body "First line
Second line
Third line"
```

**Comment from file:**
```bash
gh issue comment 123 --repo owner/repo-name --body-file comment.md
```

**Interactive comment:**
```bash
gh issue comment 123 --repo owner/repo-name
# Opens editor for comment
```

### Search Issues

**Search across all repositories:**
```bash
gh search issues "memory leak" --limit 20
```

**Search in specific repository:**
```bash
gh search issues "bug" --repo owner/repo-name
```

**Search with filters:**
```bash
gh search issues "crash" --label bug --state open --limit 10
```

**Search by author:**
```bash
gh search issues "feature" --author username
```

**Search by date:**
```bash
gh search issues "security" --created ">2025-01-01"
```

**Search in organization:**
```bash
gh search issues "todo" --owner myorg
```

**Complex query:**
```bash
gh search issues "is:open label:bug assignee:username"
```

## Common Patterns

### Triage Workflow

```bash
# List new untriaged issues
gh issue list --repo owner/repo-name --label "needs-triage" --state open

# Review an issue
gh issue view 123 --repo owner/repo-name

# Add labels and assign
gh issue edit 123 --repo owner/repo-name \
  --add-label "bug" \
  --add-label "high-priority" \
  --remove-label "needs-triage" \
  --add-assignee developer1

# Add triage comment
gh issue comment 123 --repo owner/repo-name --body "Confirmed bug. High priority for next sprint."
```

### Bug Report Processing

```bash
# Create bug from template
gh issue create --repo owner/repo-name \
  --title "Bug: API returns 500 error" \
  --body "$(cat bug-details.md)" \
  --label "bug" \
  --label "api"

# Get issue number from output, e.g., #456

# Link to related issue
gh issue comment 456 --repo owner/repo-name --body "Related to #123"

# Update when fixed
gh issue close 456 --repo owner/repo-name --comment "Fixed in commit abc123"
```

### Bulk Operations

**Close multiple stale issues:**
```bash
# List stale issues
gh issue list --repo owner/repo-name --label "stale" --state open --json number --jq '.[].number' > stale_issues.txt

# Close each one
while read issue_num; do
  gh issue close $issue_num --repo owner/repo-name --comment "Closing stale issue"
done < stale_issues.txt
```

**Add label to multiple issues:**
```bash
for issue in 101 102 103 104; do
  gh issue edit $issue --repo owner/repo-name --add-label "sprint-3"
done
```

### Issue Templates

**Create from bug template:**
```bash
gh issue create --repo owner/repo-name --template bug_report.md --web
```

**Create from feature template:**
```bash
gh issue create --repo owner/repo-name --template feature_request.md --web
```

## Error Handling

### Issue Not Found
```bash
# Check if issue exists
gh issue view 123 --repo owner/repo-name 2>&1 | grep -q "could not find" && echo "Issue not found"
```

### Invalid Label
```bash
# List available labels first
gh label list --repo owner/repo-name

# Then create issue with valid label
gh issue create --repo owner/repo-name --title "Test" --body "Test" --label "valid-label"
```

### Permission Denied
```bash
# Check repository access
gh auth status

# Verify you have write access
gh api repos/owner/repo-name --jq '.permissions'
```

## Best Practices

1. **Use descriptive titles**: Make titles clear and searchable
2. **Add relevant labels**: Use labels for categorization and filtering
3. **Assign appropriately**: Only assign when someone is actively working on it
4. **Link related issues**: Reference related issues with #123 syntax
5. **Close with context**: Always add a comment when closing issues
6. **Use templates**: Create issue templates for consistency
7. **Regular triage**: Review and label new issues regularly
8. **Track progress**: Use project boards or milestones to track issue progress

## Issue State Transitions

```
[Open] -> [Closed]                    # gh issue close
[Closed] -> [Open]                    # gh issue reopen
[Open] -> [In Progress]               # Add label/project card
[In Progress] -> [Closed]             # Complete work and close
```

## Integration with Other Skills

- Use `repository-management` to create repos before creating issues
- Use `pull-request-management` to link PRs that fix issues
- Use `search-operations` for advanced cross-repository issue searches
- Use `commit-operations` to reference commits that address issues

## References

- [GitHub CLI Issue Documentation](https://cli.github.com/manual/gh_issue)
- [GitHub Issues Guide](https://docs.github.com/en/issues)
- [Issue Search Syntax](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)
