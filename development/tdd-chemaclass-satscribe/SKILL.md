---
description: Implement a feature test-first with strict red-green-refactor
argument-hint: "<what to build>"
disable-model-invocation: true
allowed-tools: "Read, Write, Edit, Glob, Grep, Bash(vendor/bin/phpunit *), Bash(composer *), Task"
---

# TDD Workflow

Implement `$ARGUMENTS` test-first. Never skip red.

Test conventions (suites, mocking, naming) are in `.claude/rules/testing.md` — read it, don't re-derive.

For a multi-step feature where you want the discipline enforced turn by turn, delegate to the **`tdd-coach`** agent instead.

## RED

1. Identify module and layer — Action in `Application/`, value object in `Domain/Data/`, repository in `Infrastructure/Repository/`.
2. Declare the interface in `Domain/` first. That is the requirement, written down.
3. Write **one** failing test. `tests/Unit/<Module>/` unless it needs DB or HTTP, then `tests/Feature/`.
4. Run it and confirm it fails **for the right reason**:
   ```bash
   vendor/bin/phpunit tests/Unit/<Module>/<Name>Test.php
   ```
   Passing now means it proved nothing — fix the test, not the code.

## GREEN

5. Minimal implementation. No speculative branches, no extra methods.
6. Add the `$singletons` binding.
7. Re-run.

## REFACTOR

8. Improve naming, extract methods, remove duplication — green after every step.
9. Gate:
   ```bash
   composer test
   ```

Loop back to RED for each additional behavior. Never batch several tests before implementing.
