---
name: timermeet-easyphp-builder
description: Implement and modify the TimerMeet EasyPHP web app. Use when changing PHP, JavaScript, CSS, timers, alarms, local persistence, translations, or UI behavior in this project, especially when compatibility with EasyPHP 14.1 and PHP 5.4 must be preserved.
---

# TimerMeet EasyPHP Builder

## Overview

Implement features and fixes in `TimerMeet` without breaking the local EasyPHP runtime. Keep changes scoped, compatible with `PHP 5.4.31`, and verified with local syntax and HTTP checks.

## Workflow

1. Run `git rev-parse --show-toplevel` and locate `monitoreos/timermeet`.
2. Read `SDD.md` before changing behavior that affects product scope or validation.
3. Inspect the current implementation files:
- `index.php`
- `assets/app.js`
- `assets/styles.css`
- `api/meetings.php`
- `data/meetings.json`
4. Implement the smallest change that satisfies the request.
5. Bump the asset version in `index.php` whenever `JS` or `CSS` changes could be cached by the browser.
6. Read `references/validation.md` and run the relevant checks before finishing.
7. Update `SDD.md` and `README.md` when user-visible behavior changes.

## Hard Constraints

- Do not use modern PHP syntax such as scalar type hints, return types, nullable syntax, or `declare(strict_types=1)`.
- Keep the default storage model file-based and local.
- Keep browser fallback storage unless the user explicitly removes it.
- Comment only the code that would otherwise be hard to parse quickly.
- Preserve Spanish as the default language and keep English support working.

## References

- Read `references/validation.md` when you need the exact EasyPHP validation commands.
