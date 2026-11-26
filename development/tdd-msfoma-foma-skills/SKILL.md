---
name: tdd
description: >-
  Builds a change test-first in red-green slices. Use when the user asks for tests first, TDD, a test-driven change, or a regression test for a bug fix. Not for plain "add a function", review or debugging.
license: Apache-2.0
metadata:
  level: "atomic"
  uses: ""
  agents: ""
  tokens: "476"
---

Write a failing test, see it fail for the right reason, add the minimum code to pass it, repeat one behaviour at a time.

Path: one small behaviour on a named function → steps 1, 3–5 once; several behaviours, a bug fix or an unclear interface → the full loop. Say which path in one line.

## Steps
1. Test command: `## Commands` in the project's CLAUDE.md. If missing, detect it (package.json, Makefile, pyproject.toml, Cargo.toml); if none, say so and ask how to run tests.
2. Agree the seam: the public interface to test at, ideally one. If the user named the function or interface, that is the seam; state it and go on. Otherwise propose one, with a line on what it catches and misses, and ask.
3. Pick the next behaviour. Write one test for it through that seam. Take the expected value from the spec or a hand calculation, never from the code under test.
4. Run that test. It must fail (not error) because the behaviour is missing. Passes or fails oddly: fix the test.
5. Write the least code that passes. Run it, then the rest of the suite.
6. Repeat from 3 for the next behaviour. Bug fix: the first test reproduces the bug.
7. Refactoring happens after green, as a separate step, not inside the loop.

## Rules
- One slice at a time: one test, then its code. Never write all tests first, never code ahead of a test.
- Never edit, skip or weaken a test to make it pass; fix the code.
- Test behaviour through the public interface, not private methods or internals; a refactor must not break the test.
- Proportional: new non-trivial logic gets a test; renames, config and copy changes get none.
- Code you wrote before its test: delete it and redo test-first. Do not keep it as reference.

If a test needs a mock, a fake or heavy setup, read `references/mocking.md`.

## Report
- Tests added, each seen failing then passing; suite result.
- Not checked: <behaviours or edge cases without a test>
