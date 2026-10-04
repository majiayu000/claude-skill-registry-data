---
model_tier: medium
name: laravel
description: "Writes Laravel PHP — Eloquent, Artisan controllers, FormRequests, jobs, events, policies, providers. For Symfony / Doctrine use `symfony-workflow`. For framework-free PHP use `php-coder`."
domain: engineering
workspaces:
  - engineering
packs:
  - laravel
trust:
  level: professional
install:
  default: false
  removable: true
---

# laravel

## When to use

Use this skill for all Laravel-specific code generation and editing tasks, especially when working with:

- Controllers
- Form Requests
- Middleware
- Service Providers
- Jobs / Queued Jobs
- Events / Listeners
- Policies / Gates
- Notifications
- Console Commands
- Config, Routing, and Application Structure

This skill extends the base `php-coder` skill and applies Laravel conventions on top of the project's general PHP rules.

## When NOT to use — components without the framework

```
A DEPENDENCY PROVES A LIBRARY IS AVAILABLE. ONLY THE ENTRY POINT AND THE
ROUTER PROVE WHICH APPLICATION SHAPE IS RUNNING.
`illuminate/*` PACKAGES WITH NO SKELETON MARKER IS A THIRD STATE, AND THIS SKILL
DOES NOT APPLY TO IT.
```

Laravel ships its ORM, container, collections and HTTP layer as
independently installable packages, usable with no framework present — a
published distribution model, not one consumer's arrangement. An application
built that way has a **custom entry point and a custom router**. Routing it here
offers a CLI that does not exist, a request-validation primitive that is not
wired, and a routes file that was never there: every suggestion confidently
wrong, and the reason visible only from the entry point.

**The probe set, and its cost.** A fixed set of filesystem existence checks plus
one manifest read — no directory walk, no content scan, and never re-derived per
session. Any ONE marker present means the framework is real:

| Probe | Meaning |
|---|---|
| `artisan` | the console entry point the skeleton writes |
| `config/app.php` | the skeleton's bootstrap config |
| `bootstrap/app.php` | the application bootstrap |

`illuminate/*` in `composer.json` with **none** of those markers is
*components-without-the-framework*. Say so and route away from this skill rather
than answering as though the framework were there.

Implemented deterministically in `src/install/detect_php_shape.ts`
(`detectPhpShape`), whose `PROBE_PATHS` is this table and whose verdict names
what a wrong route would have offered.

## Procedure: Write Laravel code

→ **First apply the `php-coder` skill** — it handles project docs, module docs, patterns, and quality tools.

Then add these **Laravel-specific** checks:

1. **Confirm this is a Laravel app** — check whether `artisan` exists.
2. **Inspect app structure** — classic Laravel, modules (`app/Modules/`), or domain folders.
3. **Check routes and HTTP flow** — understand how requests enter the application and where logic belongs.
4. **Check test conventions** — inspect existing tests in the same domain before writing new code.

## Core Laravel principles

- Follow **Laravel conventions first** unless the project explicitly does otherwise.
- Keep **controllers thin** — delegate business logic to services/actions.
- Keep **Form Requests responsible for validation and authorization**.
- Use **dependency injection** through the container.
- Prefer **framework features** over custom infrastructure when the built-in solution is sufficient.
- Avoid hidden magic when explicit code is clearer for the project.
- Respect the existing architecture — do not force "pure Laravel" if the project uses modules or service layers.

## HTTP layer rules

- Controllers should:
    - accept the request
    - delegate business logic
    - return a response / resource / redirect
- Do not put business logic, calculations, or large data transformations in controllers.
- Use **Form Request** classes for validation instead of inline controller validation when the request is non-trivial.
- Use route model binding when it improves clarity and matches existing patterns.
- Keep controller actions focused and small.

## Validation rules

- Use **Form Requests** for reusable or non-trivial validation.
- Prefer explicit validation rules over implicit behavior.
- Reuse existing custom rules when available.
- Keep validation close to the HTTP boundary.
- Do not mix validation with persistence or business decisions.

## Service layer rules

- Put orchestration and business logic into dedicated services/actions.
- Services should be framework-light when possible.
- A service should have one clear responsibility.
- Prefer constructor injection for dependencies.
- Do not move trivial one-line controller behavior into a service unless the project consistently does that.

## Routing rules

- Follow the existing route organization:
    - `routes/web.php`
    - `routes/api.php`
    - module-specific route files
- Keep route definitions readable and grouped logically.
- Use route names consistently.
- Apply middleware explicitly and according to project conventions.
- Do not introduce route patterns that differ from the surrounding code without a good reason.

## Response rules

- Use the response style already established in the project:
    - Blade views
    - JSON responses
    - API Resources
    - Redirects with flash messages
- For APIs, prefer:
    - consistent status codes
    - structured JSON payloads
    - API Resources when the project uses them
- Do not return raw models directly unless that is already the established project pattern.

## Queues, jobs, and async work

- Use Jobs for clearly asynchronous or deferred work.
- Keep Jobs focused on a single responsibility.
- Pass only the data needed by the job.
- Avoid putting excessive domain logic directly into the Job class — delegate to services where appropriate.
- Be mindful of serialization when passing models or objects.

## Events and listeners

- Use events for meaningful domain or application events, not for every small action.
- Name events clearly in the past tense when something already happened.
- Keep listeners focused and side-effect oriented.
- Do not introduce event-driven complexity unless it is already part of the project architecture.

## Auth, policies, and authorization

- Use Laravel authorization features consistently:
    - policies
    - gates
    - request authorization
- Keep authorization logic out of controllers where possible.
- Reuse existing policies and permission patterns.
- Do not hardcode role checks in multiple places if a policy/gate already exists.

## Config and environment

- Read configuration from config files, not directly from `env()` outside config files.
- Do not introduce new environment variables unless necessary.
- Reuse existing config structure and naming patterns.

## Database interaction

- Prefer Eloquent for normal application data access unless the project uses repositories or query objects.
- Use transactions when multiple writes must succeed or fail together.
- Avoid N+1 problems — eager load when appropriate.
- For heavy data access logic, follow the dedicated `eloquent` skill.

## Migrations and schema changes

- Keep migrations focused and reversible.
- Follow existing naming conventions for columns, foreign keys, and indexes.
- Do not mix unrelated schema changes in a single migration.
- Be careful with destructive changes on existing production tables.

## Blade and view rules

- Keep views dumb — presentation only.
- Avoid embedding business logic in Blade templates.
- Extract reusable UI pieces into components/partials when it matches project patterns.
- Escape output by default and use raw output only when safe and intentional.

## Translations and language files

- **Flat dot-notation keys only** — `'type.daily_report' => 'Daily Report'`.
  Nested arrays (`'type' => ['daily_report' => …]`) are forbidden: they break
  key referencing and make a one-line addition a nested diff.
- Reference with the helper and the same flat key —
  `__('report.type.daily_report')`, `__('email.report.created.subject', ['number' => $number])`.
- Every key exists in **every** shipped locale. Adding to `lang/en/` without
  `lang/de/` is a bug, not a TODO — the app ships to both audiences.
- Never hardcode a user-visible string in PHP.

## What NOT to do

- Do not put business logic into controllers, models, or Blade templates.
- Do not validate large requests inline in controllers when Form Requests are more appropriate.
- Do not call `env()` outside config files.
- Do not introduce new architectural layers unless the project already uses them.
- Do not bypass Laravel features already used consistently in the project.
- Do not return inconsistent API response shapes in an established API.

## Output expectations

When generating Laravel code:

- follow Laravel naming conventions
- use dependency injection
- keep classes small and focused
- match the surrounding project structure
- prefer explicit, readable code over clever abstractions
- integrate with existing requests, resources, services, policies, and tests

## Output format

1. Laravel code following framework conventions and project architecture
2. All related files (controller, service, request, resource, test) as needed

## Do NOT

- Do NOT put business logic in controllers — delegate to services.
- Do NOT use facades in service classes — use dependency injection.
- Do NOT skip middleware for route groups that need authentication.

## Known pitfalls

| Symptom | Root cause | Fix |
|---|---|---|
| A list endpoint fires hundreds of queries / is slow under load | N+1: a relation is accessed inside a loop without eager loading | Eager-load with `with('relation')`; enable `Model::preventLazyLoading()` in non-prod to catch it early |
| Config changes / new env vars have no effect in production | `config:cache` cached the old config, and `env()` returns `null` once config is cached | Read env only in `config/*`, use `config()` elsewhere; re-run `config:cache` on deploy |
| A form field silently isn't saved | The attribute isn't in `$fillable` and mass-assignment drops it | Add it to `$fillable` (or set it explicitly); never blanket-`$guarded = []` on user input |
| Queued jobs never run / run with stale code | No worker is running, or workers weren't restarted after a deploy so they hold the old code in memory | Run/supervise `queue:work`; `queue:restart` on every deploy |
| Timestamps or times are off by hours | Comparing/formatting a Carbon instance without honoring `config('app.timezone')` vs the DB's UTC storage | Store UTC; convert for display; set the app timezone explicitly, don't assume server local time |

## Gotcha

- `env()` only works in config files — use `config()` everywhere else.
- Don't mix `Route::resource()` with single-action controllers — pick the project's convention.
- Don't return Eloquent models directly — always use API Resources.
- Don't bypass existing middleware stacks when adding new routes.

## Auto-trigger keywords

- Laravel
- controller
- service
- middleware
- route
- application structure

## Security audit checks (from security-audit)

Laravel-specific audit list (carved out of the generic `security-audit`
skill, 2026-07-12):

- `env()` in non-config files (leaks in debug mode)
- Debug mode (`APP_DEBUG=true`) in production
- Missing `$fillable` on models used with `request()->all()`
- `Route::any()` exposing unintended HTTP methods
- Missing rate limiting on login/register/password-reset
- Broadcast channels without proper authorization
- Missing encryption on sensitive cookie/session data
