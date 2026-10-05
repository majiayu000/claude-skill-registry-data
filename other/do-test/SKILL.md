---
name: do-test
description: 'Write or update tests for a code change. Operates in two modes: `unit` (module-scoped, fast, deterministic) and `integration` (crosses module / service / database boundaries). Intended to be invoked once per testable change from inside a do-issue-* or do-epic phase. Mode is required.'
argument-hint: 'mode: unit or integration'
user-invocable: true
disable-model-invocation: false
---

# Write or Update Tests

Wraps test-writing work in a Maverick skill so the workflow report
records what was tested and the agent applies the project's testing
standards before writing tests. Invoke this skill **once per testable
change** from inside `do-issue-solo` /
`do-issue-guided` / `do-epic` Phase 5 —
typically as a sibling call to `do-code`, before the
commit for that task.

This skill is a thin wrapper. The actual test files are written by the
orchestrating Claude Code session using its built-in tools (Read, Edit,
Write, Bash). The skill's job is to pin the right standards for the
mode and keep scope tight.

## Preflight (mandatory)

Run this **first**. If it exits non-zero, halt and report the stderr
output to the user verbatim. Do not proceed.

```bash
uv run maverick preflight do-test
```

Skip the preflight when invoked from inside a `do-issue-*` or
`do-epic` phase — the orchestrator already ran a stricter one this
session. Run it only when this skill is invoked standalone.

The check verifies the project is initialised and `uv` is on PATH.

## Mode Selection

`$ARGUMENTS` must specify a mode:

- `unit` — module-scoped, fast, deterministic. No network, no real
  database, no real filesystem outside the test's own `tmp_path`.
  Use this for any change that can be exercised through its public
  surface in-process.
- `integration` — crosses module / service / database / external API
  boundaries. Real I/O is allowed (and usually required). Slower;
  reserved for changes whose behaviour only emerges across that
  boundary.

If no mode is specified, halt and ask the caller to pick one. Do not
guess — getting the mode wrong invites flaky tests or fast-but-untrue
coverage.

## Unit Mode

Apply `mav-bp-testing` for the project's unit-testing
conventions (test framework, naming, fixture style, assertion
patterns).

1. **Locate the test file.** Look for an existing test file that
   corresponds to the production code you just changed. If none
   exists, follow the project's convention for placement
   (`tests/unit/test_<module>.py`, `<module>.test.ts`, etc.) — check
   how nearby modules are tested.
2. **Identify what changed in observable behaviour.** Write tests
   against the public surface, not the internals. If the change is
   purely refactoring with no behaviour change, the existing tests
   should already cover it — re-running them is the validation.
3. **Write one test per branch / case.** Cover the happy path,
   relevant edge cases, and any error paths the change introduced.
   Don't write a single mega-test that exercises everything.
4. **Verify** by running the project's unit suite per
   `mav-local-verification`. The whole suite — not just
   the new tests — must stay green.

## Integration Mode

Apply `mav-bp-testing` for the project's
integration-testing conventions (which real services are stood up,
fixture lifecycle, isolation strategy, slowness budget).

1. **Locate or create the integration test file.** Integration tests
   typically live separately from unit tests
   (`tests/integration/`, `e2e/`, `__tests__/integration/`, etc.) and
   have their own runner config.
2. **Stand up real dependencies.** Do not mock the boundary the test
   is supposed to exercise — if a test "covers" the database layer
   with a mocked database, it's a unit test, not an integration test.
3. **Test the boundary, not the unit.** Assert observable end-to-end
   behaviour, not implementation details on either side of the
   boundary.
4. **Clean up.** Integration tests must leave no state behind —
   transactions roll back, fixtures tear down, temporary resources
   are released. Failure to clean up makes the next test flaky.
5. **Verify** by running the project's integration suite. Note the
   wall-clock cost — if a new test pushes a green CI run past the
   project's slowness budget, refactor it or split it.

## Rules

- **No mocks at the unit's own boundary.** If you're testing `foo()`,
  don't mock `foo()`'s direct collaborators with such fidelity that
  the test passes regardless of `foo()`'s behaviour. Mock at one hop
  out: the network, the database, the clock.
- **Tests describe behaviour, not implementation.** A test that breaks
  on internal refactors without a behaviour change is a maintenance
  cost. Write assertions against return values, side effects, and
  invariants — not against private call sequences.
- **No `assert True` placeholders.** If you don't know how to test
  the change, halt and ask rather than ship an empty test.
- **Stay inside the task envelope.** Don't refactor adjacent unrelated
  tests in this skill. Follow `mav-scope-boundaries`.
- **Tests must be deterministic.** No reliance on system time, random
  seeds, network availability outside the boundary under test, or
  ordering between independent tests.

## Return Protocol

`do-test` is a **subroutine of the calling workflow's
per-task loop** — not a terminal action. Returning from this skill is a
hand-back to the caller's next numbered step, not a completion event
(#106).

When you return from this skill, **do not** post a closing summary, do
not stop, do not treat green-tests as "task done." The calling
workflow's loop still owns, in order:

1. Closing the `skill-dispatch` interval that wrapped this invocation
   (`uv run maverick report end skill-dispatch … --outcome success`).
2. Conventional commit referencing the issue number, then push (with
   stacked-PR retarget if applicable).
3. Logging the commit row to the workflow report
   (`uv run maverick report commit …`).
4. Updating the tasks comment / closing the sub-issue.
5. Heartbeat refresh.

If you find yourself drafting a final summary after returning here,
that is the signal: scroll back to the calling workflow's per-task
loop and resume from the step immediately after the
`/do-test` invocation.

<!-- maverick-plugin-version: 4.0.2-dev -->
