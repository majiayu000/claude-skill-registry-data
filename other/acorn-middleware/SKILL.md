---
name: superpowers-sage:acorn-middleware
description: >
  HTTP middleware, JWT authentication, auth middleware, custom guards, JWT guard,
  route middleware, request filter, middleware group, Acorn middleware, guard,
  rate limiting, CORS, CheckRole, throttle, bearer token, request filtering,
  middleware registration, HTTP Kernel — using Acorn's Laravel middleware stack
  inside WordPress/Sage/Bedrock
user-invocable: false
---

# Middleware & Authentication

## When to use

- Protecting Acorn routes with authentication (JWT, API tokens, custom guards)
- Request preprocessing: rate limiting, CSRF validation, locale detection
- Response postprocessing: adding headers, logging, caching
- Role / capability checks before a controller runs
- Route-specific authorization groups

## When NOT to use

- Filtering native WordPress admin pages or `register_rest_route()` endpoints — middleware does NOT run there; use `add_action('admin_init')` / `rest_pre_dispatch` instead
- Template-hierarchy front-end pages (pages, archives, single posts) — use `template_redirect` action
- Business logic that should live in a service class
- Authentication for REST endpoints that bypass Acorn routes — extend `wp-rest-api` skill guidance instead

## Prerequisites

- Acorn installed with a working `routes/web.php` or `routes/api.php`
- `RouteServiceProvider` booted
- For JWT: `firebase/php-jwt` installed via `lando theme-composer require firebase/php-jwt`

## What Middleware Does in Acorn

Middleware filters HTTP requests before they reach route controllers — the same pipeline concept as Laravel. Each middleware inspects or transforms the request, then either passes it forward or returns a response early.

**Critical distinction:** Middleware only runs on Acorn-registered routes (defined in `routes/web.php` or `routes/api.php`). It does NOT intercept native WordPress requests (admin pages, REST API endpoints registered via `register_rest_route()`, or front-end page loads handled by the template hierarchy). Use `add_action`/`add_filter` hooks for WordPress-native requests.

## Quick Start

```bash
# 1. Generate a middleware class
lando acorn make:middleware EnsureJsonResponse

# Or use the helper script (see Scripts section)
bash skills/acorn-middleware/scripts/create-middleware.sh MyMiddleware --type=filter
```

```php
// app/Http/Middleware/EnsureJsonResponse.php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureJsonResponse
{
    public function handle(Request $request, Closure $next): Response
    {
        $request->headers->set('Accept', 'application/json');
        return $next($request);
    }
}
```

```php
// app/Http/Kernel.php — register middleware aliases
protected $middlewareAliases = [
    'auth.jwt' => \App\Http\Middleware\AuthenticateJwt::class,
    'role'     => \App\Http\Middleware\CheckRole::class,
    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
];

// routes/api.php — apply to routes
Route::middleware(['auth.jwt', 'throttle:60,1'])->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
    Route::post('/posts', [PostController::class, 'store'])->middleware('role:editor,administrator');
});
```

## Common Patterns (Summary)

| Pattern | Class | Registration |
|---|---|---|
| Force JSON responses | `EnsureJsonResponse` | `api` middleware group |
| JWT auth | `AuthenticateJwt` | `'auth.jwt'` alias |
| Role check | `CheckRole` | `'role:administrator'` |
| Rate limiting | built-in `ThrottleRequests` | `'throttle:60,1'` |
| CORS | built-in `HandleCors` | global middleware |
| Capability check | `CheckCapability` | `'capability:edit_posts'` |

## References

Deep content extracted from this skill. Read on demand — zero tokens until needed.

- **[jwt-auth.md](references/jwt-auth.md)** — Full JWT setup: `JwtService`, `AuthenticateJwt` middleware, `AuthController` (login/refresh/me), route registration, client-side token flow, and `.env` variables.
- **[custom-guards.md](references/custom-guards.md)** — Laravel `Guard` contract, `WordPressGuard` implementation, registering via `Auth::extend()`, configuring `config/auth.php`, using `auth()->user()` in controllers.
- **[request-filtering.md](references/request-filtering.md)** — Before/after middleware, HTTP Kernel setup, middleware groups (`web`, `api`, `api.auth`), middleware parameters, `CheckRole`, `ThrottleRequests`, CORS config, middleware ordering.
- **[troubleshooting.md](references/troubleshooting.md)** — Common failure modes (middleware not executing, JWT secret issues, `current_user_can()` returning false), best practices table, common mistakes table, escalation paths.

## Scripts

```bash
# Create a new middleware via Lando
bash skills/acorn-middleware/scripts/create-middleware.sh <Name> [--type=auth|filter]

# Examples
bash skills/acorn-middleware/scripts/create-middleware.sh CheckApiKey --type=filter
bash skills/acorn-middleware/scripts/create-middleware.sh AuthenticateJwt --type=auth
```

Script: [`scripts/create-middleware.sh`](scripts/create-middleware.sh) — runs `lando acorn make:middleware <Name>` with guard checks.

## Assets

Boilerplate templates with `{{PLACEHOLDER}}` tokens. Copy and replace placeholders.

- **[middleware-auth.php.tpl](assets/middleware-auth.php.tpl)** — Auth guard check middleware. Replace `{{CLASS_NAME}}` and `{{GUARD_NAME}}`.
- **[middleware-filter.php.tpl](assets/middleware-filter.php.tpl)** — General-purpose request filter with `passes()` hook. Replace `{{CLASS_NAME}}`, `{{REJECTION_MESSAGE}}`, `{{REJECTION_STATUS}}`.

## Verification

- Send a request without credentials — confirm middleware returns a 401/403 JSON response (not pass through).
- Send a request with a valid JWT Bearer token — confirm the controller responds with 200.
- Run `lando acorn route:list` and verify the middleware alias appears in the middleware column for protected routes.

For detailed debug tips and common mistake patterns, read [`references/troubleshooting.md`](references/troubleshooting.md).

## Failure modes

See [`references/troubleshooting.md`](references/troubleshooting.md) for the full failure modes list, common mistakes table, and escalation paths.

## Critical Rules

1. **Middleware only runs on Acorn routes.** Never expect it to intercept WordPress admin, REST API (`register_rest_route`), or template-hierarchy requests.
2. **Always call `wp_set_current_user($user->ID)`** in JWT/auth middleware, or `current_user_can()` will fail downstream.
3. **Never hardcode `JWT_SECRET`.** Use `env('JWT_SECRET')` and store a 32+ character random string in `.env`.
4. **Create `app/Http/Kernel.php`** before registering middleware aliases or groups — without it, aliases silently do nothing.
5. **Order middleware correctly:** auth before role/capability checks; `EnsureJsonResponse` before auth in API groups.
6. **Throttle auth endpoints strictly:** `throttle:5,1` for login, `throttle:10,1` for token refresh.
7. **Return JSON errors from API middleware**, not HTML. Always pair error returns with the correct HTTP status code (401 for unauthenticated, 403 for unauthorized).
8. **Use `$request->bearerToken()`**, not manual `Authorization` header parsing.
