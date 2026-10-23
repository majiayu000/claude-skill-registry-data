---
name: django-conventions
description: "Use when writing or reviewing Django: where behaviour lives (services and selectors), the ORM and transactions, migrations, settings and the deployment checklist, the API layer and tests."
paths: "**/models.py, **/views.py, **/urls.py, **/settings*.py, **/settings/**, **/migrations/*.py, **/services.py, **/selectors.py, **/manage.py, **/admin.py, **/forms.py"
---

# django-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of Django code, on top of
`skills/python-conventions` (typing, async, the toolchain) which stays on the language. Every rule below holds in a
repo with **nothing installed** (`CONVENTIONS.md`, rule A). **Special status**: like `go-conventions`, no in-house
production experience sits behind this block yet. The content comes from the framework's own documentation (the
development docs, Django 6.2 alpha when read on 2026-10-02) and one public style guide for the project structure;
treat it as a base to confront with the first real Django project, not as proven doctrine. A rule that needs a
recent feature carries the version; a project on an older release reads it as "not yet".

## When
As soon as Django code is written or modified, during `code` (6) or `tdd` (5): a model, a view or API handler, a
service, a queryset, a migration, a setting, a template that outputs user data, a test.

## Steps

**Read only the sections the task touches.** One file per section under `references/`; a section read is a section
that has to be applied. For a whole-diff review, pick the rows whose trigger the diff meets.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Where behaviour lives: services, selectors, models, signals, tasks | a rule has to be placed, or a model, a view or a task is written | [`01-structure-logic.md`](./references/01-structure-logic.md) |
| 2 | The ORM and transactions | a queryset, a loop over related objects, a bulk write, a lock, `atomic` or `on_commit` is written | [`02-orm-transactions.md`](./references/02-orm-transactions.md) |
| 3 | Migrations | a model change needs a migration, data is changed in one, or CI guards the migration state | [`03-migrations.md`](./references/03-migrations.md) |
| 4 | Settings, deployment, security | a setting, a deployment, a form that changes state, a template outputting user data, or a proxy is involved | [`04-settings-security.md`](./references/04-settings-security.md) |
| 5 | The API layer and tests | an endpoint, an error shape or a test is written | [`05-api-tests.md`](./references/05-api-tests.md) |

## Output / checkpoint
Code compliant with the sections read, `manage.py check` clean, `makemigrations --check` reporting nothing to
generate, and `check --deploy` against the production settings clean of findings the project has not recorded as
accepted. Tests green. Checked by `gate` (7) and `review` (8). Where the project cannot run these (no environment),
the checkpoint records which could not be run rather than reporting a pass, and nothing is installed to make them
run (`CONVENTIONS.md`: a block names a dependency and stops).

## Guardrails
No comments in the code produced. These rules govern **new** code; an existing fat `save()`, signal or view stays
until touched. A database constraint beats a model validation: when the two disagree, fix the schema. Never
loosen a check, a setting of the deployment checklist or a coverage threshold to get a diff through. The
services-and-selectors structure is a preference of one style guide, not a framework rule: a project with its own
established layering keeps it, and what this block insists on is that there is exactly one place for a rule, not
that the place has a given name. For the error body shape and idempotency, `skills/api-design`; for queues,
`skills/background-jobs-conventions`; for authentication and sessions, `skills/auth-session-conventions`.

## Origin
Rewritten from the Django documentation and one public Django style guide; the full provenance, licences and the
audit of what was left out are in [`references/origin.md`](./references/origin.md). Read it when checking a rule's
freshness, not when applying one.
