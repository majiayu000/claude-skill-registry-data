---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: better-auth
description: >
  Authentication and authorization with better-auth in Spiceflow and TypeScript apps.
  Covers server config with Drizzle adapter (Postgres and SQLite), Spiceflow middleware
  for forwarding auth requests, client setup, session middleware, social and email/password
  auth, server-side session checks, and React client hooks (useSession, signIn, signOut,
  signUp). Also covers device authorization (CLI device flow), bearer token auth,
  server actions with auth, and SQLite Durable Objects (betterAuth inside the DO,
  getCookieCache in the Worker). ALWAYS load this skill when a project uses better-auth.
  Load durable-objects.md when auth tables live in a Durable Object.
  Load mcp.md when adding remote HTTP MCP OAuth (Cursor, Claude, hosted /mcp).
---

# better-auth

better-auth is the most comprehensive authentication framework for TypeScript. It provides email/password, social OAuth, session management, 2FA, and more out of the box. It works with any backend that uses standard Request/Response objects.

Full docs: https://better-auth.com/llms.txt

When you need docs for a better-auth feature not covered in this skill (specific plugin API, config options, edge cases), use WebFetch to fetch `https://better-auth.com/llms.txt`. It contains the full better-auth documentation in a single file optimized for LLMs.

## URL construction

Always use `new URL(path, base)` instead of string concatenation or template literals for building URLs:

```ts
// GOOD
const url = new URL('/api/auth', process.env.BETTER_AUTH_URL)

// BAD
const url = `${process.env.BETTER_AUTH_URL}/api/auth`
const url = process.env.BETTER_AUTH_URL + '/api/auth'
```

`new URL` handles trailing slashes, normalizes paths, and avoids double-slash bugs.

## Installation

### Recommended: `better-auth-drizzle-adapter` (works with drizzle v0 and v1)

Always use `better-auth-drizzle-adapter` (npm) instead of the official `@better-auth/drizzle-adapter`. Three reasons:

1. **drizzle-orm v1 support.** The official `@better-auth/drizzle-adapter` only works with drizzle-orm v0 (^0.45). It crashes on drizzle-orm v1 (1.0.0-beta) with `"model 'user' was not found in the schema object"`. The community adapter is vendored from PR #9489 which adds relations-v2 support.

2. **SQL null bug fixed.** Both the official adapter and the upstream PR code use `eq(column, null)` which generates `column = NULL` in SQL. This is never true (SQL null semantics). It silently breaks device authorization, refresh-token rotation, and any operation using `{ value: null }` WHERE clauses. `better-auth-drizzle-adapter@>=1.0.3` fixes this with `isNull()`/`isNotNull()`.

3. **postgres-js deleteMany fix.** The official adapter's `deleteMany` returns 0 on postgres-js because `Result` extends `Array` and `res.length` is 0 for DELETE without RETURNING. Fixed in `>=1.0.4`.

```bash
pnpm add better-auth better-auth-drizzle-adapter
```

```ts
import { betterAuth } from 'better-auth/minimal'
import { drizzleAdapter } from 'better-auth-drizzle-adapter'

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: 'sqlite' }), // or 'pg'
  // ...
})
```

Use `better-auth/minimal` on Cloudflare Workers to avoid bundling Kysely (~400KB). The `/minimal` entry strips the built-in database layer, so a drizzle adapter is required.

Source: https://github.com/remorses/better-auth-drizzle-adapter

## Server config

Create `src/lib/auth.ts` (or `lib/auth.ts`). Export the auth instance as `auth`.

### Drizzle adapter (Postgres)

```ts
// src/lib/auth.ts
import { betterAuth } from 'better-auth'
import { drizzleAdapter } from 'better-auth-drizzle-adapter'
import { db } from 'db' // drizzle instance from your db workspace package

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'pg',
  }),
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL!,
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 365, // 1 year
    updateAge: 60 * 60 * 24, // refresh expiry every 1 day of activity
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
    },
  },
})
```

### Drizzle adapter (SQLite / Cloudflare D1)

```ts
import { betterAuth } from 'better-auth/minimal'
import { drizzleAdapter } from 'better-auth-drizzle-adapter'
import { db } from 'db'

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'sqlite',
  }),
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL!,
  emailAndPassword: { enabled: true },
  session: {
    expiresIn: 60 * 60 * 24 * 365, // 1 year
    updateAge: 60 * 60 * 24, // refresh expiry every 1 day of activity
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
    },
  },
})
```

### Environment variables

`BETTER_AUTH_URL` is **always a secret**, never a plain env var or hardcoded value. It differs per environment: dev uses `http://localhost:3000`, preview uses the preview deploy URL, production uses the real domain. Treat it the same as `BETTER_AUTH_SECRET`.

**`BETTER_AUTH_URL` must match the Origin header the browser sends.** BetterAuth validates the `Origin` header on every `/api/auth/*` request against the configured `baseURL`. If they don't match, you get `403 {"message":"Invalid origin","code":"INVALID_ORIGIN"}`. This commonly happens when secrets management tools (Sigillo, Doppler) inject the production URL during local dev. Set it correctly in sigillo or doppler with BETTER_AUTH_URL secret. Or use a wrangler.json vars variable. Also make sure sigillo is configured to the dev env locally, check with `sigillo me`

For Cloudflare Workers, put both in `secrets.required` in `wrangler.jsonc`:

```jsonc
{
  "secrets": {
    "required": [
      "BETTER_AUTH_SECRET",
      "BETTER_AUTH_URL",
      "GOOGLE_CLIENT_ID",
      "GOOGLE_CLIENT_SECRET"
    ]
  }
}
```

For Doppler/Sigillo, set per-environment values:

| Variable | development | preview | production |
|---|---|---|---|
| `BETTER_AUTH_URL` | `http://localhost:3000` | `https://preview.example.com` | `https://example.com` |
| `BETTER_AUTH_SECRET` | (random 32+ chars) | (random 32+ chars) | (random 32+ chars) |

```env
BETTER_AUTH_SECRET=  # min 32 chars, generate with: openssl rand -base64 32
BETTER_AUTH_URL=     # MUST be set per env — never hardcode
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

## Schema generation

better-auth manages its own tables (`user`, `session`, `account`, `verification`). Generate the Drizzle schema for them:

```bash
pnpm dlx auth@latest generate
```

This outputs a Drizzle schema file. Add the generated tables to your `src/schema.ts` and run `drizzle-kit generate` + `drizzle-kit migrate` as usual.

When you add plugins that require new tables (2FA, organization, etc.), re-run `pnpm dlx auth@latest generate` to update the schema.

## Spiceflow integration

### Auth route middleware

In Spiceflow, mount better-auth using a `.use()` middleware that forwards requests with the `/api/auth` prefix to `auth.handler()`. If auth returns a 404 (no matching auth endpoint), fall through to your own routes instead of returning the 404:

```ts
import { Spiceflow } from 'spiceflow'
import { auth } from './lib/auth'

export const app = new Spiceflow()
  .use(async ({ request }, next) => {
    if (request.parsedUrl.pathname.startsWith('/api/auth')) {
      const response = await auth.handler(request)
      // Return auth responses (200, 401, 403, etc.) directly.
      // Only fall through on 404 (no matching auth endpoint).
      if (response.ok || response.status !== 404) return response
    }
    return next()
  })
  // ... rest of your routes
```

Use `res.ok || res.status !== 404` instead of just `res.status === 404` so auth error responses (401, 403, 400) are returned directly instead of falling through to your app routes:

```ts
.use(async ({ request }, next) => {
  if (request.parsedUrl.pathname.startsWith('/api/auth')) {
    const response = await auth.handler(request)
    if (response.ok || response.status !== 404) return response
  }
  return next()
})
```

This handles ALL better-auth endpoints (sign-in, sign-up, OAuth callback, session, etc.). The middleware short-circuits for auth paths and returns the auth response directly. Non-auth paths and unmatched auth paths fall through to `next()`.

### Session state + loader

Use `.state()` to resolve the session once in middleware, then expose it to all pages and client components via a `/*` loader. This is the recommended pattern — it's fully type-safe and avoids prop drilling:

```ts
import { Spiceflow, redirect } from 'spiceflow'
import { auth } from './lib/auth'

// Session type — includes both session and user, with plugin-extended fields
type AuthSession = typeof auth.$Infer.Session | null

export const app = new Spiceflow()
  // 1. Auth middleware — forward /api/auth/* to better-auth
  .use(async ({ request }, next) => {
    if (request.parsedUrl.pathname.startsWith('/api/auth')) {
      const response = await auth.handler(request)
      if (response.ok || response.status !== 404) return response
    }
    return next()
  })

  // 2. Session state — resolved once per request via middleware
  .state('session', null as AuthSession)
  .use(async ({ request, state }) => {
    state.session = await auth.api.getSession({ headers: request.headers })
  })

  // 3. Session loader — exposes session to all pages and client components
  // Matched by every page/layout via wildcard. Loader data is merged,
  // so pages can add their own loaders and session is always available.
  .loader('/*', ({ state }) => {
    return { session: state.session }
  })
```

This runs on every request including landing pages. When no session cookie is present, `getSession` returns `null` immediately (no DB query). When a session exists and cookie caching is enabled (which it should always be), `getSession` reads the signed cookie and skips the database entirely. The DB is only hit once every `maxAge` interval (default 5 minutes) to refresh the cache.

Now **every page, layout, and client component** can access the session type-safely:

**In server components (pages/layouts)** — via `loaderData`:

```tsx
.layout('/*', async ({ loaderData, children }) => {
  return (
    <html>
      <body>
        {loaderData.session && <nav>{loaderData.session.user.name}</nav>}
        {children}
      </body>
    </html>
  )
})

.page('/dashboard', async ({ loaderData }) => {
  if (!loaderData.session) throw redirect('/login')
  return <Dashboard user={loaderData.session.user} />
})
```

**In client components** — via `useLoaderData` hook from `spiceflow/react`:

```tsx
'use client'

import { useLoaderData } from 'spiceflow/react'

export function UserMenu() {
  // Type-safe when SpiceflowRegister is declared in the app entry file
  const { session } = useLoaderData('/*')

  if (!session) return <a href="/login">Sign in</a>

  return (
    <div>
      <span>{session.user.name}</span>
      <button onClick={async () => {
        await authClient.signOut()
        window.location.href = '/login'
      }}>Sign out</button>
    </div>
  )
}
```

The `/*` loader matches all pages, so `session` is always available in `useLoaderData`. When multiple loaders match (e.g. `/*` and `/dashboard`), their return values are merged into a single flat object — more specific loaders override less specific ones on key conflicts.

### Protecting API routes

For API routes (not pages), use `state.session` directly since loaders only run for pages:

```ts
.route({
  method: 'POST',
  path: '/api/posts',
  request: z.object({
    title: z.string(),
    content: z.string(),
  }),
  async handler({ request, state }) {
    if (!state.session) {
      return new Response('Unauthorized', { status: 401 })
    }
    const body = await request.json()
    // use state.session.user.id or state.session.session.userId
    return { id: '1', authorId: state.session.user.id }
  },
})
```

### Server actions with auth

Spiceflow server actions (`'use server'` functions) run in a different request context than the page render. You cannot access the page's `request` or `state` directly. Use `getActionRequest()` from spiceflow to get the action's request, then call `requireSession()` on it:

```tsx
import { getActionRequest, parseFormData } from 'spiceflow'

async function deletePost(formData: FormData) {
  'use server'
  const request = getActionRequest()
  const session = await requireSession(request) // throws 401 if not signed in
  const { postId } = parseFormData(z.object({ postId: z.string() }), formData)
  await db.delete(posts).where(eq(posts.id, postId))
  throw redirect('/posts')
}
```

Always call `requireSession(getActionRequest())` at the top of every server action that mutates data. The action request carries the user's cookies/auth headers, so `getSession` works the same as in route handlers.

### Full Spiceflow app example

```ts
import { Spiceflow, redirect } from 'spiceflow'
import { auth } from './lib/auth'
import { z } from 'zod'

type AuthSession = typeof auth.$Infer.Session | null

export const app = new Spiceflow()
  // Auth middleware
  .use(async ({ request }, next) => {
    if (request.parsedUrl.pathname.startsWith('/api/auth')) {
      const response = await auth.handler(request)
      if (response.ok || response.status !== 404) return response
    }
    return next()
  })
  // Session state
  .state('session', null as AuthSession)
  .use(async ({ request, state }) => {
    state.session = await auth.api.getSession({ headers: request.headers })
  })
  // Session loader — available to all pages and client components
  .loader('/*', ({ state }) => {
    return { session: state.session }
  })
  // Pages
  .page('/login', async ({ loaderData }) => {
    if (loaderData.session) throw redirect('/')
    const { LoginButton } = await import('./components/login-button')
    return <LoginButton />
  })
  .page('/dashboard', async ({ loaderData }) => {
    if (!loaderData.session) throw redirect('/login')
    return <div>Hello, {loaderData.session.user.name}</div>
  })
  // API routes use state.session directly
  .get('/api/me', ({ state }) => {
    if (!state.session) return new Response('Unauthorized', { status: 401 })
    return state.session.user
  })

declare module 'spiceflow/react' {
  interface SpiceflowRegister { app: typeof app }
}
```

## Client setup

### React client

```ts
// src/lib/auth-client.ts
import { createAuthClient } from 'better-auth/react'

export const authClient = createAuthClient({
  // omit baseURL if client and server share the same domain
  baseURL: process.env.NEXT_PUBLIC_URL,
})

export const { signIn, signUp, signOut, useSession } = authClient
```

### With plugins

```ts
import { createAuthClient } from 'better-auth/react'
import { twoFactorClient } from 'better-auth/client/plugins'

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_URL,
  plugins: [
    twoFactorClient({
      twoFactorPage: '/two-factor',
    }),
  ],
})

export const { signIn, signUp, signOut, useSession } = authClient
```

### Vanilla client (non-React)

```ts
import { createAuthClient } from 'better-auth/client'

export const authClient = createAuthClient({
  
})
```

## Client usage patterns

### useSession — reactive session in components

This is discouraged. Prefer passing down session via spiceflow loaders or props instead.

```tsx
import { useSession } from '@/lib/auth-client'

function UserProfile() {
  const { data: session, isPending, error } = useSession()

  if (isPending) return <div>Loading...</div>
  if (!session) return <div>Not signed in</div>

  return <div>Hello, {session.user.name}</div>
}
```

### Sign in with email/password

```ts
import { signIn } from '@/lib/auth-client'

await signIn.email(
  {
    email: 'user@example.com',
    password: 'password123',
    callbackURL: '/dashboard',
    rememberMe: true,
  },
  {
    onRequest: () => setLoading(true),
    onResponse: () => setLoading(false),
    onError: (ctx) => toast.error(ctx.error.message),
  },
)
```

### Sign in with social provider (Google)

```ts
import { signIn } from '@/lib/auth-client'

await signIn.social({
  provider: 'google',
  callbackURL: '/dashboard',
})
```

### Sign up

```ts
import { signUp } from '@/lib/auth-client'

await signUp.email({
  email: 'user@example.com',
  password: 'password123',
  name: 'John Doe',
  image: '', // optional, base64 or URL
  callbackURL: '/dashboard',
  fetchOptions: {
    onRequest: () => setLoading(true),
    onResponse: () => setLoading(false),
    onError: (ctx) => toast.error(ctx.error.message),
  },
})
```

### Sign out

```ts
import { signOut } from '@/lib/auth-client'

await signOut({
  fetchOptions: {
    onSuccess: () => router.push('/login'),
  },
})
```

### Using with Spiceflow typed fetch client

When calling authenticated Spiceflow API routes from the client, use `createSpiceflowFetch` with `credentials: 'include'` so cookies are sent:

```ts
import { createSpiceflowFetch } from 'spiceflow/client'

// Type safety comes from SpiceflowRegister declared in the app entry file
const safeFetch = createSpiceflowFetch(new URL('/', process.env.NEXT_PUBLIC_URL!).href)

const me = await safeFetch('/api/me', {
  fetch: { credentials: 'include' },
})
if (me instanceof Error) {
  console.error(me.message)
  return
}
console.log(me.name, me.email) // fully typed from the route handler return type
```

## Server-side session checks

With the `/*` loader pattern above, session is already available in `loaderData` for all pages. For standalone server code that needs a session outside of Spiceflow (scripts, cron jobs, etc.):

```ts
import { auth } from './lib/auth'

const session = await auth.api.getSession({
  headers: request.headers,
})
if (!session) {
  // handle unauthenticated
}
```

## Session caching

**Always enable cookie caching.** Without it, every `getSession` call hits the database. With cookie caching, the session is stored in a signed cookie and `getSession` just verifies the signature; zero database queries on most requests. This is especially important in Spiceflow apps where the `/*` loader calls `getSession` on every single page load.

```ts
export const auth = betterAuth({
  // ...
  session: {
    expiresIn: 60 * 60 * 24 * 365, // 1 year
    updateAge: 60 * 60 * 24, // refresh expiry every 1 day of activity
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
      strategy: 'compact', // smallest size, signed, default
      // 'jwt' for JWT compatibility
      // 'jwe' for full encryption
    },
  },
})
```

Every `betterAuth()` config in this skill and in new projects must include `session.cookieCache.enabled: true`. Omitting it means a database round-trip per request, which adds latency and load for no reason.

To bypass the cache for sensitive operations (e.g. before a destructive action):

```ts
const session = await auth.api.getSession({
  headers: request.headers,
  query: { disableCookieCache: true },
})
```

## Session expiration — always set to 1 year

**Always set `session.expiresIn` to 1 year** in every better-auth project. The default is only 7 days, which forces users to re-login every week. This is especially painful for CLI tools using the device flow, where re-authenticating means opening a browser and approving again.

```ts
session: {
  expiresIn: 60 * 60 * 24 * 365, // 1 year
  updateAge: 60 * 60 * 24, // refresh expiry every 1 day of activity
},
```

`updateAge` means the session expiry timestamp gets pushed forward on every day of activity. Active users effectively never expire; only truly idle sessions (no API call for a full year) will need to re-authenticate.

This applies to all session types: browser cookies, CLI device-flow bearer tokens, and any other session created by better-auth. There is no per-auth-method session config in better-auth; `expiresIn` is global.

If you omit `expiresIn`, better-auth defaults to `60 * 60 * 24 * 7` (7 days). Never rely on this default.

## Plugins

better-auth has a plugin system for adding features. Common plugins:

### Two-factor authentication

**Server:**
```ts
import { betterAuth } from 'better-auth'
import { twoFactor } from 'better-auth/plugins'

export const auth = betterAuth({
  // ...
  plugins: [twoFactor()],
})
```

**Client:**
```ts
import { createAuthClient } from 'better-auth/react'
import { twoFactorClient } from 'better-auth/client/plugins'

export const authClient = createAuthClient({
  plugins: [twoFactorClient({ twoFactorPage: '/two-factor' })],
})
```

After adding plugins, re-run `pnpm dlx auth@latest generate` to generate updated schema, then run drizzle migrations.

### Device authorization (CLI device flow)

Use the `deviceAuthorization` plugin when your app has a CLI companion that needs to authenticate via a browser. The CLI displays a user code, opens a browser to your verification page, and polls until the user approves.

**Server:**

```ts
import { betterAuth } from 'better-auth'
import { deviceAuthorization, bearer } from 'better-auth/plugins'

export const auth = betterAuth({
  // ...
  plugins: [
    deviceAuthorization({ verificationUri: '/device', schema: {} }),
    bearer(), // needed so the CLI can use the session token as a Bearer header
  ],
})
```

**IMPORTANT: pass `schema: {}` to `deviceAuthorization()`.** (Optional again in 1.7.x; still safe.) In `better-auth@1.6.9+`, the plugin's Zod options schema has `schema: z.custom(() => true)` which is non-optional. Without passing it, the plugin throws a ZodError at init time: `"expected": "nonoptional", "path": ["schema"]`. The `schema` field is only for user-provided table overrides and the plugin merges it with its built-in schema via `mergeSchema()`. Passing an empty object is safe and satisfies the validator. No `as any` cast needed; the published types accept `{}`.

```
// Error without schema field:
// ZodError: [{ "code": "invalid_type", "expected": "nonoptional",
//   "path": ["schema"], "message": "Invalid input: ..." }]
//   at deviceAuthorization (better-auth/dist/plugins/device-authorization/index.mjs)
```
```

**Schema:** The plugin requires a `device_code` table. Generate it with `pnpm dlx auth@latest generate`. The table stores device codes, user codes, expiry, and approval status.

```ts
// import * as s from 'drizzle-orm/sqlite-core'
export const deviceCode = s.sqliteTable('device_code', {
  id: s.text('id').primaryKey().notNull().$defaultFn(() => ulid()),
  deviceCode: s.text('device_code').notNull().unique(),
  userCode: s.text('user_code').notNull().unique(),
    userId: s.text('user_id').references(() => user.id, { onDelete: 'cascade' }),
    expiresAt: s.integer('expires_at', { mode: 'timestamp_ms' }).notNull(),
    status: s.text('status', {
      enum: ['pending', 'approved', 'denied', 'expired'],
    }).notNull().default('pending'),
    lastPolledAt: s.integer('last_polled_at', { mode: 'timestamp_ms' }),
    pollingInterval: s.integer('polling_interval', { mode: 'number' }),
  clientId: s.text('client_id'),
  scope: s.text('scope'),
})
```

**Verification page (Spiceflow):**

The device flow verification page must:
1. Check the user code is valid via `auth.api.deviceVerify()` **with request headers**
2. Require the user to be signed in (redirect to login if not)
3. Provide approve/deny actions via `auth.api.deviceApprove` / `auth.api.deviceDeny`

**`deviceVerify` must receive `headers: request.headers`.** Without headers, better-auth cannot claim the device code for the authenticated session. The subsequent `deviceApprove` or `deviceDeny` call will fail with `"Device code has not been claimed by a verifying session"`. Make sure the user is signed in **before** calling `deviceVerify`, so the headers carry a valid session cookie.

**Requires `better-auth-drizzle-adapter` >= 1.0.5** which implements `consumeOne` and `incrementOne`. Older versions silently fail with "Invalid device code" errors because the device plugin depends on these methods.

```tsx
import { getActionRequest, parseFormData, Spiceflow, redirect } from 'spiceflow'
import { router } from 'spiceflow/react'
import { z } from 'zod'

const devicePageQuerySchema = z.object({
  user_code: z.string().optional(),
  status: z.enum(['approved', 'denied']).optional(),
})

const deviceUserCodeSchema = z.object({ userCode: z.string().min(1) })

export const app = new Spiceflow()
  // ... auth middleware ...
  .page({
    path: '/device',
    query: devicePageQuerySchema,
    handler: async ({ request, query }) => {
      const userCode = query.user_code ?? ''
      const status = query.status

      if (!userCode) {
        return <div>Open this page from the CLI login flow.</div>
      }

      if (status === 'approved') {
        return <div>CLI approved. You can close this page.</div>
      }
      if (status === 'denied') {
        return <div>CLI denied. You can close this page.</div>
      }

      // 1. Require sign-in BEFORE deviceVerify so headers carry session cookie
      const session = await getSession(request)
      if (!session) {
        throw redirect(router.href('/login', {
          callbackURL: `${request.parsedUrl.pathname}${request.parsedUrl.search}`,
        }))
      }

      // 2. Validate AND claim the device code for this session
      const auth = getAuth()
      const device = await auth.api.deviceVerify({
        query: { user_code: userCode },
        headers: request.headers, // REQUIRED: links device code to the authenticated session
      }).catch(() => null)

      if (!device) {
        return <div>Invalid or expired device code.</div>
      }

      // 3. Server actions for approve/deny
      async function approveDevice(formData: FormData) {
        'use server'
        const actionRequest = getActionRequest()
        await requireSession(actionRequest)
        const { userCode: code } = parseFormData(deviceUserCodeSchema, formData)
        const actionAuth = getAuth()
        await actionAuth.api.deviceApprove({
          body: { userCode: code },
          headers: actionRequest.headers,
        })
        throw redirect(router.href('/device', { user_code: code, status: 'approved' }))
      }

      async function denyDevice(formData: FormData) {
        'use server'
        const actionRequest = getActionRequest()
        await requireSession(actionRequest)
        const { userCode: code } = parseFormData(deviceUserCodeSchema, formData)
        const actionAuth = getAuth()
        await actionAuth.api.deviceDeny({
          body: { userCode: code },
          headers: actionRequest.headers,
        })
        throw redirect(router.href('/device', { user_code: code, status: 'denied' }))
      }

      return (
        <div>
          <p>A CLI is requesting access. Code: {userCode}</p>
          <form action={approveDevice}>
            <input type="hidden" name="userCode" value={userCode} />
            <button type="submit">Approve</button>
          </form>
          <form action={denyDevice}>
            <input type="hidden" name="userCode" value={userCode} />
            <button type="submit">Deny</button>
          </form>
        </div>
      )
    },
  })
```

**Device flow tips:**
- Pass `headers: request.headers` to `auth.api.deviceToken()` when you call it from your own route: the new session stores that request's `user-agent` and IP (e.g. `mycli/1.0 (Mac name)`), so a dashboard can list and revoke CLI sessions.
- In bearer-token API routes the CLI calls, never wrap `getSession` in a catch that returns null. A DB outage then becomes a 401, and a CLI that deletes its token on 401 signs every user out. Let it throw (5xx); catch only for browser pages with stale cookies.

**CLI side** (polling loop):

**Always use `createAuthClient` with `deviceAuthorizationClient` plugin** instead of hardcoding endpoint URLs. Endpoint paths change between better-auth versions (e.g. `/device-authorization/request` → `/device/code`). Hardcoded URLs silently break on upgrades and are too easy to get wrong.

```ts
import { createAuthClient } from 'better-auth/client'
import { deviceAuthorizationClient } from 'better-auth/client/plugins'

const client = createAuthClient({
  baseURL: 'https://myapp.com',
  plugins: [deviceAuthorizationClient()],
})

// 1. Request a device code
const { data, error } = await client.device.code({
  client_id: 'my-cli',
})
if (error || !data) throw new Error(`Failed to request device code: ${error?.message}`)

const verificationUrl = data.verification_uri_complete
  || `https://myapp.com/device?user_code=${data.user_code}`
console.log(`Open: ${verificationUrl}`)
console.log(`Code: ${data.user_code}`)

// 2. Open the browser for the user
open(verificationUrl)

// 3. Poll until approved
const pollInterval = (data.interval || 5) * 1000
const deadline = Date.now() + (data.expires_in || 300) * 1000

while (Date.now() < deadline) {
  await new Promise((r) => { setTimeout(r, pollInterval) })
  const { data: tokenData, error: pollError } = await client.device.token({
    grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
    device_code: data.device_code,
    client_id: 'my-cli',
  })
  if (tokenData?.access_token) {
    // Store access_token for Bearer auth on subsequent API calls
    break
  }
  // authorization_pending and slow_down mean keep polling
  const errorCode = (pollError as { error?: string })?.error
  if (errorCode === 'authorization_pending' || errorCode === 'slow_down') continue
  if (pollError) throw new Error(`Device auth failed: ${pollError.message}`)
}
```

The client proxy maps method names to endpoint paths via kebab-case conversion: `client.device.code()` → POST `/device/code`, `client.device.token()` → POST `/device/token`, `client.device.approve()` → POST `/device/approve`. The `pathMethods` from the plugin tell the proxy which HTTP method to use.

### Bearer token auth

The `bearer` plugin lets clients authenticate with `Authorization: Bearer <session-token>` instead of cookies. Essential for CLI tools, API clients, and mobile apps.

**Server:**

```ts
import { betterAuth } from 'better-auth'
import { bearer } from 'better-auth/plugins'

export const auth = betterAuth({
  // ...
  plugins: [bearer()],
})
```

No client plugin needed. The CLI or API client just sends the session token as a Bearer header:

```ts
const response = await fetch('https://myapp.com/api/me', {
  headers: { Authorization: `Bearer ${sessionToken}` },
})
```

`auth.api.getSession({ headers })` automatically checks both cookies and the Authorization header when the bearer plugin is enabled. No code changes needed in your session resolution logic.

### Other plugins

- **organization** — multi-tenant orgs with roles and teams
- **passkey** — WebAuthn/passkey authentication
- **magic-link** — passwordless email links
- **email-otp** — one-time password via email
- **username** — username-based auth
- **admin** — admin panel and user management
- **bearer** — Bearer token auth for APIs
- **api-key** — API key authentication

See https://better-auth.com/llms.txt for full plugin docs.

## Error handling with onAPIError

Use `onAPIError.onError` to capture auth errors with your observability stack. Without this, auth errors (failed OAuth callbacks, expired sessions, DB issues) are silently logged to console and never reach your error tracker.

```ts
import { betterAuth } from 'better-auth'
import { captureException } from '@strada.sh/sdk' // or Sentry, etc.

export const auth = betterAuth({
  // ... your config ...
  onAPIError: {
    onError(error) {
      captureException(
        error instanceof Error ? error : new Error(String(error)),
        { tags: { source: 'better-auth' } },
      )
    },
  },
})
```

The `onAPIError` config is a top-level `betterAuth()` option (not nested under `advanced`). Available fields:

- **`onError?: (error: unknown, ctx: AuthContext) => void`** — called on every API error (except redirects). The `error` is `unknown`, so wrap non-Error values. When set, this **replaces** better-auth's default error logging, so include your own logging if needed.
- **`throw?: boolean`** — re-throw the error instead of swallowing (for frameworks that catch at a higher level)
- **`errorURL?: string`** — redirect URL for OAuth error pages (defaults to `/api/auth/error`)
- **`customizeDefaultErrorPage?`** — style the built-in error page

If using the `strataBetterAuth()` plugin from `@strada.sh/sdk/better-auth`, error capture is already wired up automatically. You don't need to add `onAPIError` manually.

## Spiceflow page examples

### Login page

**Always create a `/login` page.** Users, agents, OAuth callbacks, and redirects throughout the app expect `/login` to exist. Without it, unauthenticated users hit a 404 instead of a sign-in form. Every better-auth project must have a `/login` route from day one.

A standalone login page that redirects to the dashboard if already authenticated. Uses `loaderData.session` from the `/*` loader — no need to call `getSession` again:

```tsx
// In your app entry (src/main.tsx or src/app.tsx)
// Assumes auth middleware + session state + /* loader are registered (see above)

  .page('/login', async ({ loaderData }) => {
    if (loaderData.session) throw redirect('/')
    const { LoginButton } = await import('./components/login-button')
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="text-center max-w-sm">
          <h1 className="text-2xl font-bold tracking-tight mb-2">My App</h1>
          <p className="text-muted-foreground mb-6">Sign in to continue</p>
          <LoginButton callbackURL="/" />
        </div>
      </div>
    )
  })
```

```tsx
// src/components/login-button.tsx
'use client'

import { useState } from 'react'
import { authClient } from '../lib/auth-client'

export function LoginButton({ callbackURL = '/' }: { callbackURL?: string }) {
  const [loading, setLoading] = useState(false)

  return (
    <button
      onClick={async () => {
        setLoading(true)
        await authClient.signIn.social({
          provider: 'google',
          callbackURL,
        })
      }}
      disabled={loading}
      className="h-10 px-6 rounded-lg bg-primary text-primary-foreground font-semibold"
    >
      {loading ? 'Redirecting...' : 'Sign in with Google'}
    </button>
  )
}
```

### Signup route

**Always create a `/signup` route that redirects to `/login`.** Users, agents, and external links expect `/signup` to exist. Without it, visitors hit a 404. Since better-auth handles registration through the same sign-in flow (social OAuth creates accounts automatically, `signUp.email` uses `/api/auth/sign-up`), a dedicated signup page is unnecessary. A redirect keeps the URL alive:

```ts
.get('/signup', ({ request }) => {
  const callbackURL = request.parsedUrl.searchParams.get('callbackURL')
  throw redirect(router.href('/login', { callbackURL: callbackURL || undefined }))
})
```

If the app later needs a separate signup page with different UI (e.g. an onboarding form), replace the redirect with a full `.page()`.

### Pricing route

**Always create a `/pricing` route.** Users, agents, and external links try `/pricing` first. Without it they hit a 404. If the real pricing page lives elsewhere (for example `/docs/pricing`), keep `/pricing` alive with a redirect:

```ts
.get('/pricing', ({ redirect }) => {
  throw redirect('/docs/pricing', { status: 301 })
})
```

Do not leave `/pricing` undefined just because a docs site already has a pricing page under another path.

### 404 page

**Always render a 404 page** that explains the page was not found. Spiceflow's default is unstyled. When no page matches, the root `/*` layout receives `children === null`. If that layout returns `{children}` unchanged, the page is **blank white**.

Handle it in the root layout. Do **not** add `.page('/*')` if the app also has API routes: a wildcard page steals GET `/api/*` and aliases like `/signup`.

```tsx
function NotFoundPage({ path }: { path?: string }) {
  return (
    <main>
      <h1>Page not found</h1>
      <p>{path ? `The page ${path} was not found.` : 'This page was not found.'}</p>
    </main>
  )
}

.layout('/*', ({ children, response, request }) => {
  if (children == null) response.status = 404
  return <>{children ?? <NotFoundPage path={request.parsedUrl.pathname} />}</>
})
```

See the spiceflow README "Redirects and Not Found" section.

### Dashboard redirect for authenticated users

**Never redirect `/` to a dashboard automatically.** The landing page should always render for all users (authenticated or not). Instead, add a `/dash` or `/dashboard` link in your navbar that resolves the user's default destination.

The `/dash` route should resolve the full target path in a single query and issue **one redirect** directly to the final URL. Never chain redirects (e.g. `/dash` → `/orgs/{id}` → `/projects/{id}` → `/projects/{id}/envs/dev`). Each redirect is a separate worker invocation with its own DB queries, and on Cloudflare Workers with D1 the latency compounds fast; users far from the database region will see multi-second page loads.

```ts
// Resolve org → project → env in one hop, redirect to the final URL
.get('/dash', async ({ state, request }) => {
  if (!state.session) throw redirect('/login?redirect=/dash')
  const db = getDb()
  const org = await db.query.orgMember.findFirst({
    where: { userId: state.session.user.id },
    with: { org: true },
    orderBy: { createdAt: 'desc' },
  })
  if (!org) throw redirect('/dash/new-org')
  const project = await db.query.project.findFirst({
    where: { orgId: org.orgId },
    with: { environments: true },
    orderBy: { createdAt: 'desc' },
  })
  if (!project) throw redirect(`/dash/orgs/${org.orgId}`)
  const envSlug = project.environments?.[0]?.slug ?? '_'
  throw redirect(`/dash/projects/${project.id}/envs/${envSlug}`)
})
```

### Protected layout with session

Use a layout to enforce auth for a group of pages. The session is available from `loaderData` (provided by the `/*` loader), so the layout just checks it and renders:

```tsx
.layout('/app/*', async ({ loaderData, children }) => {
  if (!loaderData.session) throw redirect('/login')
  const { user } = loaderData.session

  return (
    <div className="flex min-h-screen">
      <aside className="w-64 border-r p-4">
        <div className="text-sm text-muted-foreground">{user.email}</div>
        <nav>{/* sidebar links */}</nav>
        {/* Use a client component with authClient.signOut() for sign-out */}
      </aside>
      <main className="flex-1 p-6">{children}</main>
    </div>
  )
})
```

### Protected page

Pages under a protected layout don't need to re-check auth — the layout already redirected unauthenticated users. Session data is still available via `loaderData`:

```tsx
.page('/app/settings', async ({ loaderData }) => {
  const { user } = loaderData.session!
  return (
    <div>
      <h1 className="text-2xl font-bold">Settings</h1>
      <p>Signed in as {user.name} ({user.email})</p>
    </div>
  )
})
```

### Protected API route

API routes don't use loaders — use `state.session` directly:

```ts
.route({
  method: 'POST',
  path: '/api/posts',
  request: z.object({
    title: z.string().min(1),
    content: z.string(),
  }),
  async handler({ request, state }) {
    if (!state.session) {
      return new Response(JSON.stringify({ error: 'unauthorized' }), {
        status: 401,
        headers: { 'content-type': 'application/json' },
      })
    }
    const body = await request.json()
    const post = await createPost({ ...body, authorId: state.session.user.id })
    return { ok: true, id: post.id }
  },
})
```

### Sign out button

**Do NOT use `<a href="/api/auth/sign-out">`** — the GET sign-out endpoint does not work reliably. Always use the client method which POSTs to the correct endpoint:

```tsx
'use client'
import { createAuthClient } from 'better-auth/react'

const authClient = createAuthClient()

function SignOutButton() {
  return (
    <button onClick={async () => {
      await authClient.signOut()
      window.location.href = '/login'
    }}>
      Sign out
    </button>
  )
}
```

### Reading session in any client component

Any client component can read the session via `useLoaderData` without props — it's type-safe and always available from the `/*` loader:

```tsx
'use client'
import { useLoaderData } from 'spiceflow/react'

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { session } = useLoaderData('/*')

  if (!session) return <a href="/login">Please sign in</a>
  return <>{children}</>
}
```

## Auto-join organization by email domain

Pattern for automatically adding users to an org when their verified email matches a domain (e.g. all `@acme.com` users join the Acme org). This is application-level logic built on top of better-auth sessions, not a better-auth plugin.

**Schema:** add a nullable `autoJoinDomain` column on the org table, indexed for lookup. A blocklist of common public domains (gmail.com, outlook.com, etc.) prevents misuse.

```ts
// Schema (SQLite example)
const org = s.sqliteTable('org', {
  id: s.text('id').primaryKey().$defaultFn(() => ulid()),
  name: s.text('name').notNull(),
  autoJoinDomain: s.text('auto_join_domain'), // e.g. 'acme.com'
}, (table) => [
  s.index('org_auto_join_domain_idx').on(table.autoJoinDomain),
])
```

**Auto-join function:** runs on every authenticated page load (e.g. in a Spiceflow `loader`). Checks `emailVerified`, skips public domains, queries matching orgs, inserts memberships with `onConflictDoNothing`. No pre-read of existing memberships needed; the unique index handles duplicates.

```ts
async function autoJoinOrgsByDomain(session: Session): Promise<void> {
  if (!session.user.emailVerified) return
  const domain = getEmailDomain(session.user.email)
  if (!domain || COMMON_EMAIL_DOMAINS.has(domain)) return

  const db = getDb()
  const matchingOrgs = await db.query.org.findMany({
    where: { autoJoinDomain: domain },
    columns: { id: true },
  })
  if (matchingOrgs.length === 0) return

  const queries = matchingOrgs.map((o) =>
    db.insert(schema.orgMember)
      .values({ orgId: o.id, userId: session.userId, role: 'member' })
      .onConflictDoNothing({ target: [schema.orgMember.orgId, schema.orgMember.userId] }),
  )
  await db.batch(queries as [any, ...any[]])
}
```

**Where to call it:** in the authenticated layout loader, before querying the user's org memberships. The function is idempotent, so calling it on every page load is safe.

```ts
.loader('/dash/*', async ({ request }) => {
  const session = await requirePageSession(request)
  await autoJoinOrgsByDomain(session) // join matching orgs before listing them
  const members = await db.query.orgMember.findMany({
    where: { userId: session.userId },
    with: { org: true },
  })
  // ...
})
```

**UI for enabling:** add a checkbox in the org creation form (hidden for public email domains like gmail.com) and a toggle in org settings. Both the create action and the update action should require `emailVerified: true` on the admin before allowing auto-join to be enabled.

**Key rules:**
- The domain blocklist and `getEmailDomain()` helper must live in a **client-safe module** (no server imports). Client components need them to show/hide the checkbox. Server code can re-export them.
- Require `emailVerified: true` on the admin who enables auto-join and on users who get auto-joined.
- Use `onConflictDoNothing` on the `(org_id, user_id)` unique index so the function is idempotent.
- No domain ownership verification (DNS TXT, Google Admin SDK) is needed for self-hosted tools. First user to claim a domain gets it.

## Drizzle ORM v1 (beta) compatibility

The official `@better-auth/drizzle-adapter` does **not** work with `drizzle-orm@beta` (v1.0.0-beta). It relies on v0 APIs (`db._.fullSchema`, `db.query`) that changed in v1 and crashes with `"model 'user' was not found in the schema object"`.

Use `better-auth-drizzle-adapter` instead. It's vendored from better-auth PR #9489 (relations-v2 support) with additional bug fixes for `eq(null)` SQL generation and postgres-js `deleteMany` row counts.

```bash
pnpm add better-auth better-auth-drizzle-adapter drizzle-orm@beta
```

```ts
import { drizzleAdapter } from 'better-auth-drizzle-adapter'

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: 'pg' }), // or 'sqlite'
  // ...
})
```

No subpath import needed. Works with both drizzle-orm v0 and v1. Source and bug tracker: https://github.com/remorses/better-auth-drizzle-adapter

### TS2742 from exported `getAuth()` in app packages

If a private app exports a BetterAuth instance factory like `getAuth()` and `tsc` fails with `TS2742`, first check whether the app package is emitting declaration files.

The error looks like this:

```txt
The inferred type of 'getAuth' cannot be named without a reference to '../node_modules/better-auth/dist/types/auth.d.mts'. This is likely not portable. A type annotation is necessary.
```

This usually happens when `declaration`, `declarationMap`, `emitDeclarationOnly`, or `composite` forces TypeScript to emit `.d.ts` files for an app package. The inferred BetterAuth return type is large and can include transitive pnpm/pkg-pr-new internals, so TypeScript cannot print a portable public type.

For private application packages, prefer disabling declaration emit instead of writing a fake wrapper type:

```json
{
  "compilerOptions": {
    "noEmit": true
  }
}
```

Then keep `getAuth()` exported normally:

```ts
export function getAuth() {
  const db = getDb()
  return betterAuth({
    database: drizzleAdapter(db, { provider: 'sqlite' }),
    // ...
  })
}
```

Only keep declaration emit for packages that are actually consumed as libraries. If a package is only a Vite/Spiceflow app, Vite emits the runtime build and `tsc --noEmit` is the right typecheck path.

If the package must emit declarations, add an explicit real exported BetterAuth type annotation instead of hand-writing a partial auth shape. Also try `pnpm dedupe better-auth @better-auth/core better-auth-drizzle-adapter`, but do not expect dedupe to fix TS2742 when declaration emit is the root cause.

## Server-side API calls and cookies

When calling `auth.api.*` methods server-side (e.g. `auth.api.signInSocial()`), the response cookies (state cookies, session cookies) are **not automatically sent to the browser**. If you extract just the URL and create your own `Response.redirect()`, all `Set-Cookie` headers are lost.

This causes `state_mismatch` errors on OAuth callbacks because BetterAuth stores a signed state cookie for CSRF protection. Without it, the callback validation fails.

**Always use `returnHeaders: true`** and manually forward cookies when the result is a browser redirect:

```ts
// BAD — cookies lost, causes state_mismatch on callback
.get('/sign-in', async ({ request }) => {
  const auth = getAuth()
  const res = await auth.api.signInSocial({
    body: { provider: 'google', callbackURL: request.url },
  })
  return Response.redirect(res.url, 302) // ← bare redirect, no cookies!
})

// GOOD — returnHeaders + manual cookie forwarding
.get('/sign-in', async ({ request }) => {
  const auth = getAuth()
  // signInSocial returns JSON { url, redirect } on server calls.
  // Use returnHeaders to get both the parsed body AND Set-Cookie headers.
  const { response: result, headers } = await auth.api.signInSocial({
    body: { provider: 'google', callbackURL: request.url },
    headers: request.headers,
    returnHeaders: true,
  })
  if (!result?.url) {
    return new Response('Failed to initiate sign-in', { status: 500 })
  }
  const redirect = new Response(null, { status: 302, headers: { Location: result.url } })
  for (const cookie of headers.getSetCookie()) {
    redirect.headers.append('Set-Cookie', cookie)
  }
  return redirect
})
```

**Do NOT use `asResponse: true`** for `signInSocial` — it returns a JSON Response with `{ url, redirect: true }` body, not a 302 redirect. The redirect is client-side behavior. On the server you must build the redirect yourself.

**When to use each pattern:**

- **`returnHeaders: true`** — when you need Set-Cookie headers from the response (OAuth redirects, sign-in flows that set state cookies). Returns `{ headers, response }` where `response` is the parsed body and `headers` is a `Headers` object with `getSetCookie()`.
- **`asResponse: true`** — when you want the raw `Response` object (rarely useful for `signInSocial` since it returns JSON, not a redirect).
- **Default (no flag)** — when you just need the data (e.g. `getSession`). Returns the parsed body directly. Cookies are not forwarded.

**`headers` parameter** — always pass the original `request.headers` when the API call needs request context (cookies, user agent, IP). Without it, BetterAuth can't read existing cookies or set new ones with the correct domain.

## Server-side social sign-in redirect (protected layouts)

**Never redirect to `/api/auth/sign-in/social?provider=discord&callbackURL=/dashboard` as a GET URL.** There is no GET endpoint at that path. Better-auth's social sign-in is a POST endpoint consumed by the client SDK internally. Redirecting the browser to it returns a 404.

When a server-side layout or route needs to redirect an unauthenticated user to a social provider (e.g. Discord OAuth), call `auth.api.signInSocial()` programmatically and redirect to the returned OAuth URL:

```ts
// In a Spiceflow layout that guards /dashboard/*
.layout('/dashboard/*', async ({ children, request, state }) => {
  const auth = createAuth({ env: state.env, baseURL: new URL(request.url).origin })
  const session = await auth.api.getSession({ headers: request.headers })
  if (!session) {
    // Use the current path so users return to the page they tried to visit
    const callbackURL = new URL(request.url).pathname
    const { response: result, headers } = await auth.api.signInSocial({
      body: {
        provider: 'discord',
        callbackURL,
      },
      headers: request.headers,
      returnHeaders: true,
    })
    if (!result?.url) {
      throw new Response('Failed to initiate sign-in', { status: 500 })
    }
    const redirect = new Response(null, {
      status: 302,
      headers: { Location: result.url },
    })
    for (const cookie of headers.getSetCookie()) {
      redirect.headers.append('Set-Cookie', cookie)
    }
    throw redirect
  }
  return <DashboardLayout>{children}</DashboardLayout>
})
```

`returnHeaders: true` is required to capture the CSRF state cookie that better-auth sets. Without forwarding those cookies, the OAuth callback fails with `state_mismatch`.

## SQLite/D1 dates

Better Auth fields are `type: "date"`. Use the official SQLite column:

```ts
createdAt: s.integer('created_at', { mode: 'timestamp_ms' }).notNull().$defaultFn(() => new Date()),
```

SQL is `INTEGER` ms. TypeScript is `Date`. D1 binds a number. Cookie cache is `z.date()`. Defaults are `new Date()`, not `Date.now()`.

Do not wrap D1 in a `Proxy`. Do not set `supportsDates: false` (ISO strings in INTEGER columns). Do not use `mode: 'timestamp'` (unix seconds).

Older remorses apps used an `epochMs` customType so app JSON stayed numbers. That is legacy. Never use it on Better Auth tables. If cookie cache fails with `Cookie cache payload failed schema validation`, the column is returning a number. Switch it to `timestamp_ms`. Do not disable `cookieCache`.

SQLite `string[]` / `json` Better Auth fields must be `text(name, { mode: 'json' })`. Copy OAuth FKs from https://github.com/better-auth/better-auth/blob/main/packages/oauth-provider/src/schema.ts. Missing `onDelete` is NO ACTION. Do not invent CASCADE on `oauthClient.userId` or on token `client_id`. A CIMD client is one shared row. CASCADE there deletes everyone’s tokens or fights NO ACTION child FKs. Full map is in `mcp.md`.


## Cloudflare Workers

better-auth uses AsyncLocalStorage. Enable it in `wrangler.jsonc`:

```jsonc
{
  "compatibility_flags": ["nodejs_compat"]
}
```

Or for just AsyncLocalStorage: `["nodejs_als"]`.

### Bundle size: always use `better-auth/minimal`

For Cloudflare Workers and edge runtimes, **always import from `better-auth/minimal`** instead of `better-auth`. The default entrypoint bundles Kysely (~400 KB) for when no database adapter is provided. Since Cloudflare projects always use an explicit adapter (drizzle, prisma, etc.), Kysely is dead code.

```ts
import { betterAuth } from 'better-auth/minimal'
```

The API is identical. Plugins are imported from `better-auth/plugins` as usual. Saves ~400 KB from the bundle.

### Durable Objects

When auth tables live in a SQLite Durable Object, follow **[durable-objects.md](./durable-objects.md)**.

### Remote MCP OAuth

When the app needs a hosted HTTP MCP that Cursor or Claude can add with OAuth, follow **[mcp.md](./mcp.md)**. Use `@better-auth/mcp` plus `cimd()`, not `mcp` from `better-auth/plugins`. Skip this for local stdio CLI MCP.

`betterAuth()` runs inside the DO. The Worker verifies `session_data` with `getCookieCache` and RPCs the DO only on a miss or for `/api/auth/*`. Do not put better-auth behind the drizzle sqlite-proxy pattern. Do not call the DO on every page load.

## Social providers

### Google

Always set `prompt: 'select_account'` so Google shows the account picker every time. Without it, users with a single Google session are silently signed in with no way to switch accounts.

```ts
socialProviders: {
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    prompt: 'select_account', // always show account picker
  },
}
```

### GitHub

```ts
socialProviders: {
  github: {
    clientId: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
  },
}
```


Multiple providers can be enabled simultaneously. Each provider needs its own OAuth app credentials.

## Core schema

better-auth creates and manages these tables:

- **user** — id, name, email, emailVerified, image, createdAt, updatedAt
- **session** — id, token, userId, expiresAt, ipAddress, userAgent, createdAt, updatedAt
- **account** — id, userId, accountId, providerId, accessToken, refreshToken, expiresAt, etc.
- **verification** — id, identifier, value, expiresAt, createdAt, updatedAt

Generate the Drizzle schema for these with `pnpm dlx auth@latest generate`. Do not define these tables manually. Plugins add additional tables (e.g. `twoFactor` adds a `twoFactor` table).

## Table name customization

If your Drizzle schema uses different table names (e.g. `users` instead of `user`):

```ts

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'pg',
    schema: {
      ...schema,
      user: schema.users, // map better-auth's "user" to your "users" table
    },
  }),
})
```

Or configure via `modelName`:

```ts
export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: 'pg' }),
  user: { modelName: 'users' },
  session: { modelName: 'sessions' },
})
```

Or if all tables are plural:

```ts
drizzleAdapter(db, {
  provider: 'pg',
  usePlural: true,
})
```

## Always typecheck before building

**Always run `tsc` before `vite build`** in build and deploy scripts. Vite does not typecheck; it only transpiles. Auth misconfigurations (wrong types on session, missing plugin fields, adapter type mismatches) will slip through to production silently without `tsc`. Your `build` script should be `tsc && vite build`.

## Testing with vitest

Test better-auth apps by calling `app.handle()` directly with vitest. No browser, no build, sub-second feedback. This tests the real business logic: user creation, session validation, protected pages, server actions with auth, resource CRUD with ownership checks.

Much faster than browser e2e tests and covers the important things: auth flows, authorization guards, data isolation between users, redirect behavior after mutations.

**Setup:** set `AUTH_DB=:memory:` in vitest env so tests run against an in-memory SQLite database. Add a setup file that applies drizzle migrations before tests start. Enable the `bearer()` plugin so tests can authenticate with `Authorization: Bearer <token>` headers.

**Pattern:** create real users via `auth.api.signUpEmail`, get bearer tokens, pass them to `createSpiceflowFetch(app, { headers })`. Call server actions with `runAction` + authed request. Assert on page renders, loader data, and redirect responses.

Full working example: https://github.com/remorses/spiceflow/tree/main/example-better-auth

**Use cases to test:**

- Public pages render without auth (landing, login, marketing)
- Protected pages redirect unauthenticated users to login
- Protected API routes return 401 for unauthenticated requests
- Authenticated users see their own data (dashboard renders user name/email)
- Multi-step resource creation: signup → create org → redirect → dashboard → create project → verify render
- Mutations via server actions with auth (update profile, create/delete resources)
- Redirect behavior after mutations (action creates resource, redirects to its page)
- **Security: unauthenticated users cannot access protected resources**
- **Security: users cannot access resources owned by other users** (user B cannot see user A's org dashboard)
- **Security: ownership checks on mutations** (user B cannot create/delete projects in user A's org)
- Multiple users with separate sessions see isolated data
- Loader data contains correct values for the authenticated user
