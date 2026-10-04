---
name: foundation-testing
description: Set up testing infrastructure — install the test framework, author conftest fixtures, mocking patterns, factory helpers, coverage reporting, in-memory test doubles, Makefile targets that mirror CI, and an initial smoke test that proves the harness works. Loads at testing bootstrap when no `tests/` exists, or when the operator says "set up testing", "add pytest", "we need a test framework", "wire up coverage".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# foundation-testing

The foundation skill that authors a project's testing harness. AICP's pattern (per [tests/](../../../tests/)): pytest mirroring `aicp/` structure, mock httpx for backend tests, no live LocalAI required for unit tests, profile tests at `tests/test_profiles.py` (58 tests), 1,840 tests total.

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **No tests exist**: project has no `tests/` directory, no `pytest.ini`/`pyproject.toml [tool.pytest.ini_options]`, no test runner configured.
- **Direct verb**: operator says "set up testing", "add pytest", "we need a test framework", "wire up coverage", "bootstrap the test infrastructure".
- **Foundation-stage of project-lifecycle**: a new sister project at the foundation stage; testing harness is one of the foundation deliverables.
- **Migration**: project tests exist in another framework (unittest, nose) and operator wants to move to the project's standard.

Do NOT load when:

- Tests exist; you're adding tests for a new feature — load `feature-test`.
- Coverage gap audit on existing tests — load `quality-coverage`.
- A specific test is broken — load `feature-iterate` or fix it directly as a bug.
- Refactoring fixtures/factories that already exist — load `refactor-extract` (extract a fixture) or `refactor-architecture` (move conftest scope).

## Operations

This skill has 4 named operations. Execute in order.

### Operation 1: Pick framework + structure

**Trigger**: skill loaded; operator confirmed greenfield testing harness.

**Process**:

1. Detect language → pick framework:
   - **Python** (AICP-domain default): pytest + pytest-mock optional. Already in `[dev]` extras.
   - **Node**: jest or vitest (vitest if Vite project, jest otherwise).
   - **Rust**: built-in `cargo test`; add `proptest` for property-based.
   - **Go**: built-in `go test`; add `testify` for assertions if operator prefers.
2. Decide directory structure. AICP-domain canonical: `tests/` at project root, mirroring `aicp/` package layout — `tests/test_<module>.py` per source module. Sub-packages get `tests/<subpkg>/test_*.py`.
3. Decide test categories the project will need:
   - **Unit** (always): module-level, mocked dependencies.
   - **Integration** (if external services): real HTTP / DB / file system, gated behind `--integration` flag.
   - **Property** (if data-heavy): property-based via Hypothesis or proptest.
   - **End-to-end** (if user-facing flows): full stack, slowest, gated.
4. State the plan: framework / structure / categories. Wait for "go".

**Quality bar (Operation 1 done when)**:

- [ ] Framework chosen and matches the language / project conventions.
- [ ] Directory structure decided (mirroring source by default).
- [ ] Test categories enumerated; integration/e2e gated explicitly.
- [ ] Operator approved.

### Operation 2: Configure runner + author fixtures

**Trigger**: Operation 1 plan approved.

**Process**:

1. Configure the runner. For pytest in `pyproject.toml`:
   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = ["test_*.py"]
   python_classes = ["Test*"]
   python_functions = ["test_*"]
   addopts = "-ra --strict-markers --strict-config"
   markers = [
     "integration: requires live LocalAI / external service",
     "slow: takes >5s — skip in fast loop",
   ]
   ```
2. Author root `conftest.py` with shared fixtures. AICP-pattern examples:
   ```python
   # tests/conftest.py
   import pytest
   from pathlib import Path

   @pytest.fixture
   def project_path(tmp_path):
       """Fresh per-test project dir."""
       return tmp_path

   @pytest.fixture
   def mock_httpx_post(monkeypatch):
       """Patch httpx.post to return a controllable mock."""
       calls = []
       def _post(url, **kwargs):
           calls.append({"url": url, **kwargs})
           return _MockResponse(json_data={"ok": True})
       monkeypatch.setattr("httpx.post", _post)
       return calls
   ```
3. Author per-package `conftest.py` for fixtures only that subset needs. Don't push everything to root.
4. Author factory helpers in `tests/factories.py` (or per-package): functions that produce realistic test data with sensible defaults that callers can override.
5. Configure coverage. For Python: add `pytest-cov` to dev deps, configure in `pyproject.toml`:
   ```toml
   [tool.coverage.run]
   source = ["aicp"]
   omit = ["*/tests/*", "*/__init__.py"]
   [tool.coverage.report]
   fail_under = 80
   show_missing = true
   ```

**Quality bar (Operation 2 done when)**:

- [ ] Runner config in `pyproject.toml` (or equivalent), not scattered config files.
- [ ] `tests/conftest.py` exists with at least the fixtures the project will need across packages.
- [ ] Factory helpers exist for any non-trivial domain object.
- [ ] Coverage configured with a real threshold (project default: 80%).
- [ ] Markers defined and documented (`integration`, `slow`).

### Operation 3: Author smoke test + verify harness

**Trigger**: Operation 2 config + fixtures landed.

**Process**:

1. Author the smoke test that proves the harness itself works:
   ```python
   # tests/test_smoke.py
   def test_package_imports():
       """Verify the main package imports — catches install/wiring breaks early."""
       import aicp  # noqa: F401

   def test_smoke_fixture_works(project_path):
       """conftest fixture is reachable + tmp_path works."""
       assert project_path.exists()

   def test_mock_pattern_works(mock_httpx_post):
       """The httpx mocking pattern doesn't crash on import."""
       import httpx
       httpx.post("http://test", json={})
       assert len(mock_httpx_post) == 1
   ```
2. Run the test gate: `.venv/bin/pytest tests/ -v`. Verify exit 0, all 3 smoke tests pass, runner output is clean.
3. Run with coverage: `.venv/bin/pytest tests/ --cov=aicp --cov-report=term-missing`. Verify coverage threshold gate works (will warn at greenfield since no source covered yet).
4. Add Makefile targets that mirror what CI uses:
   ```make
   test:          ; .venv/bin/pytest tests/ -x --tb=short
   test-coverage: ; .venv/bin/pytest tests/ --cov=aicp --cov-report=term-missing
   test-fast:     ; .venv/bin/pytest tests/ -x -m "not integration and not slow"
   test-watch:    ; .venv/bin/pytest-watch tests/  # requires pytest-watch
   ```

**Quality bar (Operation 3 done when)**:

- [ ] Smoke tests exist and pass.
- [ ] `make test` exits 0.
- [ ] `make test-coverage` runs without crashing (threshold may be unmet at greenfield — OK).
- [ ] Makefile targets mirror CI commands literally (per foundation-ci pattern).

### Operation 4: Document and hand off

**Trigger**: Operation 3 verifications pass.

**Process**:

1. Document testing in README (or `docs/testing.md`):
   - How to run tests (`make test`, `pytest tests/test_X.py::test_specific`).
   - How to run integration tests (`pytest -m integration` — requires what services).
   - How to add a new test (mirror the source module, use existing fixtures, follow naming).
   - Coverage threshold and where to read the report.
2. Note any tests deliberately deferred — explicit "we don't test X yet because Y" comments are better than silence.
3. Suggest the next foundation skill if applicable: `foundation-ci` (pipeline that runs these tests), `foundation-logging` (log capture in tests).
4. If the project has existing source code (this skill ran late), suggest `quality-coverage` next to backfill tests for the existing code.

**Quality bar (Operation 4 done when)**:

- [ ] README has testing section with run commands + integration gating + coverage.
- [ ] Deferred test areas explicitly noted (not silently dropped).
- [ ] Next-step skill suggested.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Tests that depend on test ordering

Test A leaves global state (env var, monkeypatch, file in tmp); test B reads it. Tests pass when run in order, fail when run via `pytest -p random` or with `-x` after a B-only run. Flaky in CI.

**The rule**: every test sets up its own state via fixtures (auto-cleaned by pytest) and never mutates module-global or process-wide state without `monkeypatch`. Run `pytest -p random` periodically — if anything fails, that's a fixture-leak bug.

### Gotcha 2: Mocking the wrong layer

Test mocks `httpx` at the import path the test file uses (`tests.test_X.httpx`), but the production code imports `httpx` at `aicp.backends.localai.httpx`. The mock doesn't intercept the production call.

**The rule**: mock at the IMPORT SITE of the production code, not where the test imports. `monkeypatch.setattr("aicp.backends.localai.httpx.post", ...)`. Verify the mock fires by adding an `assert mock_called` after the production call.

### Gotcha 3: Coverage as a number, not a signal

Threshold of 80%; team adds tests that exercise lines but don't assert behavior (just `assert result is not None`). Coverage stays high, real bugs ship.

**The rule**: coverage is necessary, not sufficient. Pair the coverage gate with a "every test has at least one meaningful assertion" review at PR time. Use `pytest --cov-report=term-missing` to spot lines that ARE covered but not via meaningful paths.

### Gotcha 4: Live external services in unit tests

Unit test calls real LocalAI, real OpenRouter, real database. Test takes 5s, requires the service running, breaks the moment the service is down. CI fails for "unrelated reasons" weekly.

**The rule**: unit tests mock all external HTTP / DB / network. Integration tests use real services BUT are marked `@pytest.mark.integration` and excluded from `make test-fast`. The default `make test` may include integration tests if they're fast and stable; if they're either of those, gate them.

### Gotcha 5: Smoke test that verifies nothing

`def test_smoke(): pass` — passes always. Gives "tests passing" green light. Catches nothing. The test runner has no signal.

**The rule**: smoke tests have ≥1 meaningful assertion. The package-imports test is the canonical smoke — it catches install breaks, wiring errors, circular imports. Add 2-3 more for fixture reachability and mocking pattern. Skip the empty-pass tests.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning.

The canonical AICP-domain testing reference: [tests/](../../../tests/) — 1,840 tests across 97 files, mirrors `aicp/` structure, conftest patterns at [tests/conftest.py](../../../tests/conftest.py) (if present) or per-package. Backend tests use mocked httpx exclusively (no live LocalAI required).

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP-domain defaults:

- Framework: pytest (already in `[dev]` extras).
- Structure: `tests/test_<module>.py` mirroring `aicp/`.
- Mocking: `monkeypatch` + `unittest.mock` for httpx; no live LocalAI in unit tests.
- Coverage: aspirational 80%; gate not currently enforced (deferred until rewrite phase).
- Markers: `integration` (live services), `slow` (>5s).

Per [wiki/config/domain-profiles/backend-ai-platform-python.yaml](../../../wiki/config/domain-profiles/backend-ai-platform-python.yaml), the implement-stage gate is `pytest tests/ -x --tb=short` and the test-stage gate is full `pytest tests/` plus test count drift check.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| feature-test | Author tests for a single feature | foundation-testing AUTHORS the harness; feature-test FILLS it |
| quality-coverage | Audit coverage gaps on existing tests | foundation-testing greenfield; quality-coverage on populated codebase |
| foundation-ci | CI that runs these tests | foundation-testing authors; foundation-ci runs |
| foundation-deps | Install pytest + pytest-cov | Different concern; pytest is already in `[dev]` for AICP-domain |
| refactor-extract | Pull a duplicated test helper into a fixture | Different operation; foundation-testing greenfield |
