---
name: tests-are-code
description: "Use when writing, reviewing, or deleting tests. Tests get the same care as production code. Fast, independent, repeatable, self-validating, written at the same time as the change. One concept per test. Delete tests that guard deleted behavior."
disable-model-invocation: true
kind: principle
---

# Tests are code

Dirty tests are worse than no tests. They rot, someone deletes them, and then everyone's afraid to change anything. Clean tests let you refactor without fear, and that's what makes every other rule in this stack possible.

## FIRST

- **Fast.** Runs in seconds. A slow test doesn't get run, and a test that doesn't get run doesn't exist.
- **Independent.** No test depends on another having run. Any order, any subset, same result.
- **Repeatable.** Same result every run, on every machine, with no network and no clock. A flaky test is a broken test.
- **Self-validating.** Pass or fail, no human reading output to decide.
- **Timely.** Written with the change, not after. For a bug, before the fix, so you watch it go red then green.

## One concept per test

A test checks one thing and its name says what. If the name has "and" in it, it's two tests. When it fails, the name alone should tell you what broke.

## What isn't coverage

- **A pile of smoke tests.** "It doesn't crash" is not a test of behavior.
- **Tests that guard deleted features.** When the behavior goes, its tests go with it. Tests protecting how an old implementation worked inside protect nothing.
- **Tests that mirror the code.** If the test restates the implementation line by line, changing the code means changing the test the same way, and the test caught nothing.

## Fast tier and full tier

Every project splits tests into what runs in seconds and what takes the long wall. The fast tier runs before and inside the review loop. The full tier runs once at the end. Which tests go where is the only per-project decision.

## The test

Would you be comfortable refactoring this module with only these tests to catch you? If not, the tests aren't done.
