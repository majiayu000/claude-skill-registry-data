---
name: dotkernel-project-variants
description: >
  Use at the start of any non-trivial task in a Dotkernel repository, and whenever a convention
  might differ between projects — to work out whether this is Dotkernel API, Admin,
  Frontend, Light, Queue or a derived project, and what that implies for handler naming,
  authorization config, responses, forms, templates, documentation and tests. Also use when a
  skill's guidance does not match what the repo actually contains, or when the same feature has
  to be built in more than one Dotkernel project.
---

# Which project am I in, and what changes?

```text
Applies to
  Projects:  - all
  Packages:  - none
```

Detect first, then apply. Guessing produces confidently wrong code that looks plausible.

The tables below describe the stock repositories' default branches as of 2026-10-30: API `7.0`,
Admin `7.0`, Frontend `5.0`, Light `1.0`, Queue `2.0`. Other branches and derived projects can
differ — the repo in front of you wins.

## Detection

Read `composer.json`:

```bash
grep -m1 '"name"' composer.json
grep -A 12 '"psr-4"' composer.json
grep -E 'mezzio-hal|laminas-form|dot-controller|dot-session|dot-rbac-guard|oauth2|swagger-php|dot-cli|messenger' composer.json
```

Then confirm with the filesystem:

```bash
ls src                                   # module names, and whether a Core layer exists
ls src/*/templates 2>/dev/null           # templates present → templated project
ls src/*/src/Controller 2>/dev/null      # controllers present → Frontend-style
ls config/autoload | grep -i authorization
ls src/*/src/OpenAPI.php 2>/dev/null     # documented API
```

| Variant | Root namespace | Distinctive packages | Distinctive files |
| --- | --- | --- | --- |
| **API** | `Api\` + `Core\` | `mezzio/mezzio-hal`, `mezzio-authentication-oauth2`, `zircote/swagger-php`, `mezzio/mezzio-cors` | `src/Core/`, `Collection/`, `OpenAPI.php`, `authorization.global.php`, `documentation/command/` |
| **Admin** | `Admin\` + `Core\` | `dot-session`, `dot-rbac-guard`, `dot-twigrenderer`, `dot-flashmessenger` | `src/Core/`, `templates/`, `Form/`, `authorization.global.php` + `authorization-guards.global.php` |
| **Frontend** | `Frontend\` | `dot-controller`, `laminas/laminas-form`, `dot-session`, `dot-rbac-guard` | `Controller/`, `templates/`, `Form/`, `Entity/` inside modules, `data/doctrine/migrations/` |
| **Light** | `Light\` | `mezzio-twigrenderer` and little else — no Doctrine, no session, no forms | `Handler/`, `templates/`, hand-written `Factory/` classes |
| **Queue** | `Queue\` (flat, `src/`) | `dot-cli`, `netglue/laminas-messenger`, `symfony/redis-messenger` | `src/Swoole/Command/`, `src/App/Message/`, no HTTP routes |

A project derived from one of these keeps its parent's conventions. Infer the parent from the
PSR-4 roots and installed packages.

## What actually differs

| Concern | API | Admin | Frontend | Light | Queue |
| --- | --- | --- | --- | --- | --- |
| Request entry point | handler, `{Verb}{Resource}[{Sub}][{Action}]{Resource\|Collection}Handler` | handler, `{Verb}{Action}{Resource}[Form]Handler` — `GetCreateAdminFormHandler`, `PostCreateAdminHandler` | controller with an `{action}` route segment — `UserController` | handler — `GetPageViewHandler` | console command |
| Update verb | `PATCH` | `POST` (form submit) | `POST` (form submit) | n/a | n/a |
| Authorization | RBAC roles → route-name permissions, `authorization.global.php` | roles → permissions in `authorization.global.php`; route name → permission in `authorization-guards.global.php` | same two files; guards keyed by route **and action** | none | none |
| Unlisted route | denied | **allowed** — guards use `POLICY_ALLOW` | **allowed** — guards use `POLICY_ALLOW` | n/a — every route is public | n/a |
| Input | `laminas-inputfilter` | `laminas-form` (wrapping an InputFilter) + CSRF | `laminas-form` + CSRF | none | message payloads |
| Response | HAL resource/collection, ProblemDetails errors | rendered template, redirect, flash message | rendered template, redirect, flash message | rendered template | exit codes, logs |
| Documentation | per-module `OpenAPI.php`, `documentation/command/*.md` | none | none | none | none |
| Sessions/CSRF | none — stateless tokens | required | required | none | n/a |
| Entities | `Core` layer | `Core` layer | inside each module | none | none |
| Migrations | `src/Core/src/App/src/Migration/` | `src/Core/src/App/src/Migration/` | `data/doctrine/migrations/` | none | none |
| DI | `#[Inject]` + `AttributedServiceFactory` | `#[Inject]` + `AttributedServiceFactory` | `#[Inject]` + `AttributedServiceFactory` | hand-written factories | `#[Inject]` + `AttributedServiceFactory` |
| Scaffolding | `dot-maker` | `dot-maker` | none | none | none |
| Tests | `test/Unit/`, `test/Functional/` | `test/Unit/`, `test/Functional/` | `test/Unit/` | `test/Unit/` | `test/App/`, `test/Swoole/` |

The `documentation/` directory is the least reliable row: derived projects add or drop it freely,
so check for it before writing docs there (`dotkernel-feature-docs`) rather than inferring it.

## What is the same everywhere

- Mezzio underneath, with per-module `ConfigProvider`s registered in `config/config.php`.
- Laminas Coding Standard, phpstan, phpunit; `composer check`. Twig-rendering projects add
  `composer twig-cs-check`.
- Evolution over versioning for anything clients depend on.
- Secrets only in `*.local.php`.
- UTF-8, LF, `declare(strict_types=1)`.

## Working across two projects at once

In the stock repositories only API and Admin share a `Core` layer — both carry the same `Core\`
modules over one database. A feature spanning those two means: the entity, repository and shared
service go in `Core` **once**; each project gets its own handlers, routes, authorization entries
and presentation. Change a `Core` signature and you have changed it for every project on that
database — check the others before you do, and mention it (see `dotkernel-core-submodule`).

Frontend keeps its own entities and migrations, so a feature spanning Frontend and API means two
models of the same data. Say so rather than assuming a shared `Core`.

## Rule of thumb

Before writing a file, open the two closest existing files of the same kind **in this repo** and
match them. That beats every table above, because it reflects the version you are actually on.
When the repo contradicts a skill, follow the repo and tell the user the skill needs updating.
