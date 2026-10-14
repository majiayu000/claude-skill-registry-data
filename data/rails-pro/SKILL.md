---
name: rails-pro
description: Ruby on Rails guidance — MVC conventions, ActiveRecord mastery, Hotwire, background jobs, and production ops.
category: development
---

## Overview

Rails is the original convention-over-configuration framework: follow its opinions about naming, directories, and REST, and enormous amounts of behavior (routing, ORM, migrations, mailers, jobs, caching) come free. Deviate silently and you fight the framework at every step. This skill covers idiomatic Rails — the parts that make teams fast (ActiveRecord, migrations, Hotwire) and the parts that bite (N+1s, callback spaghetti, deploy config) — plus modern Rails with import maps, Turbo, and Stimulus.

## When to use

- Building a full-stack web app the Rails way (monolith-first).
- Fixing N+1 queries, slow pages, or callback-heavy models.
- Structuring jobs, mailers, and service objects in a growing app.
- Using Hotwire (Turbo + Stimulus) instead of a JS SPA.
- Deploying Rails to production (assets, DB, workers, caching).
- Upgrading Rails across major versions.
- Adding an API to an existing Rails monolith.

## Core concepts

- **Convention over configuration.** File names, class names, table names, and routes map to each other (`UsersController` → `app/controllers/users_controller.rb` → `users` table). Learn the conventions once and the framework disappears.
- **ActiveRecord is the heart.** Models map to tables; associations (`has_many`, `belongs_to`) generate queries. Eager load with `.includes` to kill N+1s; use scopes for composable query logic; keep SQL fragments minimal and parameterized.
- **Migrations with discipline.** Each migration should be small, reversible (`change`), and safe on large tables — add columns without defaults/backfill separately, add indexes `CONCURRENTLY` (via `algorithm: :concurrently` on Postgres), never rewrite history that's deployed.
- **Callbacks are a code smell at scale.** `before_save`/`after_commit` chains create invisible coupling. Prefer explicit service objects or form objects for multi-model operations; reserve callbacks for true model invariants.
- **Hotwire over SPA.** Turbo Drive/Frames/Streams plus Stimulus controllers deliver SPA-like interactivity with server-rendered HTML. Reach for it before adding React — most CRUD apps don't need a JS framework.
- **Background jobs via ActiveJob.** Sidekiq (Redis-backed) is the standard adapter. Jobs must be idempotent and retry-safe; pass IDs, not objects; keep payloads small.
- **The asset pipeline, modern.** Import maps + Sprockets or Propshaft for JS without a bundler; use a bundler (esbuild/vite via jsbundling-rails) only when you need npm-heavy frontend code.
- **Strong Parameters.** `params.require(:user).permit(:name, :email)` — the mass-assignment protection at the controller boundary. Never skip it; it's the difference between a form and a privilege-escalation vector.
- **Caching.** Russian-doll fragment caching, low-level `Rails.cache.fetch`, HTTP caching with ETags — Rails' caching is excellent when keys are versioned on the underlying records (`cache_key_with_version`).
- **Zeitwerk autoloading.** Constants map to file paths; no more `require` spaghetti. Name files correctly and autoloading disappears as a concern — misname them and you get uninitialized-constant mysteries.
- **ActiveStorage.** Uploads backed by local disk/S3/GCS with variants for image processing; use direct uploads so large files bypass the app server.
- **Action Mailbox/Text.** Inbound email/SMS routed into the app as first-class objects — handy for support inboxes and reply-by-email features without extra services.

## Practical workflow

1. **Generate with intent.** `rails new shop --database=postgresql --css=tailwind`; keep the monolith until a real boundary demands extraction.
2. **Model the domain.** Resources first (`resources :orders`), models with validations and associations, scopes for query logic, service objects (`app/services/`) for multi-step operations.
   ```ruby
   class Order < ApplicationRecord
     belongs_to :customer
     has_many :line_items, dependent: :destroy
     scope :recent, -> { order(created_at: :desc) }
     scope :paid, -> { where(status: "paid") }
   end
   ```
3. **Kill N+1s early.** Install the `bullet` gem in development — it shouts when you eager-load wrong. Review with `rack-mini-profiler` on slow pages.
4. **Add interactivity with Hotwire.** Turbo Frames for partial updates, Turbo Streams for realtime via ActionCable, Stimulus controllers for client-side behavior. Write system tests for the flows.
   - Keep Stimulus controllers small and single-purpose; reach for Turbo Streams before custom JS.
5. **Jobs and mailers.** ActiveJob + Sidekiq; mailers with parameterized previews; all async work idempotent with exponential backoff.
   ```ruby
   class InvoiceJob < ApplicationJob
     queue_as :billing
     retry_on ActiveRecord::Deadlocked, attempts: 5
     def perform(invoice_id)
       Invoice.find(invoice_id).generate_pdf!
     end
   end
   ```
6. **Test the pyramid.** Model/unit tests fast and many; request specs for API behavior; system tests (Cuprite/Selenium) sparingly for critical flows — they're slow, so choose the flows that matter.
7. **Cache deliberately.** Fragment caching with versioned keys, `stale?`/`fresh_when` for HTTP caching, and low-level caching for expensive computations — with explicit expiration strategies.
8. **Ship it.** Compile assets at build time, run migrations in a release phase (not in web boot), provision Redis for cache/jobs/Cable, set `RAILS_MASTER_KEY` via secrets management, and enable structured logging.

   ```ruby
   # Turbo Stream broadcast from a model — realtime without custom JS
   class Message < ApplicationRecord
     after_create_commit -> { broadcast_append_to "room_#{room_id}", target: "messages" }
   end
   ```

## Common pitfalls

- **N+1 queries** in views and serializers — Bullet in dev, `includes` in code, query-count assertions in tests.
- **Callback hell** — chains of `after_save` that trigger other saves; extract to service objects with explicit sequencing.
- **Unsafe migrations on big tables** — locking `ALTER TABLE` during deploys; use concurrent index creation and multi-step column changes.
- **Passing ActiveRecord objects to jobs** — serialization breaks and stale data; pass IDs and re-fetch.
- **Ignoring the asset pipeline** — shipping uncompiled assets or massive JS bundles; audit with build output sizes.
- **Secrets in the repo** — `credentials.yml.enc` + master key via env/secret store; never commit the key.
- **No database timeouts** — set `statement_timeout` and pool sizes; a hung query should fail, not cascade.
- **Skipping Strong Parameters** — mass-assignment vulnerabilities; permit explicitly at every controller boundary.
- **ActionCable without Redis in production** — the async adapter doesn't work across processes; configure the Redis adapter.
- **Forgetting `dependent:` on associations** — orphaned rows accumulating; decide destroy/nullify/restrict explicitly per association.
- **Turbo + custom JS conflicts** — event listeners vanish on Turbo navigation; hook `turbo:load` or move behavior into Stimulus controllers.
- **Abusing `default_scope`** — surprising query behavior in every context; prefer explicit named scopes at call sites.
- **CookieStore overflow** — sessions over 4KB break; switch the session store to cache or DB when storing more than a user id.
