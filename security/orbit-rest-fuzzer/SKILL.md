---
name: orbit-rest-fuzzer
description: Discover every `register_rest_route()` call in a WordPress plugin and fuzz-test each endpoint with malformed payloads, missing auth, oversized requests, type-juggling attacks, and SQLi/XSS injection vectors. Catches REST endpoint vulns most plugins ship. Use when the user says "REST API fuzzer", "fuzz endpoints", "REST security", "test REST permissions", or after adding any new `register_rest_route` call.
---

# 🪐 orbit-rest-fuzzer — REST endpoint fuzzing

REST endpoints are the #1 attack vector for modern WP plugins. This skill auto-discovers every endpoint in your plugin and bombards it with attacks.

---

## Quick start

```bash
PLUGIN_SLUG=my-plugin \
WP_TEST_URL=http://localhost:8881 \
  bash ~/Claude/orbit/scripts/rest-fuzz.sh
```

Output: `reports/rest-fuzz-<timestamp>.md`.

---

## How it works

1. Scan plugin source for `register_rest_route()` calls
2. Parse each: namespace, route, methods, args schema, permission_callback
3. Generate a fuzz suite per endpoint:
   - Anonymous request (must respect `permission_callback`)
   - Missing nonce (if `permission_callback => '__return_true'` — flag immediately)
   - Type-juggle each param (string in int field, array in string, null, etc.)
   - Boundary values (max int, min int, very long strings)
   - Injection vectors: `'; DROP TABLE`, `<script>`, `../../etc/passwd`
   - Oversized JSON (10MB body)
   - Malformed JSON
   - Wrong Content-Type
4. Send each, record response
5. Flag deviations from expected behaviour

---

## What it catches

### Auth bypass
```php
// ❌ Anyone can call this — checked by code review AND fuzz response
register_rest_route( 'my-plugin/v1', '/save', [
  'callback' => 'save_data',
  'permission_callback' => '__return_true',  // ← red flag
] );

// ✅
register_rest_route( 'my-plugin/v1', '/save', [
  'callback' => 'save_data',
  'permission_callback' => function( $req ) {
    return current_user_can( 'manage_options' );
  },
] );
```

### Missing input validation
```php
// ❌ No 'args' schema — accepts any input
register_rest_route( 'my-plugin/v1', '/save', [
  'callback' => function( $req ) {
    update_option( 'my_setting', $req['value'] );
  },
  'permission_callback' => '__return_true',
] );

// ✅ args schema validates types
register_rest_route( 'my-plugin/v1', '/save', [
  'callback' => 'save_data',
  'permission_callback' => 'check_perm',
  'args' => [
    'value' => [
      'type' => 'string',
      'required' => true,
      'sanitize_callback' => 'sanitize_text_field',
      'validate_callback' => fn( $v ) => strlen( $v ) <= 200,
    ],
  ],
] );
```

### SQL injection
The fuzzer sends `'; DROP TABLE wp_users--` to every parameter. If the response is anything other than 400 / properly-escaped, your handler isn't using `$wpdb->prepare()`.

### Type juggling
The fuzzer sends `0` for `id`, then a string `"abc"` to an int param, then `[1,2,3]` to a string param. Type-strict handlers reject these; loose ones may misinterpret.

### Oversized payloads
10MB JSON body to a string field — must return 413 (Payload Too Large) or 400, not 500.

### Path traversal
For any param accepting a filename: `../../wp-config.php`, `..\\..\\wp-config.php`, `%2e%2e%2f%2e%2e%2fwp-config.php`. Must reject.

### XSS in error messages
If your error message echoes user input back unescaped, `?id=<script>alert(1)</script>` results in stored XSS via the error UI.

---

## Permission callback patterns (code review)

| Pattern | Use when | Verdict |
|---|---|---|
| `'__return_true'` | Public, read-only, non-sensitive | ⚠ Always flag for review |
| `is_user_logged_in` | Logged-in only, but not role-gated | OK for read-only |
| `current_user_can('manage_options')` | Site admin only | Common |
| `current_user_can('edit_posts')` | Editors+ | OK for content endpoints |
| Custom callback inspecting nonce | Form-style POSTs | Best for state-changing |

---

## Example output

```markdown
# REST Fuzz — my-plugin

## Endpoints discovered: 8

### POST /my-plugin/v1/save
**permission_callback:** `__return_true`  ❌ Anonymous access allowed

#### Findings (7 — 2 critical, 3 high)
- ❌ **Critical**: SQL injection in `id` param — `'; DROP TABLE--` reflected in error
- ❌ **Critical**: No auth — anonymous POST succeeds with `value=hello`
- ❌ **High**: XSS — `<script>alert(1)</script>` in error response
- ❌ **High**: Type juggling — `id=0` returns first record (intended id=1)
- ⚠  **Medium**: 10MB body — returns 500 instead of 413
- ⚠  **Medium**: Missing CSRF nonce — relies only on permission_callback
- ℹ Info: No rate-limit headers in response

**Fix:**
1. Set `permission_callback` to require auth
2. Add `args` schema with type validation + sanitize_callback
3. Use `$wpdb->prepare()` everywhere
4. Escape all error message output with `esc_html()`
5. Add `Retry-After` and rate-limit headers via `nocache_headers()` / custom

---

### GET /my-plugin/v1/list
**permission_callback:** `current_user_can('edit_posts')`  ✓
**args schema:** `per_page` (int 1-100), `search` (string max 200)  ✓

#### Findings (1 — 1 low)
- ℹ Info: `search` param does LIKE query — could leak via timing if used with prepared but unindexed column. Add LIMIT enforcement.
```

---

## CI

```yaml
- run: PLUGIN_SLUG=my-plugin npx playwright test --project=rest-fuzz
- if: failure()
  uses: actions/upload-artifact@v4
  with: { name: rest-fuzz, path: reports/rest-fuzz/ }
```

---

## Pair with `/orbit-ajax-fuzzer` and `/orbit-wp-security`

- `/orbit-rest-fuzzer` — REST API endpoints
- `/orbit-ajax-fuzzer` — admin-ajax.php / `wp_ajax_*` handlers (legacy AJAX)
- `/orbit-wp-security` — full source code review

A plugin's attack surface is REST + AJAX + form handlers. All three skills together = full coverage.

---

## Hard rules

- ❌ Never run this against a live production site. Local wp-env only.
- ❌ Never run this against any URL you don't own.
- ✅ The fuzzer follows ethical-testing patterns — it doesn't chain exploits, it just probes.
- ✅ Findings are reported with severity + clear repro steps.
