---
name: rails-docs
description: "Offline Ruby on Rails reference — the official Rails Guides and core API class docs bundled as on-demand markdown. Use when working in a Rails app or answering Rails questions: Active Record (migrations, validations, callbacks, associations, querying, encryption), Active Model, Action Controller (routing, strong parameters), Action View (layouts, form helpers), Action Mailer/Mailbox, Action Cable, Action Text, Active Job, Active Storage, Active Support, i18n, caching, security, testing, engines, generators, the asset pipeline, autoloading/Zeitwerk, deployment tuning, or upgrading Rails. Prefer this over web fetches and over recall for Rails behavior, defaults, and API signatures."
---

# Ruby on Rails Reference

Bundled, offline snapshot of the official Rails documentation:

- `references/guides/` — 54 Rails Guides (the conceptual "how Rails works" docs)
- `references/api/` — 80 core API class pages from api.rubyonrails.org (signatures, methods, options)
- `references/overview.md` — the Rails framework overview (what each component does)

**Source:** crawled from `guides.rubyonrails.org` and `api.rubyonrails.org`. Treat these files as the source of truth for Rails behavior, defaults, and method signatures. When a question is answerable from a bundled file, load that file with `Read` instead of fetching the web or answering from memory — Rails defaults change between versions and the bundled docs are the snapshot in hand.

## How to use this skill

1. Identify the Rails component/topic from the user's question (the map below).
2. `Read` the matching `references/guides/<file>` for concepts/behavior, and/or `references/api/<Class>.md` for exact method signatures and options.
3. Quote/apply the specific behavior; cite the guide name. Don't paraphrase from recall when the file is right here.

If unsure which component owns a concept, read `references/overview.md` first — it summarizes the responsibility of each Rails framework (Model/View/Controller layers + Action Mailer, Active Job, Action Cable, Active Storage, Action Text, Active Support).

## Topic → guide map

**Getting started / project setup**
- `getting_started.md` — first app, full walkthrough
- `install_ruby_on_rails.md`, `development_dependencies_install.md` — installation
- `command_line.md` — `rails`/`rake` commands, runners, consoles
- `configuring.md` — config files, initializers, `config.*` options
- `generators.md` — writing and customizing generators

**Models — Active Record** (load `references/api/ActiveRecord_*.md` for signatures)
- `active_record_basics.md` — models, CRUD, conventions → API: `ActiveRecord_Base.md`, `ActiveRecord_Persistence.md`, `ActiveRecord_Core.md`
- `active_record_migrations.md` — schema changes → API: `ActiveRecord_Migration.md`
- `active_record_validations.md` — validations → API: `ActiveRecord_Validations.md`, `ActiveModel_Validations.md`, `ActiveModel_Errors.md`
- `active_record_callbacks.md` — lifecycle hooks → API: `ActiveRecord_Callbacks.md`
- `association_basics.md` — has_many/belongs_to/etc. → API: `ActiveRecord_Associations.md`, `ActiveRecord_Associations_ClassMethods.md`, `ActiveRecord_NestedAttributes.md`
- `active_record_querying.md` — query interface → API: `ActiveRecord_FinderMethods.md`, `ActiveRecord_Scoping.md`, `ActiveRecord_Sanitization.md`
- `active_record_multiple_databases.md` — multi-DB → API: `ActiveRecord_ConnectionHandling.md`
- `active_record_composite_primary_keys.md`, `active_record_encryption.md` (→ `ActiveRecord_Encryption_EncryptableRecord.md`), `active_record_postgresql.md`
- Transactions/locking → API: `ActiveRecord_Transactions.md`, `ActiveRecord_Locking_Optimistic.md`, `ActiveRecord_Locking_Pessimistic.md`
- `active_model_basics.md` — Active Model for non-DB objects → API: `ActiveModel_API.md`, `ActiveModel_AttributeMethods.md`, `ActiveModel_Dirty.md`, `ActiveModel_Serialization.md`

**Views — Action View**
- `action_view_overview.md`, `action_view_helpers.md` — templates and helpers
- `layouts_and_rendering.md` — render/redirect/layouts
- `form_helpers.md` — form_with, form builders, nested forms

**Controllers — Action Controller**
- `action_controller_overview.md` — params, sessions, filters, strong params → API: `ActionController_Base.md`, `ActionController_Parameters.md`
- `action_controller_advanced_topics.md` — streaming, rescue, etc.
- `routing.md` — the router, resources, constraints
- Sessions/cookies → API: `ActionDispatch_Session_CookieStore.md`

**Other framework components**
- `action_mailer_basics.md`, `action_mailbox_basics.md` — outbound/inbound email
- `action_text_overview.md` — rich text
- `action_cable_overview.md` — WebSockets
- `active_job_basics.md` — background jobs
- `active_storage_overview.md` — file attachments
- `active_support_core_extensions.md`, `active_support_instrumentation.md` — Active Support helpers + instrumentation events
- `working_with_javascript_in_rails.md`, `asset_pipeline.md` — front-end assets, import maps

**Cross-cutting concerns**
- `i18n.md` — internationalization
- `security.md` — security guide (CSRF, mass assignment, injection)
- `caching_with_rails.md` — fragment/Russian-doll caching
- `error_reporting.md`, `debugging_rails_applications.md` — diagnostics
- `autoloading_and_reloading_constants.md` — Zeitwerk autoloading
- `threading_and_code_execution.md` — concurrency, the executor/reloader
- `sign_up_and_settings.md` — built-in authentication generator example

**Testing**
- `testing.md` — the full testing guide (model/controller/system/integration tests, fixtures)

**Deploy / maintain / extend**
- `tuning_performance_for_deployment.md` — app servers, threads, YJIT, pooling
- `upgrading_ruby_on_rails.md`, `maintenance_policy.md` — version upgrades and support windows
- `engines.md`, `plugins.md`, `rails_on_rack.md`, `initialization.md` — extending Rails internals
- `api_app.md` — API-only Rails apps

**Contributing to Rails** (only when the task is patching Rails itself)
- `contributing_to_ruby_on_rails.md`, `api_documentation_guidelines.md`, `ruby_on_rails_guides_guidelines.md`

## Notes & limits

- **Snapshot, not live.** These are crawled at a point in time (Rails ~8.x edge guides). For a version-specific question, confirm the target Rails version; if it differs materially, note that the bundled snapshot may not match and fall back to a targeted web fetch.
- **API coverage is partial.** `references/api/` holds the most-used Active Record / Active Model / Action Controller classes (depth-2 from the API index), not the entire API tree. If a needed class isn't bundled, the guides usually cover the behavior; otherwise fetch `https://api.rubyonrails.org/classes/<Class>.html`.
- **Don't dump whole files into context.** These guides are large. `Read` the single relevant file (and use `offset`/`limit` or grep within it) rather than loading several at once.
