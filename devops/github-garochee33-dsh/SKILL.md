---
name: github
description: "GitHub repository management — triage PRs/issues, check Actions status, manage branch protection, tag releases, housekeeping (stale branches, stashes), CODEOWNERS, badges, and repo hardening. Use when the user asks about GitHub, PRs, CI/CD status, repo health, branch protection, releases, or any GitHub operations."
---

# GitHub

## Overview

Umbrella entrypoint for all GitHub repository work. Handles triage, repo-ops, hardening, and routes to specialist skills when needed.

This skill is intentionally hybrid:
- Prefer `gh` CLI for Actions, branch protection, releases, API calls, and repo management.
- Use local `git` for branch state, stashes, unpushed commits, and local housekeeping.
- Route to specialist skills for narrow workflows (review, CI debug, publish).

## Core Capabilities

### 1. Actions / CI-CD Health
- `gh run list` — check workflow status (green/red/in-progress)
- `gh run view <id> --log-failed` — diagnose failures
- Verify full pipeline: CI → CD (deploy) chain
- Concurrency configuration audit

### 2. Branch Protection
- Enable/disable via `gh api repos/{owner}/{repo}/branches/{branch}/protection`
- Required status checks (strict mode)
- Force-push and deletion prevention
- Enforce admins toggle
- PR review requirements

### 3. Release Management
- `gh release create` — tag from current main with changelog
- Semantic versioning (vMAJOR.MINOR.PATCH)
- Release notes from recent commits
- Rollback anchors for production deploys

### 4. Repository Housekeeping
- Stale remote branches: `gh api` + `git remote prune`
- Local stashes: `git stash list` / `git stash clear`
- Unpushed commits: `git log origin/main..HEAD`
- Dangling refs and orphan branches

### 5. CODEOWNERS & Governance
- Create/update `.github/CODEOWNERS`
- Map ownership by directory (server/, client/, .github/, infra/)
- Validate CODEOWNERS syntax

### 6. Secret Scanning & Security
- Enable GitHub native secret scanning (if plan supports)
- Verify gitleaks workflow presence as fallback
- Dependabot configuration (`.github/dependabot.yml`)

### 7. Status Badges
- CI/Deploy/Security badges in README
- Badge format: `[![Name](url/badge.svg)](url)`

### 8. PR & Issue Triage
- Open PR list with status
- Issue summarization
- PR patch inspection
- Comments, labels, reactions

## Routing Rules

1. **Resolve context**: repo from user input, URL, or local `git remote -v`
2. **Classify**:
   - `health check` → Actions status, branch protection audit
   - `hardening` → protection rules, CODEOWNERS, dependabot, badges
   - `housekeeping` → stale branches, stashes, dangling refs
   - `release` → tag, changelog, version bump
   - `triage` → PRs, issues, patches, comments
   - `review follow-up` → route to `gh-address-comments`
   - `CI debugging` → route to `gh-fix-ci`
   - `publish` → route to `yeet`
3. **Execute** with confirmation for destructive ops (force-push, branch delete, stash clear)

## Command Reference

```bash
# Actions
gh run list --repo OWNER/REPO --limit 10
gh run view RUN_ID --log-failed

# Branch Protection
gh api repos/OWNER/REPO/branches/main/protection -X PUT --input protection.json
gh api repos/OWNER/REPO/branches/main/protection  # GET current

# Releases
gh release create vX.Y.Z --target main --title "title" --notes "notes"
gh release list --repo OWNER/REPO

# Branches
gh api repos/OWNER/REPO/branches --jq '.[].name'
gh api repos/OWNER/REPO/git/refs/heads/BRANCH -X DELETE

# Secret Scanning
gh api repos/OWNER/REPO -X PATCH -f security_and_analysis='{"secret_scanning":{"status":"enabled"}}'

# Housekeeping
git remote prune origin
git stash list / git stash clear
git log origin/main..HEAD --oneline
```

## Hardening Checklist

When user asks to "harden" or "audit" a repo, run through:

- [ ] Branch protection enabled on default branch
- [ ] CI required to pass before merge
- [ ] Force-push disabled
- [ ] CODEOWNERS file present
- [ ] Dependabot or Renovate configured
- [ ] Secret scanning (native or gitleaks)
- [ ] At least one tagged release
- [ ] No stale branches
- [ ] Status badges in README
- [ ] Concurrency configured in CI workflow

## Output Expectations

- Health checks: table of workflow statuses with ✅/❌/🔄
- Hardening: checklist with pass/fail and remediation commands
- Housekeeping: list of items cleaned with before/after state
- Releases: link to created release
- Always end with clear summary of what changed

## Examples

- "Check if CI/CD is green"
- "Harden this repo"
- "Any stale branches or open PRs?"
- "Tag a release"
- "Enable branch protection"
- "Add status badges to README"
- "Run the full housekeeping pass"
