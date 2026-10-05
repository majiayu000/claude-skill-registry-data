---
name: runner-selection
description: Bootstrap Laravel projects by detecting Sail or host tooling, verifying dependencies and services, and choosing consistent PHP, Composer, Node, and test commands.
tags:
  - laravel
  - php
---

# Runner Selection

Use this skill before executing Laravel commands in an unfamiliar repository. It consolidates the former `bootstrap-check` skill into one environment-detection workflow.

## Detection Order

1. Read project instructions for required containers, wrappers, or task runners.
2. Check for `vendor/bin/sail`, Docker Compose files, and a Sail dependency in `composer.json`.
3. Check whether the expected containers are already running and whether required services are healthy.
4. If Sail is absent, verify host `php`, `composer`, `node`, and the selected package manager.
5. Inspect `composer.json`, lock files, `package.json`, and test configuration before choosing commands.

Prefer Sail when the project is configured around it and its services are available. Use host tooling when the repository is intentionally non-Sail or the user has chosen the host workflow.

Do not silently mix runners within one verification sequence. Container and host PHP versions, extensions, environment variables, databases, and filesystem permissions may differ.

## Command Map

| Task | Sail | Host |
| --- | --- | --- |
| Artisan | `./vendor/bin/sail artisan ...` | `php artisan ...` |
| Composer | `./vendor/bin/sail composer ...` | `composer ...` |
| PHP tests | `./vendor/bin/sail artisan test ...` | `php artisan test ...` |
| Pint | `./vendor/bin/sail pint ...` | `vendor/bin/pint ...` |
| Node script | `./vendor/bin/sail npm run ...` | `npm run ...` |

Use the package manager selected by the lock file. Do not replace npm, pnpm, Yarn, or Bun merely because another tool is installed globally.

## Bootstrap Checks

- Required PHP and Node versions match project constraints.
- Composer and frontend dependencies are installed.
- `.env` exists when runtime commands need it, without printing secrets.
- The application key and writable directories are ready when relevant.
- Database, cache, queue, mail, search, and browser-test services required by the task are reachable.
- Pending migrations are understood before applying them.
- Test environment configuration points to safe, non-production services.

Starting containers or applying migrations changes local state. Do it when the requested workflow requires it; otherwise report the exact readiness issue and the command that would resolve it.

## Output

State the selected runner once, then use it consistently. When handing off, report environment limitations that prevented a check from running.
