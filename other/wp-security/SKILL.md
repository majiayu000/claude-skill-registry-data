---
name: superpowers-sage:wp-security
description: >
  WordPress security hardening — nonce verification, wp_nonce_field,
  check_admin_referer, sanitize_text_field, sanitize_email, esc_html, esc_attr,
  esc_url, wp_kses, SQL injection prevention, $wpdb->prepare(), capability checks,
  current_user_can, authentication hardening, wp-config.php secrets,
  security headers, file permissions, Bedrock .env secrets, disable XML-RPC,
  brute force wp-login.php, CSRF protection.
  Invoke for: security audit, input sanitization, output escaping, nonce verification,
  SQL injection prevention, CSRF protection, capability checks in REST endpoints.
user-invocable: false
---

# WordPress Security Patterns for Sage/Acorn

## When to use

Apply this skill whenever writing or reviewing code that handles user input, renders output, checks permissions, interacts with the database via `$wpdb`, processes file uploads, or stores sensitive configuration. This skill is also used as a final review pass by the sage-router when other skills produce code.

## Inputs required

- The code or feature under review/development
- The context: Blade template, Livewire component, Service class, middleware, or REST endpoint

## Procedure

### Step 1 — Sanitize on input

Every value originating from the user (`$_GET`, `$_POST`, `$_REQUEST`, form submissions, URL parameters) must be sanitized before storage or processing.

**Common sanitization functions:**

| Function | Use for |
|---|---|
| `sanitize_text_field()` | Single-line plain text |
| `sanitize_textarea_field()` | Multi-line plain text |
| `sanitize_email()` | Email addresses |
| `sanitize_url()` | URLs |
| `absint()` | Non-negative integers |
| `sanitize_file_name()` | File names |
| `wp_kses_post()` | Rich HTML (post-level allowed tags) |
| `wp_kses()` | HTML with custom allowed tags |
| `sanitize_title()` | Slugs |

In Acorn Service classes and controllers, sanitize at the point of entry:

```php
public function store(Request $request): void
{
    $title = sanitize_text_field($request->input('title'));
    $body  = wp_kses_post($request->input('body'));
}
```

### Step 2 — Escape on output

Every dynamic value rendered in a Blade template must be escaped. Blade's `{{ }}` syntax auto-escapes via `htmlspecialchars`. Use `{!! !!}` only when you have already sanitized the content and intentionally need raw HTML.

```blade
{{-- Safe — auto-escaped --}}
<h1>{{ $post->post_title }}</h1>
<p>{{ get_the_excerpt() }}</p>

{{-- Raw output — only after sanitization --}}
{!! wp_kses_post($post->post_content) !!}
```

**Contextual escaping helpers:**

| Context | Function |
|---|---|
| HTML body | `esc_html()` or `{{ }}` |
| HTML attribute | `esc_attr()` |
| URL / href | `esc_url()` |
| JavaScript inline | `esc_js()` |
| Textarea content | `esc_textarea()` |

In Blade, when outputting into attributes:

```blade
<a href="{{ esc_url($link) }}" title="{{ esc_attr($title) }}">
    {{ $label }}
</a>
```

### Step 3 — Nonce verification

Always pair form submissions and AJAX requests with nonce verification.

**Traditional forms in Blade:**

```blade
<form method="POST" action="{{ admin_url('admin-post.php') }}">
    @csrf {{-- If using Acorn middleware --}}
    {!! wp_nonce_field('my_action', '_my_nonce', true, false) !!}
    <button type="submit">Submit</button>
</form>
```

Server-side verification:

```php
if (! wp_verify_nonce($_POST['_my_nonce'] ?? '', 'my_action')) {
    wp_die('Security check failed.', 403);
}
```

**AJAX requests:**

```php
// In callback
check_ajax_referer('my_ajax_action', 'nonce');
```

**Livewire components:** Livewire handles CSRF automatically via its middleware. No manual nonce is needed for Livewire actions, but verify capabilities on the server side in every action method.

### Step 4 — Capability checks

Never rely on nonces alone. Always verify the user has permission to perform the action:

```php
if (! current_user_can('edit_posts')) {
    wp_die('Unauthorized.', 403);
}
```

Pair capability checks with nonces — the nonce proves intent, the capability proves authorization:

```php
public function handleFormSubmission(): void
{
    if (! wp_verify_nonce($_POST['_nonce'] ?? '', 'update_settings')) {
        wp_die('Invalid nonce.', 403);
    }

    if (! current_user_can('manage_options')) {
        wp_die('Insufficient permissions.', 403);
    }

    // Proceed with action
}
```

### Step 5 — SQL preparation

When using `$wpdb` directly (in Service classes or legacy code), always use `$wpdb->prepare()`:

```php
global $wpdb;

$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_type = %s AND post_status = %s",
        'custom_type',
        'publish'
    )
);
```

**Eloquent is safe by default.** Acorn's Eloquent ORM uses parameterized queries internally. Standard Eloquent usage does not require manual preparation:

```php
// Safe — parameterized by Eloquent
$posts = Post::where('post_type', 'custom_type')
    ->where('post_status', 'publish')
    ->get();
```

Never pass raw user input into `DB::raw()` or `whereRaw()` without bindings:

```php
// DANGEROUS
DB::raw("SELECT * FROM posts WHERE title = '$userInput'");

// SAFE
DB::select('SELECT * FROM posts WHERE title = ?', [$userInput]);
```

### Step 6 — CSRF protection via Acorn middleware

If the project uses Acorn's HTTP layer, register the `VerifyCsrfToken` middleware in the kernel:

```php
// app/Http/Kernel.php
protected $middlewareGroups = [
    'web' => [
        \App\Http\Middleware\VerifyCsrfToken::class,
    ],
];
```

Blade forms using Acorn routes must include `@csrf`:

```blade
<form method="POST" action="{{ route('contact.store') }}">
    @csrf
    {{-- fields --}}
</form>
```

### Step 7 — File upload validation

For Livewire components using `WithFileUploads`:

```php
use Livewire\WithFileUploads;

class UploadForm extends \Livewire\Component
{
    use WithFileUploads;

    public $file;

    protected $rules = [
        'file' => 'required|file|mimes:jpg,png,pdf|max:2048', // 2MB max
    ];

    public function save(): void
    {
        $this->validate();

        // Use WordPress upload functions for proper media library integration
        $attachment_id = media_handle_upload('file', 0);
    }
}
```

For traditional uploads, validate MIME types server-side — never trust the client extension:

```php
$filetype = wp_check_filetype($filename, null);
if (! in_array($filetype['type'], ['image/jpeg', 'image/png', 'application/pdf'], true)) {
    wp_die('Invalid file type.');
}
```

### Step 8 — Secrets management

All sensitive values go in `.env` and are accessed via `env()` or `config()`:

```env
STRIPE_SECRET_KEY=sk_live_...
API_TOKEN=abc123
```

```php
// config/services.php
'stripe' => [
    'secret' => env('STRIPE_SECRET_KEY'),
],

// Usage
$key = config('services.stripe.secret');
```

Never hardcode secrets in:
- PHP source files
- Blade templates
- JavaScript files
- Version-controlled config files
- Composer scripts

Ensure `.env` is listed in `.gitignore`.

## Verification

- [ ] No `{!! !!}` usage without prior sanitization (`wp_kses_post` or equivalent)
- [ ] All form submissions verify a nonce
- [ ] All privileged actions check `current_user_can()`
- [ ] All `$wpdb` queries use `$wpdb->prepare()`
- [ ] No raw user input in `DB::raw()` or `whereRaw()` without bindings
- [ ] File uploads validate MIME types server-side
- [ ] Secrets are in `.env`, never in source code
- [ ] `.env` is in `.gitignore`
- [ ] CSRF middleware is active for Acorn web routes

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| XSS in rendered page | Using `{!! !!}` with unsanitized data | Switch to `{{ }}` or sanitize with `wp_kses_post()` before raw output |
| CSRF attack succeeds | Missing nonce or `@csrf` | Add `wp_nonce_field()` or `@csrf` and verify server-side |
| Unauthorized access | Missing `current_user_can()` check | Add capability check before every privileged operation |
| SQL injection | Raw `$wpdb` query without `prepare()` | Wrap query in `$wpdb->prepare()` with typed placeholders |
| Secrets leaked in repo | Hardcoded API keys | Move to `.env`, rotate compromised keys immediately |
| Malicious file upload | Missing MIME validation | Validate with `wp_check_filetype()` and restrict allowed types |

## Escalation

- If a vulnerability is found in production code, flag it to the user immediately with severity level and remediation steps.
- If a third-party plugin introduces a security concern, recommend the user contact the plugin author or find an alternative.
- If the security requirement exceeds WordPress capabilities (e.g., SOC 2 compliance), recommend consulting a security specialist.
