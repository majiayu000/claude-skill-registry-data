---
name: wp-security-escaping
description: Use when writing or reviewing code that outputs data, handles input or checks permissions in a WordPress + Acorn project - Blade {{ }} vs {!! !!}, esc_html, esc_attr, esc_url, wp_kses_post, "&#038; in the URL", double escaping, sanitize_text_field, nonces, current_user_can, map_meta_cap, permission_callback, $wpdb->prepare, whereRaw, file uploads, escaping ACF values, secrets in .env. For route middleware use acorn-routes-api; for ACF validation use acf-native; for Livewire actions use acorn-livewire.
---

# Security: escape once, sanitise in, authorise always

Three rules cover most findings in Acorn projects: escape output **exactly once** (Blade or WordPress, never both), sanitise and validate input at the entry point, and pair every state change with a capability check (a nonce proves intent, a capability proves authority).

Runner placeholders come from the session context: `{{runner.wp}}` (Lando default `lando wp`), `{{runner.test}}` (the project's test command), `{{runner.cache}}`. Never run `wp`, `composer` or `php` on the host.

## When to use

- Any Blade view, component or block render template that prints dynamic data.
- Form handlers, AJAX handlers, REST callbacks, Acorn controllers, Livewire actions.
- Roles, custom capabilities, CPT capability mapping, REST `permission_callback`.
- Raw SQL through `$wpdb` or the query builder, file uploads, secrets.
- A final security pass over code another skill produced.

## Inputs required

- The file(s) and context: Blade view, component, block render, provider, controller, REST callback.
- Who can reach the code: anonymous visitor, logged-in user, editor, admin, CLI.
- The active profile and app path (session context) to know where views and routes live.

## Procedure

### 1. Escape output once

Blade `{{ $x }}` compiles to `e($x)`: `htmlspecialchars(…, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8', double_encode = true)`. WordPress escapers already return HTML-safe text. Wrapping one in the other escapes twice: `{{ esc_url($url) }}` turns `?a=1&b=2` into a visible `&#038;` and breaks the link.

| Value | Write | Never |
|---|---|---|
| Plain text from PHP | `{{ $title }}` | `{{ esc_html($title) }}` |
| Text that may already hold entities (`get_the_title()`, ACF formatted text) | `{!! esc_html($title) !!}` (WordPress does not double-encode) | `{{ get_the_title() }}` when you see `&amp;amp;` |
| URL in `href` / `src` | `{!! esc_url($url) !!}` | `{{ esc_url($url) }}` |
| Attribute from WordPress | `{!! esc_attr($label) !!}` or `{{ $label }}` | `{{ esc_attr($label) }}` |
| Trusted rich HTML (post content, WYSIWYG) | `{!! wp_kses_post($html) !!}` | `{!! $html !!}` unfiltered |
| Data for JavaScript | `@json($data)` (hex-escapes `<`, `>`, `'`, `"`, `&`), or `wp_add_inline_script()` with `wp_json_encode()` | string-built JS |
| Component attributes | `$attributes->merge(['href' => $url])` escapes the defaults with `e()`; pass `false` as the second argument when the value comes from `esc_url()` / `esc_attr()` | merging an `esc_url()` value with escaping on |

Bound attributes on a component tag (`<x-link :href="$url">`) that land in the attribute bag are already escaped with `e()` at compile time; do not pass `esc_url()` output there either. Details and a guard test: [references/blade-escaping.md](references/blade-escaping.md).

### 2. Sanitise and validate input

- Read explicit keys, never the whole `$_POST`; `wp_unslash()` before sanitising superglobals.
- Pick the sanitiser by type (`sanitize_text_field`, `sanitize_textarea_field`, `sanitize_email`, `absint`, `sanitize_key`, `esc_url_raw`, `wp_kses_post`). In Acorn controllers, `$request->validate([...])` checks shape; still sanitise what you store.
- ACF: `acf_save_post()` already filters posted values with `wp_kses_post_deep()` for users without `unfiltered_html`; add `acf/update_value/key=…` for type-specific sanitising and `acf/validate_value` for rules (acf-native). Without ACF, `register_post_meta()` with `sanitize_callback` and `auth_callback`.
- Table of sanitisers, uploads and secrets: [references/input-and-sql.md](references/input-and-sql.md).

### 3. Verify intent and authority

- Forms and admin-post: `wp_nonce_field('action', '_name')` + `check_admin_referer('action', '_name')` or `wp_verify_nonce()`; AJAX: `check_ajax_referer()`; REST with cookie auth: the `X-WP-Nonce` header (`wp_rest` nonce) is checked by core.
- Then `current_user_can()` with the most specific capability (meta capabilities like `edit_post` take the object ID).
- REST routes: always a real `permission_callback` (WordPress logs `_doing_it_wrong` when it is missing); `__return_true` only for public reads.
- `wp_ajax_nopriv_*` and public Acorn routes are attacker-controlled traffic: validate everything, expose nothing private.
- Roles, custom capabilities and CPT mapping: [references/capabilities.md](references/capabilities.md).

### 4. Prepare every query

`$wpdb->prepare()` with `%s`, `%d`, `%f`, and `%i` for identifiers; `$wpdb->esc_like()` for `LIKE`. Eloquent and the query builder bind parameters; `DB::raw()`, `whereRaw()` and `selectRaw()` must take bindings (`whereRaw('title = ?', [$input])`).

### Profiles

| | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Views to audit | theme `resources/views/**` | plugin `resources/views/**` (namespaced views) | project `resources/views/**`, including native block render views |
| Extra input surface | ACF fields, theme forms | ACF fields, Livewire components, plugin REST/Acorn routes | block attributes saved from the editor (escape them at render), REST/Acorn routes; no ACF by default |
| Meta sanitising | ACF hooks | ACF hooks | `register_post_meta()` `sanitize_callback` / `auth_callback` |
| Guard test location | theme tests | plugin `tests/` | project `tests/` (Pest) |

## Verification

- Grep for double escaping: `rg -n "\{\{\s*esc_(url|attr|html|textarea|js)(__|_x)?\(" <app>/resources/views` returns nothing; better, keep the guard test from the reference running in `{{runner.test}}`.
- Grep for unfiltered raw output: `rg -n "\{!!" <app>/resources/views` and justify each hit (an `esc_*`, `wp_kses*`, `@json`, or a trusted Htmlable).
- Every handler that writes data shows a nonce (or REST auth) check **and** `current_user_can()`.
- `rg -n "\$wpdb->(query|get_(results|row|var|col))\(" <app>/app` hits all go through `prepare()`.
- Hit protected endpoints as anonymous and as a low-role user (`{{runner.wp}} user create test-sub sub@example.test --role=subscriber`); expect 401/403.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `&#038;` or `&amp;amp;` visible in links or titles | Escaped twice (`{{ esc_url() }}`, or `{{ }}` on text that already has entities) | `{!! esc_url($url) !!}` / `{!! esc_html($text) !!}`; add the guard test |
| XSS through a WYSIWYG or block attribute | `{!! $html !!}` without filtering | `{!! wp_kses_post($html) !!}` or `wp_kses()` with an allow-list |
| CSRF on an Acorn `web` route | Acorn's default `web` middleware group ships with the CSRF middleware commented out; `@csrf` alone verifies nothing | Use WordPress nonces in the controller, or append the CSRF middleware with `withMiddleware()` (see acorn-routes-api) |
| Subscriber can call an admin action | Nonce checked, capability not | Add `current_user_can()` before acting |
| REST route open to everyone | `permission_callback` missing or `__return_true` on a write | Capability-based callback |
| `current_user_can('edit_project', $id)` always false | CPT with custom `capability_type` and `map_meta_cap` false | Set `map_meta_cap => true` and grant the primitive caps |
| SQL injection | Interpolated input in `$wpdb` or `whereRaw()` | `prepare()` / bindings |
| Secret in the repo | Hard-coded key or committed `.env` | Move to the environment, rotate the key, check `.gitignore` |

## Escalation

- A vulnerability in production code: tell the user immediately with severity, affected endpoint and the fix; do not wait for the end of the task.
- A third-party plugin is the source: report it to the user with the evidence; suggest updating or replacing it (wp-composer-plugins).
- Route middleware, auth guards or API design: acorn-routes-api. Livewire action authorisation: acorn-livewire. ACF validation and save flow: acf-native.

<!-- verified:
vendor/illuminate/view/Compilers/BladeCompiler.php:124 — echo format 'e(%s)'; vendor/illuminate/support/helpers.php:124-138 — e() = htmlspecialchars ENT_QUOTES|ENT_SUBSTITUTE, doubleEncode true;
wp/wp-includes/formatting.php:4587 — esc_url display context turns &amp; into &#038;; :945 _wp_specialchars double_encode false (esc_html/esc_attr);
vendor/illuminate/view/ComponentAttributeBag.php:237-243 — merge($defaults, $escape = true) escapes defaults with e(); Compilers/Concerns/CompilesComponents.php:211-219 + ComponentTagCompiler.php:790-795 — bound attributes escaped with e();
vendor/illuminate/view/Compilers/Concerns/CompilesJson.php:12 — @json uses JSON_HEX_TAG|APOS|AMP|QUOT;
advanced-custom-fields-pro/includes/acf-form-functions.php:139-149 — wp_kses_post_deep on $_POST['acf'] without unfiltered_html; includes/api/api-template.php:26,103-139 — get_field $escape_html, the_field escapes;
vendor/roots/acorn/src/Roots/Acorn/Configuration/Middleware.php:88 (acorn 6.2.0) — PreventRequestForgery commented out of the web group;
wp/wp-includes/rest-api.php:122-129 — _doing_it_wrong when permission_callback missing; class-wpdb.php:656-685 — %i identifier placeholder;
wp/wp-includes/class-wp-post-type.php:610-619 — map_meta_cap defaults true only for capability_type post/page;
a Blade single-escape guard test in the reference acorn-mu-plugin project — guard test pattern (generalised in references/blade-escaping.md).
-->
