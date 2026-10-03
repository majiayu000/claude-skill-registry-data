---
description: Run rector, php-cs-fixer, and phpstan; fix what static analysis reports
argument-hint: "[optional path]"
disable-model-invocation: true
allowed-tools: "Read, Edit, Bash(composer *), Bash(vendor/bin/*), Bash(./vendor/bin/*)"
---

# Fix Code Style

PHP files edited during a session are auto-formatted by the PostToolUse hook. Use this for a full sweep or when phpstan is failing.

## Instructions

1. **Auto-fix**:
   ```bash
   composer fix   # rector + php-cs-fixer
   ```

2. **Review what rector changed** — it applies dead-code and code-quality sets and can be aggressive. Read the diff before keeping it:
   ```bash
   git diff
   ```

3. **Static analysis**:
   ```bash
   composer phpstan
   ```

4. **Fix each phpstan error at the source.** Never silence a real type problem with `@phpstan-ignore`.

   | Error | Fix |
   |---|---|
   | Missing return type | Add it, `void` included |
   | `array` without shape | `@param list<int>` / `@return array<string, mixed>` |
   | Possibly null | Early return, or narrow the type |
   | Unknown Eloquent magic | Larastan usually knows it — check the model's `@property` docblock |

5. **Verify nothing broke**:
   ```bash
   composer test
   ```

## Checklist for new files

- `declare(strict_types=1);` present
- `final` unless inheritance is used, `readonly` where immutable
- Constructor property promotion, all params typed
- Interface in `Domain/`, implementation in `Application/` or `Infrastructure/`
