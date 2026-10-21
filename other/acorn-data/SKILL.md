---
name: acorn-data
description: Use when storing or querying data through Acorn's database layer - Eloquent models (app/Models, models over wp_posts, postmeta, users), custom tables, migrations (make:migration, migrate --force on deploy), seeders and factories, the DB facade, table prefix errors ("Table wp_wp_x doesn't exist"), and choosing post meta vs options vs a post type vs a custom table. For queues use acorn-background; for endpoints use acorn-routes-api; for post type registration use acorn-scaffolding.
---

# Data with Eloquent and migrations under Acorn

Acorn registers Laravel's database layer with a default `wordpress` connection built from the WordPress constants (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_CHARSET`) and **the WordPress table prefix** (`$wpdb->prefix`). Every Eloquent model, `DB::table()` call and migration on that connection is prefixed automatically.

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.composer}}`, `{{runner.test}}`) come from the session context; on Lando they default to `lando wp`, `lando wp acorn`, `lando composer` and the project's test tooling.

## When to use

- A custom table for application data (submissions, queues, audit logs, sync state).
- Read-heavy or reporting queries over WordPress tables that `WP_Query` expresses badly.
- Migrations, seeders and test data for those tables, and running migrations in a deploy.

### Native first: where should the data live?

| Data | Native mechanism (verify in `wp-includes/`) | Custom table when |
|---|---|---|
| Content editors manage, with URLs, revisions, search | custom post type + post meta (`register_post_type`, `update_post_meta`) | never for this case |
| A few site-wide settings | options (`get_option`, autoload off for large values) | never |
| Per-user settings | user meta | never |
| Per-term data | term meta | never |
| High-volume rows, queues, logs, joins, unique constraints, rows nobody edits in wp-admin | none fits well | yes: migration + model |

Write the reason in the change when you choose a custom table.

## Inputs required

1. Active profile, Acorn base path and namespace (session context).
2. The database config the app actually uses: `config/database.php` in the base path if present, otherwise Acorn's default (`wordpress` connection, prefix from `$wpdb->prefix`).
3. Existing models (`app/Models`) and migrations (`database/migrations`) in the base path.
4. How the project deploys: which step runs migrations, and whether production has several instances starting at once.

### Profile differences

| Item | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Models | `app/Models` in the theme, `App\Models` | `app/Models` in the plugin, `<Namespace>\Models` | `app/Models` at the root, `App\Models` (the starter already ships models over WordPress tables) |
| Migrations, seeders | `database/migrations`, `database/seeders` in the theme | same folders in the plugin | same folders at the root |
| Environment for `migrate` | `app.env` = `WP_ENV`, else `production` | same; projects without `WP_ENV` are always `production`, so `migrate` asks for confirmation or `--force` even locally | Bedrock-style `WP_ENV` is set per environment |
| Deploy hook | the theme's deploy script | the image or release script that starts the app | the project's deploy script |

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

1. **Choose the store** with the native-first table. If a CPT or meta fits, stop here and use `acorn-scaffolding` or plain WordPress APIs.
2. **Create the migration**: `{{runner.acorn}} make:migration create_form_submissions_table`. In `up()` use the **unprefixed** name (`Schema::create('form_submissions', …)`); the connection adds the prefix, giving `wp_form_submissions`. Always write `down()`. Details: [references/migrations.md](references/migrations.md).
3. **Run it locally**: `{{runner.acorn}} migrate` (add `--force` when `app.env` is `production`), then `{{runner.acorn}} migrate:status`. The log table is `migrations` on the same connection (`wp_migrations` with the default prefix); `migrate:install` creates it if missing.
4. **Create the model**: `{{runner.acorn}} make:model FormSubmission` (Acorn 6.2 has `make:model`; it has no `make:factory`, so do not pass `--factory` or `--all`). Set `$table` without the prefix only when the name differs from the plural snake case, list `$fillable`, declare `$casts`. For WordPress tables: `$table = 'posts'`, `$primaryKey = 'ID'` (or `meta_id`, `term_id`, `umeta_id`), `public $timestamps = false`. Details: [references/models.md](references/models.md).
5. **Write through WordPress for WordPress data.** Inserts and updates on posts, meta, users, terms and options go through `wp_insert_post()`, `update_post_meta()`, `wp_update_user()` and friends so hooks, caches and revisions stay correct. Use Eloquent for reads there, and for reads and writes on your own tables.
6. **Mind the object cache.** Eloquent bypasses the WordPress object cache. After writing to a WordPress table outside its API, call the matching `clean_*_cache()`; better, do not write there.
7. **Seed and test data**: seeders in `database/seeders` (`{{runner.acorn}} make:seeder`, `{{runner.acorn}} db:seed --class=…`). Factories need `fakerphp/faker` as a dev dependency and hand-written classes: [references/factories-seeders.md](references/factories-seeders.md).
8. **Deploy**: run `{{runner.acorn}} migrate --force` once per release, after the new code is in place and caches are rebuilt (`optimize`), before traffic switches. With several instances, run it from one job or one instance only, and keep migrations backward compatible with the previous release while both run.

## Verification

- `{{runner.acorn}} migrate:status` shows every migration as `Ran`.
- `{{runner.wp}} db query "SHOW TABLES LIKE '%form_submissions'"` lists the table exactly once, with the expected prefix (a `wp_wp_` hit means a doubled prefix).
- `{{runner.wp}} eval 'var_dump(App\Models\FormSubmission::query()->count());'` (with your namespace) runs without SQL errors. Acorn providers boot for every WP-CLI command, so facades and models work inside `wp eval`.
- Tests that touch the database run through `{{runner.test}}` against a test database, never the shared one.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `Table 'db.wp_wp_x' doesn't exist` | `$table` or `Schema::create()` includes the prefix, which the connection adds again | Use unprefixed names everywhere on the `wordpress` connection |
| `Unknown column 'updated_at'` | WordPress tables have no Laravel timestamps | `public $timestamps = false` |
| `find()` returns null on posts or users | Default primary key `id` | `$primaryKey = 'ID'` |
| `migrate` stops with "Application in production" | `app.env` resolves to `production` (no `WP_ENV`) | Pass `--force` when you intend to run it; set `WP_ENV` where the project supports it |
| `Migration table not found` | Fresh database or other connection | `{{runner.acorn}} migrate:install`, check `DB_CONNECTION` |
| `Command "make:factory" is not defined` | Acorn does not register the factory generator | Write the factory class by hand |
| `Call to undefined function fake()` | `fakerphp/faker` not installed | `{{runner.composer}} require --dev fakerphp/faker` in the base path |
| Edited post meta does not show on the site | Write bypassed WordPress, object cache still holds the old value | Write through `update_post_meta()`, or `clean_post_cache()` after the write |
| Mass assignment error | Attribute not in `$fillable` | Add it; do not use `$guarded = []` |
| Two instances run the same migration at once | Migrations run on every container start | Move `migrate --force` to one release job |

## Escalation

- Destructive migrations on shared data (`dropColumn`, `migrate:fresh`, `migrate:reset`, `db:wipe`, `migrate:rollback` on production): stop and ask.
- Writing directly to WordPress core tables with Eloquent or `DB`: ask first and name the WordPress API you are bypassing and why.
- A second database or a non-WordPress connection: ask; credentials belong in the environment, never in code.
- Queued processing of the rows: `acorn-background`. Endpoints over them: `acorn-routes-api`.

<!-- verified:
vendor/roots/acorn/config/database.php:20 default connection 'wordpress'; :47-57 built from DB_* constants with 'prefix' => $wpdb->prefix; :149-150 migrations table 'migrations'
vendor/roots/acorn/config/app.php:32 env = WP_ENV or 'production'; :45 debug = WP_DEBUG && WP_DEBUG_DISPLAY
vendor/roots/acorn/src/Roots/Acorn/Console/Kernel.php:84-96 — SeedCommand, SeederMakeCommand, ModelMakeCommand registered; no FactoryMakeCommand
vendor/roots/acorn/src/Roots/Acorn/DefaultProviders.php:37 MigrationServiceProvider added; composer.json requires illuminate/database, not fakerphp/faker
vendor/roots/acorn/src/Roots/Acorn/Application/Concerns/Bootable.php:79-82 — WP-CLI boot bootstraps the console kernel (providers boot for every wp command)
reference acorn-mu-plugin project: database/migrations/*_create_*_table.php — Schema::create() with unprefixed names; app/Models/PostMeta.php:11-13 — $table 'postmeta', meta_id, no timestamps; container setup script runs acorn migrate --force once per start
roots-docs acorn/eloquent-models.md — WP models with $table 'posts', ID, timestamps false; its custom-table example 'wp_custom_table' would double-prefix; its "no make:model" note is outdated for Acorn 6.2
roots-docs acorn/creating-and-running-laravel-migrations.md — migrate --force after optimize in deploys, migrate:install
radicle-app facts checked against a licensed local Radicle project; not reproduced here
-->
