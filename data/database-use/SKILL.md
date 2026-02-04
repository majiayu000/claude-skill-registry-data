---
name: database-use
description: Any time database-related activity is required.
---

# Database use instructions

## Configuration & Standards
- **Engine**: PostgreSQL only (Port: 5433).
- **Connection string**: sourced from `.env` via `DATABASE_URL` (see `SQLALCHEMY_DATABASE_URI` / `DATABASE_URL` in `config.py`).
- **Testing DB**:
    - By default tests also use the live DB (see `pytest` note below).
    - Optional override: `TEST_DATABASE_URL` (used by `TestingConfig` in `config.py`).
- **SQLAlchemy instance**: Import `db` from `utils_db/database.py`. Do NOT create a new instance in `app.py`.
- **Scripts location**:
    - Canonical database scripts/utilities live in `utils_db/`.
    - No ad-hoc “root scripts” in the repo root.
- **Execution safety**:
    - Do NOT paste multi-line SQL or Python into the terminal.
    - Draft ad-hoc scripts in `temp/` first, then promote reusable ones into `utils_db/`.
- **Testing CSRF**: `TestingConfig` disables CSRF (`WTF_CSRF_ENABLED = False`) specifically for tests.

## Credentials
- Connection credentials: `.env`.
- Users' credentials: `.env`
    User passwords in DB are hashed. Hash is stored in the pw_hashed column.

## Structure
- Schema documentation: `.roo/docs/database_schema.md`
- SQLAlchemy model files: `models/models_*.py` (eg, `models/models_user.py`)
- SQLAlchemy database instance: `utils_db/database.py`
- Schema tools:
    - Primary: `utils_db/schema_inspector.py`
    - Supplemental: `utils_db/schema_compare.py` (writes reports to `temp/`)

## Preferred Utilities
Reuse existing tools in `utils_db/` before writing new ones:
- `utils_db/user_password_utils.py`
- `utils_db/user_management_utils.py`
- `utils_db/media_utils.py`

## Source of Truth Hierarchy
The formal Source of Truth (SoT) hierarchy for database schema information:
1) PGDB (live PostgreSQL)
2) models_*.py (SQLAlchemy) (eg, `models/models_user.py`)
3) `.roo/docs/database_schema.md` (generated)

When there is any doubt about a column, see PGDB. If a column is needed or a column name needs to change, always ask user for permission to make the add/change.

## Schema Update Workflow
When making schema or data changes, follow this workflow in order:
1) Modify PGDB
    - Make changes to the live database (see "Credentials" above).
    - When creating a script to check or change the database:
        - Do NOT paste the script into the terminal.
        - Check `utils_db/` for a suitable or near-suitable script first; reuse/extend if possible.
        - If it’s a true one-off, draft it in `temp/` first.
        - If it’s reusable, create/update a `.py` utility in `utils_db/`.
2) Update models
    - Update the appropriate SQLAlchemy model file(s) under `models/models_*.py`.
3) Regenerate documentation
    - Run: `python utils_db/schema_inspector.py generate-docs` to update `.roo/docs/database_schema.md`.
4) Log changes
    - Record the date and change in `.roo/docs/pgdb_changes.md`.

## Schema Inspector Utility
The `utils_db/schema_inspector.py` tool provides commands for schema management:
- `introspect` - Inspect live database schema and display structure
- `compare-db-models` - Compare live database against SQLAlchemy models to identify discrepancies
- `compare-models-doc` - Compare SQLAlchemy models against `.roo/docs/database_schema.md`
- `generate-docs` - Generate/update `.roo/docs/database_schema.md` from current database state
- `report` - Generate discrepancy reports under `.roo/reports/` (JSON and Markdown)
- `validate` - Verify schema documentation is up-to-date with the database

Usage notes:
- This utility uses the configured database URL (from `.env`) and initializes `db` from `utils_db/database.py`.
- Some schema comparison utilities may emit reports under `.roo/reports/` when run.

Usage examples:
- Introspect schema: `python utils_db/schema_inspector.py introspect`
- Compare: `python utils_db/schema_inspector.py compare-db-models`
- Compare models vs docs: `python utils_db/schema_inspector.py compare-models-doc`
- Generate docs: `python utils_db/schema_inspector.py generate-docs`
- Validate docs: `python utils_db/schema_inspector.py validate`

## Testing
- Run tests with `pytest` against the live PostgreSQL database.
- In `TestingConfig` (`config.py`), CSRF is disabled (`WTF_CSRF_ENABLED = False`).
