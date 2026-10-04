---
name: orbit-ajax-fuzzer
description: Discover every `wp_ajax_*` and `wp_ajax_nopriv_*` action in a WordPress plugin and fuzz-test admin-ajax.php endpoints with malformed payloads, missing nonces, anonymous access attempts, and injection vectors. Use when the user says "AJAX fuzzer", "admin-ajax security", "test AJAX handlers", or after adding any new `add_action('wp_ajax_*', ...)`.
---

# 🪐 orbit-ajax-fuzzer — admin-ajax.php fuzzing

REST has a fuzzer. Legacy AJAX (`admin-ajax.php`) needs one too — it's a different attack surface, often less hardened.

---

## Quick start

```bash
PLUGIN_SLUG=my-plugin \
WP_TEST_URL=http://localhost:8881 \
  bash ~/Claude/orbit/scripts/ajax-fuzz.sh
```

Output: `reports/ajax-fuzz-<timestamp>.md`.

---

## How it works

1. Scan plugin source for `add_action('wp_ajax_*', ...)` and `add_action('wp_ajax_nopriv_*', ...)`
2. For each:
   - Detect the handler function
   - Check for nonce verification (`check_ajax_referer`, `wp_verify_nonce`)
   - Check for capability check (`current_user_can`)
   - Detect what params it accepts
3. Send fuzz requests to `/wp-admin/admin-ajax.php?action=<action>`:
   - **Logged out** (for `nopriv` actions only)
   - **Logged in but no nonce** — must reject if action has `check_ajax_referer`
   - **Logged in with wrong nonce** — must reject
   - **Logged in with correct nonce, no capability** — must reject if `current_user_can` is required
   - **Type juggling, injection, oversized body** — same suite as REST fuzzer
4. Record responses, flag misses

---

## What it catches

### Missing nonce check
```php
// ❌ Vulnerable — no nonce, accepts any logged-in user
add_action( 'wp_ajax_my_save', function() {
  update_option( 'my_setting', $_POST['value'] );
  wp_send_json_success();
} );

// ✅
add_action( 'wp_ajax_my_save', function() {
  check_ajax_referer( 'my_save_nonce', 'nonce' );
  if ( ! current_user_can( 'manage_options' ) ) wp_send_json_error( 'Forbidden', 403 );
  $value = sanitize_text_field( wp_unslash( $_POST['value'] ?? '' ) );
  update_option( 'my_setting', $value );
  wp_send_json_success();
} );
```

### Missing capability check
```php
// ❌ Any logged-in user (incl. subscribers) can hit this
add_action( 'wp_ajax_my_admin_action', function() {
  check_ajax_referer( 'my_nonce', 'nonce' );
  delete_post( $_POST['id'] );
} );

// ✅
add_action( 'wp_ajax_my_admin_action', function() {
  check_ajax_referer( 'my_nonce', 'nonce' );
  if ( ! current_user_can( 'delete_posts' ) ) wp_send_json_error( '', 403 );
  // ...
} );
```

### `wp_ajax_nopriv_*` handlers (the dangerous ones)
```php
// ❌ DANGEROUS — public AJAX endpoint with no validation
add_action( 'wp_ajax_nopriv_my_public', function() {
  $email = $_POST['email'];
  // do stuff with email — no nonce, no rate limit, no validation
} );

// ✅ When you must have public AJAX:
add_action( 'wp_ajax_nopriv_my_public', function() {
  // 1. Sanitize aggressively
  $email = sanitize_email( $_POST['email'] ?? '' );
  if ( ! is_email( $email ) ) wp_send_json_error( 'Invalid email' );

  // 2. Rate limit (e.g. 3 per IP per minute)
  $ip = $_SERVER['REMOTE_ADDR'];
  $key = 'my_plugin_rate_' . md5( $ip );
  if ( ( get_transient( $key ) ?: 0 ) > 3 ) wp_send_json_error( 'Rate limited', 429 );
  set_transient( $key, ( get_transient( $key ) ?: 0 ) + 1, MINUTE_IN_SECONDS );

  // 3. Optional: simple proof-of-work nonce (CSRF-style)
  if ( ! isset( $_POST['challenge'] ) || ! wp_verify_nonce( $_POST['challenge'], 'public_form' ) ) {
    wp_send_json_error( 'Invalid request' );
  }

  // ...
} );
```

### Direct PHP access bypass
admin-ajax.php loads WP. If the handler reads `$_POST` directly without sanitisation, an attacker can:
```bash
curl -X POST 'https://target.example.com/wp-admin/admin-ajax.php' \
  -d 'action=my_save' \
  -d "value=' OR 1=1--"
```

The fuzzer simulates this exact request.

---

## Example output

```markdown
# AJAX Fuzz — my-plugin

## Handlers discovered: 6

### wp_ajax_my_save (logged-in only)
**Code:** includes/class-admin.php:42

✓ Has check_ajax_referer
❌ MISSING capability check — any logged-in user (incl. subscribers) can save settings
❌ Param `value` not sanitized — direct DB write
❌ Param `value` not escaped in admin notice on response

#### Severity: Critical

#### Reproduce
```bash
# As subscriber-level user
curl -X POST 'http://localhost:8881/wp-admin/admin-ajax.php' \
  -H 'Cookie: ...subscriber session...' \
  -d 'action=my_save' \
  -d 'nonce=<valid_subscriber_nonce>' \
  -d "value='; DROP TABLE wp_options--"
```

Returns 200 + writes the malicious payload to wp_options.

#### Fix
Add: `if ( ! current_user_can( 'manage_options' ) ) wp_send_json_error( '', 403 );`
Add: `$value = sanitize_text_field( wp_unslash( $_POST['value'] ?? '' ) );`

---

### wp_ajax_nopriv_subscribe (anonymous endpoint)
✓ Sanitizes input
✓ Rate-limited via transient
❌ No CSRF token (any site can submit on behalf of a user)

#### Severity: High
**Fix:** Add a public-form nonce verified server-side.
```

---

## Coverage targets

| Pattern | Required for `wp_ajax_*` | Required for `wp_ajax_nopriv_*` |
|---|---|---|
| Nonce check | Yes | Yes (CSRF) |
| Capability check | Yes (sensitive) | N/A |
| Input sanitization | Yes | Yes (more aggressive) |
| Output escaping in response | Yes | Yes |
| Rate limiting | Optional | **Yes** |

---

## CI

```yaml
- run: PLUGIN_SLUG=my-plugin npx playwright test --project=ajax-fuzz
```

---

## Pair with `/orbit-rest-fuzzer` + `/orbit-wp-security`

Three layers of attack-surface:
- REST endpoints → `/orbit-rest-fuzzer`
- admin-ajax handlers → this skill
- Source code review → `/orbit-wp-security`

Run all three on every release. Together they cover the WP attack surface.

---

## Hard rules

- ❌ Never fuzz against a production site.
- ❌ Never fuzz any URL you don't own.
- ✅ Local wp-env only. Findings reported with full repro steps.
