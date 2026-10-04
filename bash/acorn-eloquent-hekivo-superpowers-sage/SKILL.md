---
name: superpowers-sage:acorn-eloquent
description: >
  Eloquent, model, migration, relationship, hasMany, belongsTo, belongsToMany,
  Acorn Eloquent, custom table, wp_posts, wp_users, wp_postmeta, factory,
  query scope, scopePublished, global scope, make:model, make:migration,
  lando acorn migrate, $fillable, $casts, $timestamps, $primaryKey, HasFactory,
  db:seed, seeder — Eloquent ORM for custom and WordPress tables via Acorn
user-invocable: false
---

# Eloquent ORM in WordPress via Acorn

## When to Use Eloquent vs WordPress Functions

| Use case | Use Eloquent | Use WordPress functions |
|---|---|---|
| Custom tables (event logs, testimonials, form entries) | Yes | No |
| Complex joins across custom tables | Yes | No |
| Relationships between custom models | Yes | No |
| Post types, taxonomies, menus | No | Yes (`WP_Query`, `get_posts`) |
| User management, roles, capabilities | No | Yes (`wp_insert_user`, `get_userdata`) |
| Options, transients | No | Yes (`get_option`, `get_transient`) |
| Complex read queries on `wp_posts` | Read-only, carefully | Prefer `WP_Query` first |

**Rule:** WordPress-managed content goes through WordPress functions so hooks fire. Custom application data goes through Eloquent.

## Quick Start — Scripts

```bash
# Create a model (PascalCase name required)
bash skills/acorn-eloquent/scripts/create-model.sh Testimonial

# Create a model with a migration
bash skills/acorn-eloquent/scripts/create-model.sh EventLog --migration

# Run pending migrations
bash skills/acorn-eloquent/scripts/run-migration.sh

# Run with additional flags (passed through to lando acorn migrate)
bash skills/acorn-eloquent/scripts/run-migration.sh --seed
bash skills/acorn-eloquent/scripts/run-migration.sh --step=2
```

Scripts: [`scripts/create-model.sh`](scripts/create-model.sh) · [`scripts/run-migration.sh`](scripts/run-migration.sh)

## Models

Models live in `app/Models/`. Always declare `$table` explicitly with the WordPress prefix.

```php
class Testimonial extends Model
{
    use HasFactory;

    protected $table = 'wp_testimonials';

    protected $fillable = ['author_name', 'company', 'body', 'rating', 'is_featured', 'published_at'];

    protected $casts = [
        'rating'       => 'integer',
        'is_featured'  => 'boolean',
        'published_at' => 'datetime',
        'metadata'     => 'array',
    ];
}
```

See [`references/models.md`](references/models.md) for:
- Full property reference (`$primaryKey`, `$keyType`, `$incrementing`)
- Custom table example
- WP core table mirror example with read-only guard
- Accessors/mutators with `Attribute::make()`

## Assets

Boilerplate templates with `{{PLACEHOLDER}}` tokens:

- **[model-custom-table.php.tpl](assets/model-custom-table.php.tpl)** — Custom table model with `$table`, `$primaryKey`, `$timestamps`, `$fillable`, `$casts`. Replace `{{CLASS_NAME}}`, `{{TABLE_NAME}}`.
- **[model-wp-mirror.php.tpl](assets/model-wp-mirror.php.tpl)** — Read-only WP core table mirror with `$primaryKey = 'ID'`, `$timestamps = false`, write guards. Replace `{{CLASS_NAME}}`, `{{WP_TABLE}}`.

## Migrations

```bash
lando acorn make:migration create_testimonials_table
lando acorn migrate
lando acorn migrate:status
lando acorn migrate:rollback
```

```php
return new class extends Migration
{
    public function up(): void
    {
        Schema::create('wp_testimonials', function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger('user_id')->nullable();
            $table->string('author_name');
            $table->text('body');
            $table->unsignedTinyInteger('rating')->default(5);
            $table->boolean('is_featured')->default(false);
            $table->timestamp('published_at')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('wp_testimonials');
    }
};
```

See [`references/migrations.md`](references/migrations.md) for:
- Column types reference table
- Adding columns to existing tables
- Full migration commands reference
- Naming conventions

## Relationships

```php
class Testimonial extends Model
{
    public function author(): BelongsTo
    {
        return $this->belongsTo(User::class, 'user_id');
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class, 'wp_testimonial_tag', 'testimonial_id', 'tag_id');
    }
}
```

Eager load to avoid N+1:

```php
Testimonial::with('author', 'tags')->get();
```

See [`references/relationships.md`](references/relationships.md) for:
- `wp_posts` → `wp_postmeta` (`hasMany` with `ID` key)
- `wp_terms` → `wp_termmeta`
- Wrapping `wp_users` for read-only relationships
- Polymorphic relationships (event logs)

## Query Scopes

```php
public function scopePublished(Builder $query): void
{
    $query->whereNotNull('published_at')
          ->where('published_at', '<=', now());
}

public function scopeMinRating(Builder $query, int $rating): void
{
    $query->where('rating', '>=', $rating);
}
```

Chain fluently:

```php
Testimonial::published()->featured()->minRating(4)->with('author')->get();
```

See [`references/query-scopes.md`](references/query-scopes.md) for:
- Global scopes with `booted()` registration
- `withoutGlobalScope()` usage
- Conditional scopes with `->when()`
- Raw queries with safe binding

## Factories

```bash
lando acorn make:factory TestimonialFactory
```

```php
class TestimonialFactory extends Factory
{
    protected $model = Testimonial::class;

    public function definition(): array
    {
        return [
            'author_name'  => fake()->name(),
            'body'         => fake()->paragraphs(2, asText: true),
            'rating'       => fake()->numberBetween(1, 5),
            'is_featured'  => fake()->boolean(20),
            'published_at' => fake()->optional(0.8)->dateTimeBetween('-1 year'),
        ];
    }
}
```

```php
Testimonial::factory()->count(10)->create();
Testimonial::factory()->featured()->count(3)->create();
```

Seed:

```bash
lando acorn db:seed --class=TestimonialSeeder
```

See [`references/factories.md`](references/factories.md) for:
- Factory states (`featured()`, `unpublished()`)
- `fake()` helper reference
- Seeder structure and `DatabaseSeeder` registration
- WordPress context in seeders

## Critical Rules

1. **Set `$timestamps = false`** for WP core tables (`wp_posts`, `wp_users`) — they have no `created_at`/`updated_at`.
2. **Use `$table` explicitly** for every model — avoid Eloquent's table name guessing with WP prefix.
3. **Never use Eloquent to create/update WP core table rows in production** — use `wp_insert_post()`, `wp_update_post()`, `update_post_meta()` so hooks fire.
4. **Run migrations via `lando acorn migrate`** — never write raw SQL directly.
5. **Use `$fillable` explicitly** — never use `$guarded = []`; list only known, safe attributes.
6. **Eager load relationships** — use `::with()` or `->load()` to prevent N+1 queries in loops.

## Verification

- Run `lando acorn migrate:status` and confirm all migrations show as "Ran".
- Use `lando acorn tinker` to verify: `App\Models\Testimonial::first()` returns data from the correct table.
- Verify relationships: `App\Models\Testimonial::with('author')->first()` returns related data without errors.

## Failure modes

See [`references/troubleshooting.md`](references/troubleshooting.md) for all failure modes and escalation paths.

## References

Deep content loaded on demand — zero tokens until needed.

- **[models.md](references/models.md)** — Model class, `$table`, `$fillable`, `$casts`, custom primary key, `$timestamps = false` for WP tables, accessors.
- **[migrations.md](references/migrations.md)** — `Schema::create`, column types reference, `up()`/`down()`, running via `lando acorn migrate`.
- **[relationships.md](references/relationships.md)** — `hasMany`, `belongsTo`, `belongsToMany`, WP-specific: Post → PostMeta, Term → TermMeta, polymorphic.
- **[factories.md](references/factories.md)** — `HasFactory`, `definition()`, `fake()` reference, states, seeding with `lando acorn db:seed`.
- **[query-scopes.md](references/query-scopes.md)** — Local scopes, global scopes, `withoutGlobalScope()`, conditional `->when()`, raw queries.
- **[wp-tables.md](references/wp-tables.md)** — Integrating Eloquent models with WordPress core tables (`wp_posts`, `wp_postmeta`, etc.), read-only reporting, canonical patterns.
- **[troubleshooting.md](references/troubleshooting.md)** — Common errors, debugging commands, escalation paths for persistent issues.

## Escalation

- N+1 performance issues: see `superpowers-sage:wp-performance` for eager loading strategies.
- Writing to WP core tables: use WP API functions — `wp_insert_post()`, `update_post_meta()`, `wp_insert_user()`.
