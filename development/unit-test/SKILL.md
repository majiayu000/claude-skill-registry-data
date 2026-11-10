---
name: unit-test
description: Write or extend Catch2 + FFF unit tests for a module of the framework under tests/, build and run them, and report coverage. Use when the user asks to test a header or module, or to add tests for new or changed behaviour.
---

# Unit test Skill

Read `docs_llm/LLM_GUIDE.md` first.

## Most important rules
- Write tests only. Never change the code under test, its header or its comments. If a test finds a bug, report it with file and line; do not fix it.
- Never weaken or delete an existing test to make a run pass.
- Statics persist across test cases. Reset all module state in the fixture constructor and undo it in the destructor, or the next test fails for the wrong reason.
- Follow `AGENTS.md`: no `malloc`/`free`/`new`; check every return value with `CHECK` or `REQUIRE`, never cast it to `(void)`.
- Goal: at least 90% line coverage AND at least 90% branch coverage of every source file under test. If you cannot reach it, stop and report it to the human (see "Build, run and coverage"). Never reach the number by weakening tests, by tests that assert nothing, or by changing the code under test.

## Inputs
- Header path of the module, normally `inc/<layer>/<module>/ez_<module>.h`.
- Optional: the behaviour to cover (new feature, bug fix, list of functions).

## Steps
1. Read the header and the implementation `src/<layer>/<module>/ez_<module>.c` completely. For each public function list: every return value and its cause, argument checks, state changed, callbacks invoked, and what happens when a dependency fails.
2. Find the existing test and extend it. Test folder and file names often differ from the header (e.g. `inc/service/data_model/ez_data_model.h` is tested in `tests/service/datamodel/unittest_ez_datamodel.cpp`). Use `Glob tests/**/*unittest*<module>*` or `Grep -rl "<first function name>" tests/`.
3. If none exists, create `tests/<layer>/<module>/unittest_ez_<module>.cpp` from `.claude/skills/unit-test/template.cpp`, and copy `CMakeLists.txt` from a sibling module under `tests/` with the names replaced (`ez_<module>_test`). Register the folder in `tests/CMakeLists.txt` under `if(ENABLE_EZ_<MODULE>)`. Match the style of one neighbouring test of the same layer.
4. Write a one-line-per-behaviour test plan, then the tests (see "What to cover").
5. Build, run and check coverage with the script (see below). Fix the test, not the code under test. Each test must pass on its own, in any order.
6. If line or branch coverage is below 90%, read the uncovered lines and the lines with branches not taken, add tests for the behaviours they belong to, and run the script again. Repeat until the goal is met. If the remaining lines cannot be reached from the public API, stop and report to the human.
7. Prove the tests can fail (see below).
8. Report.

## What to cover
- Every public function: invalid arguments (exact error code, no state change), the success path (return value, state, arguments forwarded to a dependency via FFF `argN_val`), and each error path (force the fake to fail, check the code and that the module is still usable).
- A missing optional dependency (NULL function pointer), and calls in the wrong order (not initialized, busy, already registered).
- Callbacks: called once, with the right arguments and in the right state, not called when none is registered, and a callback that starts a new operation.
- Boundaries: limits, buffer sizes, empty and full.

Style: BDD (`TEST_CASE_METHOD`, `WHEN`, `THEN`, `AND_WHEN`), tag `"[<layer>][<module>]"`. Use `REQUIRE` for setup and `CHECK` for the assertions under test. Use fakes for hardware and OS; never sleep or wait for wall-clock time. Simulate an ISR by calling the function the interrupt would call.

## Build, run and coverage
Run from anywhere; the script finds the repository root:
```
.claude/skills/unit-test/scripts/run_tests.sh [-t 90] ez_<module>_test <source file> [<source file> ...]
```
Example: `run_tests.sh ez_spi_test src/hal/spi/ez_spi.c`. It configures and builds the `linux_test_debug` preset (32-bit, strict warnings: fix every warning in the test), runs only that test with ctest, and prints the line and branch coverage of each source file with the uncovered lines and the lines whose branches are not all taken. The HTML report is in `coverage/<test_name>/index.html`. The threshold applies to line coverage and to branch coverage of each source file; a file without branches only needs the line coverage.

| Exit code | Meaning | What to do |
|-----------|---------|------------|
| 0 | Build ok, tests pass, line and branch coverage >= threshold | Continue |
| 1 | Configure or build failed, or a test failed | Fix the test. If the failure is in another module, do not fix it: use the manual build below and report it |
| 2 | Tests pass but line or branch coverage is below threshold | Add tests for the uncovered lines and the branches not taken (step 6). If you cannot reach the threshold, stop and report it to the human |
| 3 | Tool missing, bad arguments, or no coverage data for a file | Fix the call. No data means the test does not run that file |

**When coverage cannot reach a minimum value of 90%**, do not lower the threshold and do not hide lines or branches. Stop and tell the human: the achieved line and branch percentages, the uncovered lines and the branches not taken of each file, and for each group why it is unreachable or untestable (for example a defensive branch that the public API cannot trigger, a hardware-only path, or code that needs a change in the module to be testable). Let the human decide.

**Manual build when the full build fails in another module:** compile the module source and your test with `--coverage -m32` and the `-D`/`-I` flags from `build_linux_test_debug/compile_commands.json` into a scratch directory, link with the libraries of the existing build (`libez_utilities_lib.a`, Catch2), run the executable, then evaluate the result with `run_tests.sh --coverage-only --build-dir <scratch dir> <test_name> <source file>`. Say in the report that the full build did not run and why.

## Prove the tests can fail
Change one behaviour of the code in a temporary copy (skip a release, drop a NULL check, return a wrong code), build the copy, and confirm at least one test fails. Delete the copy afterwards. A test that cannot fail does not count.

## Report back
- Files created or changed.
- Behaviours covered, per function.
- Build and ctest result (test cases, assertions, failures with output), and whether the full build ran.
- Line and branch coverage of each source file and whether the 90% goal is met for both. If not met: the uncovered lines and branches and why, for the human to decide.
- Result of "Prove the tests can fail".
- Bugs or doubtful behaviour found in the code under test, with file and line.
- Anything you could not run or verify.
