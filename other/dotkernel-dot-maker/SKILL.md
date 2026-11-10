---
name: dotkernel-dot-maker
description: >
  Use before hand-writing any new scaffolding in a Dotkernel project — a module, entity,
  repository, service, service interface, handler, collection, form, input, input filter,
  middleware or CLI command. dot-maker (dotkernel/dot-maker, "composer make …") generates these
  to the Dotkernel file structure and naming pattern. Also use when asked how to create a new
  module, what "composer make" can do, or why generated boilerplate looks a certain way.
---

# dot-maker: generate, then customise

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
  Packages:  - none
```

`dotkernel/dot-maker` generates files matching the Dotkernel/Mezzio layout and the handler
naming pattern. It is comparable to the Symfony Maker Bundle, and more opinionated than Mezzio's
own CLI tooling because it targets Dotkernel conventions specifically.

**Always propose the `composer make …` command before hand-writing boilerplate.** Manual file
creation is where registrations get missed.

Availability varies: the stock API and Admin have it in `require-dev` with a `make` script alias;
the stock Frontend, Light and Queue do not. Check `composer.json`. If the project does not have
it, say so and fall back to copying the nearest existing module by hand.

## Running it

`composer make <thing>` or `./vendor/bin/dot-maker <thing>` — the `composer make` form needs the
script alias present in `composer.json`.

It is **interactive** and prompts through a series of choices. In an agent session, do not try to
pipe answers blindly: give the user the exact command and the answers to give, then continue from
the generated files. Treat generation like an install — the user's call.

## Commands

| Command | Generates |
| --- | --- |
| `module` | a full module: entity, repository, service, handler(s), ConfigProvider, RoutesDelegator, and documentation stub |
| `entity` | `Entity/X.php` + `Repository/XRepository.php` (skips whichever exists) |
| `repository` | the same pair, from the repository side |
| `service` | `Service/XService.php` + `Service/XServiceInterface.php` |
| `service-interface` | the same pair, from the interface side |
| `handler` | a handler in an existing module |
| `collection` | a `…Collection` (API-style projects) |
| `form` | a Form (Admin — not used in the API) |
| `input` | a single `Input/…Input.php` |
| `input-filter` | an InputFilter — prompts for `create` / `edit` / `replace` |
| `middleware` | a PSR-15 middleware |
| `command` | a CLI command |

**dot-maker detects which Dotkernel project it is running in** and generates accordingly —
collections in an API, forms and templates in Admin. That detection is also a useful
confirmation of the variant you think you are in.

## What it does *not* do — your job afterwards

1. **Register the module.** It creates the `ConfigProvider` and prints what to add, but you still
   add the entry to `config/config.php` and the PSR-4 entries to `composer.json` (which needs
   user approval).
2. **Configure authorization.** Add every new route name to this project's authorization
   config. API: `authorization.global.php`, where a missed entry denies the route. Admin:
   `authorization-guards.global.php`, where a missed entry leaves the route open to everyone.
3. **Migrations.** It tells you the command; you run
   `php ./vendor/bin/doctrine-migrations diff` (it prompts for approval), then give the user the
   `migrate` command to run — the `guard-bash.sh` hook refuses `migrate` for Claude, approval or
   not. Never hand-write a migration.
4. **Real logic.** Generated services and handlers are skeletons. Fill in validation, ownership
   checks, presentation metadata, documentation detail.
5. **Tests.** Nothing is generated under `test/`.
6. **QA.** Run the repo's `cs-fix` then `check` — generated code still has to pass phpcs and
   phpstan.

## Post-generation checklist

- [ ] `composer dump-autoload` after any new PSR-4 namespace.
- [ ] Both `ConfigProvider`s (application module and `Core`) registered in `config/config.php`.
- [ ] Handlers present under `factories` — and under `delegators` too in the API.
- [ ] Service interface aliased to the concrete service.
- [ ] Routes named per this project's dialect (`dotkernel-handler-naming`); authorization entries
      added.
- [ ] Presentation registered — HAL metadata or template path.
- [ ] Documentation completed with real request/response detail, where the project publishes it.
- [ ] Migration generated, reviewed, applied.
- [ ] QA suite green.
- [ ] Generated files are UTF-8 without BOM and LF.

## When not to use it

Editing an existing class, adding a method, or any single-file change. dot-maker creates; it does
not refactor.
