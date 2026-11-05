---
name: statenour-migration
description: Use when changing the statenour Prisma schema (apps/statenour/prisma/schema.prisma) — migrations are hand-applied and one wrong flag silently drops pgvector data.
triggers: prisma schema, schema.prisma, prisma migration, statenour schema, hand-applied migration, pgvector, migrate, data loss flag, apply migration
---

# statenour-migration

statenour's Prisma migrations are NOT auto-applied. A schema change
needs a deliberate, prod-verified apply.

## Hard rules

- **NEVER `prisma db push --accept-data-loss`** — and never put that
  flag in a `package.json` script or CI. pgvector
  (`vector_embeddings.embedding_vec*`) and the `chat_messages`
  tsvector generated column live partly outside Prisma's model view;
  `--accept-data-loss` silently drops them. A pre-push gate guards
  against this — don't defeat it. Recovery is
  `scripts/recover-pgvector-*.ts`.
- **`prisma migrate status` against prod Neon is the source of truth** —
  not "I ran release:db". Local success messaging can lie when the prod
  DB is unreachable or auth fails silently (the v10.0.473 incident).
- **Nothing auto-records the ledger any more.** The guarded endpoint
  `POST /api/system/apply-pending-migration` applies its registry DDL but
  deliberately does **not** write `_prisma_migrations` (#1231). Hand-
  inserted rows for names with no `prisma/migrations/<name>/` dir are what
  turned `migrate status` red in the first place — 9 orphan rows deleted
  2026-07-30. Recording is always: promote the SQL into
  `prisma/migrations/<name>/`, then `prisma migrate resolve --applied`.
- **A deliberate DROP must also prune every re-apply path.** Removing a
  table means removing its endpoint registry entry, its one-shot apply
  scripts, and any parked SQL — otherwise `IF NOT EXISTS` machinery
  quietly resurrects it. Found live 2026-07-30 (#1233): a registry entry
  would have re-created three tables retired weeks earlier.

## Workflow

1. Edit `prisma/schema.prisma`.
2. Generate the migration SQL; park it under `prisma/migrations-pending/`
   if prod connectivity isn't confirmed yet.
3. Apply with `scripts/apply-pending-migration.ts` — it uses an
   autocommit pg driver, required for `CREATE INDEX CONCURRENTLY`
   (which cannot run inside Prisma's implicit transaction wrap).
4. Record it: `prisma migrate resolve --applied <name>`.
5. Confirm: `prisma migrate status` shows clean.
6. `pnpm typecheck` — the generated client changed.
7. Add the directory name to `lib/db/migration-manifest.ts`
   (`tests/lib/system/owner-panel-migrations.test.ts` fails until you do).
   The Owner Panel pages `migration_unapplied` for any manifest name prod's
   `_prisma_migrations` lacks — **committing a migration is not applying it**:
   `20260929123500_reality_event_envelope` sat committed-but-unapplied for
   three days (2026-09-29..10-02) while every `reality_events` write failed.

## When NOT to use

nickstire migrations — different conventions (hand-applied SQL in
`apps/nickstire/drizzle/NNNN_*.sql`, no Prisma).
