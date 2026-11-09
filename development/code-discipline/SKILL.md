---
name: code-discipline
description: >
  Apply whenever writing or editing code. Extract pure functions, test each
  new file as it's written, reuse existing helpers over new ones, keep
  values in shared types/config, work in small verified steps.
---

# Code Discipline

## 1. Extract pure functions

Pull deterministic, side-effect-free logic out of components and handlers
into standalone functions - even with only one caller today.

## 2. Test with the file, not after

Write each new file's test in the same step as the file. Never defer tests
to a later pass across several files.

Exception: skip a test with no real failure mode to guard (a trivial
one-liner, no branch, no edge case) - state why in one line.

## 3. Reuse before you add

Search for an existing convention, utility, or shared helper first. Reuse
it instead of writing a parallel version - covers patterns (error shapes,
service structure), not just literal functions.

## 4. No local constants for shared concepts

Check for an existing shared type, enum, or constants module before adding
a hardcoded list or value to a file. Use the shared one.

Exception: a literal may stay inline only if it has no meaning outside that
one function or component.

## 5. Verify in small steps

Split implementation into pieces small enough to verify individually
(build, test, or a quick check) before moving to the next. Never implement
several files in one unverified pass.
