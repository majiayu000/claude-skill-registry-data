---
name: laravel
description: Laravel PHP web framework. Use when building Laravel apps, Eloquent ORM models, Artisan CLI commands, Blade templates, Livewire/Inertia.js, Sail Docker config, or PHPUnit testing.
---

## laravel

Expressive PHP framework with elegant syntax and batteries-included tooling.

### Core Concepts
- Eloquent ORM: Active Record implementation with fluent query builder, relationships, and mutators
- Artisan CLI: code generation, migrations, queue management, and custom commands via `php artisan`
- Blade templates: lightweight template engine with inheritance, components, and direct PHP support
- Service Container: automatic dependency injection, binding interfaces to implementations

### Common Patterns
- Livewire: full-stack PHP components without writing JavaScript, real-time validation
- Inertia.js: build SPAs using server-side routing and client-side Vue/React
- Middleware pipeline: HTTP request filters for auth, CORS, rate limiting, and sanitization
- Queue/Jobs: async processing with Redis, database, or SQS with retry and failure handling

### Best Practices
- Repository pattern for complex queries, Eloquent for simple CRUD to keep controllers lean
- Form Request validation classes instead of inline validation in controllers
- Sail for Docker development: consistent PHP/MySQL/Redis environment per project
- PHPUnit with feature tests covering HTTP endpoints, database assertions, and mail fakes

### Common Code Patterns
- `Route::resource('posts', PostController::class)` for RESTful resource routing
- `Post::with('comments.user')->where('published', true)->get()` for eager loading
