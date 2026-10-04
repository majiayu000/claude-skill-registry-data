---
name: appflare-cli-deploy
description: Configure, generate, migrate and deploy Appflare projects on Cloudflare Workers. Covers appflare.config.ts (D1 database with query limits, KV, R2, Better Auth options, scheduler queue, realtime Durable Object, handler exclude globs, wranglerOverrides), the Bun CLI commands build, dev --watch, migrate --local/--remote/--preview, migrate:custom and add-admin, the generated wrangler.json bindings, secrets, ALLOWED_DOMAINS CORS and wrangler deploy. Use when setting up a new Appflare backend, adding Cloudflare bindings, fixing generation, migration or deploy errors, writing custom SQL migrations, creating an admin user or shipping to production.
metadata:
  author: appflare
  version: "0.3.0"
compatibility: Requires Bun >= 1.3.9 and Wrangler with access to a Cloudflare account.
---

# Appflare CLI and deployment

## Commands (run from the backend package, always with Bun)

```bash
bun appflare dev              # generate once
bun appflare dev --watch      # regenerate on changes in scanDir
bun appflare build --no-build # generate without running `tsc --build`
bun appflare migrate --local  # regenerate + drizzle-kit generate + wrangler d1 migrations apply
bun appflare migrate --remote
bun appflare migrate:custom --name add_guards  # empty SQL migration (triggers, views, backfills)
bun appflare add-admin -n "Admin" -e admin@example.com -p "…" --local
```

Every command accepts `-c <config path>`.

## Minimal config

```ts
import { bearer } from "better-auth/plugins";

export default {
	scanDir: "./src",
	outDir: "./_generated",
	exclude: ["**/__fixtures__/**"],                             // optional, skipped by discovery
	schemaDsl: { entry: "./schema.ts" },
	schema: ["./_generated/schema.compiled.js", "./_generated/auth.schema.js"],
	database: {
		binding: "DB",
		databaseName: "my-app-d1",
		databaseId: "<id>",
		migrationsDir: "./drizzle",
		query: { defaultLimit: 100, maxLimit: 1000 },              // optional ctx.db read limits
	},
	kv: { binding: "CACHE", id: "<id>" },                       // optional
	r2: { binding: "ASSETS", bucketName: "my-app-assets" },     // optional, needed for storage
	auth: {
		enabled: true,
		basePath: "/api/auth",
		options: { emailAndPassword: { enabled: true }, plugins: [bearer()] },
		clientOptions: {},
	},
	scheduler: { enabled: true, binding: "MY_APP_QUEUE", queue: "my-app-scheduler" },
	wranglerOutPath: "./",
	wranglerOverrides: {
		name: "my-app-api",
		main: "./_generated/server.js",
		compatibility_date: "2026-04-08",
		compatibility_flags: ["nodejs_compat", "nodejs_compat_populate_process_env"],
	},
};
```

## New project checklist

- [ ] `bun add appflare hono zod drizzle-orm better-auth better-auth-cloudflare @hono/standard-validator`
- [ ] `bun add -d drizzle-kit wrangler typescript @better-auth/cli`
- [ ] Create resources: `bunx wrangler d1 create …`, `kv namespace create`, `r2 bucket create`, `queues create`
- [ ] Write `appflare.config.ts` with the real ids, and set `wranglerOverrides.main`
- [ ] Write `schema.ts` and at least one handler under `src/`
- [ ] `bun appflare dev`, then `bun appflare migrate --local`, then `bunx wrangler dev`
- [ ] Add `_generated/` to `.gitignore`, and commit `drizzle/`

## Production deploy checklist

- [ ] `bun appflare build`
- [ ] `bun appflare migrate --remote` (review the SQL first)
- [ ] `bunx wrangler secret put BETTER_AUTH_SECRET` (plus any app secrets)
- [ ] Set `wranglerOverrides.vars.ALLOWED_DOMAINS` to a comma-separated list of origins
- [ ] `bunx wrangler deploy`
- [ ] Optional: `bun appflare add-admin … --remote`, then open `/admin`

## Gotchas

- The config is validated **strictly**, so unknown keys fail. Don't annotate the object as `AppflareConfig`, because that widens the client auth plugin types.
- The generated `main` defaults to `./src/index.ts`. Override it with `./_generated/server.js`.
- `wranglerOverrides` merges objects deeply, but **arrays replace** generated arrays (`d1_databases`, `queues`, `routes`…).
- Only the **first** `database`, `kv` and `r2` entries are used by the runtime and by `migrate`.
- Queue bindings are generated only when a `scheduler` or `cron` handler exists. Realtime Durable Object bindings are on by default.
- `migrate` regenerates artifacts itself before diffing, so it can't run against a stale schema. Pass one target flag only.
- When `tsconfig.json` exists and `build` is true, generation ends with `tsc --build`, so type errors fail the command. Use `--no-build` to isolate generation problems.
- With `ALLOWED_DOMAINS` unset, CORS allows every origin with credentials.
- `add-admin` needs Better Auth's `admin()` plugin (for the `role` and `banned` columns) and a migrated database.

## References

- Read [references/config-reference.md](references/config-reference.md) for every config option with its defaults, the full list of generated `wrangler.json` bindings, and generated file names.
