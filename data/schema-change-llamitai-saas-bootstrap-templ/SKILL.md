---
name: schema-change
description: Evolve SQLAlchemy models, constraints, indexes, Alembic revisions or data transformations. Use when a change adds or alters tables, columns, relationships, migrations or stored data. DTO, Pydantic or zod-only edits do not activate this workflow.
---

# schema-change

Read the project profile, affected data criteria, central ORM models
(`backend/src/common/database/models/`) and the Alembic graph. Coordinate with
backend-change and consumers when HTTP contracts change.

## Steps

1. Generate with `just backend new-migration "description"` when appropriate,
   then deliberately review SQL, FK ordering, constraints and data transforms.
   Merge conflicting revisions through Alembic's graph workflow.
2. Test an empty database and the supported previous revision with
   representative data. Use `just backend check-migrations`; it owns disposable
   databases, upgrades and drift checks. Add data-preservation assertions when a
   migration transforms existing values.
3. Confirm an unambiguous integrated head, model parity and preserved data. Plan
   compatible deployment phases when API, frontend and schema do not update
   simultaneously. When the change reaches DTOs or routes, refresh the API
   snapshot with [openapi-sync](../openapi-sync/SKILL.md). Place shared domain
   models as [backend-architecture](../backend-architecture/SKILL.md) describes.
4. Record the structural decision in an ADR and the technical evidence on the
   exact integrated revision. Return findings to the implementer;
   [validate-change](../validate-change/SKILL.md) checks evolution and
   compatibility acceptance. Clean only owned resources.

## Gotchas

- Autogeneration is a starting point, not a reviewed migration.
- `metadata.create_all` and migrate-current are not migration evidence.
- Do not require a destructive downgrade by default.
- Run `just backend migrate` before `just backend new-migration`; autogenerate
  diffs against the local database, so a stale database yields a wrong revision.
- `Base.metadata` has no `naming_convention`: name new constraints and indexes
  explicitly (`name="uq_<table>_<cols>"`, `ix_...`, `fk_...`) so later revisions
  can drop them deterministically.
- Revision ids follow `YYYYMMDD_NNNNNN` (date plus a global sequence, e.g.
  `20260907_000002`) with files named `<revision>_<slug>.py` in
  `backend/src/common/database/versions/`. The recipe's `file_template` produces a
  timestamped name with a random hex id, so set `revision` and rename the file to
  the next sequence before review.
- `env.py` `include_object` skips `directus_*` tables; never write migrations for
  them, and do not read their absence from autogenerate as drift.
