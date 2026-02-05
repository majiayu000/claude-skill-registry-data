---
name: astro
description: Astro framework patterns for SSR/SSG, middleware, and TypeScript. Use when working with Astro pages, API routes, middleware configuration, or debugging rendering issues. Trigger phrases include "Astro", "prerender", "middleware", "SSR", "SSG", "static site".
---

# Astro Framework Skill

Patterns and gotchas for Astro development, with focus on authentication, middleware, and rendering modes.

## Rendering Modes

### SSG vs SSR for Protected Content

**Critical**: In Astro 5.x with `output: "static"`, pre-rendered pages bypass middleware completely.

```
User Request → Vercel CDN → Pre-rendered HTML (cached)
                         ↳ Middleware SKIPPED for static content
```

| Rendering Mode | Middleware Runs? | Use Case |
|----------------|------------------|----------|
| SSG (`prerender = true`) | **No** - build time only | Public content, marketing |
| SSR (`prerender = false`) | **Yes** - every request | Protected content, auth |

### Protecting Content Pages

```typescript
// src/pages/learn/[workshop]/[slug].astro
---
// REQUIRED: Forces middleware to run on every request
export const prerender = false;

const auth = Astro.locals.auth();
if (!auth?.userId) {
  return Astro.redirect('/sign-in');
}
---
```

### API Routes Always Need SSR

```typescript
// src/pages/api/members/index.ts
// API routes needing locals.auth MUST disable prerender
export const prerender = false;

export const GET: APIRoute = async ({ locals }) => {
  const auth = locals.auth?.();
  if (!auth?.userId) {
    return new Response("Unauthorized", { status: 401 });
  }
  // ...
};
```

## Middleware Patterns

### Basic Route Protection

```typescript
// src/middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/astro/server";

const isPublicRoute = createRouteMatcher([
  "/",
  "/sign-in(.*)",
  "/sign-up(.*)",
  "/api/webhooks/(.*)",
]);

export const onRequest = clerkMiddleware((auth, context) => {
  const { userId } = auth();

  if (isPublicRoute(context.request)) {
    return; // Allow public routes
  }

  if (!userId) {
    return auth().redirectToSignIn();
  }
});
```

### Member Status Validation

Check member status in addition to authentication:

```typescript
import { checkMemberAccess, ACCESS_LEVELS } from "@lib/auth";

async function checkAccess(userId, context) {
  const member = await memberQueries.findByClerkId(userId);

  if (!member) {
    return context.redirect("/pending-approval");
  }

  // Check status (expired, pending_approval, etc.)
  const access = checkMemberAccess(member, ACCESS_LEVELS.MEMBER);
  if (!access.hasAccess && access.redirectTo) {
    return context.redirect(access.redirectTo);
  }

  return undefined; // Allow access
}
```

## TypeScript Gotchas

### Unused Variable in Template Strings

Astro's TypeScript preprocessor may report variables as "unused" even when used in template literals:

```typescript
// ❌ TypeScript error: 'slug' is declared but never read
---
const slug = entries[0]?.slug.split("/").pop();
return Astro.redirect(`/learn/${workshop}/${slug}`);
---

// ✅ Inline the expression
---
return Astro.redirect(`/learn/${workshop}/${entries[0]?.slug.split("/").pop() ?? "default"}`);
---
```

### Path Brackets in Shell Commands

File paths with brackets need quoting in shell:

```bash
# ❌ Shell interprets brackets as glob
git add src/pages/learn/[workshop]/index.astro

# ✅ Quote the path
git add 'src/pages/learn/[workshop]/index.astro'
```

## Content Collections

### Dynamic Routes with SSR

When using SSR, you can't use `getStaticPaths()`. Use direct lookups instead:

```typescript
// ❌ SSR mode - getStaticPaths not available
export const prerender = false;
export function getStaticPaths() { ... } // Won't work

// ✅ Direct content lookup
export const prerender = false;
const { workshop, slug } = Astro.params;
const entry = await getEntry("workshops", `${workshop}/${slug}`);
if (!entry) {
  return Astro.redirect("/404");
}
```

## Cache Headers

### Prevent Caching of Status Pages

Status pages (pending, expired, error) should never be cached:

```typescript
---
// Prevent caching - status can change
Astro.response.headers.set("Cache-Control", "no-store, no-cache, must-revalidate");
Astro.response.headers.set("Pragma", "no-cache");
---
```

## Configuration Reference

### astro.config.mjs

```javascript
export default defineConfig({
  output: "static",  // Default - SSG with per-page SSR opt-in
  // OR
  output: "server",  // Full SSR - all pages server-rendered

  adapter: vercel(), // Required for SSR on Vercel
});
```

### Per-Page Rendering

```typescript
// Force SSG (build-time)
export const prerender = true;

// Force SSR (request-time)
export const prerender = false;
```

## Common Issues

### Middleware Not Running

**Symptoms**: Auth checks bypassed, expired users see content

**Cause**: Page is pre-rendered (SSG default)

**Fix**: Add `export const prerender = false;`

### 404 on Dynamic Routes

**Symptoms**: `/learn/workshop/module` returns 404

**Cause**: Dynamic params not handled in SSR mode

**Fix**: Check `Astro.params` and handle missing values:
```typescript
const { workshop, slug } = Astro.params;
if (!workshop || !slug) {
  return Astro.redirect("/404");
}
```

### Build Fails with Type Errors

**Symptoms**: `ts(6133): variable is declared but never read`

**Cause**: Astro preprocessor quirk with template strings

**Fix**: Inline expressions or suppress with `// @ts-ignore`

---

*Last updated: December 2025*
