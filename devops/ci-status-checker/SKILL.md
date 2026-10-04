---
license: Apache-2.0
name: ci-status-checker
description: |
  Interprets GitHub Actions run status and logs, diagnoses CI failure patterns, and suggests targeted fixes. Handles dependency install failures, test timeouts, build OOM, flaky tests, and workflow misconfigurations. Activate on: 'CI failing', 'build broken', 'workflow error', 'GitHub Actions debug', 'flaky CI', 'pipeline timeout', 'CI red'. NOT for: writing new workflows from scratch (use github-actions-pipeline-builder), CI caching strategy (use ci-cache-optimizer), deployment orchestration (use devops-automator).
category: DevOps & Infrastructure
tags:
  - ci
  - github-actions
  - debugging
  - workflow
  - automation
allowed-tools:
  - Read
  - Bash(*)
  - Glob
  - Grep
  - Write
  - Edit
pairs-with:
  - skill: github-actions-pipeline-builder
    reason: Builder creates workflows, this skill diagnoses when they break
  - skill: ci-cache-optimizer
    reason: Many CI failures stem from cache misses or stale caches
  - skill: test-automation-expert
    reason: Flaky test diagnosis often requires test framework expertise
---

# CI Status Checker

Diagnoses CI/CD pipeline failures by reading GitHub Actions logs, identifying failure patterns, and producing actionable fix recommendations. This skill does not write workflows from scratch -- it triages what went wrong with existing ones.

## Activation Triggers

**Activate on:** "CI failing", "build broken", "workflow error", "GitHub Actions debug", "flaky CI", "pipeline timeout", "CI red", "actions run failed", "check failed on PR", "why is CI broken"

**NOT for:** Writing new workflows --> `github-actions-pipeline-builder` | Caching strategy --> `ci-cache-optimizer` | Deployment pipelines --> `devops-automator` | Performance testing --> `performance-profiler`

## Core Capabilities

- Read GitHub Actions run logs and extract the failing step with surrounding context
- Classify failures into known categories (dependency, build, test, timeout, OOM, permissions, config)
- Suggest targeted fixes based on error pattern matching against known CI failure modes
- Detect workflow YAML syntax and configuration issues before they cause runtime failures
- Identify flaky tests by analyzing pass/fail patterns across recent runs
- Check for common misconfigurations: wrong Node version, missing secrets, incorrect paths
- Diagnose matrix build failures where only specific combinations fail
- Trace failure cascades (step A fails silently, step B fails loudly because of A)

## Diagnostic Process

### Step 1: Get Run Status

```bash
# Check most recent run status
gh run list --limit 5

# Get details for a specific failed run
gh run view <run-id>

# Get the full log for a failed run
gh run view <run-id> --log-failed
```

Always start with `--log-failed` rather than `--log` to avoid pulling megabytes of passing step output. Only escalate to full logs if the failed step output is insufficient.

### Step 2: Identify the Failing Step

Parse the log output to find the first step that failed. CI logs contain noise -- focus on:

1. The step name that shows a red X
2. The last 50 lines of that step's output
3. The exit code (non-zero)
4. Any `##[error]` annotations

### Step 3: Classify the Failure

## Failure Classification Guide

### Category 1: Dependency Installation Failures

**Signals:**
- `npm ERR!` or `yarn error` in install step
- `ERESOLVE unable to resolve dependency tree`
- `404 Not Found` for a package
- `ENOENT` for lockfile
- `pip install` failures with version conflicts
- `Could not find a version that satisfies the requirement`

**Common causes and fixes:**

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `ERESOLVE` peer dependency conflict | Incompatible package versions | `npm install --legacy-peer-deps` or fix version constraints |
| `404 Not Found` for package | Package unpublished or registry down | Check npm status, pin working version |
| `ENOENT package-lock.json` | Lockfile not committed | Commit lockfile, or use `npm install` instead of `npm ci` |
| `engine "node"` incompatible | Wrong Node version in CI | Match `node-version` in workflow to `engines` in package.json |
| `ENOMEM` during install | Runner out of memory | Use larger runner or reduce parallelism |
| `ETARGET` no matching version | Version range resolves to nothing | Pin specific version, check if package was yanked |

### Category 2: Build Failures

**Signals:**
- TypeScript errors: `TS2304`, `TS2339`, `TS2345`, etc.
- `Module not found` or `Cannot find module`
- `SyntaxError: Unexpected token`
- Build step exits non-zero

**Common causes and fixes:**

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `TS2307: Cannot find module` | Missing type declarations | Install `@types/*` package or add to `tsconfig.json` paths |
| `TS2345: Argument of type` | Type mismatch introduced in PR | Fix the type error in source code |
| `Module not found: 'X'` | Import path wrong or package missing | Check import paths, verify package in dependencies |
| `JavaScript heap out of memory` | Build exceeds Node memory limit | Add `NODE_OPTIONS=--max-old-space-size=4096` to env |
| `SIGKILL` during build | OOM killer terminated process | Use larger runner (`ubuntu-latest-4-cores`) or optimize build |

### Category 3: Test Failures

**Signals:**
- Test runner reports failures with assertion messages
- `FAIL` markers in Jest/Vitest output
- `Expected X but received Y`
- Test timeout exceeded

**Common causes and fixes:**

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| Assertion failure with clear diff | Real bug introduced in PR | Fix the code (not the test, unless test is wrong) |
| `Timeout` on async test | Missing await or slow operation | Add proper await, increase timeout, or mock slow calls |
| `ECONNREFUSED` in test | Test needs running service | Use service containers or mock the dependency |
| Snapshot mismatch | Intentional UI change | Update snapshots with `--update-snapshot` if change is correct |
| Different results on CI vs local | Environment difference | Check timezone, locale, file ordering, parallelism |

### Category 4: Timeout Failures

**Signals:**
- `The job running on runner ... has exceeded the maximum execution time`
- Step shows no output for extended period then dies
- `##[error]The operation was canceled`

**Common causes and fixes:**

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| Job timeout (6h default) | Infinite loop or hung process | Set explicit `timeout-minutes` per job, investigate hang |
| Step hangs with no output | Interactive prompt waiting for input | Add `-y` or `--yes` flags, pipe `yes`, set `CI=true` env |
| E2E test timeout | Browser not starting or page not loading | Check `playwright install --with-deps`, add retry |
| Docker build timeout | Layer cache miss on large image | Use `docker/build-push-action` with cache-from |

### Category 5: Permission and Secret Failures

**Signals:**
- `Error: Resource not accessible by integration`
- `Error: Input required and not supplied: token`
- `fatal: could not read Username`
- `403 Forbidden` on API calls

**Common causes and fixes:**

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `Resource not accessible` | Insufficient `GITHUB_TOKEN` permissions | Add `permissions:` block to workflow |
| `Input required: token` | Secret not available in fork PRs | Use `pull_request_target` or conditional step |
| `could not read Username` | Private repo access without token | Use `actions/checkout` with `token: ${{ secrets.PAT }}` |
| `403` on deployment | Deploy key or token expired | Rotate secret in repo settings |

### Category 6: Workflow Configuration Errors

**Signals:**
- `Invalid workflow file` before any step runs
- `Unexpected value` in YAML parsing
- Steps reference nonexistent actions or wrong versions

**Common causes and fixes:**

| Error Pattern | Likely Cause | Fix |
|---------------|-------------|-----|
| `Invalid workflow file` | YAML syntax error | Validate with `actionlint` locally |
| `Unexpected value 'X'` | Wrong key name or indentation | Check GitHub Actions schema for correct key names |
| `Unable to resolve action` | Action not found or wrong version | Verify action exists, use `@v4` not `@master` |
| `Context access might be invalid` | Typo in `${{ }}` expression | Check variable names against available contexts |

## Flaky Test Analysis

Flaky tests are tests that pass and fail nondeterministically. They erode trust in CI. Diagnose by pattern:

### Detection

```bash
# Get last 20 runs for the test job
gh run list --workflow=tests.yml --limit 20 --json status,conclusion,startedAt

# Compare pass/fail ratio
gh run list --workflow=tests.yml --limit 50 --json conclusion | \
  jq 'group_by(.conclusion) | map({conclusion: .[0].conclusion, count: length})'
```

If the same workflow alternates between success and failure without code changes, you have flaky tests.

### Common Flaky Patterns

1. **Race condition**: Tests share mutable state. Fix: isolate test state, use `beforeEach` reset.
2. **Timing dependency**: Test assumes operation completes in N ms. Fix: use polling/waitFor instead of sleep.
3. **Order dependency**: Test passes in isolation but fails when run after another test. Fix: ensure cleanup in afterEach.
4. **Port collision**: Multiple test suites bind to same port. Fix: use random ports or `--shard`.
5. **Timezone/locale**: Test passes in US locale but fails in CI (usually UTC). Fix: set `TZ=UTC` in test env.
6. **File system ordering**: `readdir` returns different order on different OS. Fix: sort results before comparing.

### Quarantine Strategy

If a flaky test cannot be fixed immediately:

1. Move to a `flaky/` directory or tag with `.skip` + a TODO comment with issue link
2. Create a tracking issue with reproduction details
3. Set a deadline (2 weeks max) for resolution
4. Never delete a flaky test -- it caught a real issue at least once

## Workflow Validation

Before a workflow runs in CI, validate it locally:

```bash
# Install actionlint (the gold standard for workflow linting)
brew install actionlint  # macOS
# or: go install github.com/rhysd/actionlint/cmd/actionlint@latest

# Lint all workflow files
actionlint .github/workflows/*.yml

# Check a specific file with verbose output
actionlint -verbose .github/workflows/ci.yml
```

### Common YAML Pitfalls

1. **Unquoted `on:` triggers**: `on: push` works, but `on: [push, pull_request]` needs the brackets
2. **Missing `runs-on`**: Every job needs it
3. **Wrong indentation**: Steps under `steps:` must be at the right level
4. **Expression syntax**: `${{ github.event.pull_request.number }}` not `${ github.event... }`
5. **Matrix include/exclude**: `include` adds combinations, it does not filter -- use `exclude` to remove

## Anti-Patterns

### 1. Retry Until Green

**Symptom**: Re-running failed workflow until it passes
**Why wrong**: Masks real issues, wastes compute minutes, teaches team to ignore CI
**Fix**: Investigate every failure. If genuinely flaky, quarantine the test and fix the root cause.

### 2. Disabling Failing Checks

**Symptom**: Removing status checks from branch protection because they fail
**Why wrong**: Opens main branch to broken code
**Fix**: Fix the check, or mark it as `continue-on-error: true` with a tracking issue.

### 3. Blaming the Runner

**Symptom**: "CI is slow/broken, works on my machine"
**Why wrong**: CI environment differences are the test -- if it fails there, the code has assumptions
**Fix**: Match CI environment locally. Use `act` or Docker to reproduce. Add `CI=true` to local test runs.

### 4. Giant Log Dumps

**Symptom**: Pasting entire CI log into an issue or PR comment
**Why wrong**: No one reads 10,000 lines of logs
**Fix**: Extract the relevant 10-20 lines around the failure. Include the step name, error message, and exit code.

### 5. Ignoring Warnings

**Symptom**: CI passes but with deprecation warnings, security advisories, or linting warnings
**Why wrong**: Warnings become errors in the next major version. Technical debt compounds.
**Fix**: Treat warnings as errors in CI (`--max-warnings 0` for ESLint, `--strict` for TypeScript).

### 6. Monolithic Workflow Files

**Symptom**: Single 500-line workflow file that does lint + test + build + deploy
**Why wrong**: One failure blocks everything, hard to debug, impossible to re-run selectively
**Fix**: Split into separate workflows or use reusable workflows with `workflow_call`.

## Decision Points

### When to escalate vs fix locally

- **Fix locally**: Dependency version bump, lockfile update, snapshot update, env variable typo
- **Escalate**: Infrastructure issue (GitHub Actions outage), permission change needed (admin-only), flaky test requiring architecture change

### When a failure is infrastructure vs code

Check https://www.githubstatus.com/ first. If Actions shows degraded:
- Note the incident in the PR
- Wait and re-run
- Do NOT push empty commits to trigger reruns

If infrastructure is healthy, the failure is yours to own.

### When matrix failures are partial

If only `node-18, ubuntu-latest` fails but `node-20, ubuntu-latest` passes:
- The fix is probably a Node 18 compatibility issue
- Check if the project's `engines.node` matches the matrix
- Consider dropping the failing version if it is EOL

## Quality Checklist

```
[ ] Identified the exact failing step (not just "CI failed")
[ ] Classified failure into correct category (dependency/build/test/timeout/permission/config)
[ ] Reproduced locally when possible (or explained why not)
[ ] Fix addresses root cause, not symptoms (no blind retries)
[ ] Flaky tests either fixed or quarantined with tracking issue
[ ] Workflow YAML validates with actionlint after changes
[ ] CI minutes impact considered (larger runner = more cost)
[ ] Secrets verified as available for the trigger type (push vs pull_request vs fork)
[ ] Timeout values set explicitly on long-running jobs
[ ] Status check passes on the fix PR before merging
```

## Quick Reference Commands

```bash
# List recent workflow runs
gh run list --limit 10

# View a specific run (shows jobs and steps)
gh run view <run-id>

# Get only failed step logs
gh run view <run-id> --log-failed

# Re-run failed jobs only (not the whole workflow)
gh run rerun <run-id> --failed

# Watch a running workflow
gh run watch <run-id>

# List workflow files
ls .github/workflows/

# Validate workflow syntax locally
actionlint .github/workflows/*.yml

# Check GitHub Actions service status
open https://www.githubstatus.com/

# Run workflow manually (if workflow_dispatch enabled)
gh workflow run <workflow-name>
```

---

**Covers**: GitHub Actions diagnosis | Failure classification | Flaky test analysis | Workflow validation | Permission debugging | Timeout investigation

**Use with**: github-actions-pipeline-builder (create workflows) | ci-cache-optimizer (fix cache issues) | test-automation-expert (fix failing tests) | site-reliability-engineer (production CI/CD)
