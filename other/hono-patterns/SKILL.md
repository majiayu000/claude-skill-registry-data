---
name: hono-patterns
description: 'Use when building APIs on Hono (Cloudflare Workers, Bun, Deno, Node), debugging route ordering, wiring middleware, validating with @hono/zod-validator, returning streaming responses, configuring CORS with credentials, handling errors via app.onError, or composing typed RPC clients. Triggers: c.env binding types, c.header + c.redirect interaction, missing await next() bugs, Set-Cookie not attaching to redirect, route-precedence surprises, JWT middleware setup, hono/client typed RPC end-to-end. NOT for Express/Fastify/Koa idioms, tRPC/GraphQL paradigms, or Next.js Route Handlers.'
category: Backend & Infrastructure
tags:
  - hono
  - cloudflare-workers
  - bun
  - edge
  - middleware
  - typescript
---

# Hono Patterns

Hono is a small router with a strong middleware model and ergonomic typing. Most surprises come from middleware ordering, deferred header semantics, and the `c.env`/`Variables` generic dance.

## When to use

- Designing an API on Workers, Bun, or Deno where Express would be overkill.
- Type-safe end-to-end RPC client (`hono/client`).
- Streaming SSE / NDJSON responses.
- A redirect-driven login flow where Set-Cookie must attach to the response.
- CORS with credentials, where `*` won't work.
- Custom error responses through `app.onError`.

## Core capabilities

### The `Hono` generic — typed bindings and locals

```ts
type Bindings = {
  DB: D1Database;
  KV: KVNamespace;
  WINDAGS_INTERNAL_TOKEN: string;
};

type Variables = {
  user: { id: string; role: 'admin' | 'member' };
  startedAt: number;
};

const app = new Hono<{ Bindings: Bindings; Variables: Variables }>();
```

Now `c.env.DB` is typed `D1Database`; `c.var.user` is typed; `c.set('user', …)` and `c.get('user')` are checked.

### Route ordering

Hono matches in registration order. Specific before wildcard:

```ts
app.get('/v1/skills/search', searchHandler);   // specific
app.get('/v1/skills/:id', getOneHandler);      // param
app.all('/v1/*', fallback);                    // catch-all LAST
```

Mounting sub-apps:

```ts
const v2 = new Hono<{ Bindings: Bindings }>();
v2.get('/skills', listV2);
app.route('/v2', v2);

// Or basePath for the whole app:
const api = new Hono().basePath('/api');
```

### Middleware

The chain is request → middleware → handler → middleware-after → response. `await next()` is where you switch direction.

```ts
app.use('*', async (c, next) => {
  const start = Date.now();
  await next();
  c.header('Server-Timing', `total;dur=${Date.now() - start}`);
});

app.use('/admin/*', async (c, next) => {
  const session = c.req.header('Cookie');
  if (!session) return c.text('forbidden', 403);
  c.set('user', await loadUser(session));
  await next();
});
```

Forgetting `await next()` is the most common bug. The handler never runs and the request hangs at middleware.

### Validator middleware

```ts
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const createSkill = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/).max(80),
  name: z.string().min(1).max(120),
  tags: z.array(z.string()).max(20).optional(),
});

app.post(
  '/v1/skills',
  zValidator('json', createSkill),
  async (c) => {
    const body = c.req.valid('json'); // typed, narrowed
    await c.env.DB.prepare(
      'INSERT INTO skills (id, name, tags) VALUES (?, ?, ?)'
    ).bind(body.id, body.name, JSON.stringify(body.tags ?? [])).run();
    return c.json({ ok: true }, 201);
  },
);
```

Validation slots: `'json' | 'form' | 'query' | 'param' | 'header' | 'cookie'`. Each adds a typed accessor.

### `c.header()` + `c.redirect()` — the deferred-headers model

```ts
app.get('/_internal/login', (c) => {
  const token = c.req.query('token');
  if (token !== c.env.WINDAGS_INTERNAL_TOKEN) return c.text('forbidden', 403);
  c.header(
    'Set-Cookie',
    `session=${token}; HttpOnly; Secure; SameSite=Lax; Path=/_internal; Max-Age=${30*86400}`,
  );
  return c.redirect('/_internal/dashboard');
});
```

`c.header()` registers a deferred header on the context; the final `Response` (whether from `c.json`, `c.text`, or `c.redirect`) merges those deferred headers. The cookie WILL attach. If a downstream observer says it didn't, the issue is browser-side (SameSite=Strict on a redirect) or upstream (proxy stripping headers), not Hono.

### Streaming

```ts
import { streamSSE } from 'hono/streaming';

app.get('/v1/events', (c) => {
  return streamSSE(c, async (stream) => {
    let id = 0;
    while (!stream.aborted) {
      await stream.writeSSE({ id: String(id++), event: 'tick', data: JSON.stringify({ now: Date.now() }) });
      await stream.sleep(1000);
    }
  });
});
```

`stream.aborted` flips when the client disconnects — check it in any long loop or you'll leak.

For raw bytes/NDJSON:

```ts
import { stream } from 'hono/streaming';

app.get('/v1/dump', (c) => stream(c, async (s) => {
  for await (const row of fetchRows()) {
    await s.write(JSON.stringify(row) + '\n');
  }
}));
```

### Error handling

```ts
import { HTTPException } from 'hono/http-exception';

app.onError((err, c) => {
  if (err instanceof HTTPException) return err.getResponse();
  // Log with the right severity; don't leak internals.
  console.error('unhandled', err);
  return c.json({ error: 'internal' }, 500);
});

// Throw a typed error from anywhere:
throw new HTTPException(429, { message: 'rate limited', res: new Response('go slow', { status: 429 }) });
```

`onError` wraps the whole app. Routes that throw end up here unless an explicit try/catch handles them.

### Cookies via `hono/cookie`

```ts
import { setCookie, getCookie, deleteCookie } from 'hono/cookie';

setCookie(c, 'session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'Lax',
  path: '/_internal',
  maxAge: 30 * 86400,
});

const session = getCookie(c, 'session');
deleteCookie(c, 'session', { path: '/_internal' });
```

Helper-based cookies are easier to read than raw `Set-Cookie` strings; both work.

### CORS with credentials

```ts
import { cors } from 'hono/cors';

app.use('/v1/*', cors({
  origin: (origin) => origin?.endsWith('.windags.ai') ? origin : null,
  credentials: true,                    // sends cookies cross-origin
  allowMethods: ['GET', 'POST', 'OPTIONS'],
  allowHeaders: ['Content-Type', 'Authorization'],
  maxAge: 86400,
}));
```

`credentials: true` requires the explicit origin echoed back — `*` won't work and the browser will block.

### Typed RPC client

```ts
// server
const route = app
  .get('/v1/skills/:id', (c) => c.json({ id: c.req.param('id'), name: 'x' }))
  .post('/v1/skills', zValidator('json', createSkill), (c) => c.json({ ok: true as const }));
export type AppType = typeof route;

// client
import { hc } from 'hono/client';
const client = hc<AppType>('https://api.windags.ai');
const res = await client.v1.skills[':id'].$get({ param: { id: 'foo' } });
const data = await res.json(); // typed { id: string; name: string }
```

The client mirrors the server type tree exactly. Refactor a route → the client breaks at compile time.

## Anti-patterns

### Catch-all before specific routes

**Symptom:** Specific routes return 404 / wrong handler responses.
**Diagnosis:** `app.all('*', …)` registered before specific GETs. First match wins.
**Fix:** Register catch-alls last. Use `app.notFound(handler)` for 404 instead of a wildcard.

### Forgetting `await next()`

**Symptom:** Request hangs or returns nothing; logs show middleware ran but handler didn't.
**Diagnosis:** Middleware returned without awaiting `next()`.
**Fix:** Always `await next()` unless you intentionally short-circuit (auth fail, rate limit). Linting rule helps.

### `c.set` without typed Variables

**Symptom:** `c.get('user')` returns `unknown`; downstream code does string casts.
**Diagnosis:** Variables generic not declared.
**Fix:** Add `Variables` to the `Hono<{Bindings, Variables}>` generic. Now both `set` and `get` are typed.

### Heavy work in middleware

**Symptom:** Every endpoint, even health checks, costs 50ms.
**Diagnosis:** Middleware does DB-loaded user-loading or audit-logging on every path.
**Fix:** Scope middleware narrowly (`app.use('/api/v1/*', loadUser)`), or memoize per-request.

### SameSite=Strict on a redirect-driven login

**Symptom:** Browser shows 302 with Set-Cookie; immediate follow-up request to dashboard returns 403.
**Diagnosis:** Strict drops cookies on cross-context navigation in some browsers, including the auto-followed redirect from the login URL.
**Fix:** `SameSite=Lax` for session cookies that ride a redirect.

### Returning a raw `Response` and expecting middleware to mutate it

**Symptom:** Middleware "after `next()`" can't read body, can't set headers reliably.
**Diagnosis:** The middleware mutates `c.res`, but the handler returned a fresh Response that bypassed it.
**Fix:** Either use `c.res = newResponse;` in the handler, or return through `c.json/c.text/c.html/c.body`.

## Quality gates

- [ ] Every route has a validator (zod) or explicit typed parsing.
- [ ] Catch-all routes registered last; `app.notFound` set.
- [ ] Every middleware that intends to continue calls `await next()`.
- [ ] `Bindings` and `Variables` generics declared on the root app.
- [ ] `app.onError` returns a sanitized response — no stack leaks.
- [ ] CORS with `credentials: true` echoes a typed allowlist of origins, never `*`.
- [ ] Streaming endpoints check `stream.aborted` in any long loop.
- [ ] Cookie helpers used over raw Set-Cookie unless a specific reason.

## NOT for

- **Express/Fastify/Koa** — different middleware models, different ergonomics.
- **tRPC/GraphQL** — different paradigms; Hono's RPC is REST-flavored.
- **Next.js Route Handlers** — `app/api/*/route.ts` is a different framework.
- **Pure node http** — Hono's value is the middleware + typing; if you need neither, drop down. No dedicated skill.
- **Cloudflare Workers platform issues** (binding errors, deploy failures, secret upload) — once it's the platform, → `cloudflare-workers-debugging`.
- **Webhook signature verification on Hono routes** — Hono is the framework, not the protocol. → `webhook-receiver-design` for HMAC, raw-body, idempotency.
