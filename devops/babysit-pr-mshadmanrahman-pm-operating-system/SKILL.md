---
name: babysit-pr
description: |
  Monitor open PRs, retry flaky CI, resolve merge conflicts, and auto-merge when ready. Use when managing multiple PRs, after creating PRs, or when CI is failing intermittently. Triggers on: "babysit my PRs", "check PR status", "why is CI failing", "merge my PRs", "monitor PRs", "PR status", "what's blocking my PRs", "/babysit-pr".
---

# Babysit PR

Continuous PR lifecycle management: monitor CI, retry flaky checks, resolve merge conflicts, and enable auto-merge. Inspired by Thariq's CI/CD & Deployment pattern from Anthropic's internal playbook.

## When to Activate

- User says "babysit my PRs", "check PR status", "monitor PRs"
- User says "why is CI failing", "what's blocking my PRs"
- User says "merge my PRs", "auto-merge when ready"
- After a batch PR creation session (e.g., 10+ PRs in a day)
- When CI is flaky and user wants automatic retries

## Modes

### Single PR Mode

Monitor one specific PR by number or URL.

```
babysit-pr #4105
babysit-pr https://github.com/your-org/your-repo/pull/4105
```

**Steps:**
1. Parse PR number from input (strip URL if needed)
2. Run `scripts/check-pr-status.sh <repo> <pr-number>`
3. Analyze CI failures against `references/ci-patterns.md`
4. Take action or report findings

### Batch Mode

Scan all open PRs by the current user across a repo.

```
babysit-pr your-org/your-repo
babysit-pr --all
```

**Steps:**
1. Run `scripts/batch-check.sh <repo>` (defaults to current repo's origin)
2. Sort PRs by urgency: failing CI > merge conflicts > pending review > green
3. Present summary table
4. Offer to act on each issue

## PR Health Checks

For each PR, check all of the following:

### 1. CI Status
```bash
gh pr checks <number> --repo <repo>
```
- Map each check to pass/fail/pending
- Cross-reference failures with `references/ci-patterns.md`
- Distinguish required checks from optional/informational

### 2. Review Status
```bash
gh pr view <number> --repo <repo> --json reviews,reviewRequests
```
- Approved: ready to merge
- Changes requested: needs author action
- Pending: waiting on reviewers

### 3. Merge Conflicts
```bash
gh pr view <number> --repo <repo> --json mergeable,mergeStateStatus
```
- MERGEABLE: no conflicts
- CONFLICTING: needs rebase/conflict resolution
- UNKNOWN: GitHub still computing (wait and retry)

### 4. Branch Staleness
```bash
gh pr view <number> --repo <repo> --json baseRefName,headRefName,updatedAt
```
- If behind base by 10+ commits, suggest updating branch
- If no activity for 7+ days, flag as stale

## Auto-Actions

### Retry Flaky CI
When a check fails and `references/ci-patterns.md` marks the pattern as retryable:

```bash
# Re-run failed GitHub Actions workflows
gh run rerun <run-id> --failed --repo <repo>
```

Rules:
- Max 2 retries per check
- Only retry if the failure pattern matches a known flaky pattern
- Log each retry attempt
- If still failing after 2 retries, report as real failure

### Update Branch
When PR is behind base branch and has no merge conflicts:

```bash
# GitHub API branch update (no force push)
gh api repos/<owner>/<repo>/pulls/<number>/update-branch \
  --method PUT \
  --field expected_head_sha="<sha>"
```

Rules:
- Only update if mergeable state is clean
- Never force-push
- Report the update to the user

### Enable Auto-Merge
When CI is green and reviews are approved:

```bash
gh pr merge <number> --repo <repo> --auto --squash
```

Rules:
- **Always ask before enabling auto-merge**
- Only enable if: CI passing + reviews approved + no conflicts
- Default to squash merge
- Never force-merge or bypass required checks

## Safety Rules

1. **Never force-merge** a PR under any circumstances
2. **Never dismiss reviews** or bypass review requirements
3. **Always report before acting** on merge conflicts; let the user decide
4. **Ask before enabling auto-merge**; present the PR state first
5. **Never push code** to resolve conflicts without explicit user approval
6. **Respect branch protection** rules; do not circumvent them
7. **Log all actions taken** so the user has a clear audit trail

## Output Format

### Single PR Report
```
PR #4105: Fix recommendation form validation
  CI:       2/3 passing (vercel/preview-deploy pending - 1m ago)
  Reviews:  Approved (2/2)
  Merge:    Clean, no conflicts
  Branch:   3 commits behind main
  Action:   Update branch? [y/n]
```

### Batch Summary
```
your-org/your-repo - 14 open PRs by @your-github-handle

 #   | Title                          | CI      | Reviews  | Merge     | Action
-----|--------------------------------|---------|----------|-----------|--------
4105 | Fix form validation            | Passing | Approved | Clean     | Auto-merge?
4103 | Update i18n strings            | Failing | Approved | Clean     | Retry CI (flaky playwright)
4101 | Refactor search component      | Passing | Pending  | Conflicts | Report conflicts
4099 | Add landscape mode support     | Pending | Pending  | Clean     | Wait

Actions available:
1. Retry flaky CI on #4103
2. Enable auto-merge on #4105
3. Show conflict details for #4101
```

## Gotchas

- **Vercel preview deploys** take 2-3 minutes; do not declare failure before 3 minutes have elapsed. Check the `updatedAt` timestamp on pending checks.
- **`gh pr checks` shows ALL checks** including optional/informational ones. Cross-reference with branch protection rules to identify which are required.
- **Some repos have required reviewers**; auto-merge will not work without the required number of approvals, even if CI is green.
- **GitHub mergeable state** can be UNKNOWN for up to 30 seconds after a push. If UNKNOWN, wait 10 seconds and retry once.
- **Rate limits**: `gh` CLI shares GitHub API rate limits. Batch mode across many repos can hit limits. Space requests if checking 20+ PRs.
- **Forked PRs** have different permissions; CI retry may not work on PRs from external contributors.

## Scripts

- `scripts/check-pr-status.sh <repo> <pr-number>` : Single PR status as JSON
- `scripts/batch-check.sh [repo]` : All open PRs by current user with status

## References

- `references/ci-patterns.md` : Known CI failure patterns and retry policy
