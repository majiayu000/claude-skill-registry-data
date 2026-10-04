---
name: superpowers-land-and-deploy
description: >
  Use when asked to "land and deploy", "merge and ship", "deploy this PR", "merge to production",
  "ship to prod", or after /ship creates a PR. Picks up after /ship — verifies CI, merges PR,
  waits for deploy, runs canary checks, and produces a deploy report.
---

> **DEPRECATED** — use `/land-and-deploy` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Land and Deploy

**Purpose:** Merge PR → wait for CI → deploy → verify production via canary checks.

**Prerequisite:** A PR must exist (typically created by `/ship`).

---

## Step 0: Pre-flight

```bash
# Verify GitHub CLI auth
gh auth status 2>&1

# Detect current branch and associated PR
CURRENT_BRANCH=$(git branch --show-current)
echo "Branch: $CURRENT_BRANCH"

# Find the PR
gh pr list --head "$CURRENT_BRANCH" --state open --json number,title,url,body 2>/dev/null
```

If no PR found:
```
No open PR found for branch "$CURRENT_BRANCH".
Run /ship first to create a PR.
```

---

## Step 1: Pre-Merge Checks

```bash
# CI status
gh pr view --json statusCheckRollup,commits -q '.'
gh pr view --json mergeable --jq '.mergeable'

# Check for merge conflicts
gh pr view --json hasMergeConflict --jq '.hasMergeConflict'
```

If CI is not passing → STOP. Report which checks are failing.

If merge conflicts exist → STOP. Report conflicts.

---

## Step 2: Wait for CI

If checks are pending:

```
CI checks are pending. Waiting for them to complete...
(Polling every 60s, timeout: 15 minutes)
```

```bash
gh pr view --json statusCheckRollup --jq '.statusCheckRollup[] | "\(.name): \(.conclusion // .status)"'
```

Poll every 60 seconds. After 15 minutes of waiting → STOP and ask what to do.

---

## Step 3: Pre-Merge Readiness Gate

Present the readiness dashboard before merging:

```
PRE-MERGE READINESS GATE
════════════════════════════════════════
PR:           #[N] — [title]
Author:       [user]
CI Status:    [PASSING / FAILING]
Conflicts:    [NONE / EXISTS]
Base:         [branch]
════════════════════════════════════════

Evidence checklist:
[ ] CI checks passing (all green)
[ ] No merge conflicts
[ ] Tests included in PR
[ ] Code review approved
[ ] PR description accurate
[ ] CHANGELOG updated (if applicable)
════════════════════════════════════════
```

Ask for explicit confirmation before merging:

```
Ready to merge #[N] to [base]?
A) Merge now
B) Wait for CI to complete
C) Abort — something needs attention
```

---

## Step 4: Merge

```bash
# Detect merge method
# Auto-detect: squash / merge commit / rebase based on repo settings
gh pr view --json viewerCanMerge --jq '.viewerCanMerge'

# Merge with auto-detected method
gh pr merge --auto --delete-branch 2>&1 || gh pr merge --squash 2>&1 || gh pr merge --merge 2>&1
```

After merge:
```
Merged! PR #[N] merged to [base].
Branch deleted: $CURRENT_BRANCH
```

---

## Step 5: Deploy Strategy Detection

Detect how this project deploys:

```bash
# GitHub Actions
ls .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null

# Platform-specific
ls Vercel.json netlify.toml render.yaml fly.toml app.yaml 2>/dev/null

# Kubernetes
kubectl config current-context 2>/dev/null || true

# Docker
ls Dockerfile docker-compose*.yml 2>/dev/null

# Custom deploy
grep -rE "deploy|ship|release" package.json 2>/dev/null | head -5
```

| Platform | Detection | Verification method |
|----------|---------|-------------------|
| Vercel | `vercel.json` | `vercel inspect <url>` |
| Netlify | `netlify.toml` | `netlify deploy --prod --dry-run` |
| Fly.io | `fly.toml` | `fly releases` |
| Render | `render.yaml` | `render get services` |
| GitHub Actions | `.github/workflows/` | Check Actions tab |
| Heroku | `Procfile` | `heroku releases` |
| Custom | package.json scripts | Run deploy script |

---

## Step 6: Wait for Deploy

For each detected platform, wait for the deploy to complete:

```bash
# GitHub Actions — poll deployment
gh run list --workflow="Deploy.yml" --limit=1 --json status,conclusion,htmlUrl -q '.[0]'

# Vercel
vercel ls 2>/dev/null | grep production || echo "Checking..."

# Fly.io
fly releases 2>/dev/null | head -5
```

Poll every 30 seconds. Timeout: 30 minutes. After timeout → offer to continue monitoring or proceed with available evidence.

---

## Step 7: Canary Verification

Verify production health. Depth varies by scope:

| Scope | Verification |
|-------|-------------|
| Docs only | Skip canary |
| Config/infra | Smoke test (health endpoint) |
| Backend API | Health endpoint + basic smoke test |
| Frontend | Health + console errors + screenshot |
| Full stack | All of the above |

```bash
# Health check
curl -s -o /dev/null -w "%{http_code}" https://<app-url>/health 2>/dev/null || \
curl -s -o /dev/null -w "%{http_code}" https://<app-url>/api/health 2>/dev/null || \
echo "NO_HEALTH_ENDPOINT"

# Console errors (if browser available)
# Run: agent-browser open <url> && agent-browser console errors && agent-browser screenshot

# Screenshot comparison
# Run: agent-browser open <url> && agent-browser screenshot /tmp/prod-deploy.png
```

---

## Step 8: Revert Flow

If canary verification fails:

```
CANARY CHECK FAILED
════════════════════════════════
What failed: [description]
Expected: [what should happen]
Actual: [what happened]
════════════════════════════════

A) Revert immediately — rollback to previous version
B) Investigate first — diagnose the issue
C) Ignore and continue — this is a false positive
```

If user chooses A:
```bash
# Revert via git
git revert HEAD --no-edit
git push

# Or via platform-specific rollback
# (add platform-specific rollback commands here)
```

---

## Step 9: Deploy Report

```
DEPLOY REPORT
════════════════════════════════
PR:           #[N] — [title]
Merged:       [time]
Branch:       [branch] (deleted)
CI:           [PASSED / FAILED]
Deploy:       [COMPLETE / IN PROGRESS / TIMEOUT]
Canary:       [PASSING / FAILED / SKIPPED]
Production:   [url]
════════════════════════════════
VERDICT: [SUCCESS / NEEDS_ATTENTION / REVERTED]
════════════════════════════════
```

Save to `.claude/deploy-reports/deploy-$(date +%Y-%m-%d-%H%M%S).json`:

```bash
mkdir -p .claude/deploy-reports
```

---

## Step 10: Follow-up Suggestions

```
Deploy complete.

Suggested next steps:
- /canary — set up post-deploy monitoring
- /retro — record what shipped
- /document-release — update docs for this change
- /benchmark — measure performance impact
```

---

## Key Principles

- **Mostly automated** — only stops at the pre-merge readiness gate and canary failures
- **Revert always available** — escape hatch at every failure point
- **Auto-detect everything** — PR number, merge method, deploy platform, canary depth
- **Completeness first** — E2E, docs checks, review staleness all evaluated

---

## Completion Status

- **DONE** — PR merged, deployed, canary passed
- **DONE_WITH_CONCERNS** — Deployed but canary had issues
- **BLOCKED** — CI failing or merge conflict
- **NEEDS_CONTEXT** — No PR found or deploy platform unclear
