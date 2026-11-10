---
name: migration
description: Create, review and test an Alembic migration after changing SQLAlchemy models. Use whenever a model, column, index or constraint changes.
---

The schema is owned by Alembic. Nothing creates tables at startup in production.

```bash
export DATABASE_URL=sqlite:////tmp/migration-check.db
rm -f /tmp/migration-check.db
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "add <thing>"
uv run alembic upgrade head && uv run alembic downgrade -1 && uv run alembic upgrade head
unset DATABASE_URL
```

Then edit the generated file:

- Keep the `__all__` line the other migrations have, and remove the autogenerate comments.
- Check every column type, nullability, default, foreign key and `ondelete` against the model.
- A `mapped_column` with no `nullable=` takes its nullability from the `Mapped` type: `Mapped[str | None]` is nullable and `Mapped[str]` is not.
- Postgres specifics (pgvector columns, GIN or HNSW indexes) go behind a dialect check, as in the knowledge migration, so SQLite still upgrades.
- A migration that rewrites data must work on both SQLite and Postgres and must be safe to run on SoDA's live database. Never drop a column or table that a live client reads; deprecate it first.
- A new model module goes in `MODEL_MODULES` in `modules/manifest.py`. `alembic/env.py` and `tests/conftest.py` read that list.

`make ci` runs `alembic check`, which fails when models and migrations disagree.

The ID of the new revision goes in the PR body, so deployers know to run `alembic upgrade head`.
