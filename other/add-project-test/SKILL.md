---
name: add-project-test
description: Add or convert typed pytest tests in this hardware automation project. Use when asked to create unit, software-integration, or physical-hardware tests; add pytest markers or fixtures; create YAML-driven cases with yaml-test-params; or place a test in the correct test layer.
---

# Add Project Test

Create a focused test in the correct layer while keeping ordinary quality gates independent of
physical hardware.

## Inspect and classify

1. Read `AGENTS.md` completely and follow its approval and verification rules.
2. Inspect the behavior under test, nearby tests, fixtures, markers, fakes, and public APIs.
3. Classify the test before choosing its location:
   - place isolated behavior using fakes in `tests/unit`;
   - place multi-component framework composition without network I/O in `tests/integration`;
   - place tests requiring a real stand in `tests/hardware`.
4. Preserve existing markers, fixtures, cleanup, mocks, and assertions when converting a test.
5. If production behavior must change, propose and implement that change first; update tests only
   after the user approves the production code.

## Design and review

1. Fully type test functions, fixtures, fakes, and test models.
2. Keep unit tests free of network and physical equipment.
3. Use fakes in integration tests; never open real SSH connections there.
4. Make hardware tests consume `TestStand` logical roles and device domain APIs, never physical IDs
   or direct SSH commands.
5. Require `--stand` only for hardware tests.
6. Use registered pytest markers and preserve `--strict-markers` compatibility.
7. Use `yield` with `try/finally` for fixtures that allocate resources or change device state.
8. When a hardware-test group needs shared behavior or fixtures, place a local `base.py` in that
   group's directory and inherit its custom base class from `tests.hardware.base.BaseTest`.
   A custom base class may define typed class-method fixtures with `@pytest.fixture(scope="class")`
   above `@classmethod`; use `cls` instead of an instance `self` parameter, resolve devices from
   the injected `TestStand` by logical role, and never keep mutable runtime state on the class.
9. Import the group-specific base in test modules under the common local name `BaseTest`, for
   example `from tests.hardware.recovery.base import RecoveryBaseTest as BaseTest`.
10. Show complete representative test code and list every file to create or modify.
11. Request explicit approval before modifying files.

## YAML-driven cases

Use YAML parametrization when cases are declarative scenario data:

1. Store scenario data under `configs/`, never inventory or settings.
2. Define typed Pydantic case and collection models close to the target test.
3. Use `YamlConfigSource` and `@yaml_parametrize` from `yaml-test-params`.
4. Rely on the automatically loaded plugin; do not add `pytest_generate_tests` without a genuine
   integration need.
5. Give cases stable, readable `test_name` IDs.

## Implement and verify

1. Modify only the approved tests, fixtures, models, configs, and documentation.
2. Run the narrowest relevant test first; use `-vv` for YAML-parametrized cases.
3. Never run hardware tests without explicit permission and a ready physical stand.
4. Stage the intended changes and run `./scripts/ci.sh`.
5. Report the test layer, collected case count when relevant, and verification results.
