---
name: next-16
description: Build, review and upgrade Next.js 16 App Router code (next@16.x, checked against 16.4.3) the way 16 actually behaves. Covers the 15 to 16 changes that fail silently or only at runtime (sync cookies/headers/params removed, revalidateTag needing a profile and what each profile serves next, sitemap and image-metadata ids now Promises, images.qualities defaulting to [75], middleware renamed to proxy), the Cache Components model (cacheComponents, partialPrefetching, 'use cache', cacheLife, cacheTag, Suspense and "uncached data during prerendering" build errors), choosing updateTag vs revalidateTag vs revalidatePath vs refresh, and server actions as public endpoints (auth and ownership inside every action, forgeable .bind() arguments). Use when package.json has next 16, when a Next 15 app is upgraded, when adding caching, revalidation, webhooks, proxy.ts or server actions, or when you see unstable_cache, revalidateTag('x'), middleware.ts, UnsafeUnwrappedCookies, export const revalidate or experimental.dynamicIO.
license: MIT
---

# Next.js 16

Next.js 16 is the current major (`next@16.4.3` as of November 2026, with React 19.3). Most Next.js
code on the web and in training data is 13-15, and several 15 habits still compile on 16 while doing
something different. Every behaviour called measured, every quoted error and the unmarked rows in
the tables of sections 2 and 3 were run on 16.4.3 with `next build` and `next start`; the rest comes
from the documentation bundled with 16.4.3 ([sources](references/sources.md)).

## 1. Know what you are working in

```sh
npm ls next                                              # installed version
rg -n -e cacheComponents -e partialPrefetching next.config.*
rg --files node_modules/next/dist/docs                   # version-matched docs ship in the package
```

| You see | It means |
| --- | --- |
| `cacheComponents: true` | Cache Components: dynamic by default, opt-in `'use cache'`, Partial Prerendering. Section 4. |
| no `cacheComponents` | Previous model: `fetch` cache options, `unstable_cache`, `export const revalidate`, ISR. Still supported in 16. |
| `proxy.ts` | The request interceptor formerly called middleware. Section 6. |
| `middleware.ts` | Deprecated name. Still runs in 16; it is the only way to keep the Edge runtime. |

`node_modules/next/dist/docs/` is the documentation for the installed version. When something here
and those docs disagree for a newer 16.x, the bundled docs win.

## 2. Next 15 habits that break or silently change on 16

The dangerous rows are the silent ones: the build passes and the app does something else. Rows
marked † are from the bundled upgrade guide; the others were reproduced on 16.4.3.

| Next 15 code | Next 16 | If you keep it |
| --- | --- | --- |
| `cookies().get()`, `headers()`, `draftMode()` without `await`, `UnsafeUnwrappedCookies` casts | `(await cookies()).get('x')`; make the component `async` | TS error (`UnsafeUnwrapped*` types are gone); `TypeError` in plain JS |
| `params.slug`, `searchParams.q` without `await` | `const { slug } = await params`; type props with `PageProps<'/blog/[slug]'>` | **builds even when typed `{ params: { slug: string } }`, renders `undefined`** |
| `revalidateTag('posts')` | pick a profile by what the **next request** must see (section 3) | TS error. Behaves like `{ expire: 0 }` if forced through |
| fixing that error with `revalidateTag('posts', 'max')` | `'max'` is stale-while-revalidate | **the next view is served stale**, a later one is fresh |
| `sitemap({ id })` with `id * 50000` after `generateSitemaps` | `const n = Number(await id)`: `id` is `Promise<string>` | **builds, then emits NaN / empty sitemaps** |
| `opengraph-image`/`icon` `Image({ params, id })` used synchronously | `await params`, `await id` (`generateImageMetadata` still gets sync `params`) | **builds**; the image reads `undefined` (†) |
| `<Image quality={90}>` with no `images.qualities` | `images: { qualities: [75, 90] }` | **silently coerced to 75**; direct `/_next/image?q=90` returns 400 |
| `images.domains` | `images.remotePatterns: [{ protocol: 'https', hostname: '…' }]` | deprecation warning |
| local image `src="/a.png?v=2"` † | `images.localPatterns` with `search` | the optimizer refuses the image |
| `middleware.ts` + `export function middleware` | `proxy.ts` + `export function proxy` (or default export) | deprecation warning; **both files present = build error** |
| `export const config = { runtime: 'nodejs' }` in the interceptor | delete `runtime`: proxy is always Node.js | build error in `proxy.ts` |
| `experimental.turbopack` | top-level `turbopack` | invalid-config warning + TS error |
| custom `webpack()` config † | migrate to `turbopack` options, or build with `--webpack` | `next build` fails (Turbopack is the default) |
| `eslint: { … }` in next.config, `next lint` | ESLint/Biome CLI directly; `next build` no longer lints | warning + TS error; the command is gone |
| `experimental.dynamicIO`, `experimental.useCache`, `experimental.ppr`, `experimental_ppr` † | `cacheComponents: true` (a model change, not a rename) or remove | removed; enabling the new flag surfaces new build errors |
| `unstable_cacheLife`, `unstable_cacheTag` | `cacheLife`, `cacheTag` from `next/cache` | still exported in 16.4.3, logs an error on first use, slated for removal |
| `serverRuntimeConfig`, `publicRuntimeConfig`, `getConfig()` † | `process.env` (server), `NEXT_PUBLIC_*` (client), `await connection()` before runtime env reads | removed |
| parallel route slot without `default.tsx` | add `default.tsx` returning `null` or `notFound()` | build error ("Parallel route slots cannot render the same URLs") |
| `unstable_rootParams()` † | `import { lang } from 'next/root-params'` (16.3+) | removed |
| relying on Next to override `scroll-behavior: smooth` on navigation † | add `data-scroll-behavior="smooth"` to `<html>` | smooth scrolling on every route change |

Also changed defaults: `images.minimumCacheTTL` is 4 hours (was 60 s), `imageSizes` no longer
contains 16, `images.maximumRedirects` is 3, local IPs are blocked unless
`images.dangerouslyAllowLocalIP`. Node 20.9+ and TypeScript 5.1+ are required; 16.3+ can type-check
with TypeScript 7.

Before/after code, grep patterns and the upgrade order are in
[the upgrade reference](references/upgrade-15-to-16.md).

## 3. Invalidation: choose by what the next request must show

Measured on 16.4.3 with `next start`, both with Cache Components (`'use cache'` + `cacheTag`) and
without (`unstable_cache` with `tags`):

| Call | Where it works | First request after the call |
| --- | --- | --- |
| `updateTag(tag)` | **Server Actions only** | fresh (waits for new data): read-your-own-writes |
| `revalidateTag(tag, 'max')` | Server Actions, Route Handlers | **stale**, and starts a background refresh; a later request is fresh |
| `revalidateTag(tag, 'hours')` or any profile | same | stale while inside that profile's `expire` window |
| `revalidateTag(tag, { expire: 0 })` | same | fresh. Use it in webhooks that must behave like the old one-argument call |
| `revalidatePath('/a/b')` | same | fresh for that path; other pages using the same data keep their cache (†) |
| `refresh()` † | Server Actions only | refreshes the client router; invalidates nothing on the server |
| `updateTag` in a Route Handler | | **throws**: "updateTag can only be called from within a Server Action" (500) |

Rules that follow:

1. A user saving their own change (form, settings, editor): `updateTag` in the action, before `redirect()`.
   `revalidateTag(tag, 'max')` there means the user reloads and sees their old value.
2. A webhook, cron or another service: Route Handler with `revalidateTag(tag, 'max')` when one stale
   response is acceptable, `{ expire: 0 }` when the next request must be fresh. Never `updateTag`.
3. Upgrading `revalidateTag(tag)`: the old call expired immediately. `{ expire: 0 }` (or `updateTag` in
   an action) preserves behaviour; `'max'`, which the upgrade guide's before/after shows, changes it.
4. Tags are case-sensitive and at most 256 characters; a longer tag is never attached, so revalidating
   it does nothing. Build tags from ids with one helper shared by the reader and the writer.
5. Call invalidation after the write succeeds and before `redirect()` (which throws to exit).

## 4. Cache Components

```ts
// next.config.ts
const nextConfig: NextConfig = { cacheComponents: true, partialPrefetching: true }
```

Leaving `partialPrefetching` unset logs a warning in 16.4. Cache Components is the recommended model
since 16.4 and becomes the default in Next 17.

**Dynamic by default.** During `next build` every route is prerendered. Anything that cannot finish
during prerendering must be either cached or inside `<Suspense>`:

- uncached I/O (database, `fs/promises`, `fetch`), `cookies()`, `headers()`, `searchParams`,
  `connection()`, and `await params` for params not returned by `generateStaticParams`;
- otherwise the build fails with *"Route "/x": Next.js encountered uncached or runtime data during
  prerendering"*. Fix with `<Suspense>` around the reading component (stream), `'use cache'` (cache),
  or `export const instant = false` on the segment (allow a blocking route, 16.3+).
- `Date.now()`, `new Date()`, `Math.random()`, `crypto.randomUUID()` in the prerendered part are build
  errors that `instant = false` does not clear: `await connection()` first inside a Suspense
  boundary, or move them to a Client Component.

**Segment configs are gone.** `export const dynamic`, `revalidate`, `fetchCache`, `dynamicParams`
and `runtime` fail the build: *"Route segment config "revalidate" is not compatible with
`nextConfig.cacheComponents`. Please remove it."* Replace them with `'use cache'` + `cacheLife`.
`generateStaticParams` must return at least one entry; unlisted params still render on request.

**`'use cache'`** marks an async function, component or whole file as cacheable:

```ts
import { cacheLife, cacheTag } from 'next/cache'

export const articleTag = (slug: string) => `article:${slug}`

export async function getArticle(slug: string) {
  'use cache'
  cacheLife('hours') // stale 5 min, revalidate 1 h, expire 1 day
  cacheTag(articleTag(slug))
  return db.article.findUnique({ where: { slug } })
}
```

- The key is the build id, the function id and the serialized arguments; variables captured from the
  enclosing scope become arguments too. Arguments must be serializable (no class instances,
  functions, URL objects); JSX and functions can be passed through untouched as `children` or props.
- `cookies()`, `headers()` and `searchParams` are not allowed inside, including in helpers it calls:
  *"`cookies()` can't be read inside `"use cache"`"*. On a dynamic route this passes `next build`
  and fails at request time. Read them outside and pass the values in, or use `'use cache: private'`.
- Set `cacheLife` in every scope. Presets: `seconds`, `minutes`, `hours`, `days`, `weeks`, `max`;
  no call means `default` (stale 5 min, revalidate 15 min, never expires). `revalidate: 0` or
  `expire` under 5 min makes it a request-time hole that needs `<Suspense>`.
- `React.cache` values set outside a `'use cache'` scope are not visible inside it.
- The default handler is in-memory per server instance and does not survive a deploy.
  `unstable_cache` keeps working unchanged and persists across deploys; `'use cache: remote'` uses a
  platform cache handler.

**Personalised pages** keep the per-user part out of the cache and stream it:

```tsx
export default function Page({ params }: PageProps<'/articles/[slug]'>) {
  return (
    <>
      <Suspense fallback={<SignInLink />}>
        <ReaderMenu /> {/* reads cookies(): request time, never cached */}
      </Suspense>
      <Suspense fallback={<ArticleSkeleton />}>
        {params.then(({ slug }) => <ArticleBody slug={slug} />)}
      </Suspense>
    </>
  )
}
```

Recipes (product page with a per-user header, ISR with `generateStaticParams`, nested lifetimes,
`ensureStatic`, `navigation()`/`prefetch()`, debugging headers) are in
[the Cache Components reference](references/cache-components.md).

## 5. Server actions are public endpoints

Every async function exported from a `'use server'` file, and every inline `'use server'` function
rendered into a page, is reachable with a direct POST. Next adds unguessable ids, drops unused
actions and checks `Origin` against the host, but none of that is authorization.

1. **Authenticate and authorize inside every action.** A page that only renders the form for admins,
   or a `proxy.ts` matcher, does not protect the action: it is a separate entry point, and moving it or
   changing the matcher silently removes proxy coverage.
2. **Arguments are client input, including `.bind()` arguments.** `action.bind(null, id)` serializes
   `id` into the page as plain JSON in a hidden form field (`value="[&quot;ws_42&quot;]"`) and the
   client sends it back; a user who edits it gets the action run with any id (measured). Hidden
   inputs are the same.
   Values captured by an inline action's closure are encrypted per build, but re-check anyway.
3. **Authorize against the target, not a flag.** Load the resource by the id you received and compare
   its owner to the session user. Never accept `isOwner`, `role` or `userId` from the form or bound args.
4. **Validate every field** (type, length, trimming) on the server; `formData.get()` returns
   `string | File | null`.
5. **Return only what the UI needs**; return values are serialized to the client.
6. A `'use server'` file may export only async functions. Keep schemas, constants and helpers in a
   separate module (an un-exported helper in the same file is fine).
7. `redirect()` and `notFound()` throw. Do not wrap them in `try/catch`; invalidate before calling them.

```ts
'use server'
import { updateTag } from 'next/cache'
import { redirect } from 'next/navigation'

async function workspaceAdminOrThrow(workspaceId: unknown) {
  const session = await getSession() // reads cookies(); null when signed out
  if (!session) throw new Error('Not signed in')
  const ws = typeof workspaceId === 'string' ? await db.workspace.find(workspaceId) : null
  if (!ws || !ws.adminIds.includes(session.userId)) throw new Error('Forbidden')
  return ws
}

export async function archiveWorkspace(workspaceId: string) {
  const ws = await workspaceAdminOrThrow(workspaceId)
  await db.workspace.archive(ws.id)
  updateTag(`workspace:${ws.id}`)
  redirect('/workspaces')
}
```

Body size is limited to 1 MB by default (`experimental.serverActions.bodySizeLimit`); extra
origins behind proxies go in `experimental.serverActions.allowedOrigins`. More patterns, including
`useActionState` errors and how to test actions without a browser, are in
[the server actions reference](references/server-actions-security.md).

## 6. Proxy (formerly middleware)

- One `proxy.ts` (or `.js`) next to `app/` (or in `src/`), exporting `proxy` or a default function,
  plus an optional static `config.matcher`. Matcher values must be literals.
- Always Node.js runtime; `runtime` in its config is a build error. Need Edge? Stay on `middleware.ts`.
- Use it for redirects, rewrites and headers based on the request, and for **optimistic** auth checks
  (cookie present). Real authorization belongs in pages, Route Handlers and actions.
- Without a matcher it runs for every request, including `_next/static` and images.
- Pass data to the app with request headers: `NextResponse.next({ request: { headers } })`.
- `fetch` cache options and `revalidateTag`/`revalidatePath` do nothing or throw in proxy.
- Config flags were renamed too: `skipMiddlewareUrlNormalize` is `skipProxyUrlNormalize`.

## 7. Prove it

```sh
# next build type-checks, prerenders and validates Cache Components. Read every ⚠ line.
npm run build
# next start serves the production build. Request each changed page twice.
npm start
```

- Request each changed page twice. `x-nextjs-cache: HIT | STALE | MISS` shows the
  response cache; `NEXT_PRIVATE_DEBUG_CACHE=1 next start` logs cache decisions.
- To check read-your-own-writes, submit the action, then load the page **twice**: a stale-while-
  revalidate bug only shows on the first load.
- Cache Components validation insights in `next dev` do not change HTTP status; the build is the gate.

## 8. Anti-patterns

| Don't | Do |
| --- | --- |
| `revalidateTag(tag, 'max')` after a user saves their own data | `updateTag(tag)` in the Server Action |
| `updateTag` in a webhook Route Handler | `revalidateTag(tag, 'max')` or `{ expire: 0 }` |
| `revalidateTag('x') // @ts-expect-error` | choose the profile explicitly |
| `export const revalidate = 3600` with `cacheComponents` | `'use cache'` + `cacheLife('hours')` |
| `cookies()` inside a `'use cache'` function | read outside, pass the value as an argument |
| per-user UI in a cached component or layout | its own component inside `<Suspense>` |
| hiding the button as the only permission check | check ownership inside the action |
| trusting `.bind()` args or hidden inputs | load the target and authorize against the session |
| `sitemap({ id }: { id: number })` | `{ id }: { id: Promise<string> }`, `Number(await id)` |
| `quality={90}` without `images.qualities` | list every quality you use |
| renaming middleware but keeping `runtime: 'nodejs'` | delete `runtime`; proxy is Node.js |

## References

- [Upgrading from 15: before/after code, grep patterns, order of work](references/upgrade-15-to-16.md)
- [Cache Components recipes and debugging](references/cache-components.md)
- [Server actions: authorization patterns, measured facts, testing](references/server-actions-security.md)
- [Sources checked](references/sources.md)
