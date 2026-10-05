---
name: github
description: Use when gitHub Automation Hub — Actions, Issues, and PR management for
  CI/CD, project tracking, and code review workflows. Monetize through automation-as-a-service.
domain: integrations
author: oyi77
license: Apache-2.0
subdomain: integrations
tags:
- api
- automation
- ci-cd
- github
- integrations
- workflow
- github-actions
- github-issues
- github-pr
- devops
version: 1.0.0
category: integrations
---
## Overview

This skill is the GitHub automation hub — Actions, Issues, and PR management for CI/CD, project tracking, and code review workflows. Use it when repository operations should be automated rather than manual. It covers the workflows that keep a repo healthy and its releases flowing.



# GitHub Automation Hub



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Money-Making Overview

GitHub is the backbone of modern software development. Monetize your GitHub automation skills through these high-value offerings:

| Service | ROI Estimate | Market |
|---------|-------------|--------|
| CI/CD pipeline setup & optimization | $2K-$10K/client | Dev teams, startups |
| Issue triage automation service | $500-$3K/month retainer | Open-source projects, SaaS teams |
| PR review automation + merge trains | $1K-$5K/setup | Engineering orgs (20+ devs) |
| Custom GitHub Action marketplace listings | $3K-$15K/action | Companies needing internal tools |
| GitHub compliance & audit reporting | $2K-$8K/quarter | Regulated industries (SOC2, HIPAA) |
| Migration automation (GitLab/Bitbucket → GitHub) | $3K-$12K/project | Enterprises migrating platforms |

**Combined monthly recurring potential: $5K-$20K/client** (as DevOps automation retainer).

### Who Pays
- **Startups** — need CI/CD setup but no DevOps hire yet ($150-250/hr)
- **Mid-market SaaS** — compliance automation + PR workflow ($3-8K/mo retainer)
- **Agencies** — white-label CI/CD for client delivery ($500-2K/project markup)
- **Open-source maintainers** — issue/PR triage bots ($200-500/mo)
- **Enterprises** — custom internal GH Actions for compliance gates ($10-30K/project)

## Combined Capabilities

| Capability | Scope | Output |
|-----------|-------|--------|
| **GitHub Actions** | CI/CD pipelines, scheduled jobs, composite actions, matrix builds, Docker/JS actions, OIDC auth, self-hosted runners | Workflow YAML, action repos, runner configs |
| **GitHub Issues** | CRUD operations, labels, milestones, comments, assignees, templates, webhooks, automation | REST/GraphQL API scripts, issue templates, bot automation |
| **GitHub PR** | Create/review/merge PRs via CLI (`gh`) and API, branch protection, required checks, auto-merge, squash/rebase/merge | PR templates, merge policies, automation scripts |

## Authentication & Setup

All three sub-skills share the same auth stack:

```bash
# Option A: Personal Access Token (classic or fine-grained)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
gh auth login --with-token < <(echo "$GITHUB_TOKEN")

# Option B: GitHub App installation token (for orgs/bots)
# Generate via: https://github.com/settings/apps
# Then:
export GITHUB_APP_ID="123456"
export GITHUB_APP_INSTALL_ID="654321"
export GITHUB_APP_PRIV_KEY=$(cat /path/to/private-key.pem)

# Generate token from app
curl -X POST \
  "https://api.github.com/app/installations/$GITHUB_APP_INSTALL_ID/access_tokens" \
  -H "Authorization: Bearer $(jq -r .token < <( \
    curl -X POST "https://api.github.com/app/installations/$GITHUB_APP_INSTALL_ID/access_tokens" \
    -H "Authorization: Bearer $(echo '{"alg":"RS256"}' | jq -c .)" \
  ))"

# Option C: OIDC (for Actions running in the same org)
# Actions can get a GITHUB_TOKEN automatically: ${{ secrets.GITHUB_TOKEN }}
```

Rate limits: 5,000 requests/hr (authenticated), 60/hr (unauthenticated). Fine-grained tokens give higher org limits.

## Concrete Action Flows

### Flow 1: CI/CD Pipeline (GitHub Actions)

Automate build-test-deploy for any project in under 30 minutes.

```yaml
# .github/workflows/ci.yml — Multi-stage CI pipeline
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.node-version }}
          path: coverage/

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

### Flow 2: Issue Triage Automation

Create an issue-triaging Action that auto-labels, assigns, and greets:

```yaml
# .github/workflows/triage.yml
name: Triage
on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const title = issue.title.toLowerCase();
            const body = issue.body?.toLowerCase() || '';

            // Auto-label based on content patterns
            const labels = [];
            if (/bug|error|fail|crash|broken/i.test(title + body)) labels.push('bug');
            if (/feature|request|would like|please add/i.test(title + body)) labels.push('enhancement');
            if (/help|how|question|guide/i.test(title + body)) labels.push('question');
            if (/urgent|critical|blocker|p0/i.test(title + body)) labels.push('priority:high');
            if (labels.length) await github.rest.issues.addLabels({
              ...context.repo, issue_number: issue.number, labels
            });

            // Add welcome comment for first-time contributors
            const isFirst = issue.author_association === 'FIRST_TIME_CONTRIBUTOR'
                         || issue.author_association === 'FIRST_TIMER';
            if (isFirst) {
              await github.rest.issues.createComment({
                ...context.repo,
                issue_number: issue.number,
                body: `Thanks for contributing @${issue.user.login}! A maintainer will review soon.`
              });
            }
```

### Flow 3: Automated PR Merge Train

Safely auto-merge PRs that pass all checks:

```bash
#!/usr/bin/env bash
# auto-merge-prs.sh — Auto-merge PRs matching criteria
# Usage: ./auto-merge-prs.sh owner/repo

REPO="${1:-owner/repo}"
gh pr list --repo "$REPO" --state open --json number,title,headRefName,reviews,labels \
  | jq -c '.[] | select(
      .reviews | length > 0 and any(.state == "APPROVED")
    )' \
  | while read -r pr; do
      PR_NUM=$(echo "$pr" | jq -r '.number')
      echo "Merging #$PR_NUM: $(echo "$pr" | jq -r '.title')"
      gh pr merge "$PR_NUM" --repo "$REPO" --squash --delete-branch
    done
```

### Flow 4: Bulk Issue Management via API

Create, update, and close issues at scale:

```python
#!/usr/bin/env python3
"""Bulk issue operations via GitHub REST API."""
import os, json, requests

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}
API = "https://api.github.com"

def create_issue(owner, repo, title, body="", labels=None, assignees=None):
    """Create a GitHub issue."""
    resp = requests.post(
        f"{API}/repos/{owner}/{repo}/issues",
        headers=HEADERS,
        json={
            "title": title,
            "body": body,
            "labels": labels or [],
            "assignees": assignees or [],
        },
    )
    resp.raise_for_status()
    return resp.json()["number"]

def list_issues(owner, repo, state="open", label=None):
    """List issues with optional label filter."""
    params = {"state": state, "per_page": 100}
    if label:
        params["labels"] = label
    resp = requests.get(
        f"{API}/repos/{owner}/{repo}/issues",
        headers=HEADERS,
        params=params,
    )
    resp.raise_for_status()
    return resp.json()

def add_comment(owner, repo, issue_number, body):
    """Add a comment to an issue."""
    resp = requests.post(
        f"{API}/repos/{owner}/{repo}/issues/{issue_number}/comments",
        headers=HEADERS,
        json={"body": body},
    )
    resp.raise_for_status()

def close_issue(owner, repo, issue_number):
    """Close an issue."""
    resp = requests.patch(
        f"{API}/repos/{owner}/{repo}/issues/{issue_number}",
        headers=HEADERS,
        json={"state": "closed"},
    )
    resp.raise_for_status()

# Example: Close all stale "wontfix" issues
for issue in list_issues("owner", "repo", label="wontfix"):
    close_issue("owner", "repo", issue["number"])
    add_comment("owner", "repo", issue["number"],
                "Auto-closing: marked as wontfix.")
    print(f"Closed #{issue['number']}: {issue['title']}")
```

### Flow 5: CI/CD Pipeline Audit & Fix

Audit a repo's CI/CD health and generate fixes:

```bash
#!/usr/bin/env bash
# audit-ci.sh — Check GitHub Actions CI health for a repo
set -euo pipefail

REPO="${1?Usage: $0 owner/repo}"

echo "=== CI/CD Audit for $REPO ==="

# 1. Check workflow files exist
WORKFLOWS=$(gh api "/repos/$REPO/actions/workflows" --jq '.total_count')
echo "Workflow count: $WORKFLOWS"

# 2. Check last 10 workflow runs
gh run list --repo "$REPO" --limit 10 --json conclusion,workflowName,createdAt \
  | jq -r '.[] | "\(.createdAt) \(.workflowName): \(.conclusion)"'

# 3. Check branch protection on main
BRANCH_PROTECTION=$(gh api "/repos/$REPO/branches/main/protection" --jq '.required_status_checks.contexts // []' 2>/dev/null || echo '[]')
echo "Required CI checks: $(echo "$BRANCH_PROTECTION" | jq -r '.[] // "none"')"

# 4. Check for stale workflow caches
gh actions cache list --repo "$REPO" --json id,key,lastAccessedAt,sizeInBytes \
  | jq -r '.[] | select(.lastAccessedAt < (now - 86400*30 | strftime("%Y-%m-%d"))) | "Stale: \(.key) (\(.sizeInBytes) bytes)"'

echo "=== Audit Complete ==="
```

### Flow 6: Release Automation

Create a release with auto-generated changelog:

```bash
#!/usr/bin/env bash
# release.sh — Tag, release notes, and publish
set -euo pipefail

REPO="${1?Usage: $0 owner/repo}"
VERSION="${2:-$(date +%Y%m%d.%H%M)}"

# Create tag
git tag "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

# Generate release notes (uses PR titles between last two tags)
LAST_TAG=$(git describe --tags --abbrev=0 HEAD~1 2>/dev/null || echo "")
if [ -n "$LAST_TAG" ]; then
  gh release create "v$VERSION" \
    --repo "$REPO" \
    --title "Release v$VERSION" \
    --notes-start-tag "$LAST_TAG" \
    --generate-notes
else
  gh release create "v$VERSION" \
    --repo "$REPO" \
    --title "Release v$VERSION" \
    --generate-notes
fi

echo "Released v$VERSION"
```

## First Action in 60 Minutes

```
00:00-05:00 — Create GitHub PAT with repo, workflow, and actions scopes
05:00-10:00 — Install gh CLI and authenticate: gh auth login
10:00-15:00 — Clone target repo, examine existing workflows
15:00-30:00 — Add a .github/workflows/ci.yml with lint+test
30:00-35:00 — Commit and push, verify the workflow triggers
35:00-45:00 — Set up issue template: .github/ISSUE_TEMPLATE/bug.yml
45:00-50:00 — Create a test issue via API (curl/gh) to verify labels work
50:00-60:00 — Open a test PR, approve and merge it via CLI
```

**By the end of 60 minutes, you have:**
- Working CI pipeline
- Issue template + API automation working
- PR merge workflow tested
- Audit script ready to run on any repo
- Proven infrastructure you can sell as a DevOps audit deliverable

## Verification

- Create a test issue and PR in a sandbox repo and confirm the documented automation (labels, assignment, CI) fires.
- Verify Actions: push a commit and confirm the workflow runs and reports the expected status.
- Test webhook/notification paths with an invalid secret and confirm signature failures are logged, not silently accepted.
- Confirm the automation respects repo permissions — no operation escalates beyond the token's scope.

## Anti-Rationalization Table

| Rationalization | Reality |
|---------------|---------|
| "I'll set up CI manually per project" | Template-based CI saves 2+ hours per project. Create reusable starter workflows. |
| "Issue labels are not that important" | Proper labeling enables automation. A triage bot pays for itself in maintainer time. |
| "CLI is enough for PRs" | The API unlocks auto-merge trains, cross-repo dependencies, and compliance gates at scale. |
| "GitHub Actions only lives in YAML" | Composite actions, Docker actions, and JavaScript actions are reusable products you can sell. |
| "I don't need webhooks if I poll" | Webhooks are instant; polling burns rate limits. Set up a webhook receiver on day one. |
| "OIDC is too complex for small projects" | OIDC eliminates long-lived secrets entirely. Worth the setup for any team with >1 cloud deployment. |

## Output Format

All GitHub automation deliverables follow this structure:

```
.github/
  workflows/
    ci.yml               # Build, test, lint
    release.yml          # Tag, changelog, publish
    triage.yml           # Issue/PR triage automation
  ISSUE_TEMPLATE/
    bug.yml              # Bug report template
    feature.yml          # Feature request template
  dependabot.yml         # Dependency update config
scripts/
  audit-ci.sh            # CI/CD health audit
  bulk-issues.py         # Bulk issue management
  auto-merge.sh          # PR merge train
```

## Verification Checklist

- [ ] CI pipeline runs end-to-end (push triggers → build → test → report)
- [ ] Issue CRUD operations work via both API and `gh` CLI
- [ ] PR creation, review, approval, and merge all function
- [ ] Branch protection rules match CI status checks
- [ ] Issue templates render correctly (both bug and feature)
- [ ] Auto-labeling regex triggers on test issue
- [ ] Rate limit handling: script retries on 429/403 responses
- [ ] Secrets are injected via `${{ secrets.* }}`, never hardcoded
- [ ] OIDC tokens work for cloud provider auth (if configured)
- [ ] Dependabot is configured for npm/pip/cargo/gomod updates
- [ ] Audit script produces meaningful output on a real repo
- [ ] Release workflow creates a tag, changelog, and GitHub Release
- [ ] Money protocol: deliverable is packaged and billable


## When to Use
Use this skill when working with github.


## Workflow
See the parent skill for authoritative workflow documentation.
