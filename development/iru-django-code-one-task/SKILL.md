---
name: iru-django-code-one-task
description: "Invoked as /iru-django-code-one-task <task description> (the task's text with its implementation_plan.md checkbox lines) via Skill. Implements one Django (any project shape, migrations included) plan task and its tests, compile-checks, ticks the checkbox with a group-validation-pending note; no baseline or full gates, which iru-django-code-one-task-group runs."
model: sonnet
allowed-tools: Read Edit Write Bash(uv run *) Bash(poetry run *) Bash(pdm run *) Bash(pipenv run *) Bash(.venv/bin/*) Bash(python *) Bash(python3 *) Bash(command -v *) Bash(git status *) Bash(git diff *) Bash(git log *) Bash(find *) Bash(grep *) Bash(ls *) Bash(cat *) Bash(mkdir -p build*)
---

# Implement one plan task (Django)

Carry out a single task's implementation, tests, migration (when the task changes a model), and checkbox update
against a Django project — nothing else. This is the narrowest execution unit for a Django project in the `iru-code`
pipeline: `iru-django-code-one-task-group` calls it once per task in a bucket (potentially several at once, in
parallel agents), then handles license headers, docstrings, the Django system and migration checks, coverage, code
quality, the full fast suite, and the container-backed integration tier itself, once for the whole bucket.

Two things make Django different from the other coding keys:

1. **Django forgives some mistakes silently.** A `ModelSerializer` with `fields = "__all__"`, a `get_queryset()`
   that isn't scoped to the user, a side effect fired inside a transaction that later rolls back, an N+1 loop in a
   template, a model change without its migration — each works on the happy path and passes a careless test. The
   reference files exist mostly to prevent those.
2. **The migration is part of the task.** A task that changes a model is not done until `makemigrations` has
   generated the migration and it has been read. Applied migrations are history: never edited, never deleted.

It uses a medium model on purpose: the plan already carries the hard reasoning, and the guidance lives in
`reference/` rather than being re-derived per task.

## Step 1 — Detect the project's shape, then read only the reference material this task needs

Detect once, from files rather than assumptions — the same facts the group skill and the `iru-python-*` gates
detect, so a task never disagrees with its validator. Never assume the catalog's scaffold; many Django projects
predate it.

1. **Runner prefix** — `uv.lock` → `uv run`; `poetry.lock` → `poetry run`; `pdm.lock` → `pdm run`; `Pipfile.lock`
   → `pipenv run`; a `.venv/` → `.venv/bin/python`; otherwise bare `python -m` (say so in Step 8 — it may resolve to
   the wrong interpreter). Every command below is written as `<run>`; never `pip install` anything, never into the
   system Python.
2. **Django project root and version** — the directory holding `manage.py` (the repository root, or e.g. `src/`
   or `backend/` in a polyglot repository). Version from the lock file, else `<run> python -m django --version`.
   Don't use APIs newer than it: `django.tasks`, CSP middleware and template partials are 6.0; fetch modes
   (`FETCH_PEERS`/`FETCH_RAISE`), `MAILERS`, and `DB_CASCADE` are 6.1; `LoginRequiredMiddleware` is 5.1;
   `CompositePrimaryKey` is 5.2.
3. **Settings modules** — the one `manage.py` defaults to (`os.environ.setdefault("DJANGO_SETTINGS_MODULE", …)`),
   and the **test settings**: `DJANGO_SETTINGS_MODULE` / `--ds` in `[tool.pytest.ini_options]`, `pytest.ini`,
   `setup.cfg` or `tox.ini`, else `[tool.django-stubs] django_settings_module`, else a `settings/test.py` /
   `settings_test.py`. Note the split (`config/settings/{base,local,test,production}.py`, `dev`/`prod`, or one
   `settings.py` driven by env vars) and where a new setting belongs (`reference/settings.md`).
4. **App layout** — from `INSTALLED_APPS` and the `apps.py` files: apps under a top-level `apps/` package
   (`AppConfig.name = "apps.catalog"`, `label = "catalog"`), root-level apps (`name = "catalog"`), or apps inside a
   project-slug package (cookiecutter-django). Record the **app label** of every app the task touches —
   `makemigrations` and `reverse()` namespaces use it.
5. **API style** — `rest_framework` in `INSTALLED_APPS` → **DRF** (and `drf_spectacular` → schema generation
   validated by the group); `django-ninja` in the dependencies / a `NinjaAPI(` instance → **Ninja**; neither →
   plain Django views. Both can coexist under different prefixes — follow the one the touched app uses.
6. **Test runner and data builders** — `pytest-django` in the dev dependencies with a settings module configured
   → **pytest-django**; otherwise the built-in **`manage.py test`** runner. `factory-boy` (`<app>/tests/factories.py`)
   or `model-bakery` (`baker.make`), or neither. Test placement: `<app>/tests/test_*.py`, `<app>/tests.py`, or a
   root `tests/` tree.
7. **Fast vs. integration** — fast tests need no external service (SQLite in memory in the test settings, or no
   database at all). Integration tests carry the project's marker or tag (`@pytest.mark.integration`, `@tag("integration")`,
   whatever `markers =` declares) and use testcontainers, a PostgreSQL service, Redis, a live server, or a browser.
   **If the test settings point every test at a PostgreSQL/MySQL server, every `django_db` test is integration** —
   only `SimpleTestCase`/no-DB tests are fast; record it, Step 6 depends on it.
8. **Type checker and docstring convention** — `[tool.mypy]` with `mypy_django_plugin.main` (django-stubs; plus
   `mypy_drf_plugin.main`) and whether `strict = true`, or `pyright`/`basedpyright`; Ruff's
   `[tool.ruff.lint.pydocstyle] convention` (Google unless it says `numpy`/`pep257`); the formatter (`ruff format`
   or `black`).
9. **Background work** — a `TASKS` setting / `from django.tasks import task` (`django.tasks`), or Celery
   (`config/celery.py`, `celery` in the dependencies, `@shared_task`). Only matters if the task enqueues work.
10. **UI test wiring** — only when the task touches server-rendered UI: `pytest-playwright` and
    `axe-playwright-python` in the dev dependencies, a registered `ui` marker, `tests/ui/ui_screenshots.py`,
    `.ui-quality.yml` at the repository root, `LocaleMiddleware` with an RTL language in `LANGUAGES`, and whether
    HTMX (`django-htmx`, `hx-` attributes), Stimulus/Alpine, or `django-components`/`django-cotton` are in use.

Then read `reference/README.md` first — it is short and routes you to the rest — then read only what it points at:

| Read | When |
|---|---|
| `reference/code-style.md` | **Always.** |
| `reference/testing.md` | **Always** — writing the tests is part of the task. |
| `reference/models-and-orm.md` | The task adds/changes a model, field, relation, constraint, index, manager/QuerySet, migration, query, transaction, signal, or service function. |
| `reference/views-urls-templates.md` | The task adds/changes a view (FBV/CBV/async), URL pattern, template, template tag, middleware, or htmx fragment. |
| `reference/ui-contract.md` + `reference/ui-implementation.md` | The task adds or changes a screen, component, list or other UI — a page template, a partial/inclusion tag, a paginated list, or an htmx fragment users see. |
| `reference/forms-and-validation.md` | The task adds/changes a `Form`/`ModelForm`/formset, a validator, or model `clean()`. |
| `reference/drf.md` | API style is DRF and the task touches a serializer, viewset/view, router, permission, throttle, pagination, filter, or the OpenAPI schema. |
| `reference/ninja.md` | API style is Ninja and the task touches a router, operation, or schema. |
| `reference/admin.md` | The task touches `admin.py`, a `ModelAdmin`, inline, admin action, or admin template. |
| `reference/settings.md` | The task reads or adds a setting or environment variable, touches the settings modules, logging, caches, storages, or adds a system check. |
| `reference/tasks-and-celery.md` | The task enqueues background work, adds a `django.tasks` task or Celery task, or adds a management command. |
| `reference/auth.md` | The task touches the user model, login/logout/sign-up, passwords, permissions, groups, or object-level access. |
| `reference/security.md` | The task touches request input, rendered output, raw SQL, file uploads, redirects, CORS/CSP/CSRF, outgoing email or HTTP, or secrets — **always** for a new view or API endpoint. |

Don't read the optional files speculatively — a change inside one existing service function needs `code-style.md`,
`testing.md`, and `models-and-orm.md`, and nothing else.

If `reference/` is missing (e.g. the skill directory was copied without it), proceed using this repository's own
`CLAUDE.md` conventions and the surrounding code's style, and say so in Step 8's report — don't guess at what the
reference would have said.

## Step 2 — Re-check the current code state

Read the actual current content of every file the task touches, plus the touched app's `models.py` (or `models/`
package), its `urls.py`, and its latest migration when the task changes a model. Don't trust any "current code
state" notes passed in with the task; other tasks in the same bucket may be landing concurrently.

Also read one or two neighbouring files and note what they already do about the things `reference/` has opinions
on — services vs. fat models, FBV vs. CBV, DRF viewsets vs. `APIView`, factory style, test style (pytest functions
vs. `TestCase` classes), type-annotation density, docstring style. The reference's rules are the default for new
code; an app that consistently does something else wins (README rule 1) — **except on security and data integrity**
(`security.md`, `auth.md`, the migration rules), where new code follows the reference regardless and the
neighbouring problem goes in Step 8's report.

## Step 3 — Implement exactly what the task specifies

The named files, the described model/service/view/serializer/form/command, the behavior. Apply the reference files
from Step 1, plus this repository's own `CLAUDE.md` where it is more specific.

Non-negotiable, because a later gate, a reviewer, or production enforces them:

- **Layering**: views, viewsets, Ninja operations, admin actions, commands, and tasks stay thin and call one
  service function or QuerySet method; business rules that span models or have side effects live in
  `services.py` under `@transaction.atomic`, with side effects (email, task enqueue, cache invalidation, HTTP) in
  `transaction.on_commit(...)`. No business rules in signals, templates, or `save()` overrides.
- **Every input through a form, serializer, or schema with explicit fields** — never `fields = "__all__"` or
  `exclude`, never `request.POST[...]`/`request.data[...]` passed straight to the ORM. Owner/author/`is_staff`
  fields are set server-side.
- **Every query that returns user-visible rows is scoped** to the requesting user where the data isn't public
  (`get_queryset()`, `get_object_or_404(<scoped qs>, …)`, a `visible_to(user)` QuerySet method) — other users'
  rows are a 404, not a 403 and not a leak.
- **No N+1**: `select_related("<named fields>")` / `prefetch_related(...)` wherever a list touches a relation,
  and a query-count assertion in the test (`testing.md`).
- **Type annotations on everything new**, valid for the project's checker (`code-style.md`'s django-stubs notes),
  and a docstring on every new public module, class, function, and method in the project's convention.
- **No new dependency, no settings-module restructuring, no `pyproject.toml`/`pytest.ini`/`mypy` config edit** unless
  the task explicitly calls for it — a blocker to report (Step 4), not a decision to make quietly. Adding the app's
  own entry to `INSTALLED_APPS` or a `path()` to the root URLconf is fine when the task creates the app/route.
- **No debugging leftovers** (`print`, `breakpoint()`, `pdb`, `import ipdb`) and no commented-out code.

**Migrations** — when the task adds, changes, renames, or removes a model, field, relation, constraint, index, or
`Meta.ordering`/`choices`-affecting option:

```bash
<run> python manage.py makemigrations <app_label> --name <descriptive_snake_case> --settings=<test settings>
<run> python manage.py makemigrations --check --dry-run --settings=<test settings>   # must print "No changes detected"
```

Use the test settings (they need no secrets and no database server; `makemigrations` only warns if it can't reach
one). Then **read the generated file**: a rename that came out as `RemoveField` + `AddField` loses data (re-run and
answer the rename prompt — `--noinput` answers "no"); a non-nullable field added to a populated table needs the
nullable → backfill (`RunPython` with a reverse) → non-null sequence (`models-and-orm.md`). **Never edit or delete a
migration that may already be applied anywhere** — fix forward with a new one. Hand-write only data migrations
(`makemigrations <app_label> --empty --name …`, then fill in `RunPython(forward, reverse)` using
`apps.get_model()`). If `makemigrations` reports a **conflict** (two leaf nodes — usually a sibling task in the same
app), stop and report it rather than running `--merge`; the group serializes such tasks.

If `makemigrations` can't run at all (settings import fails, missing environment variable, no interpreter), don't
hand-write a schema migration: report the task as blocked with the error.

Format only the files you touched with the project's formatter when one is configured (`<run> ruff format <files>`
or `<run> black <files>`) and, if Ruff is configured, look at `<run> ruff check <files>` and fix what it reports by
hand — never `--fix` across the project, never the whole tree.

**UI** — when the task adds or changes a screen, component or list: decompose it first (`ui-contract.md` §2 —
screens, regions, components, each component's inputs/events/states, existing partials reused) and keep the
`Screen › Region › Component` tree for Step 8; build leaves first (inclusion tags/partials), then the page template,
then the URL; lists are paginated with one item partial per row (`ui-implementation.md` §4), never an unbounded
loop over a queryset.

Don't add anything the task didn't ask for — no speculative abstraction, no repository layer over the ORM, no
unrelated cleanup, no restyling of code the task doesn't touch.

## Step 4 — When to interrupt the user

Keep interruptions rare — most tasks should complete unattended. Stop and use `AskUserQuestion` (or plain text if no
real choice is being offered) only when:

- The task is ambiguous in a way that changes correctness or scope and can't be safely inferred — in particular
  **who may call a new endpoint or view** (public, any authenticated user, owner only, staff, a named permission),
  or what happens to existing rows when a field becomes required.
- The described approach is infeasible against the real code (it names a model, app, URL name, or setting that
  doesn't exist and isn't a trivial typo), or needs a new dependency, a settings restructure, or a test-infrastructure
  change (testcontainers, a new pytest plugin) the task didn't ask for.
- **The task as written would require insecure or data-losing code** — `fields = "__all__"` on user input,
  `csrf_exempt` on a browser view, an unscoped detail endpoint over private data, raw SQL built with f-strings,
  `mark_safe` on user input, editing an applied migration, a destructive rename without a data path. Report it with
  the safe alternative; don't implement the unsafe version, and don't silently implement something different.
- Step 1's detection is genuinely ambiguous in a way that changes the code you'd write (two settings modules that
  disagree on `AUTH_USER_MODEL`, an app installed under two labels, DRF and Ninja both serving the touched app).

Don't stop merely because the task is nontrivial — implement it. Don't report the task done to work around a
blocker; report it as blocked (Step 8) with what was tried, what failed, and why.

## Step 5 — Write or update the tests

Follow `reference/testing.md` and the existing tests next to the touched code — runner (pytest-django functions or
`TestCase` classes), factories, fixtures, naming. Cover the new behavior, every exception a service documents in
`Raises:`, the validation-failure path of anything taking input, the **unauthorized paths** (anonymous, wrong user →
404/403/302, wrong method → 405), and a query-count assertion on every list the task adds or changes. Side effects
deferred with `on_commit` are asserted with `django_capture_on_commit_callbacks(execute=True)` /
`self.captureOnCommitCallbacks(execute=True)`.

**UI tests** — for a screen, component or list the task added or changed, also write the browser UI tests of
`ui-implementation.md` §5–§7 in `tests/ui/` (`ui` marker, `live_server`): every applicable visual state with the
minimal/typical/many-items data sets, events and HTMX swaps asserted once (ltr, light), and a capture per state ×
`.ui-quality.yml` direction × theme through `tests/ui/ui_screenshots.py` (`capture_ui_state`), with
`check_accessibility(page)` after each capture. Create the helper from `ui-implementation.md` §6 if the project has
pytest-playwright but no helper yet; if pytest-playwright/axe-playwright-python aren't dependencies, write the
template-rendering unit tests only and report the missing UI-test wiring (Step 4 — a dependency change).

Put each test in the tier that matches what it needs: anything that needs PostgreSQL-only behavior
(`select_for_update` semantics, `contrib.postgres` fields, full-text search, real constraint races), Redis, Celery,
a live server, or a browser carries the project's integration marker/tag and goes where the project keeps those
tests. Never make a fast test depend on Docker.

If the project has no test setup at all, don't scaffold one — that's a plan-level decision. Write nothing, and say
so in Step 8 so the group's coverage-gate failure has an explanation.

## Step 6 — Run only the fast tests this task touched

Run the fast test files you wrote or changed, scoped by path — nothing more:

```bash
# pytest-django
<run> pytest apps/catalog/tests/test_services.py apps/catalog/tests/test_api.py -m "not integration" -p no:randomly
# add --no-cov when the project's addopts includes --cov (otherwise a scoped run trips fail_under)
# built-in runner (dotted labels, the project's test settings, integration tag excluded)
<run> python manage.py test apps.catalog.tests.test_services --settings=<test settings> --exclude-tag=integration --noinput
```

(`-p no:randomly` only when `pytest-randomly` is installed; use whatever marker/tag name Step 1 found in place of
`integration`.) If Step 1 found that the test settings need a database server for every `django_db` test, run only
the files that need no database, and leave the rest to the group — say so in Step 8.

**Never run, by any means:** the integration marker/tag, anything that starts Docker or testcontainers or connects
to PostgreSQL/MySQL/Redis, a live-server or Playwright/Selenium test (the `ui` marker — add `and not ui` to the
`-m` expression when the project has it), coverage (`--cov` reports, `coverage run`),
`-n`/`--parallel`, the whole suite (a bare `pytest` or `manage.py test` with no labels), `mypy`/`pyright`, or the
Django system checks. Several of these agents run concurrently; the integration tier is serialized behind the
group's lock, and everything else is validated once per bucket.

If a test fails, fix the implementation or the test and re-run until green — don't hand back a red test. If the
behavior genuinely can't be verified without the integration tier, write that test (unrun), write whatever fast test
*is* meaningful, and say so in Step 8. Never delete an assertion to make a file pass. If no usable interpreter or
environment exists (no `.venv`, lock not synced), skip the run and say so — the group runs the tests anyway; don't
run `uv sync`/`poetry install` here.

## Step 7 — Check off this task's checkbox now

If this task did not stop on a blocker (Step 4), update `implementation_plan.md` at the repository root before
reporting back. Re-read the file fresh (other tasks in the same bucket may be landing concurrently), locate this
task's own checkbox line by the exact text passed in with the task, flip `[ ]` to `[x]` for it and for every
sub-task covered by the work just completed, and add a short note naming the files touched, e.g.:

```
- [x] Task 2. **Add `reserve_copies` service and `POST /api/v1/books/{id}/reserve/`** — apps/catalog/services.py,
  apps/catalog/api/views.py, migration 0004_book_reserved_copies; pytest-django tests added (passing); group
  validation pending.
```

The "group validation pending" wording is what `iru-django-code-one-task-group` replaces with the final outcome.
Edit only this task's own line(s) — never surrounding lines or other tasks' checkboxes.

If this task stopped on a blocker, leave its checkbox untouched.

## Step 8 — Report the outcome

Hand control back to the caller with a short summary:

- **The shape Step 1 detected** — runner prefix, Django version, test settings module, app layout and the touched
  app labels, API style, test runner and data builders, fast/integration split, type checker — and the reference
  files actually read.
- **The files touched**, including settings, URLconf, and `INSTALLED_APPS` edits, and **every migration generated**
  (name, whether it was auto-generated or a hand-written data migration, and anything you checked in it — a rename,
  a three-step non-null addition).
- **The tests added/updated**, split into fast tests (with Step 6's result, or why they weren't run) and
  integration tests (written, not run — the group runs them).
- **For UI work**: the `Screen › Region › Component` tree from Step 3, and the UI tests written (not run — the group
  runs `ui` behind the lock) with the screenshot `<kind>/<Id>` entries and states they will capture, or why none
  could be written (missing pytest-playwright/axe-playwright-python, no RTL language configured).
- **Whether this task stopped on a blocker** per Step 4, with enough detail for the caller to surface it.
- **Any deliberate deviation from `reference/`** (a `TestCase` class to match the app, a fat model method the app
  already uses, no type annotations in an untyped codebase), and any **insecure or N+1 neighbouring code** noticed
  and left alone — or say so if `reference/` was missing (Step 1), the runner prefix was a guess, or the project had
  no test setup (Step 5).

This skill has already checked off its own checkbox with a pending-validation note (Step 7). It never captures a
quality baseline, adds license headers, audits docstrings, runs coverage, mypy, the Django system checks, the full
suite, or any integration test.
