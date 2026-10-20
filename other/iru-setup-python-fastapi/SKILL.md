---
name: iru-setup-python-fastapi
description: >-
  Scaffold a new FastAPI service with uv (`uv init --bare` + `uv add` with the pinned ranges of the author's docs:
  `fastapi[standard]>=0.142.2,<0.143.0`, Pydantic 2, pydantic-settings, SQLModel or plain SQLAlchemy 2.0 async on
  asyncpg/aiosqlite, Alembic), or bring an existing FastAPI service up to this catalog's toolchain, then lay down a
  real, tested skeleton: the layered `app/` package (`main.py` app factory + lifespan, `settings.py` with
  `env_prefix="APP_"` and `SecretStr`, `dependencies.py` `Annotated` aliases, `db.py`, `routers/`, `services/` with a
  `Protocol` port, `data/` adapters, `models/`), `/healthz` + `/readyz`, one sample CRUD resource (router → service →
  repository) with fast tests on in-memory SQLite and a testcontainers PostgreSQL integration tier
  (`@pytest.mark.integration`), Alembic with an async `env.py`, a naming convention and a reviewed initial
  revision, optional PyJWT + pwdlib[argon2] auth, `scripts/export_openapi.py`, Sphinx API docs sources in
  `docs/api/`, a multi-stage non-root uv `Dockerfile` + `.dockerignore` + `compose.yaml` (postgres:18, one-shot
  `migrate`, app), `.env.example`, `sonar-project.properties` when Sonar is enabled, and every tool config in
  `pyproject.toml` (Ruff, mypy strict + pydantic plugin, pytest markers, coverage 80% with XML at
  `build/coverage/coverage.xml`) exactly as the Python scaffold contract the `iru-python-*` gates and
  `iru-setup-python-github-workflows` rely on. Invoke as `/iru-setup-python-fastapi`. Accepts pre-resolved inputs via
  `args` (`key: value` lines) — `name`, `package`, `description`, `license`, `developer-name`, `developer-email`,
  `organization-url`, `python-version`, `database` (`postgresql`/`sqlite`/`none`), `orm` (`sqlmodel`/`sqlalchemy`),
  `auth` (`yes`/`no`), `open-source`, `visibility`, `ci`, `distribution`, `sonar` (+ `sonar-organization`/
  `sonar-project-key`/`sonar-host-url`), `mode` (`new`/`existing`), `on-existing` (`ask`/`keep`/`update`/`replace`)
  — so `iru-setup-python-repository` can drive it without re-prompting; stand-alone it asks whatever `args` didn't
  resolve. Announces whether it is scaffolding from scratch or updating an existing service and, for every artifact
  it owns that already exists, warns and asks Update / Keep as is / Replace (or Stop). Ends by running the contract's
  canonical commands (uv sync, ruff, mypy, fast + integration pytest, coverage, Alembic checks, Sphinx, OpenAPI
  export, uv build, docker build). Use whenever a repository needs a FastAPI service bootstrapped with its full
  test/lint/type/migration/container toolchain from this house template, instead of wiring it by hand.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(uv *) Bash(uvx *) Bash(docker *) Bash(curl *) Bash(python3 *) Bash(openssl *) Bash(git *) Bash(gh repo view *) Bash(mktemp *) Bash(mv *) Bash(cp *) Bash(rm *) Bash(mkdir *) Bash(touch *) Bash(ls *) Bash(find *) Bash(grep *) Bash(cat *) Bash(test *) Bash(command -v *) Bash(head *) Bash(date *) Bash(sleep *)
---

# Setup Python FastAPI

Scaffold a FastAPI service with uv, then layer on this catalog's Python toolchain and a small, real, tested
application: validated settings, a lifespan-owned database engine, health probes, one sample resource through every
layer, Alembic migrations, fast and container-backed test tiers, API docs sources, a production container image, and
Sonar configuration. Everything in this skill and its `reference/` files was rendered into throwaway projects and
proven against the real tooling (2026-10-14: uv 0.12.8, CPython 3.13.15, FastAPI 0.142.4, Starlette 1.8, Pydantic
2.14, SQLModel 0.0.47, SQLAlchemy 2.0.54, Alembic 1.20, pytest 9.1, testcontainers 4.15, Ruff 0.17, mypy 2.4, Sphinx
9.1, Docker 29.8, PostgreSQL 18) — the gotchas called out inline are observed behavior. See **Verification notes**.

The generated code is the **first exemplar** of what `iru-fastapi-code-one-task` enforces (web → service → data
layering, `Annotated` dependencies, the SQLModel model family, one transaction per request, domain errors mapped in
`main.py`, Alembic for every schema change), and the commands, paths and markers are the **scaffold contract** that
`iru-python-test`/`-coverage`/`-code-quality`/`-docstrings`/`-bump-version` and `iru-setup-python-github-workflows`
detect and call.

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/tooling-templates.md` | **Always.** The `uv` commands, the verified `pyproject.toml` (+ per-shape diffs), `scripts/export_openapi.py`, `docs/api/conf.py` + `index.rst`, `.env.example` per shape. |
| `reference/app-templates.md` | **Always.** Every `app/` module and every fast test of the default shape. |
| `reference/persistence-templates.md` | **Always.** Alembic + the integration tier (`database: postgresql`/`sqlite`), and the file replacements for `orm: sqlalchemy`, `database: sqlite`, `database: none`. |
| `reference/auth-templates.md` | Only with `auth: yes`. |
| `reference/docker-and-sonar.md` | **Always** (the `Dockerfile` is always written); its Sonar section only when `sonar` ≠ `none`. |

## Step 0 — Resolve inputs

Invoked stand-alone (`/iru-setup-python-fastapi`) or by `iru-setup-python-repository`, which passes resolved answers
through `args` as `key: value` lines, one per line, e.g.:

```
name: orders-api
package: orders_api
description: Order management API.
license: MIT
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
python-version: 3.13
database: postgresql
orm: sqlmodel
auth: no
open-source: yes
visibility: public
ci: yes
distribution: internal
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_orders-api
sonar-host-url: https://sonarcloud.io
mode: new
on-existing: ask
```

Parse any such lines now; every key found is resolved — never ask it again. If `args` is absent or not in this
format, treat everything as unset.

Recognized keys:

- **Identity**: `name` (the distribution name in `[project].name`, lowercase kebab-case; also the image name and
  what `importlib.metadata.version()` looks up), `package` (snake_case identifier — the code itself always lives in
  the `app/` package per the docs' layout, so `package` is only used for the Compose project/database names and as
  a fallback title; accept and validate it, don't create a second package), `description`, `license` (SPDX id or
  display name — MIT License → `MIT`, Apache License 2.0 → `Apache-2.0`, No license → omit the `license` key and say
  so), `developer-name`, `developer-email`, `organization-url` (→ `[project].authors` and `[project.urls]`).
- **Shape (this skill)**: `python-version` (default `3.13`; `requires-python` stays `>=3.12`), `database`
  (`postgresql`/`sqlite`/`none`, default `postgresql`), `orm` (`sqlmodel`/`sqlalchemy`, default `sqlmodel`; ignored
  with `database: none`), `auth` (`yes`/`no`, default `no`).
- **Shared pipeline vocabulary**: `open-source` (`yes`/`no`), `visibility` (`public`/`private`/`internal` — only
  keys the Sonar recommendation), `ci` (`yes`/`no` — only consulted by the Sonar question), `distribution`
  (`none`/`internal`/`store` — recorded for the report only: the `Dockerfile` is written in every case and
  `iru-setup-python-github-workflows` decides what is pushed), `sonar` (`cloud`/`self-hosted`/`none`) plus, only when
  `cloud`/`self-hosted`, `sonar-organization`/`sonar-project-key`/`sonar-host-url`, `mode` (`new`/`existing`),
  `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask`, for scripted runs).

Ignore any other key (`ci-tests`, `pages`, `publish`, `integration-branch`, `stable-branch`, `api`, `flavor` — an
orchestrator may send its whole vocabulary). `mode: existing` marks an **update** run but never means "update
silently": Step 1 still warns and asks per pre-existing artifact unless `on-existing` says otherwise.

## Step 1 — Survey the repository

- If `mode` wasn't supplied, derive it: a root `pyproject.toml` ⇒ `existing`, else `new`. Don't ask it.
- **Classify an existing `pyproject.toml`**: `fastapi` among its dependencies (or `requirements*.txt`, or an
  `app/main.py`/`src/*/main.py` creating `FastAPI(`) ⇒ an **existing FastAPI service** — no `uv init`; later steps
  merge into it. Read its layout (`app/` package vs `src/<pkg>/` vs the Full Stack template's `app/api/` +
  `app/core/`), its persistence (`sqlmodel`/`sqlalchemy`/`alembic.ini`), its runner (`uv.lock` / `poetry.lock` /
  `pdm.lock` / `Pipfile.lock` / plain pip) and fix `database`/`orm`/`auth` from what is there, telling the user when
  that disagrees with `args`. **Never move existing code into the `app/` layout** — adapt paths (`[tool.coverage.run]
  source`, Sphinx automodules, `Dockerfile` `COPY`, `[tool.fastapi] entrypoint`) to the real package instead.
  A non-uv runner: say this skill's commands are uv-based, and ask **Adopt uv** (convert dev extras to
  `[dependency-groups]`, `uv lock`, keep the other tool's files until the user removes them) / **Stop**. Anything
  else with a `pyproject.toml` (Django, a library, Flask) ⇒ stop and say so (suggest `iru-setup-python-repository`
  to pick the right flavor); never `uv init` over another project.
- **Survey every artifact this skill owns**: `pyproject.toml` (`[project]` metadata/version, `[build-system]`, the
  dependency groups, `[tool.fastapi]`, `[tool.ruff*]`, `[tool.mypy]`/`[tool.pydantic-mypy]`,
  `[tool.pytest.ini_options]`, `[tool.coverage.*]`), `uv.lock`, `.python-version`, the `app/` package (`main.py`,
  `settings.py`, `db.py`, `dependencies.py`, `routers/`, `services/`, `data/`, `models/`, `security.py`), the sample
  resource (`app/routers/books.py` and siblings), `tests/` (`conftest.py`, `fakes.py`, `unit/`, `integration/`),
  `alembic.ini` + `migrations/` (`env.py`, `script.py.mako`, `versions/`), `scripts/export_openapi.py`,
  `docs/api/conf.py` + `docs/api/index.rst`, `Dockerfile`, `.dockerignore`, `compose.yaml`/`docker-compose.yml`,
  `.env.example`, `sonar-project.properties`.
- **Announce the mode** before asking anything else:
  - **Nothing owned exists**: "Scaffolding the FastAPI service **from scratch**."
  - **Anything owned exists** (or `mode: existing`): "**Updating an existing setup** — found: <list with paths>
    (FastAPI <version from uv.lock or the installed package>, layout <app/ | src/<pkg>/ | full-stack template>,
    runner <uv | poetry | ...>)." Warn that each will be handled individually, then resolve one action per artifact:
    - **`on-existing` is `keep`/`update`/`replace`**: apply it to every artifact without asking (still print the
      warning). Exception: `replace` never regenerates existing application source or tests (see below) — treat
      them as `keep` and say so.
    - **Otherwise**: ask with `AskUserQuestion`, up to 4 artifacts per call (one question each), naming concrete
      contradictions with this run's choices in the question (e.g. "`[tool.coverage.xml]` writes `coverage.xml` at
      the root — the gates and Sonar read `build/coverage/coverage.xml`", "no `integration` marker — the workflows'
      integration job selects `-m integration`", "`main.py` uses `@app.on_event` — the templates use a lifespan",
      "`alembic.ini` hard-codes `sqlalchemy.url` with a password", "a `sonar-project.properties` exists but you chose
      `sonar: none`"):
      - **Update (Recommended)** — merge: add what's missing and correct what this skill owns (tool sections and
        their contract values, missing dev/docs dependencies via `uv add`, the coverage XML path, the
        `.dockerignore` entries, the `env.py` URL source), keeping everything else. Show the diff; customizations
        survive, but a customized part this skill owns may be rewritten.
      - **Keep as is** — leave it untouched and skip the steps that only serve it. It may stay out of date or
        disagree with this run's choices — Step 15 lists each mismatch.
      - **Replace** — regenerate from the template; customizations are lost (recoverable only from git history).
        **Not offered for application source, tests, or applied migrations** (`app/**`, `tests/**`,
        `migrations/versions/**`) — that is real code once the project exists; recommend **Keep as is** and say why.
      - **Stop** (first batch only) — end without changing anything; report that and end here.
    - Never add the sample resource to an **existing** service unless the user asks — on the update path it would be
      dead code. Ask once: "Add the `books` sample resource as a reference?" (default **No**).
    - Ask about `sonar-project.properties` only after Step 2 resolves `sonar`: with `sonar: none`, Update/Replace
      mean removing the file and Keep leaves it as a reported mismatch.
- **Placement** (new service): the repository root. Other files (docs, CI, `README.md`, `LICENSE`, `.git`,
  `CLAUDE.md`) are fine — `uv init --bare` only writes `pyproject.toml`. If the root holds something that looks like
  another application (`src/`, `app/`, `manage.py`, `package.json`), ask whether to scaffold into the root anyway or
  into a subdirectory named `<name>`.

## Step 2 — Collect identity and options

For every key Step 0 resolved, use it. In `mode: existing`, read identity from `[project]` (`name`, `description`,
`license`, `authors`, `urls`) and confirm it in one line instead of asking. Otherwise ask (plain conversation for free
text, `AskUserQuestion` for bounded choices):

1. **name** (default: the repository directory's basename, lowercased, kebab-cased), **package** (derived:
   `name` with `-` → `_`; confirm only — must be a legal identifier and not `app`, `fastapi`, `pydantic`, `test`, or
   a stdlib module), **description**, **developer name/email**, **organization URL** (default from
   `git remote get-url origin`).
2. **license** — **MIT (Recommended)** "FastAPI's own license" / **Apache-2.0** / **No license (proprietary)** — omit
   `[project].license` / **Other** (ask the SPDX id). Remind in Step 15 to add a `LICENSE` file if missing.
3. **python-version** — **3.13 (Recommended)** "what the author's docs run and CI images use" / **3.14** "newest;
   check every dependency has wheels" / **3.12** "the floor (`requires-python = ">=3.12"`)". Use only a version `uv
   python list` can provide (Step 3).
4. **database** — **PostgreSQL (Recommended)** "async SQLAlchemy engine on asyncpg; fast tests on in-memory SQLite,
   the integration tier on a real PostgreSQL via testcontainers" / **SQLite** "aiosqlite file database — a single
   host and writer; no integration tier" / **None** "no persistence layer: an in-memory adapter behind the same
   repository port, no ORM, no Alembic".
5. **orm** (only when `database` ≠ `none`) — **SQLModel (Recommended)** "the FastAPI docs' default: one class family
   for table + validation + OpenAPI" / **SQLAlchemy 2.0** "`DeclarativeBase` + `Mapped` with separate Pydantic
   schemas — full typing, no SQLModel coupling".
6. **auth** — "Add a sample bearer-token login protecting the write endpoints (PyJWT + pwdlib/Argon2, one admin
   account from settings)?" **No (Recommended)** "add real auth when the product decides on an identity provider" /
   **Yes**.
7. **open-source**, then **sonar** — "Configure SonarCloud / SonarQube for this project?". Resolve `visibility`
   only now if missing (`gh repo view --json visibility -q .visibility`, lowercased; else ask Public/Private —
   `internal` counts as private). If `open-source: yes` but private/internal, flag the contradiction and ask which is
   right. Recommend **SonarCloud** (`cloud`) only for a public open-source repository; otherwise say SonarCloud is
   free only for public open-source projects and recommend **None**, offering **self-hosted** second. With
   `ci: no`, say no CI workflow would send reports and recommend **None**; if the user still picks one, write the
   properties file anyway and say so in Step 15. For `cloud` ask `sonar-organization` (suggest `<owner>-github`) and
   `sonar-project-key` (suggest `<owner>_<repo>`), host `https://sonarcloud.io`; for `self-hosted` ask the host URL,
   the organization only if the server uses them, and the project key.
8. **distribution** — only recorded for the report (Step 0). Don't ask it stand-alone.

Derive `<title>` (the human title used in `FastAPI(title=...)` and the Sphinx project) from `name`
(`orders-api` → "Orders API"); confirm it in one line.

## Step 3 — Toolchain and versions

- **uv**: `command -v uv && uv --version`. Missing → tell the user to install it
  (<https://docs.astral.sh/uv/getting-started/installation/>) and stop; never `pip install` into a system Python.
- **Python**: `uv python find <python-version>` or `uv python install <python-version>` (verified: installs
  CPython 3.13 in seconds; nothing system-wide changes).
- **Versions**: the `uv add` ranges in `reference/tooling-templates.md` are the digest's pins and were verified —
  use them as written. Look up the latest releases only to report drift
  (`curl -s https://pypi.org/pypi/<pkg>/json | python3 -c 'import json,sys; print(json.load(sys.stdin)["info"]["version"])'`):
  if FastAPI has moved past the pinned minor (0.143.x existed at verification time), say so in the report and leave
  the upgrade to a deliberate follow-up (FastAPI is 0.x — breaking changes land in minors). Never pin Starlette.
- **uv image tag** for the `Dockerfile`: the latest `uv` release from the same PyPI lookup (verified
  `ghcr.io/astral-sh/uv:0.13.1`); fall back to `0.13.1` offline. Record live vs fallback for the report.
- **Docker**: `docker info >/dev/null 2>&1` — needed only for Step 14's integration tier, Alembic check against
  PostgreSQL, and image build; without it those are reported **unverified**, never passed.

## Step 4 — Project manifest with uv

**New service**: run the commands in `reference/tooling-templates.md` ("`uv` commands") in order — `uv init --bare`,
`uv python pin`, then edit `[project]` (`version = "0.1.0.dev0"`, `license`, `authors`, `requires-python =
">=3.12"`, `[project.urls]`) and add `[build-system]` (`uv_build`) + `[tool.uv.build-backend]` (`module-name =
"app"`, `module-root = ""`) **and create `app/__init__.py` before the first `uv add`** (gotcha, verified: `uv add`
builds the project and fails with `Expected a Python module at: app/__init__.py`). Then the three `uv add` calls
for the run's shape. Don't add `readme = "README.md"` unless a README already exists (`uv_build` fails on a missing
readme; `iru-setup-readme` writes it later).

**Existing service** (Update): `uv add` only what's missing from the same lists (respecting ranges the project
already pins — report conflicts instead of overriding them), keep its build backend, and set `version` only if it
has none (`0.1.0.dev0`; a version already present is never touched — `iru-python-bump-version` owns it).

The version's single source is `[project].version`; the app reads it with `importlib.metadata.version("<name>")`
(`app/__init__.py`). Development versions are PEP 440 `X.Y.Z.dev0`.

## Step 5 — Tool configuration (all in `pyproject.toml`)

Append the tool sections from the verified `pyproject.toml` in `reference/tooling-templates.md`, applying its
per-shape diff:

- `[tool.fastapi] entrypoint = "app.main:app"`.
- `[tool.ruff] line-length = 88` (Ruff/Black's default — `ruff format` output with no config; PEP 8's 79 is prose
  advice in the docs, 88 keeps formatter and linter in agreement), `[tool.ruff.lint] select = ["E", "F", "W", "I",
  "N", "UP", "B", "S", "C4", "SIM", "RUF", "D", "PT", "ASYNC", "FAST"]`, `pydocstyle.convention = "google"`,
  per-file-ignores `tests/** = ["S101", "D"]`, `migrations/versions/** = ["D"]`.
- `[tool.mypy] strict = true`, `plugins = ["pydantic.mypy"]` (+ `[tool.pydantic-mypy]`); `uv run mypy .` checks
  `app/`, `tests/`, `migrations/`, `scripts/` and `docs/api/conf.py` (all verified clean).
- `[tool.pytest.ini_options]` `addopts = "-ra --strict-markers --strict-config"`, `testpaths = ["tests"]`,
  `markers = ["integration: needs Docker (testcontainers)"]`, `filterwarnings = ["error::DeprecationWarning"]`.
- `[tool.coverage.run] branch = true, source = ["app"], concurrency = ["greenlet", "thread"]` (the concurrency line
  only with a database — gotcha in the tooling reference), `[tool.coverage.report] fail_under = 80, show_missing =
  true` (the author's docs use 90 — offer it as a ratchet, the catalog gate is 80), `[tool.coverage.xml] output =
  "build/coverage/coverage.xml"`.

An existing service with another layout: point `source` at its real package; keep its own stricter settings (a
higher `fail_under`, more Ruff rules) and only add what the contract needs.

## Step 6 — Application skeleton

Write the `app/` package from `reference/app-templates.md` (new service, or an existing one only for files that are
absent and the user wants): `__init__.py`, `settings.py` (`DatabaseSettings` with `APP_DATABASE_URL` as a required
`SecretStr`, `Settings(DatabaseSettings)`, `@lru_cache get_settings`), `db.py`, `models/` (naming convention, the
SQLModel `Book` family, `HealthStatus`), `services/` (`errors.py`, `ports.py`, `books.py`), `data/books.py`,
`dependencies.py`, `routers/health.py` + `routers/books.py`, `main.py` (`create_app()` + module-level `app`,
lifespan, exception handlers). Replace the placeholders as that file's header says; rename the sample resource only
if the user asked for a different first resource. Apply the shape's replacements from
`reference/persistence-templates.md` (`orm: sqlalchemy`, `database: none`).

## Step 7 — Persistence (`database` ≠ `none`)

From `reference/persistence-templates.md`: run `uv run alembic init -t async migrations` (new service), then replace
`alembic.ini`, `migrations/env.py` and `migrations/script.py.mako` with the templates, delete `migrations/README`,
and write `migrations/versions/0001_create_book_table.py` verbatim (`Create Date` = today) — no database is needed to
write it; Step 14 proves it matches the models. An existing service that already has Alembic: never touch applied
revisions; Update only `env.py`'s URL source (settings instead of a literal URL), `compare_type=True`, and the
`render_as_batch` line, and add the post-write hooks to `alembic.ini`. Schema changes always ship as reviewed
revisions; nothing calls `create_all` outside tests, and the app never migrates at start-up.

## Step 8 — Auth (`auth: yes`)

From `reference/auth-templates.md`: `uv add "pyjwt>=2.15,<3" "pwdlib[argon2]>=0.3,<0.4"`, write `app/security.py`,
`app/models/auth.py`, `app/routers/auth.py`, the auth versions of `settings.py`, `dependencies.py`,
`routers/books.py`, the test files, and apply its small diffs (`models/__init__.py`, `main.py`, `docs/api/index.rst`,
`compose.yaml`, `.env.example`). Never commit a real secret or hash; `.env.example` carries placeholders.

## Step 9 — Tests

From `reference/app-templates.md` (and the shape's replacements): `tests/__init__.py`, `tests/unit/__init__.py`
(empty), `tests/conftest.py`, `tests/fakes.py`, `tests/unit/test_*.py`; with `database: postgresql` also
`tests/integration/__init__.py`, `tests/integration/conftest.py` and `test_books_postgres.py` from the persistence
reference — one `postgres:18-alpine` container per test session via `testcontainers.community.postgres` (gotcha,
verified: the old `testcontainers.postgres` path emits a `DeprecationWarning` that the strict `filterwarnings` turns
into a collection error on testcontainers 4.15), migrated with `alembic.command.upgrade`, the real app driven through
`asgi_lifespan.LifespanManager`, and a `compare_metadata(...) == []` test. Every integration test carries
`pytest.mark.integration` and lives under `tests/integration/` — both signals the gates use.

## Step 10 — OpenAPI export and Sphinx API docs

Write `scripts/export_openapi.py`, `docs/api/conf.py` and `docs/api/index.rst` from
`reference/tooling-templates.md` (one `.. automodule::` per module of the run's shape; the `autodoc-skip-member`
hook in `conf.py` is required — see that file's gotcha). Never create or edit `docs/antora.yml`,
`docs/antora-playbook.yml` or `docs/modules/` — `iru-setup-antora` owns them; the Sphinx output goes to
`build/api-docs/` and the workflows publish it under the site's `api/`.

## Step 11 — Container image, local stack, `.env.example`

Write `Dockerfile`, `.dockerignore`, `compose.yaml` (`database: postgresql`/`sqlite` — none for `database: none`)
from `reference/docker-and-sonar.md` and `.env.example` from the tooling reference, with `python:<python-version>-slim`
and the uv tag from Step 3. Written for every run — `distribution` only decides what the workflows push. An existing
`Dockerfile` that runs migrations in its `CMD`/entrypoint, runs as root, or uses shell-form `CMD`: name it in the
Step 1 question rather than fixing it silently.

## Step 12 — `sonar-project.properties`

Only when `sonar` is `cloud`/`self-hosted`: write it from `reference/docker-and-sonar.md` (`sonar.python.version`,
coverage `build/coverage/coverage.xml`, xunit `build/test-results/pytest*.xml`, Ruff `build/reports/ruff.json`).
With `sonar: none`, write nothing (and handle an existing file per Step 1).

## Step 13 — Lock, format, lint-fix

```bash
uv lock && uv sync --locked
uv run ruff format .
uv run ruff check --fix .
```

The templates are already formatted; this catches placeholder substitutions that changed line lengths (fix any
remaining `E501` by rewording, never by raising `line-length`). In an existing service, run `ruff format --check .`
first and ask before reformatting files this skill didn't write (suggest a separate "apply Ruff format" commit).

## Step 14 — Verify with the contract's canonical commands

Run, in order, and fix anything this skill wrote until green — never "fix" pre-existing application code to make a
gate pass; report it instead:

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest -m "not integration" --cov --cov-report=xml --cov-report=term-missing \
  --junitxml=build/test-results/pytest.xml                     # coverage ≥ 80% (fail_under) from these tests only
uv run --group docs sphinx-build -W --keep-going -b html docs/api build/api-docs
uv run python scripts/export_openapi.py build/api-docs/openapi.json
uv build                                                       # sdist + wheel into dist/
```

Then, only when Docker is reachable (otherwise mark each **unverified** — never skip silently):

```bash
uv run pytest -m integration --junitxml=build/test-results/pytest-integration.xml   # database: postgresql
# Alembic against a throwaway PostgreSQL (database: postgresql), exactly what CI's migrations job runs:
docker run -d --rm --name <name>-verify-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=app -p 127.0.0.1::5432 postgres:18
PORT="$(docker port <name>-verify-db 5432 | head -1 | cut -d: -f2)"   # wait for pg_isready first
APP_DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:$PORT/app" sh -c \
  'uv run alembic upgrade head && uv run alembic check && uv run alembic heads && uv run alembic downgrade base && uv run alembic upgrade head'
docker rm -f <name>-verify-db
docker build -t <name>:verify .
```

- `database: sqlite`: run the same Alembic sequence with `APP_DATABASE_URL=sqlite+aiosqlite:///build/alembic-check.db`
  (no Docker needed); there is no integration tier (`pytest -m integration` exits 5 — "no tests collected" — which
  is expected, not a failure).
- `database: none`: no Alembic, no integration tier.
- With Docker, smoke-test the image as in `reference/docker-and-sonar.md`: database container on a user network,
  `alembic upgrade head` from the image, then the app — `docker inspect` health `healthy`, `/readyz` → `200`, one
  `POST /api/v1/books` → `201`; remove everything you started. `auth: yes` also passes `APP_JWT_SECRET` and
  `APP_ADMIN_PASSWORD_HASH` at run time.
- Expected on a new default-shape service (verified): Ruff clean, 35 files formatted, mypy strict clean on 35 files,
  33 fast tests passed at 100% coverage, 4 integration tests passed, `alembic check` "No new upgrade operations
  detected." with one head, Sphinx built with 0 warnings, OpenAPI 3.1.0 exported, wheel + sdist built, image built.

Remove nothing the gates produce under `build/` (ignored); delete `dist/` only if the user prefers.

## Step 15 — Report

Start with the mode (**scaffolded from scratch** or **updated an existing setup**) and the location. Then:

- Per owned component, the action actually taken — **created / updated / replaced / kept as is / removed /
  skipped** — for: `pyproject.toml`/`uv.lock`/`.python-version`, application sources (`app/`), tests config and
  tests, quality configs (Ruff/mypy/pytest/coverage sections), Alembic (`alembic.ini` + `migrations/`), Sphinx API
  docs sources (`docs/api/`), `scripts/export_openapi.py`, `Dockerfile`/`.dockerignore`/`compose.yaml`/
  `.env.example`, `sonar-project.properties`; and for every kept one, each mismatch with this run's choices.
- The resolved shape: `python-version`, `database`, `orm`, `auth`, license, `open-source`, `distribution` (recorded),
  `sonar` (with the `visibility` used and where it came from; if `ci: no` and Sonar was configured, say no CI step
  sends reports).
- Versions: the installed FastAPI/Starlette/Pydantic/SQLModel or SQLAlchemy/Alembic/pytest/Ruff/mypy from `uv.lock`,
  the uv image tag (live or fallback), and any drift past the pins (e.g. a newer FastAPI minor) left for a follow-up.
- Each Step 14 command and its result (tests passed, coverage %, mypy/Ruff counts, `alembic check`, Sphinx
  warnings, image built), plus anything **unverified** and why.
- For the workflows/orchestrator: database URL env var `APP_DATABASE_URL` (driver `postgresql+asyncpg://`, or
  `sqlite+aiosqlite://`), migration commands `uv run alembic upgrade head` / `check` / `heads` / `downgrade base`,
  integration marker `integration` + `tests/integration/`, OpenAPI at `build/api-docs/openapi.json`, Compose services
  `db`/`migrate`/`api`.

Finish with a **Warn explicitly** block:

- Review before committing — `[project]` identity/license/authors and the Sonar keys.
- **Never commit `.env`**; `.env.example`, `uv.lock` and `.python-version` **are** committed. `auth: yes`: keep the
  Argon2 hash single-quoted in `.env`.
- Migrations run once per release as a one-shot job (`compose.yaml` `migrate`, a Kubernetes Job), never at start-up
  or per replica; review every autogenerated revision.
- `database: sqlite` is single-host/single-writer; `database: none` keeps data in one worker's memory — both are
  starting points, not production storage.
- The image runs **one** Uvicorn process: scale with replicas, not `--workers`, under an orchestrator.
- `sonar: cloud`/`self-hosted`: a `SONAR_TOKEN` secret and the Sonar project must exist before CI analysis succeeds.
- No `.gitignore`, workflows, `CHANGELOG.md`, `README.md` or Antora files were written —
  `iru-setup-python-gitignore` (must ignore `build/`, `dist/`, `.venv/`, `.env`, the caches, `.coverage*`),
  `iru-setup-python-github-workflows`, `iru-setup-changelog`, `iru-setup-readme` and `iru-setup-antora` cover them
  (`iru-setup-python-repository` runs them next). Add `readme = "README.md"` to `[project]` once the README exists.
- If a license was chosen and no `LICENSE` file exists, suggest `iru-check-license`.

## Verification notes

Rendered into `$TMPDIR/iru-verify/python/setup-fastapi/` (outside the repository) on 2026-10-14 — uv 0.12.8,
CPython 3.13.15, Docker 29.8.2 — in six projects: the default shape (`postgresql` + `sqlmodel`), `orm: sqlalchemy`,
`auth: yes` on both ORMs, `database: sqlite`, `database: none`. Each passed `uv sync --locked`, `uv lock --check`,
`ruff check .`, `ruff format --check .`, `mypy .` (strict), the fast tier with coverage ≥ 80% (98.6–100%),
`sphinx-build -W`, `export_openapi.py`, `uv build`, and `docker build`. PostgreSQL shapes: integration tier green
(4 tests, ~3.5 s incl. container start) and `alembic upgrade head` / `check` / single head / `downgrade base` /
`upgrade head` green against `postgres:18` with **only** `APP_DATABASE_URL` set (as CI does — also with
`auth: yes`); images migrated a real database and served `healthy` / `201` (auth: `401` without a token, `201` with
one from `/token`). SQLite: the Alembic sequence on a file database, image migrated through a volume and served
`201`. `docker compose config -q` validated each `compose.yaml` (not brought up with `compose up`; the same services
were run with `docker run` on a user network). Observed gotchas, each fixed in the templates: greenlet missing without
`sqlalchemy[asyncio]`; coverage under-reporting without `concurrency = ["greenlet", "thread"]`; `uv add` failing
before `app/__init__.py` exists; `testcontainers.postgres` deprecation; SQLModel `Field(regex=...)` not enforcing the
pattern (use `schema_extra={"pattern": ...}`); `import sqlmodel` in revisions failing mypy; sphinx-autodoc-typehints
warnings from imported names; Starlette 1.8 `TestClient` requiring `httpx2` (the templates use `AsyncClient` +
`ASGITransport` instead); Alembic needing a URL-only settings class so migration jobs don't need app secrets. Not
verified: Python 3.12/3.14 runs (only 3.13), and the GitHub Actions side (owned by the workflows skill).

## Sources

- irurueta docs: `backend/fastapi/getting-started.adoc` (uv, `[tool.fastapi]`), `project-structure-and-layered-architecture.adoc`,
  `dependency-injection.adoc`, `dependencies-with-yield.adoc` (`scope="function"`, commit placement),
  `settings-lifespan-and-background-tasks.adoc`, `sql-databases-with-sqlmodel.adoc` (model family, async stack,
  Alembic), `testing.adoc` (`dependency_overrides`, SQLite + PostgreSQL tiers, `httpx2` note), `async-and-concurrency.adoc`,
  `oauth2-password-and-jwt.adoc`, `deployment.adoc` (pinning), `docker-and-kubernetes.adoc` (uv Dockerfile, health
  probes, Compose, migration job), `pydantic-v2-essentials.adoc`, `introduction-and-architecture.adoc`
- irurueta docs: `backend/flask/database-migrations.adoc` (naming convention, autogenerate review, CI checks),
  `backend/flask/flask-sqlalchemy.adoc`, `backend/flask/docker-and-kubernetes.adoc` (multi-stage uv image, UID 10001,
  stdlib health check), `backend/pyramid/sqlalchemy-transactions-and-migrations.adoc` (`alembic check`, metadata
  comparison test), `backend/tornado/databases-and-async-drivers.adoc` (`sqlalchemy[asyncio]`, AsyncSession rules),
  `programming-languages/python/virtual-environments-and-packaging.adoc`, `programming-languages/python/docstrings.adoc`,
  `programming-languages/python/testing.adoc`, `backend/docker/image-best-practices-and-security.adoc`
- This catalog: the Python scaffold contract shared with `iru-setup-python-repository`,
  `iru-setup-python-github-workflows` and the `iru-python-*` gates; `iru-setup-nestjs-app` and `iru-setup-php-laravel`
  (structure)
- uv: <https://docs.astral.sh/uv/guides/integration/fastapi/>, <https://docs.astral.sh/uv/guides/integration/docker/>;
  Alembic: <https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic>;
  testcontainers-python: <https://testcontainers-python.readthedocs.io/>; Sphinx:
  <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>
