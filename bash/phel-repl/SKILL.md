---
description: Evaluate a Phel expression to verify behaviour without writing a test
argument-hint: "<phel expression>"
disable-model-invocation: true
allowed-tools: "Bash(./vendor/bin/phel *), Bash(vendor/bin/phel *), Bash(timeout *)"
---

# /phel-repl

1. Take the expression from `$ARGUMENTS` (ask if empty).
2. Eval via the Phel CLI:
   ```bash
   timeout 10 vendor/bin/phel eval "$ARGUMENTS"
   ```
3. For multi-line snippets or `(require phel.pdo)` setup, drop into a scratch file:
   ```bash
   printf '%s\n' '(ns repl-scratch (:require phel.pdo))' '$ARGUMENTS' > /tmp/phel-pdo-repl.phel
   timeout 10 vendor/bin/phel run /tmp/phel-pdo-repl.phel
   ```
4. Report the result. On error, name the layer (resolution / interop / DB).

## Examples

```
/phel-repl (pdo/get-available-drivers (pdo/connect "sqlite::memory:"))
/phel-repl (pdo/quote (pdo/connect "sqlite::memory:") "I'm fine.")
```
