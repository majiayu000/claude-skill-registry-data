---
name: pull-request-management
description: GitHub PR operations - create, list, merge, update, and manage pull requests using gh CLI
---
# GitHub Pull Request Management Skill

This skill provides comprehensive pull request (PR) management operations including creating, listing, reviewing, merging, and managing PR status.

## Available Operations

### 1. Create Pull Request
Create a new pull request from one branch to another.

### 2. List Pull Requests
List PRs with filters (state, base branch, head branch, etc.).

### 3. Get Pull Request Details
Retrieve detailed information about a specific PR.

### 4. Get Pull Request Files
View the list of files changed in a PR.

### 5. Get Pull Request Status
Check the status of CI/CD checks and reviews.

### 6. Get Pull Request Comments
View review comments on a PR.

### 7. Get Pull Request Reviews
View all reviews submitted on a PR.

### 8. Update Pull Request Branch
Update PR branch with latest changes from base branch.

### 9. Merge Pull Request
Merge a pull request using different merge strategies.

## Usage Examples

### Create a Pull Request

**Basic PR:**
```bash
gh pr create --repo owner/repo-name \
  --base main \
  --head feature-branch \
  --title "Add new feature" \
  --body "This PR adds a new feature to the application"
```

**PR with labels and reviewers:**
```bash
gh pr create --repo owner/repo-name \
  --base main \
  --head feature-branch \
  --title "Fix critical bug" \
  --body "Fixes issue #123" \
  --label "bug" \
  --label "urgent" \
  --reviewer reviewer1,reviewer2
```

**Draft PR:**
```bash
gh pr create --repo owner/repo-name \
  --base main \
  --head feature-branch \
  --title "WIP: New feature" \
  --body "Work in progress" \
  --draft
```

**Interactive PR creation:**
```bash
gh pr create --repo owner/repo-name
# Follow prompts for base, title, and body
```

**PR from current branch:**
```bash
cd repo-name
git checkout feature-branch
gh pr create --title "My feature" --body "Description"
```

**PR with template:**
```bash
gh pr create --repo owner/repo-name --template pull_request_template.md
```

### List Pull Requests

**List all open PRs:**
```bash
gh pr list --repo owner/repo-name
```

**List all PRs (including closed):**
```bash
gh pr list --repo owner/repo-name --state all
```

**List closed/merged PRs:**
```bash
gh pr list --repo owner/repo-name --state closed
gh pr list --repo owner/repo-name --state merged
```

**Filter by base branch:**
```bash
gh pr list --repo owner/repo-name --base main
```

**Filter by head branch:**
```bash
gh pr list --repo owner/repo-name --head feature-branch
```

**Filter by label:**
```bash
gh pr list --repo owner/repo-name --label "needs-review"
```

**Filter by author:**
```bash
gh pr list --repo owner/repo-name --author username
```

**Filter by assignee:**
```bash
gh pr list --repo owner/repo-name --assignee username
```

**Limit results:**
```bash
gh pr list --repo owner/repo-name --limit 50
```

**Custom JSON output:**
```bash
gh pr list --repo owner/repo-name --json number,title,state,headRefName --jq '.[] | "\(.number): \(.title) (\(.headRefName))"'
```

### Get Pull Request Details

**View PR in terminal:**
```bash
gh pr view 123 --repo owner/repo-name
```

**View with comments:**
```bash
gh pr view 123 --repo owner/repo-name --comments
```

**View in browser:**
```bash
gh pr view 123 --repo owner/repo-name --web
```

**JSON output:**
```bash
gh pr view 123 --repo owner/repo-name --json number,title,body,state,isDraft,mergeable,reviews,statusCheckRollup
```

**Get PR by branch:**
```bash
gh pr view feature-branch --repo owner/repo-name
```

### Get Pull Request Files

**List changed files:**
```bash
gh pr diff 123 --repo owner/repo-name --name-only
```

**View full diff:**
```bash
gh pr diff 123 --repo owner/repo-name
```

**View diff for specific file:**
```bash
gh pr diff 123 --repo owner/repo-name -- path/to/file.js
```

**Get file list with stats:**
```bash
gh api repos/owner/repo-name/pulls/123/files --jq '.[] | "\(.filename): +\(.additions) -\(.deletions)"'
```

### Get Pull Request Status

**Check overall status:**
```bash
gh pr view 123 --repo owner/repo-name --json statusCheckRollup
```

**Check if checks passed:**
```bash
gh pr checks 123 --repo owner/repo-name
```

**Watch checks in real-time:**
```bash
gh pr checks 123 --repo owner/repo-name --watch
```

**Check specific workflow:**
```bash
gh pr checks 123 --repo owner/repo-name --json | jq '.[] | select(.name=="CI")'
```

### Get Pull Request Comments

**View comments:**
```bash
gh pr view 123 --repo owner/repo-name --comments
```

**Get review comments as JSON:**
```bash
gh api repos/owner/repo-name/pulls/123/comments --jq '.[] | {author: .user.login, body: .body, path: .path}'
```

**List all conversation threads:**
```bash
gh pr view 123 --repo owner/repo-name --json comments --jq '.comments[] | "\(.author.login): \(.body)"'
```

### Get Pull Request Reviews

**View all reviews:**
```bash
gh pr view 123 --repo owner/repo-name --json reviews
```

**Check review status:**
```bash
gh pr view 123 --repo owner/repo-name --json reviewDecision
# Returns: APPROVED, CHANGES_REQUESTED, or REVIEW_REQUIRED
```

**List reviewers:**
```bash
gh pr view 123 --repo owner/repo-name --json reviews --jq '.reviews[] | {reviewer: .author.login, state: .state}'
```

### Update Pull Request Branch

**Update with base branch:**
```bash
gh pr checkout 123 --repo owner/repo-name
git pull origin main
git push
```

**Rebase on base branch:**
```bash
gh pr checkout 123 --repo owner/repo-name
git fetch origin
git rebase origin/main
git push --force-with-lease
```

**Merge base into PR branch:**
```bash
gh pr checkout 123 --repo owner/repo-name
git merge origin/main
git push
```

**Using GitHub API to update:**
```bash
gh api repos/owner/repo-name/pulls/123/update-branch -X PUT
```

### Merge Pull Request

**Merge with merge commit:**
```bash
gh pr merge 123 --repo owner/repo-name --merge
```

**Squash and merge:**
```bash
gh pr merge 123 --repo owner/repo-name --squash
```

**Rebase and merge:**
```bash
gh pr merge 123 --repo owner/repo-name --rebase
```

**Auto-merge when checks pass:**
```bash
gh pr merge 123 --repo owner/repo-name --auto --squash
```

**Merge with custom commit message:**
```bash
gh pr merge 123 --repo owner/repo-name --squash --subject "feat: add new feature" --body "Detailed description"
```

**Delete branch after merge:**
```bash
gh pr merge 123 --repo owner/repo-name --squash --delete-branch
```

**Merge and close issues:**
```bash
gh pr merge 123 --repo owner/repo-name --squash --body "Fixes #456, closes #457"
```

## Common Patterns

### Complete PR Workflow

```bash
# 1. Create feature branch
cd repo-name
git checkout -b feature/new-feature
git commit -m "Add feature"
git push -u origin feature/new-feature

# 2. Create PR
gh pr create --title "Add new feature" --body "Implements feature X"

# 3. Check status
gh pr checks --watch

# 4. Request reviews
gh pr edit --add-reviewer team1,user1

# 5. Respond to feedback
git commit -m "Address review comments"
git push

# 6. Merge when ready
gh pr merge --squash --delete-branch
```

### Review and Approval Workflow

```bash
# 1. List PRs needing review
gh pr list --label "needs-review" --repo owner/repo-name

# 2. View PR details
gh pr view 123 --comments

# 3. Check out PR locally
gh pr checkout 123

# 4. Test changes
npm test

# 5. Add review (see code-review skill)
gh pr review 123 --approve --body "LGTM!"

# 6. Merge if approved
gh pr merge 123 --squash
```

### Handle Merge Conflicts

```bash
# 1. Check if PR has conflicts
gh pr view 123 --json mergeable

# 2. Check out PR
gh pr checkout 123

# 3. Update with base branch
git fetch origin
git merge origin/main

# 4. Resolve conflicts
# (manually edit files)

# 5. Complete merge
git add .
git commit -m "Resolve merge conflicts"
git push
```

### Draft PR Workflow

```bash
# 1. Create draft PR
gh pr create --draft --title "WIP: Feature X"

# 2. Continue working
git commit -m "Progress on feature"
git push

# 3. Mark as ready when done
gh pr ready 123

# 4. Request reviews
gh pr edit 123 --add-reviewer team1
```

### Auto-merge Setup

```bash
# Enable auto-merge when checks pass
gh pr merge 123 --auto --squash

# Cancel auto-merge
gh pr merge 123 --auto=false
```

## Error Handling

### PR Already Exists
```bash
# Check for existing PR from branch
gh pr list --head feature-branch --repo owner/repo-name
```

### Merge Conflicts
```bash
# Check if PR is mergeable
gh pr view 123 --json mergeable --jq '.mergeable'

# If not mergeable, update branch
gh pr checkout 123
git merge origin/main
# Resolve conflicts, commit, push
```

### Failed Checks
```bash
# View failed checks
gh pr checks 123 --repo owner/repo-name

# View workflow runs
gh run list --branch feature-branch

# Rerun failed checks
gh run rerun <run-id>
```

### Insufficient Permissions
```bash
# Check permissions
gh api repos/owner/repo-name --jq '.permissions'

# Ensure you're authenticated
gh auth status
```

## Best Practices

1. **Write clear PR descriptions**: Explain what, why, and how
2. **Reference issues**: Use "Fixes #123" to auto-close issues
3. **Keep PRs focused**: One feature/fix per PR
4. **Request specific reviewers**: Tag relevant domain experts
5. **Respond to feedback**: Address all review comments
6. **Keep branch updated**: Regularly merge/rebase with base branch
7. **Use draft PRs**: For work-in-progress changes
8. **Clean up branches**: Delete branches after merging
9. **Use templates**: Create PR templates for consistency
10. **Squash commits**: Use squash merge for cleaner history

## PR States and Transitions

```
[Draft] -> [Ready for Review]         # gh pr ready
[Open] -> [Merged]                    # gh pr merge
[Open] -> [Closed]                    # gh pr close
[Closed] -> [Open]                    # gh pr reopen
[Open] -> [Auto-merge Enabled]        # gh pr merge --auto
```

## Integration with Other Skills

- Use `issue-management` to link PRs to issues
- Use `code-review` to add reviews and comments
- Use `commit-operations` to view commit history
- Use `repository-management` to manage branches

## References

- [GitHub CLI PR Documentation](https://cli.github.com/manual/gh_pr)
- [GitHub Pull Requests Guide](https://docs.github.com/en/pull-requests)
- [GitHub Merge Methods](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges)
