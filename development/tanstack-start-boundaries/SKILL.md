---
name: tanstack-start-boundaries
description: "TanStack Start server/client code boundary patterns. Use when: debugging virtual module resolution errors (tanstack-start-injected-head-scripts, tanstack-start-manifest, #tanstack-router-entry), importing from @tanstack/react-start/server, using getCookie/getRequestHeaders/getRequestUrl, adding providers to router.tsx, or when Vite fails to resolve TanStack Start imports. Covers createServerFn patterns, dynamic imports, and proper placement of server-only code."
---

# TanStack Start Server/Client Boundaries

## The Problem

TanStack Start uses Vite's environment API to register virtual modules (`tanstack-start-injected-head-scripts:v`, `tanstack-start-manifest:v`, etc.) **only for the server environment**. When you import server-only code at the top level of files that are also bundled for the client, Vite fails to resolve these virtual modules.

## Error Signatures

```
Failed to resolve import "tanstack-start-injected-head-scripts:v"
Failed to resolve import "tanstack-start-manifest:v"
Could not resolve "#tanstack-router-entry"
Could not resolve "#tanstack-start-entry"
```

## Root Cause

Top-level imports from `@tanstack/react-start/server` in files processed by both client AND server:

```typescript
// __root.tsx, router.tsx, or any route file
import { getCookie } from "@tanstack/react-start/server"  // BREAKS CLIENT BUNDLE
```

## Problematic Files

These files are bundled for BOTH client and server:
- `src/router.tsx`
- `src/routes/__root.tsx`
- `src/routes/**/*.tsx` (all route files)
- Any file imported by the above

## Problematic Imports

Never import these at top level in client-bundled files:

```typescript
// FROM @tanstack/react-start/server
import { getCookie, setCookie } from "@tanstack/react-start/server"
import { getRequestHeaders } from "@tanstack/react-start/server"
import { getRequestUrl } from "@tanstack/react-start/server"
import { getRequest } from "@tanstack/react-start/server"

// FROM @tanstack/react-start-server (internal package)
import { getCookie } from "@tanstack/react-start-server"
```

## Solutions

### Solution 1: Use createServerFn with Dynamic Import

Wrap server-only code in a server function using dynamic imports:

```typescript
// server-fns/cookie-fns.ts
import { createServerFn } from "@tanstack/react-start"

export const getThemeCookieFn = createServerFn({ method: "GET" }).handler(
  async () => {
    const { getCookie } = await import("@tanstack/react-start/server")
    return getCookie("theme")
  },
)
```

Then use the server function instead:

```typescript
// routes/__root.tsx
import { getThemeCookieFn } from "@/server-fns/cookie-fns"

beforeLoad: async () => {
  const theme = await getThemeCookieFn()  // Safe - calls server function
  return { theme }
}
```

### Solution 2: Keep Server Imports in server-fns/ Files

Server function files (`src/server-fns/*.ts`) can use top-level imports from `@tanstack/react-start/server` IF they only export `createServerFn` functions:

```typescript
// server-fns/auth-fns.ts - OK because only exports server functions
import { createServerFn } from "@tanstack/react-start"
import { getCookie } from "@tanstack/react-start/server"  // OK here

export const getSessionFn = createServerFn({ method: "GET" }).handler(
  async () => {
    const sessionId = getCookie("session")
    // ...
  },
)
```

**Warning**: If any non-server-function code imports from this file, the chain breaks.

### Solution 3: Move Client Providers Out of router.tsx

The `router.tsx` file's `InnerWrap` runs during SSR. Client-only providers here cause issues:

```typescript
// router.tsx - BAD
import { PostHogProvider } from "./lib/posthog/provider"  // Client-only!

export const getRouter = () => {
  const router = createRouter({
    routeTree,
    InnerWrap: ({ children }) => (
      <PostHogProvider>{children}</PostHogProvider>  // Breaks SSR
    ),
  })
  return router
}
```

Move providers to `__root.tsx` RootDocument:

```typescript
// routes/__root.tsx - GOOD
import { PostHogProvider } from "@/lib/posthog/provider"

function RootDocument({ children }) {
  return (
    <html>
      <body>
        <PostHogProvider>
          {children}
        </PostHogProvider>
      </body>
    </html>
  )
}
```

## File Organization Pattern

```
src/
├── router.tsx              # NO server imports, NO client-only providers
├── routes/
│   ├── __root.tsx          # NO direct server imports, use server-fns
│   └── *.tsx               # NO direct server imports, use server-fns
├── server-fns/             # Server functions with createServerFn
│   ├── auth-fns.ts         # Can import from @tanstack/react-start/server
│   └── cookie-fns.ts       # Wraps getCookie in createServerFn
└── lib/
    └── posthog/
        └── provider.tsx    # "use client" - add to __root.tsx body, not router.tsx
```

## Quick Diagnostic

When you see virtual module errors:

1. Search for `@tanstack/react-start/server` imports outside `server-fns/`:
   ```bash
   grep -r "@tanstack/react-start/server" src/ --include="*.tsx" | grep -v server-fns
   ```

2. Check router.tsx for client-only provider imports

3. Look for import chains that pull server code into client bundles

## GitHub References

- Issue #5196: Server imports in route files
- Issue #6189: Virtual module resolution failures
- Issue #5795: #tanstack-router-entry resolution
