---
name: github-issues
description: "Create, triage, label, assign GitHub issues via gh or REST."
allowed-tools:
  - bash
enabled: true
related-skills: [github-auth, github-pr-workflow]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# GitHub Issues Management

Create, search, triage, and manage GitHub issues. Each section shows `gh` first,
then `curl` fallback.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repo with GitHub remote, or specify repo explicitly

## Setup

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="curl"
fi

REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

## 1. Viewing Issues

```bash
# With gh
gh issue list --state open --limit 20
gh issue view 42

# With curl
curl -s "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20" | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    print(f'#{i[\"number\"]:4d} [{i[\"state\"]:6s}] {i[\"title\"][:60]}')
"
```

## 2. Creating Issues

```bash
# With gh (interactive editor)
gh issue create

# With gh (inline)
gh issue create --title "Bug: login fails on Safari" --body "Description..."

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d '{"title":"Bug: login fails","body":"Description","labels":["bug"]}'
```

## 3. Searching Issues

```bash
# Search within repo
gh issue list --search "login error" --state all

# Search across GitHub
gh search issues "is:issue is:open repo:$OWNER/$REPO label:bug"

# With curl (GitHub Search API)
curl -s "https://api.github.com/search/issues?q=repo:$OWNER/$REPO+label:bug+state:open" | python3 -c "
import sys, json
r = json.load(sys.stdin)
print(f'Total: {r[\"total_count\"]}')
for i in r['items']:
    print(f'#{i[\"number\"]:4d} {i[\"title\"][:60]}')
"
```

## 4. Labels

```bash
# List labels
gh label list

# Create label
gh label create "priority-high" --color "D73A4A" --description "High priority"

# Add label to issue
gh issue edit 42 --add-label "priority-high"

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \
  -d '{"labels":["priority-high"]}'
```

## 5. Assigning

```bash
# With gh
gh issue edit 42 --add-assignee username

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/assignees \
  -d '{"assignees":["username"]}'
```

## 6. Comments

```bash
# With gh
gh issue comment 42 --body "Can you reproduce with the latest version?"

# With curl
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/comments \
  -d '{"body":"Can you reproduce with the latest version?"}'
```

## 7. Closing / Reopening

```bash
# With gh
gh issue close 42
gh issue reopen 42

# With curl
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  -d '{"state":"closed"}'
```

## 8. Triage Workflow

```bash
# List untriaged issues (no labels)
gh issue list --state open --search "no:label"

# Bulk add labels
for num in 10 11 12 13; do
  gh issue edit $num --add-label "triaged"
done

# List issues assigned to you
gh issue list --assignee @me --state open
```

## Pitfalls

- **Issues vs PRs**: GitHub API returns PRs in the issues endpoint. Filter
  with `pull_request` field: `if 'pull_request' not in i`.
- **Rate limits**: authenticated 5000/hour, unauthenticated 60/hour. Always
  use token.
- **Label colors**: must be 6-char hex without `#` (e.g. `D73A4A`).
- **Assignees**: must be collaborators. Non-collaborators silently ignored.
