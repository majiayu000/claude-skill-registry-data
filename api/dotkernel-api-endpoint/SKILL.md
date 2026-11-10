---
name: dotkernel-api-endpoint
description: >
  Use when adding or changing an endpoint in a Dotkernel API project (or a project derived
  from it) — a new route, handler, request or response contract, resource loading by id, a
  caller-scoped /account route, an action segment like /activate, an upload, a guest grant, or
  an operationId — and as the end-to-end checklist before calling an API endpoint done. Not for
  Admin, Frontend, Light or Queue projects.
---

# API endpoint conventions

```text
Applies to
  Projects:  - Dotkernel API
  Packages:  - none
```

**API only.** Confirm the variant with `dotkernel-project-variants` first. In a templated
project this skill does not apply — use `dotkernel-handler-naming` dialect B instead.

This skill is the checklist and the API-specific rules no other skill states. For everything
else it points to the skill that owns the topic. When the repo differs from the stock skeleton,
follow the repo and tell the user this skill needs updating.

## Where each topic lives

| Concern | Skill |
| --- | --- |
| Where files go, ConfigProvider wiring, new module registration | `dotkernel-module-structure` |
| Handler class name, URL shape, route name, RoutesDelegator style | `dotkernel-handler-naming` |
| InputFilters, Inputs, sort/filter whitelisting | `dotkernel-input-validation` |
| HAL resources and collections, pagination, errors | `dotkernel-responses` |
| Authorization config, ownership, guest access | `dotkernel-security` |
| `OpenAPI.php` operations | `dotkernel-openapi` |
| Coverage matrix and test helpers | `dotkernel-testing` |
| Changing a live contract, deprecation | `dotkernel-evolution-pattern` |
| Scaffolding before hand-writing | `dotkernel-dot-maker` |

## URLs and methods

- The caller's own resource lives under `account`, never under an id: `/user/account`,
  `/user/account/avatar`. Its handlers live in `Handler/Account/`.
- An action on an item is a trailing verb segment changed with `PATCH`:
  `PATCH /user/{id}/activate`.
- A process that creates no resource is a `POST`: `POST /user/account/recover` sends an e-mail.
- A one-time token from an e-mail link is a path placeholder:
  `/user/account/reset-password/{hash}`.
- A related list with no parent item is a fixed segment: `/user/role`.
- No `PUT`. No version prefix by default — the rare exceptions, and how to propose one, are in
  `dotkernel-evolution-pattern`.

## The caller and the item in the path

- The caller is `$request->getAttribute(IdentityInterface::class)`. Never take the caller's id
  from the path, the query or the body.
- Load the item in the path with `#[Resource(entity: X::class)]` on `handle()`. The resource
  provider middleware finds it by `{id}`, throws `NotFoundException` when it is missing or
  `isDeleted()`, and puts it on the request as `$request->getAttribute(X::class)`. The handler
  does not repeat that check.
- `identifier:` and `placeholder:` look an item up by another column. `guard:` takes an
  invokable `ResourceGuardInterface` class that refuses by throwing — one way to enforce
  ownership (see `dotkernel-security` for the alternatives).

## Request and response shape

- Request and response fields are `camelCase`: `passwordConfirm`, `firstName`.
- An upload is validated from `$request->getUploadedFiles()`, and its route gets its own
  `multipart/form-data` entry in `config/autoload/content-negotiation.global.php`, keyed by route
  name.
- Return through the `AbstractHandler` helpers only:

| Helper | Status | Use |
| --- | --- | --- |
| `createResponse($request, $entityOrCollection)` | 200 | read, update |
| `createdResponse($request, $entity)` | 201 | create |
| `noContentResponse()` | 204 | delete |
| `infoResponse($message)` | 200 | an action with no resource; body `{"info": {"messages": [...]}}` |

- `getArrayCopy()` never exposes a password hash, token, one-time hash or internal numeric id.
  The stock `User::getArrayCopy()` returns the activation `hash` — do not copy that into new
  entities.
- An action that is already done (activating an active account) is a `ConflictException`.

## Lists

`Paginator::getParams($params, '<default sort>')` defaults `limit` to 10 but accepts any positive
value, and `all` returns up to 1,000 rows. Clamp `limit` to a documented maximum in the service,
next to the `sort` whitelist.

## Authorization

- A request without a token runs as guest; a route not granted to guest answers 403, not 401.
- A new guest grant makes an endpoint public. State that decision explicitly in the merge
  request; never add it as a side effect.

## OpenAPI

- `operationId` is the handler class name without `Handler`, in lowerCamelCase:
  `getUserCollection`, `postUserResource`, `patchUserActivate`.
- Authenticated operations declare `security: [['AuthToken' => []]]`; public ones omit it.

## Tests beyond the standard matrix

On top of the coverage table in `dotkernel-testing`, cover:

- a caller without a token — 403 unless the route is granted to guest;
- another user's item, where a guard or ownership check applies;
- a conflict, where the endpoint can raise one.

## Checklist for a new endpoint

- [ ] Path, method, handler class, route name and `operationId` follow the naming rules.
- [ ] Handler extends `AbstractHandler`, takes dependencies through `#[Inject]`, holds no
      business logic.
- [ ] An item in the path is loaded with `#[Resource]`; ownership enforced if it belongs to a
      user.
- [ ] Input validated by an InputFilter of Input classes, catalogue messages, lengths matching
      the columns.
- [ ] `sort` whitelisted and `limit` clamped in the service.
- [ ] Response through a helper; entity or collection registered in the HAL `MetadataMap`.
- [ ] `getArrayCopy()` exposes only the intended fields.
- [ ] Errors thrown as typed exceptions with catalogue messages.
- [ ] Handler under `delegators` and `factories` in the module `ConfigProvider`.
- [ ] Route name granted in `authorization.global.php` to every role that needs it; to guest
      only by explicit decision.
- [ ] A non-JSON request body has its content-negotiation entry.
- [ ] Operation in the module's `OpenAPI.php`, with its failure responses.
- [ ] Tests cover the matrix plus the cases above; `composer check` passes.
