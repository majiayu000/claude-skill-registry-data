---
name: verify
description: Run unit tests then integration tests (LocalStack) and surface any failures before committing
disable-model-invocation: false
---

When the user invokes `/verify`, run the full test suite in two stages and report clearly.

## Steps

1. **Lint** — run golangci-lint first:
   ```bash
   make lint 2>&1
   ```
   Report any issues. If golangci-lint is not installed, skip and note it.

2. **Unit tests** — run and capture output:
   ```bash
   make test 2>&1
   ```
   Report pass/fail. If any tests fail, show the failing test names and error output, then stop (don't proceed to integration tests).

3. **Integration tests** — only if unit tests passed:
   ```bash
   make test-integration 2>&1
   ```
   These require Docker. If Docker is not running, tell the user and skip this step.
   Report pass/fail. Show failing test names and errors if any.

4. **Summary**: Report the final status clearly:
   - All tests passed → "Ready to commit."
   - Failures found → list which tests failed and in which packages.
   - Docker unavailable → note that integration tests were skipped.
