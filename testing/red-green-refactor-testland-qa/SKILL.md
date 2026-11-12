---
name: red-green-refactor
description: "Use before changing code to fix a bug or add behavior, in any language, even when the user just says \"fix it\" or pastes a one-line function: reproduce the problem with a failing test first, watch it fail for the right reason, make the smallest change that passes, refactor, and show the test output before saying it is fixed or works."
---

# red-green-refactor

## Overview

Test-driven development (TDD) writes the test before the code, one small
behavior at a time. Martin Fowler's short form of the loop
([fowler-tdd][fowler]):

1. "Write a test for the next bit of functionality you want to add."
2. "Write the functional code until the test passes."
3. "Refactor both new and old code to make it well structured."

Kent Beck's [Canon TDD][canon] adds the step most people skip: start
from a written **list** of test scenarios and turn "exactly one item on
the list into an actual, concrete, runnable test" at a time.

For a coding agent, the loop is also the proof that a change works.
Anthropic's [Claude Code best practices][cc-bp] put it as "Give Claude a
check it can run" and "Have Claude show evidence rather than asserting
success: the test output". A test that was seen failing and then seen
passing is that evidence. A test written after the code and only ever
seen passing is not: it may pass for the wrong reason.

[fowler]: https://martinfowler.com/bliki/TestDrivenDevelopment.html
[canon]: https://tidyfirst.substack.com/p/canon-tdd
[cc-bp]: https://www.anthropic.com/engineering/claude-code-best-practices

## When to use

- Adding a function, endpoint, rule or option that has observable
  behavior.
- Fixing a bug: reproduce it as a failing test first (Step 6).
- Changing code that other code depends on, where "it still works"
  needs proof.
- Any time you are about to write "done", "fixed" or "this should work".

Not a fit: throwaway spikes (delete them, then test-drive the real
code), pure layout or styling (use a visual check), or a project with no
way to run tests yet. In that last case, set up the runner first and say
so; don't skip the loop silently.

Neighbors: `test-case-ideation-from-story` (qa-process) and
`boundary-value-generator` (qa-test-data) help fill the test list in
Step 2; the per-language unit-test skills (`python-unit-tests`,
`js-unit-tests`, `jvm-unit-tests`, `go-unit-tests`, `dotnet-unit-tests`)
cover the frameworks themselves; `test-code-conventions` (qa-test-review) reviews
finished tests. This skill owns the order of work and the evidence.

## Step 1 - Find the test command and run the suite once

Before changing anything, find how this project runs tests (README,
`package.json` scripts, `pyproject.toml`, `Makefile`, CI workflow) and
run the existing suite. Write down the result.

This baseline matters later: if three tests were already red before you
started, they are not yours, and you must not "fix" them by editing them
to pass. Say they were red at the start.

Commands to run **one** test, which the loop below uses constantly:

| Stack | Run one file or test | Source |
|---|---|---|
| pytest | `pytest tests/test_mod.py::test_func` | [pytest usage][pytest-usage] |
| Vitest | `npx vitest run foobar -t "name pattern"` | [vitest cli][vitest-cli] |
| Jest | `npx jest path/to/my-test.js -t "name pattern"` | [jest cli][jest-cli] |
| Go | `go test ./pkg/... -run 'TestParse$' -count=1` | `go help testflag`; [go test][go-test] |
| Maven Surefire | `mvn -Dtest=TestCircle#mytest test` | [surefire single test][surefire] |
| Gradle | `./gradlew test --tests SomeTestClass.someSpecificMethod` | [gradle testing][gradle] |
| .NET | `dotnet test --filter "FullyQualifiedName~MyTestsClass"` | [dotnet filter][dotnet] |
| Rust | `cargo test name_filter` | [cargo test][cargo] |

Per [go test][go-test], "The idiomatic way to disable test caching
explicitly is to use -count=1", which matters when you need to see a
test actually run red.

[pytest-usage]: https://docs.pytest.org/en/stable/how-to/usage.html
[vitest-cli]: https://vitest.dev/guide/cli.html
[jest-cli]: https://jestjs.io/docs/cli
[go-test]: https://pkg.go.dev/cmd/go#hdr-Test_packages
[surefire]: https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html
[gradle]: https://docs.gradle.org/current/userguide/java_testing.html
[dotnet]: https://learn.microsoft.com/en-us/dotnet/core/testing/selective-unit-tests
[cargo]: https://doc.rust-lang.org/cargo/commands/cargo-test.html

## Step 2 - Write the test list

Per [Canon TDD][canon], step 1 is "Write a list of the test scenarios
you want to cover". Write it in plain words, in your reply or a scratch
note, before any test code:

```text
parse_duration
- [ ] "90s" -> 90 seconds
- [ ] "1h30m" -> 5400 seconds (units combine)
- [ ] "" -> ValueError
- [ ] "5x" (unknown unit) -> ValueError naming the unit
- [ ] "-5m" -> ValueError (negative not allowed per spec)
```

Include the error cases and edges the request implies, not only the
happy path. Do not turn the whole list into test code now: Canon TDD
calls converting "all the items on the Test List into concrete tests"
up front a mistake, because the first passing test usually changes what
the rest should look like.

## Step 3 - Red: one test, run it, read the failure

Turn exactly one item into a test. Run **only that test** (Step 1
table) and read the output before writing any production code.

The test must fail, and fail for the right reason:

| What the run shows | Right red? | Next move |
|---|---|---|
| Assertion fails: expected `5400`, got `90`, or the function raises the wrong error | Yes | Go to Step 4. |
| `ImportError` / `cannot find module` / `undefined: ParseDuration` for the new function | Yes, for a brand-new function | Add an empty stub (raise "not implemented" or return a wrong value), re-run, and confirm the failure is now an assertion. |
| Syntax error, typo in a fixture name, wrong file path, test not collected ("no tests ran") | No | Fix the test until it runs and fails on its assertion. |
| The test **passes** | No | The behavior already exists or the test doesn't check it. Read the test again, tighten the assertion, or drop the item. |

A test you never saw fail proves nothing. If you only see it pass after
the change, you can't tell a real fix from an assertion that can't fail.

## Step 4 - Green: smallest change, then the whole suite

Change production code until the one test passes. Per Canon TDD:
"Change the code to make the test (& all previous tests) pass (adding
items to the list as you discover them)".

1. Re-run the single test. It must pass.
2. Run the **whole** suite. Everything that was green in Step 1 must
   still be green.
3. New ideas that came up ("what about `1H` in capitals?") go on the
   list, not into this step.

Rules while going green:

- Don't edit the test to match what the code returns. Canon TDD names
  "copying actual, computed values & pasting them into the expected
  values of the test" as a mistake. If the test itself was wrong,
  say so and fix it as a separate, stated decision.
- Don't delete or loosen an assertion to get green. Canon TDD: "Make it
  pass for real."
- Don't mock the unit under test, and don't special-case the test's
  input (`if s == "1h30m": return 5400`). The next list item would
  expose it, but the reviewer reading your diff sees a fake.

## Step 5 - Refactor while green

With every test green, improve names, remove duplication, extract
helpers, in both the new code and the code around it ([fowler-tdd][fowler]:
"Refactor both new and old code"). Fowler: "The most common way that I
hear to screw up TDD is neglecting the third step."

Run the whole suite after the refactor. Two limits from Canon TDD:
don't mix "refactoring into making the test pass", and don't refactor
"further than necessary for this session".

Then tick the item and go back to Step 3 with the next one, until the
list is empty.

## Step 6 - Bug fix: reproduce first

For a reported bug, the first test is the reproduction:

1. Write a test at the lowest level that shows the bug: the function,
   not the whole HTTP stack, unless the bug only exists in the stack.
2. Run it and confirm it fails **with the reported symptom** (same wrong
   value, same exception). A failure for any other reason means you
   haven't reproduced the bug yet.
3. Fix the code. Re-run: the reproduction passes, the suite stays green.
4. Keep the test, named after the behavior (`test_rounds_half_up_for_eur`),
   not the ticket alone, so it guards against the bug coming back.

The Claude Code best practices give the same order for symptoms: "write
a failing test that reproduces the issue, then fix it" ([cc-bp][cc-bp]).

## Step 7 - Prove it before calling it done

Finish with evidence, not adjectives. The final message states:

```markdown
**Tests**
- Red: `pytest tests/test_duration.py::test_combined_units` failed with
  `AssertionError: assert 90 == 5400` before the change.
- Green: same test passes after the change.
- Suite: `pytest` -> 47 passed (was 42 passed before; 5 new tests).
- Not verified: behavior on Windows paths (no Windows runner here).
```

- Quote the actual command and the actual counts from the run.
- List what was **not** run or not verifiable. "Should work" is not a
  result.
- If tests could not be run at all (missing dependency, no database),
  say exactly that and what the user must run, instead of reporting
  success.
- Tests that were red before you started (Step 1) are reported as such,
  not hidden and not "fixed" by editing them.

## Worked example

Request: "Add `parse_duration` to `timeutil.py` that accepts strings
like `90s`, `5m`, `1h30m` and returns seconds."

1. Step 1: `pytest` -> `12 passed`. Baseline recorded.
2. Step 2: test list as in the example above (5 items, two of them
   error cases).
3. Red: `test_seconds_only` asserts `parse_duration("90s") == 90`.
   `pytest tests/test_timeutil.py::test_seconds_only` ->
   `ImportError: cannot import name 'parse_duration'`. A stub
   `def parse_duration(s): raise NotImplementedError` turns it into a
   real failure: `NotImplementedError`.
4. Green: parse `(\d+)([hms])` pairs and sum them. Single test passes;
   `pytest` -> `13 passed`.
5. Next item `test_combined_units` (`"1h30m" == 5400`) already passes,
   because the regex loop handled it. Per Step 3, the item is dropped as
   covered, not kept as a test that never failed.
6. `test_empty_string_raises` fails (`assert` on `pytest.raises` not
   raised: the loop returned `0`). Add the guard; green; refactor the
   unit table into a dict; `pytest` -> `15 passed`.
7. Final message: the evidence block from Step 7, listing the three red
   runs, the green runs and `15 passed` (was 12).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Writing the code first, then tests that pass on the first run | Nothing shows the tests can fail; they may assert nothing useful | Red first (Step 3) |
| Writing every test up front, then making them pass | Canon TDD calls this out; the first design choice reshapes the rest | One item at a time (Step 2) |
| Editing expected values to what the code returns | Locks the bug into the test | Fix the code, or state that the test was wrong (Step 4) |
| Deleting or loosening assertions to get green | The suite passes and proves nothing ("Make it pass for real") | Step 4 rules |
| Tests with no assertions "for coverage" | Canon TDD: "write tests without assertions just to get code coverage" is a mistake | Every test asserts the behavior on its list item |
| Running only the new test before claiming done | Breaks elsewhere stay hidden | Whole suite in Steps 4 and 5 |
| "Fixed, should work now" with no output | The reader can't tell what ran | Evidence block (Step 7) |
| Refactoring while a test is red | Two changes at once; a failure can't be attributed | Refactor only on green (Step 5) |

## Limitations

- TDD drives design for code with observable behavior. Visual layout,
  performance and exploratory questions need other checks.
- The loop is only as good as the test list. Pair it with
  `boundary-value-generator` or `test-case-ideation-from-story` when the
  input space is large.
- Slow suites tempt skipping the full run. Run the affected package
  during the loop and the full suite once before Step 7, and say which.
- Legacy code with no seams may need a characterization test of current
  behavior before the first red test; record it as such.

## References

- [fowler][fowler] - Martin Fowler, "Test Driven Development": the
  three steps and neglected refactoring.
- [canon][canon] - Kent Beck, "Canon TDD": test list, one test at a
  time, and the listed mistakes.
- [cc-bp][cc-bp] - Anthropic, Claude Code best practices: give Claude a
  check it can run, show evidence, reproduce a bug with a failing test.
- [pytest-usage][pytest-usage], [vitest-cli][vitest-cli],
  [jest-cli][jest-cli], [go-test][go-test], [surefire][surefire],
  [gradle][gradle], [dotnet][dotnet], [cargo][cargo] - single-test
  commands in Step 1. Go `-run`: `go help testflag`.
