---
name: bats-fixture-full-validation
description: >-
  Use when a Bats helper, stub or fixture in `tests/bats/` has been edited and the change is about
  to be staged. Symptoms include a filtered `bats -f "pattern"` run passing while the full suite
  fails, a helper name defined twice in one file, and a ShellCheck `SC2329` unreachable-function
  warning on the first of the two definitions.
---

# Bats Fixture Full Validation

## Profile keys consumed

- None — this skill is independent of the profile. The Bats suite target and the ShellCheck target
  have no logical key in the profile schema, so both are named by purpose here and shown as
  concrete commands only inside `# profile-example` fences.

## Overview

Bats helpers and stubs are shared state across every test in the file. A filtered run executes only
the matching tests, so a shadowed or broken helper stays invisible exactly when it matters: the
tests that would have caught it never run.

## When to use

- A helper function, command stub or shared setup in `tests/bats/` was edited.
- Iteration used `bats -f "pattern"` to focus one case, and the change is about to be staged.
- ShellCheck reports `SC2329` (function never invoked) on a helper that is obviously used.
- Two definitions of the same helper name exist in one file and it is unclear which one wins.
- Not for: editing a single `@test` body that touches no shared helper, and not as a substitute for
  fixing the shadowing — a green full run does not un-duplicate a definition.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): yes — the repository's Bats suite target runs the whole `tests/bats` tree in the dev
  container, helpers live in `tests/bats/test_helper.bash`, and the repository's shell-lint target
  ShellChecks `tests/bats/*.bash` at `--severity=warning`, which is where `SC2329` surfaces.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — the Bats suite
  target and `tests/bats/test_helper.bash` (plus a `fixtures/` directory) work the same way, but
  there is no ShellCheck target, so the static half of the signal has to come from running
  ShellCheck directly.
- **Component-library shape** (Storybook-first, no bootable app, published package): partial — the
  Bats suite target and `tests/bats/test_helper.bash` are present; again no ShellCheck target.

## Procedure

1. Iterate with a filter while writing the case:

   ```bash
   bats -f "lint-commit-range" tests/bats/ci_scripts.bats
   ```

2. Before staging any change to a helper, stub or fixture, run the whole suite through the
   repository's Bats suite target — not the filtered subset:

   ```bash # profile-example
   make test-bats
   ```

3. Read the ShellCheck output for the helper files as well, via the repository's shell-lint target.
   `SC2329` on a function that is plainly called means a later definition of the same name shadows
   it, and the first body is dead.

   ```bash # profile-example
   make lint-shell
   ```

4. Fix by removing the duplicate, or by merging the two into one definition that takes an optional
   parameter for whatever differed. Do not keep both and rely on definition order.
5. Re-run the full suite and confirm every test passes, including the ones that consume the changed
   helper. Only then stage.

## Why a filtered run cannot see it

In Bash, a second `function name() { … }` in the same file silently replaces the first, so:

- Tests that call the name get whichever definition was sourced last.
- Tests that never call the name are unaffected and stay green.
- A filter that excludes the callers passes vacuously — the suite reports success for a fixture it
  never exercised.

A second command stub added next to an existing one is the common shape: the focused test does not
call the stub, so the filtered run is green, and the full suite fails as soon as a test that does
call it picks up the wrong body.

## Common mistakes

- Treating the filtered green run as verification — it proves only that the filtered tests pass.
- Adding a second stub definition "temporarily" — order-dependent behaviour outlives the intent.
- Ignoring `SC2329` because the function is obviously used — that is precisely the shadowing signal.
- Re-ordering the definitions so the wanted body wins — the duplicate is still there and the next
  edit reintroduces the bug; delete or merge instead.
- Relying on ShellCheck alone — it is a partial static signal; the full suite is the canonical
  validator because it exercises the interdependencies.
