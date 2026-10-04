---
name: pipeline-deploy
version: 1.0.0
description: "Safe deploy pipeline — pre-deploy security and ops checks, baseline capture, deploy, post-deploy canary and benchmark verification. Chains security-critique, operations-critique, canary, benchmark, and railway-deploy/vercel-deploy into a verified deployment workflow."
---

# Pipeline: Safe Deploy

You are orchestrating a safe deployment pipeline. Every deploy is preceded by security checks, baseline capture, and followed by canary monitoring and performance benchmarking.

## Input Parameters

Collect before starting:

- **target**: `railway` | `vercel` (required)
- **production-url**: The live production URL to monitor (required for baseline/canary/benchmark)
- **environment**: `production` | `staging` (default: `production`)

## Pipeline State

Create a tracker at `.gstack/pipeline-deploy-{date}.md`.

```markdown
## Pipeline: Safe Deploy
Started: {timestamp}
Target: {target}
URL: {production-url}
Environment: {environment}

| # | Stage | Status | Gate | Notes |
|---|-------|--------|------|-------|
| 1 | PRE-DEPLOY | pending | — | — |
| 2 | BASELINE | pending | — | — |
| 3 | DEPLOY | pending | — | — |
| 4 | VERIFY | pending | — | — |
| 5 | REPORT | pending | — | — |
```

---

## Stage 1: PRE-DEPLOY CHECKS (parallel)

Run security and operations critiques as parallel subagents:

### 1a: Security check
Dispatch a subagent to invoke `/security-critique` on the current branch diff:
- Focus on: secrets exposure, auth changes, new API endpoints, dependency vulnerabilities
- Scope: only changed files (`git diff main...HEAD --name-only`)

### 1b: Operations check
Dispatch a subagent to invoke `/operations-critique`:
- Focus on: Dockerfile changes, CI/CD pipeline changes, infra config changes, env var changes
- Scope: only changed infra files

**Gate:** No **Critical** findings from either critique. High findings are warnings (noted but not blocking).

If Critical findings exist:
1. Report them to the user
2. Ask: "Critical issues found. Deploy anyway? (yes/no)"
3. If no → STOP pipeline, update tracker → BLOCKED
4. If yes → note the override in tracker, proceed

**On pass:** Update tracker → PASS.

---

## Stage 2: BASELINE CAPTURE (parallel)

Capture the current production state before deploying:

### 2a: Canary baseline
Invoke `/canary --baseline {production-url}` to capture:
- Console error count per page
- Page load times
- Screenshots of key pages

### 2b: Performance baseline
Invoke `/benchmark --baseline {production-url}` to capture:
- Core Web Vitals (LCP, FID, CLS)
- Resource sizes and counts
- Load time per page

Both run as parallel subagents. Their outputs are saved to `.gstack/canary-reports/baselines/` and `.gstack/benchmark-reports/baselines/`.

**Gate:** Baselines captured successfully. If production URL is unreachable, warn user and ask whether to skip baselines.

---

## Stage 3: DEPLOY

Based on the target:

### Railway
Invoke `/railway-deploy`:
- Links project if not linked
- Sets environment variables from `.env` or `.env.example`
- Runs `--dry-run` before applying
- Triggers build
- Waits for deployment to complete
- Runs HTTP health check on the production URL

### Vercel
Invoke `/vercel-deploy`:
- Links project if not linked
- Configures environment variables
- Deploys (preview or production based on environment parameter)
- Waits for deployment to complete

**Gate:** Deployment successful. Health check passes (HTTP 200 on production URL).

If deployment fails:
1. Report the error and deployment logs
2. Update tracker → BLOCKED
3. Do NOT proceed to verification — the old version is still live

**On pass:** Wait 30 seconds for the deployment to stabilize, then proceed.

---

## Stage 4: VERIFY (parallel)

Run post-deploy verification as parallel subagents:

### 4a: Canary monitoring
Invoke `/canary {production-url} --duration 5m`:
- Monitors for new console errors
- Checks page load times against baseline
- Takes periodic screenshots
- Reports: HEALTHY / DEGRADED / BROKEN

### 4b: Performance benchmark
Invoke `/benchmark {production-url} --diff`:
- Compares current metrics against Stage 2 baseline
- Reports: regressions, improvements, unchanged

**Gate:**
- Canary verdict must be **HEALTHY**. DEGRADED triggers a warning. BROKEN triggers rollback discussion.
- Benchmark must show no **REGRESSION** (>50% slower or >500ms absolute increase).

If BROKEN or REGRESSION:
1. Report the specific failures with evidence
2. Ask: "Rollback to previous version? (yes/no/monitor-longer)"
3. If rollback → provide the rollback command but do NOT execute without user confirmation
4. If monitor-longer → re-run canary with --duration 10m

---

## Stage 5: REPORT

Produce the deploy report:

```markdown
## Deploy Report
Target: {target}
URL: {production-url}
Environment: {environment}
Date: {timestamp}

### Pre-Deploy
- Security: {grade} — {critical/high/medium/low counts}
- Operations: {grade} — {critical/high/medium/low counts}
- Overrides: {any critical findings overridden}

### Deployment
- Status: {SUCCESS/FAILED}
- Build time: {duration}
- Health check: {HTTP status}

### Post-Deploy Verification
- Canary: {HEALTHY/DEGRADED/BROKEN}
  - Console errors: {baseline} → {current}
  - Load time: {baseline} → {current}
- Benchmark: {PASS/WARNING/REGRESSION}
  - LCP: {baseline} → {current}
  - CLS: {baseline} → {current}

### Before/After Screenshots
{links to canary screenshots}
```

### Persist
- Save report to `.gstack/deploy-reports/deploy-{target}-{date}.md`
- Invoke `/obsidian-vault` to persist deploy record (background)

---

## Final Pipeline Report

```markdown
## Pipeline Report: Safe Deploy
Target: {target} | URL: {production-url}
Run: {timestamp}
Duration: {total elapsed}

| # | Stage | Skill(s) | Result | Gate | Duration |
|---|-------|----------|--------|------|----------|
| 1 | PRE-DEPLOY | security-critique, operations-critique | {result} | {gate} | {time} |
| 2 | BASELINE | canary, benchmark | {result} | Captured | {time} |
| 3 | DEPLOY | {deploy skill} | {result} | HTTP {status} | {time} |
| 4 | VERIFY | canary, benchmark | {result} | {verdict} | {time} |
| 5 | REPORT | — | PASS | Saved | {time} |

Overall: {PASS / PASS_WITH_WARNINGS / BLOCKED / ROLLBACK_RECOMMENDED}
```
