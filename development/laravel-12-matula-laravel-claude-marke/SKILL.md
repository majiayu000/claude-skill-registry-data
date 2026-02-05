---
name: laravel-12
description: Expert guidance for building Laravel 12 applications following best practices, modern conventions, and the streamlined Laravel 12 architecture. Use this skill when creating Laravel projects, working with Eloquent models, building APIs, implementing authentication, writing tests, or any Laravel development task.
---

# Laravel 12 Development Skill

This skill provides comprehensive guidance for developing high-quality Laravel 12 applications using modern best practices, proper architecture patterns, and Laravel's streamlined structure.

## Purpose

Provide expert-level Laravel 12 development guidance covering:
- Modern Laravel 12 streamlined architecture and file structure
- Eloquent ORM patterns with proper type hints and relationships
- Authentication and authorization using current best practices
- Form validation with Form Request classes
- Queue and job management for background processing
- Database migrations, models, and API development
- Testing patterns and conventions
- Configuration and environment management

## When to Use

Use this skill when:
- Creating or working with Laravel 12 applications
- Building models, controllers, migrations, or any Laravel components
- Implementing authentication or authorization
- Creating APIs with Eloquent resources
- Writing database queries or working with relationships
- Setting up queues and background jobs
- Writing form validation
- Configuring Laravel applications
- Following Laravel best practices and conventions
- Ensuring proper Laravel 12 structure compliance

## Core Principles

### 1. Use Artisan Commands

Always create files using `php artisan make:` commands with appropriate options:

```bash
# Models with migrations, factories, seeders
php artisan make:model Post -mfs

# Form Requests for validation
php artisan make:request StorePostRequest

# Controllers
php artisan make:controller PostController --resource

# Jobs
php artisan make:job ProcessPodcast

# Generic PHP classes
php artisan make:class Services/PaymentService
```

**Important**: Pass `--no-interaction` when running commands programmatically.

### 2. Follow Laravel 12 Streamlined Structure

Laravel 12 uses a simplified structure:
- **No `app/Http/Middleware/`** directory - register middleware in `bootstrap/app.php`
- **No `app/Console/Kernel.php`** - use `bootstrap/app.php` or `routes/console.php`
- **Commands auto-register** from `app/Console/Commands/`
- Central configuration in `bootstrap/app.php` for middleware, routing, exceptions

Read `references/structure.md` for complete details on Laravel 12 architecture.

### 3. Authentication: Always Use $request->user()

**CRITICAL**: Always retrieve authenticated user via `$request->user()`, never use `auth()->user()` or `Auth::user()`:

```php
// ✅ CORRECT
public function index(Request $request): Response
{
    $user = $request->user();
    // ...
}

// ❌ WRONG
public function index(): Response
{
    $user = auth()->user();  // Don't do this
}
```

Read `references/authentication.md` for complete authentication and authorization guidance.

### 4. Database: Eloquent Over DB Facade

Prefer Eloquent models and relationships over raw queries:

```php
// ✅ PREFER
$users = User::query()->where('active', true)->get();

// ❌ AVOID
$users = DB::table('users')->where('active', true)->get();
```

**Prevent N+1 queries** by eager loading relationships:

```php
// ✅ GOOD - Prevents N+1
$posts = Post::with('user', 'comments')->get();

// ❌ BAD - Causes N+1
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // New query each iteration
}
```

Read `references/database.md` for Eloquent patterns, relationships, migrations, and query optimization.

### 5. Validation: Always Use Form Requests

Never use inline validation. Always create Form Request classes:

```bash
php artisan make:request StorePostRequest
```

Form Requests should include:
- Validation rules (check project conventions for array vs string format)
- Custom error messages
- Authorization logic when needed

```php
public function rules(): array
{
    return [
        'title' => ['required', 'string', 'max:255'],
        'body' => ['required', 'string'],
    ];
}
```

Read `references/validation.md` for complete validation patterns and examples.

### 6. Configuration: Never Use env() Outside Config Files

```php
// ❌ WRONG
$apiKey = env('API_KEY');

// ✅ CORRECT
$apiKey = config('services.api.key');
```

Environment variables should only be accessed in `config/*.php` files, then accessed via `config()` helper throughout the application.

### 7. Background Processing: Use Queues

Use queued jobs with `ShouldQueue` interface for time-consuming operations:

```bash
php artisan make:job ProcessPodcast
```

```php
class ProcessPodcast implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;
    
    public int $tries = 3;
    public int $timeout = 120;
    
    public function __construct(public Podcast $podcast) {}
    
    public function handle(): void
    {
        $this->podcast->process();
    }
}
```

Read `references/queues.md` for queue patterns, job chains, batches, and worker management.

## Working with Models

### Model Creation

When creating models, use appropriate flags:

```bash
# Model with migration, factory, seeder
php artisan make:model Post -mfs

# Model with migration, factory, seeder, policy, controller
php artisan make:model Post -mfsc --policy
```

### Model Conventions

1. **Use return type hints** on relationships:
```php
public function posts(): HasMany
{
    return $this->hasMany(Post::class);
}
```

2. **Use `casts()` method** for type casting:
```php
protected function casts(): array
{
    return [
        'published_at' => 'datetime',
        'is_featured' => 'boolean',
        'metadata' => 'array',
    ];
}
```

3. **Use constructor property promotion**:
```php
public function __construct(
    public string $name,
    public int $age,
) {}
```

## Working with Controllers

1. **Type-hint Request** in controller methods
2. **Use resource controllers** for CRUD operations
3. **Return proper response types** with type hints
4. **Use Form Requests** for validation
5. **Keep controllers thin** - move business logic to services/actions

```php
public function store(StorePostRequest $request): RedirectResponse
{
    $post = Post::create($request->validated());
    
    return redirect()->route('posts.show', $post);
}
```

## API Development

Use Eloquent API Resources for consistent API responses:

```bash
php artisan make:resource PostResource
```

```php
class PostResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'author' => new UserResource($this->whenLoaded('user')),
        ];
    }
}
```

## Migrations

**CRITICAL**: When modifying columns, include ALL previous attributes or they will be lost:

```php
// ❌ WRONG - Loses 'nullable' attribute
$table->string('email')->unique()->change();

// ✅ CORRECT - Preserves all attributes
$table->string('email')->nullable()->unique()->change();
```

## Reference Files

This skill includes detailed reference files for specific topics:

- **`references/structure.md`** - Laravel 12 file structure, Artisan commands, configuration
- **`references/authentication.md`** - Authentication, authorization, policies, gates
- **`references/database.md`** - Eloquent, relationships, migrations, queries, API resources
- **`references/validation.md`** - Form Requests, validation rules, custom messages
- **`references/queues.md`** - Jobs, queues, workers, chains, batches

Read the appropriate reference file(s) when working on related tasks to ensure following best practices.

## PHP Conventions

1. **Always use curly braces** for control structures, even single-line
2. **Use explicit return type declarations** for all methods
3. **Use PHP 8+ constructor property promotion**
4. **Use type hints** for method parameters
5. **Prefer PHPDoc blocks** over inline comments

```php
protected function isAccessible(User $user, ?string $path = null): bool
{
    // Implementation
}
```

## Best Practices Summary

1. ✅ Use `php artisan make:` commands to create files
2. ✅ Follow Laravel 12 streamlined structure
3. ✅ Always use `$request->user()` for authentication
4. ✅ Prefer Eloquent over DB facade
5. ✅ Always create Form Request classes for validation
6. ✅ Never use `env()` outside config files
7. ✅ Use queues for time-consuming operations
8. ✅ Add return type hints on relationships
9. ✅ Eager load to prevent N+1 queries
10. ✅ Include all attributes when modifying columns
11. ✅ Use named routes with `route()` helper
12. ✅ Use API Resources for APIs
13. ✅ Keep controllers thin
14. ✅ Write descriptive, type-safe code

## Common Tasks Workflow

### Creating a New Resource

1. Create model with migrations and factory: `php artisan make:model Post -mf`
2. Create Form Requests: `php artisan make:request StorePostRequest`
3. Create controller: `php artisan make:controller PostController --resource`
4. Create API resource (if needed): `php artisan make:resource PostResource`
5. Define routes in appropriate routes file with named routes
6. Write tests for all functionality

### Adding Authentication to Routes

1. Use middleware in route definition or `bootstrap/app.php`
2. Access user via `$request->user()`
3. Use policies for authorization
4. Return appropriate responses for unauthorized access

This skill ensures Laravel applications follow modern best practices, maintain clean architecture, and leverage Laravel 12's streamlined structure effectively.
