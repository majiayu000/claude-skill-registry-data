---
name: bridge-index
description: The named cross-package handoffs — who owns each translation between litestone, junction, sierra and the browser client. Use before grepping for a seam, or before adding to one — a gate copy, an error mapper, the result envelope, a directive, a schema keyword, a broadcast, a tether.
---

# Bridge index — the named cross-package handoffs

The current seams: reach for one before grepping, and add to its owner rather than beside it (Invariant 4). They may move, merge or change signature as long as ownership and dependency direction hold.

**One line per seam: name — what it answers — owner.** Before you change a seam or build on it, read its full entry in the section's reference file: the contract, what it refuses, who else reads it, and its ruling. `packages/cli/core/seams.js` parses the lines below — the section headings, the backticked names that open a bullet, and the owner as the first package path in the line. `fli check`'s `seam-owner` fails a stated owner that does not resolve, and `seam-listed` compares the names with the key list in the root `CLAUDE.md`. `references/glossary.md` is the one definition of each term the four catalog skills share; it is not a seam list and `seams.js` does not read it.

**Accessor query** — the `db.$x(accessor, …)` family. An unknown accessor answers empty (*I cannot judge this* is not *this is wrong*), every client flavor answers the same (root, `$setAuth`, `asSystem`, `$scopedBy`), and a principal is passed as an argument rather than read off the client.

**Data → API**
Detail: `references/data-api.md`
- `$setAuth(user)` / `asSystem()` — the Data-boundary checkpoint, and its bypass — `litestone/src/core/client.js`
- `$tapEvents(fn)` — every write announced; `scope: 'row' | 'collection'` is stated by the write, never read off `result` — `litestone/src/core/client.js`
- `withLitestoneDb(db)` — the per-request scoped client, read as `$.db` — `junction/src/core/litestone.ts`
- `gateAuth()` + `autoValidate()` — schema-derived 401s and 400s for model services — `junction/src/core/litestone.ts`
- `validateInput(type)` — the same 400 for a method no model describes, through `methods: [{ method, input }]` — `junction/src/core/litestone.ts`
- `customMethodGrade(method, declared, levels)` — what grades a custom method: `declared` · `floor` · `unchecked` — `junction/src/core/litestone.ts`
- `needsBackfill` — the middle step of an expand/contract split, found in the app's source by `fli release:check` — `cli/core/backfills.js`
- `sessionGateLevel(user)` — a session → the 0–7 scale with the shipped `gradeStanding`; the default `getLevel`, so a caller's level is asked of `db.$levelOf` — `junction/src/core/litestone.ts`
- `toDataPrincipal(user)` — a session → the principal `auth()` reads (`userId` → `id`) — `junction/src/core/litestone.ts`
- `bearerClaim({ from, model, column, claims, key, subject, session })` / `BEARER` / `bearerOf(ctx, model)` — from `@frontierjs/junction/bearer`, the resolver for a caller with no session who still owns rows; `ctx.locals[BEARER]` is the first grant resolved in the app's stated order and `bearerOf` reads any; a session beside the grant is a 400 before the grant is read unless `session: 'merge'` (`FJS-D832`) — `junction/src/core/bearer.ts`
- `bearerClaim(...).mint(db, data)` / `.mintOnCreate()` / `.redeem(db)` — a grant minted by the caller's own create (the digest named in `system:`, `FJS-D819`) and a link redeemed for the httpOnly cookie `from: cookie()` reads (`FJS-D340`); the one place the key, purpose, model and column are stated — `junction/src/core/bearer.ts`
- `resolveTenancy(schema)` / `registry.tenantFor({host, headers, principal})` — the one reading of `tenancy { }` — `litestone/src/core/tenancy.js`, `litestone/src/tenant.js` (the registry)
- `accessorCandidates()` — `model Post` ⇄ service `posts` ⇄ `db.post` — `junction/src/core/litestone.ts`
- `db.$checkWhere(accessor, where)` — is this a valid filter key; throws — `litestone/src/core/client.js`
- `db.$checkOrderBy(accessor, orderBy)` — is this a sortable key, with the reason when it is not; throws — `litestone/src/core/client.js`
- `db.$readAs(accessor, row, principal)` — the row as that principal would read it, for a broadcast; fails closed — `litestone/src/core/client.js`
- `db.$checkWrite(accessor, op, row, changes?)` — would this client's caller be let make this write, for a write that does not reach the table first (a claimed mirror's forward); a verdict, gate and grid and row policy, never field or transition (`FJS-D1162`) — `litestone/src/core/client.js`
- `db.$levelOf(accessor?, principal?)` — the level the app's own `getLevel` grades a caller at; `null` is *cannot grade* — `litestone/src/core/client.js`
- `db.$primaryKey(accessor)` — the key's columns in key order — `litestone/src/core/client.js`
- `db.$mirrorKey(accessor)` — the column `@@mirror(key:)` names, or `null` — `litestone/src/core/client.js`
- `db.$claimsFor(principal)` — the claims the schema reads off a row pointing at the caller — `litestone/src/core/client.js`
- `db.$protectedFields(accessor)` — which columns are guarded, encrypted or hashed — `litestone/src/core/client.js`

**Schema → API/UI**
Detail: `references/schema.md`
- `generateJsonSchema(schema)` — the schema as JSON Schema; `$defs` stays whole; snapshot-gated — `litestone/src/jsonschema.js`
- `ctx.system` — the `@system` columns this call supplies; hooks add to the Set — `junction/src/core/context.ts`
- `ctx.transients` — the `@transient` half of a payload, lifted off `ctx.data` — `junction/src/core/litestone.ts`
- `ServiceTypes` — the schema's types on the far side of the wire, audience-split — `litestone/src/tools/typegen.js`
- `@label` → `title`, validator messages → `x-messages` — the keyword table both validators look up — `litestone/src/jsonschema.js`
- `buildFieldRules()` / `validateAgainstFields()` / `coerceToSchema()` / `normalizeBlanks()` — client-side coerce → blankToNull → validate — `sierra/src/resource/field-rules.js`
- `controlFor(rule, {field, model})` / `formFieldList(fields, {only, except, model})` — the one place a field becomes a control; `registerControl` is the way in — `sierra/src/resource/field-rules.js`
- `labelFieldInfo(fields, fallback, declared)` — which column identifies a row to a person — `sierra/src/resource/field-rules.js`
- `x-values` — a declared value set, from the schema to the request a picker sends — `litestone/src/jsonschema.js`
- `resource.options(field)` — what a picker offers; `error` separates *none* from *could not ask* — `sierra/src/resource/resource.js`
- `toFieldErrors(err)` — a thrown value → per-field messages — `sierra/src/resource/field-rules.js`
- `$context.form` — the form context every control resolves from; `reportInvalid` goes the other way — `ui/components/forms/Form.mesa`
- `buildRelations()` / `buildGate()` / `canAtLevel()` — `x-relations` and `x-gate` on the client; the gate is an affordance only — `sierra/src/resource/field-rules.js`
- `x-version` — the `@version` column an update carries back — `litestone/src/jsonschema.js`
- `x-rank` — which column a board orders by and the columns that are its scope — `litestone/src/jsonschema.js`
- `retryable` — race or refusal on a 409, the one thing a status cannot carry — `junction/src/core/errors.ts`
- `buildTransitions()` / `transitionsAt()` — `x-transitions`, the gate half of a move; `refusedBy` — `sierra/src/resource/field-rules.js`
- `buildCommitments()` / `commitmentsAt()` — `x-commitments`, the date a `@system` move falls due — `sierra/src/resource/field-rules.js`
- `modelNameFor()` / `schemaFor()` — service name → model, over `toolbelt/inflect` — `sierra/src/resource/schema-registry.js`
- `authUserModel(db)` / `authMachineryModels(db)` — auth's two `.lite` files, split by owner — `auth/schema.ts`
- `extend model X { … }` — what an app says about a model it did not write; adds only — `litestone/src/core/parser.js`
- `attachments` — what the app needs and does not own, checked at startup against the environment — `junction/src/core/attachments.ts`

**Machine ↔ control plane**
Detail: `references/api-internals.md`
- `app.conduit.receive(receiver)` / `Dialect` — the receiving end of a Provider: a connector's dialect, an app's receiver, conduit's order (`accept()`, beside the types) and applied-not-seen receipts (`FJS-D899`) — `conduit/src/conduit.ts`
- `app.conduit.mirror(claim)` / `mirrored(accessor)` — a connector's claim on the models a Provider feeds; junction's generated writes forward through it (`FJS-D1125`) — `conduit/src/mirror.ts`, `junction/src/core/litestone.ts` (`mirrorClaimFor`)
- `signRequest()` / `verifyRequest()` — what a signed machine-to-machine request is — `toolbelt/src/signature/signature.js`
- `requestMeta().traceparent` / `.tracestate` — the inbound W3C trace, carried verbatim into conduit's `trace` — `junction/src/core/context.ts`
- `ctx.raw.rawBody` — the body as bytes, for a signature — `junction/src/transport/http.ts`

**API internals**
Detail: `references/api-internals.md`
- `$` / `enterCall(ctx, fn)` / `currentCall()` — the service call in progress, ambient; throws outside a call — `junction/src/core/context.ts`
- `$.config` / `app.configFor(tenant)` — config at call scope, per tenant — `junction/src/core/config-scope.ts`
- `$.log` — the logger bound to this call's correlation id, user and tenant — `junction/src/core/context.ts`
- `bridge.toContext()` / `toResponse()` — transport ↔ service — `junction/src/transport/bridge.ts`
- `toFrameworkError()` — a thrown value → HTTP status; give an owned error class a `status` — `junction/src/core/errors.ts`
- `wrapResult(raw, service, method)` / `unwrapResult()` / `isServiceResult()` — the result envelope, both sides of the wire — `junction/src/core/envelope.ts`
- `enterRequest(src, fn)` / `reenterAs(user, fn)` — the one owner of the request store — `junction/src/core/context.ts`
- `ctx.directives` — `$`-params, parsed by the bridge alone — `junction/src/transport/bridge.ts`
- `collectCustomMethods(def, name, methods?)` — is this key an option or a method — `junction/src/core/service.ts`
- `CALL_OPTIONS_AT` — which argument of each `ServiceCaller` method holds `CallOptions` — `junction/src/core/app.ts`
- `svc.pipelines(appHooks)` — the hook chain, memoized — `junction/src/core/service.ts`
- `svc.describe()` — what this service is, for `/manifest`, OpenAPI and `/metrics` — `junction/src/core/service.ts`
- `isBuiltService(v)` / `Symbol.for('junction.service')` — has `buildService` already built this (`createService` only returns the definition; the registry builds) — `junction/src/core/service.ts`
- `normalizePrefix()` — the one owner of `apiPrefix` — `junction/src/core/app.ts`
- `ctx.enqueue(job, payload)` / `deliverOutbox(app)` — the durable effect, inside the call's transaction — `junction/src/plugins/outbox/engine.ts`
- `claimIdempotency(ctx, key, config)` — claimed once in `callService`, for both transports — `junction/src/core/idempotency.ts`
- Plugin protocol `{ name, register, boot, work, ready, shutdown, requires }` — `register` is sync, async setup goes in `boot()`, and anything on a clock (a worker, a poller, a timer) goes in `work()`, which `_startOnce()` skips so `junction call` and the snapshot tools start nothing (`FJS-D551`) — `junction/src/core/app.ts`
- `runStartPhases(bindHost)` — the one startup list — `junction/src/core/app.ts`
- `IAuth.verifySession(token)` — inbound auth; junction accepts `SessionVerifier` — `junction/src/auth/types.ts`
- `app.withDb(fn)` / `app.onTenantClient(observer)` — `$.db` for work that holds no ctx — `junction/src/core/app.ts`
- `app.principal()` / `app.runAs(userId, fn)` — the seam deferred work runs through — `junction/src/core/app.ts`
- `createLitestoneAuth(db, { sessionFields })` — the one place an app's `User` columns reach the session — `auth/auth.ts`
- `manifest()` + litestone `status()` — migration state into `/manifest` — `junction/src/plugins/manifest/index.ts`
- `app.registerMetricsSource(name, fn)` / `app.registerReadiness(name, fn)` — what a plugin says about itself in `/metrics` and `/health` — `junction/src/core/app.ts`
- `app.registerDevService(name, { url, note })` — a sidecar listener, announced — `junction/src/core/app.ts`
- `devtools({ port, auth })` — the dev console on 8503; fails closed in production — `junction/src/plugins/devtools/index.ts`

**API → UI**
Detail: `references/api-ui.md`
- `client.setCallHeader(name, value)` + `config.http.callHeaders` — a per-call header over either transport, allow-listed — `junction/src/client/index.ts`
- `x-fjs-build` + the `connected` frame's `build` → `client.stale` — which build the browser is on — `junction/src/core/build-id.ts`
- `wsSend()` / `flushSendQueue()` — put this frame on that socket — `junction/src/transport/send-queue.ts`
- **A broadcast is GRADED per recipient, in cohorts** — `gradeRecipients` asks `$readAs` once per principal, and on a channel whose resolver answers no claim, again under each claim it answers for that principal on their other channels — `junction/src/transport/channels.ts`
- `announce()` hook + `app.channel(name)` — real-time; `callService` is the one announcement point — `junction/src/transport/channels.ts`
- **Transport: WebSocket when one is connected, HTTP as the fallback.** — `verifyTransportParity()` asks whether they agree
- `createJunctionClient()` / `client.resource(name)` — the browser client — `junction/src/client/index.ts`
- `connectApp()` / `createResource(name, { app })` — a Resource over ANOTHER app: its client, its schema table — `sierra/src/resource/index.js`
- `resource.save(data, { mode })` — the one owner of *write this record* — `sierra/src/resource/resource.js`
- `resource.move(id, { after, before, into })` — a drag as one patch; the key minted on the device with `toolbelt/rank`, the one minter litestone uses too — `sierra/src/resource/resource.js`
- `client.auth.*` — the browser half of `@frontierjs/auth` — `junction/src/client/index.ts`
- `signIn` → `completeSignIn(code)` — a session or a challenge; the client holds the ticket — `junction/src/client/index.ts`
- `client.auth.providers()` + `OAUTH_ERRORS` / `session.oauthMessage` — which providers exist, and what an OAuth error means — `junction/src/client/index.ts`, `sierra/src/resource/session.js` (`OAUTH_ERRORS`)
- `tokenStorage` on the client + `session` in sierra — one owner for the token, one shape for the session — `junction/src/client/index.ts`
- `client.entries` / `resource.record(id)` — one entry per row keyed by model; a list is a view — `junction/src/client/entries.ts`
- `matchesQuery(fields, record, query)` — is a pushed record still in this list — `toolbelt/src/match/match.js`
- `$after` / `endCursor` / `tethered().more()` — a live list grows a keyset window — `toolbelt/src/directives/directives.js`
- `comparatorFor(orderBy)` — the one reading of `orderBy` and `select` — `toolbelt/src/query/query.js`

**UI**
Detail: `references/ui.md`
- `*.mount.js` — a package's routes, mounted by one file — `sierra/src/scanner/walk.js`
- `page.query` / `page.directives` — the URL split exactly as the bridge splits a request — `sierra/src/router/index.js`
- `watchProxy()` / `createSignal()` / `createRoot(fn)` — the reactive seam and lifetime ownership — `mesa/src/runtime.js`
- `mount(label, Component, {props, root})` — page entry; registers the delegation root — `mesa/src/runtime.js`
- `renderComponent(src, opts)` — UI → HTML at build time — `mesa/src/render-component.js`
- `appSrcDir(root)` / `appAliasPlugin()` — `@` is the surface's own `src/`, for Vite and prerender alike — `sierra/src/build/app-alias-plugin.js`
- `swapInstances(entries, newFn, newSetMark, label)` — the DOM a hot update replaces; no imports — `mesa/mesa-vite/swap.js`
- `island(anchor, Comp, props, block, meta)` — the island seam; markers are comments — `mesa/src/runtime.js`
- **The theme is a class on `<html>` and Sierra owns the switch** — `sierra.config.js` `theme: {}`
- **There is no cross-package reactivity registry.** — sierra passes `externalReactivityHints: 'strict'`
