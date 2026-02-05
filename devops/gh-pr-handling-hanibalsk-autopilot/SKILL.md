---
name: gh-pr-handling
description: Expert GitHub CLI and PR handling. Use when working with pull requests, GitHub issues, reviews, CI checks, or any gh command operations.
allowed-tools: Bash, Read
---

# GitHub CLI & Pull Request Handling

Expert guidance for GitHub CLI (`gh`) operations and pull request management.

## When to Use

Activate this skill when the user:
- Works with pull requests (create, review, merge, close)
- Checks CI/CD status or workflow runs
- Manages GitHub issues
- Needs to interact with GitHub API via `gh`
- Handles Copilot reviews or PR comments

## Essential Commands

### PR Creation

```bash
# Create PR with proper formatting (use HEREDOC for body)
gh pr create --title "feat: add feature X" --body "$(cat <<'EOF'
## Summary
- Brief description of changes

## Test plan
- [ ] Unit tests pass
- [ ] Manual testing completed
EOF
)"

# Create draft PR
gh pr create --draft --title "WIP: feature X"

# Create PR with labels
gh pr create --title "fix: bug" --label "bug,priority:high"
```

### PR Status & Info

```bash
# View current PR
gh pr view

# Get PR number
gh pr view --json number -q '.number'

# Get PR state (OPEN, MERGED, CLOSED)
gh pr view --json state -q '.state'

# List open PRs
gh pr list --state open

# List PRs for specific branch pattern
gh pr list --state open --json headRefName,number \
  -q '.[] | select(.headRefName | test("^feature/")) | "\(.number):\(.headRefName)"'
```

### CI Checks

```bash
# View all checks
gh pr checks

# Get check conclusions
gh pr checks --json conclusion -q '.[].conclusion'

# Get failed checks with details
gh pr checks --json name,conclusion,detailsUrl \
  -q '.[] | select(.conclusion == "FAILURE")'

# Wait for checks to complete
gh pr checks --watch
```

### Reviews & Comments

```bash
# Get all reviews
gh pr view --json reviews -q '.reviews'

# Get Copilot review state
gh pr view --json reviews -q '
  [.reviews[] | select(.author.login | test("copilot"; "i"))]
  | sort_by(.submittedAt) | .[-1].state // ""
'

# Get latest Copilot comment
gh pr view --json comments,reviews -q '
  (
    [.comments[] | select(.author.login | test("copilot"; "i"))] +
    [.reviews[] | select(.author.login | test("copilot"; "i"))]
  ) | sort_by(.createdAt) | .[-1]
'

# Add comment to PR
gh pr comment --body "Comment text here"

# Request review
gh pr edit --add-reviewer username
```

### Merging

```bash
# Squash merge and delete branch
gh pr merge --squash --delete-branch

# Merge with auto-merge when checks pass
gh pr merge --auto --squash

# Rebase merge
gh pr merge --rebase --delete-branch
```

### Branch Protection Awareness

When branch protection requires:
- **Copilot review**: Wait for `copilot[bot]` APPROVED state
- **CI checks**: All checks must pass (no FAILURE conclusions)
- **Approvals**: Required number of approving reviews

```bash
# Check if PR is mergeable
gh pr view --json mergeable -q '.mergeable'

# Get merge state status
gh pr view --json mergeStateStatus -q '.mergeStateStatus'
```

## Common Patterns

### Check PR exists for current branch
```bash
if gh pr view >/dev/null 2>&1; then
  echo "PR exists"
else
  echo "No PR for this branch"
fi
```

### Get PR info safely
```bash
pr_info="$(gh pr view --json number,state 2>/dev/null || echo "")"
if [ -n "$pr_info" ]; then
  pr_number="$(echo "$pr_info" | jq -r '.number')"
  pr_state="$(echo "$pr_info" | jq -r '.state')"
fi
```

### Poll for CI completion
```bash
for i in $(seq 1 60); do
  conclusions="$(gh pr checks --json conclusion -q '.[].conclusion')"
  if echo "$conclusions" | grep -iq "failure"; then
    echo "CI failed"
    break
  fi
  if ! echo "$conclusions" | grep -iq "pending"; then
    echo "CI passed"
    break
  fi
  sleep 30
done
```

## Review Thread Management

### Get unresolved review threads (GraphQL)
```bash
gh api graphql -f query='
  query($owner: String!, $repo: String!, $pr: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        reviewThreads(first: 100) {
          nodes {
            id
            isResolved
            comments(first: 1) {
              nodes { body author { login } }
            }
          }
        }
      }
    }
  }
' -F owner="OWNER" -F repo="REPO" -F pr=123
```

### Resolve a review thread
```bash
gh api graphql -f query='
  mutation($threadId: ID!) {
    resolveReviewThread(input: {threadId: $threadId}) {
      thread { isResolved }
    }
  }
' -F threadId="THREAD_NODE_ID"
```

### Reply to a review comment
```bash
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body="Fixed in latest commit"
```

## Auto-Approve Workflow

The `auto-approve.yml` GitHub workflow automates PR approval with strict conditions.

**Approval conditions (ALL must be met):**
1. At least 10 minutes since last push
2. Copilot review exists
3. All review threads resolved
4. All review comments answered
5. All CI checks passed

**Flow:**
1. Copilot submits review → triggers workflow
2. Waits 2 min for CI to start
3. Polls CI every 30s (max 30 min), fails fast on failure
4. Checks 10 min elapsed since last push
5. Checks Copilot has reviewed
6. Checks 0 unresolved threads via GraphQL
7. **Dismisses stale approvals** if unresolved threads exist
8. Auto-approves only if ALL conditions met

**Manual trigger (fallback):**
```bash
gh workflow run auto-approve.yml -f pr_number=123
```

**Check workflow status:**
```bash
# List recent runs
gh run list --workflow=auto-approve.yml

# Watch current run
gh run watch

# View run details
gh run view <run-id>
```

**Why auto-approve exists:**
- Branch protection requires approval before merge
- Copilot review alone doesn't count as approval
- This workflow bridges the gap: Copilot reviews → workflow approves → merge allowed

**Critical: Fix issues before approval:**
- Unresolved threads block approval
- Stale approvals are dismissed if threads exist
- Must reply to comments AND resolve threads
- 10 min wait ensures Copilot has time to re-review after fixes

**When autopilot should NOT wait:**
- After creating PR, auto-approve workflow handles approval
- Autopilot can continue to next epic immediately
- Only need to wait/fix if unresolved threads exist

## Best Practices

1. **Always use `--json` for scripting** - Parse structured output with `jq`
2. **Handle empty responses** - Commands may return empty when no PR exists
3. **Use HEREDOC for multi-line body** - Preserves formatting in PR descriptions
4. **Check PR state before operations** - Verify OPEN before trying to merge
5. **Respect rate limits** - Add sleep between repeated API calls
6. **Resolve threads after fixing** - Use GraphQL mutation to mark threads resolved
7. **Trust auto-approve workflow** - Don't manually poll for approval, let workflow handle it
