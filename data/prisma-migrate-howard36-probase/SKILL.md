---
name: prisma-migrate
description: Create a Prisma migration for a schema change against the local database. Use after editing prisma/schema.prisma.
disable-model-invocation: true
---

Migration name (from arguments, kebab-case; ask if missing): $ARGUMENTS

1. Confirm `prisma/schema.prisma` has the intended change and nothing else (`git diff prisma/schema.prisma`).
2. Generate and apply the migration against the local DB. The env wrapper is required; Prisma does not read `.env.local` on its own:
   ```
   npm run local -- prisma migrate dev --name $ARGUMENTS
   ```
3. Read the generated SQL under `prisma/migrations/<timestamp>_<name>/migration.sql` and check for destructive statements (`DROP COLUMN`, `DROP TABLE`, type changes on populated columns). Call these out explicitly in your reply.
4. If the change affects seed data, update `prisma/seed.mjs` and re-run `npm run local -- prisma db seed`.
5. Run `/verify`.

Remind the user in your reply: merging this PR to `main` runs `prisma migrate deploy` against production automatically. Never run migrations with `npm run prod -- ...` yourself.
