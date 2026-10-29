---
name: docker-patterns
description: "Use when writing or reviewing Docker and docker-compose setups for a Laravel application — multi-stage PHP-FPM images, services (nginx, MySQL, Redis, queue worker, scheduler, Vite build), healthchecks, secrets, and image hardening."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/security/backend.md` — never bake secrets into image layers, inject them at runtime; apply least privilege (non-root user, dropped capabilities, least-privileged DB user).
- Apply `@rules/laravel/laravel.md` — respect Laravel's directory layout, artisan commands, and config caching.
- Pin every base image to a specific tag (never `:latest`) for reproducible builds.
- One process per container: PHP-FPM, queue worker, and scheduler are separate containers sharing the same image.
- `.env` and secrets stay out of images and out of git.

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `build`):

- **`build` (default)** — full container work: write and edit `Dockerfile`s and compose files, add services, healthchecks, and volumes, and change how a secret reaches the build. Every section below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by `@skills/code-review/SKILL.md`, `code-review-github`, `code-review-jira`, and `code-review-bugsnag` when the diff touches a container build or runtime surface)** — **never modify a `Dockerfile`, a compose file, or any other project file, never author a test, never stage / commit / push, never run fixers or checkers, and never chain a follow-up review.** Scope the analysis to the lines added or modified by the PR diff and return the findings as markdown only, carrying the reproducer fields the CR folds into its standard Critical / Moderate buckets.
Every instruction below that would touch a file or an image — add, pin, split, drop, mount, configure, or any other such verb — is emitted as a written proposal carrying a concrete Dockerfile or compose snippet, never applied to the project.

> **What this lens owns in a CR:** the shape of the image and its services — stage layout and layer caching, pinned base image tags, the non-root user and dropped capabilities, healthchecks, one process per container, and how a secret is delivered to the build — a runtime injection or a BuildKit `--mount=type=secret` against an `ENV` / `COPY` that persists in a layer. It **defers the fetch, the transport trust, and the concealment on a line** — a silent remote fetch, disabled TLS validation, suppressed error output, and the hidden-file-plus-detached-process pattern — to the walk *Malicious Code & Supply-Chain Indicators* (`@rules/security/backend.md`), and never raises a finding that walk owns.
> A **hardcoded** secret — a credential, key, or token written literally into a `Dockerfile`, a compose file, or an env file copied into an image — is not the lens's either: `@rules/security/backend.md` *General Secure Coding Practices* and `@skills/security-review/SKILL.md` own it, and a security finding is never moved out of a security owner.
> The lens runs whatever stack the project has. **Never raise a finding whose only fix is to adopt a service the project does not run** — a queue worker, a scheduler, a Redis container, or a Vite build stage: the service list is a project decision, not a defect on the diff.

## Use when
- Writing or reviewing a `Dockerfile` / `docker-compose.yml` for a Laravel app.
- Setting up local dev (nginx + PHP-FPM + MySQL + Redis) or a build pipeline for a production image.
- Reviewing image size, layer caching, healthchecks, or secret handling.

## Multi-Stage Dockerfile (PHP-FPM)

Separate Composer deps, the Vite/asset build, and the lean runtime so each layer caches independently and dev tooling never ships to production.

```dockerfile
# syntax=docker/dockerfile:1

# --- Stage: composer deps (cached unless composer.* change) ---
FROM composer:2 AS vendor
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --prefer-dist \
    --optimize-autoloader --no-interaction

# --- Stage: node/vite asset build ---
FROM node:22-alpine AS assets
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY vite.config.js ./
COPY resources ./resources
RUN npm run build              # emits public/build via laravel-vite-plugin

# --- Stage: runtime (php-fpm, non-root, opcache) ---
FROM php:8.4-fpm-alpine AS runtime   # match composer.json require.php
RUN apk add --no-cache fcgi \
    && docker-php-ext-install pdo_mysql opcache bcmath pcntl \
    && addgroup -g 1000 -S app && adduser -S app -u 1000 -G app
COPY docker/php/opcache.ini /usr/local/etc/php/conf.d/opcache.ini
WORKDIR /var/www/html
COPY --chown=app:app . .
COPY --from=vendor --chown=app:app /app/vendor ./vendor
COPY --from=assets --chown=app:app /app/public/build ./public/build
USER app
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
    CMD php-fpm-healthcheck || exit 1
EXPOSE 9000
CMD ["php-fpm"]
```

Key points:
- `--no-dev --optimize-autoloader` strips dev packages and builds a classmap autoloader — smaller image, faster boot.
- `--no-scripts` during build avoids running artisan before the full app is copied; run cache-warming at deploy/entrypoint instead.
- Production `opcache.ini`: `opcache.enable=1`, `opcache.validate_timestamps=0` (no per-request stat — invalidate by redeploying), tuned `memory_consumption` / `max_accelerated_files`.
- Run as the non-root `app` user; the alpine base keeps the image small.

## opcache.ini (production)

```ini
opcache.enable=1
opcache.memory_consumption=256
opcache.max_accelerated_files=20000
opcache.validate_timestamps=0
opcache.preload=/var/www/html/preload.php
opcache.preload_user=app
```

## docker-compose (local dev)

```yaml
services:
  app:                                   # PHP-FPM
    build: { context: ., target: runtime }
    volumes:
      - .:/var/www/html                  # bind mount for hot reload
      - /var/www/html/vendor             # protect image vendor from host
    env_file: [.env]
    depends_on:
      mysql: { condition: service_healthy }
      redis: { condition: service_started }

  nginx:
    image: nginx:1.27-alpine
    ports: ["8080:80"]
    volumes:
      - .:/var/www/html
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on: [app]

  mysql:
    image: mysql:8.4
    environment:
      MYSQL_DATABASE: app
      MYSQL_USER: app
      MYSQL_PASSWORD: ${DB_PASSWORD}     # from host/.env, never inline
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    ports: ["127.0.0.1:3306:3306"]       # host-only; omit entirely in prod
    volumes: [mysqldata:/var/lib/mysql]
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10

  redis:
    image: redis:7-alpine
    command: ["redis-server", "--maxmemory-policy", "allkeys-lru"]
    volumes: [redisdata:/data]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  queue:                                 # worker — same image, different command
    build: { context: ., target: runtime }
    command: ["php", "artisan", "queue:work", "redis", "--tries=3", "--max-time=3600"]
    env_file: [.env]
    restart: unless-stopped
    depends_on:
      redis: { condition: service_started }
      mysql: { condition: service_healthy }

  scheduler:                             # one container running the scheduler loop
    build: { context: ., target: runtime }
    command: ["php", "artisan", "schedule:work"]
    env_file: [.env]
    restart: unless-stopped
    depends_on:
      mysql: { condition: service_healthy }

volumes:
  mysqldata:
  redisdata:
```

- Services resolve each other by name on the Compose network: `DB_HOST=mysql`, `REDIS_HOST=redis`.
- `schedule:work` runs the scheduler in-container (replaces a host crontab); the queue worker is its own restartable container so it scales independently of web.
- For the Vite dev server (HMR) add `npm run dev` in a node service exposing port 5173, instead of the build stage.

## Healthchecks

- PHP-FPM: ship `php-fpm-healthcheck` (or a small FastCGI ping) — a plain TCP check won't catch a wedged pool.
- Gate dependents with `depends_on: { condition: service_healthy }` so the app doesn't boot before MySQL accepts connections.
- Queue/scheduler containers: `restart: unless-stopped` so a transient crash self-recovers.

## Secrets

- Inject at runtime via `env_file` / `environment` / orchestrator secrets — never `ENV SECRET=...` or `COPY .env` into a layer (layers are inspectable forever; see `@rules/security/backend.md`).
- Use `--mount=type=secret` for build-time-only secrets (private Composer repo token) so they never persist in the final image.
- Give the app a least-privileged MySQL user (no `GRANT ALL`); reserve root for migrations/admin only.

## .dockerignore

```
vendor
node_modules
.env
.env.*
.git
storage/logs/*
storage/framework/cache/*
public/build
docker-compose*.yml
*.md
tests
```

Excluding `vendor`/`node_modules` shrinks build context and forces deps to come from the cached `composer`/`npm ci` layers, not stale host copies.

## Image Size & Layer Caching

- Copy `composer.json composer.lock` (and `package*.json`) **before** the app source so dependency layers cache across code changes.
- Use `-alpine` bases; install with `--no-cache` (apk) / clean apt lists in the same `RUN`.
- Chain related `RUN` commands with `&&` to avoid extra layers; multi-stage keeps build tools out of the runtime image.
- Add `--mount=type=cache` (BuildKit) for the Composer/npm cache to speed rebuilds without bloating the image.

## Anti-Patterns

- `:latest` tags — non-reproducible builds. Pin versions.
- Running as root — always create and `USER` a non-root user.
- Secrets in `docker-compose.yml` or image layers — use env/secrets.
- One container running web + queue + scheduler — split them; one process per container.
- No volumes for MySQL/Redis — data lost on `down`. Use named volumes.
- Plain Compose as the production orchestrator for scale — fine for a single host; use Swarm/Kubernetes/ECS beyond that.

## Done when
- Final image runs as non-root, ships `--no-dev` optimized autoload + opcache, and contains no secrets or dev tooling.
- Web, queue worker, and scheduler are separate containers sharing one image.
- MySQL and Redis have healthchecks and named volumes; dependents wait on `service_healthy`.
- Secrets come from env/secrets at runtime; `.dockerignore` excludes `vendor`, `node_modules`, `.env`, `.git`.
- Dependency layers are copied before source so the layer cache holds across code changes.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
