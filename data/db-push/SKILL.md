---
name: db-push
description: Sync the Prisma schema to PostgreSQL using prisma db push (no migration files), regenerate the client, and restart the API server if needed. Use after editing schema.prisma.
---

# db-push

Per ADR 005, dev iteration uses `prisma db push` (not `migrate dev`) — no migration files in dev. This skill is the safe wrapper.

## Steps

1. **Verify the schema parses** before pushing:
   ```bash
   cd data/schema && npx prisma validate
   ```
2. **Check for destructive changes** by running a diff first:
   ```bash
   npx prisma db push --accept-data-loss=false
   ```
   If Prisma warns about data loss, **stop and ask the user**. Don't pass `--accept-data-loss` without explicit permission.
3. **Once safe**, run the actual push:
   ```bash
   npx prisma db push
   ```
4. **Regenerate the client**:
   ```bash
   npx prisma generate
   ```
5. **Restart the API server** if it's running in the background — the new client types won't load otherwise.
6. **Update the vault** — append the new model/column to `Aqarkom_Knowledge/Architecture/Database Schema.md`.
7. **Run `/typecheck`** to surface any type errors caused by the schema change.

## Verification

- [ ] No data loss warnings (or user approved)
- [ ] Client regenerated
- [ ] API server restarted
- [ ] Schema vault note updated
- [ ] `/typecheck` clean

## Anti-patterns

- Don't bypass the data-loss check — even in dev, you may be dropping seeded test data the user wants
- Don't switch to `prisma migrate dev` without an ADR — that changes the project's workflow
- Don't run against production — `db push` is dev-only
