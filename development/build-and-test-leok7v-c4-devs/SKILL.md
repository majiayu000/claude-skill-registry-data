---
name: build-and-test
description: Rebuild cx and run the full dual-path test suite. Use
  after any change to cx.c, toys.c, or tests/*.c. Passes only when
  every test returns 45/45 under both native and self-hosted paths.
allowed-tools: Bash, Read
---

# build-and-test

The project's single verification gate. `tests/all.c` runs every
test twice — once natively (`build/cx <file>`) and once through
self-hosted cx (`build/cx cx.c <file>`). A change is not done until
both paths report `SUMMARY: 45/45 tests passed.`

## The command

    cc -Wall -Wpedantic -o build/cx cx.c && build/cx cx.c tests/all.c

That's it. No flags, no selection — run the whole suite. Selecting
a subset hides regressions in other tests the change might have
broken by accident.

## Reading the output

The suite prints per-stage headers and per-test OK/FAIL lines. The
line to grep for at the end is:

    SUMMARY: N/45 tests passed.

- `45/45`: done. Report success and stop.
- `<45/45`: regression. Find the first `FAIL:` line (or the first
  stage that shows lower counts on its second pass), that's where
  the self-host path diverged.

## When it fails under self-host only

A test that passes natively but fails the second time through is
almost always hitting one of the patterns in
`.claude/rules/cx-constraints.md`:

- stacked case labels
- break inside braced switch case
- local shadowing a non-zero global
- bytecode overflow of `code_pool`
- a stubbed `#else __cx__` intrinsic branch

Narrow the failing test to the smallest repro, then check which
pattern fits.

## What not to do

- Don't `--no-verify` or `-w` your way around warnings. Fix them.
- Don't skip tests because they're "flaky." The suite is
  deterministic; flakiness means a real bug.
- Don't claim success on partial runs.
