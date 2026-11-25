---
name: rails-rules
description: Standing rules for Rails code covering conventions, strong parameters, restraint with callbacks, eager loading, deploy-safe migrations, background jobs and request specs.
license: CC0-1.0
metadata:
  version: 1.0.0
  kind: rule
  category: conventions
  source: https://hermes-ide.com/prompts/rails-rules
  catalog: 2026.1014.1
---

# Ruby on Rails rules

Apply these rules to files matching: `app/**/*.rb`, `config/**/*.rb`, `db/**/*.rb`, `lib/**/*.rb`, `spec/**/*.rb`, `test/**/*.rb`, `app/views/**`.

When you write or change code in this Rails application:

**Conventions first**
- Check the Rails version in `Gemfile.lock` and follow the idioms of that version and of this codebase. Use Rails naming, RESTful resource routes and the standard directory layout before inventing structure. Add a custom route only when no resource action fits.
- Keep controllers to the seven resource actions where possible; a new verb is usually a new resource (`resource :publication` instead of `post :publish`).
- When logic spans several models or calls external services, put it in a plain Ruby object in the project's chosen place (service objects, `app/models` POROs, or concerns if that is the house style). Do not introduce a new architectural pattern the codebase does not already use.

**Strong parameters**
- Permit attributes explicitly with the version's strong-parameters API (`params.expect` on versions that have it, otherwise `params.require(...).permit(...)`). Never use the bang form of `permit` that allows every attribute, and never permit `role`, `admin`, `user_id`, prices or other server-owned fields from user input.
- Scope lookups through the current user or tenant (`current_user.projects.find(params[:id])`), never a bare `Project.find` on a user-controlled id.

**Callbacks**
- Use model callbacks only for changes to the record itself (normalising a field, setting a default). Do not send email, enqueue jobs, call APIs or update other models from `before_*` or `after_save` callbacks; do it explicitly in the code path that owns the action.
- When a side effect must follow a successful write, use `after_commit` (or the project's equivalent) so it never runs for a rolled-back transaction.

**Queries**
- Eager load every association a view, serializer or loop touches (`includes`, `preload` or `eager_load`). When you add a field that follows an association, update the query in the same change. Respect `strict_loading` where the project enables it.
- Never query inside a loop. Use `where(id: ids)`, `pluck`, `exists?`, `insert_all`, `update_all` or counter caches, and `find_each` for large batches.
- Use parameterised conditions (`where(name: value)` or placeholders); never interpolate user input into SQL strings or `order` clauses.
- Back every uniqueness validation with a unique index, and every foreign key with a database constraint.

**Migrations**
- Write reversible migrations (`change` with reversible operations, or explicit `up` and `down`).
- On large tables, keep deploys safe: add indexes concurrently with DDL transactions disabled (on PostgreSQL), add columns without volatile defaults, backfill in batches in a separate job or migration, and remove a column in two deploys (add it to `ignored_columns` first, then drop it).
- Never reference application model classes in migrations that will outlive them; use SQL or a minimal model defined inside the migration.

**Background jobs**
- Make jobs idempotent and safe to retry. Pass ids or GlobalID-serialisable records, not large objects, and handle a record that no longer exists.
- Enqueue jobs after the surrounding transaction commits, set a sensible retry and discard policy, and keep each job to one unit of work.

**Views and security**
- Rely on output escaping; never call `html_safe` or `raw` on user content. Use `sanitize` with an allow list when rich text is required.
- Keep CSRF protection on for browser controllers. Store secrets in encrypted credentials or environment variables, never in the repository.

**Tests**
- Test behaviour through request specs (or integration tests in Minitest projects) rather than controller specs, plus model specs for validations and scopes. Use the project's factories or fixtures.
- Cover authorisation: a user must not read or change another user's records.
- Before finishing, run the test suite and the linter the project uses, and confirm `db/schema.rb` (or `structure.sql`) matches the migration you wrote.
