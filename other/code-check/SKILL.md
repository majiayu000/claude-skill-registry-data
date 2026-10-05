---
name: code-check
description: Detect and run project test, lint, and format commands; diagnose and fix failures when requested. Use when asked to run tests, lint, format, check, verify, or fix failing tests/lint/format/check commands.
---

Run project checks (tests, lint, formatting); diagnose and fix failures with minimal targeted changes when requested.

## Process

### Step 1 - Identify Context

- For code changes: `jj diff -s` lists changed files; `jj diff -- path` restricts scope.
- Focus on user-specified files, commands, or failures.
- Read any provided failure output fully before editing.

### Step 2 - Detect Command

Detect test, lint, and format commands in this order (single shared list, not duplicated per kind):

1. **Project instructions**: `README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CODEX.md`.
2. **Task runners**: `Makefile`, `justfile`, `Taskfile.yml`.
3. **Wrapper scripts**: `bin/`, `.my/bin/` (`test`, `lint`, `check`, `fmt`, `format`, `*-test`, `*-lint`, `*-fmt`).
4. **Package manager scripts**: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, etc.
5. **Common defaults by language**:
   - **JavaScript/TypeScript**:
     - Test: `npm test`
     - Lint: `npm run lint`, `npx tsc --noEmit`
     - Format: `npm run format`, `prettier --check .` (check) / `prettier --write .` (write)
   - **Python**:
     - Test: `pytest`
     - Lint: `ruff check .`, `mypy .` (when configured)
     - Format: `ruff format --check .` (check) / `ruff format .` (write)
   - **Go**:
     - Test: `go test ./...`
     - Lint: `golangci-lint run`, `go vet ./...`
     - Format: `gofmt` (check) / `gofmt -w` (write)
   - **Rust**:
     - Test: `cargo test`
     - Lint: `cargo clippy`
     - Format: `cargo fmt --check` (check) / `cargo fmt` (write)
   - **Ruby**:
     - Test: `bundle exec rake test`, `bundle exec rspec`
     - Lint: `bundle exec rubocop`
   - **Nix**:
     - Test/Lint/Check: `nix flake check path:.` for flakes (read the `nix` reference first)
     - Format: `nix run path:.#treefmt -- --ci` (check) / `nix run path:.#treefmt --` (write)

### Step 3 - Run Checks

- Default to check-only; do not edit unless asked to fix or apply formatting.
- Prefer the most specific command covering the requested files or changes.
- Use bounded timeouts; avoid watch modes.

### Step 4 - Modes

- **Run-only** (default): run, report pass/fail, suggest fixes without editing.
- **Fix**: proceed to Step 5. For formatting, applying the formatter is the fix.

### Step 5 - Diagnose and Fix (fix mode only)

- Prefer the exact failing command from the user or project output.
- Diagnose the root cause before editing.

Apply a researcher lens to identify the root cause of the failure ({error output}):

- Prefer official documentation over blog posts.
- Cite sources with URLs.
- Separate confirmed facts from plausible interpretations.
- Note version requirements.
- Lead with the single most actionable recommendation.

Classify the failure as one of: product-code bug, test bug, environment issue, stale expectation. Find relevant docs or known issues.

Then, apply a worker lens to apply a minimal fix for the {root cause} in {file}:

- Read files before editing; keep diffs minimal and idiomatic; preserve public behavior; verify with the narrowest meaningful command.
- Do not weaken assertions, skip tests, or broaden ignores unless explicitly approved with sound rationale.

### Step 6 - Verify

- Re-run the relevant command(s) to confirm the fix.

### Step 7 - Stop Condition

- If a fix fails twice, stop, analyze the root cause, and ask for guidance.

### Step 8 - Report

Report to the user:

1. **Command Used**
2. **Mode**: run-only or fix
3. **Results**: pass/fail summary
4. **Failures** with root cause and file references
5. **Fixes Applied** (if fix mode)
6. **Remaining Issues** requiring manual action
7. **Verification** from re-running relevant commands

## Guardrails

- Run-only by default; do not edit unless asked to fix or apply formatting.
- Do not weaken assertions, skip tests, or broaden ignores to make failures pass.
- Use the exact failing command from the user or project output when available.
- Avoid watch modes; use bounded timeouts.
- Prefer the most specific command covering the requested scope.
- For runtime/production errors not surfaced by a check command, use `code-debug`.
