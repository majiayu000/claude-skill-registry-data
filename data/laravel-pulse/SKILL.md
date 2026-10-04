---
model_tier: medium
name: laravel-pulse
description: "Use when setting up Laravel Pulse — real-time dashboard, built-in cards, custom recorders, performance insights — even when the user just says 'I need app monitoring' without naming Pulse."
domain: engineering
workspaces:
  - engineering
packs:
  - laravel
trust:
  level: professional
install:
  default: false
  removable: true
---

# laravel-pulse

## When to use

Use this skill when working with Laravel Pulse:
- Setting up the Pulse monitoring dashboard
- Configuring built-in recorders (slow queries, exceptions, queues, etc.)
- Creating custom Pulse cards and recorders
- Performance monitoring and alerting

## Procedure: Set up Pulse

1. **Inspect current monitoring** — Check `composer.json`, existing telemetry packages, and `config/` for Pulse, Telescope, or Horizon already installed; identify gaps.
2. **Install** — `composer require laravel/pulse`, publish config, run migrations.
3. **Configure** — Set up recorders in `config/pulse.php`.
4. **Add dashboard** — Register route and authorize access.
5. **Verify** — Visit `/pulse` dashboard, confirm data is being recorded.

### Installation

```bash
composer require laravel/pulse
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
php artisan migrate
```

## Dashboard

### Access control

```php
// PulseServiceProvider or Gate
Gate::define('viewPulse', function (User $user): bool {
    return $user->isSuperuser();
});
```

### Dashboard route

Pulse registers `/pulse` automatically. Customize in `config/pulse.php`:

```php
'path' => 'pulse',
'middleware' => ['web', 'auth'],
```

## Built-in cards

| Card | What it shows |
|---|---|
| `<livewire:pulse.servers />` | CPU, memory, storage per server |
| `<livewire:pulse.usage />` | Top users by request count |
| `<livewire:pulse.queues />` | Queue throughput and wait times |
| `<livewire:pulse.slow-queries />` | Slowest database queries |
| `<livewire:pulse.slow-requests />` | Slowest HTTP requests |
| `<livewire:pulse.slow-jobs />` | Slowest queued jobs |
| `<livewire:pulse.slow-outgoing-requests />` | Slowest external HTTP calls |
| `<livewire:pulse.exceptions />` | Most frequent exceptions |
| `<livewire:pulse.cache />` | Cache hit/miss ratio |

### Dashboard view

```blade
{{-- resources/views/vendor/pulse/dashboard.blade.php --}}
<x-pulse>
    <livewire:pulse.servers cols="full" />

    <livewire:pulse.usage cols="4" rows="2" />
    <livewire:pulse.queues cols="4" />
    <livewire:pulse.cache cols="4" />

    <livewire:pulse.slow-queries cols="8" />
    <livewire:pulse.exceptions cols="4" />

    <livewire:pulse.slow-requests cols="6" />
    <livewire:pulse.slow-jobs cols="6" />
</x-pulse>
```

## Configuration

### config/pulse.php

```php
'recorders' => [
    \Laravel\Pulse\Recorders\SlowQueries::class => [
        'enabled' => true,
        'threshold' => 1000,  // ms
        'sample_rate' => 1.0,
    ],
    \Laravel\Pulse\Recorders\SlowRequests::class => [
        'enabled' => true,
        'threshold' => 1000,  // ms
        'sample_rate' => 1.0,
    ],
    \Laravel\Pulse\Recorders\Exceptions::class => [
        'enabled' => true,
        'sample_rate' => 1.0,
    ],
],

// Data retention
'ingest' => [
    'trim' => [
        'lottery' => [1, 1000],
        'keep' => '7 days',
    ],
],
```

## Custom recorders

```php
use Laravel\Pulse\Facades\Pulse;

// Record a custom entry
Pulse::record('api_call', 'stripe', 250)  // type, key, value
    ->avg()
    ->count();
```

## Core rules

- **Trim old data** — configure retention to prevent database bloat.
- **Use sample rates** in production — not every request needs recording.
- **Separate database** — consider a dedicated DB connection for Pulse data.
- **Restrict access** — always gate the dashboard behind authentication.
- **Monitor what matters** — don't enable all recorders if you don't need them.

## Output format

1. Pulse configuration with recorders and dashboard cards
2. Custom recorder class if needed

## Auto-trigger keywords

- Pulse
- monitoring dashboard
- slow queries
- slow requests
- application monitoring
- performance dashboard

## Gotcha

- Pulse stores data in the same database by default — configure a separate connection for production.
- The model forgets that Pulse data is sampled, not exact — don't use it for billing or exact counts.
- Custom recorders must be registered in a service provider — they don't auto-discover.

## Do NOT

- Do NOT expose the Pulse dashboard without authentication.
- Do NOT set sample rate to 1.0 on high-traffic production — use 0.1 or lower.
- Do NOT forget to run `pulse:check` for server metrics.
- Do NOT store Pulse data in the main application database on large apps.
