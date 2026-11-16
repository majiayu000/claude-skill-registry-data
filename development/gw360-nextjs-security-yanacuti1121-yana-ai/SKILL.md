---
name: nextjs-security
description: Find Next.js-specific security issues across App Router, Pages Router, and Server Actions. Covers the middleware-bypass class, NEXT_PUBLIC environment leakage, RSC over-fetch, CSP for App Router, open redirects, and next/image SSRF via permissive remotePatterns. Invoke when reviewing a Next.js app before launch, after a major version upgrade, or when adding authenticated routes.
---

# Next.js Security

Next.js moves fast and its security model has shifted with every major version. The most common failure mode is reaching for a familiar pattern from a year ago that no longer holds — middleware-only auth, naive Server Actions, NEXT_PUBLIC_ env handling. This skill is the spot-check list.

Tested patterns target App Router on Next.js 14+; most apply to 15/16 too. Pages Router callouts are marked.

## When to invoke

- New Next.js app heading to production
- Major version upgrade (13 → 14 → 15 → 16)
- Adding authenticated routes, Server Actions, or new middleware logic
- Investigating an incident or suspicious request pattern
- Code review for an inherited Next.js codebase

## 1. Middleware is not authoritative auth

Middleware runs on every matched request, but it is a network-edge thing — not a substitute for per-route authorization. Treat middleware as a **performance optimization for redirects and headers**, not as a security boundary.

The 2025 middleware bypass class (CVE-2025-29927-style) showed that header smuggling can skip middleware entirely on misconfigured setups. Patch your Next.js to the fixed version *and* assume the bypass is possible — every protected route still re-checks auth server-side.

```ts
// app/admin/page.tsx — every protected route does its own check
import { redirect } from 'next/navigation';
import { getSession } from '@/lib/session';

export default async function AdminPage() {
  const session = await getSession();
  if (!session || session.role !== 'admin') redirect('/login');
  // ... render
}
```

For Server Actions specifically, **re-validate inside the action**:

```ts
'use server';
export async function deletePost(id: string) {
  const session = await getSession();
  if (!session) throw new Error('unauthenticated');
  if (!canDelete(session.userId, id)) throw new Error('forbidden');
  // ... mutate
}
```

A Server Action is callable from any client that knows the action ID; middleware only sees the request, not the action target.

## 2. `NEXT_PUBLIC_` env leakage

Any environment variable starting with `NEXT_PUBLIC_` is **baked into the client bundle**. It is visible to anyone who opens DevTools.

```bash
# Find what's actually shipped
grep -r 'NEXT_PUBLIC_' .next/static/chunks 2>/dev/null | head
```

Common mistakes:

- A "publishable" API key that turns out to be more powerful than its name suggests (e.g. Supabase `anon` key without RLS, Sentry DSN with project-wide scope)
- Internal admin URLs prefixed `NEXT_PUBLIC_ADMIN_API=...`
- Build-time secret values that the dev assumed were server-only because they "feel server-only"

Rule: if it would matter that a competitor or attacker sees it, do not prefix it `NEXT_PUBLIC_`. Use a Server Component / Route Handler / Server Action to mediate access.

## 3. Server Actions — input validation and rate limiting

Server Actions look like function calls but they are HTTP endpoints. Apply the same hygiene you would to any POST endpoint:

```ts
'use server';
import { z } from 'zod';
import { rateLimit } from '@/lib/rate-limit';

const schema = z.object({
  title: z.string().min(1).max(200),
  bodyHtml: z.string().max(50_000),
});

export async function createPost(input: unknown) {
  const session = await requireSession();
  await rateLimit(`create-post:${session.userId}`, { window: '1m', max: 5 });
  const { title, bodyHtml } = schema.parse(input);
  const safeHtml = sanitizeHtml(bodyHtml);
  return db.posts.create({ title, bodyHtml: safeHtml, userId: session.userId });
}
```

Specifically:

- **Validate every input** with Zod / Valibot — never trust the call site
- **Sanitize HTML** before storing if it will be rendered (DOMPurify on server input, server-side renderer)
- **Rate limit** per user and per IP — Server Actions can be invoked from anywhere
- **Avoid taking arbitrary identifiers** — if the user "should only edit their own posts", do not accept arbitrary `postId`; resolve it via session-scoped query

## 4. RSC over-fetch

React Server Components serialize fetched data and ship it to the client. It is easy to over-fetch and accidentally serialize fields the UI never displays.

```ts
// Bad — passes the whole user record (incl. password_hash, email_verified_at) to the client component
const user = await db.users.findUnique({ where: { id }});
return <UserCard user={user} />;

// Good — explicit projection
const user = await db.users.findUnique({
  where: { id },
  select: { id: true, displayName: true, avatarUrl: true },
});
return <UserCard user={user} />;
```

Audit checklist:

- Every server-component fetch uses an explicit `select`/`pick` (or a typed DTO function)
- No record types include credentials, internal flags, or PII not needed for render
- `JSON.stringify` of the page's RSC payload (visible in the HTML source) does not contain anything you would not put in a public API response

## 5. Content Security Policy

Inline scripts and styles are common in Next; CSP needs a strategy.

- **App Router + nonce-based CSP** is the modern path. Generate a per-request nonce in middleware, attach to the response header, and pass to `next/script` via the `nonce` prop.
- **`unsafe-inline` is a footgun** but sometimes unavoidable for legacy components. If you use it, document why and revisit per release.
- **`script-src 'self' 'nonce-...'`** baseline; add specific allowed origins only as needed (analytics, etc.)
- **`frame-ancestors 'none'`** unless you intentionally support embedding
- **`upgrade-insecure-requests`** is cheap and helpful

Start in `Content-Security-Policy-Report-Only` for a week, then promote to enforcing.

## 6. Open redirects and unsafe `redirect()`

Any flow that takes a destination from user input is a potential open redirect:

```ts
// Bad
const next = searchParams.get('next');
redirect(next ?? '/');

// Good — allowlist or strip to relative path
function safeNext(next: string | null): string {
  if (!next || !next.startsWith('/')) return '/';
  if (next.startsWith('//')) return '/';   // protocol-relative would escape
  return next;
}
```

Same logic for OAuth callback `state`, post-login destinations, and "return to" parameters.

## 7. `next/image` and remote patterns

`next/image` can fetch remote images on behalf of your server. If `remotePatterns` is too permissive, you have an SSRF + image-resize-amplification gift.

```js
// next.config.js — bad
images: { remotePatterns: [{ protocol: 'https', hostname: '**' }] }

// Good
images: {
  remotePatterns: [
    { protocol: 'https', hostname: 'cdn.example.com' },
    { protocol: 'https', hostname: 'images.unsplash.com', pathname: '/**' },
  ],
}
```

Never use `domains: ['*']` or `remotePatterns` matching all hosts in production.

## 8. Route Handlers — auth and method discipline

API route handlers under `app/api/*/route.ts` are public unless protected:

```ts
// app/api/admin/users/route.ts
import { requireSession } from '@/lib/auth';

export async function GET() {
  const session = await requireSession();
  if (session.role !== 'admin') return new Response('forbidden', { status: 403 });
  return Response.json(await db.users.findMany({ select: safeFields }));
}

// Be explicit about which methods exist. Unexported methods 405 by default — that's the desired behavior.
```

Mistakes to watch for:

- Route handlers that read body without size limit (DoS) — set a sensible cap
- CORS handlers that echo `Origin` back as `Access-Control-Allow-Origin` (effectively allow-any)
- JSON parse without catch — malformed body crashes the handler and leaks stack in dev

## 9. Edge runtime vs Node runtime

`export const runtime = 'edge'` changes the threat model:

- Smaller surface for some attacks (no Node APIs)
- But: many auth libraries assume Node crypto. Misconfigured edge auth has produced incidents.
- Secrets in Edge are available to the function but not "less exposed" than Node — same caution applies.
- Edge middleware has even tighter constraints. If your middleware imports `crypto.subtle` and a buggy polyfill, you can get inconsistent behavior between local dev and prod.

Pick a runtime per route deliberately, document why, and stick to it.

## 10. Headers (server-side baseline)

For routes not behind Cloudflare with header injection, set in `next.config.js`:

```js
async headers() {
  return [{
    source: '/(.*)',
    headers: [
      { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
      { key: 'X-Frame-Options', value: 'DENY' },
    ],
  }];
}
```

If you are behind Cloudflare, prefer setting these at the edge — see [`cloudflare-hardening`](../cloudflare-hardening/SKILL.md).

## 11. Build-time and dependency hygiene

- **Lockfile committed** (`package-lock.json`, `pnpm-lock.yaml`) — required for reproducible builds
- **`npm audit` / `pnpm audit`** in CI, fail on high
- **`next telemetry disable`** if you do not want Next's anonymous telemetry
- **Pin Next.js patch versions** in `package.json`, do not rely on caret to pull a fix automatically

## Quick checklist

- [ ] Patched against the latest Next.js advisories (middleware bypass class)
- [ ] Every protected route re-checks auth, not just middleware
- [ ] Every Server Action validates inputs and re-checks auth
- [ ] No `NEXT_PUBLIC_*` env contains anything sensitive
- [ ] RSC fetches use explicit field projection
- [ ] CSP applied, nonce-based preferred
- [ ] `redirect()` destinations are validated against an allowlist or stripped to relative
- [ ] `next/image` `remotePatterns` is a real allowlist, not `**`
- [ ] Route handlers have size limits and explicit method exports
- [ ] Edge vs Node runtime chosen per route deliberately
- [ ] Security headers set (Next config or Cloudflare)
- [ ] Lockfile committed; audit gates in CI

## What this skill will not do

- Help bypass Next.js authentication on apps you do not own
- Recommend disabling Next.js security features for convenience
- Cover Pages-Router-specific historical issues in depth (most legacy patterns are still vulnerable in their original form; migrate)
