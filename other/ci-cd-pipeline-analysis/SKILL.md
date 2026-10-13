---
name: ci-cd-pipeline-analysis
description: Analyze and improve CI/CD pipelines across GitHub Actions, Jenkins, and TeamCity. Diagnose slow builds, flaky tests, and deployment failures. Prioritize MCP-based agent access when available; fall back to REST API with personal access tokens. Grounded in DORA metrics for delivery performance.
triggers:
  - "pipeline is slow"
  - "build failing"
  - "flaky tests in CI"
  - "deployment failing"
  - "improve CI/CD"
  - "analyze pipeline"
  - "why is the build broken"
  - "Jenkins pipeline"
  - "TeamCity build"
  - "GitHub Actions workflow"
audience:
  - engineer
  - manager
---

# CI/CD Pipeline Analysis

Diagnose, analyze, and improve your CI/CD pipelines — with MCP agent access where available, PAT-based API access as fallback.

---

## Agent Access Strategy

### Option A: MCP-First (GitHub Actions)

If your AI agent has an MCP server connected to GitHub, use native tool calls — no tokens needed:

```
# With GitHub MCP server connected, an agent can:
- list_workflow_runs: See recent pipeline runs and their status
- get_workflow_job: Inspect individual job steps, timings, exit codes
- get_job_logs: Retrieve full logs for failed jobs
- list_workflow_run_artifacts: Access build artifacts and test reports
```

**When to use**: Claude Code with `github-mcp-server` configured, or GitHub Copilot CLI with MCP access.

**Prompt pattern**:
```
Using the GitHub MCP tools, analyze the last 10 workflow runs for 
the [workflow name] pipeline on branch [main/release].
Identify: failure patterns, slowest jobs, flakiness rate.
Summarize findings and suggest top 3 improvements.
```

---

### Option B: PAT-Based REST API (GitHub, Jenkins, TeamCity)

When MCP is not available, authenticate with a Personal Access Token and call the REST API.

#### GitHub Actions via API
```bash
# Required PAT scopes: repo, actions:read
export GH_TOKEN="your_token"

# List recent workflow runs
gh run list --workflow=ci.yml --limit=20 --json status,conclusion,createdAt,databaseId

# Get failed run logs
gh run view [run-id] --log-failed

# Job timing breakdown
curl -H "Authorization: Bearer $GH_TOKEN" \
  "https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/jobs" \
  | jq '.jobs[] | {name, conclusion, started_at, completed_at}'
```

#### Jenkins via REST API
```bash
# Required: API token from Jenkins user settings
export JENKINS_TOKEN="your_token"
export JENKINS_URL="https://jenkins.yourcompany.com"

# Last 10 builds for a job
curl -u "user:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/{pipeline-name}/api/json?tree=builds[number,result,timestamp,duration]{0,10}"

# Console output for a specific build
curl -u "user:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/{pipeline-name}/{build-number}/consoleText"

# Pipeline stages timing
curl -u "user:$JENKINS_TOKEN" \
  "$JENKINS_URL/job/{pipeline-name}/{build-number}/wfapi/describe"
```

#### TeamCity via REST API
```bash
# Required: Access token from TeamCity user profile
export TC_TOKEN="your_token"
export TC_URL="https://teamcity.yourcompany.com"

# Recent builds for a build type
curl -H "Authorization: Bearer $TC_TOKEN" \
  -H "Accept: application/json" \
  "$TC_URL/app/rest/builds?locator=buildType:{buildTypeId},count:10"

# Build log
curl -H "Authorization: Bearer $TC_TOKEN" \
  "$TC_URL/app/rest/builds/{buildId}/log"

# Test failures in a build
curl -H "Authorization: Bearer $TC_TOKEN" \
  -H "Accept: application/json" \
  "$TC_URL/app/rest/testOccurrences?locator=build:{buildId},status:FAILURE"
```

---

## Pipeline Diagnostic Checklist

### Failure Analysis
```
1. What is the failure rate over the last 30 days?
   - < 5%: 🟢 Healthy
   - 5-15%: 🟡 Investigate
   - > 15%: 🔴 Unreliable pipeline — engineers working around it

2. Are failures deterministic or flaky?
   - Deterministic: Same test/step fails every time → real bug or broken environment
   - Flaky: Fails < 50% of runs on same code → timing, network, test isolation issue

3. Which stage/job fails most often?
   [ ] Build / compile
   [ ] Unit tests
   [ ] Integration tests
   [ ] Security scan
   [ ] Deployment step

4. Is the failure new (regression) or long-standing?
```

### Performance Analysis
```
Total pipeline duration trend:
  - Measure p50 and p95 build time over last 30 days
  - p95 > 3× p50 = high variance (flakiness or resource contention)

Stage breakdown:
| Stage | Avg Duration | % of Total | Parallelizable? |
|---|---|---|---|
| Checkout | | | No |
| Dependencies install | | | Partial (cache) |
| Build/compile | | | Yes |
| Unit tests | | | Yes |
| Integration tests | | | Partial |
| Security scan | | | Yes |
| Deploy | | | No |

Target total pipeline time by stage:
  - PR validation: < 10 min (engineers waiting)
  - Merge to main: < 20 min
  - Deploy to prod: < 30 min total from merge
```

---

## Common Pipeline Problems & Fixes

### Slow Builds

| Problem | Diagnosis | Fix |
|---|---|---|
| No dependency caching | Cache miss on every run | Cache `node_modules`, `.gradle`, pip packages by lockfile hash |
| Sequential jobs that could parallelize | One long chain of steps | Split into parallel jobs; merge artifacts after |
| Large Docker image builds | Build time > 5 min | Multi-stage Dockerfile; cache FROM layers; use BuildKit |
| Test suite runs serially | 1000 tests × 100ms = 100 sec | Shard tests across parallel runners |
| Artifact upload/download | Transfer of large files | Use build cache instead of artifacts for intermediate steps |

### Flaky Tests

| Pattern | Likely Cause | Fix |
|---|---|---|
| Fails on timing | Async waits too short | Use explicit waits/polling instead of `sleep` |
| Fails on shared state | Tests share DB/files | Isolate: separate DB per test or truncate between runs |
| Fails on external calls | HTTP calls to real services | Mock external dependencies in CI |
| Fails under load | Resource contention on shared runners | Reserve dedicated runner for integration tests |
| Passes locally, fails in CI | Environment difference | Containerize test environment; use same image locally and in CI |

### Deployment Failures

| Problem | Fix |
|---|---|
| Deploy fails after successful tests | Environment parity — staging ≠ prod config | Infrastructure as Code; config drift detection |
| Rollback not tested | Test rollback in staging regularly | Add rollback smoke test to pipeline |
| No deployment observability | Can't tell if deploy succeeded | Add post-deploy health check job (ping /health, check error rate) |
| Manual approval gates delay | Engineers waiting for humans | Auto-approve to staging; require approval only for prod |

---

## DORA Metrics from Pipeline Data

Extract DORA metrics directly from your CI/CD system:

```
Deployment Frequency:
  Count deploys to production per day/week from pipeline logs
  Elite: Multiple times per day
  High: Once per day to once per week

Lead Time for Changes:
  Time from first commit to production deployment
  Measure: git commit timestamp → successful prod deploy timestamp
  Elite: < 1 hour | High: 1 day | Medium: 1 week

Change Failure Rate:
  (deployments that caused incidents / total deployments) × 100
  Elite: 0-5% | High: 5-10%

Mean Time to Recovery (MTTR):
  Time from incident detection to service restored
  Extract from incident tracker or on-call tool
  Elite: < 1 hour | High: < 1 day
```

**Prompt for agent analysis**:
```
Using the last 90 days of pipeline run data, calculate:
1. Deployment frequency (deploys/week to main/production branch)
2. p50 lead time from first commit on a PR to successful production deploy
3. Change failure rate (% of deploys followed by a rollback or hotfix within 24h)
Report current tier (Elite/High/Medium/Low) for each DORA metric.
```

---

## Output: Pipeline Health Report

```markdown
## CI/CD Pipeline Health: [Pipeline Name]
**Date**: [date]  
**Data range**: last [N] days  
**Tool**: [GitHub Actions / Jenkins / TeamCity]

### Summary

| Metric | Current | Target | Status |
|---|---|---|---|
| Failure rate | X% | < 5% | 🟢/🟡/🔴 |
| p50 build time | X min | < 10 min (PR) | |
| p95 build time | X min | < 20 min | |
| Flaky test rate | X% | < 2% | |
| Deployment frequency | X/week | [DORA target] | |
| Lead time | X hours | [DORA target] | |

### Top Issues
1. [Most impactful problem + root cause]
2. [Second issue]
3. [Third issue]

### Recommendations
| Action | Estimated Improvement | Effort |
|---|---|---|
| [fix] | [X min saved / X% failure reduction] | [S/M/L] |
```

---

## References
- DORA: [State of DevOps Report](https://dora.dev)
- Martin Fowler: [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
- Martin Fowler: [Continuous Delivery](https://martinfowler.com/bliki/ContinuousDelivery.html)
- Google SRE Book: [Release Engineering](https://sre.google/sre-book/release-engineering/)
