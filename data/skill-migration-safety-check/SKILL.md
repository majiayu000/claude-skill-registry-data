---
name: Migration Safety Check
description: "Review an Alembic migration for safety, backward compatibility, FedRAMP audit constraints, and zero-downtime risk. Triggers on phrases like 'migration safety', 'review this migration', or when files under `api/src/db/migrations/versions/` are added or modified. Flags risky operations (DROP, NOT NULL without default, table locks) and suggests safer patterns."
model: inherit
---

## Purpose

Catch migration foot-guns before they reach a production deploy. Simpler-grants-gov runs FedRAMP-Moderate Postgres with online deploys; certain Alembic operations either lock tables, break older app revisions still in flight, or violate audit-log requirements.

## When to Invoke

- A new file is added under `api/src/db/migrations/versions/`.
- An existing migration is edited.
- A reviewer says "migration safety" or "is this safe to deploy".
- Before tagging a release that includes any schema change.

## When NOT to Invoke

- For data-only seed scripts not under `versions/`.
- For SQLAlchemy model changes that have no migration yet — run `alembic revision --autogenerate` first.
- As a substitute for staging deploys.

## Inputs

- **migration_file**: path to a single Alembic version file, or active editor file.
- **mode** (optional): `strict` (default — block on any HIGH) or `advisory`.

## Procedure

1. Resolve the migration file. Reject anything not under `api/src/db/migrations/versions/`.
2. Parse the `upgrade()` and `downgrade()` bodies via AST or regex.
3. Run the deterministic risk rules:
   - **HIGH** `op.drop_column`, `op.drop_table`, `op.drop_constraint` without `if_exists` and without a deprecation comment.
   - **HIGH** `op.add_column` with `nullable=False` and no `server_default`.
   - **HIGH** `op.alter_column` changing type on a populated table without a USING clause.
   - **HIGH** `op.create_index` without `postgresql_concurrently=True` on a table > 100k rows (heuristic: any table referenced in production seed data).
   - **HIGH** Renames (`op.alter_column ... new_column_name=`) — break older app revisions.
   - **MED** Missing `downgrade()` body or `pass` only.
   - **MED** Raw `op.execute("...")` SQL without a comment explaining intent.
   - **MED** Foreign keys added without `ondelete` policy.
   - **LOW** Migration touches an audit-logged table (cross-reference `documentation/rules/data-privacy.mdc`) without a corresponding audit-log update.
4. Verify revision chain: `down_revision` references an existing prior migration; no fork.
5. Verify the file name matches the Alembic convention `YYYY_MM_DD_HHMM_<slug>_<hash>.py`.
6. Cross-reference `documentation/rules/api-*.md` for project-specific DB rules.
7. Emit the Output Format. Do not modify the migration.

## Outputs

```
Migration Safety Check — api/src/db/migrations/versions/2026_04_05_1130_add_status_index_a7f3.py
Mode: strict

Findings (3):
  [HIGH] L24  op.create_index without postgresql_concurrently=True on `opportunity`
         Fix:  op.create_index(..., postgresql_concurrently=True)
               Wrap migration with: def upgrade(): op.execute("COMMIT"); ...
               Set `transactional_ddl = False` in env.py for this revision.
  [HIGH] L31  op.add_column nullable=False without server_default
         Fix:  add server_default='draft' OR ship in two migrations (add nullable → backfill → set NOT NULL)
  [MED]  L48  downgrade() is empty
         Fix:  implement reverse op or document irreversibility

Revision chain: OK (down_revision -> 9b2e1f4cd0a8)
Filename convention: OK
Audit-log impact: opportunity table is audit-logged (documentation/rules/data-privacy.mdc §4.2)

Block merge: yes (2 HIGH)
```

## Safety

- Read-only.
- Never runs `alembic upgrade` or any DB command.
- Heuristics only — does not query the live database for row counts.
- Defers final risk judgment to the on-call DBA for HIGH findings.
- FedRAMP: never emits the contents of audit-logged columns.

## Examples

**Example 1 — Concurrent index miss**
Author adds a btree index on `opportunity.posted_date`. Skill flags missing `postgresql_concurrently=True` and explains the transactional-DDL workaround.

**Example 2 — Two-step backfill required**
Author drops `legacy_status` in the same migration that adds `status`. Skill flags HIGH and suggests splitting into two releases.

**Example 3 — Empty downgrade**
Skill flags MED, recommends documenting the irreversibility decision in the migration docstring.

## Related

- `.cursor/skills/skill-impact-analysis/` — find downstream consumers of the changed model.
- `.cursor/skills/skill-sql-explain/` — sanity-check query plans after schema changes.
- `documentation/rules/data-privacy.mdc` — audit-log column inventory.
