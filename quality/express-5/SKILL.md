---
name: express-5
description: >-
  Writes, upgrades and hardens Express 5 (express@5.x, current 5.3) HTTP APIs in Node.js. Covers the
  path-to-regexp v8 route syntax (named wildcards like /*splat, {/:optional} groups, no ? + ( ) in
  paths), the silent behaviour changes that break apps without an error (res.send(404) and
  res.json(obj, 201) now reply 200, res.redirect('back'), req.query getter and "simple" parser,
  urlencoded extended=false, req.body undefined), async error forwarding, safe JSON error handlers
  that never leak stack traces, and production defaults (body limits, trust proxy, x-powered-by).
  Use when adding routes or middleware to an Express app, migrating or bumping express from 4 to 5,
  fixing "Missing parameter name", "Unexpected ?" or "TypeError: ... is not a function" after an
  upgrade, writing an Express error handler or 404 handler, or reviewing an Express API for
  security.
license: MIT
---

# Express 5

Facts below are for **express@5.3.0** (Oct 2026), which ships `router@2` (path-to-regexp 8),
`body-parser@2` and requires Node.js 18+. Check what the project actually runs before you write code:

```sh
npm ls express router path-to-regexp body-parser
```

If it prints `express@4.x`, the Express 4 rules you already know apply. Everything here is about 5.x.

## The two classes of breakage

Express 5 breaks code in two ways. The first is loud and easy. The second is why upgrades ship bugs.

**Loud: throws at startup or on the first request.** You will see it in any test run.

| Express 4 code | Error on Express 5 | Write instead |
| --- | --- | --- |
| `app.get('*', h)`, `app.all('*', h)`, `app.use('*', h)` | `Missing parameter name at index 1: *` | catch-all: `app.use(h)` (no path); wildcard: `'/*splat'` |
| `'/assets/*'` | `Missing parameter name` | `'/assets/*assetPath'` (value is an array) |
| `'/:teamId?'`, `'/:invoiceId.:ext?'` | `Unexpected ? at index ...` | `'{/:teamId}'`, `'/:invoiceId{.:ext}'` |
| `'/teams/:teamId(\\d+)'`, `'/a+'`, `'/[a\|b]'` | `Unexpected ( / + / [` | validate in the handler, a RegExp route, or an array of paths |
| `app.del(...)` | `app.del is not a function` | `app.delete(...)` |
| `req.param('teamId')` | `req.param is not a function` | `req.params.teamId` / `req.body?.teamId` / `req.query.teamId`, explicitly |
| `res.sendfile(...)` | `res.sendfile is not a function` | `res.sendFile(relativePath, { root })` |
| `req.acceptsCharset/Encoding/Language` | not a function | the plural forms `req.acceptsCharsets()` etc. |
| `router.param(['a', 'b'], fn)` | `argument name must be a string` | one `router.param(name, fn)` per name |
| `res.status(undefined)`, `res.status('404')`, `res.status(99)` | `TypeError`/`RangeError: Invalid status code` | pass an integer 100-999 |
| `res.redirect('/login', 301)` | `Invalid status code: "/login"` on that request (order is now status first) | `res.redirect(301, '/login')` |

**Silent: no error, wrong response.** Tests that only check bodies, or only the happy path, pass.

| Express 4 code | What Express 5 does | Write instead |
| --- | --- | --- |
| `res.send(404)` | replies **200** with JSON body `404` | `res.sendStatus(404)` (same status and body as Express 4) |
| `res.send(410)` and other bare numbers | replies **200** with that number as the body | `res.sendStatus(410)` |
| `res.json(obj, 202)` / `res.send(obj, 202)` / `res.jsonp(obj, 202)` | ignores the status, replies **200** | `res.status(202).json(obj)` |
| `res.redirect('back')`, `res.location('back')` | sends `Location: back` (a relative URL) | `res.redirect(req.get('Referrer') \|\| fallbackUrl)` |
| `req.query.perPage = 25` then read `req.query.perPage` | `req.query` is a getter that re-parses the URL on every access; the write is lost | keep derived values in local variables |
| `req.query = {...}` | throws in strict mode (`only a getter`) | same: local variables, or `res.locals` |
| `?where[state]=open` read as `req.query.where.state` | default `query parser` is `"simple"`: you get `{ 'where[state]': 'open' }` | `app.set('query parser', 'extended')` if clients send bracket syntax |
| `express.urlencoded()` with forms posting `contact[phone]=...` | `extended` defaults to `false`: flat keys | `express.urlencoded({ extended: true })` when nested form fields exist |
| `const { handle } = req.body` in a route that may get no body | `req.body` is `undefined` (was `{}`): `TypeError` | `req.body ?? {}` or validate `req.body` first |
| `'/*'` renamed to `'/*splat'` but the handler still reads `req.params[0]` | `req.params[0]` is `undefined`; the value is `req.params.splat`, an **array of decoded segments** | `req.params.splat.join('/')` |
| optional param unmatched | key is **absent** (was `undefined`) | `req.params.ext ?? defaultExt` |
| `req.params.hasOwnProperty('teamId')` | `req.params` has a null prototype (string paths): throws | `Object.hasOwn(req.params, 'teamId')` or `'teamId' in req.params` |
| `req.host` | keeps the port (`example.com:8080`) | `req.hostname` for the name only |
| `express.static('public')` serving `/.well-known/...` | dotfiles and dot-directories are ignored (404) by default | mount `.well-known` with `{ dotfiles: 'allow' }` |
| `res.clearCookie(name, { maxAge })` | `maxAge`/`expires` are ignored | nothing to do unless you relied on it |

When you migrate, go through the silent table line by line over the whole codebase, not only the
code the failing tests touch. [references/migration-checklist.md](references/migration-checklist.md)
has a grep for every row and the before/after for each.

## Route paths (path-to-regexp 8)

| Need | Path | `req.params` for an example request |
| --- | --- | --- |
| one segment | `/teams/:teamId` | `/teams/t-9` → `{ teamId: 't-9' }` |
| literal suffix | `/invoices/:invoiceId.pdf` | `/invoices/INV-77.pdf` → `{ invoiceId: 'INV-77' }` |
| optional suffix | `/invoices/:invoiceId{.:ext}` | `/invoices/INV-77` → `{ invoiceId: 'INV-77' }`; `.html` → `{ invoiceId, ext: 'html' }` |
| optional segment | `/teams/:teamId/avatar{/:variant}` | `/teams/t-9/avatar` → `{ teamId: 't-9' }` |
| one or more segments | `/assets/*assetPath` | `/assets/img/hero%20v2.png` → `{ assetPath: ['img', 'hero v2.png'] }` |
| zero or more segments | `/assets{/*assetPath}` | `/assets` → `{}` |
| everything incl. `/` | `/{*splat}` | `/` → `{}` |
| catch-all 404 | `app.use(handler)` | no path at all |
| name that is not an identifier | `/:"asset-id"` | `{ 'asset-id': '...' }` |
| a literal reserved char `()[]?+!` | escape it: `'/v\\(1\\)'` matches `/v(1)` | |
| a digits-only param | `/teams/:teamId`, then reject non-digits in the handler (or a RegExp route) | |

Rules that save time:

- `/*splat` does **not** match the bare prefix (`/assets/*assetPath` does not match `/assets` or
  `/assets/`). Use `{/*assetPath}` when the bare prefix should match too.
- Wildcard values are already URL-decoded per segment. Join with `/`; never string-concatenate the
  array (`${req.params.assetPath}` gives `img,hero v2.png`).
- Register the specific route before the general one when both could match
  (`/:invoiceId.pdf` before `/:invoiceId`), or use one route with `{.:ext}` and branch.
- RegExp routes still work (`app.get(/^\/legacy-assets\/(.+)$/, ...)`, numbered `req.params[0]`), so
  they are a valid escape hatch when the string syntax cannot express a pattern.
- In TypeScript (`@types/express@5`), route strings infer param types: wildcards are `string[]` and
  `{...}` params are optional. Let the inference catch `req.params.assetPath.split` mistakes.

More cases, including `app.param`, `mergeParams` and the error messages, are in
[references/routing.md](references/routing.md).

## Async handlers and errors

Express 5 forwards a **returned** rejected promise to the error middleware, exactly as `next(err)`.
`async` handlers therefore need no wrapper and no `express-async-errors`/`express-async-handler`.

```js
app.get('/teams/:teamId/members', async (req, res) => {
  const team = await teams.find(req.params.teamId) // a rejection goes to the error handler
  if (!team) throw new ApiProblem(404, 'No team with that id')
  res.json(await members.listFor(team))
})
```

Express only sees promises the handler returns. These still need `next(err)` or `await`:

```js
// BAD: the promise is not returned. A rejection is unhandled and, on Node's default
// --unhandled-rejections=throw, kills the process. The request also never gets a response.
app.post('/teams/:teamId/archive', (req, res) => {
  teams.archive(req.params.teamId).then((team) => res.json(team))
})

// GOOD (either)
app.post('/teams/:teamId/archive', async (req, res) => {
  res.json(await teams.archive(req.params.teamId))
})
app.post('/teams/:teamId/archive', (req, res, next) => {
  teams.archive(req.params.teamId).then((team) => res.json(team), next)
})
```

Callbacks (`fs.readFile(p, cb)`), timers, event emitters and streams are not promises: pass errors to
`next` yourself, inside the callback.

### An error handler that is safe in production

The built-in final handler replies with **HTML and the full stack trace** unless
`NODE_ENV=production`. Never rely on the environment variable: install your own last middleware. This
one answers with RFC 9457 problem details; keep whatever envelope the API already documents.

```js
import { STATUS_CODES } from 'node:http'

const problem = (res, status, detail) =>
  res
    .status(status)
    .type('application/problem+json')
    .json({ type: 'about:blank', title: STATUS_CODES[status], status, ...(detail && { detail }) })

// Last two app.use calls, after every route.
app.use((req, res) => problem(res, 404, 'No such route'))

app.use((err, req, res, next) => {
  if (res.headersSent) return next(err) // let Express abort a response that already started
  const status = err?.status ?? err?.statusCode
  if (Number.isInteger(status) && status >= 400 && status < 500) {
    return problem(res, status, err.expose === false ? undefined : err.message)
  }
  console.error(err) // log the details server-side, never send them
  problem(res, 500)
})
```

Decision rules for the handler:

- Keep 4xx statuses from upstream middleware. body-parser errors carry `status` and `type`
  (`400` + `entity.parse.failed` for malformed JSON, `413` + `entity.too.large`, `415` for an unsupported
  charset or encoding). A handler that maps everything to 500 turns client mistakes into alerts.
- Only expose messages that are meant for clients: your own error classes, or `http-errors` style
  errors with `expose: true` (set for 4xx). For 5xx always send a generic message.
- Never call `res.status(err.status)` without checking it is an integer 100-999: on Express 5 that
  throws inside your error handler and Express falls back to the HTML stack-trace page.
- Map domain errors explicitly (`MissingRecordError` → 404, `VersionConflictError` → 409) instead of
  matching message strings.
- The handler has exactly four parameters `(err, req, res, next)`; Express detects error middleware by
  arity, so keep `next` even when it looks unused.

[references/errors-and-hardening.md](references/errors-and-hardening.md) has an `ApiProblem` class,
validation without extra dependencies, and the full body-parser error table.

## Request parsing defaults (body-parser 2)

| Parser | Default you get | Set explicitly when |
| --- | --- | --- |
| `express.json()` | `limit: '100kb'`, `strict: true` (only objects and arrays), type `application/json` | the endpoint needs a different size cap; set it per route if one route takes uploads |
| `express.urlencoded()` | `extended: false`, `parameterLimit: 1000`; with `extended: true` nesting `depth` is 32 | the form posts nested `a[b]` fields |
| any parser | `req.body` stays `undefined` when there is no body or the type does not match | always: handlers must not assume an object |

Since 5.3.0 an invalid `limit` value throws when the parser is created instead of silently disabling
the size check. Use a number of bytes or a `bytes` string like `'256kb'`.

## Production defaults checklist

Apply these to any Express app you create or touch, unless the project already does it differently:

- [ ] `app.disable('x-powered-by')` (on by default), or `helmet()` if the project already uses it.
- [ ] A 404 handler (`app.use` with no path) and an error handler, as above, registered last, both
      answering in the API's format instead of the HTML defaults.
- [ ] Body parsers with an explicit `limit` sized for the API; a larger limit only on the routes that
      need it (mount that parser on the route, not globally).
- [ ] Validate `req.params`, `req.query` and `req.body` at the edge (types, ranges, lengths) and reply
      400 with a stable error shape. Treat everything in them as untrusted strings or arrays: even the
      simple parser turns `?tag=a&tag=b` into `['a', 'b']`, and the extended one builds nested objects.
- [ ] `trust proxy` set to the real topology (`1` hop, or the proxy subnet), never `true` unless the
      last proxy overwrites `X-Forwarded-For`, `-Host` and `-Proto`. Otherwise `req.ip` is spoofable,
      which defeats rate limits and audit logs.
- [ ] `res.sendFile(relativePath, { root: ASSETS_ROOT })` for user-influenced paths (it rejects `..`
      with 403), never `path.join(ASSETS_ROOT, userInput)` followed by an absolute `sendFile` or
      `fs.readFile`.
- [ ] Redirect targets from user input are checked against an allow-list (open redirects).
- [ ] `app.listen(port, (err) => { if (err) throw err })`: listen errors like `EADDRINUSE` are passed
      to the callback in Express 5 instead of being thrown.

## Migration procedure (4 → 5)

1. Confirm the installed version (`npm ls express`) and the Node version (18+).
2. Start the app or run the tests once and fix every **loud** error from the first table. The process
   cannot start until all route strings parse.
3. Grep the whole codebase for every row of the **silent** table
   ([references/migration-checklist.md](references/migration-checklist.md)), including routes no test
   covers. Keep behaviour identical unless the user asks for a change: a bare `res.send(<status>)`
   becomes `res.sendStatus(<status>)` (same status and status-text body), not a new JSON shape.
4. Decide parser settings from the clients, not from the code you see: if any client sends
   `where[x]=` query strings or nested form fields, set `query parser` to `'extended'` and/or
   `urlencoded({ extended: true })`.
5. Remove wrappers made obsolete by native promise support only if they are simple pass-throughs.
6. Write or extend tests for status codes, redirects (`redirect: 'manual'` in `fetch`), empty bodies,
   nested query/form input and the 404/error handlers, then run the whole suite.

The official codemods (`expressjs/codemod`) target mechanical renames: redirect-back, `sendfile`
casing, `req.param`, pluralized `accepts*`, redirect argument order, `app.del`, `sendFile`/`static`
options and status/send argument order. Going by the transform list (Nov 2026), none targets route
path syntax, the query parser, `urlencoded` `extended`, `req.body` or `req.query` writes, so step 3 is
still yours.

## Testing Express apps without extra dependencies

```js
import assert from 'node:assert/strict'
import { after, before, test } from 'node:test'
import { buildServer } from '../lib/build-server.mjs'

let server, origin
before(async () => {
  server = buildServer().listen(0)
  await new Promise((resolve) => server.once('listening', resolve))
  const { port } = server.address()
  origin = `http://127.0.0.1:${port}`
})
after(() => new Promise((resolve) => server.close(resolve)))

test('a missing team is a problem+json 404', async () => {
  const res = await fetch(`${origin}/teams/t-missing/members`, { redirect: 'manual', signal: AbortSignal.timeout(5000) })
  assert.equal(res.status, 404)
  assert.match(res.headers.get('content-type'), /^application\/problem\+json/)
})
```

Export a factory that builds the Express app separately from the `listen` call so tests and production
share the same wiring. Assert status codes on every test: the silent breakages only show up there.

## Anti-patterns

| Anti-pattern | Fix |
| --- | --- |
| Adding `express-async-errors` to an Express 5 app | delete it; return or await the promise |
| `app.all('*', fallback)` | `app.use(fallback)` after all routes |
| `res.status(err.status).json(...)` | validate the status, default 500 |
| Sending `err.message` or `err.stack` for 5xx | generic message to the client, `console.error(err)` (or the app logger) server-side |
| Checking `process.env.NODE_ENV === 'production'` to hide stacks | a custom error handler that never sends them |
| `req.query.perPage = Number(req.query.perPage) \|\| 25` | `const perPage = Number(req.query.perPage) \|\| 25` |
| `const { handle } = req.body` | `const { handle } = req.body ?? {}`, then validate |
| `res.sendFile(path.join(ASSETS_ROOT, req.params.assetPath.join('/')))` | `res.sendFile(req.params.assetPath.join('/'), { root: ASSETS_ROOT })` |
| Downgrading to Express 4 to make an upgrade pass | finish the migration; a downgrade undoes the work that was asked for |
| An error handler with three parameters `(err, req, res)` | four parameters: with three, Express runs it as ordinary middleware on every request that reaches it |
