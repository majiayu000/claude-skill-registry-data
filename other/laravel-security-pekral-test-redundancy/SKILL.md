---
name: laravel-security
description: "Use when building, configuring, or hardening security-sensitive Laravel features — authentication, authorization, Eloquent safety, CSRF/XSS, API security, file uploads, secrets, and production configuration. Provides condensed, copy-ready secure defaults for Laravel 12/13 / PHP 8.4/8.5."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/security/backend.md` and `@rules/security/frontend.md`
- Apply `@rules/php/core-standards.md` — `final` classes, `declare(strict_types=1)`, typed signatures
- If the project uses Laravel, also apply `@rules/laravel/laravel.md`, `@rules/laravel/architecture.md`, `@rules/laravel/filament.md`, `@rules/laravel/livewire.md`
- Stack: Laravel 12/13 / PHP 8.4/8.5, Filament, Livewire, Alpine.js, Blade, Tailwind, Pest, Vite, MySQL, Redis
- Never hardcode secrets; never reveal them in output

## Scope
Secure-by-default building blocks for security-sensitive Laravel work. Use the matching section, copy the minimal snippet, and verify against the checklist. For an audit of existing code use `@skills/security-review/SKILL.md`.

## Use when
- Setting up authentication / authorization (Sanctum, gates, policies, middleware)
- Configuring production settings and environment variables
- Writing secure Eloquent queries and models
- Hardening CSRF / XSS / input validation / file uploads / API endpoints
- Managing secrets, queue payloads, and security event logging

## Production Configuration

```php
// config/app.php
'debug' => (bool) env('APP_DEBUG', false), // CRITICAL: never true in production
'key' => env('APP_KEY'),                    // php artisan key:generate

// config/session.php
'secure' => env('SESSION_SECURE_COOKIE', true),
'http_only' => true,
'same_site' => 'lax',
```

Validate required config at boot and fail fast:

```php
// AppServiceProvider::boot()
foreach (['app.key', 'database.connections.mysql.database'] as $key) {
    if (empty(config($key))) {
        throw new RuntimeException("Missing required config key: {$key}");
    }
}
```

HTTPS and trusted proxies:

```php
if (app()->environment('production')) {
    URL::forceScheme('https');
}
// Use specific CIDR ranges, never '*' (X-Forwarded-* spoofing)
'trusted_proxies' => ['10.0.0.0/8', '172.16.0.0/12'],
```

Keep `.env` out of version control (`.gitignore` ships with `.env`); ship `.env.example` with empty placeholders.

## Authentication

### Sanctum (API tokens)

```php
// config/sanctum.php
'expiration' => 60 * 24,                          // minutes; null = never
'token_prefix' => env('SANCTUM_TOKEN_PREFIX', ''),

$token = $user->createToken('api', ['posts:read', 'posts:write'])->plainTextToken;

Route::middleware('auth:sanctum')->group(function () {
    Route::get('/posts', [PostController::class, 'index'])->middleware('abilities:posts:read');
    Route::post('/posts', [PostController::class, 'store'])->middleware('abilities:posts:write');
});
```

### Passwords

```php
// config/hashing.php — bcrypt rounds >= 12, or Argon2id
'bcrypt' => ['rounds' => env('BCRYPT_ROUNDS', 12)],

// FormRequest rules
'password' => [
    'required', 'confirmed',
    Password::min(12)->letters()->mixedCase()->numbers()->symbols()->uncompromised(),
],
```

### Sessions

```php
// config/session.php — 'driver' => 'database' or 'redis' (avoid 'file' in prod)

public function store(LoginRequest $request): RedirectResponse
{
    $request->authenticate();
    $request->session()->regenerate(); // CRITICAL: prevents session fixation
    return redirect()->intended('/dashboard');
}

public function destroy(Request $request): RedirectResponse
{
    Auth::guard('web')->logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();
    return redirect('/');
}
```

## Authorization

### Gates

```php
// AppServiceProvider::boot()
Gate::define('update-post', fn (User $user, Post $post): bool => $user->id === $post->user_id);

Gate::before(function (User $user, string $ability): ?bool {
    return $user->role === 'super-admin' ? true : null; // null = fall through
});

// Controller
Gate::authorize('update-post', $post);
```

### Policies

```php
final class PostPolicy
{
    public function view(?User $user, Post $post): bool
    {
        return $post->is_published || ($user && $user->id === $post->user_id);
    }

    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}

// Controller: $this->authorize('update', $post);
// Blade: @can('update', $post) ... @endcan
```

Laravel auto-discovers policies by naming convention; register explicitly only when names differ.

### Middleware

```php
Route::put('/posts/{post}', [PostController::class, 'update'])->middleware('can:update,post');

Route::middleware(['auth', 'role:admin'])->group(function () {
    Route::get('/admin', [AdminController::class, 'index']);
});
```

For Filament, enforce access via policies and `canAccessPanel()`; for Livewire, re-check authorization inside actions — a mounted component is not an authorization boundary (`@rules/laravel/filament.md`, `@rules/laravel/livewire.md`).

## Eloquent Security

### Mass assignment

```php
final class User extends Authenticatable
{
    protected $fillable = ['name', 'email', 'phone', 'avatar'];
    // NEVER list 'role', 'is_admin'; NEVER use $guarded = []
}

User::create($request->validated());        // GOOD: validated fields only
// User::create($request->all());           // VULNERABLE
```

### SQL injection

```php
User::where('email', $userInput)->first();                  // parameterized
User::whereRaw('email = ?', [$userInput])->first();         // parameterized
DB::select('SELECT * FROM users WHERE email = ?', [$input]); // parameterized

// VULNERABLE — never interpolate user input:
// User::whereRaw("email = '{$userInput}'")->first();
// User::orderByRaw($userInput);  DB::statement("... '{$userInput}'");
```

### Casting and hidden attributes

```php
final class User extends Authenticatable
{
    protected $casts = [
        'is_admin' => 'boolean',
        'settings' => 'array',
        'metadata' => 'encrypted:array', // encrypted cast
        'password' => 'hashed',          // auto-hash on set
    ];

    protected $hidden = ['password', 'remember_token', 'two_factor_secret'];
}
```

## CSRF Protection

CSRF is on by default for the `web` group. State-changing forms need `@csrf`:

```blade
<form method="POST" action="/posts">@csrf ...</form>
```

Exclude only specific signature-verified webhooks — never blanket `api/*` (stateful Sanctum needs CSRF):

```php
// bootstrap/app.php — $middleware->validateCsrfTokens(except: ['stripe/*'])
```

For JS, send the token header (Axios ships preconfigured in Laravel):

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

## XSS Prevention

```blade
{{ $userInput }}        {{-- SAFE: auto-escaped --}}
{!! $userInput !!}      {{-- DANGEROUS: raw, never with user input --}}
{!! $trustedHtml !!}    {{-- only for content you fully control --}}

<script>
    const user = @js($user);      {{-- escaped for JS context --}}
    const cfg  = @json($config);
</script>
```

When user HTML must survive, purify with an allowlist before storing/output:

```php
// composer require ezyang/htmlpurifier
$config = \HTMLPurifier_Config::createDefault();
$config->set('HTML.Allowed', 'p,b,i,a[href],ul,ol,li,br');
$config->set('URI.AllowedSchemes', ['http', 'https', 'mailto']);
$clean = (new \HTMLPurifier($config))->purify($dirty);
```

In Alpine, prefer `x-text` over `x-html`; only use `x-html` on sanitized content. Add security headers via middleware:

```php
$response->headers->set('X-Content-Type-Options', 'nosniff');
$response->headers->set('X-Frame-Options', 'DENY');
$response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');
$response->headers->set('Content-Security-Policy',
    "default-src 'self'; frame-ancestors 'none'");
```

## Input Validation

Always validate through a FormRequest; never persist `$request->all()`:

```php
final class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()?->can('create', Post::class) ?? false;
    }

    public function rules(): array
    {
        return [
            'title'   => ['required', 'string', 'max:255'],
            'content' => ['required', 'string', 'max:10000'],
            'tags'    => ['array'],
            'tags.*'  => ['integer', 'exists:tags,id'],
        ];
    }
}
```

Keep validation messages generic — never leak which auth factor failed, whether a record exists, or framework internals (`@rules/security/backend.md`).

## API Security

### Rate limiting

```php
// AppServiceProvider::boot()
RateLimiter::for('api', fn (Request $r) =>
    Limit::perMinute(60)->by($r->user()?->id ?: $r->ip()));

RateLimiter::for('auth', fn (Request $r) =>
    Limit::perMinute(5)->by($r->ip()));

Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:auth');
```

### CORS

```php
// config/cors.php
'paths' => ['api/*', 'sanctum/csrf-cookie'],
'allowed_origins' => explode(',', env('CORS_ALLOWED_ORIGINS', '')), // explicit allowlist
'supports_credentials' => true, // required for Sanctum SPA auth
// NEVER ['*'] when credentials are supported
```

## File Upload Security

```php
public function rules(): array
{
    return [
        'document' => ['required', 'file', 'mimes:pdf,doc,docx', 'max:10240',
                       'extensions:pdf,doc,docx'],
        'avatar'   => ['nullable', 'image', 'mimes:jpg,jpeg,png,webp', 'max:2048',
                       'dimensions:max_width=2000,max_height=2000'],
    ];
}
```

Store sensitive files off the public disk and serve through an authorized, time-limited URL:

```php
$path = $request->file('document')->store('documents', 'local'); // not 'public'

public function download(Request $request, string $path): RedirectResponse
{
    $this->authorize('download', $path);
    return redirect(Storage::temporaryUrl($path, now()->addMinutes(15)));
}
```

## Secrets and Dependencies

```bash
composer audit          # run in CI; fail the build on advisories
# keep composer.lock committed; run composer update deliberately, never in CI
```

Read every secret from `env()`/`config()`; validate presence at boot. For production use a secret manager rather than a deployed `.env`.

## Queue Security

```php
// Encrypt sensitive payloads on the wire
final class ProcessPaymentJob implements ShouldQueue, ShouldBeEncrypted
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        private readonly string $paymentIntentId,
        private readonly string $cardFingerprint,
    ) {}

    public function handle(): void { /* ... */ }

    public function retryUntil(): \Carbon\CarbonInterface
    {
        return now()->addMinutes(5);
    }
}
```

## Logging Security Events

```php
// config/logging.php — dedicated 'security' channel
final class SecurityLogger
{
    public static function log(string $event, array $context = []): void
    {
        Log::channel('security')->warning($event, array_merge([
            'user_id' => Auth::id(),
            'ip'      => request()->ip(),
            'url'     => request()->fullUrl(),
        ], $context));
    }
}

SecurityLogger::log('failed_login_attempt', ['email' => $email]);
SecurityLogger::log('role_change', ['target_user' => $targetId, 'new_role' => 'admin']);
```

## Quick Security Checklist

| Check | Description |
|-------|-------------|
| `APP_DEBUG=false` | Never run with debug enabled in production |
| `APP_KEY` set | Always run `php artisan key:generate` |
| HTTPS enforced | Force HTTPS in production via middleware or proxy |
| `$fillable` whitelisted | Never use `$guarded = []` |
| CSRF active | `@csrf` on all state-changing forms |
| Sanctum scopes | Token abilities enforced per route |
| Rate limiting | Throttle API and auth endpoints |
| Input validation | FormRequest with specific rules, never `$request->all()` |
| File upload restrictions | Validate MIME, extension, size, dimensions |
| `composer audit` in CI | Check dependencies for known vulnerabilities |
| Password hashing | Laravel bcrypt/Argon2, `'password' => 'hashed'` cast |
| Session regeneration | Call `$request->session()->regenerate()` on login |
| Security headers | CSP, X-Frame-Options, X-Content-Type-Options |
| Security event logging | Audit auth failures, role changes, suspicious activity |
| `.env` not committed | Verify `.gitignore` includes `.env` |

## Laravel Security Audit

When auditing an existing Laravel application (instead of building new features), use `@skills/laravel-security/references/audit-workflow.md`. It covers the 7 audit areas — Authorization/IDOR/BOLA, Authentication, Validation, XSS, File upload, Secrets/configuration, Dependencies — with severity mapping (Critical → Critical; High/Medium/Low → Moderate; Info → not published), Grep patterns, and a required regression-test sketch per confirmed finding. The building blocks in this file (Production Configuration, Authentication, Authorization, Eloquent Security, CSRF, XSS Prevention, Input Validation, File Upload Security, Secrets and Dependencies) are the reference fixes the audit workflow links back to.

## Done when
- The relevant secure default is applied and matches the project's existing style
- No secret is hardcoded; required config/secrets are validated at boot
- Every applicable row of the checklist is satisfied or consciously waived
- Tests (Pest) cover the new auth/authorization/validation behavior

## Related Skills
- `@skills/security-review/SKILL.md` — review workflow for existing code
- `@skills/security-threat-analysis/SKILL.md` — remediate a referenced advisory/CVE
- `@skills/test-driven-development/SKILL.md` — drive the implementation test-first

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
