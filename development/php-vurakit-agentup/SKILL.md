---
name: php-pro-max
description: "PHP development intelligence. 12 domains, 8 stacks, 300+ entries. Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check PHP code. Domains: pattern, package, error, perf, test, security, interface, arch, idiom, anti, tooling, dependency. Stacks: laravel, symfony, codeigniter, slim, api-platform, livewire, database, queue. Integrations: arch_system generator."
---

# PHP Pro Max - Backend Generator

## When User Requests PHP Work

Follow this workflow for every PHP-related task:

### 1. Analyze Requirements

Extract from the user's request:

- **Project type**: REST API, web app, microservice, CMS, e-commerce, CLI
- **Domain**: web, database, queue, messaging, real-time
- **Constraints**: specific framework? PHP version? Docker? cloud?
- **Scale**: small project, enterprise, SaaS

### Default Stack (always use unless user specifies otherwise)

| Component     | Default        | Package                             |
| ------------- | -------------- | ----------------------------------- |
| **Framework** | **Laravel 11** | `laravel/laravel`                   |
| **Database**  | **MySQL 8**    | `illuminate/database` (Eloquent)    |
| **Auth**      | JWT            | `tymon/jwt-auth` or Laravel Sanctum |
| **Cache**     | Redis          | `predis/predis`                     |
| **Queue**     | Redis/Database | Laravel Queue                       |
| **Config**    | ENV vars       | `.env` + `config/*.php`             |
| **Deploy**    | Docker Compose | `Dockerfile` + `docker-compose.yml` |

**Project structure**: Laravel standard layout:

```
app/Http/Controllers/    — HTTP controllers
app/Http/Middleware/      — request middleware
app/Http/Requests/        — form request validation
app/Models/               — Eloquent models
app/Services/             — business logic
app/Repositories/         — data access layer
app/Exceptions/           — custom exceptions
config/                   — configuration files
database/migrations/      — database migrations
database/seeders/         — database seeders
routes/api.php            — API routes
routes/web.php            — web routes
resources/views/          — Blade templates
tests/Unit/               — unit tests
tests/Feature/            — feature tests
```

### 2. Generate Architecture System (REQUIRED for new projects)

```bash
python3 skills/php/scripts/search.py "<project description>" --arch-system -p "ProjectName"
```

This gives you: architecture, packages, error strategy, patterns, structure, testing approach.

### 3. Supplement with Domain Searches

Based on the project needs, search relevant domains:

```bash
# Patterns for the task
python3 skills/php/scripts/search.py "repository service pattern" --domain pattern

# Error handling approach
python3 skills/php/scripts/search.py "custom exception handler" --domain error

# Security patterns
python3 skills/php/scripts/search.py "sql injection xss prevention" --domain security

# Performance tips
python3 skills/php/scripts/search.py "opcache query optimization" --domain perf

# Testing patterns
python3 skills/php/scripts/search.py "phpunit mocking feature test" --domain test
```

### 4. Stack Guidelines

If using a specific framework/stack:

```bash
python3 skills/php/scripts/search.py "middleware authentication" --stack laravel
python3 skills/php/scripts/search.py "doctrine entity mapping" --stack symfony
python3 skills/php/scripts/search.py "route middleware" --stack slim
```

### 5. Implement

Apply all recommendations from the search results:

- Use recommended architecture and project structure
- Apply patterns (Repository, Service Layer, DTO, etc.)
- Follow error handling strategy
- Implement security best practices
- Add tests following testing strategy

### 6. Always Generate Docker Files

Every project MUST include these files:

**Dockerfile** (multi-stage build):

```dockerfile
FROM composer:2 AS vendor
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-autoloader

FROM php:8.3-fpm-alpine AS app
RUN apk add --no-cache \
    libpng-dev libjpeg-turbo-dev freetype-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo pdo_mysql opcache bcmath
WORKDIR /var/www
COPY --from=vendor /app/vendor vendor
COPY . .
RUN composer dump-autoload --optimize
RUN chown -R www-data:www-data storage bootstrap/cache
EXPOSE 9000
CMD ["php-fpm"]
```

**docker-compose.yml** (App + MySQL + Nginx + Redis):

```yaml
services:
  app:
    build: .
    volumes:
      - .:/var/www
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    environment:
      - DB_CONNECTION=mysql
      - DB_HOST=db
      - DB_PORT=3306
      - DB_DATABASE=appdb
      - DB_USERNAME=root
      - DB_PASSWORD=secret
      - REDIS_HOST=redis
  nginx:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/conf.d/default.conf
      - .:/var/www
    depends_on:
      - app
  db:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      MYSQL_DATABASE: appdb
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - dbdata:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 5
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
volumes:
  dbdata:
```

**Makefile** (must include):

```makefile
serve:
	php artisan serve
test:
	php artisan test --parallel
lint:
	./vendor/bin/phpstan analyse --memory-limit=512M
format:
	./vendor/bin/pint
docker-up:
	docker-compose up -d --build
docker-down:
	docker-compose down
migrate:
	php artisan migrate
seed:
	php artisan db:seed
```

## Pre-Delivery Checklist

Before delivering PHP code, verify:

- [ ] `./vendor/bin/phpstan analyse` passes (level 6+)
- [ ] `./vendor/bin/pint` or `php-cs-fixer` passes
- [ ] `php artisan test` or `./vendor/bin/phpunit` passes
- [ ] No raw SQL queries (use Eloquent/Query Builder or prepared statements)
- [ ] All user input validated (Form Requests or manual validation)
- [ ] CSRF protection enabled on web routes
- [ ] Passwords hashed with `bcrypt` or `argon2`
- [ ] No sensitive data in error responses (production mode)
- [ ] Mass assignment protection (`$fillable` or `$guarded`)
- [ ] Database migrations are reversible
- [ ] Environment variables used for secrets (not hardcoded)
- [ ] Rate limiting on auth/API endpoints
- [ ] Proper exception handling (custom exceptions per domain)
- [ ] Type hints and return types on all methods
- [ ] PSR-12 coding standard followed

## Quick Domain Reference

| Domain       | When to Search                                                        |
| ------------ | --------------------------------------------------------------------- |
| `pattern`    | Need a design pattern (repository, service, factory, DTO, middleware) |
| `package`    | Choosing a Composer package for a use case                            |
| `error`      | Exception handling strategy, custom exceptions, error responses       |
| `perf`       | Performance optimization, OPcache, caching, N+1 queries               |
| `test`       | Testing approach, PHPUnit, Pest, mocking, feature tests               |
| `security`   | SQL injection, XSS, CSRF, auth, input validation                      |
| `interface`  | Interface design, SOLID, traits, type hints, OOP                      |
| `arch`       | Project structure, architecture decisions                             |
| `idiom`      | PHP conventions, PSR standards, modern PHP features                   |
| `anti`       | Avoiding common mistakes                                              |
| `tooling`    | PHP tools, static analysis, formatting, debugging                     |
| `dependency` | Composer, autoloading, versioning, packages                           |

## Resources

- **scripts/**: BM25 search engine, architecture system generator
- **data/**: 12 domains and 8 stacks with 300+ curated PHP entries
