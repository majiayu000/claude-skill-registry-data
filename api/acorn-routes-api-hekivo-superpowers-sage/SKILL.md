---
name: acorn-routes-api
description: Use when adding or fixing an HTTP endpoint or virtual page in an Acorn project - Acorn routes (routes/web.php, routes/api.php, withRouting, Route::get, controllers, middleware, route:list) versus register_rest_route (permission_callback, /wp-json, X-WP-Nonce); webhooks, JSON APIs, CORS, throttle, API-key or JWT auth, "Target class [auth] does not exist", 404 on a defined route. For Livewire use acorn-livewire; for models use acorn-data; for nonces and capabilities in depth use wp-security-escaping.
---

# HTTP endpoints: Acorn routes or WordPress REST

Two native mechanisms serve HTTP in an Acorn project. Pick one per endpoint before writing code:

- **WordPress REST**: `register_rest_route()` on `rest_api_init`, served under `/wp-json/<namespace>/…`, with WordPress authentication (cookie plus `wp_rest` nonce, application passwords), argument schemas and `permission_callback`. Behaviour verified in `wp-includes/rest-api.php` and `wp-includes/rest-api/class-wp-rest-server.php`.
- **Acorn routes**: Laravel's router inside Acorn, enabled by `withRouting(...)` on `Application::configure()`. Laravel middleware, validation, controllers, container injection and Blade responses, at any path outside wp-admin, the login page and `/wp-json`.

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.test}}`, `{{runner.cache}}`) come from the session context; on Lando they default to `lando wp`, `lando wp acorn`, the project's test tooling and its cache-clear tooling.

## When to use

- A new JSON endpoint, webhook receiver, form POST target, virtual page or redirect route.
- Middleware, auth, CORS or rate limiting for an endpoint.
- A defined route returns 404, 405, 500 or the wrong middleware runs.

Not for: Livewire's own endpoints (`acorn-livewire`), WordPress admin screens (`add_menu_page`), content URLs that belong to the template hierarchy.

## Inputs required

1. Active profile, Acorn base path and namespace (session context).
2. The boot call's `withRouting(...)` arguments (`web`, `api`, `apiPrefix`, `wordpress`) and any `withMiddleware(...)` callback.
3. Who calls the endpoint: block editor or wp-admin JS, a logged-in visitor's browser, an anonymous browser, a server (webhook, integration).
4. Whether the project documents an API contract (OpenAPI file, endpoint inventory) and where; the project's `AGENTS.md` or guidelines say so.

### Decide the mechanism

| Need | Use |
|---|---|
| Called by the block editor, `apiFetch`, wp-admin JS, or must appear in `/wp-json` discovery | `register_rest_route` |
| Must authenticate with application passwords or the REST cookie + nonce flow | `register_rest_route` |
| Laravel validation, controllers with DI, middleware stacks, Blade or redirect responses | Acorn route |
| A virtual page with its own URL rendered by Blade | Acorn route (`Route::view` or a controller) |
| Same codebase already standardised on one style | follow the project |

### Profile differences

| Item | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Where routing is enabled | `withRouting(...)` in the theme's `functions.php` | `withRouting(...)` in the plugin's boot or configurator class | the tracked Acorn boot mu-plugin, `web:` route file only by default (write-guarded: show the diff) |
| Route files | `routes/web.php` in the theme (picked up automatically when it exists) | files passed to `web:` / `api:` (paths inside the plugin) | `routes/web.php` at the root |
| API style by default | none; add `api:` or REST | often an `api:` file with a custom `apiPrefix` | `register_rest_route()` from a service provider listed in `composer.json` `extra.acorn.providers` |
| Controllers and middleware | `app/Http/Controllers`, `app/Http/Middleware` under `App\` | same folders under the plugin namespace | same folders under `App\` |

## Procedure

1. **Read the wiring.** Open the boot call. `withRouting(web: …, api: …, apiPrefix: 'api', wordpress: …)`: `web` routes get the `web` middleware group; `api` routes get the `api` group and the `apiPrefix` (default `api`); `wordpress: true` also routes every unmatched front-end request through the kernel under the `wordpress` group. List what exists: `{{runner.acorn}} route:list`.
2. **Pick the mechanism** with the table above. Then follow the matching branch.
3. **Acorn route branch.**
   - Generate classes: `{{runner.acorn}} make:controller Api/LeadController --api`, `{{runner.acorn}} make:middleware EnsureApiKey`.
   - Add the route to the right file, under a prefix that cannot collide with WordPress content (an Acorn route that matches wins over a page with the same path and the request never reaches WordPress).
   - Validate input with `$request->validate([...])`; return `response()->json()` with explicit status codes.
   - Authorise explicitly. Acorn ships without Laravel's `auth`, `can`, `guest` and `verified` aliases, and its `web` group has no CSRF middleware. For logged-in browser calls, `current_user_can()` works (the user resolves from the auth cookie) but nothing stops cross-site requests: verify a WordPress nonce (`wp_verify_nonce`) or enable `ValidateCsrfToken` through `withMiddleware()`. Patterns: [references/middleware-auth.md](references/middleware-auth.md).
   - Know the request lifecycle: Acorn answers matched routes on `parse_request` and exits, so `init` has run but `template_redirect`, `wp_head` and SEO plugin output do not run. Set title, canonical and sitemap entries yourself for virtual pages.
   - Details for routes, controllers, binding and caching: [references/acorn-routes.md](references/acorn-routes.md).
4. **WordPress REST branch.**
   - Register on `rest_api_init` from a service provider's `boot()` (never at file load), with a namespace and version (`vendor/v1`).
   - Always pass `permission_callback`; use `__return_true` only for truly public reads, and say so in a comment.
   - Declare `args` with `type`, `required`, `sanitize_callback` and `validate_callback`; return `WP_REST_Response` or `WP_Error` with a status.
   - Browser calls from logged-in users must send `X-WP-Nonce` (`wp_create_nonce('wp_rest')`); without it WordPress treats the request as anonymous.
   - Pattern and pitfalls: [references/rest-routes.md](references/rest-routes.md). For the full REST API reference (schema, controllers, discovery) see the `wp-rest-api` skill.
5. **Cross-cutting.** CORS: Acorn's global middleware includes `HandleCors`; configure `config/cors.php` (publish with `{{runner.acorn}} vendor:publish --tag=acorn-configs` if missing). Rate limiting: the `throttle` alias exists and needs a working cache store.
6. **Keep the contract in sync.** If the project documents its API (an OpenAPI file, an endpoint inventory, a changelog), update it in the same change as the route. The project layer says where; do not invent a location.
7. **Clear caches**: `{{runner.cache}}` (or `{{runner.acorn}} route:clear` and `optimize:clear`). If the deploy runs `route:cache`, every route file must be loadable at cache time.

## Verification

- `{{runner.acorn}} route:list --path=<prefix>` shows method, URI, name and middleware as intended. For REST, request `/wp-json/<namespace>` and read its `routes` index.
- `curl -si` the endpoint: unauthenticated, authenticated, invalid input. Expect 401/403, 200/201, and for bad input 422 (Acorn validation, when the request sends `Accept: application/json`; otherwise Laravel redirects back) or 400 (`rest_invalid_param`).
- Tests through `{{runner.test}}`: controller or middleware unit tests, plus HTTP-level tests if the project has them.
- The API contract file (when the project keeps one) changed in the same diff.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `Target class [auth] does not exist` | Acorn's default aliases omit `auth`, `can`, `guest`, `verified` | Use your own middleware class (capability check), or define the alias in `withMiddleware()` |
| Route listed but the URL serves WordPress (or 404) | Path under wp-admin, the login page, `/wp-json`, or ending in `.php`; Acorn skips those | Move the route; for `/wp-json` use `register_rest_route` |
| A WordPress page vanished | An Acorn route matches the same path and wins | Prefix Acorn routes; check `route:list` against the page tree |
| `/api/...` returns 404 | `api:` file not passed to `withRouting`, or a custom `apiPrefix` | Read the boot call; call the prefixed URL |
| Route missing after editing a route file | Route cache from a deploy or an earlier `optimize` | `{{runner.acorn}} route:clear` |
| POST from a logged-in browser works from any site | No CSRF check on Acorn's `web` group | Verify a WordPress nonce or enable `ValidateCsrfToken` |
| REST call from the front end acts as logged out | Missing `X-WP-Nonce` header; `rest_cookie_check_errors` resets the user to 0 | Send `wp_create_nonce('wp_rest')` as `X-WP-Nonce` |
| `_doing_it_wrong` notice for `register_rest_route` | No `permission_callback`, or called before `rest_api_init` | Add the callback; register inside `rest_api_init` |
| `Rate limiter [api] is not defined` | `throttleApi()` or `throttle:api` without `RateLimiter::for('api', …)` | Define the limiter in a provider, or use `throttle:60,1` |
| Session-dependent code fails on `api` routes | The `api` group has no session middleware | Use `web` routes for session needs, or token auth |

## Escalation

- Changing an existing public endpoint's path, method or response shape, or adding a new API version: stop and ask; consumers outside the repo may break.
- Auth design (JWT issuer, key rotation, application passwords for integrations): ask before choosing; record it where the project keeps decisions.
- The endpoint needs a custom table or model: `acorn-data`. Long work behind the endpoint: `acorn-background` (queue it).

<!-- verified:
vendor/roots/acorn/src/Roots/Acorn/Configuration/ApplicationBuilder.php:59-90 — withRouting(web, api, apiPrefix='api', wordpress=false); routes/web.php auto-detected
vendor/roots/acorn/src/Illuminate/Foundation/Configuration/ApplicationBuilder.php:211-219 — api routes get middleware('api')->prefix($apiPrefix)
vendor/roots/acorn/src/Roots/Acorn/Configuration/Middleware.php:43-49 global (TrustProxies, HandleCors, ValidatePostSize, ConvertEmptyStringsToNull); :83-97 web/api groups, PreventRequestForgery commented; :143-153 auth/can/guest/verified aliases commented, throttle present
vendor/roots/acorn/src/Roots/Acorn/Application/Concerns/Bootable.php:216-228 — admin, login, registration, rest_url paths and *.php skipped; :243-244 matched route handled on parse_request; Bootable.php:290-300 handleRequest sends and exits
vendor/roots/acorn/src/Illuminate/Foundation/Configuration/Middleware.php:605,625,743 — preventRequestForgery(), validateCsrfTokens(), throttleApi()
wp/wp-includes/rest-api.php:34 register_rest_route; :81 notice before rest_api_init; :122-129 permission_callback notice; :1130-1162 nonce missing -> wp_set_current_user(0), checks 'wp_rest'
wp/wp-includes/default-filters.php:520-522 determine_current_user from auth cookie; :545 rest_api_init on init
roots-docs acorn/routing.md, controllers-middleware-kernel.md — withRouting(web:), make:controller --api/--resource, make:middleware, custom kernel; routing.md's Route::middleware('auth') example needs an alias Acorn does not define
radicle-app facts checked against a licensed local Radicle project; not reproduced here
-->
