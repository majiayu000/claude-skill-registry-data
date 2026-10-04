---
name: dl-rails-8
description: Implement, debug, refactor, and test Rails 8 applications using the project's supported Ruby version. Use for ActiveRecord, migrations, jobs, authentication, Solid adapters, Hotwire, and Rails 8 configuration. Match existing conventions and preserve behavior during refactoring; do not upgrade the stack as part of unrelated work.
---

# Rails 8 development

Inspect `.ruby-version`, Gemfile.lock, database adapters, frontend setup, and CI before editing. Use the application's Ruby version and Rails minor version, not a fixed Ruby 4 baseline. Rails 8 requires Ruby 3.2 or newer; compatibility of native gems, adapters, and deployment images must be checked separately.

Consult the version-matched [Rails guides](https://guides.rubyonrails.org/) for exact generator/API behavior. Do not upgrade Ruby or Rails merely to use an example from this skill.

## What changed in Rails 8 (don't carry old habits)

These are the defaults that trip up code written from older muscle memory:

- **No Redis required.** The "Solid" trifecta uses the SQL database instead: **Solid Queue** (Active Job backend, replaces Sidekiq/Resque for most apps), **Solid Cache** (Rails.cache backend, disk-backed, replaces Redis/Memcached), **Solid Cable** (Action Cable backend). New apps get these by default.
- **Propshaft**, not Sprockets, is the default asset pipeline. There is no `app/assets/config/manifest.js` Sprockets ceremony. Don't reach for Webpacker — it's gone.
- **Importmap + Turbo + Stimulus (Hotwire)** is the default frontend. No Node build step unless the user opts into `--javascript=esbuild|bundling`.
- **Built-in authentication generator**: `bin/rails generate authentication` scaffolds a session-based auth system (`User`, `Session`, `has_secure_password`, password reset mailer). Prefer it over hand-rolling auth or adding Devise unless the user needs Devise's feature set.
- **Kamal 2** is the default deploy tool (Docker-based, zero-downtime); a `Dockerfile`, `config/deploy.yml`, and **Thruster** (HTTP proxy for caching/compression/X-Sendfile) ship by default.
- **SQLite is production-viable** in Rails 8 (WAL, tuned defaults) for many small/medium apps. Don't reflexively swap it for Postgres unless the workload calls for it.

Read `references/rails8-features.md` for the deeper feature reference (Solid stack config, Kamal, generators, new APIs).

## Clean-code principles for Rails

Apply these where they solve an observed problem. During review, distinguish behavior defects from optional restructuring; a long model or missing service object alone is not a finding.

### Controllers stay skinny
Controllers coordinate; they don't hold business logic. A controller action should read like a short paragraph: find/build, delegate, respond. Push logic into models, query objects, or service objects. Use strong parameters via a private `*_params` method. Favor the standard seven RESTful actions and add new controllers rather than custom actions.

### Models stay focused (fat model ≠ god model)
Logic belongs in models, but a model that does everything is its own smell. Extract cohesive behavior into **concerns** (`app/models/concerns/`) for shared traits, **value objects** for domain concepts, and **service objects** (`app/services/`) for multi-step operations that span models or call external systems. A service object is a plain Ruby class with a single public `call` method and an intention-revealing name (`Orders::Checkout`, `Users::Invite`).

### Query objects for complex scopes
A query with reused or independently testable business meaning may belong in a query object (`app/queries/`) or a well-named scope — not inlined in a controller. Keep ActiveRecord scopes small and composable; name them for intent (`scope :active, -> { where(archived_at: nil) }`).

### Naming reveals intent
Methods and variables say what they mean. Predicates end in `?`, dangerous/bang methods in `!`. Avoid abbreviations. A reader should not need the implementation to understand the name. Prefer `overdue?` over `check_date`.

### Small methods, one level of abstraction
Each method does one thing at one level of abstraction. If a method mixes high-level orchestration with low-level detail, extract the detail into a private helper with a descriptive name. Aim for methods that fit on a screen.

### Avoid N+1 and other ActiveRecord traps
Eager-load associations with `includes`/`preload`/`eager_load`. Use `find_each` for large batches. Use `exists?` for database existence checks; `any?` without a block already uses an efficient existence check for many unloaded relations. Avoid an extra query when the relation is already loaded. Use `pluck`/`select` to avoid instantiating full records you won't use. Wrap multi-write operations in transactions. Lean on the `bullet` gem in development to catch N+1s.

### Callbacks sparingly
Callbacks that touch other models or external services make behavior hard to follow and test. Prefer explicit service calls. Reserve callbacks for in-model, side-effect-free data massaging (normalizing a field, setting a default).

### Tests are not optional
Add focused regression coverage for meaningful behavior changes; use existing checks for mechanical edits. Follow the test pyramid: many fast model/unit tests, fewer controller/request tests, a thin layer of system tests for critical flows. Use fixtures or factories, keep tests independent and deterministic, and assert behavior not implementation. Rails 8 ships with the default Minitest setup and parallel test runners; RSpec is fine if the project already uses it.

### Modern Ruby idioms (Ruby 3.2 → 4.0)
Use these where they improve clarity:
- Endless method definitions for one-liners: `def full_name = "#{first} #{last}"`.
- Pattern matching (`case/in`) for structured data and API response handling.
- Keyword arguments over positional for anything with more than one option.
- Hash shorthand: `{ user:, total: }` when the local and key names match.
- `Data.define(...)` for immutable value objects instead of `Struct` when you don't need mutation.
- Safe navigation `&.` instead of nested nil checks.
- Frozen string literals (the default magic comment is added by generators).

See `references/clean-code-patterns.md` for concrete before/after refactors of each principle, and `references/rubocop-config.md` for a starter RuboCop setup (rubocop-rails-omakase is the Rails 8 default style).

## Workflow

When the user asks you to build or change something:

1. **Confirm versions** — read `.ruby-version`/`Gemfile` or ask. Don't generate code for a stack you haven't confirmed.
2. **Use generators** — `bin/rails generate ...` for models, migrations, controllers, mailers, jobs, channels, and authentication. Generators produce the correct Rails 8 file layout and test stubs. Edit the output; don't write boilerplate from scratch.
3. **Run migrations safely** — generate the migration, review it (reversibility, indexes on foreign keys and lookup columns, `null: false` + defaults where appropriate, no data changes mixed with schema changes), then apply only to the intended development/test database. Check adapter/version-specific lock behavior and deployment order before proposing production execution.
4. **Apply the clean-code principles above** as you write — skinny controllers, focused models, extracted services/queries, intention-revealing names, tests alongside code.
5. **Verify** — run the relevant tests and `bin/rubocop` (autocorrect with `bin/rubocop -a` for safe fixes) before declaring done.

When the user asks for a **review or refactor**, read the code, identify which principles are violated, and for each one show the smell, name it, and give the concrete refactor — not vague advice. Prioritize correctness and the highest-leverage changes; don't bikeshed style that RuboCop would handle.

## Reference files

- `references/rails8-features.md` — Rails 8 feature reference: Solid Queue/Cache/Cable setup, Kamal + Thruster deploys, Propshaft/importmap, the authentication generator, SQLite-in-production tuning, and notable new APIs. Read when working with any of these.
- `references/clean-code-patterns.md` — Before/after refactors for each clean-code principle (skinny controller, service object, query object, concern, value object, callback removal, N+1 fixes). Read when writing or reviewing application code.
- `references/rubocop-config.md` — Starter `.rubocop.yml` based on rubocop-rails-omakase plus rationale. Read when setting up linting or resolving style questions.

## Transactions, jobs, and rollout

Before implementing a multi-step change, state its invariant: for example, one reservation per item, tenant-scoped uniqueness, or one provider charge per order. Put corresponding constraints in the database as well as validations; test competing requests where the invariant matters.

Trace the outer transaction. External HTTP calls are not rolled back, and nested transactions may not commit independently. Select after-commit enqueueing, provider idempotency keys, or an outbox based on the existing architecture. Test retries after a successful external call but before local acknowledgement.

For migrations, separate expand/backfill/contract steps when old and new app instances coexist. Backfills should be resumable and bounded, avoiding callbacks on today's application model in historical migrations. Index strategy depends on the actual adapter and version; do not copy PostgreSQL options into Oracle or MySQL migrations.

For Solid Queue/Cache/Cable, inspect the installed adapter and connection-pool topology rather than replacing an existing backend. A queue in another database does not share the application's transaction. Account for worker shutdown, retry exhaustion, and connection demand.

Verify the relevant request/model/job behavior, query count under representative cardinality, and the migration's compatibility with the current deployment. Report tests skipped because a database or service was unavailable.
