---
name: build-test-verify
description: Use this skill when asked to build the project, run tests, lint the code, or verify that the TTA.dev platform is stable before committing.
---

### Build, Test, and Verify (TTA.dev)

Validate code changes to ensure they meet quality standards before committing.

#### Process

Execute the following steps in order. Do not skip steps.

0. **Orient** (before writing any code): query CGC for the target.
   ```
   mcp__codegraphcontext__find_code — search for the target function/class
   mcp__codegraphcontext__analyze_code_relationships — callers, dependencies
   mcp__codegraphcontext__calculate_cyclomatic_complexity — risk level
   ```
   If CGC is unavailable, note it and proceed. Do not block on CGC absence.

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

6. **Validate in E2B** (when adding or changing Python code): run the tests
   identified in the Orient step inside a clean E2B sandbox.
   ```python
   from ttadev.primitives.integrations.e2b_primitive import CodeExecutionPrimitive
   from ttadev.primitives.core.base import WorkflowContext

   async with CodeExecutionPrimitive() as executor:
       result = await executor.execute({
           "code": "import subprocess; r = subprocess.run(['python', '-m', 'pytest', '<test_file>', '-v', '--tb=short'], capture_output=True, text=True); print(r.stdout); print(r.stderr)"
       }, WorkflowContext(workflow_id="validate"))
       # Check result["success"] and result["output"] for PASSED/FAILED
   ```
   If E2B is unavailable, fall back to local pytest and note the deviation.

7. **Retain**: after a successful commit, call `mcp__hindsight__retain` with bank_id
   `tta-dev` documenting any decision, pattern, or failure from this task.

#### Common Issues

- **Type errors**: Ensure all new functions have strict type annotations (`str | None`, not `Optional[str]`).
- **Test failures**: Fix the implementation, never comment out tests. Follow the AAA pattern (Arrange-Act-Assert).
- **Import errors**: All primitives imports must use `from ttadev.primitives.X` — never `from primitives.X`.
- **Quarantined tests**: Tests marked `@pytest.mark.quarantine` are auto-skipped unless selected with `-m quarantine`.

#### Deep Reference

For full testing patterns, markers, CI pipeline details, and MockPrimitive API, see
[`docs/agent-guides/testing-architecture.md`](../../docs/agent-guides/testing-architecture.md).
