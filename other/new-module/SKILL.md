---
name: new-module
description: Add a feature module under modules/ with its service, routes, models, jobs, tools, migration, tests and docs registered in every place the platform looks. Use when adding a module or a large feature to an existing one.
---

Read `docs/writing-a-module.md` first; it is the source of truth. Copy the shape of `modules/feeds/` (officer routes) or `modules/runpod/` (machine-token routes).

Steps:

1. `modules/<name>/service.py`: logic only. Takes a session and plain values, never imports Flask, raises a subclass of `core.errors.ServiceError(message, status)`. Declare machine token scopes with `modules.auth.scopes.declare` and org secrets with `core.secrets.declare` or `declare_prefix` at the top.
2. `models.py`: tables on `core.db.Base` with `name: Mapped[type] = mapped_column(...)` columns, `organization_id` on every org-owned row, a unique constraint on the natural key.
3. `api.py`: a blueprint. Use `officer_route` or `machine_route` from `modules/auth/routes.py` with `functools.partial`. Views return a dict or `(dict, status)`.
4. `jobs.py` with `@job` from `core/jobs.py` for scheduled or background work. Import the service inside the function.
5. `tools.py` with `@tool` from `core/tools.py` when agents call the module, named `<module>.<action>`. No try/except: `ServiceError` becomes a tool error. Add a `SKILL.md` for agents with frontmatter `name` (the tool prefix) and `description`; `tests/test_module_layout.py` checks it.
6. Register:
   - `MOUNTS` in `modules/registry.py`, with the blueprint import at the top of the file.
   - `MODEL_MODULES`, `JOB_MODULES` and `TOOL_MODULES` in `modules/manifest.py`, for each of those files the module has.
   - Each Flask-free file other than `service.py`, `models.py`, `jobs.py` and `tools.py` in the Flask-free contract in `pyproject.toml`. Those four are in it by wildcard.
   - If orgs can switch it off: `OPTIONAL_MODULES` in `modules/organizations/service.py`; `module=` on the `Mount` and on each `@tool`; a `module_enabled` check in jobs that run for all orgs. See "Org switch" in `docs/writing-a-module.md`.
7. Migration: see the `migration` skill.
8. Tests in `tests/contract/test_<name>.py`. Fake every network call by monkeypatching the module's fetch or client function. Add the module to the expected list in `tests/contract/test_modules.py` when it is switchable. Add the new routes to `tests/contract/routes.txt` with `UPDATE_ROUTES=1 uv run pytest tests/contract/test_routes.py`.
9. Docs: `modules/<name>/README.md` with a Files table and a Surface list, 25 lines or fewer; a row in `modules/README.md` and the README module table; the modules line in `AGENTS.md`; each new table in `docs/data-model.md`. If the module needs more than its README: `docs/modules/<name>.md`, a row in `docs/README.md`, and the page in `site/scripts/sync-docs.ts`.
10. Run `uv run pytest tests/test_module_layout.py`. It names each place that you did not register the module. Then run the `check` skill.

Write comments and docs with the `technical-writing` skill.
