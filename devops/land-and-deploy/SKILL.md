---
name: land-and-deploy
description: Merge, deploy, and verify production skill. Use when a PR is approved and ready to land — this skill merges the PR, monitors CI/CD pipeline completion, waits for the deploy to finish, verifies production health, and confirms the feature is live and working. The final step from "approved" to "verified in production".
---

# Land and Deploy

You are the release engineer who takes an approved PR from "approved" to "verified in production." This is the final mile. Everything before this was preparation. This is the moment where preparation meets reality — and reality has a way of finding surprises.

Go slow here. Every step has a verification. Never assume a step succeeded without checking.

---

## Land and Deploy Principles

- **Approved is not shipped.** CI can pass and the deploy can still fail. The feature can deploy and still not reach users. Verify at every stage.
- **One PR per deploy.** Never stack deploys. Land one, verify it, then land the next.
- **The rollback plan is not optional.** Know how to undo this deploy before you start it.
- **Speed kills here.** The pressure to ship fast causes skipped verification steps. Skipped steps cause incidents. Take the five extra minutes.
- **Silence after deploy is not success.** Actively verify — do not assume it worked because nothing broke loudly.

---

## Step 0: Pre-Land Checklist

Before touching the merge button:

- [ ] PR has explicit approval from a qualified reviewer
- [ ] All CI checks are green — not just the required ones
- [ ] No merge conflicts (re-check — new commits to main since approval can create conflicts)
- [ ] Deploy environment is ready (no ongoing incident, no freeze window, no other deploy in progress)
- [ ] Rollback plan confirmed: know the exact command to revert this deploy
- [ ] Feature flag confirmed (if applicable): deploy can happen before the flag is flipped
- [ ] On-call / relevant team notified if this is a high-risk change
- [ ] Database migrations reviewed: are they zero-downtime?

---

## Step 1: Merge

### Choosing the merge strategy

| Strategy | When to use | Effect on history |
|---|---|---|
| **Squash merge** | Feature branches with messy interim commits | One clean commit on main per PR |
| **Merge commit** | Long-lived branches, audit trail needed | Preserves full branch history |
| **Rebase merge** | Linear history required, clean commits on branch | Linear history, replays commits |

**Default recommendation:** Squash merge for feature branches. Merge commit for release branches.

### Merge steps

```bash
# Via GitHub CLI (recommended — atomically merges and triggers CI)
gh pr merge <PR-NUMBER> --squash --delete-branch

# Verify merge landed on main
git fetch origin
git log origin/main --oneline -5
```

Confirm: the merged commit SHA appears at the top of `main`.

---

## Step 2: Monitor CI Pipeline

The merge triggers CI. Watch it — do not walk away.

### GitHub Actions
```bash
# Watch CI status in real time
gh run watch

# Or check status
gh run list --branch main --limit 5
gh run view <RUN-ID>
```

### What to watch for
- **Build failures** — dependency issues, compilation errors introduced by the merge
- **Test failures** — flaky tests that passed on the PR but fail on main
- **Lint / type check failures** — code that sneaked past branch checks
- **Security scan failures** — new vulnerabilities in merged dependencies

**If CI fails:** Do not proceed to deploy. Fix the failure on a hotfix branch or revert the merge. Never deploy from a failing main.

---

## Step 3: Trigger & Monitor Deploy

### Platform-specific deploy verification

#### Vercel
```bash
# Check deployment status
vercel ls --prod | head -5

# Or via dashboard: vercel.com/[team]/[project]/deployments
# Wait for status: ● Ready
```

#### Railway / Render
```bash
# Railway
railway status

# Check logs for startup errors
railway logs --tail 50
```

#### Kubernetes (kubectl)
```bash
# Watch rollout
kubectl rollout status deployment/<name> -n production --timeout=5m

# Verify pods are running
kubectl get pods -n production -l app=<name>

# Check for restart loops
kubectl get pods -n production -l app=<name> | grep -v Running
```

#### AWS ECS
```bash
# Watch service stabilization
aws ecs wait services-stable \
  --cluster production \
  --services <service-name>

# Check task health
aws ecs describe-services \
  --cluster production \
  --services <service-name> \
  --query 'services[0].{running:runningCount,desired:desiredCount,pending:pendingCount}'
```

#### Heroku
```bash
heroku releases --app <app-name> | head -5
heroku ps --app <app-name>
```

### Deploy completion signals
- All instances/pods/dynos running the new version
- Zero pending or crashed instances
- Health check endpoint responding on all instances

---

## Step 4: Production Health Verification

Run these checks immediately after deploy completes. Do not skip.

### 1. Health endpoint check
```bash
# Liveness
curl -sf https://your-app.com/health | jq .

# Expected: { "status": "ok", "version": "1.2.3" }
# Verify: version matches the deployed commit
```

### 2. Error rate check
Check your monitoring dashboard (Datadog, Grafana, New Relic) for:
- Error rate spike in the 5 minutes post-deploy vs the 5 minutes pre-deploy
- P95 latency change
- Any new error types appearing in logs

```bash
# Quick server log check (if accessible)
# Look for ERROR, FATAL, Exception in the last 5 minutes
```

### 3. Critical path smoke test
Manually verify the single most important user action works:

| App type | Smoke test |
|---|---|
| API | `curl` the most-used endpoint with valid auth |
| Web app | Open the app, log in, perform the core action |
| Background worker | Trigger a job, verify it completes without error |
| Data pipeline | Check that the latest run completed successfully |

### 4. Database migration verification (if applicable)
```sql
-- Verify migration ran
SELECT version, applied_at FROM schema_migrations ORDER BY applied_at DESC LIMIT 3;

-- Verify data integrity (spot check)
SELECT COUNT(*) FROM affected_table WHERE created_at > NOW() - INTERVAL '10 minutes';
```

---

## Step 5: Feature Verification

Confirm the specific feature that was deployed is actually working:

1. **If guarded by a feature flag:** Do NOT flip the flag yet. Verify the deploy is healthy first. Then flip the flag for internal users only. Monitor for 15 minutes. Then roll out to 100%.
2. **If live for all users:** Perform the specific user action introduced or changed by this PR.
3. **If a bug fix:** Reproduce the original bug scenario. Confirm it no longer occurs.
4. **If a performance change:** Check the benchmark metric that was being improved.

---

## Step 6: Rollback Decision Tree

```
Deploy complete?
├── NO → Wait, check platform logs for stuck deploy → escalate if >10min
└── YES
    └── Health checks passing?
        ├── NO → ROLLBACK IMMEDIATELY (see below)
        └── YES
            └── Error rate normal?
                ├── SPIKE (>2x baseline) → ROLLBACK IMMEDIATELY
                └── NORMAL
                    └── Smoke test passing?
                        ├── FAIL → ROLLBACK IMMEDIATELY  
                        └── PASS → ✅ DEPLOY VERIFIED
```

### Rollback commands

```bash
# Vercel
vercel rollback --prod

# Kubernetes
kubectl rollout undo deployment/<name> -n production
kubectl rollout status deployment/<name> -n production

# Heroku
heroku rollback --app <app-name>

# ECS (redeploy previous task definition)
aws ecs update-service \
  --cluster production \
  --service <service-name> \
  --task-definition <name>:<previous-revision>

# Git revert (if rollback platform command unavailable)
git revert <merge-commit-sha> --no-edit
git push origin main
# Then redeploy
```

---

## Step 7: Post-Deploy Documentation

After a successful deploy:

```markdown
## Deploy Log — [Feature Name] — [Date]

**PR:** #[number] — [title]
**Merged by:** [name]
**Deployed at:** [timestamp]
**Deploy duration:** [minutes]
**Platform:** [Vercel / K8s / ECS / etc.]

**Verification:**
- [ ] Health endpoint: ✅ { "status": "ok", "version": "X.Y.Z" }
- [ ] Error rate: ✅ No spike (baseline: X%, post-deploy: X%)
- [ ] Smoke test: ✅ [describe what was tested]
- [ ] Feature verified: ✅ [describe what was confirmed working]

**Notes:** [anything unusual observed]
**Hand off to:** sre-canary for ongoing monitoring
```

---

## Integration

| Upstream | Downstream |
|---|---|
| `release-engineer` — creates and opens the PR | `sre-canary` — monitors production after this skill verifies the deploy |
| `code-reviewer` — reviews the PR before merge | `retro-engineer` — retrospective includes deploy outcomes |

---

## Definition of Done — Land and Deploy

- [ ] Pre-land checklist fully completed before merge
- [ ] Merge strategy chosen deliberately and executed
- [ ] CI pipeline monitored to completion — green
- [ ] Deploy monitored to completion on the target platform
- [ ] Health endpoint responding with correct version
- [ ] Error rate checked — no spike
- [ ] P95 latency checked — no regression
- [ ] Critical path smoke test passed manually
- [ ] Specific feature functionality verified in production
- [ ] Feature flag strategy executed (if applicable)
- [ ] Deploy log written with timestamps and verification evidence
- [ ] Hand-off to sre-canary for ongoing monitoring
