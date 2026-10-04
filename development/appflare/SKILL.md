---
name: appflare
description: Build and modify Appflare backends, the generate-first framework for Cloudflare Workers that compiles a schema DSL plus query/mutation/scheduler/cron/storageManager handlers into a Hono Worker (D1 + Drizzle, Better Auth, R2, Queues, Cron Triggers, Durable Object realtime, /admin) and a typed client with React hooks. Use when a project contains appflare.config.ts, imports from "appflare", "appflare/react" or "_generated/handlers", or the user mentions Appflare. Covers the dev loop and points to the focused appflare-* skills.
metadata:
  author: appflare
  version: "0.3.0"
---

# Appflare

## Recognize the project

An Appflare backend package has:

- `appflare.config.ts`, which sets `scanDir` (handlers, usually `./src`), `outDir` (usually `./_generated`) and `schemaDsl.entry` (usually `./schema.ts`)
- `schema.ts`, which exports `schema({...})` built from `table()` and `v.*`
- handler files under `scanDir` that import from a relative `_generated/handlers`
- `_generated/`, which is generated output. **Never edit it**

Frontends import `Appflare` from the backend's `_generated/client` and hooks from `appflare/react`.

## Mental model

1. You write the schema and handlers.
2. `bun appflare dev` generates the server, handler runtime, typed client, auth schema and `wrangler.json`.
3. `bun appflare migrate --local` diffs the schema into SQL and applies it to D1.
4. `wrangler dev` serves `GET /queries/...`, `POST /mutations/...`, `/api/auth/*`, `/storage/*`, `/realtime/*` and `/admin`.

## Default workflow for any change

- [ ] Read `appflare.config.ts` to find `scanDir`, `outDir` and the schema entry
- [ ] Schema change: edit `schema.ts` (load **appflare-schema**)
- [ ] Backend logic: add or edit handlers under `scanDir` (load **appflare-handlers**, plus **appflare-querying** for `ctx.db`)
- [ ] Regenerate: `bun appflare dev` from the backend package. It must finish without errors
- [ ] Schema changed: `bun appflare migrate --local`
- [ ] Frontend: call the new route through the generated client (load **appflare-client**)
- [ ] Config, bindings or deploy work: load **appflare-cli-deploy**

## Which skill to load

| Task | Skill |
| --- | --- |
| Tables, columns, enums, JSON columns, indexes, checks, relations, migrations | `appflare-schema` |
| query / mutation / scheduler / cron / storageManager, auth checks, errors | `appflare-handlers` |
| `ctx.db` reads, writes, batch/transaction, aggregates, filters, pagination | `appflare-querying` |
| `new Appflare()`, `.run()`, `useQuery`/`useMutation`, realtime, sign-in, uploads | `appflare-client` |
| `appflare.config.ts`, CLI commands, wrangler bindings, CORS, deploy | `appflare-cli-deploy` |

## Gotchas that apply everywhere

- The CLI only runs under **Bun**. Use `bun appflare <cmd>` and never `node`/`npx`.
- Generated code is stale until you regenerate. Missing routes or types usually mean "run `bun appflare dev`".
- Handlers are discovered only as `export const name = query({...})` (or mutation/scheduler/cron/storageManager). Default exports, function declarations and re-exports are ignored.
- Route and client names come from file paths: `src/posts.ts#listPosts` becomes `appflare.queries.posts.listPosts`. A leading `queries/` or `mutations/` folder is dropped.
- Relations create FK fields named `<relation>Id`. Filter and insert with `ownerId`, and read the related row with `with: { owner: true }`.
- Query args arrive as URL strings and are converted to what the zod schema expects, so plain `z.boolean()`, `z.number()` and `z.array()` work in a `query`.
- `ctx.db` is strict: `findMany` defaults to 100 rows, unknown `where` keys throw, and `update`/`delete` need a filter (or `allowAll: true`).
- `ctx.db` writes are atomic, and `ctx.db.batch` / `ctx.db.transaction` extend that across tables. `ctx.$db` remains the raw Drizzle escape hatch.
- Unhandled errors return a sanitized 500. Use `ctx.error(status, message)` for anything the client should read.
- `ctx.user` is typed non-null but is `null` for anonymous requests unless `authRequired: true`, and always `null` in scheduler/cron.
- JSON responses turn `Date` into ISO strings on the client.
