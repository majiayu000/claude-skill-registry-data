---
name: hardware-base-test
description: Create or modify the shared BaseTest command helpers and class-based hardware tests in this pytest hardware automation repository. Use when adding reusable command execution, standard INFO logging, CommandResult assertions, fixture-managed state, or unit coverage for tests/hardware/base.py.
---

# Hardware Base Test

Keep reusable hardware-test behavior in `tests/hardware/base.py` and follow the repository
`AGENTS.md` rules.

## Workflow

1. Inspect `Dut`, `TestStand`, `Transport`, `CommandResult`, logging configuration, and existing fake
   transports before changing the helper.
2. Expose command execution through a public device API. Never access `_transport` from
   `BaseTest` and never create SSH clients, stands, devices, or connections there.
3. Implement `BaseTest` helpers as typed class methods. Pass a `Dut` explicitly; do not introduce
   class or global runtime state.
4. When one hardware-test group needs shared behavior or fixtures, allow a group-local `base.py`
   inside that group's directory. Its custom base class must inherit from
   `tests.hardware.base.BaseTest`; do not move project-specific behavior into the shared helper.
5. A group-local base class may declare typed pytest fixtures as class methods with
   `@pytest.fixture(scope="class")` above `@classmethod`; use `cls`, not an instance `self`
   parameter. Obtain devices from the injected `TestStand` through logical roles, return or yield
   them to tests, and never store the stand, devices, or other mutable runtime state on the class.
   Fixtures that change device state must use `yield` with `try/finally`.
6. Import a group-specific base in test modules under the common local name `BaseTest`, for
   example `from tests.hardware.recovery.base import RecoveryBaseTest as BaseTest`.
7. Use `run_command` for logging and execution, `check_command` for assertions, and
   `run_and_check_command` for their immediate composition. Return `CommandResult` when callers
   may need additional test-specific checks.
8. Log command execution details through the module's standard logger at `INFO` level. Keep
   numbered `StepLogger` calls in tests and fixtures for significant scenario actions. Do not log
   commands, results, or expected values containing credentials or secrets.
9. Keep named domain operations on device classes. Accept arbitrary command strings only when the
   DUT command-line interface is itself under test.
10. Read `docs/hardware-base-test.md` when adding preparation or cleanup fixtures, or when showing
   users how `BaseTest` composes with fixture-managed state.
11. Unit-test the helper with fake transports and a captured logger. Cover delegation, timeout,
   logging, successful return values, and assertion failures without network or physical hardware.
12. Run the narrow unit test first, then `./scripts/ci.sh`. Never run hardware tests unless the user
   explicitly requests them and confirms that a real stand is ready.
