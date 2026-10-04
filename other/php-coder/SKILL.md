---
model_tier: medium
name: php-coder
description: "Writes or edits PHP code — controllers, classes, type hints, SOLID refactors, modern idioms — even without naming PHP. NOT for writing tests (use pest-testing) or explaining PHP concepts."
domain: engineering
workspaces:
  - engineering
packs:
  - php
trust:
  level: professional
install:
  default: false
  removable: true
---

# coder

## When to use

This skill applies to ALL code generation and editing tasks. Every other skill builds on top of this one.

Do NOT use when:
- Only reading/reviewing code (use `code-review` skill)
- Only running quality tools (use `quality-tools` skill)

## Procedure: Before writing code

### Step 0: Inspect project

1. Read `AGENTS.md` and `.github/copilot-instructions.md` for project-specific rules.
2. If working in a module (`app/Modules/*/`), check `app/Modules/{Module}/agents/` for module docs.
3. Look at neighboring files in the same directory — match the style.
4. Read `./agents/` for project-specific architecture.
5. Check `ecs.php` / `rector.php` (if they exist) — code accordingly.
6. Read `Makefile` or `Taskfile.yml` for available build/test/quality targets.

### Step 1: Detect project type

- `artisan` exists → Laravel project (Pest, Modules if present)
- No `artisan` + `composer.json` → Standalone PHP / Composer project
- Check `AGENTS.md` and `./agents/` for conventions

### Step 2: Apply conventions

→ See `php-coding` rule (always loaded) for PHP coding standards.
→ See guideline `php/general.md` for detailed PHP conventions.
→ See guideline `php/controllers.md`, `php/eloquent.md`, etc. for domain-specific conventions.

### Step 3: Stop-gate — branching on a discriminator?

Before writing **a second** `match`/`switch` arm, **a second** `if/elseif`
branch, or **a second** class hardcoded to one enum/string value (e.g.
`Provider::FOO->value`, `'stripe'`, a `case Type::CSV`), STOP and run the
Strategy sniff test.

Trigger keywords in the task or surrounding code:

- enum/string used as a type-tag: `Provider`, `Type`, `Channel`, `Format`,
  `Driver`, `Kind`
- repeated `match ($x)` / `switch ($x)` blocks on the same value
- class names that bake a single enum case in: `StripeImportService`,
  `CsvExporter`, `Ks21Job` next to `GeoCaptureJob` with the same shape
- allowlist constants: `private const SUPPORTED_FOO = [Type::A, Type::B]`

→ Run the sniff test in
[`docs/guidelines/php/patterns/strategy.md`](../../../docs/guidelines/php/patterns/strategy.md#sniff-test--when-an-enumstring-discriminator-wants-to-become-a-strategy).
Two "yes" answers → propose Strategy + Registry **before** adding the new
branch. Three "yes" → it is already overdue and the refactor is the change.

This gate fires **per task**, not per file — once you've passed the sniff
test for a given discriminator, do not re-ask on the next branch.

### Core principles

- **KISS** — simplest solution that works. No over-engineering.
- **YAGNI** — only build what's needed now.
- **DRY** — extract shared logic. Don't abstract prematurely.
- **SOLID** — single responsibility, depend on abstractions, small interfaces.

### Validate

- Run PHPStan on changed files — must pass at level 9.
- Run affected tests — must pass.
- Verify strict types, typed properties, return types on all new code.
- Check that no `dd()`, `var_dump()`, `print_r()` remain.

## Output format

1. Code following project guidelines and existing patterns
2. All downstream changes (callers, tests, imports) included

## Verification examples

- **Backend changes (service, controller, repository)**: probe the route with `curl` or an `actingAs()` HTTP test under `api/`; assert response shape and side effects.
- **Frontend-adjacent changes (Blade / Livewire component wiring)**: drive the component with a `livewire test`, a Playwright spec, or a browser `screenshot` snapshot.
- Always run the targeted test (`pest --filter=…`) and the relevant `phpstan` / `rector` checks before claiming done.

## Gotcha

- Don't introduce new patterns without being asked.
- Don't refactor code you're not working on.
- Use `Math` helper for ALL calculations — never raw PHP arithmetic.
- `MonitoringHelper::captureException()` for Sentry reporting.

## Do NOT

- Do NOT use native arithmetic (`+`, `-`, `*`, `/`) for business calculations — use `Math` helper.
- Do NOT refactor code you're not actively working on.
- Do NOT use `var_dump()`, `print_r()`, `dd()` — disallowed by PHPStan.

## Anti-bruteforce — diagnose before retry

When PHPStan, Rector, or a test goes red after a change, do not retry blindly by toggling type hints, adding `@phpstan-ignore`, or shuffling arguments until it passes. Diagnose the root cause first — read the error, trace the symbol, then apply a targeted fix. Trial-and-error type narrowing hides real type errors.

## Auto-trigger keywords

- PHP coding
- coding standards
- SOLID
- clean code
- best practices
