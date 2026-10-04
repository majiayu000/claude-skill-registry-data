---
name: add-cron-job
description: Create a scheduled background job using node-cron with logging, error handling, and health tracking. Use for nightly recalculations, campaign processing, alert checks.
---

# add-cron-job

Creates a new scheduled background job that runs on a cron schedule. Includes execution logging, error handling, retry logic, and health monitoring.

## Inputs to gather

- **Job name** — e.g., "recalculate-lead-scores", "process-drip-campaigns", "check-fal-expiry"
- **Schedule** — cron expression (e.g., `0 2 * * *` for 2am daily, `*/15 * * * *` for every 15 min)
- **What it does** — the business logic (query + transform + update)
- **Failure behavior** — retry count, alert on failure

## Steps

1. **Check cron infrastructure exists.** Read `apps/api/cron/index.ts`. If missing, create:
   ```typescript
   import cron from "node-cron";
   const jobs: Map<string, cron.ScheduledTask> = new Map();
   export function registerJob(name: string, schedule: string, handler: () => Promise<void>) { ... }
   ```

2. **Create the job file** at `apps/api/cron/{job-name}.ts`:
   ```typescript
   export async function handler() {
     const startedAt = Date.now();
     // ... business logic using prisma
     const duration = Date.now() - startedAt;
     await prisma.cron_runs.create({ data: { jobName, status: "SUCCESS", durationMs: duration } });
   }
   ```

3. **Register the job** in `apps/api/cron/index.ts`:
   ```typescript
   import { handler as recalcScores } from "./recalculate-lead-scores";
   registerJob("recalculate-lead-scores", "0 2 * * *", recalcScores);
   ```

4. **Add the cron_runs tracking model** (if not exists):
   ```prisma
   model cron_runs {
     id         String   @id @default(uuid())
     jobName    String
     status     String   // SUCCESS, FAILED
     durationMs Int
     error      String?
     createdAt  DateTime @default(now())
   }
   ```

5. **Add error handling wrapper:**
   ```typescript
   try { await handler(); }
   catch (err) { await prisma.cron_runs.create({ data: { jobName, status: "FAILED", error: err.message } }); }
   ```

6. **Install node-cron** if needed: `pnpm add node-cron && pnpm add -D @types/node-cron`

## Verification checklist

- [ ] Job runs at the expected schedule
- [ ] Success/failure logged in cron_runs table
- [ ] Error handling catches and logs failures
- [ ] Job does not block the main Express thread
- [ ] Job respects org isolation (processes all orgs or specific org)
- [ ] `/typecheck` passes

## Anti-patterns

- Don't run expensive queries without LIMIT — process in batches
- Don't run cron jobs during peak hours — schedule for 2-4am Saudi time (UTC+3)
- Don't skip the tracking table — you need visibility into job health
- Don't use setInterval — use node-cron for proper cron expressions
