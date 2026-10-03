---
name: release-engineer
description: Structured release and ship workflow skill. Use when the user wants to ship code, create a PR, merge to main, deploy to production, run pre-ship checks, bootstrap a test framework, or needs a repeatable release process from final review to live deployment.
---

# Release Engineer

Approach every release as the engineer who owns it end-to-end — from the last line of code to verified traffic in production. A release isn't done when the PR is merged. It's done when the system is healthy, metrics are normal, and you could roll back in under five minutes if they weren't.

---

## Step 0: Triage the Release Path

Before executing any steps, determine which path applies:

1. **Normal release** — feature or fix developed on a branch, PR into `main`, standard CI gate, deploy to production on merge.
2. **Hotfix release** — production is broken right now. Branch from the production tag or `main`, fix, fast-track review, deploy, backport.
3. **Release candidate** — a named, versioned artifact that will be promoted through staging → production with a manual gate.

If the user hasn't said which path, ask. Choosing the wrong path (treating a hotfix like a normal release) adds minutes you don't have when production is down. Choosing the wrong path in the other direction (treating a normal feature like a hotfix) bypasses the quality gates that exist for a reason.

State which path you're on at the start of every release workflow, and why.

---

## Step 1: Pre-Ship Checklist

Run this checklist before touching `git` for any release. Every item has a reason — don't skip any without documenting why.

### 1.1 Sync with Base Branch

```bash
git fetch origin
git checkout main && git pull --ff-only origin main
git checkout <your-branch>
git rebase origin/main
# Resolve any conflicts. Rebasing (not merging) keeps history linear and
# makes the diff in the PR exactly what you changed — not mixed with merge noise.
```

If the rebase surfaces conflicts, resolve them now. A PR with conflicts doesn't merge cleanly and signals to reviewers that the branch is stale.

### 1.2 Automated Quality Gates

Run the full local quality suite — don't skip steps because "CI will catch it." CI feedback takes minutes; local feedback takes seconds. A red CI on a PR you just opened is a social and velocity cost.

```bash
# Lint — catches style, potential bugs, and enforces consistency
npm run lint          # or: ruff check . / golangci-lint run / cargo clippy

# Type check — catches contract violations that tests might not cover
npm run type-check    # or: mypy . / tsc --noEmit

# Unit tests with coverage
npm run test:unit -- --coverage
# or: pytest --cov=src --cov-report=term-missing
# or: go test ./... -coverprofile=coverage.out

# Integration tests (if applicable locally)
npm run test:integration
```

**If any step fails, stop.** Fix the failure, re-run from the top of this section. Shipping broken tests is shipping a broken trust baseline — the next engineer can't tell if a new test failure is their fault or yours.

### 1.3 Coverage Audit

Coverage isn't a target to game — it's a signal. If you're adding a significant new path and coverage dropped, ask yourself whether the untested paths are acceptable risks.

```bash
# Check coverage against your project's threshold
npx nyc check-coverage --lines 80 --functions 80 --branches 70
# or: pytest --cov=src --cov-fail-under=80
# or: go tool cover -func=coverage.out | tail -1
```

If coverage is below threshold:
- Add tests for the new code paths you introduced, not random tests to inflate the number.
- If the uncovered path is intentionally untestable (e.g., a panic recovery branch), add a `// coverage: ignore` annotation with a comment explaining why.

### 1.4 Secrets Scan

```bash
# Scan for accidentally committed secrets before they leave your machine
git diff origin/main --name-only | xargs grep -l -E "(api_key|secret|password|token|BEGIN (RSA|EC|OPENSSH))" 2>/dev/null
# or use a dedicated tool:
trufflehog git file://. --since-commit origin/main --only-verified
# or: gitleaks detect --source . --verbose
```

If secrets are found:
1. Do NOT proceed with the PR.
2. Remove the secret from the code.
3. If the secret was ever committed (even briefly), rotate it immediately — git history is persistent and public/internal repos are leaked constantly.
4. If the secret appeared in CI logs, treat those logs as compromised and rotate too.

### 1.5 Debug Code & Temporary Scaffolding Audit

```bash
# Find debug artifacts that must not ship
git diff origin/main | grep -E "^\+" | grep -iE "(console\.log|debugger|TODO:|FIXME:|print\(|pprint\(|pp\(|binding\.pry|byebug|fmt\.Print)" | grep -v "test\|spec\|_test\.go"
```

Review every hit. Not all are blockers — a `console.log` in a test file is fine; a `console.log('SECRET VALUE:', token)` in a route handler is not. Use judgment, but don't let the grep pass unread.

### 1.6 Documentation Currency Check

- [ ] `README.md` reflects any new environment variables, setup steps, or API changes.
- [ ] `CHANGELOG.md` has an entry for this release (see Release Notes section below).
- [ ] API documentation is updated if public-facing contracts changed.
- [ ] Any architectural decision records (ADRs) created if a significant design choice was made.
- [ ] `.env.example` updated if new env vars were added.

---

## Step 2: Test Framework Bootstrapping

If the project has no test framework, or the user says "we don't have tests yet," do not skip to shipping. Bootstrap a minimal, working test harness first. A single working test is worth more than 100 tests that don't run.

### Detect What's Missing

```bash
# JavaScript/TypeScript
ls package.json && cat package.json | grep -E '"(jest|vitest|mocha|test)"'

# Python
ls pytest.ini pyproject.toml setup.cfg 2>/dev/null | head -1

# Go
ls *_test.go 2>/dev/null | head -1
```

### Bootstrap by Ecosystem

**Node.js / TypeScript — Vitest (preferred for modern projects)**

```bash
npm install -D vitest @vitest/coverage-v8

# vitest.config.ts
cat > vitest.config.ts << 'EOF'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'html'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 70,
      },
    },
  },
})
EOF

# package.json scripts
npm pkg set scripts.test="vitest run"
npm pkg set scripts.test:watch="vitest"
npm pkg set scripts.test:coverage="vitest run --coverage"
```

**Python — pytest**

```bash
pip install pytest pytest-cov pytest-asyncio

cat > pyproject.toml << 'EOF'
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
fail_under = 80
show_missing = true
EOF

mkdir -p tests
touch tests/__init__.py tests/conftest.py
```

**Go — built-in testing + testify**

```bash
go get github.com/stretchr/testify/assert
go get github.com/stretchr/testify/require

# Example test file scaffold
cat > internal/yourpackage/yourpackage_test.go << 'EOF'
package yourpackage_test

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestSomething(t *testing.T) {
    t.Run("expected behavior", func(t *testing.T) {
        result, err := SomeThing(input)
        require.NoError(t, err)
        assert.Equal(t, expected, result)
    })
}
EOF
```

Write at least one passing test for the most critical path in the codebase before proceeding to ship. If nothing critical has tests, write one for the entry point or the most frequently called function.

---

## Step 3: Commit & Push

### 3.1 Stage Changes Intentionally

```bash
# Review exactly what you're about to commit
git diff --staged

# Stage by hunk, not by file — avoid accidentally staging debug code
# that survived the audit in Step 1.5
git add -p

# Final pre-commit check
git status
```

Never use `git add .` blindly on a release commit. Review what's staged.

### 3.2 Conventional Commits Format

Every commit message must follow Conventional Commits. This is not a style preference — it's what enables automated changelog generation, semantic versioning, and legible history for the next engineer.

```
<type>(<scope>): <subject>

[optional body]

[optional footer: BREAKING CHANGE, Closes #123, etc.]
```

**Types:**

| Type | When to use |
|---|---|
| `feat` | A new feature visible to users or consumers of the API |
| `fix` | A bug fix |
| `perf` | A performance improvement with no behavior change |
| `refactor` | Code restructuring with no behavior or API change |
| `test` | Adding or fixing tests only |
| `docs` | Documentation only |
| `chore` | Build system, dependency updates, tooling |
| `ci` | CI/CD configuration changes |
| `revert` | Reverting a previous commit |

**Rules:**
- Subject line: imperative mood, lowercase, no period, ≤72 characters. `fix: handle null user on login` not `Fixed the null user bug on login.`
- Body: explain *why*, not *what*. The diff explains what. The why lives only in the commit message.
- `BREAKING CHANGE:` footer is mandatory if the commit changes a public API, env var name, DB schema in a non-backward-compatible way, or removes a previously available behavior.

```bash
# Good commits
git commit -m "feat(auth): add refresh token rotation on every use"
git commit -m "fix(payments): handle Stripe webhook timeout with idempotency key"
git commit -m "chore(deps): bump express from 4.18.1 to 4.19.2"

# With breaking change
git commit -m "feat(api)!: rename /user/profile to /users/{id}/profile

BREAKING CHANGE: All clients using the old endpoint path must update.
The old path now returns 410 Gone with a migration header."
```

### 3.3 Push

```bash
git push origin <your-branch>
# If the branch already has a remote and you rebased:
git push --force-with-lease origin <your-branch>
# --force-with-lease is safer than --force: it will refuse to push if someone
# else pushed to the branch since you last fetched, protecting against
# overwriting their work.
```

---

## Step 4: Open the Pull Request

### 4.1 PR Title

The PR title becomes the squash-merge commit message. It must follow Conventional Commits exactly.

```
feat(scope): short description of what this PR does
```

### 4.2 PR Description Template

```markdown
## What & Why

<!-- What does this PR do? One paragraph. Why does it need to exist?
     Link to the ticket/issue it closes. -->

Closes #<issue-number>

## How It Works

<!-- Brief technical description of the approach taken. Why this approach
     over the alternatives? What trade-offs were made? -->

## Testing

<!-- How was this tested? What scenarios were covered? What wasn't tested
     and why? -->

- [ ] Unit tests added / updated
- [ ] Integration tests pass locally
- [ ] Manually tested against: <!-- describe the scenario -->

## Pre-Ship Checklist

- [ ] `git rebase origin/main` — branch is current
- [ ] Lint passes (`npm run lint` / `ruff check .` / etc.)
- [ ] Tests pass with coverage above threshold
- [ ] No secrets in diff (`trufflehog` / `gitleaks` clean)
- [ ] No debug code or `console.log` in production paths
- [ ] `.env.example` updated if new env vars added
- [ ] `CHANGELOG.md` entry added
- [ ] Documentation updated if behavior changed

## Screenshots / Recordings

<!-- If this changes UI or observable behavior, show it. -->

## Rollback Plan

<!-- If this PR causes a production incident, what's the rollback?
     "Revert the PR" is acceptable if it's true. "Requires DB migration
     rollback — see runbook" is also acceptable if documented. -->
```

### 4.3 Reviewer Assignment

- Assign at least one reviewer who understands the changed domain.
- For changes touching security, auth, payments, or data persistence: require a second reviewer.
- For changes touching public APIs or breaking changes: notify downstream consumers before merging.

---

## Step 5: Land & Deploy Workflow

### 5.1 Wait for CI

Do not merge until all required CI checks pass. Green CI is a necessary condition, not a sufficient one — but a red CI is always a hard stop.

```bash
# Monitor CI from the terminal (GitHub CLI)
gh pr checks <pr-number> --watch

# Or just watch the PR page. Either way, don't merge on red.
```

If CI is flaky (tests passing on re-run without code changes), fix the flakiness before merging. Flaky CI trains engineers to ignore failures — that's how a real failure gets missed.

### 5.2 Address Review Feedback

- Respond to every comment, even if only to say "done" or "I disagree because X."
- If a review comment surfaces a design question that changes the approach, update the PR description to reflect the final approach — the PR description is the permanent record of what was decided and why.
- Re-run the full pre-ship checklist (Step 1) after making review-driven changes.

### 5.3 Merge Strategy

Choose the merge strategy that matches the project's history policy:

| Strategy | When to use |
|---|---|
| **Squash merge** | Default for most projects. One commit per PR, clean linear history, PR title becomes the commit message. |
| **Rebase merge** | When the branch commits are already clean, atomic, and individually meaningful. Preserves each commit. |
| **Merge commit** | When you need a record that a merge happened (e.g., release branch into main). Avoid for feature branches. |

```bash
# Squash merge via GitHub CLI
gh pr merge <pr-number> --squash --delete-branch

# Or via git directly
git checkout main
git merge --squash <your-branch>
git commit -m "feat(scope): your pr title here"
git push origin main
git branch -d <your-branch>
```

### 5.4 Post-Merge CI Gate

After merge, wait for the `main` branch CI to complete before assuming the deploy will succeed. Merge conflicts resolved incorrectly, or interactions between two simultaneously merged PRs, can cause a green PR to produce a red main.

```bash
gh run watch --repo <owner>/<repo>
```

### 5.5 Deploy to Production

Deployment mechanism depends on the project's CD setup. In all cases:

**GitOps (ArgoCD/Flux):**
```bash
# Update the manifest repo with the new image SHA
# ArgoCD/Flux will detect the change and sync automatically.
# Watch sync status:
argocd app get <app-name> --watch
# or: flux get kustomizations --watch
```

**Direct kubectl:**
```bash
kubectl set image deployment/<app-name> <container>=<image>:<sha> -n <namespace>
kubectl rollout status deployment/<app-name> -n <namespace>
# rollout status blocks until the new pods are healthy or the timeout elapses.
```

**Platform CLI (Heroku, Railway, Render, Fly.io):**
```bash
# Heroku
heroku releases --app <app-name>   # confirm the release is present
heroku ps --app <app-name>         # confirm dynos are running

# Fly.io
fly status --app <app-name>
fly logs --app <app-name>
```

---

## Step 6: Post-Deploy Health Verification

This step is mandatory. "Deployed" ≠ "working." A deploy that silently starts failing 2 minutes after going live is worse than a deploy that fails immediately, because by the time you notice, real users have hit real errors.

### 6.1 Immediate Verification (First 5 Minutes)

```bash
# Check error rate — this is the single most important signal
# Compare the 5-minute window after deploy to the 5-minute window before.

# Application logs
kubectl logs -l app=<app-name> -n <namespace> --tail=100 --since=5m
# or: heroku logs --tail --app <app-name>

# Health endpoint
curl -sf https://<your-domain>/health | jq .
# Expect: { "status": "ok", "version": "<sha>", "dependencies": { "db": "ok" } }

# Spot-check critical user flows
curl -sf -H "Authorization: Bearer $TEST_TOKEN" https://<your-domain>/api/users/me | jq .
```

### 6.2 Metrics Dashboard (First 15 Minutes)

Open your observability dashboard and verify:

- [ ] **Error rate** — 5xx rate is at or below pre-deploy baseline
- [ ] **Latency** — p95 and p99 latency within acceptable bounds (define these before deploying, not after)
- [ ] **Throughput** — request rate is normal (a sudden drop often means a load balancer health check failure pulling the instance from rotation)
- [ ] **Deployment marker** visible on the timeline — confirms the dashboard is showing post-deploy data
- [ ] **No new alert firings** in the alerting system

If any of these are abnormal, move immediately to the Rollback Procedure (Step 7). Do not wait to "see if it stabilizes."

### 6.3 Sustained Observation Window

For a normal release: observe for 15 minutes post-deploy before considering the release closed.
For a release touching critical paths (payments, auth, data pipelines): 30 minutes minimum.
For a major version or architectural change: 1 hour, with an on-call engineer watching.

---

## Step 7: Rollback Procedure

A rollback is not a failure. A rollback is the correct response to a production incident caused by a deploy. Executing it quickly and calmly is a mark of operational maturity.

### 7.1 Decision Threshold

Initiate rollback immediately if any of these are true within the observation window:
- Error rate exceeds 1% (or your defined SLO threshold) for more than 2 minutes
- p99 latency increases by more than 2× baseline
- Any crash loop, OOMKill, or pod restart storm
- Any alert fires that wasn't firing before the deploy
- Any critical user-facing flow is broken (login, checkout, data retrieval)

Do not wait for the incident to be "confirmed." Roll back, then investigate. It's faster to recover and do RCA than to debug under live traffic.

### 7.2 Application Rollback

**Kubernetes:**
```bash
# Roll back to the previous deployment revision (fastest)
kubectl rollout undo deployment/<app-name> -n <namespace>
kubectl rollout status deployment/<app-name> -n <namespace>

# Or roll back to a specific revision
kubectl rollout history deployment/<app-name> -n <namespace>
kubectl rollout undo deployment/<app-name> --to-revision=<N> -n <namespace>
```

**GitOps:**
```bash
# Revert the manifest change in the GitOps repo and push
git revert HEAD --no-edit
git push origin main
# The controller will reconcile automatically. Watch:
argocd app get <app-name> --watch
```

**Docker / Direct deploy:**
```bash
# Re-deploy the previous known-good image SHA
docker pull <image>:<previous-sha>
docker stop <container> && docker run -d --name <container> <image>:<previous-sha>
```

**Platform CLI:**
```bash
# Heroku
heroku rollback --app <app-name>               # rolls back one release
heroku releases --app <app-name>               # verify

# Fly.io
fly deploy --image <image>:<previous-sha> --app <app-name>
```

### 7.3 Database Rollback

Database rollbacks are the hardest part of any release. Handle them carefully:

- If the migration added a nullable column or a new index: rolling back the app code is usually sufficient — the column stays but is ignored.
- If the migration renamed or removed a column: you need to run the down migration AND ensure no in-flight requests are using the old column during the transition.
- If the migration changed data (a data migration): rollback may be impossible without a restore from backup. This is why data migrations should be idempotent and run in separate, independently reversible steps.

```bash
# Run the down migration (schema rollback)
# Django
python manage.py migrate <app> <previous-migration-name>

# Alembic
alembic downgrade -1

# Flyway
flyway undo

# Prisma — requires shadow database or manual SQL
# There is no built-in down migration in Prisma. Write reverse SQL.
```

**Golden rule:** Never run a database migration that cannot be cleanly reversed without a full restore, unless you have a tested restore procedure and a maintenance window.

### 7.4 Post-Rollback

1. Verify production is healthy using the same checks in Step 6.
2. Communicate status: post a message in your incident channel that the rollback is complete and the system is stable.
3. Open a post-mortem ticket: what failed, when, how it was detected, and what the fix will be before the next ship attempt.
4. Do not re-attempt the release until the root cause is understood and fixed.

---

## Step 8: Release Notes Generation

Release notes are written for two audiences: engineers (what changed technically) and users/stakeholders (what changed for them). Don't conflate them.

### 8.1 CHANGELOG.md — Engineer-Facing

Format: [Keep a Changelog](https://keepachangelog.com) — sections by type under a version header.

```markdown
## [1.4.0] — 2026-07-22

### Added
- Refresh token rotation on every use — improves session security for all users.
- `GET /users/{id}/profile` endpoint replacing the deprecated `/user/profile`.

### Fixed
- Stripe webhook timeout now handled correctly with idempotency key, preventing
  duplicate charge processing under high load.
- Null pointer on login when user record has no associated OAuth provider.

### Changed
- Upgraded `express` from 4.18.1 to 4.19.2 (security patch).

### Deprecated
- `GET /user/profile` — returns 301 to new path. Will be removed in v2.0.

### Breaking Changes
- None in this release.

## [1.3.2] — 2026-07-10
...
```

### 8.2 Automated from Git Log

```bash
# Generate a draft CHANGELOG entry from commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD \
  --pretty=format:"- %s (%h)" \
  --no-merges \
  | grep -E "^- (feat|fix|perf|refactor|docs|chore|ci)(\(.*\))?:" \
  | sort

# Or use a tool
npx conventional-changelog-cli -p angular -i CHANGELOG.md -s
# or: git-cliff --tag v1.4.0 --output CHANGELOG.md
```

Review and edit the generated draft. Automated tools get the structure right; the human adds the "why this matters" context.

### 8.3 User-Facing Release Notes

For user-visible releases (public APIs, customer-facing products):

```markdown
# Release Notes — v1.4.0 (July 22, 2026)

## What's New
**Improved session security** — sessions now automatically rotate tokens on
each use, reducing the window of exposure if a token is ever intercepted.

## Bug Fixes
**Duplicate charge prevention** — a rare edge case where a slow network
could cause a payment to be processed twice has been resolved.

## Deprecation Notice
The `/user/profile` endpoint is deprecated and will be removed in v2.0.
Please migrate to `/users/{id}/profile`. Both endpoints return the same data
during the transition period.
```

---

## Step 9: Hotfix Path

A hotfix is a release that bypasses the normal release queue because production is broken now.

### 9.1 Hotfix Branch

```bash
# Branch from the current production tag, not from main
# (main may have unreleased work that shouldn't go to production)
git fetch --tags
git checkout -b hotfix/<ticket-id>-<brief-description> v<current-production-version>
# Example: git checkout -b hotfix/INC-4421-null-user-crash v1.3.2
```

If `main` and the production tag are the same commit (i.e., everything merged to main is deployed), you can branch from `main` directly.

### 9.2 Hotfix Development

Apply the minimum change to fix the production issue. This is not the time to refactor, clean up, or add features. Every additional change is additional risk and additional review surface.

```bash
# Make the fix
git add -p
git commit -m "fix(auth): prevent null pointer when user has no OAuth provider

Closes #INC-4421. The login handler was not checking for a nil OAuthProvider
record before dereferencing it. Added nil guard and falling back to password
auth. Affects users who signed up via email/password and never connected OAuth."
```

### 9.3 Fast-Track Review

- Assign your most senior available reviewer.
- Describe the production impact (who is affected, how severely, since when) in the PR description.
- Minimum one approval required — do not merge unreviewed, even in an emergency.
- The pre-ship checklist still applies, but run it in parallel with review rather than sequentially.

### 9.4 Deploy Hotfix

Follow the standard deploy and verification steps (Steps 5–6). A rushed verification on a hotfix is how you turn one incident into two.

### 9.5 Backport to Main

After the hotfix is verified in production:

```bash
# Cherry-pick the fix commit onto main
git checkout main
git cherry-pick <hotfix-commit-sha>
git push origin main
# Open a minimal PR if your branch protection rules require it.
```

This ensures the fix isn't regressed by the next normal release.

### 9.6 Hotfix Release Notes

Tag the hotfix release:

```bash
git tag -a v1.3.3 -m "Hotfix: prevent null pointer on login for email/password users"
git push origin v1.3.3
```

Add a CHANGELOG entry:

```markdown
## [1.3.3] — 2026-07-22

### Fixed
- **CRITICAL:** Null pointer crash on login for users without a linked OAuth
  provider. Affected email/password-only accounts since v1.3.0 under certain
  load conditions. (INC-4421)
```

---

## Definition of Done — Release

A release is complete when every item here is checked. Not "CI is green." Not "PR is merged." Every item.

### Code Quality
- [ ] Branch rebased on `origin/main` — no stale base, no merge noise in the diff
- [ ] Lint passes with zero warnings in production-scope files
- [ ] Type check passes (no `any` suppressions added without a comment)
- [ ] All tests pass locally and in CI
- [ ] Coverage at or above the project threshold — any drop is explained and justified
- [ ] No secrets in the diff (`gitleaks` or `trufflehog` clean)
- [ ] No debug code, `console.log`, `debugger`, `print()`, `pry`, or equivalent in production paths
- [ ] No `TODO` or `FIXME` comments that block this release (existing ones are acceptable, new ones that block the feature are not)

### Process & Documentation
- [ ] PR description filled out — what, why, how, testing notes, rollback plan
- [ ] At least one approval from a reviewer who understands the changed domain
- [ ] `CHANGELOG.md` entry added with the correct version and date
- [ ] `.env.example` updated if new environment variables added
- [ ] API documentation updated if public contracts changed
- [ ] README updated if setup, configuration, or architecture changed materially

### Deployment & Verification
- [ ] CI is green on `main` after merge — not just on the PR branch
- [ ] Deploy initiated and confirmed (correct SHA/image visible in target environment)
- [ ] Health endpoint returns `200 OK` with expected version
- [ ] Error rate baseline unchanged for 15 minutes post-deploy (30 minutes for critical paths)
- [ ] p95/p99 latency within acceptable bounds for 15 minutes post-deploy
- [ ] No new alerts firing in the alerting system
- [ ] Deployment marker visible on observability dashboards

### Release Artifacts
- [ ] Git tag created for versioned releases (`git tag -a v<version> -m "..."`)
- [ ] Tag pushed to origin (`git push origin v<version>`)
- [ ] Release notes published (GitHub Releases, internal wiki, or equivalent)
- [ ] Hotfix commits cherry-picked to `main` if applicable

### Operational Readiness
- [ ] Rollback procedure is documented and has been verified to work (at minimum, you know what the previous image SHA was and how to re-deploy it)
- [ ] On-call engineer aware of the release if it touches a critical path
- [ ] Any dependent teams notified of breaking changes before the release went live — not after
