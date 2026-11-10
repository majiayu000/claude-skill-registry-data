---
name: dotkernel-handler-naming
description: >
  Use when naming or reviewing a PSR-15 request handler class, a route URL, a route name, or an
  authorization key in any Dotkernel project — creating a new endpoint or page, renaming
  one, adding a route to a RoutesDelegator, wiring a handler into a ConfigProvider, or checking
  that a handler follows the Dotkernel naming pattern. Also use when a route returns 403 or 404
  unexpectedly, when choosing between PATCH and POST, or when deciding whether a handler needs
  a Form suffix.
---

# Handler, route and authorization naming

```text
Applies to
  Projects:  - Dotkernel API
             - Dotkernel Admin
             - Dotkernel Light
  Packages:  - none
```

The naming pattern exists so that any developer can tell what a file does from its name alone.
It has **two dialects**, and the word order differs between them — pick by variant
(`dotkernel-project-variants`). Frontend has no handlers: it routes to controllers with an
`{action}` segment, so none of this applies there.

## Dialect A — API (REST, no forms)

```text
{HttpVerb}{Resource}[{SubResource}][{Action}]{Resource|Collection}Handler
```

Resource first, then the optional action. Suffix with `ResourceHandler` (a single entity) or
`CollectionHandler` (a paginated list). Non-CRUD actions that return a message rather than a
resource end in `…{Action}Handler`. No CRUD word in the class name — the HTTP verb says it.
**Updates use PATCH, never PUT.**

| Class | Route |
| --- | --- |
| `GetUserCollectionHandler` | `GET /user` |
| `PostUserResourceHandler` | `POST /user` |
| `GetUserResourceHandler` | `GET /user/{id}` |
| `PatchUserResourceHandler` | `PATCH /user/{id}` |
| `DeleteUserResourceHandler` | `DELETE /user/{id}` |
| `PatchUserActivateHandler` | `PATCH /user/{id}/activate` |
| `PostUserAvatarResourceHandler` | `POST /user/{id}/avatar` |
| `GetUserRoleCollectionHandler` | `GET /user/role` |

## Dialect B — Admin (templated, form-driven)

```text
{HttpVerb}{Action}{Resource}[{SubResource}][Form]Handler
```

Action first, then the resource — the reverse of the API. A `Form` suffix means the handler
**renders a form** that submits to another handler. The pair is always a `Get…FormHandler` that
renders and a `Post…Handler` that acts — deletes included, which get a confirmation form.

| Class | Route | Route name |
| --- | --- | --- |
| `GetCreateAdminFormHandler` | `GET /admin/create-admin` | `admin::create-admin-form` |
| `PostCreateAdminHandler` | `POST /admin/create-admin` | `admin::create-admin` |
| `GetEditAdminFormHandler` | `GET /admin/edit-admin/{id}` | `admin::edit-admin-form` |
| `PostEditAdminHandler` | `POST /admin/edit-admin/{id}` | `admin::edit-admin` |
| `GetDeleteAdminFormHandler` | `GET /admin/delete-admin/{id}` | `admin::delete-admin-form` |
| `PostDeleteAdminHandler` | `POST /admin/delete-admin/{id}` | `admin::delete-admin` |
| `GetListAdminHandler` | `GET /admin/list-admin` | `admin::list-admin` |
| `PostEditUserAvatarHandler` | `POST /user/edit-user-avatar/{id}` | `user::edit-user-avatar` |
| `GetListUserHandler` | `GET /user/list-user` | `user::list-user` |

Action words are `Create`, `Edit`, `Delete`, `List` and `View`, plus explicit verbs
(`ChangeAccountPassword`, `Logout`, `Store`). Admin uses **POST for updates** (browser form
submit), never PATCH, and puts the action in the URL.

Light is a starter with two handlers, `GetIndexViewHandler` and `GetPageViewHandler`; the second
registers one `GET` route per template listed in config, named `<prefix>::<template>`. Its names
put the resource first. When you add to Light, match those two files rather than either dialect.

## Naming a new one — the one-minute method

1. Which HTTP verb? → prefix.
2. API: resource, then sub-resource, then a non-CRUD action. Admin: action, then resource.
3. Admin only: does it render a form to be submitted later? → append `Form`.
4. API only: one thing or a list? → `Resource` / `Collection`.
5. Append `Handler`.

## URL conventions

API:

- Lowercase, `kebab-case` for multi-word segments: `/user/account/reset-password`.
- Singular resource segments: `/user`, not `/users` — collection-ness comes from verb and path.
- Item identifiers are UUIDs, matched by the `REGEXP_UUID` constant in Core's `App`
  `ConfigProvider`, whose placeholder is `{id}`. Never declare an unconstrained placeholder —
  the UUID pattern is what keeps fixed segments like `/user/role` from colliding with
  `/user/{id}`.
- Sub-resources nest: `/user/{id}/avatar`.

Admin: `/<module>/<action>-<resource>[/{id}]`, grouped by module prefix — `/admin/edit-admin/{id}`.

## Route names

```text
<module>::<action>-<resource>
```

| | API | Admin |
| --- | --- | --- |
| Actions | `list`, `view`, `create`, `update`, `delete`, plus `activate`, `recover`… | `list`, `view`, `create`, `edit`, `delete`, plus `store`, `change`… |
| Form-rendering route | n/a | add `-form`: `admin::edit-admin-form` |
| Example | `PatchUserResourceHandler` → `user::update-user` | `PostEditUserHandler` → `user::edit-user` |

## Route name = authorization key — but the default differs

- **API** — RBAC permissions in `authorization.global.php`. **A route name absent there is
  denied for every role**, the usual cause of "my new route returns Forbidden".
- **Admin** — roles map to permissions (`authenticated`, `unauthenticated`, …) in
  `authorization.global.php`; route names map to those permissions in
  `authorization-guards.global.php`. The guards use `POLICY_ALLOW`, so **a route name absent from
  the guards is open to everyone, guests included**. Forgetting the entry never shows up as a
  403 — it shows up as an unprotected page.

## RoutesDelegator style

Group by path prefix; order routes alphabetically inside a group.

```php
$routeCollector->group('/book')
    ->get('', GetBookCollectionHandler::class, 'book::list-book')
    ->post('', PostBookResourceHandler::class, 'book::create-book');

$routeCollector->group('/book/' . $id)
    ->delete('', DeleteBookResourceHandler::class, 'book::delete-book')
    ->get('', GetBookResourceHandler::class, 'book::view-book')
    ->patch('', PatchBookResourceHandler::class, 'book::update-book');

return $callback();
```

## Handler body conventions (all variants)

Handlers hold **no business logic**: validate → call service → shape response. Extend the
project's abstract handler if it has one, take dependencies through `#[Inject]` where the project
uses `dot-dependency-injection`, throw the project's typed exceptions for errors, and never
`echo` or hand-build a response object.

## Checklist for a new route

- [ ] Class name follows the dialect for **this** project.
- [ ] File under `src/<Module>/src/Handler/<Resource>[/<Sub>]/`.
- [ ] Extends the repo's abstract handler; deps via `#[Inject]`.
- [ ] Registered in `ConfigProvider` under `factories` (and `delegators` in the API).
- [ ] Route in `RoutesDelegator` named for this dialect.
- [ ] Authorization entry added — API: every role that should reach it; Admin: a guard rule,
      without which the route is public.
- [ ] Presentation registered — HAL metadata (API) or template (templated project).
- [ ] Documented, if this project publishes OpenAPI.
- [ ] Test covering success and the denied path.
- [ ] The repo's route-listing command shows it as expected.
