---
name: mutation-testing-python
description: Check whether Python tests actually catch bugs by mutating the code and seeing if the tests fail. Use after a Python slice passes its tests, before calling it done, and whenever a Python test suite looks green but unproven. Python only. Only invoke via the orcinus router.
license: MIT
user-invocable: false
compatibility: Requires Python 3.11+, pytest, and mutmut 3.x; install with pip install mutmut pytest.
---

# MUTATION-TESTING-PYTHON — do the Python tests catch anything?

A green test suite proves nothing on its own. A test that passes no matter what the code does is not a test. Mutation testing proves the tests: change the code in small ways (mutants) and check whether the tests fail. A mutant the tests kill is proof the tests work. A mutant that survives is a gap in the tests — record it, do not hide it. This is the Python companion of `mutation-testing` (JavaScript/TypeScript, Stryker); the discipline is the same, the tool is different.

## Rules

- Baseline first. Run the test suite before mutating. If it is not green, stop — mutation testing on a broken suite measures nothing.
- Never weaken a test to raise the score. A surviving mutant is fixed by adding or strengthening a test, never by deleting the mutant or the test.
- Never report a score without running. A score from memory, from another project, or from a failed run is not a score.
- A surviving mutant is a finding, not a failure to hide. List every one, with file and line.
- A check that did not run is never reported as passed.

## Steps, in order

### 1. Baseline

Run the test suite (for example `pytest tests -q`). Record the output. All tests must pass. If not, stop.

### 2. Run mutmut as-is

Use mutmut (boxed/mutmut, BSD-3-Clause) as-is. Do not rewrite it, and do not hand-roll mutants when mutmut can generate them.

- Install: `mutmut` and `pytest` (a virtual environment, never `--break-system-packages` on an externally managed Python).
- Configure (`setup.cfg`, `[mutmut]` section): `source_paths` lists the files to mutate; `pytest_add_cli_args_test_selection` lists the tests. Do NOT use the deprecated keys `paths_to_mutate` and `tests_dir`, and do NOT set `test_command` — mutmut 3.x ignores it and runs pytest itself.
- Layout: the code must be importable by its own package name. A module imported as `src.budget` breaks mutmut's trampoline (`Module name starts with 'src.', which is invalid`). Use a real package (for example `src/demo_budget/budget.py`, imported as `demo_budget.budget`, with `PYTHONPATH=src` for the local test run).
- Run it (`mutmut run`). Record the full output.

### 3. Read the score

Record the exact numbers from `mutmut export-cicd-stats` (it writes `mutants/mutmut-cicd-stats.json`): total, killed, survived, timeout, suspicious, skipped, no_tests. The score is killed divided by total. Record mutmut's own numbers, do not recompute them by hand.

### 4. Prove the check can fail

The report must name at least one mutant the tests killed, with file, line, and what changed. If no mutant was killed, the check proved nothing — say so, and do not call the suite tested.

### 5. List every surviving mutant

For each surviving mutant, record file, line, the change, and what test is missing. Each one is a test gap. Fix the gaps by adding tests (one slice at a time, test first), then re-run mutmut and record the new score. Do not delete code to make a mutant disappear, and do not mark a mutant as ignored without writing down why.

## Report

Return the report in this form:

- Baseline (test output).
- mutmut version and config (source_paths, test selection).
- Mutation score with the exact numbers.
- Killed mutants (at least one, with file and line).
- Surviving mutants (every one, with file, line, and the missing test).
- Verdict: PASS (score recorded, at least one mutant killed, all survivors listed) or FAIL (mutmut did not run, no mutant killed, or survivors hidden).

## Scope

Python only. Other languages are still a gap — each needs its own verified CLI. The Trail of Bits mutation-testing skill (CC-BY-SA-4.0) is a separate licensed module, not copied here; it is referenced, not used.

## Sources

Method, in our own words, using mutmut (boxed/mutmut, BSD-3-Clause, licence verified from the primary LICENSE file) as-is. No text was copied from mutmut. The discipline mirrors `mutation-testing` (Stryker, JavaScript/TypeScript) in this repo.
