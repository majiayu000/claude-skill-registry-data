---
name: routes
description: Route layout standards for tereo's Express routers (packages/tereo/src/routes). Use when adding, moving, renaming or reviewing a route, router, controller, route schema or route-local middleware; when deciding where a new endpoint's files go or what order to register routes in; or when routeLayout.unit.test.ts fails.
paths:
  - packages/tereo/src/routes/**
---

# Route Layout

The folder tree under `src/routes` mirrors the URL, one folder per segment, and every folder has the
same files. `src/tests/conventions/routeLayout.unit.test.ts` enforces the mechanical rules; registration order is
checked in review.

## The Tree

`routes/index.ts` is the root: `/.well-known` (`well-known/`), `/health`, `/oauth`, `/v1`, then the
admin UI's files and app shell as the catch-all. `routes/v1/index.ts` mounts core's API areas
(`account/`, `admin/`, `audit/`, `files/`, `registry/`, `setup/`, `webhooks/`), each with its body
limit. **A new API route goes under `routes/v1/`.**

## Files in a Folder

| File | Holds | Never holds |
|---|---|---|
| `index.ts` | Exactly one `Router()` and its `router.<verb>/use(…)` calls | Function definitions (no `=>`, no `function`) |
| `controllers.ts` | Handlers — functions that answer the request | Routers, route registration |
| `schemas.ts` | Zod schemas and their `z.infer` types | — (the only file that calls `z.*`) |
| `middleware.ts` | Middleware used only by this folder's routes (guards, multer wrappers, `guardArchivedById(…)`) | Middleware several areas share → `src/middleware/` |
| `utils.ts`, `events.ts`, … | Other helpers, if needed | Routes |

A controller shared with a nested route stays in the parent's `controllers.ts`; the nested
`index.ts` imports it from `../controllers.js`.

## `:param` Folders

Every `:param` is its own folder, named for the **singular** of what it addresses, and mounted one
segment at a time:

| URL | Folders |
|---|---|
| `/webhooks/:id` | `webhooks/webhook/` |
| `/sessions/:sessionId` | `sessions/session/` |
| `/by-id/:id` (objects) | `by-id/object/` |
| `/entity/:entityType/:entityId` | `entity/entity-type/entity/` |
| `/*objectKey` | `objects/object/` |

- Parent: `router.use("/:id", itemRouter)` — a single-segment path, always `use`.
- Item: `Router({ mergeParams: true })`, its own routes at `"/"`.
- Never a `:param` in a verb route (`router.delete("/:userId", …)`) or inside a longer path
  (`router.use("/by-id/:id", …)`).
- Folder names match the URL segment (`signing-keys/`, `by-key/`). Only exception: `well-known/`
  for `/.well-known` (a dot folder is hidden).

## Registration Order

Within an `index.ts`, most specific first:

1. Path-less middleware — `router.use(guard)`
2. Static paths — sub-routers (`/members`) and actions (`/archive`, `/default`, `/rotate`)
3. `:param` mounts — `router.use("/:id", itemRouter)`, after the statics so `/default` is never an id
4. Generic `/` routes — `GET /`, `POST /`, `PATCH /`, `DELETE /`

HEAD before GET on the same path (Express otherwise answers HEAD with the GET handler).

Deliberate exceptions: `v1/files/index.ts` mounts `/signed` and `/shared` before its authentication
middleware (they carry their own credential); `routes/index.ts` registers the UI last.

## Example — `/v1/account/api-keys`

`GET|POST /`, `GET /default`, `GET|DELETE /:keyId`, `POST /:keyId/rotate`,
`GET /:keyId/usage/:day`, with an ownership guard on every `:keyId` route:

```
v1/account/api-keys/
├── index.ts  controllers.ts  schemas.ts        # list, create, /default
└── api-key/                                    # /:keyId
    ├── index.ts  controllers.ts  schemas.ts    # get, delete, /rotate; ApiKeyParamsSchema
    ├── middleware.ts                           # guardOwnedApiKey
    └── usage/
        ├── index.ts                            # use("/:day", dayRouter)
        └── day/                                # /:day
            └── index.ts  controllers.ts  schemas.ts
```

```typescript
// v1/account/api-keys/index.ts
const apiKeysRouter = Router();

apiKeysRouter.get("/default", getDefaultApiKey);

apiKeysRouter.use("/:keyId", apiKeyRouter);

apiKeysRouter.get("/", listApiKeys);
apiKeysRouter.post("/", createApiKey);

export default apiKeysRouter;

// v1/account/api-keys/api-key/index.ts
const apiKeyRouter = Router({ mergeParams: true });

apiKeyRouter.use(guardOwnedApiKey);

apiKeyRouter.use("/usage", usageRouter);
apiKeyRouter.post("/rotate", rotateApiKey);

apiKeyRouter.get("/", getApiKey);
apiKeyRouter.delete("/", revokeApiKey);

export default apiKeyRouter;
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Item router without `mergeParams` | `req.params.id` is `undefined`; validation 400s | `Router({ mergeParams: true })` |
| `/:id` mounted before `/default` | `/default` reaches the item router as an id | Statics first |
| Guard written inline in `index.ts` | `routeLayout.unit.test.ts`: "defines no functions in index.ts" | Move it to `middleware.ts` |
| `z.guid().safeParse(id)` in a controller | "builds Zod schemas only in schemas.ts" | Export the schema from `schemas.ts` |
| Moving a folder and hand-fixing imports | A parent still imports the old (now leaf) router; routes 404 | Re-check every parent `index.ts` import after a move, then run `npm run test:unit` and the route's tests |

Related: `backend` (validation, errors, auth, db, outbox), `openapi` (spec paths for new routes),
`test`.
