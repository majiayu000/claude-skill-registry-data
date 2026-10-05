---
name: build-test-verify
description: 'Use this skill when asked to build the project, run tests, lint the code, check types, or verify that the TTA.dev platform is stable before committing. Invoke when the user says "run tests", "check quality", "lint", "format", "verify", or before any commit or PR.'
---

### Build, Test, and Verify (TTA.dev)

Validate code changes to ensure they meet quality standards before committing.

#### Process

Execute the following steps in order. Do not skip steps.

0. **Orient** (before writing any code): search the codebase for the target function/class,
   analyze its callers and dependencies, and assess complexity/risk level.
   Use available code analysis tools if configured; otherwise proceed with manual review.

1. **Format**: Apply Ruff formatting (100-char line length).
   ```bash
   uv run ruff format .
   ```

2. **Lint**: Run Ruff linter with auto-fix.
   ```bash
   uv run ruff check . --fix
   ```

3. **Type Check**: Run Pyright in basic mode.
   ```bash
   uvx pyright ttadev/
   ```

4. **Run Tests**: Execute the pytest suite (100% coverage required for new code).
   ```bash
   uv run pytest -v --tb=short -m "not integration and not slow and not external"
   ```

5. **Full coverage** (when adding new code):
   ```bash
   uv run pytest --cov=ttadev --cov-report=html
   ```

6. **Validate in sandbox** (when adding or changing Python code): run the identified
   tests inside a clean sandbox environment if available (e.g. E2B). If unavailable,
   fall back to local pytest and note the deviation.

#### Common Issues

- **Type errors**: Ensure all new functions have strict type annotations (`str | None`, not `Optional[str]`).
- **Test failures**: Fix the implementation, never comment out tests. Follow the AAA pattern (Arrange-Act-Assert).
- **Import errors**: All primitives imports must use `from ttadev.primitives.X` — never `from primitives.X`.
- **Quarantined tests**: Tests marked `@pytest.mark.quarantine` are auto-skipped unless selected with `-m quarantine`.

#### Deep Reference

For full testing patterns, markers, CI pipeline details, and MockPrimitive API, see
[`docs/agent-guides/testing-architecture.md`](../../docs/agent-guides/testing-architecture.md).
