---
name: php-laravel
description: Laravel 12 best practices, Eloquent patterns, service classes, Form Requests, and PHP 8.x features. Use when working with Laravel projects, controllers, models, migrations, or any PHP backend code.
---

## Purpose

This skill provides Laravel 12+ development patterns, Eloquent optimization techniques, architectural guidelines, and PHP 8.x best practices. It includes automated formatting tools and comprehensive reference documentation for building maintainable Laravel applications.

## When to Use

Invoke this skill when working with:
- Laravel controllers, models, migrations, or any PHP backend code
- Eloquent queries, relationships, or database optimization
- Service layer architecture or repository patterns
- Form Requests, validation, or authorization
- Laravel testing with Pest
- PHP code formatting and style enforcement

## How to Use

### Code Formatting

Use the bundled script to format PHP code with Laravel Pint:

```bash
scripts/linter-formatter.sh --help  # View all options
scripts/linter-formatter.sh         # Format all files
scripts/linter-formatter.sh --dirty # Format only modified files
scripts/linter-formatter.sh --test  # Check style without changes
```

The script automatically detects whether to use Laravel Sail or local Pint installation.

### Reference Documentation

Load reference files as needed to inform implementation decisions:

- `references/architecture-patterns.md` - Service layer and repository patterns
- `references/eloquent-patterns.md` - Query optimization, relationships, scopes
- `references/controller-patterns.md` - Controllers and Form Requests
- `references/testing-patterns.md` - Pest testing with describe/it syntax
- `references/migration-patterns.md` - Migration conventions and best practices
- `references/security-checklist.md` - Security validation checklist

### Workflow

1. Read relevant reference files to understand patterns applicable to the task
2. Apply Laravel 12+ and PHP 8.x features (readonly properties, constructor promotion, etc.)
3. Follow architecture principles: thin controllers (max 10 lines per method), service classes for business logic
4. Use Form Requests for validation with authorization logic in `authorize()` method
5. Optimize Eloquent queries: use `select()` to limit columns, `with()` for eager loading, `lazy()` for large datasets
6. Format code using `scripts/linter-formatter.sh` before completion
7. Validate security requirements using the checklist in `references/security-checklist.md`

### Key Principles

- **Thin Controllers**: Keep controller methods under 10 lines, delegate to services
- **Eager Loading**: Always use `with()` to prevent N+1 query problems
- **Form Requests**: Never validate in controllers; always use FormRequest classes
- **Type Safety**: Use PHP 8.x readonly properties and strict types
- **Query Optimization**: Use `select()`, `withCount()`, and `chunk()`/`lazy()` for performance
- **Security First**: Apply `$fillable`/`$guarded`, policies, and proper input sanitization

### Common Patterns

**Service Class Structure**:
```php
class UserService
{
    public function __construct(
        private readonly UserRepository $users,
        private readonly NotificationService $notifications
    ) {}
}
```

**Optimized Eloquent Query**:
```php
User::select(['id', 'name', 'email'])
    ->with(['posts:id,user_id,title'])
    ->withCount('comments')
    ->lazy();
```

**Form Request**:
```php
class StoreUserRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', User::class);
    }

    public function rules(): array
    {
        return [
            'email' => ['required', 'email', 'unique:users'],
            'password' => ['required', Password::defaults()],
        ];
    }
}
```

For detailed patterns, examples, and edge cases, load the appropriate reference file from `references/`.
