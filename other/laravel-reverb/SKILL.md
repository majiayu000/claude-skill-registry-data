---
model_tier: medium
name: laravel-reverb
description: "Use when configuring Laravel Reverb — the first-party WebSocket server with Pusher protocol compatibility, horizontal scaling, and Pulse monitoring."
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

# laravel-reverb

## When to use

Use this skill for anything specific to **Laravel Reverb** as the WebSocket server:
- Reverb installation, configuration, and environment setup
- Reverb server deployment and scaling
- Reverb-specific debugging and monitoring
- Pusher protocol compatibility questions

For **general WebSocket patterns**, broadcasting events, channel authorization,
and Laravel Echo client setup, see the [laravel-websocket](../laravel-websocket/SKILL.md) skill.

## Procedure: Set up Reverb

1. **Inspect current broadcasting** — Check `config/broadcasting.php`, `.env`, and `composer.json` for Pusher / Reverb / Soketi presence and current driver.
2. **Install** — `php artisan install:broadcasting` or manual setup (see below).
3. **Configure** — Set environment variables for Reverb host, port, app credentials.
4. **Start server** — `php artisan reverb:start`.
5. **Connect client** — Configure Laravel Echo with Reverb credentials.
6. **Verify** — Confirm WebSocket connection in browser console, test event delivery.

Laravel Reverb is Laravel's first-party, blazing-fast WebSocket server. It uses the
**Pusher protocol**, making it compatible with Laravel Echo and any Pusher-compatible client.
A single Reverb server can handle thousands of concurrent connections.

## Installation

```bash
php artisan install:broadcasting
```

This scaffolds:
- `config/broadcasting.php` with Reverb driver
- `config/reverb.php` with server settings
- `routes/channels.php` for channel authorization
- `.env` variables for Reverb

## Configuration

### Environment variables

```env
REVERB_APP_ID=455493
REVERB_APP_KEY=your-app-key
REVERB_APP_SECRET=your-app-secret
REVERB_HOST="localhost"
REVERB_PORT=8080
REVERB_SCHEME=http

# Client-side (Vite)
VITE_REVERB_APP_KEY="${REVERB_APP_KEY}"
VITE_REVERB_HOST="${REVERB_HOST}"
VITE_REVERB_PORT="${REVERB_PORT}"
VITE_REVERB_SCHEME="${REVERB_SCHEME}"
```

### config/reverb.php

Note: `REVERB_HOST` / `REVERB_PORT` are for client connections (hostname/port the client connects to).
`REVERB_SERVER_HOST` / `REVERB_SERVER_PORT` are for the server binding (interface/port the server listens on).

```php
'servers' => [
    'reverb' => [
        'host' => env('REVERB_SERVER_HOST', '0.0.0.0'),
        'port' => env('REVERB_SERVER_PORT', 8080),
        'hostname' => env('REVERB_HOST'),
        'options' => [
            'tls' => [],
        ],
        'max_request_size' => 10_000,  // bytes
        'scaling' => [
            'enabled' => env('REVERB_SCALING_ENABLED', false),
            'channel' => env('REVERB_SCALING_CHANNEL', 'reverb'),
        ],
        'pulse_ingest_interval' => 15,
    ],
],
```

### config/broadcasting.php

```php
'connections' => [
    'reverb' => [
        'driver' => 'reverb',
        'key' => env('REVERB_APP_KEY'),
        'secret' => env('REVERB_APP_SECRET'),
        'app_id' => env('REVERB_APP_ID'),
        'options' => [
            'host' => env('REVERB_HOST'),
            'port' => env('REVERB_PORT', 443),
            'scheme' => env('REVERB_SCHEME', 'https'),
            'useTLS' => env('REVERB_SCHEME', 'https') === 'https',
        ],
    ],
],
```

## Running the server

```bash
# Start Reverb (foreground)
php artisan reverb:start

# Start with verbose output (debugging)
php artisan reverb:start --debug

# Production — use Supervisor or systemd
# Reverb is a long-running process, it must be managed by a process monitor
```

### Supervisor config (production)

```ini
[program:reverb]
command=php /path/to/artisan reverb:start
autostart=true
autorestart=true
user=www-data
redirect_stderr=true
stdout_logfile=/var/log/reverb.log
stopwaitsecs=3600
```

## Horizontal scaling

Enable Redis-based scaling to run multiple Reverb instances behind a load balancer:

```env
REVERB_SCALING_ENABLED=true
REVERB_SCALING_CHANNEL=reverb
```

Requires a shared Redis instance accessible by all Reverb servers.
Connections and channel subscriptions are synced across servers via Redis pub/sub.

## Monitoring with Pulse

Reverb has built-in Laravel Pulse integration. Add the Reverb Pulse cards:

```php
// In your Pulse dashboard
<livewire:reverb.connections />
<livewire:reverb.messages />
```

## SSL/TLS in production

Reverb itself does **not** handle TLS. Use a reverse proxy (Nginx, Traefik, Caddy)
to terminate SSL and proxy WebSocket connections to Reverb:

```nginx
location /app {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 60s;
    proxy_send_timeout 60s;
}
```

## Core rules

- **Reverb is a long-running process** — always use Supervisor/systemd in production.
- **TLS via reverse proxy** — Reverb doesn't handle SSL directly.
- **Scale with Redis** — enable `REVERB_SCALING_ENABLED` for multi-server setups.
- **Monitor with Pulse** — use the built-in Pulse cards for connection/message metrics.
- **Pusher protocol** — any Pusher-compatible client works (Laravel Echo, pusher-js, etc.).
- **Max request size** — default 10KB, increase for large payloads if needed.

## Output format

1. Reverb configuration with server and scaling settings
2. Broadcasting channel definitions and client integration

## Auto-trigger keywords

- Reverb
- reverb:start
- WebSocket server
- Reverb scaling
- Reverb deployment
- Reverb configuration

## Gotcha

- Reverb requires a persistent process — it's not compatible with serverless deployments.
- The model forgets to configure the `REVERB_HOST` and `REVERB_PORT` environment variables.
- WebSocket connections bypass middleware — don't rely on session auth for channel authorization.

## Do NOT

- Do NOT expose Reverb directly to the internet without a reverse proxy for TLS.
- Do NOT run `reverb:start` without a process monitor in production.
- Do NOT confuse Reverb config with Pusher SaaS — Reverb is self-hosted.
- Do NOT skip Redis when running multiple Reverb instances.
