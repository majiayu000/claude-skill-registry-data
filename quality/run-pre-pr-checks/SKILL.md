---
name: run-pre-pr-checks
description: >
  Run the full local quality gate (format, lint, typecheck, tests) before
  opening a PR. Discovers the project's real check scripts, runs them in
  order, and reports a clear PASS/FAIL summary with actionable next steps.
  Trigger on "run the checks before I push", "is this ready for a PR", "run
  lint typecheck and tests", "am I good to push this", or "check everything
  before I open a PR". Runs BEFORE create-pr as the local quality gate — it
  does not create or open the pull request itself; use create-pr for that.
---

# run-pre-pr-checks

You are a pre-PR validation assistant. Your job is to run the full local quality gate before a PR is opened or code is pushed for review. Surface failures early, with clear output and actionable next steps.

Run this before `create-pr` or any branch push where CI is expected to pass.

---

## Step 1 — Identify the validation stack

Before running any checks, discover what the project actually uses.

Inspect the root of the repository and relevant workspace roots if monorepo:

```bash
ls
cat package.json          # or equivalent manifest
```

Identify which of these are configured:

- formatter: Prettier, Black, gofmt, rustfmt
- linter: ESLint, Biome, Ruff, Pylint, golangci-lint, Clippy
- type checker: TypeScript (`tsc`), Pyright, mypy, Flow
- test runner: Jest, Vitest, pytest, go test, cargo test, RSpec
- other checks: Knip (dead exports), dependency audit, custom scripts

Look for the check scripts in:

```bash
cat package.json | grep -E '"(lint|type-?check|test|format|check|validate)"'
```

Also inspect `Makefile`, `.github/workflows/`, or `scripts/` for the canonical CI check sequence.

Find the package manager from the lockfile: `pnpm-lock.yaml` means pnpm, `yarn.lock` means yarn, `bun.lock` or `bun.lockb` means bun, `package-lock.json` means npm. In a workspace, run from the directory the project's own docs or CI use.

The commands in the steps below are written for npm and are a fallback only. Run the project's own script with the detected package manager (`pnpm lint`, `yarn typecheck`), and use a bare tool command such as `npx eslint .` only when the project has that tool and no script for it.

Do not invent commands. Only run scripts that exist and are clearly intended for local use.

---

## Step 2 — Check working tree state before running checks

Understand what is about to be validated:

```bash
git status --short
git diff --stat
git diff --staged --stat
git stash list
```

Note:

- whether there are uncommitted changes that belong in the validation scope
- whether there are untracked files that should be staged before checking
- whether there is stashed work that may be related

If there are unstaged changes the user intended to include, ask whether to stash them or include them before running checks.

---

## Step 3 — Run format checks first

Format failures are the fastest to surface and fix.

Run the format check in read-only mode first:

```bash
# examples — use the correct script for this repo
npm run format:check
npx prettier --check .
black --check .
gofmt -l .
```

Rules:

- prefer `--check` or dry-run modes before auto-fixing
- if auto-fix is safe and the user is fine with it, run the fix and show the diff
- if the fix would touch many unrelated files, ask first

---

## Step 4 — Run the linter

```bash
# examples — use the correct script for this repo
npm run lint
npx eslint .
ruff check .
golangci-lint run
```

Record:

- whether lint exited clean
- any errors vs warnings
- which files were flagged

If there are many lint errors, show a summary count before listing individual failures.

---

## Step 5 — Run the type checker

```bash
# examples — use the correct script for this repo
npm run typecheck
npx tsc --noEmit
mypy .
pyright
```

Rules:

- do not modify source files to suppress type errors unless the user asks
- report errors with the exact file, line, and message
- if the type checker is slow, note that it ran but show only failures

---

## Step 6 — Run the test suite

Run the narrowest scope that is still meaningful for a pre-PR gate:

```bash
# examples — use the correct script for this repo
npm test
npm run test:unit
pytest
go test ./...
cargo test
```

Prefer:

- unit and integration tests over full e2e
- the scope that maps closest to what CI runs for a PR check

Record:

- total: passed / failed / skipped
- any flaky tests that passed on retry

If tests take more than a couple of minutes, note that fact explicitly.

---

## Step 7 — Run any additional project-specific checks

Inspect CI config for extra gates that are not covered above:

```bash
cat .github/workflows/*.yml | grep -E 'run:|npm run|yarn|pnpm'
```

Examples of common additional checks:

- dead export detection: `npx knip`
- dependency audit: `npm audit --audit-level=high`
- build: `npm run build`
- custom scripts in `scripts/` or `Makefile`

Only run checks that are part of the PR gate and are safe to run locally.

---

## Step 8 — Report results

Produce a gate summary:

```text
Pre-PR check summary

Format        PASS | FAIL
Lint          PASS | FAIL (<N> errors)
Typecheck     PASS | FAIL (<N> errors)
Tests         PASS | FAIL (<N> failed of <total>)
Other         PASS | FAIL | SKIPPED

Gate result: READY TO PUSH | BLOCKED
```

If blocked, list each failure clearly with:

- tool name
- failing file(s) or test name(s)
- the error or assertion
- suggested next step or command to fix it

If all checks pass, say so and tell the user they can proceed with `create-pr`.

Do not claim a gate is clean unless all configured checks actually ran and passed.
