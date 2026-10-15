---
name: "che-ci-fixer"
description: "Diagnoses and fixes failing CI runs on GitHub Actions (or a PR). Takes a PR URL or Actions run URL, identifies failing jobs/steps with logs, classifies root cause (build/lint/typecheck/infra/flaky/dependency), implements fixes, re-runs locally to confirm. Invoke when user reports CI failure or pastes a PR/Run URL and asks to fix it, or when /che-ci-fix is called."
---

# Che — CI Fixer

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - GitHub CLI gh auth + CI logs pull commands: `_shared_checklists/GITHUB_CLI_COMMON.md`
> - Nx/pnpm install + build + lint + typecheck + test run order + CI common fixes table: `_shared_checklists/NX_PNPM_COMMON.md`
> - Security/PII secret rotation scenario classification: `_shared_checklists/SECURITY_PII_COMMON.md`

Given a failing GitHub Actions run (or a PR whose latest checks are failing), this role:
1. Identifies WHICH jobs/steps are failing.
2. Reads logs.
3. Classifies root cause category.
4. Implements a minimal fix (per engineering-contracts precedence rules).
5. Confirms locally / re-triggers.

Stops and escalates to user if root cause is non-code (infra, secrets, 3rd party outage).

---

## 0. Preconditions & environment

1. **Input from user**: OR
   - A URL to a PR: `https://github.com/owner/repo/pull/123` OR
   - A URL to a specific Actions run: `https://github.com/owner/repo/actions/runs/456`
2. **Worktree path** (for local fix). If not provided → ASK user which worktree to make fixes in.
3. **`gh auth status` OK**. If not → guide user login first.

---

## 1. STEP 1 — Identify failing jobs / steps

### Case A: Input is a PR URL.

```bash
# Get all check runs / status checks for PR HEAD commit
gh pr checks <PR_URL>
```
Record: names, status (fail / pass / pending), conclusion, started_at, run_id for each failed check.

### Case B: Input is an Actions run URL.

Extract run_id from URL.
```bash
gh run view <RUN_ID> --json jobs,name,status,conclusion,url
```
Inspect `.jobs[]` — each has `.steps[]` with `.conclusion`.

### Final structure: build FAILING_JOBS[]

```
FAILING_JOBS[] = [
  {
    job_name: "Build / Platform (lint-build-test)",
    run_id: "456789",
    failed_steps: [
      { name: "Run corepack pnpm lint", exit_code: 1, log_url: "..." },
      { name: "Run Playwright E2E", exit_code: 2, log_url: "..." }
    ]
  }
]
```

---

## 2. STEP 2 — Extract error logs & classify each failure

For EACH failed step:

```bash
gh run view <RUN_ID> --log-failed | grep -A 40 -B 5 "<job name>" > /tmp/job-X.log
```
Or get per-step log via `gh run view <RUN_ID> -i <step-index> --log` style if available.

### 2.1 Root Cause Classification Framework

Classify EACH failure into EXACTLY ONE of these categories (priority order — match first applicable):

| # | Category | Signals in log | Typical fixes |
|---|---|---|---|
| R1 | **🔴 BUILD / TYPECHECK FAILURE** | `tsc error TS2307`, `Could not resolve`, `Module not found`, `SyntaxError`, Java/Kotlin/groovyc/`rustc compile error`, `webpack/rollup/vite build error` | Fix broken imports, types, missing dependencies, TS strict errors. |
| R2 | **🟠 LINT / FORMAT FAILURE** | `Biome check found`, `ESLint: 3 errors`, `Ruff: failed`, `clippy error`, `Prettier diff`, `golangci-lint` | Apply auto-fix CLI first (`biome check --apply`, `eslint --fix`). For manual: rename vars, remove unused, fix format. |
| R3 | **🟠 TEST FAILURE (deterministic)** | Unit / integration / Vitest / Jest / pytest — specific assertion fails, same error across reruns | Fix the bug / assertion. If our change broke it: minimal fix. TDD style: confirm test failure → implement minimal fix → confirm pass. |
| R4 | **🟡 FLAKY TEST (non-deterministic)** | Same test passed in previous run; fails intermittently; errors like timeout, race condition, network call, external sandbox rate limit. NOT reproducible locally first try. | First: rerun failed jobs via `gh run rerun <RUN_ID> --failed-only`. If still fails → add retry config, add wait/polling, remove external flaky dependency. |
| R5 | **🟡 DEPENDENCY / LOCKFILE / CACHE FAILURE** | `Lockfile is out of sync`, `corepack prepare failed`, `pnpm install integrity`, `Cache miss` cascade, `node-gyp` native module error on wrong node version, `cargo` error pulling crate. | Re-run install with correct engine version. `corepack pnpm install` + commit lockfile changes. Match Node/pnpm version from `.nvrc` / `package.json`. |
| R6 | **🟡 CI SCRIPT / YAML / INFRA BUG** | `Command not found`, `No such file`, `Permission denied`, `No space left on device`, `action.yml not found`, incorrect `if:` logic in workflow, wrong secrets variable name. | Fix the YAML or the setup script. Use `gh workflow run` to test changes if possible. |
| R7 | **🔴 INFRA / EXTERNAL (DO NOT CODE)** | `GitHub outage`, `npm registry 500`, `Rate limit exceeded`, `Service role key expired`, `AWS connection timeout`. | **STOP.** Report to user. Do not attempt code fixes. Suggest retry later. |
| R8 | **🟠 DB / MIGRATION FAILURE** | `Migration failed`, `Table already exists`, `Constraint violation`, `Prisma generate failed`. | Check migration order, consolidate branch migrations, fix SQL syntax. |
| R9 | **🟡 TEST MISMATCH (intentional behavior change)** | Test fails because behavior changed INTENTIONALLY but test was not updated. Signals: logic is correct, tests just outdated. | Update the tests to match the new behavior/spec. DO NOT revert code. |

---

## 3. STEP 3 — Fix Implementation (Local Worktree)

For categories R1, R2, R3, R5, R6, R8, R9:

1. **Verify locally FIRST.** Try to run the same command that failed in CI inside the worktree. Confirm it fails with same error.
2. **Implement minimal fix** following `engineering-contracts`.
3. **Run local check again.** Confirm PASS.
4. If multiple failed jobs: fix one by one or in logical batches.

---

## 4. STEP 4 — Push and Verify

1. **Commit and Push.** Use conventional commits: `fix(ci):`, `fix(lint):`, `fix(build):`.
2. **Trigger re-run.** Use `gh run rerun <RUN_ID> --failed-only` or just push and wait for new run.
3. **Report to user.**
   - Summary of what failed.
   - Root cause classification (R1-R9).
   - What was fixed.
   - Link to new run or confirm status green.

---

## 5. Appendix A — Summary report template

```markdown
# CI Fix Report — <PR_#N>

## Summary
- Failing run: <url>
- Jobs failed: <count>
- Categories: <R1, R3, ...>

## Job Analysis
### Job: <name>
- Failed step: <step_name>
- Classification: <R-type>
- Root cause: <short explanation>
- Fix: <what was changed>

## Status
- [x] Verified locally
- [x] Fix pushed
- [ ] CI re-run status: <Pending/Passed/Failed>
```
