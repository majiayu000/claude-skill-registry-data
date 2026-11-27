---
name: "Pair Framework"
slug: "pair"
version: "4.1.0"
description: "Entry skill for assistants working on the Pair v4 framework repository."
tags:
  - php
  - pair
  - framework
  - review
language: "en"
---

# Pair Framework v4 — Quick start

Read [AGENTS.md](AGENTS.md) first. It owns version scope, workflow, conventions,
change hygiene, document ownership, conflict resolution, and completion format.
This file provides navigation and commands for framework development.

## Choose the next document

| Need | Read |
| --- | --- |
| Framework internals and request flow | [Architecture](PAIR_ARCHITECTURE.md) |
| Concrete implementation examples | [Patterns](PAIR_PATTERNS.md) |
| Avoiding assumptions from other frameworks | [Context](PAIR_CONTEXT.md) |
| Work crossing layers, migration, or performance risk | [Task guidance](PAIR_TASKS.md) |
| Migrating a consuming application to v4 | [Upgrade guide](UPGRADE_V4.md) |
| Application setup and public API reference | [Pair wiki](https://github.com/viames/pair/wiki) |
| Releases and package contents | [Release workflow](RELEASING.md), [Composer dist contents](docs/COMPOSER_DIST_CONTENTS.md) |

For a small local task, stop after this file unless a specific uncertainty
requires another document.

## Component map

Paths are relative to the framework repository, not a consuming application's
`vendor/viames/pair` directory.

| Area | Responsibility and starting points |
| --- | --- |
| `src/Core` | Bootstrap, routing, environment, logging, runtime adapters; `Application.php`, `Router.php`. Legacy `Controller.php`, `Model.php`, `View.php` support migration. |
| `src/Web` | Explicit web controllers, page and fragment responses; `Controller.php`, `PageResponse.php`, `FragmentResponse.php`. |
| `src/Http` | Immutable input, uploads, response contracts, JSON/text responses and HTTP caching; `Input.php`, `ResponseInterface.php`. |
| `src/Data` | Explicit read contracts and mapping; `ReadModel.php`, `RecordMapper.php`, `Payload.php`. |
| `src/Api` | API controllers, request validation, CRUD, middleware, throttling, OpenAPI; `ApiController.php`, `Request.php`, `RequestData.php`. |
| `src/Orm` | Persistence, queries, collections and database access; `ActiveRecord.php`, `Query.php`, `Collection.php`, `Database.php`. |
| `src/Models` | Built-in framework records, including users, sessions, ACL and API tokens. |
| `src/Html` | Forms, controls, menus, UI rendering and templates; `Form.php`, `FormControl.php`. |
| `src/Helpers`, `src/Traits` | Shared utilities and small reusable behaviors. |
| `src/Cache`, `src/Search` | Cache stores and search indexing contracts. |
| `src/Services`, `src/Push` | External integrations, notification delivery and subscriptions. |
| `src/Packages` | Installable ZIP/manifest packages, separate from runtime extensions. |
| `src/Console` | Module, API and CRUD generation; `MakeCommand.php`. |
| `src/Exceptions` | Framework exceptions and error codes. |
| `assets`, `translations`, `migrations` | Frontend helpers, localization and framework schema migrations. |
| `mobile` | Native iOS and Android client sources; excluded from Composer dist. |
| `tests/Unit`, `tests/Support`, `tests/Fixtures` | Behavioral tests, isolated doubles and fixture applications. |

## Targeted searches

Search by class or namespace, then by method within the owning component.
Read one complete nearby class and its tests before editing.

```sh
rg --files src/Web src/Http tests/Unit/Web tests/Unit/Http
rg -n 'function page|function pageOrFragment' src/Web
rg -n 'checkToken|validateToken' src/Html tests/Unit/Html
rg -n 'data-text|data-show' assets/PairUI.js
```

For web requests, start in `src/Web` and `src/Http`; inspect `src/Core` for
application dispatch or legacy modules. For APIs, start in `src/Api`.
Search forms and frontend behavior in `src/Html` and `assets` together.

The wiki provides focused references for [controllers](https://github.com/viames/pair/wiki/Controller),
[ORM](https://github.com/viames/pair/wiki/ActiveRecord), [forms](https://github.com/viames/pair/wiki/Form),
[PairUI](https://github.com/viames/pair/wiki/PairUI.js), and
[environment configuration](https://github.com/viames/pair/wiki/Configuration-file).
Compare them with the checked-out source when behavior is uncertain.

## Local verification

From the framework root, after installing development dependencies:

```sh
composer install
composer test
vendor/bin/phpunit -c phpunit.xml.dist tests/Unit/Web/ControllerTest.php
```

For database compatibility, provision the disposable schema described in
[the MySQL integration guide](tests/Integration/MySql/README.md), then run
`composer test:mysql`. This separate suite targets real MySQL 8.0, 8.4 and 26.10
connections; never configure it with an application's database.

Run `composer test:install` to test the actual Composer dist and executable in
isolated consuming projects. Add `-- ../pair_boilerplate` for stable starter
creation, CLI, installer and baseline checks. See the
[installation test guide](tests/Integration/Composer/README.md) for optional
disposable MySQL credentials and local artifact fixtures.

Choose the relevant test path for a focused check. Use `composer run benchmark-v4`
when assessing v4 migration/performance behavior; it is not required for every edit.
For documentation-only work, check links, source references and example syntax.

Run generators from a consuming application with Pair installed:

```sh
vendor/bin/pair make:module orders
vendor/bin/pair make:api api
vendor/bin/pair make:crud order --table=orders --fields=id,customer_id,total_amount
```

Application upgrade commands and their dry-run/write behavior belong in the
[upgrade guide](UPGRADE_V4.md); do not infer migration safety from generator commands.
