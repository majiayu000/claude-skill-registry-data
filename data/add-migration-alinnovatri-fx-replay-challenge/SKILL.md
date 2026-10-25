---
name: add-migration
description: Changes the database schema through a Drizzle migration that runs on PGlite in tests and on Neon only through migrate-on-deploy. Use for any table, column, index or constraint change.
---

# Add a migration

1. Edit the Drizzle schema. Prefer additive changes (new nullable column, new table, new index); a destructive
   change needs the owner's approval first.
2. Generate the migration with the project script (`pnpm db:generate`, Stage 2) and read the SQL it produced.
   Never edit an applied migration; add a new one.
3. Constraints that the API relies on (unique email, foreign keys) live in the database, not only in Zod.
4. Run the integration tests on PGlite; they apply every migration from scratch.
5. Never run a migration against production by hand. Production applies migrations during the Vercel production
   build only (migrate-on-deploy).
6. Note the change in `docs/DECISIONS.md` if it changes the contract, and run `code-reviewer` and
   `security-reviewer`.
