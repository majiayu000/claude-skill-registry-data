---
description: Run tests with smart scoping by module, file, or filter
argument-hint: "[module | path | filter | all | quick]"
disable-model-invocation: true
allowed-tools: "Bash(composer *), Bash(vendor/bin/phpunit *), Bash(./vendor/bin/phpunit *)"
---

# Test Runner

Run the **minimum** scope for what changed. Prefer narrow over broad.

| Changed | Command |
|---|---|
| One module | `vendor/bin/phpunit tests/Unit/<Module>/` |
| One class | `vendor/bin/phpunit --filter <ClassName>` |
| One behavior | `vendor/bin/phpunit --filter test_method_name` |
| HTTP / DB code | `vendor/bin/phpunit --testsuite=feature` |
| Types only | `composer phpstan` |
| Anything before commit | `composer test` |

Available scripts:

```bash
composer test        # phpstan + phpunit — the gate
composer phpunit     # tests only
composer phpstan     # static analysis only
composer test:coverage   # HTML coverage into local/coverage
```

## Instructions

1. Empty `$ARGUMENTS` or `all` → `composer test`
2. `quick` → `vendor/bin/phpunit --testsuite=unit` (skip phpstan and feature suite)
3. `unit` / `feature` → `vendor/bin/phpunit --testsuite=$ARGUMENTS`
4. `phpstan` → `composer phpstan`
5. `coverage` → `composer test:coverage`
6. A module name (`Chat`, `Payment`, …) → `vendor/bin/phpunit tests/Unit/<Module>/`
7. A path → `vendor/bin/phpunit "$ARGUMENTS"`
8. Anything else → `vendor/bin/phpunit --filter "$ARGUMENTS"`

Report pass/fail counts. On failure, quote the assertion verbatim and name the file:line — do not paraphrase the error.
