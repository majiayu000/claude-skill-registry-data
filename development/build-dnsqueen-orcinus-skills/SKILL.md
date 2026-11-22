---
name: build
description: Build one slice at a time, test first, with the four checks and independent verification before commit. Use when a scaffolded project exists and a slice from the calibrated brief is next. Only invoke via the orcinus router.
license: MIT
user-invocable: false
---

# BUILD — one slice at a time, test first

Build the next slice from the calibrated brief. One behaviour, one test, one minimal implementation, one commit. Do not build the whole project in one step. Do not claim done until orcinus-verify passes.

## Rules

- One slice at a time. A slice is one behaviour with acceptance criteria from the brief.
- Test first. Red before green, always.
- Test at seams. A seam is the public boundary where behaviour is observed, not internals.
- No tautological tests. Expected values come from an independent source — a known literal, a worked example, the spec — never recomputed the way the code does it.
- No hard-coding for tests. The solution must work for all valid inputs, not just the test cases.
- No test weakening. Never delete, weaken, or skip a test to make the suite pass.
- No scope creep. Touch only the files the slice needs.
- No one-shot implementation. If you are about to write the whole feature at once, stop and cut a smaller slice.

## Steps, in order

### 1. Pick one slice

Read the calibrated brief. Pick the smallest next slice with acceptance criteria. Write down the seam you will test at, in one line, and confirm it with the user before writing any test. No test at an unconfirmed seam. If there are no acceptance criteria, stop and ask for them.

### 2. Red: write one failing test

Write one test at the seam, with expected values as literals from the spec. Run it. Watch it fail. Record the failure. If it passes before any code exists, the test is wrong — fix the test, not the code.

### 3. Green: implement the minimum

Write the smallest code that makes the test pass. No speculative features, no extra files, no "for later" code. The smallest complete change — the ponytail rule, applied from build's own loop (ponytail itself is external-optional, not in this repo; see the router's rules.md). If the code needs a design decision the brief does not answer, ask the user instead of guessing.

### 4. Run the four checks

Run, in order, and record the real output and exit code for each:

1. `build`
2. `lint`
3. `typecheck` (if the project has one — the ORCINUS scaffold always sets one up, so a missing typecheck in a scaffolded project is a finding)
4. `test` (full suite, not only the new test)

All four must pass. If any fails, fix only the cause and re-run all four from the top. After 3 failed loops, stop and hand back to the user.

### 5. Check the tests themselves (mutation)

After the slice passes its tests, check the tests themselves with mutation-testing before calling it done. Run it on the slice's changed files (or the whole suite for a small project). If a mutant survives, the test suite has a gap — strengthen the test (never weaken it) and re-run. A slice is not done while its tests can be fooled.

No mutation tool is bundled in this repo: for JavaScript/TypeScript use Stryker via the mutation-testing skill, and for Python use mutmut via the mutation-testing-python skill — both installed externally (Stryker is declared only as a devDependency of the demo project; mutmut is pinned nowhere in this repo). For any other language, the slice is INCOMPLETE with a recorded reason — name the language, state that no mutation tool is bundled for it, and record what was checked instead (for example, the new tests were each shown to fail when their assertion is inverted, or when the code they cover is reverted). Do not claim the tests are strong when no mutation run proved it. If the project is small or the slice is trivial, run mutation on the changed files only (Lite mode) instead of the whole suite — Stryker is slow, and a full run on every slice is not the point.

### 6. Verify independently

Run orcinus-verify. It reads the code and the evidence, not your summary. If it says FAIL, fix the finding and re-verify from step 4. Do not commit while verification is failing.

### 7. Commit one slice

One commit per slice, with a clear message naming the behaviour. Then record progress: what is done, what is next, what is blocked. End the session in a clean state.

## If you get stuck

Do not guess. Use the diagnosing-bugs loop: first build a tight feedback loop that reproduces the failure (a failing test or a minimal command), and only then form a hypothesis. No hypothesis before the loop.

## What build is not

Not a plan for the whole project. Not a place to add features the brief did not ask for. Not a shortcut around the four checks or verification.

## Sources

Method, in our own words, inspired by: tdd (mattpocock/skills, MIT, external-optional — not in this repo; build's own test-first loop is the fallback, see the router's rules.md) for the red-green loop, seams, and anti-patterns; ponytail (external-optional, not in this repo — the "smallest complete change" rule is applied from build's own loop) for the smallest complete change; planning-and-task-breakdown (addyosmani/agent-skills, MIT) for cutting slices; clean-code (wondelai/skills, MIT) for readable code. No text was copied from those projects.
