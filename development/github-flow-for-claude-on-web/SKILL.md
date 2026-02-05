---
name: github-flow-for-claude-on-web
description: Complete GitHub workflow for Claude Code on the web. ALL GitHub operations MUST use REST API (never gh CLI). Includes branch naming (claude/*-sessionId), push retry logic, PR/issue management via API, and complete workflows. Use for all GitHub interactions in Claude Code web environment.
allowed-tools: Bash, Read, Grep
---

# GitHub Flow for Claude Code on the Web

This skill provides comprehensive Git and GitHub operations optimized for Claude Code on the web environment, including branch management, push operations, and GitHub REST API interactions.

## ⚠️ CRITICAL: Always Use GitHub REST API

**NEVER use `gh` CLI in Claude Code on the web - it is not available.**

All GitHub operations (PRs, issues, comments, reviews) MUST use the REST API via `curl`:

- ✅ `curl -s https://api.github.com/repos/OWNER/REPO/pulls/123`
- ❌ `gh pr view 123` (NOT AVAILABLE)

## When to Use

This skill is automatically activated when running in Claude Code on the web environment (`CLAUDE_CODE_REMOTE=true`).

## Table of Contents

1. [GitHub API Operations](#github-api-operations)
2. [Environment Detection](#environment-detection)
3. [Branch Naming Requirements](#branch-naming-requirements)
4. [Git Push Operations](#git-push-operations)
5. [Pull Request Creation](#pull-request-creation)
6. [Complete Workflows](#complete-workflows)
7. [Troubleshooting](#troubleshooting)

---

## GitHub API Operations

### Core Principle

**ALL GitHub operations must use the REST API.** The `gh` CLI is not available in Claude Code on the web environment.

### Common GitHub API Endpoints

#### Get PR Details

```bash
curl -s https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER
```

#### Get PR Review Comments

```bash
# Code review comments
curl -s https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/comments

# Issue comments (general discussion)
curl -s https://api.github.com/repos/OWNER/REPO/issues/PR_NUMBER/comments
```

#### Get Repository Info

```bash
# Auto-detect from git remote
REMOTE_URL=$(git remote get-url origin)
REPO_FULL=$(echo "$REMOTE_URL" | sed -E 's#.*github\.com[:/]([^/]+/[^/]+)(\.git)?$#\1#')
OWNER=$(echo "$REPO_FULL" | cut -d/ -f1)
REPO=$(echo "$REPO_FULL" | cut -d/ -f2)

curl -s "https://api.github.com/repos/$OWNER/$REPO"
```

#### List Issues

```bash
# All open issues
curl -s https://api.github.com/repos/OWNER/REPO/issues

# Filter by labels
curl -s "https://api.github.com/repos/OWNER/REPO/issues?labels=bug"
```

#### Get Issue Comments

```bash
curl -s https://api.github.com/repos/OWNER/REPO/issues/ISSUE_NUMBER/comments
```

### Authentication

```bash
# Unauthenticated (rate limit: 60 requests/hour)
curl -s https://api.github.com/repos/OWNER/REPO/pulls/123

# Authenticated with token (rate limit: 5000 requests/hour)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/pulls/123
```

### Parsing JSON Responses

```bash
# With jq (if available)
curl -s https://api.github.com/repos/OWNER/REPO/pulls/123 | \
  jq '{title, state, author: .user.login}'

# Without jq - use grep
curl -s https://api.github.com/repos/OWNER/REPO/pulls/123 | \
  grep -o '"title": *"[^"]*"' | cut -d'"' -f4
```

---

## Environment Detection

Always check if running in Claude Code on the web before applying special constraints:

```bash
# Check environment
if [ "$CLAUDE_CODE_REMOTE" = "true" ]; then
  echo "Running in Claude Code on the web"
  # Apply remote-specific logic
else
  echo "Running in local environment"
  # Use standard git commands
fi
```

**Key Environment Variables:**

- `CLAUDE_CODE_REMOTE` - Set to `"true"` in web environment
- `CLAUDE_SESSION_ID` - Session identifier (may be available)
- `GITHUB_TOKEN` - GitHub personal access token for API operations

---

## Branch Naming Requirements

### Critical Constraints

When pushing to remote in Claude Code on the web:

- ✅ Branch names **MUST** start with `claude/`
- ✅ Branch names **MUST** end with a matching session ID
- ✅ Pattern: `claude/<feature-name>-<sessionId>`
- ❌ Pushing to non-compliant branches will fail with **HTTP 403**

### Examples

**Valid branch names:**

```text
claude/fix-bug-abc123
claude/add-feature-xyz789
claude/create-pull-request-KITjd
```

**Invalid branch names:**

```text
main                          # ❌ Doesn't start with claude/
feature-branch                # ❌ Doesn't start with claude/
claude/fix-bug                # ❌ Missing session ID
fix-bug-abc123               # ❌ Doesn't start with claude/
```

### Creating Compliant Branches

```bash
#!/bin/bash

# Get session ID (use environment or default)
SESSION_ID="${CLAUDE_SESSION_ID:-9GOGf}"

# Create feature branch with proper naming
FEATURE_NAME="fix-matchglob"
BRANCH="claude/${FEATURE_NAME}-${SESSION_ID}"

# Create and checkout branch
git checkout -b "$BRANCH"

# Or checkout existing branch
git checkout "$BRANCH"
```

### Converting Existing Branches

If you're on a non-compliant branch:

```bash
#!/bin/bash

CURRENT_BRANCH="$(git branch --show-current)"
SESSION_ID="${CLAUDE_SESSION_ID:-9GOGf}"

# Check if branch needs conversion
if [[ ! "$CURRENT_BRANCH" =~ ^claude/.+-[a-zA-Z0-9]+$ ]]; then
  echo "Branch name needs conversion: $CURRENT_BRANCH"

  # Extract feature name
  FEATURE_NAME="${CURRENT_BRANCH//[^a-zA-Z0-9-]/-}"
  NEW_BRANCH="claude/${FEATURE_NAME}-${SESSION_ID}"

  # Create new branch from current position
  git checkout -b "$NEW_BRANCH"

  echo "Created new branch: $NEW_BRANCH"
fi
```

---

## Git Push Operations

### Push with Retry Logic

Claude Code on the web may experience transient network issues. Always use retry logic with exponential backoff:

```bash
#!/bin/bash

# Function: Smart push with retry and validation
smart_push() {
  local branch="${1:-$(git branch --show-current)}"

  # Only apply constraints in remote environment
  if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
    git push -u origin "$branch"
    return $?
  fi

  # Validate branch name
  if [[ ! "$branch" =~ ^claude/.+-[a-zA-Z0-9]+$ ]]; then
    echo "❌ Invalid branch name for Claude Code on the web: $branch"
    echo "   Required pattern: claude/<feature-name>-<sessionId>"
    return 1
  fi

  echo "Pushing branch: $branch"

  # Retry with exponential backoff: 2s, 4s, 8s, 16s
  local max_attempts=4
  for attempt in $(seq 1 $max_attempts); do
    if [ $attempt -gt 1 ]; then
      local delay=$((2 ** (attempt - 1)))
      echo "Retry attempt $attempt/$max_attempts after ${delay}s..."
      sleep $delay
    fi

    # Attempt push (capture output once)
    local output
    output=$(git push -u origin "$branch" 2>&1)
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
      echo "✅ Push successful!"
      return 0
    fi

    # Check for 403 error (branch name issue)
    if echo "$output" | grep -q "403"; then
      echo "❌ HTTP 403 - Branch name validation failed"
      echo "   Ensure branch follows pattern: claude/*-<sessionId>"
      return 1
    fi

    # Show error output for debugging
    echo "$output"
  done

  echo "❌ Push failed after $max_attempts attempts"
  return 1
}

# Usage
smart_push
# Or specify branch
smart_push "claude/my-feature-abc123"
```

### Quick Push Script

For quick use in bash commands:

```bash
# Inline push with retry
BRANCH="$(git branch --show-current)"
for i in 0 1 2 3; do
  if [ $i -gt 0 ]; then
    delay=$((2 ** i))
    echo "Retry $i after ${delay}s..."
    sleep $delay
  fi
  if git push -u origin "$BRANCH" 2>&1; then
    echo "✅ Push successful!"
    exit 0
  fi
done
echo "❌ Push failed after retries"
exit 1
```

### Force Push (Use with Caution)

When you need to force push (e.g., after rebase):

```bash
#!/bin/bash

force_push() {
  local branch="${1:-$(git branch --show-current)}"

  # Validate branch name
  if [[ ! "$branch" =~ ^claude/ ]]; then
    echo "❌ Can only force push claude/* branches"
    return 1
  fi

  # Confirm force push
  echo "⚠️  Force pushing to: $branch"
  read -p "Continue? (yes/no): " confirm
  if [ "$confirm" != "yes" ]; then
    echo "Aborted"
    return 1
  fi

  # Force push with retry
  for i in 0 1 2 3; do
    if [ $i -gt 0 ]; then
      sleep $((2 ** i))
    fi
    if git push -u origin "$branch" --force 2>&1; then
      echo "✅ Force push successful!"
      return 0
    fi
  done

  echo "❌ Force push failed"
  return 1
}
```

---

## Pull Request Creation

### Using GitHub API

The `gh` CLI tool is **not available** in Claude Code on the web. Use the GitHub REST API instead.

#### Prerequisites

Ensure `GITHUB_TOKEN` is available:

```bash
# Check for token
if [ -z "$GITHUB_TOKEN" ]; then
  echo "❌ GITHUB_TOKEN not found"
  exit 1
fi

echo "✅ GITHUB_TOKEN available"
```

#### Basic PR Creation

```bash
#!/bin/bash

create_pr() {
  local title="$1"
  local body="$2"
  local head_branch="${3:-$(git branch --show-current)}"
  local base_branch="${4:-main}"
  local repo="${5:-owner/repo}"  # e.g., "shabaraba/vibing.nvim"

  # Create PR via GitHub API
  local response=$(curl -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${repo}/pulls" \
    -d "{
      \"title\": \"${title}\",
      \"head\": \"${head_branch}\",
      \"base\": \"${base_branch}\",
      \"body\": \"${body}\"
    }")

  # Extract PR URL
  local pr_url=$(echo "$response" | grep -o '"html_url": *"[^"]*"' | head -1 | cut -d'"' -f4)

  if [ -n "$pr_url" ]; then
    echo "✅ PR created: $pr_url"
    echo "$pr_url"
  else
    echo "❌ Failed to create PR"
    echo "$response"
    return 1
  fi
}

# Usage
create_pr \
  "fix: improve matchGlob regex escaping" \
  "This PR fixes regex escaping in the matchGlob function..." \
  "claude/fix-matchglob-abc123" \
  "main" \
  "shabaraba/vibing.nvim"
```

#### Advanced PR Creation with Formatting

```bash
#!/bin/bash

create_pr_formatted() {
  local title="$1"
  local base_branch="$2"
  local repo="$3"
  local head_branch="$(git branch --show-current)"

  # Multi-line body with proper escaping
  local body=$(cat <<'EOF'
## Summary

Brief description of changes.

## Changes

- Change 1
- Change 2
- Change 3

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Related Issues

Fixes #123
EOF
)

  # Escape JSON special characters
  body=$(echo "$body" | jq -Rs .)

  # Create PR
  local response=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${repo}/pulls" \
    -d "{
      \"title\": $(echo "$title" | jq -Rs .),
      \"head\": \"${head_branch}\",
      \"base\": \"${base_branch}\",
      \"body\": ${body}
    }")

  # Parse response
  local pr_number=$(echo "$response" | jq -r '.number // empty')
  local pr_url=$(echo "$response" | jq -r '.html_url // empty')

  if [ -n "$pr_number" ]; then
    echo "✅ PR #${pr_number} created: $pr_url"
    echo "$pr_url"
  else
    echo "❌ Failed to create PR"
    echo "$response" | jq .
    return 1
  fi
}
```

#### Creating Multiple PRs in Parallel

When you need to create multiple PRs at once:

```bash
#!/bin/bash

# Define PRs to create
declare -A prs=(
  ["claude/fix-pr146-abc123"]="fix: import URL from url module|feat/granular-permissions-123"
  ["claude/fix-pr144-abc123"]="docs: improve comments in ftplugin|feat/vibing-lsp-133"
  ["claude/fix-pr142-abc123"]="feat: add language validation|feat/default-language-config-125"
)

REPO="shabaraba/vibing.nvim"

# Create all PRs
for branch in "${!prs[@]}"; do
  IFS='|' read -r title base <<< "${prs[$branch]}"

  echo "Creating PR for $branch..."

  curl -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${REPO}/pulls" \
    -d "{
      \"title\": \"${title}\",
      \"head\": \"${branch}\",
      \"base\": \"${base}\",
      \"body\": \"Auto-generated PR from Claude Code\"
    }" | jq -r '.html_url // "Failed"'

  sleep 1  # Rate limiting
done
```

#### Updating Existing PR

To update a PR's description:

```bash
#!/bin/bash

update_pr() {
  local pr_number="$1"
  local new_body="$2"
  local repo="$3"

  # Update PR
  curl -X PATCH \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${repo}/pulls/${pr_number}" \
    -d "{
      \"body\": $(echo "$new_body" | jq -Rs .)
    }" | jq -r '.html_url // "Failed"'
}

# Usage
update_pr 150 "Updated description..." "shabaraba/vibing.nvim"
```

---

## Complete Workflows

### Workflow 1: Feature Development and PR Creation

Complete workflow from feature development to PR:

```bash
#!/bin/bash

# Configuration
REPO="shabaraba/vibing.nvim"
SESSION_ID="${CLAUDE_SESSION_ID:-9GOGf}"
FEATURE_NAME="add-new-feature"
BASE_BRANCH="main"

echo "=== Starting feature development workflow ==="

# Step 1: Create feature branch
BRANCH="claude/${FEATURE_NAME}-${SESSION_ID}"
echo "Creating branch: $BRANCH"
git checkout -b "$BRANCH"

# Step 2: Make changes
echo "Making changes..."
# (Your code changes here)

# Step 3: Commit changes
git add .
git commit -m "feat: add new feature

This commit adds...
"

# Step 4: Push with retry
echo "Pushing to remote..."
for i in 0 1 2 3; do
  if [ $i -gt 0 ]; then
    sleep $((2 ** i))
  fi
  if git push -u origin "$BRANCH"; then
    echo "✅ Push successful!"
    break
  fi
done

# Step 5: Create PR via API
echo "Creating pull request..."
PR_BODY=$(cat <<'EOF'
## Summary

This PR adds a new feature that...

## Changes

- Added new functionality
- Updated documentation
- Added tests

## Testing

- [x] Unit tests pass
- [x] Integration tests pass
- [x] Manual testing completed
EOF
)

PR_URL=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO}/pulls" \
  -d "{
    \"title\": \"feat: add new feature\",
    \"head\": \"${BRANCH}\",
    \"base\": \"${BASE_BRANCH}\",
    \"body\": $(echo "$PR_BODY" | jq -Rs .)
  }" | jq -r '.html_url // empty')

if [ -n "$PR_URL" ]; then
  echo "✅ PR created: $PR_URL"
else
  echo "❌ Failed to create PR"
  exit 1
fi

echo "=== Workflow complete ==="
```

### Workflow 2: Review Comment Resolution

Workflow for addressing PR review comments:

```bash
#!/bin/bash

# Configuration
PR_NUMBER="146"
REPO="shabaraba/vibing.nvim"
SESSION_ID="${CLAUDE_SESSION_ID:-9GOGf}"

echo "=== Addressing review comments for PR #${PR_NUMBER} ==="

# Step 1: Fetch PR details
echo "Fetching PR details..."
PR_DATA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO}/pulls/${PR_NUMBER}")

BASE_BRANCH=$(echo "$PR_DATA" | jq -r '.head.ref')

echo "Base branch: $BASE_BRANCH"

# Step 2: Create fix branch
FIX_BRANCH="claude/fix-pr${PR_NUMBER}-${SESSION_ID}"
echo "Creating fix branch: $FIX_BRANCH"

git checkout -b "$FIX_BRANCH"

# Step 3: Make fixes
echo "Making fixes..."
# (Your code changes here)

# Step 4: Commit fixes
git add .
git commit -m "fix: address review comments on PR #${PR_NUMBER}

- Fixed issue A
- Fixed issue B
"

# Step 5: Push fix branch
echo "Pushing fix branch..."
for i in 0 1 2 3; do
  if [ $i -gt 0 ]; then sleep $((2 ** i)); fi
  if git push -u origin "$FIX_BRANCH"; then
    break
  fi
done

# Step 6: Create PR to merge fix into base branch
echo "Creating PR for fixes..."
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${REPO}/pulls" \
  -d "{
    \"title\": \"fix: address review comments on PR #${PR_NUMBER}\",
    \"head\": \"${FIX_BRANCH}\",
    \"base\": \"${BASE_BRANCH}\",
    \"body\": \"Addresses review comments on PR #${PR_NUMBER}.\"
  }" | jq -r '.html_url // "Failed"'

echo "=== Review comment resolution complete ==="
```

### Workflow 3: Multiple PR Creation

Create multiple PRs in one session:

```bash
#!/bin/bash

REPO="shabaraba/vibing.nvim"
SESSION_ID="${CLAUDE_SESSION_ID:-9GOGf}"

# Array of PR configurations: "branch|title|base|description"
declare -a prs=(
  "claude/fix-eslint-${SESSION_ID}|fix: import URL from url module|feat/granular-permissions-123|Resolves ESLint error"
  "claude/improve-docs-${SESSION_ID}|docs: improve comments in ftplugin|feat/vibing-lsp-133|Clarifies documentation"
  "claude/add-validation-${SESSION_ID}|feat: add language validation|feat/default-language-config-125|Adds validation"
)

echo "=== Creating ${#prs[@]} pull requests ==="

for pr_config in "${prs[@]}"; do
  IFS='|' read -r branch title base body <<< "$pr_config"

  echo ""
  echo "Creating PR: $title"
  echo "  Branch: $branch"
  echo "  Base: $base"

  # Create PR
  PR_URL=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${REPO}/pulls" \
    -d "{
      \"title\": \"${title}\",
      \"head\": \"${branch}\",
      \"base\": \"${base}\",
      \"body\": \"${body}\"
    }" | jq -r '.html_url // "Failed"')

  if [[ "$PR_URL" == https://* ]]; then
    echo "  ✅ Created: $PR_URL"
  else
    echo "  ❌ Failed"
  fi

  # Rate limiting
  sleep 1
done

echo ""
echo "=== All PRs created ==="
```

---

## Troubleshooting

### Issue 1: HTTP 403 on Push

**Symptom:**

```text
error: RPC failed; HTTP 403 curl 22 The requested URL returned error: 403
```

**Cause:** Branch name doesn't follow required pattern `claude/*-<sessionId>`

**Solution:**

```bash
# Check current branch
CURRENT_BRANCH="$(git branch --show-current)"
echo "Current branch: $CURRENT_BRANCH"

# Create compliant branch
SESSION_ID="${CLAUDE_SESSION_ID:-9GOGf}"
NEW_BRANCH="claude/${CURRENT_BRANCH}-${SESSION_ID}"

git checkout -b "$NEW_BRANCH"
git push -u origin "$NEW_BRANCH"
```

### Issue 2: Network Timeout/Transient Failures

**Symptom:**

```text
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly
```

**Cause:** Transient network issues in web environment

**Solution:** Use retry logic (see [Git Push Operations](#git-push-operations))

### Issue 3: "Everything up-to-date" but Push Fails

**Symptom:**

```text
error: RPC failed; HTTP 403
Everything up-to-date
```

**Cause:** Local branch is synced but network/auth issue prevents push confirmation

**Solution:** Safe to ignore if you see "Everything up-to-date" - your changes are already pushed

### Issue 4: Cannot Create PR - No gh Command

**Symptom:**

```text
gh: command not found
```

**Cause:** `gh` CLI is not available in Claude Code on the web

**Solution:** Use GitHub API instead (see [Pull Request Creation](#pull-request-creation))

### Issue 5: Multiple Retry Failures

**Symptom:** All 4 retry attempts fail

**Possible Causes:**

1. Branch name doesn't follow required pattern
2. Network is down (rare)
3. Repository permissions issue

**Solution:**

```bash
# 1. Verify branch name
git branch --show-current

# 2. Check if branch follows pattern
if [[ "$(git branch --show-current)" =~ ^claude/.+-[a-zA-Z0-9]+$ ]]; then
  echo "✅ Branch name is valid"
else
  echo "❌ Branch name is invalid"
fi

# 3. Try with a fresh branch
SESSION_ID="${CLAUDE_SESSION_ID:-9GOGf}"
git checkout -b "claude/fresh-branch-${SESSION_ID}"
git push -u origin "claude/fresh-branch-${SESSION_ID}"
```

### Issue 6: PR Creation Returns Error

**Symptom:** API returns error instead of PR URL

**Debug:**

```bash
# Create PR and capture full response
RESPONSE=$(curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/owner/repo/pulls" \
  -d '{
    "title": "Test PR",
    "head": "claude/test-abc123",
    "base": "main",
    "body": "Test"
  }')

# Pretty print error
echo "$RESPONSE" | jq .

# Common errors:
# - "message": "Validation Failed" - Check branch exists and is pushed
# - "message": "Not Found" - Check repository name
# - "message": "Bad credentials" - Check GITHUB_TOKEN
```

---

## Quick Reference

### Essential Commands

```bash
# Create compliant branch
git checkout -b "claude/my-feature-${CLAUDE_SESSION_ID:-9GOGf}"

# Push with retry
for i in 0 1 2 3; do
  [ $i -gt 0 ] && sleep $((2 ** i))
  git push -u origin "$(git branch --show-current)" && break
done

# Create PR
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/owner/repo/pulls" \
  -d '{"title":"My PR","head":"claude/my-feature-abc","base":"main","body":"Description"}'
```

### Validation Checklist

Before pushing:

- [ ] Branch name starts with `claude/`
- [ ] Branch name ends with session ID
- [ ] Pattern matches: `^claude/.+-[a-zA-Z0-9]+$`
- [ ] Changes are committed
- [ ] Ready to retry up to 4 times if needed

Before creating PR:

- [ ] `GITHUB_TOKEN` is available
- [ ] Branch is pushed to remote
- [ ] Base branch name is correct
- [ ] Repository name format is `owner/repo`
- [ ] PR title and body are prepared
