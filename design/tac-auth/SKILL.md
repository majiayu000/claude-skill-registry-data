---
name: tac-express-auth
description: Supabase Auth patterns for tac-express. Load when writing auth middleware, session hooks, sign-in/sign-up flows, or any code that touches authentication. Covers the full cookie-based SSR auth implementation with @supabase/ssr.
---

# tac-express — Authentication System

> **Auth Provider:** Supabase Auth (cookie-based SSR sessions via `@supabase/ssr`)
> **NO Clerk. NO Auth0. NO NextAuth. Zero third-party auth providers.**
> **ADR-006:** Supabase Auth is the sole auth system. See `tac-express-rules` for ADR details.

---

## Architecture Overview

```
apps/web/proxy.ts         ← Middleware: checks session, redirects if unauthenticated
apps/dashboard/proxy.ts   ← Middleware: checks session, redirects if unauthenticated
       ↓
packages/database/src/middleware.ts   ← createMiddlewareClient(req) — cookie refresh
packages/database/src/client.ts       ← createBrowserClient() + createServerClient()
       ↓
packages/auth/src/auth.service.ts     ← createAuthService(db) — sign-in/up/out/session
       ↓
packages/ui/src/hooks/use-session.ts          ← useSession() — client-side session state
packages/ui/src/components/composed/user-menu.tsx         ← UserMenu — user UI
packages/ui/src/components/composed/auth/sign-in-form.tsx ← SignInForm — email/password
```

---

## Package Roles

### `packages/database` — Supabase Client Factory

```ts
// Browser (client components)
import { createBrowserClient } from "@workspace/database/client"
const db = createBrowserClient()

// Server (server components / RSC)
import { createServerClient } from "@workspace/database/client"
import { cookies } from "next/headers"
const db = createServerClient(await cookies())

// Middleware (proxy.ts only)
import { createMiddlewareClient } from "@workspace/database/middleware"
const { supabase, response } = createMiddlewareClient(req)
```

### `packages/auth` — Auth Service

```ts
import { createAuthService } from "@workspace/auth"
import { createBrowserClient } from "@workspace/database/client"

const auth = createAuthService(createBrowserClient())

// Available methods:
await auth.signInWithEmail(email, password)
await auth.signUp(email, password)
await auth.signOut()
await auth.getSession()   // → Session | null
await auth.getUser()      // → User | null
```

### `packages/ui` — Auth UI

```ts
// Session hook (use in any client component)
import { useSession } from "@workspace/ui/hooks/use-session"
const { session, user, isLoading, signOut } = useSession()

// User menu (drop-in replacement for Clerk UserMenu)
import { UserMenu } from "@workspace/ui/components/composed/user-menu"
<UserMenu />

// Sign-in form (controlled — pass onSubmit handler)
import { SignInForm } from "@workspace/ui/components/composed/auth/sign-in-form"
<SignInForm onSubmit={handleSignIn} error={error} isLoading={isLoading} />
```

---

## Middleware Pattern (proxy.ts)

Every app has a `proxy.ts` at its root. Pattern is identical across apps:

```ts
import type { NextRequest } from "next/server"
import { NextResponse } from "next/server"
import { createMiddlewareClient } from "@workspace/database/middleware"

const PUBLIC_PATHS = ["/sign-in", "/sign-up", "/track"]

export default async function proxy(req: NextRequest) {
  const { supabase, response } = createMiddlewareClient(req)
  const { data: { user } } = await supabase.auth.getUser()

  const isPublic = PUBLIC_PATHS.some((p) => req.nextUrl.pathname.startsWith(p))

  if (!user && !isPublic) {
    const url = req.nextUrl.clone()
    url.pathname = "/sign-in"
    return NextResponse.redirect(url)
  }

  return response  // ALWAYS return response (contains refreshed cookie)
}

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
}
```

**Critical:** Always return `response` (not `NextResponse.next()`) — it carries the refreshed session cookie.

---

## Sign-In Page Pattern

Each app has its own `sign-in-client.tsx` in `app-local/components/`:

```tsx
"use client"
import { createBrowserClient } from "@workspace/database/client"
import { SignInForm } from "@workspace/ui/components/composed/auth/sign-in-form"
import { useRouter } from "next/navigation"
import * as React from "react"

export function SignInPageClient() {
  const router = useRouter()
  const [error, setError] = React.useState<string | undefined>()
  const [isLoading, setIsLoading] = React.useState(false)

  async function handleSignIn(email: string, password: string) {
    setIsLoading(true)
    setError(undefined)
    try {
      const db = createBrowserClient()
      const { error: signInError } = await db.auth.signInWithPassword({ email, password })
      if (signInError) throw signInError
      router.push("/home")      // dashboard app redirects to /home
      router.refresh()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign-in failed.")
    } finally {
      setIsLoading(false)
    }
  }

  return <SignInForm onSubmit={handleSignIn} error={error} isLoading={isLoading} />
}
```

---

## Route Protection Summary

| App | Public Paths | Protected Paths |
|-----|-------------|-----------------|
| `apps/web` | `/`, `/sign-in`, `/sign-up`, `/track/*` | `/dashboard` (redirects to apps/dashboard) |
| `apps/dashboard` | `/sign-in`, `/sign-up`, `/track/*` | Everything else |

---

## useSession Hook — How It Works

```ts
// packages/ui/src/hooks/use-session.ts
// - Calls db.auth.getSession() on mount for initial state
// - Subscribes to onAuthStateChange for real-time updates
// - Returns { session, user, isLoading, signOut }
// - signOut() calls db.auth.signOut() — redirect must be handled by caller
```

---

## Creating Supabase Users

No sign-up UI in the dashboard (internal tool). To create users:
1. Supabase Dashboard → Authentication → Users → Add user
2. Or via `auth.service.ts` `signUp()` method in a server action

---

## RLS Policy Pattern

All Supabase RLS policies must use `auth.uid()`:

```sql
-- ✅ Correct
CREATE POLICY "Users can read own data"
ON public.shipments FOR SELECT
TO authenticated
USING (created_by = auth.uid());

-- ❌ Wrong — no Supabase JWT
USING (supabase_uid = requesting_user_id());
```

---

## Session Debugging

```ts
// Check current session server-side
import { createServerClient } from "@workspace/database/client"
import { cookies } from "next/headers"

const db = createServerClient(await cookies())
const { data: { user } } = await db.auth.getUser()
console.log("Current user:", user?.email)
```

---

## Forbidden Auth Patterns

```
❌ import { auth } from "@supabase/ssr/server"
❌ import { SupabaseProvider } from "@supabase/ssr"
❌ import { UserMenu } from "@supabase/ssr"
❌ import { SignIn } from "@supabase/ssr"
❌ import { useAuth } from "@supabase/ssr"
❌ import { createClient } from "@supabase/supabase-js"  (direct — use @workspace/database)
❌ import NextAuth from "next-auth"
```
