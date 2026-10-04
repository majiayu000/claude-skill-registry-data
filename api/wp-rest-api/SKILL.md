---
name: superpowers-sage:wp-rest-api
description: >
  WordPress REST API — register_rest_route, WP_REST_Controller, WP_REST_Request,
  REST namespace, custom endpoints, Application Passwords, JWT REST authentication,
  permission_callback, schema validation, WP_REST_Response, REST API versioning,
  rest_ensure_response, coexistence with Acorn Routes, register_rest_route vs
  routes/web.php decision, REST API debugging, wp rest-api namespace list,
  wp json discovery, CORS, REST nonce, cookie auth, REST API disable, JSON schema validation
user-invocable: false
---

# WordPress REST API Patterns

## When to use

Use this skill when the task involves creating, modifying, or debugging WordPress REST API endpoints, or when deciding between native REST and Acorn Routes for an API surface.

## Inputs required

- The API requirements: what data to expose, who consumes it, and authentication needs
- Whether the project already uses Acorn Routes (check `routes/web.php` or `routes/api.php`)
- The target consumers: Gutenberg editor, mobile apps, third-party integrations, or internal front-end

## Procedure

### Step 1 — Choose between Native REST and Acorn Routes

See [`references/acorn-coexistence.md`](references/acorn-coexistence.md) for the full decision matrix.

**Quick rule:** use native REST for WordPress-ecosystem integration and Acorn Routes for application logic. Both can coexist in the same project.

### Step 2 — Register native REST endpoints

Always use `register_rest_route()` inside a `rest_api_init` action. Never omit `permission_callback`.

See [`references/custom-endpoints.md`](references/custom-endpoints.md) for full examples including `WP_REST_Controller` pattern and JSON schema validation.

```php
public function boot(): void
{
    add_action('rest_api_init', [$this, 'registerRoutes']);
}

public function registerRoutes(): void
{
    register_rest_route('myapp/v1', '/posts', [
        'methods'             => 'GET',
        'callback'            => [$this, 'getPosts'],
        'permission_callback' => '__return_true',
    ]);

    register_rest_route('myapp/v1', '/posts', [
        'methods'             => 'POST',
        'callback'            => [$this, 'createPost'],
        'permission_callback' => fn() => current_user_can('edit_posts'),
        'args'                => $this->getCreatePostArgs(),
    ]);
}
```

### Step 3 — Authentication

See [`references/authentication.md`](references/authentication.md) for Application Passwords, cookie/nonce auth, and JWT patterns.

Quick reference:
- **Same-origin JS:** Cookie + `X-WP-Nonce` header
- **External app / mobile:** Application Passwords (Basic Auth)
- **Internal Acorn routes:** JWT middleware with `wp_set_current_user()`

### Step 4 — Expose custom fields and CPTs

```php
// Expose a CPT in the REST API
register_post_type('event', [
    'show_in_rest' => true,
    'rest_base'    => 'events',
]);

// Register a custom field on an existing endpoint
add_action('rest_api_init', function () {
    register_rest_field('post', 'reading_time', [
        'get_callback' => fn($post) => (int) get_post_meta($post['id'], '_reading_time', true),
        'schema'       => ['type' => 'integer', 'description' => 'Reading time in minutes'],
    ]);
});
```

### Step 5 — Avoid anti-patterns

| Anti-pattern | Problem | Correct approach |
|---|---|---|
| Closure in route callback | Cannot be cached; breaks serialization | Use class method reference `[$this, 'method']` |
| Missing `permission_callback` | Emits `_doing_it_wrong`; endpoint unprotected | Always include `permission_callback` |
| Returning raw arrays | Missing REST response headers | Use `rest_ensure_response()` |
| Hardcoded namespace version | Version changes require find-and-replace | Define as class constants |
| No schema definition | Clients cannot discover endpoint shape | Define `get_item_schema()` on the controller |
| Duplicating endpoint in both systems | Confusing and harder to maintain | One canonical endpoint per resource |

## Verification

- [ ] Every `register_rest_route()` call includes a `permission_callback`
- [ ] Argument schemas define `type`, `required`, and `sanitize_callback` where applicable
- [ ] CPTs that need REST access have `show_in_rest => true`
- [ ] Authentication method matches the consumer
- [ ] Pagination headers (`X-WP-Total`, `X-WP-TotalPages`) are set on collection endpoints
- [ ] No closures used as route callbacks
- [ ] No direct database queries in callbacks — logic is in Service classes
- [ ] Native REST and Acorn Routes do not duplicate the same resource

## Failure modes

See [`references/troubleshooting.md`](references/troubleshooting.md) for detailed diagnosis of 401, CORS, `rest_no_route`, schema validation failures, and 404 on custom namespace.

Quick reference:

| Symptom | Cause | Fix |
|---|---|---|
| 404 on REST endpoint | Missing `rest_api_init` hook or permalink flush needed | Flush permalinks: `lando wp rewrite flush` |
| `rest_no_route` error | Typo in namespace or route path | Check namespace and path match |
| 401 on authenticated endpoint | Nonce not sent or expired | Send `X-WP-Nonce` header |
| CPT not in `/wp/v2/` | `show_in_rest` not set | Add `'show_in_rest' => true` |

## Escalation

- If the REST API is entirely disabled (by a security plugin or custom code), check for `rest_authentication_errors` filters or `rest_enabled` overrides.
- If performance is critical (hundreds of requests per second), recommend a dedicated caching layer (Varnish, Cloudflare) rather than transient-based caching.
- If the API must serve a mobile app with offline support, recommend evaluating a dedicated API framework or GraphQL layer beyond the scope of this skill.
