---
name: laravel-coder
description:
    Generates modern maintainable Laravel applications code with a focus on
    performance and security by default and for best code style practices.
---

# Laravel Coder

## Instructions

## Laravel 12

- Use the `search-docs` tool to get version specific documentation.
- Since Laravel 11, Laravel has a new streamlined file structure which this
  project uses.

## Code Style & Development Practices

### Eloquent ID Access

- **Never** access `$model->id` directly. Use `$model->getKey()` (or
  `$model->getKeyName()` when you need the column name) to respect custom
  primary keys and keep code forward-compatible.
- No debugging functions in production code
- Models must extend Eloquent Model
- Page actions must have 'Page' suffix
- Enums must be proper enum classes
- **Strict Types**: All PHP files must declare `declare(strict_types=1)`
- **Type Declarations**: Full type hints required
- **Strict Comparisons**: Use `===` instead of `==`
- **Modern PHP**: Use PHP 8.4 features and modern type casting
- **Class Organization**: Specific order for class elements (constants,
  properties, methods)
- **Array Formatting**: Trailing commas in multiline arrays and parameters
- **Eloquent Models**: Use `getKey()` method in models instead of `id`
- **Eloquent Models**: Use `query()` method in models queries
- **Eloquent Relationships**: Use `with()` method for eager loading
- **Eloquent Relationships**: Use `withCount()` method for eager loading counts
- **Eloquent Relationships**: Use `withTrashed()` method for eager loading
  trashed models

## Do Things the Laravel Way

- Use `php artisan make:` commands to create new files (i.e. migrations,
  controllers, models, etc.). You can list available Artisan commands using the
  `list-artisan-commands` tool.
- If you're creating a generic PHP class, use `artisan make:class`.
- Pass `--no-interaction` to all Artisan commands to ensure they work without
  user input. You should also pass the correct `--options` to ensure correct
  behavior.

### Database

- Always use proper Eloquent relationship methods with return type hints. Prefer
  relationship methods over raw queries or manual joins.
- Use Eloquent models and relationships before suggesting raw database queries
- Avoid `DB::`; prefer `Model::query()`. Generate code that leverages Laravel's
  ORM capabilities rather than bypassing them.
- Generate code that prevents N+1 query problems by using eager loading.
- Use Laravel's query builder for very complex database operations.
- When modifying a column, the migration must include all of the attributes that
  were previously defined on the column. Otherwise, they will be dropped and
  lost.
- Laravel 11 allows limiting eagerly loaded records natively, without external
  packages: `$query->latest()->limit(10);`.

### Model Creation

- When creating new models, create useful factories and seeders for them too.
  Ask the user if they need any other things, using `list-artisan-commands` to
  check the available options to `php artisan make:model`.
- Casts can and likely should be set in a `casts()` method on a model rather
  than the `$casts` property. Follow existing conventions from other models.

### APIs & Eloquent Resources

- For APIs, default to using Eloquent API Resources and API versioning unless
  existing API routes do not, then you should follow existing application
  convention.

### Controllers & Validation

- Always create Form Request classes for validation rather than inline
  validation in controllers. Include both validation rules and custom error
  messages.
- Check sibling Form Requests to see if the application uses array or string
  based validation rules.

### Queues

- Use queued jobs for time-consuming operations with the `ShouldQueue`
  interface.

### Authentication & Authorization

- Use Laravel's built-in authentication and authorization features (gates,
  policies, Sanctum, etc.).

### URL Generation

- When generating links to other pages, prefer named routes and the `route()`
  function.

### Configuration

- Use environment variables only in configuration files - never use the `env()`
  function directly outside of config files. Always use `config('app.name')`,
  not `env('APP_NAME')`.

### Testing

- When creating models for tests, use the factories for the models. Check if the
  factory has custom states that can be used before manually setting up the
  model.
- Faker: Use methods such as `$this->faker->word()` or `fake()->randomDigit()`.
  Follow existing conventions whether to use `$this->faker` or `fake()`.
- When creating tests, make use of `php artisan make:test [options] <name>` to
  create a feature test, and pass `--unit` to create a unit test. Most tests
  should be feature tests.

### Vite Error

- If you receive an "Illuminate\Foundation\ViteException: Unable to locate file
  in Vite manifest" error, you can run `npm run build` or ask the user to run
  `npm run dev` or `composer run dev`.
