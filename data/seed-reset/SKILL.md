---
name: seed-reset
description: Drop all data and re-seed the database with realistic Saudi demo data. Use when the user says "reset the demo data", "fresh seed", or after a schema change that invalidated existing rows. ALWAYS confirm before running.
---

# seed-reset

**Destructive.** Wipes all rows and rebuilds from `apps/api/seed.ts`. This is only safe in local development.

## Pre-flight checks

1. **Confirm with the user** — even if they just asked, repeat back the consequence: "This will delete all current rows in the database including any test customers you've added. Continue? (y/n)"
2. **Verify env** — `DATABASE_URL` must point to localhost or a known dev database. **Never** run this against staging or production. Check the host portion of the URL.
3. **Check for uncommitted DB changes** — if the user has been manually adding rows in Prisma Studio for a demo, warn them.

## Steps

1. After explicit user confirmation:
   ```bash
   cd /Users/mohammedalhajri/real-estate-CRM-project && npx tsx apps/api/seed.ts --reset
   ```
2. **Watch the output** for errors. Common ones:
   - Prisma client out of sync → run `/db-push` first
   - FK constraint violation → seed order is wrong, fix in `seed.ts`
   - Saudi phone validation fail → seed contains a non-Saudi number
3. **Verify** by counting rows in a few key tables:
   ```bash
   cd data/schema && npx tsx -e "import { PrismaClient } from '@prisma/client'; const p = new PrismaClient(); (async () => { console.log({ users: await p.users.count(), leads: await p.leads.count(), listings: await p.listings.count() }); await p.\$disconnect(); })();"
   ```
4. **Report** the row counts to the user.
5. **Restart the API server** if running, so its cached connections are fresh.

## Verification

- [ ] User explicitly confirmed
- [ ] Target DB is localhost / dev
- [ ] Seed completed without errors
- [ ] Row counts reported

## Anti-patterns

- Don't run without confirmation, even if the user already said "yes" earlier in the session — DB reset is irreversible
- Don't pass `--force` flags
- Don't run against any DATABASE_URL containing `prod`, `production`, `staging`, or a non-localhost host
