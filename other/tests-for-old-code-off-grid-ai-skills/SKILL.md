---
name: tests-for-old-code
description: Add end-to-end tests to code that has none, in tiers by confidence, and run every test before handing it over. Use before refactoring untested code, after inheriting a project, or when the user says "add tests for this flow", "write e2e tests for login" or "we have no tests for X".
---

# Tests for old code

Old code has no spec, so the tests pin down what it does today. Hold every test to `test-like-a-user`: real screens and real calls, faking only the network edge and the device.

## 1. Understand the flow
Ask what flow to cover if it isn't clear. Then find its entry points (routes, screens, handlers), what it calls and what it writes, and one existing test to copy the style and runner from. Use `learn-this-codebase` if there's no map.

## 2. Plan in tiers
- **Tier 1, sure:** the main path, with behaviour you can see in the code. These must pass.
- **Tier 2, likely:** edge cases and errors where the intended behaviour is a guess. Ask the user up to 3 yes/no questions to settle them.
- **Tier 3, hints:** security, performance and anything you can't run here. A checklist, not code.

Show the plan and ask which tiers to write.

## 3. Write, run, fix
For each tier the user chose:
1. Write it in the project's runner and style, next to its other tests.
2. Run it.
3. If it fails, read the error and fix the test, up to 3 times. If the code is what's wrong, stop and tell the user: that's a bug you found, not a test to bend.
4. Still failing after 3 tries: move it to Tier 3 with what you learned.

Never loosen an assertion or raise a timeout to get green.

## 4. Hand over
A short report: each test, its tier, pass or moved, and what it covers. Tier 3 items as a checklist. Any bugs found, first.
