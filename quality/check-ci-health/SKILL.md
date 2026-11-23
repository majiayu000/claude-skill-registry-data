---
name: check-ci-health
description: >
  Inspect CI configuration files for trigger misconfigurations, security
  risks, caching gaps, and slow-path inefficiencies. Use when CI behaves
  unexpectedly or before adding a new workflow. Trigger on "is our CI config
  secure", "review our GitHub Actions workflow", "audit our CI setup", "why
  is our CI so slow", or "check our pipeline for security issues". This is a
  static, pre-emptive audit of CI config files, not a live-failure diagnosis
  — when an actual run is failing, use triage-ci-failure instead.
---

# check-ci-health

You are a CI configuration reviewer. Your job is to find misconfigurations, security issues, and performance problems in CI pipeline definitions. Be specific — vague "check your caching" notes are not useful. Name the file, the job, the line.

---

## Step 1 — Locate all CI configuration files

Find CI pipeline definitions in common locations:

```
.github/workflows/*.yml          (GitHub Actions)
.github/workflows/*.yaml
.circleci/config.yml             (CircleCI)
.gitlab-ci.yml                   (GitLab CI)
Jenkinsfile                      (Jenkins)
.buildkite/pipeline.yml          (Buildkite)
azure-pipelines.yml              (Azure Pipelines)
bitbucket-pipelines.yml          (Bitbucket Pipelines)
.travis.yml                      (Travis CI)
```

Read each file fully. Note the CI provider, the trigger events, and the job/step structure.

---

## Step 2 — Validate trigger conditions

For each workflow/pipeline, check whether the trigger scope is appropriate:

**Overly broad triggers (flag as medium):**

- `on: push` without branch filters — runs on every push to every branch including forks
- `on: push: branches: ['*']` — equivalent; every branch triggers a full build
- Release workflows triggered on `push` to feature branches

**Missing triggers (flag as low–medium):**

- Test/lint workflows that don't run on `pull_request` — PRs merge without CI running
- Workflows that run on `push` to main but not on the PR that would create that push

**Wasteful triggers (flag as low):**

- Full build + test pipeline triggered by changes to `*.md`, `docs/`, or `.github/CODEOWNERS` only
- Suggest adding `paths-ignore` to skip expensive jobs for documentation-only changes

---

## Step 3 — Flag security risks

**Unpinned third-party actions (high):**

Any third-party action (`uses: owner/action@version`) that is not pinned to a full commit SHA is a supply-chain risk. A tag like `@v3` can be moved to a malicious commit at any time.

Safe: `uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`
Unsafe: `uses: actions/checkout@v4` or `uses: actions/checkout@main`

Flag every unpinned third-party action. First-party actions (`actions/*`, `github/*`) have a lower but non-zero risk.

**`pull_request_target` with secret access (critical):**

Workflows triggered by `pull_request_target` run in the context of the base repo (with access to secrets). If they also checkout PR code and run it, attackers can submit PRs that exfiltrate secrets.

Flag any workflow that:

- uses `pull_request_target` as a trigger AND
- checks out code with `actions/checkout` AND
- runs the checked-out code (build, test, script execution)

**Shell injection via unquoted expressions (high):**

Any workflow step that uses `${{ github.event.* }}` in a `run:` block without sanitization is vulnerable to injection if the triggering event can be controlled by an attacker (e.g., PR title, branch name, commit message).

```yaml
# Vulnerable
- run: echo "Branch: ${{ github.event.pull_request.head.ref }}"

# Safe
- run: echo "Branch: $BRANCH_NAME"
  env:
    BRANCH_NAME: ${{ github.event.pull_request.head.ref }}
```

Flag any `run:` step that interpolates `${{ github.event.* }}` directly into shell commands.

**Secrets in public logs:**

- Steps that `echo` or `print` environment variables that might contain secrets
- `env:` blocks that pass secrets to steps that don't need them

---

## Step 4 — Check caching

For each job that installs dependencies, check for a caching step:

**Missing dependency cache (medium):**

- npm/pnpm/yarn install without `actions/cache` or `setup-node` cache option
- pip install without a cache
- Go modules without a cache

**Cache key too broad (low):**

- Cache key based only on the OS or runner — never invalidates when dependencies change
- Example: `key: ${{ runner.os }}-cache` → correct: `key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}`

**Cache key too narrow (low):**

- Cache key that includes non-deterministic values like `${{ github.sha }}` — cache never hits
- Cache key that changes on every branch name push without a fallback restore key

**Missing artifact uploads (low):**

- Test jobs that don't upload test reports, coverage reports, or build artifacts — harder to debug failures

---

## Step 5 — Identify slow-path inefficiencies

**Missing `--frozen-lockfile` / `--ci` flag (medium):**

- `npm install` instead of `npm ci` — slower and non-deterministic
- `yarn install` without `--frozen-lockfile`
- `pnpm install` without `--frozen-lockfile`

**Serial test execution without sharding (low–medium):**

- A single test job running all tests for a large suite when the runner supports parallelism
- Look for `jest --runInBand` (disables parallelism) where it is not needed

**Missing job parallelization (low):**

- Lint, typecheck, and test jobs running sequentially in one job when they could run as parallel jobs with no dependencies
- Build jobs not parallelized across targets (e.g., multiple packages in a monorepo built sequentially)

**Unnecessary full checkouts (low):**

- Jobs that only need recent history checking out the full repo without `fetch-depth: 1`

---

## Step 6 — Report findings

```text
CI health review
──────────────────────────────────────────────────

Security (N findings)
1. [critical] pull_request_target with secret access — .github/workflows/pr-checks.yml
   The workflow checks out PR code and runs it with access to repository secrets.
   Fix: Use pull_request trigger instead, or add explicit permissions: read-only block.

2. [high] Unpinned third-party action — .github/workflows/deploy.yml (line 12)
   uses: some-org/action@v2 — tag can be moved to a malicious commit.
   Fix: Pin to SHA: uses: some-org/action@<full-sha>

3. [high] Shell injection risk — .github/workflows/test.yml (line 34)
   run: uses ${{ github.event.pull_request.title }} directly in shell.
   Fix: Pass via env variable.

Trigger configuration (N findings)
1. [medium] Overly broad push trigger — .github/workflows/test.yml
   Runs full test suite on every push to every branch.
   Fix: Add branches filter or use pull_request trigger.

Caching (N findings)
1. [medium] Missing dependency cache — .github/workflows/test.yml (install step)
   npm install runs on every job with no cache.
   Fix: Add actions/cache with key: ${{ runner.os }}-npm-${{ hashFiles('package-lock.json') }}

Performance (N findings)
1. [medium] npm install without --ci flag — .github/workflows/test.yml (line 8)
   Fix: Change to npm ci

Summary
  <overall verdict: healthy / issues to address / critical security issues requiring immediate action>
```
