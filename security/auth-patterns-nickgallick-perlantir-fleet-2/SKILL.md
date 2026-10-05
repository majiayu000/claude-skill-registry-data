---
name: auth-patterns
description: Authentication patterns for Next.js — Supabase Auth, Auth.js/NextAuth, JWT, session management, protected routes.
---

# Authentication Patterns Reference

> Local repos: `repos/supabase-docs`, `repos/next-auth`
> Primary pattern: **Supabase Auth with @supabase/ssr**
> Secondary reference: **Auth.js (NextAuth) v5**

---

## 1. Supabase Auth with Next.js App Router (Primary)

### Architecture Overview

```
Client Component → createBrowserClient() → reads/sets cookies directly
Server Component → createServerClient() → reads cookies (can't set)
Route Handler    → createServerClient() → reads/sets cookies
Server Action    → createServerClient() → reads/sets cookies
Middleware       → createServerClient() → refreshes token, sets cookies
```

### Install

```bash
npm install @supabase/supabase-js @supabase/ssr
```

### Browser Client (Client Components)

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### Server Client (Server Components, Route Handlers, Server Actions)

```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Called from Server Component — can't set cookies.
            // Middleware handles token refresh.
          }
        },
      },
    }
  )
}
```

### Middleware for Token Refresh

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // CRITICAL: Use getClaims() — NOT getSession()
  // getSession() reads unverified data from the cookie and CAN BE SPOOFED.
  // getClaims() cryptographically verifies the JWT.
  const { data: claims, error } = await supabase.auth.getClaims()

  if (
    !claims &&
    !request.nextUrl.pathname.startsWith('/login') &&
    !request.nextUrl.pathname.startsWith('/auth') &&
    !request.nextUrl.pathname.startsWith('/api/auth')
  ) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  return supabaseResponse
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

### Auth Callback Route (for OAuth & Magic Link)

```typescript
// app/auth/callback/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  const next = searchParams.get('next') ?? '/dashboard'

  if (code) {
    const supabase = await createClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)

    if (!error) {
      return NextResponse.redirect(`${origin}${next}`)
    }
  }

  return NextResponse.redirect(`${origin}/auth/error`)
}
```

### Server Component Auth Check

```typescript
// app/dashboard/page.tsx
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return <div>Welcome, {user.email}</div>
}
```

### Protected API Route

```typescript
// app/api/protected/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // User is verified — proceed
  return NextResponse.json({ userId: user.id })
}
```

---

## 2. Auth.js / NextAuth v5 (Reference)

> Local repo: `repos/next-auth`
> Use when: you need multi-provider auth without Supabase, or need database session strategy.

### Setup

```bash
npm install next-auth@beta
```

```typescript
// auth.ts
import NextAuth from 'next-auth'
import GitHub from 'next-auth/providers/github'
import Google from 'next-auth/providers/google'
import Credentials from 'next-auth/providers/credentials'

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET,
    }),
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      authorize: async (credentials) => {
        // Validate credentials against your database
        const user = await validateUser(
          credentials.email as string,
          credentials.password as string
        )
        if (!user) return null
        return { id: user.id, email: user.email, name: user.name }
      },
    }),
  ],

  // JWT (default) vs Database sessions
  session: {
    strategy: 'jwt', // or 'database' with an adapter
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },

  callbacks: {
    // Control who can sign in
    signIn: async ({ user, account, profile }) => {
      // Return true to allow, false to deny
      return true
    },

    // Customize JWT token
    jwt: async ({ token, user, account }) => {
      if (user) {
        token.id = user.id
        token.role = user.role // custom field
      }
      return token
    },

    // Customize session object sent to client
    session: async ({ session, token }) => {
      session.user.id = token.id as string
      session.user.role = token.role as string
      return session
    },

    // Control redirects
    redirect: async ({ url, baseUrl }) => {
      if (url.startsWith('/')) return `${baseUrl}${url}`
      if (new URL(url).origin === baseUrl) return url
      return baseUrl
    },
  },

  pages: {
    signIn: '/login',
    error: '/auth/error',
  },
})
```

### Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth'
export const { GET, POST } = handlers
```

### Middleware (Auth.js)

```typescript
// middleware.ts
export { auth as middleware } from '@/auth'

export const config = {
  matcher: ['/((?!api/auth|_next/static|_next/image|favicon.ico).*)'],
}
```

### Get Session

```typescript
// Server Component
import { auth } from '@/auth'

export default async function Page() {
  const session = await auth()
  if (!session?.user) redirect('/login')
  return <div>{session.user.name}</div>
}

// Client Component
'use client'
import { useSession } from 'next-auth/react'

export function UserInfo() {
  const { data: session, status } = useSession()
  if (status === 'loading') return <div>Loading...</div>
  if (!session) return <div>Not signed in</div>
  return <div>{session.user?.name}</div>
}
```

### Sign In / Sign Out

```typescript
// Server Action
import { signIn, signOut } from '@/auth'

export async function loginAction() {
  await signIn('github', { redirectTo: '/dashboard' })
}

export async function logoutAction() {
  await signOut({ redirectTo: '/' })
}

// Client Component
import { signIn, signOut } from 'next-auth/react'

<button onClick={() => signIn('google')}>Sign in with Google</button>
<button onClick={() => signOut()}>Sign Out</button>
```

---

## 3. Protected Routes Patterns

### Pattern A: Middleware (Recommended)

Best for: protecting entire route groups. Single point of enforcement.

```typescript
// middleware.ts — see Supabase or Auth.js middleware above
// Redirects unauthenticated users before the page even renders
```

### Pattern B: Server Component Check

Best for: per-page authorization logic (e.g., role checks).

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function AdminPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) redirect('/login')

  // Role check
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()

  if (profile?.role !== 'admin') redirect('/unauthorized')

  return <AdminDashboard />
}
```

### Pattern C: Client-Side Auth Guard

Best for: wrapping client-only sections, showing loading states.

```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import type { User } from '@supabase/supabase-js'

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()
  const router = useRouter()

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      if (!user) {
        router.push('/login')
      } else {
        setUser(user)
      }
      setLoading(false)
    })

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_OUT') {
        router.push('/login')
      }
    })

    return () => subscription.unsubscribe()
  }, [supabase, router])

  if (loading) return <div>Loading...</div>
  if (!user) return null

  return <>{children}</>
}
```

---

## 4. Auth State Management

### onAuthStateChange Listener

```typescript
'use client'
import { useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export function AuthListener() {
  const supabase = createClient()
  const router = useRouter()

  useEffect(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      switch (event) {
        case 'INITIAL_SESSION':
          // First load — session restored from storage
          break
        case 'SIGNED_IN':
          router.refresh()
          break
        case 'SIGNED_OUT':
          router.push('/login')
          break
        case 'TOKEN_REFRESHED':
          // Tokens were refreshed — new cookies set automatically
          break
        case 'USER_UPDATED':
          // User metadata changed (e.g., email confirmation)
          router.refresh()
          break
        case 'PASSWORD_RECOVERY':
          router.push('/reset-password')
          break
      }
    })

    return () => subscription.unsubscribe()
  }, [supabase, router])

  return null
}

// Place in root layout: <AuthListener />
```

### Token Refresh Flow

Supabase handles token refresh automatically:
1. **Middleware** calls `getClaims()` or `getUser()` on every request — this triggers refresh if needed
2. **Browser client** auto-refreshes via `onAuthStateChange` with `TOKEN_REFRESHED` event
3. Refresh tokens are rotated — each refresh token can only be used once
4. If refresh fails (e.g., user revoked), user is signed out

---

## 5. Security Best Practices

### NEVER Trust getSession() Server-Side

```typescript
// BAD — getSession() reads unverified data from the cookie
const { data: { session } } = await supabase.auth.getSession()
// A malicious user can modify the cookie payload!

// GOOD — getClaims() verifies the JWT cryptographically
const { data: claims } = await supabase.auth.getClaims()

// GOOD — getUser() makes a network call to Supabase Auth
const { data: { user } } = await supabase.auth.getUser()
```

### Use getClaims() vs getUser()

| Method | How it works | When to use |
|--------|-------------|-------------|
| `getClaims()` | Verifies JWT locally (no network call) | Middleware, frequent checks — fast |
| `getUser()` | Network call to Supabase Auth | When you need latest user data, API routes |
| `getSession()` | Reads raw cookie — **UNVERIFIED** | Client-side only (browser verifies via PKCE) |

### httpOnly Cookies

`@supabase/ssr` automatically uses httpOnly cookies — the auth tokens are NOT accessible via JavaScript, preventing XSS token theft.

### CSRF Protection

- Supabase auth uses PKCE flow which is inherently CSRF-resistant
- For custom forms, use Next.js Server Actions (automatically CSRF-protected)
- For custom API routes, validate the `Origin` header

### Rate Limiting Auth Endpoints

```typescript
// Example: rate limit login attempts
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, '1 m'), // 5 attempts per minute
})

export async function POST(req: Request) {
  const ip = req.headers.get('x-forwarded-for') ?? 'unknown'
  const { success } = await ratelimit.limit(ip)

  if (!success) {
    return new Response('Too many attempts', { status: 429 })
  }

  // Proceed with login...
}
```

---

## 6. Sign Out

```typescript
// Server Action
'use server'
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function signOut() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  redirect('/login')
}

// Client Component
'use client'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export function SignOutButton() {
  const supabase = createClient()
  const router = useRouter()

  return (
    <button
      onClick={async () => {
        await supabase.auth.signOut()
        router.push('/login')
      }}
    >
      Sign Out
    </button>
  )
}
```
