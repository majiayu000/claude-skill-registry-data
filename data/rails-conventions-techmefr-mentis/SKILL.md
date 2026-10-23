---
name: rails-conventions
description: "Use when writing or reviewing Ruby on Rails: routing and controllers, Active Record models and queries, migrations, configuration and jobs, the security surface, tests and the linter."
paths: "**/*.rb, **/*.erb, **/Gemfile, **/config/routes.rb, **/db/migrate/**, **/app/**/*.rb"
---

# rails-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Rails code. Every rule below holds in a
repo with **nothing installed** (`CONVENTIONS.md`, rule A). **Special status**: like `go-conventions`, no
in-house production experience sits behind this block yet. The content comes from the community Rails and Ruby
style guides, the rubocop-rails cops, and the framework's own guides, read on 2026-10-02 against the Rails 7.1 to
8.x range; it is a base to confront with the first real Rails project, not proven doctrine. Rails moves by
minor version: a rule that names a version says so, and a project on an older one reads those as upgrade notes.

## When
As soon as Rails code is written or modified, during `code` (6) or `tdd` (5): a route, a controller, a model, a
query, a migration, a job, a mailer, an initializer, a test.

## Steps

**Read only the sections the task touches.** One file per section under `references/`; a section read is a
section that has to be applied. For a whole-diff review, pick the rows whose trigger the diff meets.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Routing, controllers, views | a route, an action, a parameter list, a redirect or a template is written | [`01-routing-controllers.md`](./references/01-routing-controllers.md) |
| 2 | Models, Active Record, queries, N+1 | a model, an association, a validation, a callback or a query is written | [`02-active-record.md`](./references/02-active-record.md) |
| 3 | Migrations and the schema | a migration is written, or a column, index or constraint is added to a table with rows | [`03-migrations.md`](./references/03-migrations.md) |
| 4 | Configuration, time, translations, mail, jobs | a setting, a secret, a date, a user-facing string, an email or a job is touched | [`04-config-time-mail-jobs.md`](./references/04-config-time-mail-jobs.md) |
| 5 | Security surface | sign-in, a session, a state-changing form, a redirect, an upload, a header or an admin area is written | [`05-security.md`](./references/05-security.md) |
| 6 | Ruby judgment calls, tests, tooling | error handling or defaults in Ruby, a test, or the lint and CI set-up | [`06-ruby-tests-tooling.md`](./references/06-ruby-tests-tooling.md) |

## Output / checkpoint
Code compliant with the sections read, the framework's own checks clean, and the RuboCop Rails extension (with
the cops the sections cite switched on) producing no new finding from the diff. The test suite green, run with
`strict_loading` enabled where the project has adopted it (§2.26). Checked by `gate` (7) and `review` (8). Where
the linter is not installed in the project, the checkpoint records *no linter available* as a finding rather than
reporting a pass it did not observe, and does not install one (`CONVENTIONS.md`: a block names a dependency and
stops).

## Guardrails
No comments in the code produced. These rules govern **new** code; existing callbacks, default scopes and raw SQL
stay until touched. Never loosen a cop, a test or a coverage threshold to get a diff through: that is a project
decision. A database-level constraint beats a model validation (§2.9): when the two disagree, fix the schema.
For layer-level API design (versioning, error shape, idempotency) defer to `skills/api-design` (§5); for
authentication and session design in depth, `skills/auth-session-conventions`; for queues beyond Active Job's
own API, `skills/background-jobs-conventions`; for the language-neutral security review, `skills/security-hardening`.
This block has not been confronted with a real Rails project: if a rule diverges from an observed need, fix this
block rather than treating it as settled.

## Origin
Rewritten from the Rails and Ruby community style guides, the rubocop-rails cop reference and the Rails guides;
the full provenance, licences and the audit of what was left out are in
[`references/origin.md`](./references/origin.md). Read it when checking a rule's freshness, not when applying one.
