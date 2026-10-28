---
name: api-hazards
description: Junction — a service, the hook pipeline, HTTP/WS transport, a raw route, a plugin, `ctx`, a job or cron. Correct-but-surprising behavior in the API realm; use when touching any of them.
---

# API-realm live hazards

**Correct behavior you have to know about.** Things that are *wrong* live in `ISSUES.md`, one id each; things that are *fixed* live in git. If a rule here is pinned by a test that cannot be deleted quietly, it does not need to be here.

**The index below is each hazard's rule; its section's reference file holds the rest** — the mechanism, the measurement, and what it refuses. Read that file before changing code the rule is about. A term the rules use without defining (`asSystem()`, `@system`, `callService`) is one line in `references/glossary.md` under `bridge-index`.

## `ctx` and the call
Detail: `references/ctx-and-the-call.md`

- **`ctx.params` does not exist anywhere in Junction, and `ctx.route` is not it.**
- **Absent is not null on `auth`.**
- **`ctx.signal` aborts when the caller leaves, and a nested call does not inherit it.**
- **A payload key that is not a column is declared `@transient`, and it arrives at `ctx.transients` — never at `ctx.data`.**
- **A payload key that names no field of the model is a 400; one that names a field the caller may not WRITE is dropped in silence** (`FJS-889`)
- **`PUT` to an id that does not exist is 404 and does not create the row** (`FJS-D207`)
- **A write by id the row policy refuses is 403 for a row the caller can read, 404 for one they cannot** (`FJS-1750`)
- **`update` is `patch` with an id REQUIRED, and it MERGES** (`FJS-D179`)
- **The METHOD decides list vs single.**

## The hook pipeline
Detail: `references/the-hook-pipeline.md`

- **A custom method takes the model's READ gate as a floor, and declares anything above it** (`FJS-826`)
  - **A method authenticated by something that is NOT a session states `gate: 0`**
  - **Declaring one gate means naming the whole surface**
- **The gate runs before anything an app wrote, and `validated:` is the phase after the derived layer.**
- **An `Idempotency-Key` on a mutating request executes once and replays the first answer**
  - **A custom method is a write until it declares `read: true`** (`FJS-D505`) — undeclared, a keyed search keeps its answer, query and all, for 24 hours, and the bus announces it; declared, a write inside it would run again on a keyed retry and go unannounced, so `$.db` throws a 500 at the first `create`/`update`/`remove`/`*Many`/`upsert`/`transition` (`FJS-D581`, `FJS-1477`) — `asSystem()`, an imported client and raw SQL walk past it
- **An irreversible effect belongs in `ctx.afterCommit(fn)`, not in an `after` hook.**
- **Under `transactional:`, a result carrying a non-empty `errors` is a 422 and a rollback** (`FJS-2149`)
- **A `mailer.send()` that answers `sent` sends everything the message declared — including `cc`, `bcc`, `attachments` and `headers`** (`FJS-895`)
- **A reply tag proves the holder RECEIVED our mail, not who is holding it; attribution also needs `from` to be the address the mail went to** (`FJS-D1091`, `FJS-D1092`)
- **A recurring `app.scheduler` job does not overlap itself, and the tick it dropped is COUNTED** (`FJS-896`)
- **The log level is a CELL shared down the whole tree, and `setLevel` moves all of it** (`FJS-897`)
- **A job records the request that queued it** (`FJS-897`)
- **`ctx.enqueue(job, payload)` is the durable half, and it is a second VERB because a closure cannot be persisted** (`FJS-D35`)
  - **A row that keeps failing is given up on, and `dead` is the only thing that says so** (`FJS-778`)
  - **The relay's walk is COLD, and a tick is ONE walk.**

## Routes, query and headers
Detail: `references/routes-query-and-headers.md`

- **A query string is PARSED, and the schema still wins.**
- **Raw routes (`app.get`/`app.post`) take `{id}`, not `:id`**
- **`apiPrefix` moves EVERY route the app registers**
- **Every READ carries `$withDeleted`; on a WRITE only `update`/`patch` by id do.**
- **A wire `$limit` above the service's `paginate.max` is a 400, not a clamp.**
- **`hasRoute()` is a matching question, not an existence one**
- **A header the caller varies per call must be DECLARED, or it works until the socket connects.**
- **A raw route's own `new Response(readable)` is held to its end for a gzip caller; build a stream with `ctx.stream()` or name `content-encoding`** (`FJS-D509`)
- **The client's address is declared, never discovered.**
- **An API on a sibling subdomain needs no cookie `Domain`; the cross-origin list is `cors.origins` + `credentials` + `csrf.origins`** (`FJS-2655`) — measured in Chrome: a host-only cookie rides only a fetch that says `credentials: 'include'`, and `app.localhost` / `api.localhost` are NOT the same site (`localhost` has no registrable domain). `fli deploy` derives the list as `FRONTIER_CORS_ORIGINS` (`FJS-D912`).
- **Above 128 MB, a declared length over `http.maxBodySize` is refused by Bun, not by junction** (`FJS-3090`)
- **A `{ body: 'stream' }` route bounds nothing a chunked sender writes, and its credential verifier sees an empty body** (`FJS-D1159`)

## Sockets
Detail: `references/sockets.md`

- **A socket stays alive because the SERVER pings it, and an app calls nothing.**
- **Never call `ws.send()` directly.**
- **`app.ws` is the raw door: no `connected`, no `{type:'error'}`, a refused frame closes `1008`, and the path takes `apiPrefix`** (`FJS-D688`)
- **A `removed` frame goes only to a reader the row's BEFORE-image admitted**, and a write with no before-image sends none (`FJS-1742`, `FJS-D1199`)
- **An upgrade carrying an Origin is 403 unless the csrf list names it or its host is `Host`**, csrf installed or not (`FJS-D1207`)

## Secrets and the log line
Detail: `references/secrets-and-the-log-line.md`

- **The logger redacts a credential by NAME, on both paths, and it is a floor rather than a proof** (`FJS-775`)
- **`defineEnv` will not quote a value it must not, and infers that from the NAME.**
- **An adapter cache is keyed on `$schema`, never on the client** (`FJS-777`)
- **`$.log` inside a call, `app.logger` outside one** (`FJS-D772`)

## Plugins, config and autoload
Detail: `references/plugins-config-and-autoload.md`

- **A plugin reads `junction.config.js` in `boot()`, never in `register()`.**
- **A missing config DIRECTORY is not a missing config file.**
- **Where an app's services are is PROBED, not derived**
- **An `app.<slot>` no plugin installed THROWS on read; `'jobs' in app` is the presence test**

## The four snapshots
Detail: `references/the-four-snapshots.md`

- **What an app ANSWERS, what it RUNS with no caller, what it can TELL somebody, and who a caller BECOMES are each committed beside the API, in `api/`.**
- Plus a table and prose that are only in the reference file.

## Auth and the principal
Detail: `references/auth-and-the-principal.md`

- **`IAuth.sessionFor(userId)` is how a principal is rebuilt without a credential**
- **A bearer token is the credentials list's last entry: `verifySession`, then `verifyApiKey` when that answers null**
- **`signedRequest` remembers a nonce in ITS OWN process, twice the window, unless `seenNonce` is passed**
- **`bearerClaim` refuses a presented token that does not work (401); no token stays anonymous**
- **A socket reads its cookies from the upgrade; a changed cookie reaches it by a reconnect** — the client cycles only on a response it read, so a redeem goes through `client.fetch`
- **`bearerClaim` refuses a session beside a grant (400), BEFORE the grant is read** — a dead token beside a session is the same 400, so the request's shape is not an oracle for which tokens exist. A store whose signed-in shoppers still send the basket header states `session: 'merge'` or every one of them is refused (`FJS-D832`).

## Jobs and the clock
Detail: `references/jobs-and-the-clock.md`

- **Caravan owns the clock; `app.scheduler` is in-process only** (`FJS-D36`)
- **A background job runs as whoever asked for it, and a job nobody asked for runs as the app.**
- **A job attempt has no bound unless one is declared, and `oldestRunningMs` is how you see the ones that do not.**
- **Caravan's `unique` is a lock on work IN FLIGHT, not an idempotency key.**
- **A restored database's outbox sends nothing it already held until an operator says so** (`FJS-D665`).
- **A job in `jobs/` is named by its file and declares its own schedule.**
- **A cache value is JSON, and what JSON would LOSE is refused at `set()`.**
- **The docs page is hand-written HTML with two caller-supplied values in it.**
- **A battery names a vendor in a comment and never in a call** (`FJS-D215`)
- **Nothing here mocks a module, and the reason is a design rule.**
- **A test may not name a port, and the reason is the runner.**
- Plus a table and prose that are only in the reference file.
