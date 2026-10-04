---
name: appflare-handlers
description: Write Appflare backend handlers, including query (GET) and mutation (POST) endpoints with Zod args, authRequired, middleware and ctx.error, background scheduler tasks enqueued with ctx.scheduler, cron jobs, and storageManager rules for R2 storage. Explains how file paths map to routes, client names and task names. Use when creating or editing endpoints, API logic, auth or role checks, background jobs, scheduled tasks or file-access rules in an Appflare project, or when a route is missing from the generated client.
metadata:
  author: appflare
  version: "0.3.0"
---

# Appflare handlers

## Pick the handler kind

| Need | Helper | Exposed as |
| --- | --- | --- |
| Read data | `query` | `GET /queries/<path>/<export>`, `appflare.queries.<path>.<export>` |
| Change data | `mutation` | `POST /mutations/<path>/<export>`, `appflare.mutations.<path>.<export>` |
| Background work | `scheduler` | task `<parentDir or root>/<file>/<export>` |
| Time-based work | `cron` | Cron Trigger |
| Authorize R2 access | `storageManager` | used by `ctx.storage` and `/storage/*` |

## Workflow

- [ ] Choose a file under `scanDir`. The path becomes the client path, and a leading `queries/` or `mutations/` folder is dropped
- [ ] Import helpers from the **relative** generated module, e.g. `../_generated/handlers`
- [ ] Write `export const name = helper({...})`. Only this exact form is discovered
- [ ] Run `bun appflare dev` and confirm it succeeds
- [ ] For data access patterns, load **appflare-querying**

## Query / mutation template

```ts
import * as z from "zod";
import { mutation, query } from "../_generated/handlers";

export const listTasks = query({
	args: {
		projectId: z.string(),
		limit: z.coerce.number().int().min(1).max(100).default(20),
		done: z.stringbool().optional(),
	},
	authRequired: true,
	handler: async (ctx, args) => {
		return ctx.db.tasks.findMany({
			where: {
				projectId: args.projectId,
				...(args.done === undefined ? {} : { done: args.done }),
			},
			orderBy: { column: "id", direction: "desc" },
			limit: args.limit,
		});
	},
});

export const completeTask = mutation({
	args: { id: z.number().int() },
	authRequired: true,
	handler: async (ctx, args) => {
		const [task] = await ctx.db.tasks.update({
			where: { id: args.id, assigneeId: ctx.user.id },
			set: { done: true },
		});
		if (!task) ctx.error(404, "Task not found");
		return task;
	},
});
```

## Rules

- **`args`** is a raw Zod shape (a plain object), not `z.object(...)`. Use `args: {}` for none.
- **Query args arrive as strings** and are converted to what the schema expects, so `z.boolean()`, `z.number()`, `z.array(z.string())` and object args work in a `query`. `z.coerce.*` still works. Mutation args are JSON, so any Zod type works.
- **Auth:** `authRequired: true` returns 401 without a session. Otherwise guard with `if (!ctx.user) ctx.error(401, "…")`.
- **Roles and shared checks:** use `middleware: async (ctx, args, request) => { if (ctx.user?.role !== "admin") ctx.error(403, "Forbidden"); }`. It runs after the auth check and before the handler.
- **Errors:** `ctx.error(status, message, details?)` throws and responds `{ message, details }` with that status. Other throws become a sanitized `500 { message: "Internal error", requestId }`, so never rely on a raw `Error` message reaching the client. Constraint failures map automatically (unique → 409, trigger/check → 400).
- **Return JSON-serializable values.** A `Date` reaches the client as a string.
- **Realtime-friendly queries:** a subscribed query refreshes only if its handler uses nothing but `ctx.db` reads plus `ctx.user`/`ctx.session`. `ctx.error`, `ctx.$db`, `ctx.storage` or anything that throws on empty results disables pushes, so return `null` instead of `ctx.error(404)` in those queries.

## Scheduler and cron (quick form)

```ts
import { cron, scheduler } from "../../_generated/handlers";

// file: src/jobs/email.ts → task "jobs/email/sendDigest"
export const sendDigest = scheduler({
	args: { userId: z.string() },
	handler: async (ctx, args) => { /* ... */ },
});

// from any handler:
await ctx.scheduler.enqueue("jobs/email/sendDigest", { userId }, { delaySeconds: 60 });

export const nightly = cron({
	cronTrigger: "0 3 * * *", // string literal or array of literals
	handler: async (ctx) => { /* ... */ },
});
```

## Gotchas

- `export default`, `export function`, re-exports and wrapped helpers are **not** discovered.
- Task names use only the **last** directory: `src/a/jobs/email.ts` and `src/b/jobs/email.ts` collide and fail with `Duplicate handler operation discovered`.
- Scheduler and cron contexts have `ctx.user === null`. Failures are logged and **not retried**.
- `cronTrigger` must be a literal. Variables are invisible to the build.
- Storage is **denied by default**. Without a `storageManager` returning `true`, even `ctx.storage` calls in your own handlers get 403.
- `ctx.user` is typed non-null but can be `null` without `authRequired`.
- Writes through `ctx.$db` don't trigger realtime updates. Use `ctx.db`.
- A mutation that writes several tables should use `ctx.db.batch` or `ctx.db.transaction` so a mid-way failure leaves nothing behind.
- Files named `*.test.*` or `*.spec.*`, anything in `__tests__/`, and config `exclude` globs are not discovered.

## References

- Read [references/context.md](references/context.md) when you need a `ctx` field (`db`, `$db`, `user`, `session`, `auth`, `storage`, `scheduler`, `context.env`, `mutationEvents`, `error`).
- Read [references/background-jobs.md](references/background-jobs.md) when writing scheduler tasks or cron jobs, or debugging queue and cron execution.
- Read [references/storage.md](references/storage.md) when writing `storageManager` rules or using `ctx.storage` or the `/storage/*` routes.
