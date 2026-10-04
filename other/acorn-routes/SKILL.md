---
name: superpowers-sage:acorn-routes
description: >
  Routes, controller, Acorn routes, web.php, route:list, Route::get, Route::post,
  Route::resource, Route::apiResource, middleware, route model binding, API endpoint,
  RouteServiceProvider, named routes, resource controller, single-action controller,
  invokable controller, route group, route prefix, JSON response, rate limiting,
  token auth, Accept application/json, route cache, WP rewrite conflicts — using
  Acorn's Laravel routing inside WordPress/Sage/Bedrock
user-invocable: false
---

# Acorn Routes

## When to use

- Custom endpoints not mapped to WordPress content (forms, APIs, dashboards, webhooks)
- REST-style JSON endpoints with Laravel middleware, DI, and controller organization
- Frontend routes that render Blade views with Laravel Livewire
- Endpoints that need middleware chains (auth, rate-limit, CSRF)
- Route model binding with Eloquent models

## When NOT to use

- Permalink-based content routing (posts, pages, archives) — WordPress template hierarchy
- Gutenberg REST endpoints — must stay on `register_rest_route()` for block editor
- Admin menus and settings pages — use `add_menu_page()` / `add_submenu_page()`
- URLs expected to participate in canonical redirects and SEO plugin hooks

## Prerequisites

- Acorn installed in the theme
- `RouteServiceProvider` registered in `config/app.php`
- `routes/web.php` and/or `routes/api.php` present in the theme

## RouteServiceProvider Setup

```php
// app/Providers/RouteServiceProvider.php
namespace App\Providers;

use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Route;

class RouteServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        $this->routes(function () {
            Route::middleware('web')
                ->group($this->app->basePath('routes/web.php'));

            Route::middleware('api')
                ->prefix('api')
                ->group($this->app->basePath('routes/api.php'));
        });
    }
}
```

Register in `config/app.php`:

```php
'providers' => [
    // ...
    App\Providers\RouteServiceProvider::class,
],
```

## Quick Start — Scripts

```bash
# Create a standard controller (PascalCase name required)
bash skills/acorn-routes/scripts/create-controller.sh HomeController

# Create a full resource controller (index/create/store/show/edit/update/destroy)
bash skills/acorn-routes/scripts/create-controller.sh ProjectController --resource

# Create an API controller (no create/edit HTML methods)
bash skills/acorn-routes/scripts/create-controller.sh ProjectController --api

# Create a single-action invokable controller
bash skills/acorn-routes/scripts/create-controller.sh ExportReportController --invokable
```

Script: [`scripts/create-controller.sh`](scripts/create-controller.sh)

## Route Definitions

### Basic Routes

```php
// routes/web.php
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ContactController;

Route::get('/contact', [ContactController::class, 'show'])->name('contact.show');
Route::post('/contact', [ContactController::class, 'submit'])->name('contact.submit');
Route::put('/profile/{user}', [ProfileController::class, 'update'])->name('profile.update');
Route::delete('/account/{user}', [AccountController::class, 'destroy'])->name('account.destroy');
```

### Resource Routes

```php
// Full resource: index, create, store, show, edit, update, destroy
Route::resource('projects', ProjectController::class);

// Partial resource
Route::resource('events', EventController::class)->only(['index', 'show']);
Route::resource('comments', CommentController::class)->except(['destroy']);
```

### Route Groups

```php
Route::prefix('admin')->middleware('auth')->group(function () {
    Route::get('/reports', [ReportController::class, 'index'])->name('admin.reports');
    Route::post('/reports/export', [ReportController::class, 'export'])->name('admin.reports.export');
});
```

### Named Routes

Always name routes. Use `route()` helper in Blade and controllers — never hardcode URLs:

```php
Route::get('/projects/{project:slug}', [ProjectController::class, 'show'])->name('projects.show');

// In controllers
return redirect()->route('projects.show', ['project' => $project->id]);

// In Blade
<a href="{{ route('projects.show', $project) }}">View</a>
```

## Controllers

Controllers live in `app/Http/Controllers/`. See [`references/controllers.md`](references/controllers.md) for:
- Base controller setup
- Constructor injection patterns
- `wp_set_current_user` note (use in middleware, not constructors)
- Resource, API, and invokable controller full examples

### Quick Example

```php
class ProjectController extends Controller
{
    public function __construct(protected ProjectService $projects) {}

    public function index(): View
    {
        return view('projects.index', [
            'projects' => $this->projects->getPublished(),
        ]);
    }
}
```

## Assets

Boilerplate templates with `{{PLACEHOLDER}}` tokens:

- **[controller-resource.php.tpl](assets/controller-resource.php.tpl)** — All 7 REST methods. Replace `{{CLASS_NAME}}`, `{{VIEW_PREFIX}}`, `{{ROUTE_PREFIX}}`.
- **[controller-api.php.tpl](assets/controller-api.php.tpl)** — API controller (no create/edit). Replace `{{CLASS_NAME}}`.

## Route Model Binding

When the route parameter name matches the type-hinted variable, Laravel resolves the model automatically:

```php
Route::get('/projects/{project}', [ProjectController::class, 'show']);

// Controller
public function show(Project $project): View { /* $project auto-resolved */ }
```

Resolve by slug:

```php
Route::get('/projects/{project:slug}', [ProjectController::class, 'show']);
```

See [`references/route-model-binding.md`](references/route-model-binding.md) for:
- Scoped bindings for nested resources
- `resolveRouteBinding()` override
- WordPress post ID binding
- Missing model customization

## Middleware

```php
// Single route
Route::get('/dashboard', [DashboardController::class, 'index'])->middleware('auth');

// Group
Route::middleware(['auth', 'verified'])->group(function () {
    Route::resource('projects', ProjectController::class);
});

// With parameters
Route::post('/admin/users', [UserController::class, 'store'])->middleware('role:admin');
```

For creating custom middleware, see `superpowers-sage:acorn-middleware`.

See [`references/middleware-groups.md`](references/middleware-groups.md) for:
- Named middleware aliases (Kernel setup)
- `web` vs `api` groups
- Middleware ordering rules

## API Routes

```php
// routes/api.php — automatically prefixed /api, stateless
Route::apiResource('projects', \App\Http\Controllers\Api\ProjectController::class);

Route::post('/webhooks/stripe', [StripeWebhookController::class, 'handle'])
    ->middleware('verify.stripe.signature');
```

See [`references/api-endpoints.md`](references/api-endpoints.md) for:
- Full API controller structure with `JsonResource`
- `EnsureJsonResponse` middleware (`Accept: application/json`)
- Rate limiting with custom `RateLimiter`
- Token authentication middleware
- Versioned API setup

## WordPress Coexistence

- **Acorn routes take precedence** when they match a URL — they bypass WP rewrite rules entirely.
- **Prefix Acorn routes** with `/app/`, `/portal/`, or `/api/` to avoid colliding with WP content URLs.
- **WordPress admin** (`/wp-admin/`) and **WP REST API** (`/wp-json/`) are unaffected.
- **No permalink flush needed** — Acorn routes are not registered in WP's rewrite table.

## Lando Commands

```bash
# List all routes with methods, URIs, controllers, names, middleware
lando acorn route:list

# Filter by path segment
lando acorn route:list --path=api

# Filter by HTTP method
lando acorn route:list --method=POST

# Cache routes for production (no closure routes allowed)
lando acorn route:cache

# Clear route cache (always do this during development)
lando acorn route:clear
```

## Critical Rules

1. **Always use `routes/web.php` or `routes/api.php`** — never define Acorn routes in `functions.php`.
2. **Use `Route::middleware()` for auth/access control** — never `add_action('init')` or WP hooks on Acorn routes.
3. **Check for WP rewrite conflicts** with `lando acorn route:list` before deploying.
4. **Never use closures in route files** — they cannot be cached. Use controller classes.
5. **Always name routes** — `->name('resource.action')` — so `route()` helper and redirects work.
6. **Prefix Acorn routes** to avoid colliding with WordPress page slugs and content URLs.
7. **`wp_set_current_user()` belongs in auth middleware**, not in controller constructors.

## Verification

- Visit the route URL and confirm expected response (HTML or JSON) with correct status code.
- Run `lando acorn route:list` and verify the route has correct method, URI, controller, name, middleware.
- Test named routes: `lando acorn tinker` → `route('route.name')` returns the expected URL.

## Failure modes

See [`references/troubleshooting.md`](references/troubleshooting.md) for:
- 404 on a defined route
- Route conflicts with WP rewrite rules
- Middleware not firing
- Route model binding not resolving
- `current_user_can()` returning false in controllers
- CSRF token mismatches
- Route cache issues

## References

Deep content loaded on demand — zero tokens until needed.

- **[controllers.md](references/controllers.md)** — Controller class structure, constructor injection, resource/API/invokable controllers, `wp_set_current_user` note for constructors.
- **[route-model-binding.md](references/route-model-binding.md)** — Implicit and explicit binding, `resolveRouteBinding()`, WP post ID binding, scoped bindings.
- **[middleware-groups.md](references/middleware-groups.md)** — Middleware assignment in routes, named middleware aliases, group wrapping, `web`/`api` groups, ordering.
- **[api-endpoints.md](references/api-endpoints.md)** — JSON API responses, rate limiting, token auth, `Accept: application/json` detection, versioning.
- **[troubleshooting.md](references/troubleshooting.md)** — 404 on Acorn routes, WP rewrite conflicts, middleware not firing, route cache, CSRF issues.

## Escalation

- Route needs WordPress REST API (`/wp-json/`): use `register_rest_route()` — see `superpowers-sage:wp-rest-api`.
- Middleware not behaving: see `superpowers-sage:acorn-middleware` for Kernel setup and JWT.

## Query First — MCP Integration

Before adding routes that reference controllers or post types, query:

```
execute-ability routes/list
```

Use real route slugs and controller names from the query.
See [`sageing/references/mcp-query-patterns.md`](../sageing/references/mcp-query-patterns.md).
