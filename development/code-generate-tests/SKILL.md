---
name: code-generate-tests
description: Generate or update tests for observable public behavior. Use when asked to add tests, cover edge cases, or improve test coverage.
---

Generate tests that match existing project conventions.

## Process

### Step 1 - Identify Context

- If code changes are involved, run `jj diff -s` for changed files, then `jj diff -- path` to restrict scope.
- Focus on user-specified files, modules, behavior, or requirements.
- Identify public behavior and interfaces to test.

### Step 2 - Research and Scout

Apply a scout lens to identify critical public behavior, neighboring tests, fixtures, naming conventions, edge cases, and error paths in `{files}`:

- Map relevant files, conventions, and call paths.
- Cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs.
- Stay read-only.
- Keep it concise and task-relevant.

Apply a researcher lens to research idiomatic testing practices for the detected language/framework:

- Prefer official documentation over blog posts.
- Cite sources with URLs.
- Separate confirmed facts from plausible interpretations.
- Note version requirements.

Apply a reviewer lens to review proposed tests with a simplicity and behavior-coverage lens, avoiding unnecessary helpers or private-implementation assertions:

- Ground findings in file paths and line numbers.
- Prioritize the simplicity and behavior-coverage lens.
- Distinguish confirmed findings from speculative risks.
- Explain why each issue matters.

### Step 3 - Inspect Conventions

- Read relevant code, neighboring tests, fixtures, and helpers.
- Detect the test framework and command from task runners, wrapper scripts, package manager scripts, or defaults.
- Check `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `GEMINI.md`, and `CODEX.md`.

### Step 4 - Generate Tests

- Prioritize public interfaces and observable behavior (happy paths, edge cases, error paths) over private implementation details.
- Match existing naming, fixture, assertion, and file-layout conventions.
- Keep tests simple and explicit; avoid unnecessary helpers or abstractions.

### Step 5 - Verify

- Run the most specific test command directly.
- Fix failures if the cause is clear, but stop after two failed attempts.

### Step 6 - Report

Report to the user:

1. **Behavior Covered**
2. **Conventions Detected**
3. **Tests Added / Files Changed**
4. **Verification Results**
5. **Remaining Follow-up**
