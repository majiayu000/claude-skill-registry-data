---
name: docker-expert
description: Swoole-specific Docker patterns and house rules. Covers PHP+Swoole multi-stage builds (pecl and source compile), layer ordering for composer cache, PHP ini and opcache tuning for long-running Swoole processes, PID 1 with tini, graceful shutdown, file-based healthchecks for worker containers, Compose healthcheck-gated depends_on (house pattern), watch mode, profiles, Swoole memory budgeting and fd limits, and Swoole-specific anti-patterns. Does NOT cover general Docker basics, BuildKit features, image optimization, networking, security hardening, logging, debugging, or CI/CD — those are well-covered in training data. Use when writing or reviewing Dockerfiles and Compose files for PHP/Swoole services.
---

# Docker Expert

Reference for Docker patterns specific to the Appwrite/Swoole ecosystem. **Assumes full Docker knowledge** — only house rules, Swoole-specific patterns, and non-obvious gotchas.

Non-negotiable defaults:
- **Multi-stage builds always.** Builder compiles, runtime copies artifacts.
- **BuildKit enabled.** `# syntax=docker/dockerfile:1` at the top of every Dockerfile.
- **Non-root runtime.** Every production container runs as a non-root user.
- **No secrets in image layers.** `--mount=type=secret`, never `ENV`/`COPY` for credentials.
- **Healthchecks on every long-running service.** `depends_on` with `condition: service_healthy`.
- **Pin base image tags.** `php:8.3-cli-bookworm`, never `php:latest`. Use `@sha256:...` in CI.

---

## 1. PHP + Swoole multi-stage builds

### 1.1 Standard pattern (pecl)

```dockerfile
# syntax=docker/dockerfile:1
FROM php:8.3-cli-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev libcurl4-openssl-dev libssl-dev libsqlite3-dev zlib1g-dev \
    && docker-php-ext-install -j$(nproc) pdo_mysql pdo_pgsql pdo_sqlite sockets \
    && pecl install swoole \
    && docker-php-ext-enable swoole \
    && rm -rf /var/lib/apt/lists/*

FROM php:8.3-cli-bookworm AS runtime
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libsqlite3.so* /usr/lib/x86_64-linux-gnu/
COPY --chown=appwrite:appwrite . /app
WORKDIR /app
USER appwrite
ENTRYPOINT ["php", "server.php"]
```

- Copy the extensions **directory**, not individual `.so` files -- survives version bumps.
- Copy shared lib `.so*` glob -- catches symlinks (`libpq.so.5 -> libpq.so.5.17`).
- `--chown` on COPY -- avoids a separate `chown` layer.

### 1.2 Source compile (when custom flags needed)

```dockerfile
ARG SWOOLE_VERSION=6.0.0
RUN apt-get update && apt-get install -y --no-install-recommends \
        libcurl4-openssl-dev libssl-dev libpq-dev libsqlite3-dev liburing-dev \
    && cd /tmp \
    && curl -fSL "https://github.com/swoole/swoole-src/archive/v${SWOOLE_VERSION}.tar.gz" | tar xz \
    && cd "swoole-src-${SWOOLE_VERSION}" \
    && phpize && ./configure \
        --enable-openssl --enable-swoole-curl --enable-swoole-pgsql \
        --enable-swoole-sqlite --enable-sockets \
    && make -j$(nproc) && make install \
    && docker-php-ext-enable swoole
```

Use `pecl install swoole` for standard builds. Source compile only for `--enable-swoole-curl`, `--enable-iouring`, etc.

### 1.3 Layer ordering for cache efficiency

```dockerfile
# Order: base packages (monthly) -> extensions (monthly) -> deps (weekly) -> code (every commit)
COPY composer.json composer.lock ./
RUN --mount=type=cache,target=/root/.composer/cache \
    composer install --no-dev --prefer-dist --no-scripts --no-autoloader
COPY . .
RUN composer dump-autoload --optimize --classmap-authoritative
```

---

## 2. PHP ini and opcache for Swoole containers

```ini
; appwrite.ini -- long-running process settings
max_execution_time = 0          ; Swoole workers run indefinitely
memory_limit = 512M             ; per worker, not per request (worker_num * limit <= container memory)
max_input_time = -1             ; Swoole manages lifecycle
post_max_size = 128M
upload_max_filesize = 128M
display_errors = Off
log_errors = On
error_reporting = E_ALL
error_log = /dev/stderr
```

```ini
; opcache.ini -- CRITICAL settings for Swoole
opcache.enable = 1
opcache.enable_cli = 1
opcache.validate_timestamps = 0         ; files don't change at runtime; reload workers for updates
opcache.preload = /app/preload.php      ; hot classes shared across workers
opcache.preload_user = appwrite
opcache.memory_consumption = 256
opcache.interned_strings_buffer = 32
opcache.max_accelerated_files = 30000
opcache.jit = 1255                      ; profile-guided for Swoole hot paths
opcache.jit_buffer_size = 128M
```

For development: `validate_timestamps=1` or file watch + `$server->reload()`.

---

## 3. Signal handling, PID 1, and healthchecks

### PID 1 + tini

PID 1 in a container: no default signal handlers (SIGTERM ignored), must reap zombie children.

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends tini
ENTRYPOINT ["tini", "--"]
CMD ["php", "server.php"]
```

Or Compose `init: true`. Swoole signal handlers (`Process::signal(SIGTERM, ...)`) work but don't reap zombies.

### Graceful shutdown

```yaml
services:
  app:
    stop_grace_period: 30s  # must be >= swoole max_wait_time; SIGKILL after expiry
```

Sequence: SIGTERM -> tini forwards -> Swoole master signals workers -> workers drain -> exit.

### Healthchecks

```dockerfile
# HTTP server -- TCP or curl
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8080/health || exit 1
```

```php
// Worker/queue containers (no port) -- file-based heartbeat
file_put_contents('/tmp/heartbeat', (string) time());  // in worker loop
```

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD php -r "exit(time() - (int)file_get_contents('/tmp/heartbeat') > 60 ? 1 : 0);"
```

---

## 4. Compose orchestration (house patterns)

### 4.1 Healthcheck-gated dependencies

```yaml
services:
  mariadb:
    image: mariadb:11
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    volumes:
      - mariadb-data:/var/lib/mysql

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 3

  app:
    build: .
    depends_on:
      mariadb:
        condition: service_healthy   # NEVER bare depends_on -- waits for start, not ready
      redis:
        condition: service_healthy
```

### 4.2 Watch mode and profiles

```yaml
services:
  app:
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: ./composer.lock
        - action: sync+restart
          path: ./config
          target: /app/config

  maildev:
    image: maildev/maildev
    profiles: ["dev"]
  prometheus:
    image: prom/prometheus
    profiles: ["monitoring"]
```

```bash
docker compose watch          # or: docker compose up --watch
docker compose --profile dev up
```

---

## 5. Resource limits for Swoole

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: "2.0"
        reservations:
          memory: 512M
          cpus: "1.0"
    ulimits:
      nofile:
        soft: 65535       # Swoole needs high fd limit for concurrent connections
        hard: 65535       # default 1024 is far too low
```

**Memory budget**: `worker_num * memory_limit + master overhead + buffer`. 4 workers * 512M + 200M = ~2.3G limit.

**Logging**: `ENV SWOOLE_LOG_FILE=/dev/stderr` -- never write logs to container filesystem.

**Alpine caveat**: DNS `ndots:5` in k8s causes 5x queries -- set `ndots:1`.

---

## 6. Anti-patterns (Swoole-specific and non-obvious)

| About to write | Write instead | Why |
|---|---|---|
| `COPY . .` before `RUN composer install` | `COPY composer.json composer.lock ./` first | Code changes bust dependency cache |
| `depends_on: [mariadb]` (bare) | `depends_on: { mariadb: { condition: service_healthy } }` | Started != ready; race condition |
| No resource limits | `deploy.resources.limits` | OOM container takes down host |
| `restart: always` without healthcheck | `restart: unless-stopped` + healthcheck | Crash loop burns CPU undetected |
| `volumes: [./vendor:/app/vendor]` | Named volume or don't mount | Wrong platform binaries; defeats caching |
| `json-file` without rotation | Always set `max-size` and `max-file` | Default has NO rotation -- disk fills |
| `version: "3.8"` at top | Omit entirely | Deprecated since Compose v2; ignored |
| Default ulimits for Swoole | `nofile: 65535` | Default 1024 starves fd-heavy Swoole |
| `memory_limit=-1` in Swoole container | Explicit per-worker limit | One leak takes down entire container |
| `opcache.validate_timestamps=1` in prod | `validate_timestamps=0` + worker reload | Stat calls on every request in long-running process |
