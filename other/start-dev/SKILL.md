---
name: start-dev
description: Start the full local dev environment — frontend, backend, and database — and surface anything that's broken on startup. Use when the user says "start the app", "run dev", or you need a working environment to test a change.
---

# start-dev

Boot the project locally and verify everything is healthy.

## Steps

1. **Check ports** are free:
   - Frontend Vite: `3000`
   - Backend API: `3001` (verify in `apps/api/.env` or `apps/api/server.ts`)
   - Postgres: `5432`
   If a port is taken, ask before killing — it might be the user's other shell.
2. **Verify Postgres is running**:
   ```bash
   pg_isready -h localhost -p 5432
   ```
   If not, start it (`brew services start postgresql@16` or whatever the project uses).
3. **Check `.env`** exists at the API root and has `DATABASE_URL`. If missing, ask before guessing.
4. **Generate Prisma client** in case the schema drifted:
   ```bash
   cd data/schema && npx prisma generate
   ```
5. **Start the backend** with `run_in_background: true`:
   ```bash
   cd apps/api && npm run dev
   ```
   Wait ~3 seconds, then read the background output to confirm it bound to its port and connected to DB.
6. **Start the frontend** with `run_in_background: true`:
   ```bash
   cd apps/web && npm run dev
   ```
7. **Report status** to the user: "Frontend: http://localhost:3000 ✅ | API: http://localhost:3001 ✅"
8. **Don't open the browser** automatically — let the user choose.

## Verification

- [ ] Both servers report listening / ready
- [ ] No startup errors in either log
- [ ] DB connection successful (visible in API log)

## Anti-patterns

- Don't run `npm install` automatically — only if a startup error explicitly says a module is missing
- Don't kill processes on busy ports without asking
- Don't run servers in the foreground — they'll block the conversation
