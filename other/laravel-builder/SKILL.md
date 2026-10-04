---
name: laravel-builder
description: >
  Scaffold a complete Laravel 11 project from scratch — Breeze auth, Filament admin panel,
  PostgreSQL config, Sail/Docker dev environment, and Paymob webhook endpoint.
  Triggers when user asks to build a Laravel project, create a Laravel app,
  scaffold Laravel with admin panel, or set up Laravel with PostgreSQL.
---

# Laravel Builder Agent

## Step 1 — Bootstrap Laravel 11 Project

```bash
composer create-project laravel/laravel project-name
cd project-name
composer require filament/filament:^3.2 laravel/sanctum
composer require --dev tailwindcss/laravel-vite-plugin
php artisan filament:install --panels
```

## Step 2 — PostgreSQL Config

```env
DB_CONNECTION=pgsql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=project_db
DB_USERNAME=postgres
DB_PASSWORD=
```

```php
// database/migrations/...create_users_table.php
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email')->unique();
    $table->timestamp('email_verified_at')->nullable();
    $table->string('password');
    $table->rememberToken();
    $table->timestamps();
    // PostgreSQL-specific
    $table->uuid('uuid')->unique()->default(DB::raw('gen_random_uuid()'));
});
```

## Step 3 — Sail + Docker Dev Environment

```bash
composer require laravel/sail --dev
php artisan sail:install --with=mysql,redis,mailhog
# OR for PostgreSQL:
php artisan sail:install --with=pgsql
docker compose up -d
```

Alternative (no Docker — use Laravel Herd/DValet):
```bash
# Create PostgreSQL DB
createdb project_db
# Add to .env
DB_CONNECTION=pgsql
```

## Step 4 — Laravel Breeze Auth

```bash
php artisan breeze:install
php artisan migrate
npm install
npm run dev
```

## Step 5 — Filament Admin Panel

```bash
php artisan make:filament-resource Booking --generate
php artisan make:filament-resource Package --generate
php artisan make:filament-resource Guest --generate
```

```php
// app/Providers/FilamentServiceProvider.php
public function boot(): void
{
    Filament::registerResources([
        BookingResource::class,
        PackageResource::class,
        GuestResource::class,
    ]);
}
```

## Step 6 — Paymob Webhook Setup

```bash
# Install Paymob SDK
composer require paymob/paymob
```

```php
// routes/web.php
use App\Http\Controllers\PaymobWebhookController;

Route::post('/webhook/paymob', [PaymobWebhookController::class, 'handle'])
    ->withoutMiddleware([\Illuminate\Foundation\Http\Middleware\VerifyCsrfToken::class]);
```

```php
// app/Http/Controllers/PaymobWebhookController.php
class PaymobWebhookController extends Controller
{
    public function handle(Request $request)
    {
        $hmac = $request->input('hmac');
        $raw = $request->getContent();
        $expected = hash_hmac('sha512', config('services.paymob.hmac_secret'), $raw);

        if (!hash_equals($expected, $hmac)) {
            return response('Invalid signature', 401);
        }

        $type = $request->input('type');
        $data = $request->input('obj');

        match ($type) {
            'TRANSACTION_CREATED' => $this->handleTransaction($data),
            'TRANSACTION_REFUND' => $this->handleRefund($data),
            default => response('OK'),
        };
    }
}
```

## Step 7 — n8n Webhook Trigger

```php
// app/Services/N8nService.php
class N8nService
{
    public function trigger(string $event, array $payload): void
    {
        Http::post(config('services.n8n.webhook_url'), [
            'event' => $event,
            'timestamp' => now()->toIso8601String(),
            'payload' => $payload,
        ]);
    }
}
```

## Project Structure
```
project/
├── app/
│   ├── Filament/Resources/     ← admin resources
│   ├── Http/Controllers/      ← API + webhook controllers
│   └── Services/
│       ├── PaymobService.php
│       └── N8nService.php
├── database/migrations/         ← all table migrations
├── routes/web.php              ← web routes
├── resources/views/             ← guest-facing Blade views
├── .env.example
└── composer.json
```

## Deployment (Railway)
- Railway supports PHP 8.2 via Nixpacks
- Use `railway.json` or `Procfile`
- Connect Railway Postgres
- Set environment variables from Railway dashboard
