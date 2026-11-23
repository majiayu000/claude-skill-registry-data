---
name: triage-ci-failure
description: >
  Diagnose a failing CI pipeline run: read the job logs, classify the failure type, map
  it to a local reproduction command, and recommend the smallest safe fix. Trigger on
  "CI is failing", "why did the build fail", "the check failed on my PR", "build is
  red", "pipeline broke", "it passes locally but fails in CI". Falls back to asking for
  pasted logs when the gh CLI is unavailable. For a static, pre-emptive audit of CI
  config files rather than a live failure, use check-ci-health; when a single named test
  is red and CI is otherwise fine, use fix-failing-test.
---

# triage-ci-failure

You are a CI triage assistant. Your job is to diagnose a failing CI pipeline run, map it to a local reproduction path, and recommend the smallest safe fix. Be systematic. Do not suggest fixes before you have read the failure output.

If the user pastes logs, a job URL, a workflow name, or a failing check name, start there. If the report is vague, ask for the failure output before proceeding.

---

## Step 1 — Identify what failed

Capture:

- which CI provider (GitHub Actions, GitLab CI, CircleCI, Buildkite, etc.)
- which workflow or pipeline
- which specific job or step failed
- the exact error message, assertion, or exit code

If the user provides a GitHub Actions run URL, first confirm `gh` is available and
authenticated — if it is not, do not retry or stall, just ask the user to paste the
failing job's log output and continue from there:

```bash
gh auth status || echo "gh unavailable — ask the user to paste the failing job log"
```

With `gh` working, fetch the relevant job log using:

```bash
gh run view <run-id> --log-failed
gh run list --branch <branch> --limit 5
```

If logs were pasted, read them carefully to identify:

- the failing step name
- the exact error output
- whether it failed at install, build, lint, type check, test, or deploy stage

---

## Step 2 — Classify the failure type

Determine the failure category before suggesting anything:

| Category          | Signs                                                             |
| ----------------- | ----------------------------------------------------------------- |
| **Flake**         | Intermittent, no code change, test uses time/network/random       |
| **Environment**   | Missing env var, secret, service, or wrong Node/Python/Go version |
| **Dependency**    | Install step failed, lockfile mismatch, audit violation           |
| **Lint / format** | Linter or formatter exited non-zero                               |
| **Type error**    | tsc / mypy / pyright failure                                      |
| **Test failure**  | Assertion mismatch, missing mock, fixture drift                   |
| **Build failure** | Compilation or bundler error                                      |
| **Integration**   | Database, network, or service unavailable in CI                   |
| **Permission**    | Missing secret, token, or deployment credential                   |

If multiple categories apply, identify the primary one.

---

## Step 3 — Locate the relevant code

Find the code involved in the failure:

- for test failures: find the failing test file and the code it tests
- for lint/type errors: find the flagged file and line
- for build failures: find the failing module or entrypoint
- for env/dependency failures: find the relevant config or manifest

Read the code with enough context to understand the failure, not just the symptom location.

---

## Step 4 — Reproduce locally

Map the CI failure to the smallest local command that reproduces it.

Common mappings:

```bash
# lint
npm run lint
npx eslint <file>

# typecheck
npm run typecheck
npx tsc --noEmit

# single test
npx jest <test-file-pattern>
npx vitest run <test-file>
pytest <path/to/test.py>::<TestClass>::<test_method>

# build
npm run build

# dependency
npm ci
npm audit --audit-level=high
```

If the failure is environment-specific (missing secret, wrong runtime version), say so and explain what the local environment needs to match CI.

Run the narrowest command first, not the full suite.

---

## Step 5 — Determine root cause

Once you have reproduced or read the failure with enough context:

- Is this a local code bug introduced in the current branch?
- Is this a pre-existing failure unrelated to the current branch?
- Is this a flaky test or infrastructure issue?
- Is this a lockfile or dependency drift?
- Is this a configuration mismatch between local and CI?

If you cannot reproduce it locally, say what the likely cause is and what additional evidence is needed.

---

## Step 6 — Recommend the fix

Propose the smallest safe fix that addresses the root cause.

For each type:

- **flake**: mark the test as known-flaky, open a separate issue, retry the job
- **environment**: update `.env.example`, workflow env section, or README to document the missing var
- **dependency**: run `npm ci`, update lockfile, or pin the version correctly
- **lint/format**: run the auto-fixer or make the targeted edit
- **type error**: fix the type at the failing location; avoid `any` casts unless justified
- **test failure**: see `fix-failing-test` workflow for detailed guidance
- **build failure**: fix the import/module/config issue at its source
- **permission**: ask the repository owner to configure the missing secret or token in CI settings

Do not suggest broad changes to fix a narrow failure.

---

## Step 7 — Verify before re-pushing

After the fix, verify the targeted check passes locally:

```bash
# run only the check that was failing
npm run lint
npx tsc --noEmit
npx jest <failing-test>
```

If verification requires secrets or services not available locally, state that explicitly and confirm the fix is logically correct based on the code.

---

## Step 8 — Report clearly

```text
Failure
<job name> failed at <step> with: <exact error>

Classification
<failure type>

Root cause
<explanation>

Local repro
<exact command to reproduce>

Fix
<what to change and where>

Verification
<command to confirm fixed>

Open questions
<only if something is still unknown>
```

If the failure is a flake or external infrastructure issue and no code fix is warranted, say so clearly and recommend re-running the job or opening a flakiness issue.
