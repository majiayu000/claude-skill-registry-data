---
name: write-tests
description: Write focused, fast tests that cover behaviour, edges, and failures.
trigger: when the user asks for tests or to improve coverage
---
## When to use
The user wants tests for some code, or asks to raise coverage.

## How
1. `read_file` the target so tests match the real API.
2. Put tests in `tests/test_<module>.py`; plain `pytest`, minimal fixtures.
3. Cover the happy path, one edge case, and one failure/error path.
4. Keep each test small, independent, and named for what it asserts.
5. Assert on behaviour and return values, not internal calls.

## Avoid
- Testing implementation details that break on harmless refactors.
- Giant fixtures or shared mutable state across tests.
- Tests that assert nothing meaningful ("it runs").

## Done well
A handful of small tests that fail loudly when behaviour breaks and pass quietly
otherwise — plus a note on what you covered and what you left out.
