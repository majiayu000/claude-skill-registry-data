---
name: dotkernel-module-structure
description: >
  Use when creating, moving, renaming or locating any file in a Dotkernel project —
  deciding whether code belongs in an application module or the shared Core layer, adding a
  Handler, Service, Collection, Form, InputFilter, Input, Entity, Repository, Enum, DBAL type,
  Command, Middleware, ConfigProvider or RoutesDelegator, registering a module in
  config/config.php and composer.json autoload, or answering "where does this go" and "why is
  this class not found".
---

# Module and file structure

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
  Packages:  - none
```

Identify the variant first (`dotkernel-project-variants`). The two-layer split below is how the
stock API and Admin are built; which artefacts a module contains differs between them. Frontend
keeps entities inside its own modules, Light has no persistence, and Queue is a single flat
`Queue\` namespace — none of them has a `Core` layer.

## The two layers

| Layer | Namespace | Path | Contains |
| --- | --- | --- | --- |
| Application module | `<App>\<Module>\` | `src/<Module>/src/` | HTTP / CLI facing code |
| Shared core module | `Core\<Module>\` | `src/Core/src/<Module>/src/` | persistence + shared domain |

`<App>` is the project's root namespace — `Api` or `Admin`.
`Core` is designed to be a git submodule shared between the projects on one database
(see `dotkernel-core-submodule`). **Nothing in `Core` may depend on a project namespace.**

**Golden rule: Core is the only place that manages database entities.**

### Which layer?

| Artefact | Layer |
| --- | --- |
| Handler, RoutesDelegator, Collection, Form, InputFilter, Input, Service, ServiceInterface, OpenAPI | application module |
| Entity, Repository, Enum, DBAL type, EventListener, Fixture, Migration, shared Message catalogue | `Core` |
| Middleware, Attribute, Exception, Guard, Template helper | the project's `App` module (cross-cutting) |
| CLI Command | application module if feature-specific, `Core\App\Command` if infrastructural |
| ConfigProvider | **both** — one per module, per layer |

A service imports `Core\<Module>\Entity\X`. Never the reverse.

## Canonical module layout

Shared skeleton:

```text
src/<Module>/src/
├── Handler/<Resource>/…            one folder per resource, nested for sub-resources
├── InputFilter/
│   ├── Input/…Input.php
│   └── {Create,Update}<X>InputFilter.php
├── Service/
│   ├── <X>Service.php
│   └── <X>ServiceInterface.php
├── ConfigProvider.php
└── RoutesDelegator.php

src/Core/src/<Module>/src/
├── Entity/<X>.php
├── Repository/<X>Repository.php
├── Enum/<X>StatusEnum.php
├── DBAL/Types/<X>StatusEnumType.php
└── ConfigProvider.php
```

Variant-specific additions to the application module:

- **API**: `Collection/<X>Collection.php`, `OpenAPI.php`
- **Admin**: `Form/<X>Form.php`, and templates under `src/<Module>/templates/<module>/`

Handler folders mirror the URL: a route at `/user/{id}/avatar` lives in
`Handler/User/Avatar/`.

## Wiring a new module — all four steps, or it silently does nothing

1. `composer.json` → `autoload.psr-4`: `"<App>\\Book\\": "src/Book/src/"` and
   `"Core\\Book\\": "src/Core/src/Book/src/"`.
   **This edits composer.json — ask the user first**, then they run `composer dump-autoload`.
2. `config/config.php` → add both `ConfigProvider::class` entries to the Dotkernel modules
   block, alphabetically.
3. The module `ConfigProvider` → `dependencies` (factories / delegators / aliases), plus
   whatever else the variant needs (HAL `MetadataMap` for API, `templates` for templated projects,
   `doctrine.types` for enum columns).
4. The authorization config → an entry for every new route name.
   API: `config/autoload/authorization.global.php` — a missing entry denies the route.
   Admin: `config/autoload/authorization-guards.global.php` — a missing entry leaves the route
   **open to everyone**, because the guards use `POLICY_ALLOW`.

Config is cached in production; run the repo's cache-clear script (commonly
`composer clear-config-cache`) after config changes.

## ConfigProvider contract

```php
public function __invoke(): array
{
    return [
        'dependencies' => $this->getDependencies(),
        // API:    MetadataMap::class => $this->getHalConfig(),
        // Admin:  'templates'        => $this->getTemplates(),
    ];
}
```

- `delegators` → API: each handler maps to the repo's handler delegator factory. Admin handlers
  have no delegator entry; there `delegators` holds only `Application::class => [RoutesDelegator::class]`
  and form delegators.
- `factories`  → each handler and concrete service maps to `AttributedServiceFactory::class`.
- `aliases`    → `BookServiceInterface::class => BookService::class`.

Keep these arrays alphabetically sorted with aligned `=>` — phpcs enforces the alignment.

## Other paths

| Path | Purpose |
| --- | --- |
| `config/autoload/*.global.php` | committed defaults |
| `config/autoload/*.local.php` | git-ignored secrets; only `.dist` templates are committed |
| `config/pipeline.php` | PSR-15 middleware order |
| `config/routes.php` | thin — real routes live in each module's `RoutesDelegator` |
| `bin/` | CLI entry points |
| `test/Unit/`, `test/Functional/` | namespaces per `autoload-dev` |
| `documentation/` | project docs (CLI command docs, a generated `openapi.json`, Postman collections) where present — the stock API ships one, derived projects vary, so check |
| any Doctrine migrations directory | **generated** — never hand-edit |

## Checklist for a new artefact

- [ ] Namespace matches the directory exactly (PSR-4, case-sensitive).
- [ ] Entity/Repository in `Core` (API and Admin; Frontend: inside the owning module), everything
      request-facing in the application module.
- [ ] Registered in the module `ConfigProvider` (API handlers: factory **and** delegator; Admin
      handlers: factory).
- [ ] Route declared in `RoutesDelegator`; authorization entry added.
- [ ] Presentation registered: HAL metadata (API) or template path (templated project).
- [ ] `OpenAPI.php` operation added, if this project publishes OpenAPI.
- [ ] Test added.
