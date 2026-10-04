---
model_tier: high
name: php-debugging
description: "Use when debugging PHP with Xdebug — breakpoints, step-through, dual-container setup, IDE configuration, header-based routing — even when the user just says 'why does this blow up on request X'."
domain: engineering
workspaces:
  - engineering
packs:
  - php
trust:
  level: professional
install:
  default: false
  removable: true
---

# php-debugging

## When to use

Use this skill when:
- Setting up or troubleshooting Xdebug
- Debugging PHP code with breakpoints
- Investigating performance issues
- Running code coverage
- Helping users configure their IDE for debugging

This skill extends `php-coder` and `php`.

## Procedure: Debug with Xdebug

1. **Detect the project's debug setup** — check `docker-compose.yml` / `compose.yaml` for Xdebug containers.
2. **Check Dockerfile** — look for a `dev-xdebug` build stage or Xdebug installation.
3. **Check NGINX config** — look for header-based routing to a debug container.
4. **Read project docs** — check `Docs/XDEBUG_SETUP.md` or `docs/` for setup instructions.
5. **Check `.env`** — look for `DOCKER_XDEBUG_MODE` and `DOCKER_XDEBUG_PORT`.

## Dual-container architecture

Many projects use two PHP containers for optimal performance:

| Container | Purpose | When used |
|---|---|---|
| `*-php` | Fast PHP-FPM, no Xdebug overhead | All normal requests |
| `*-php-xdebug` | PHP-FPM with Xdebug enabled | Only debug requests |

NGINX routes requests based on HTTP headers:
- **No debug header** → fast container (no Xdebug)
- **Debug header present** → Xdebug container

### Debug headers

| Header | Value | Recommended for |
|---|---|---|
| `X-Xdebug-Enable` | `1` or `true` | Manual tests, Postman |
| `X-Debug-Session` | `PHPSTORM` | IDE integration |
| `XDEBUG-SESSION` | any value | Standard Xdebug header |

**Important:** Use hyphens, not underscores. `XDEBUG_SESSION` does NOT work — use `XDEBUG-SESSION`.

### Verify routing

Check the `X-PHP-Backend` response header to confirm which container handled the request:

```bash
# Normal request
curl -I http://localhost:8002/  # → X-PHP-Backend: *-php:9000

# Debug request
curl -I -H "X-Xdebug-Enable: 1" http://localhost:8002/  # → X-PHP-Backend: *-php-xdebug:9000
```

## Xdebug configuration

### Environment variables

```bash
DOCKER_XDEBUG_MODE=develop,debug,coverage   # Xdebug modes
DOCKER_XDEBUG_PORT=9003                      # IDE listens on this port
```

### Xdebug modes

| Mode | Purpose |
|---|---|
| `debug` | Step debugging with breakpoints |
| `develop` | Enhanced error messages, var_dump improvements |
| `coverage` | Code coverage for tests |
| `profile` | Performance profiling (generates cachegrind files) |
| `trace` | Function call tracing |

### PHP-FPM on-demand (Xdebug container)

The Xdebug container typically uses `pm = ondemand` to save resources:
- Workers start only when a debug request arrives
- Idle workers terminate after 60s
- Reduces memory usage by ~60-70% when not debugging
- Unlimited request timeout for breakpoint sessions

## IDE setup

### PhpStorm

1. **Debug port**: Settings → PHP → Debug → Port: `9003`
2. **Enable listening**: Click "Start Listening for PHP Debug Connections" (phone icon)
3. **Server config**: Settings → PHP → Servers:
   - Host: `localhost`, Port: `80` (internal container port, not host port)
   - Enable path mappings: local project root → `/var/www/html`
4. **Browser extension**: Install "Xdebug helper", set IDE key to `PHPSTORM`

### VS Code

```json
{
  "name": "Listen for Xdebug",
  "type": "php",
  "request": "launch",
  "port": 9003,
  "pathMappings": {
    "/var/www/html": "${workspaceFolder}"
  }
}
```

## Debugging workflow

1. **Start listening** in IDE (PhpStorm: green phone icon)
2. **Set breakpoints** in code
3. **Send request with debug header** (browser extension, Postman, or curl)
4. **IDE breaks** at breakpoint → inspect variables, step through code
5. **Check `X-PHP-Backend` header** if debugging doesn't trigger

## CLI debugging (Artisan commands, tests)

For debugging Artisan commands or tests, enter the Xdebug container:

```bash
make console-xdebug    # Enter Xdebug container
php artisan your:command   # Xdebug connects to IDE automatically
```

### Verifying CLI fixes

After a fix, verify the command without re-attaching the debugger:

```bash
# Run the command, capture exit code + command output
php artisan your:command; echo "exit code: $?"

# Pest CLI assertion — expectsOutput / artisan test
vendor/bin/pest --filter='ProcessInvoicesCommand'
```

Assert on the **exit code** and **command output**; never trust "looks fine" from breakpoint inspection alone.

## Troubleshooting

| Problem | Solution |
|---|---|
| Breakpoints not hit | Check IDE is listening, verify path mappings, check `X-PHP-Backend` header |
| IDE not connecting | `make console-xdebug` then `nc -zv host.docker.internal 9003` — should show "open" |
| Wrong container used | Check response header `X-PHP-Backend`, verify debug header format (hyphens!) |
| Slow normal requests | Verify normal requests go to fast container (no `X-PHP-Backend: *-xdebug*`) |
| Xdebug logs | `make console-xdebug` then `tail -f /tmp/xdebug.log` |
| Container not running | `docker compose ps` — both PHP containers should be "Up" |
| Path mapping wrong | PhpStorm: Settings → PHP → Servers → verify local ↔ `/var/www/html` |

## Container management

```bash
make console              # Fast PHP container (no Xdebug)
make console-xdebug       # Xdebug container
make rebuild-php-xdebug   # Rebuild Xdebug container only
make rebuild-php-all      # Rebuild both PHP containers
```

### Filter noisy debug output

`tail -f /tmp/xdebug.log` and `docker logs` produce far too much
data to read line-by-line. Filter with `rg`/`grep` for the relevant
event:

```bash
# Only connection / breakpoint events
rg --color=never 'Connect|Step|breakpoint' /tmp/xdebug.log

# Only this request's frames in the laravel log
docker compose logs php-xdebug | rg --color=never "$REQUEST_ID"
```

## What NOT to do

- Do not leave Xdebug enabled in production containers.
- Do not use underscores in debug headers (`XDEBUG_SESSION` fails — use `XDEBUG-SESSION`).
- Do not set PhpStorm server port to the host port (e.g. 8002) — use the internal port (80).
- Do not run performance benchmarks against the Xdebug container.
- Do not forget to check path mappings when breakpoints are silently skipped.


## Output format

1. Xdebug configuration or debugging session setup
2. Root cause identified with evidence from debugger output

## Gotcha

- Xdebug runs in a separate container — don't confuse the fast container (port 80) with the debug container (port 8080).
- The model tends to suggest `dd()` or `var_dump()` — they're forbidden by PHPStan config. Use Xdebug breakpoints.
- Step-debugging over HTTP requires the `XDEBUG_SESSION` cookie/header — without it, breakpoints don't trigger.

## Do NOT

- Do NOT leave breakpoints or debug code in committed files.
- Do NOT use var_dump() or dd() — use Xdebug breakpoints.
- Do NOT debug in the fast container — switch to the Xdebug container.

## Clarification guard — ambiguous repro → ask

If the bug repro is unclear (which request, which user, which env, which input shape?), do not start placing breakpoints at random. Ask the user for the failing payload, the exact route, or the Sentry trace. Setting breakpoints based on a guessed flow wastes a session.

## Auto-trigger keywords

- Xdebug
- PHP debugging
- breakpoint
- step debugging

## Known Laravel bug patterns (from bug-analyzer)

- N+1 queries hidden in loops or accessors
- Missing `->fresh()` after update when using same instance
- Eloquent lazy loading in queued jobs (serialization issues)
- `now()` timezone mismatches
- Missing FK constraints allowing orphaned records
- `DB::transaction()` with external side effects (emails, API calls)
- Model events firing during seeding or migration
- Off-by-one errors in pagination or date ranges
- Silent exception swallowing (`catch (\Exception $e) {}`)
- Floating point comparison for money/quantities
