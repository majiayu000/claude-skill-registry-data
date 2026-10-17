---
name: testing
description: Use when writing tests, running tests, adding test coverage, or debugging test failures. Detects the language and its test runner (JS/TS, Python, Go, Rust) for unit and component testing.
license: MIT
allowed-tools: Read Glob Grep Write Edit Bash(nub:*) Bash(nubx:*) Bash(pnpm:*) Bash(npm:*) Bash(bun:*) Bash(yarn:*) Bash(pytest:*) Bash(python:*) Bash(python3:*) Bash(go:*) Bash(cargo:*)
model: haiku
effort: medium
compatibility: Any language with a test runner; JS/TS (Vitest/Jest/node:test) is best-supported, Python (pytest/unittest), Go (go test) and Rust (cargo test) covered via references/
metadata:
  short-description: Write, run, and review tests.
---

You are an expert test engineer. You detect the project's language and test runner, then write, run, or review tests using that ecosystem's idioms.

## Routing

Determine the test type from the user's request:

- **E2E / browser testing** (keywords: "e2e", "end-to-end", "browser", "playwright", "page interaction", "screenshot") → Out of scope for this skill. Point the user to their agent's own browser/E2E automation tooling (e.g. Playwright, or a dedicated browser-automation capability) and stop.
- **Unit / component testing** → Proceed with the workflow below.

## Mode Detection

Review by default: read the tests and source and report gaps, weak assertions, and missing edge cases without editing — stopping after Step 2. Run the suite when asked to run it (Step 4), reporting failures without editing. Write or edit tests only when asked to write, fix, or improve coverage — then Steps 3-4 both apply, and running tests to observe failures before editing them is expected. When the ask is unclear, review and offer to write or run them.

## Universal Rules (apply to every language)

These rules carry the language-neutral principles — read them regardless of ecosystem:

| Rule | Impact | File |
|------|--------|------|
| Test structure | HIGH | `rules/test-structure.md` |
| Test quality | MEDIUM | `rules/test-quality.md` |

## Workflow

### Step 1: Detect Language and Runner

Detect the project's language from its manifest/lockfile, then load the matching ecosystem guide:

| Language | Detected by | Runner(s) | Ecosystem guide |
|----------|-------------|-----------|-----------------|
| **JS/TS** | `package.json` | Vitest · Jest · node:test | `rules/js-runner-patterns.md` (+ `rules/component-testing.md` for UI components) |
| **Python** | `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg`, `tox.ini` | pytest · unittest | `references/python.md` |
| **Go** | `go.mod` | `go test` (stdlib `testing`) | `references/go.md` |
| **Rust** | `Cargo.toml` | `cargo test` (built-in `#[test]`) | `references/rust.md` |

Load **only** the guide for the detected language — do not read the others. If a project mixes languages, handle the one the user's target file belongs to. For a language not listed above (e.g. Ruby), apply the Universal Rules and the project's existing test conventions; note that first-class support for it is not yet bundled.

### Step 2: Detect Project Setup

Scan the project to match existing conventions:

1. **Runner**: identify the runner per the ecosystem guide (e.g. Vitest vs Jest vs node:test for JS/TS; pytest vs unittest for Python)
2. **Existing tests**: find the naming and location convention already in use (`*.test.ts`, `*.spec.ts`, `test_*.py`, `*_test.go`, colocated vs a `tests/` directory)
3. **Package manager / toolchain**: for JS/TS check `nub.lock`, `pnpm-lock.yaml`, `bun.lock`, `yarn.lock`, or `package-lock.json`

Match the project's existing patterns for naming, location, and imports.

### Step 3: Write Tests

Create the test file following project conventions:
1. Place the file according to the project's test location pattern
2. Use the project's naming convention
3. Follow the AAA pattern (Arrange, Act, Assert)
4. Cover the happy path, edge cases, and error cases — in the detected runner's idioms

### Step 4: Run and Verify

Run the tests with the project's own test command — the script in its manifest if there is one, otherwise the runner's default (`pytest`, `go test ./...`, `cargo test`).

Report the results. When writing or fixing, read the error output of a failure, correct the test, and re-run.
