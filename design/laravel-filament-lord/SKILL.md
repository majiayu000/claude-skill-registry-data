---
name: laravel-filament-lord
description: Lord skill for Laravel 13 + Filament v5 full-stack mastery — admin panels, resources, API, database, and UI in one cohesive workflow.
triggers:
  - laravel filament lord
  - laravel filament
  - filament laravel
  - admin panel
  - filament resource
  - laravel ui
  - filament v5
  - laravel 13
  - fullstack laravel
  - لارافيل filament
  - لوحة تحكم لارافيل
personas:
  - DEV
  - DB
  - SEC
tech_stack:
  - laravel-13
  - filament-5
  - php-8-5
  - tailwind-4-3
  - mysql-9-7
  - postgresql-19
lord: true

---

# Laravel + Filament Lord

[OBJ] Full-stack mastery of Laravel 13 + Filament v5 — admin panels, resources, API, database design, and UI in one cohesive workflow. This is the primary skill for daily Laravel/Filament development.

[RULES]
1. [CMD] Query Context7 MCP for Laravel 13 and Filament v5 docs before implementation. Use `/laravel/framework` and `/filament/filament` library IDs.
2. [REQ] Version Detection: Read `composer.lock` for exact Laravel + Filament versions before loading tech-stack files. NEVER assume versions.
3. [REQ] Stack Loading: Load `tech-stack/laravel-13.md`, `tech-stack/filament-5.md`, `tech-stack/php-8-5.md`, `tech-stack/tailwind-4-3.md` at start.
4. [REQ] Filament Resource Pattern: Use `Filament\Schemas\Components` (NOT `Filament\Forms\...`). Schema is the unified composition system in v5. `Schema::make()->components([...])` for both forms and infolists.
5. [REQ] Cluster Pattern: Organize related pages via `Cluster` base class. `->discoverClusters(in:, for:)` for auto-discovery. NEVER put all resources flat in one panel.
6. [REQ] Plugin Architecture: Every feature as a plugin (`Plugin` interface: `getId()`, `register(Panel)`, `boot(Panel)`). Register via `->plugins([Plugin::make()])`. Use `configureUsing()` for global defaults.
7. [REQ] Policy + Shield: Use `FilamentShield` for RBAC. `->shield()` on resources. NEVER use `$guarded = []` or bypass policy gates. Every resource action must have a corresponding policy method.
8. [REQ] Eloquent Strict Mode: `Model::shouldBeStrict()` enabled. Use `data_get($this->getAttributes(), 'column')` for optional columns to avoid `MissingAttributeException`. NEVER access `$this->optional_column` directly.
9. [REQ] API Resources: `JsonResource` with `JSON_STRUCTURE` constants. `->assertJsonStructure(Resource::JSON_STRUCTURE)` in tests. NEVER inline response shapes in controllers.
10. [REQ] Vector Search (13.31+): Use `AsVector` cast for embeddings. `whereVectorSimilarTo()` for semantic search. Use MariaDB 11.7+ or PostgreSQL with pgvector. NEVER use `array` cast for vector columns.
11. [REQ] Database Design: Use migrations with `Schema::create()`. Index foreign keys and frequently queried columns. Use cursor pagination for >10k rows. NEVER use `SELECT *` in production queries.
12. [REQ] Testing: Pest 3+ for backend. `artisan test --filter=<test>` for FAST tier. `artisan test` for FULL tier. Factories + seeders, no hardcoded IDs. 80% logic, 90% API coverage.
13. [REQ] Tailwind v4.3: Use `@theme` in CSS (not `tailwind.config.js`). Logical properties (`ms-*`, `me-*`) for RTL/Arabic. `motion-reduce:` for a11y. Filament requires Tailwind v4.1+.
14. [REQ] Security: `FormRequest` for inputs. Parameterized queries. Whitelist `$fillable`. No PII in logs. JWT in HttpOnly cookies. API throttling. Sanitize HTML (DOMPurify).
15. [REQ] Performance: `->deferLoading()` on heavy schemas. Reverb SSE for real-time (NEVER polling). `->persistGroupingInSession()` for table grouping. Octane for long-running with state flushing.
16. [REQ] RTL/Arabic: `dir="rtl"` on `<html>`. Tailwind logical properties auto-flip. Filament SlideOver `->position('left')` for RTL. Store translations in `lang/ar/`.

[WORKFLOWS]
1. Creating a Filament Resource: `php artisan make:filament-resource User` → define schema in `getFormSchema()` → add table columns → define pages → register policy → test with Pest.
2. API + Admin Coexistence: API resources in `app/Http/Resources/`, Filament resources in `app/Filament/Resources/`. Share models + scopes. Version API via `X-Api-Version` header.
3. Vector Search Setup: `CREATE EXTENSION vector` (PG) or MariaDB 11.7+ → migration with `vectorColumn` → `AsVector` cast on model → `whereVectorSimilarTo()` in controller → Filament filter for semantic search.
4. Multi-tenant Panel: `->tenant(Team::class)` on panel → `->scopeTenancy()` → FilamentShield per-tenant roles → `globalScope` on models → database row-level security.
