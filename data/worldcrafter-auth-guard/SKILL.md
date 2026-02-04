---
name: worldcrafter-auth-guard
description: Add authentication and authorization to routes, Server Actions, and API endpoints using Supabase Auth. Use when user needs "protect [route]", "add authentication", "require login", "add RBAC", "implement login/logout", or mentions auth, permissions, OAuth, API keys. Provides patterns for protected routes, Server Action auth checks, role-based access control (5 roles), OAuth providers (Google, GitHub), email verification, password strength, account lockout, and API key authentication. Do NOT use when building new features (use worldcrafter-feature-builder which can add auth), database-only changes (use worldcrafter-database-setup for RLS policies), routes without auth (use worldcrafter-route-creator), or testing only (use worldcrafter-test-generator).
---

# WorldCrafter Auth Guard

**Version:** 2.0.0
**Last Updated:** 2025-01-09

This skill provides patterns and tools for implementing authentication and authorization in WorldCrafter using Supabase Auth.

## Skill Metadata

**Related Skills:**
- `worldcrafter-feature-builder` - Feature-builder can include auth during creation, use auth-guard to add auth to existing features
- `worldcrafter-route-creator` - Route-creator creates pages, use auth-guard to protect them
- `worldcrafter-database-setup` - Database-setup creates RLS policies (database-level auth), auth-guard adds application-level auth
- `worldcrafter-test-generator` - Use to test auth flows, protected routes, and permission checks

**Example Use Cases:**
- "Protect the dashboard page, require login" → Adds auth check to dashboard page, redirects to login if not authenticated
- "Add authentication to the blog post Server Actions" → Adds auth checks to create/update/delete Server Actions, returns unauthorized error if not logged in
- "Implement role-based access for admin panel" → Creates requireRole helper, adds admin role check to pages, redirects non-admins
- "Make the API endpoint require authentication" → Adds auth check to route.ts, returns 401 status for unauthenticated requests

## When to Use This Skill

Use this skill when:
- Protecting routes from unauthenticated access
- Implementing role-based access control (RBAC)
- Adding authentication to Server Actions
- Securing API routes
- Implementing user session management
- Creating login/logout flows
- Checking user permissions
- Implementing middleware authentication

## WorldCrafter Authentication Architecture

WorldCrafter uses **Supabase Auth** with cookie-based sessions:

- **Session Storage**: HTTP-only cookies (not localStorage)
- **Middleware**: Refreshes auth session on every request
- **Database**: `users` table syncs with Supabase auth.users
- **RLS**: Database-level authorization as second layer

## Authentication Patterns

### Pattern 1: Protect Server Component (Page)

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div>
      <h1>Protected Content</h1>
      <p>Welcome, {user.email}</p>
    </div>
  )
}
```

**When to use:**
- Individual protected pages
- Quick auth check
- Simple authentication requirement

### Pattern 2: Protect via Layout

```typescript
// src/app/(protected)/layout.tsx
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="protected-layout">
      {children}
    </div>
  )
}
```

**When to use:**
- Multiple protected pages under same path
- Shared authentication logic
- Protected route groups

### Pattern 3: Protect Server Action

```typescript
"use server"

import { createClient } from '@/lib/supabase/server'
import { prisma } from '@/lib/prisma'

export async function createPost(data: PostData) {
  // 1. Authentication check
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, error: 'Unauthorized' }
  }

  // 2. Perform action
  const post = await prisma.post.create({
    data: {
      ...data,
      authorId: user.id
    }
  })

  return { success: true, data: post }
}
```

**When to use:**
- Protecting mutations
- User-specific operations
- Data creation/updates

### Pattern 4: Protect API Route

```typescript
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  // Fetch user-specific data
  const data = await prisma.post.findMany({
    where: { authorId: user.id }
  })

  return NextResponse.json(data)
}
```

**When to use:**
- API endpoints
- External integrations
- Mobile app backends

### Pattern 5: Role-Based Access Control (RBAC)

```typescript
import { createClient } from '@/lib/supabase/server'
import { prisma } from '@/lib/prisma'
import { redirect } from 'next/navigation'

async function requireRole(allowedRoles: string[]) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  // Get user role from database
  const dbUser = await prisma.user.findUnique({
    where: { id: user.id },
    select: { role: true }
  })

  if (!dbUser || !allowedRoles.includes(dbUser.role)) {
    redirect('/unauthorized')
  }

  return { user, role: dbUser.role }
}

// Usage in page
export default async function AdminPage() {
  await requireRole(['ADMIN'])

  return <div>Admin content</div>
}
```

**When to use:**
- Admin panels
- Role-specific features
- Permission-based access

### Pattern 6: Middleware Authentication

```typescript
// src/middleware.ts
import { updateSession } from '@/lib/supabase/middleware'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  // Update auth session
  const { response, user } = await updateSession(request)

  // Protect routes
  const protectedPaths = ['/dashboard', '/settings', '/admin']
  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  )

  if (isProtectedPath && !user) {
    const redirectUrl = request.nextUrl.clone()
    redirectUrl.pathname = '/login'
    redirectUrl.searchParams.set('redirectTo', request.nextUrl.pathname)
    return NextResponse.redirect(redirectUrl)
  }

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

**When to use:**
- Global authentication
- Multiple protected routes
- Auth session refresh

## Authorization Patterns

### Check Resource Ownership

```typescript
"use server"

export async function updatePost(id: string, data: PostData) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, error: 'Unauthorized' }
  }

  // Check if user owns the post
  const post = await prisma.post.findUnique({
    where: { id },
    select: { authorId: true }
  })

  if (!post || post.authorId !== user.id) {
    return { success: false, error: 'Forbidden' }
  }

  // User is authorized, proceed
  const updated = await prisma.post.update({
    where: { id },
    data
  })

  return { success: true, data: updated }
}
```

### Permission-Based Authorization

```typescript
async function hasPermission(userId: string, permission: string): Promise<boolean> {
  const userPermissions = await prisma.userPermission.findMany({
    where: { userId },
    select: { permission: true }
  })

  return userPermissions.some(p => p.permission === permission)
}

export async function deletePost(id: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, error: 'Unauthorized' }
  }

  // Check permission
  if (!await hasPermission(user.id, 'posts.delete')) {
    return { success: false, error: 'Forbidden' }
  }

  await prisma.post.delete({ where: { id } })
  return { success: true }
}
```

## Login/Logout Flows

### Login Page

```typescript
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()
  const supabase = createClient()

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setError('')

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password
    })

    if (error) {
      setError(error.message)
    } else {
      router.push('/dashboard')
      router.refresh()
    }
  }

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      {error && <p>{error}</p>}
      <button type="submit">Login</button>
    </form>
  )
}
```

### Logout Action

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export function LogoutButton() {
  const router = useRouter()
  const supabase = createClient()

  async function handleLogout() {
    await supabase.auth.signOut()
    router.push('/login')
    router.refresh()
  }

  return <button onClick={handleLogout}>Logout</button>
}
```

## Common Patterns

### Redirect After Login

```typescript
// In login page
const searchParams = new URLSearchParams(window.location.search)
const redirectTo = searchParams.get('redirectTo') || '/dashboard'

// After successful login
router.push(redirectTo)
```

### Get Current User

```typescript
// Server Component
const supabase = await createClient()
const { data: { user } } = await supabase.auth.getUser()

// Client Component
const supabase = createClient()
const { data: { user } } = await supabase.auth.getUser()
```

### Check if Authenticated (Client)

```typescript
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function useAuth() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)
      setLoading(false)
    }

    getUser()

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null)
      }
    )

    return () => {
      subscription.unsubscribe()
    }
  }, [])

  return { user, loading }
}
```

## OAuth Provider Integration

### Google OAuth

#### Setup Google OAuth Provider

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URI: `https://YOUR_PROJECT.supabase.co/auth/v1/callback`
4. Add Google provider in Supabase Dashboard

Add to `.env`:

```bash
NEXT_PUBLIC_GOOGLE_CLIENT_ID="your-google-client-id"
```

#### Google OAuth Login Page

```typescript
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  async function handleEmailLogin(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) {
      setError(error.message)
      setLoading(false)
    } else {
      router.push('/dashboard')
      router.refresh()
    }
  }

  async function handleGoogleLogin() {
    setError('')
    setLoading(true)

    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
        queryParams: {
          access_type: 'offline',
          prompt: 'consent',
        },
      },
    })

    if (error) {
      setError(error.message)
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-8">
        <div>
          <h2 className="text-center text-3xl font-bold">Sign in</h2>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleEmailLogin} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium">
              Email
            </label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium">
              Password
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in with Email'}
          </Button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="bg-white px-2 text-gray-500">Or continue with</span>
          </div>
        </div>

        <Button
          type="button"
          variant="outline"
          className="w-full"
          onClick={handleGoogleLogin}
          disabled={loading}
        >
          <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24">
            <path
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              fill="#4285F4"
            />
            <path
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              fill="#34A853"
            />
            <path
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              fill="#FBBC05"
            />
            <path
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              fill="#EA4335"
            />
          </svg>
          Sign in with Google
        </Button>

        <p className="text-center text-sm text-gray-600">
          Don't have an account?{' '}
          <a href="/signup" className="font-medium text-blue-600 hover:text-blue-500">
            Sign up
          </a>
        </p>
      </div>
    </div>
  )
}
```

### GitHub OAuth

#### Setup GitHub OAuth Provider

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create OAuth App
3. Authorization callback URL: `https://YOUR_PROJECT.supabase.co/auth/v1/callback`
4. Add GitHub provider in Supabase Dashboard

Add to `.env`:

```bash
NEXT_PUBLIC_GITHUB_CLIENT_ID="your-github-client-id"
```

#### GitHub OAuth Button

```typescript
async function handleGitHubLogin() {
  const { error } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`,
    },
  })

  if (error) {
    setError(error.message)
  }
}
```

Add to login form:

```typescript
<Button
  type="button"
  variant="outline"
  className="w-full"
  onClick={handleGitHubLogin}
  disabled={loading}
>
  <svg className="mr-2 h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
    <path
      fillRule="evenodd"
      d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
      clipRule="evenodd"
    />
  </svg>
  Sign in with GitHub
</Button>
```

### OAuth Callback Route

Create `src/app/auth/callback/route.ts`:

```typescript
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = await createClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  // Redirect to home page or original destination
  const redirectTo = requestUrl.searchParams.get('redirectTo') || '/'
  return NextResponse.redirect(new URL(redirectTo, requestUrl.origin))
}
```

### Link OAuth Account to Existing User

```typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/button'

export function LinkAccountButtons() {
  const supabase = createClient()

  async function linkGoogle() {
    const { error } = await supabase.auth.linkIdentity({
      provider: 'google',
    })

    if (error) {
      console.error('Error linking Google account:', error)
    }
  }

  async function linkGitHub() {
    const { error } = await supabase.auth.linkIdentity({
      provider: 'github',
    })

    if (error) {
      console.error('Error linking GitHub account:', error)
    }
  }

  return (
    <div className="space-y-4">
      <h3>Link Additional Accounts</h3>
      <Button onClick={linkGoogle}>Link Google Account</Button>
      <Button onClick={linkGitHub}>Link GitHub Account</Button>
    </div>
  )
}
```

## Email Verification Flow

### Signup with Email Verification

#### Signup Page with Verification

```typescript
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useRouter } from 'next/navigation'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setLoading(true)

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/confirm`,
      },
    })

    if (error) {
      setError(error.message)
      setLoading(false)
    } else {
      setSuccess(true)
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="w-full max-w-md space-y-8 p-8">
          <div className="rounded-md bg-green-50 p-4">
            <h3 className="text-lg font-medium text-green-800">
              Check your email
            </h3>
            <p className="mt-2 text-sm text-green-700">
              We've sent a verification link to <strong>{email}</strong>.
              Please check your inbox and click the link to verify your account.
            </p>
          </div>
          <Button
            variant="outline"
            className="w-full"
            onClick={() => router.push('/login')}
          >
            Back to Login
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-8">
        <div>
          <h2 className="text-center text-3xl font-bold">Create an account</h2>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSignup} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium">
              Email
            </label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium">
              Password
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={12}
              disabled={loading}
            />
            <p className="mt-1 text-sm text-gray-500">
              Minimum 12 characters, include uppercase, number, and special character
            </p>
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign up'}
          </Button>
        </form>

        <p className="text-center text-sm text-gray-600">
          Already have an account?{' '}
          <a href="/login" className="font-medium text-blue-600 hover:text-blue-500">
            Sign in
          </a>
        </p>
      </div>
    </div>
  )
}
```

### Email Confirmation Page

Create `src/app/auth/confirm/page.tsx`:

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ConfirmPage({
  searchParams,
}: {
  searchParams: { token_hash?: string; type?: string }
}) {
  const supabase = await createClient()

  if (searchParams.token_hash && searchParams.type) {
    const { error } = await supabase.auth.verifyOtp({
      token_hash: searchParams.token_hash,
      type: searchParams.type as any,
    })

    if (!error) {
      redirect('/dashboard')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-8">
        <div className="rounded-md bg-yellow-50 p-4">
          <h3 className="text-lg font-medium text-yellow-800">
            Verification in progress
          </h3>
          <p className="mt-2 text-sm text-yellow-700">
            Please wait while we verify your email...
          </p>
        </div>
      </div>
    </div>
  )
}
```

### Resend Verification Email

```typescript
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export function ResendVerificationEmail() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const supabase = createClient()

  async function handleResend(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    const { error } = await supabase.auth.resend({
      type: 'signup',
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/confirm`,
      },
    })

    if (error) {
      setMessage(error.message)
    } else {
      setMessage('Verification email sent! Check your inbox.')
    }

    setLoading(false)
  }

  return (
    <form onSubmit={handleResend} className="space-y-4">
      <h3 className="text-lg font-medium">Resend Verification Email</h3>

      {message && (
        <div className="rounded-md bg-blue-50 p-4">
          <p className="text-sm text-blue-800">{message}</p>
        </div>
      )}

      <div>
        <label htmlFor="resend-email" className="block text-sm font-medium">
          Email
        </label>
        <Input
          id="resend-email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={loading}
        />
      </div>

      <Button type="submit" disabled={loading}>
        {loading ? 'Sending...' : 'Resend Verification Email'}
      </Button>
    </form>
  )
}
```

### Check Email Verification Status

```typescript
"use server"

import { createClient } from '@/lib/supabase/server'

export async function checkEmailVerified(): Promise<boolean> {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return false
  }

  // Check if email is verified
  return user.email_confirmed_at !== null
}
```

Use in Server Component:

```typescript
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { ResendVerificationEmail } from './ResendVerificationEmail'

export default async function ProtectedPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  if (!user.email_confirmed_at) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="w-full max-w-md space-y-8 p-8">
          <div className="rounded-md bg-yellow-50 p-4">
            <h3 className="text-lg font-medium text-yellow-800">
              Email not verified
            </h3>
            <p className="mt-2 text-sm text-yellow-700">
              Please verify your email address to access this page.
            </p>
          </div>
          <ResendVerificationEmail />
        </div>
      </div>
    )
  }

  return <div>Protected content</div>
}
```

## API Key Authentication

### Database Schema for API Keys

Add to `prisma/schema.prisma`:

```prisma
model ApiKey {
  id          String    @id @default(cuid())
  userId      String    @map("user_id")
  name        String
  key         String    @unique
  lastUsedAt  DateTime? @map("last_used_at")
  expiresAt   DateTime? @map("expires_at")
  createdAt   DateTime  @default(now()) @map("created_at")

  user        User      @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([key])
  @@map("api_keys")
}
```

### Generate API Key

```typescript
"use server"

import { createClient } from '@/lib/supabase/server'
import { prisma } from '@/lib/prisma'
import { randomBytes } from 'crypto'

export async function generateApiKey(name: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, error: 'Unauthorized' }
  }

  // Generate secure random key
  const key = `wc_${randomBytes(32).toString('hex')}`

  const apiKey = await prisma.apiKey.create({
    data: {
      userId: user.id,
      name,
      key,
    },
  })

  return { success: true, data: { key: apiKey.key, name: apiKey.name } }
}

export async function listApiKeys() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, error: 'Unauthorized' }
  }

  const keys = await prisma.apiKey.findMany({
    where: { userId: user.id },
    select: {
      id: true,
      name: true,
      lastUsedAt: true,
      createdAt: true,
      expiresAt: true,
      // Don't return the actual key for security
    },
    orderBy: { createdAt: 'desc' },
  })

  return { success: true, data: keys }
}

export async function revokeApiKey(keyId: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, error: 'Unauthorized' }
  }

  await prisma.apiKey.delete({
    where: {
      id: keyId,
      userId: user.id, // Ensure user owns the key
    },
  })

  return { success: true }
}
```

### Validate API Key (Middleware)

Create `src/lib/auth/api-key.ts`:

```typescript
import { prisma } from '@/lib/prisma'
import { NextRequest } from 'next/server'

export async function validateApiKey(
  request: NextRequest
): Promise<{ valid: boolean; userId?: string }> {
  const authHeader = request.headers.get('authorization')

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return { valid: false }
  }

  const key = authHeader.substring(7) // Remove 'Bearer '

  const apiKey = await prisma.apiKey.findUnique({
    where: { key },
    select: {
      id: true,
      userId: true,
      expiresAt: true,
    },
  })

  if (!apiKey) {
    return { valid: false }
  }

  // Check if expired
  if (apiKey.expiresAt && apiKey.expiresAt < new Date()) {
    return { valid: false }
  }

  // Update last used timestamp
  await prisma.apiKey.update({
    where: { id: apiKey.id },
    data: { lastUsedAt: new Date() },
  })

  return { valid: true, userId: apiKey.userId }
}
```

### Protect API Route with API Key

```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { validateApiKey } from '@/lib/auth/api-key'
import { prisma } from '@/lib/prisma'

export async function GET(request: NextRequest) {
  // Validate API key
  const { valid, userId } = await validateApiKey(request)

  if (!valid || !userId) {
    return NextResponse.json(
      { error: 'Invalid or missing API key' },
      { status: 401 }
    )
  }

  // Fetch user-specific data
  const data = await prisma.world.findMany({
    where: { ownerId: userId },
  })

  return NextResponse.json(data)
}
```

### API Key Management UI

```typescript
'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { generateApiKey, listApiKeys, revokeApiKey } from './actions'

export function ApiKeyManager() {
  const [keys, setKeys] = useState<any[]>([])
  const [newKeyName, setNewKeyName] = useState('')
  const [generatedKey, setGeneratedKey] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadKeys()
  }, [])

  async function loadKeys() {
    const result = await listApiKeys()
    if (result.success) {
      setKeys(result.data)
    }
  }

  async function handleGenerate(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)

    const result = await generateApiKey(newKeyName)
    if (result.success) {
      setGeneratedKey(result.data.key)
      setNewKeyName('')
      await loadKeys()
    }

    setLoading(false)
  }

  async function handleRevoke(keyId: string) {
    if (!confirm('Are you sure you want to revoke this API key?')) {
      return
    }

    await revokeApiKey(keyId)
    await loadKeys()
  }

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-bold">API Keys</h2>
        <p className="text-gray-600">
          Manage your API keys for programmatic access
        </p>
      </div>

      {generatedKey && (
        <div className="rounded-md bg-green-50 p-4">
          <h3 className="text-lg font-medium text-green-800">
            API Key Generated
          </h3>
          <p className="mt-2 text-sm text-green-700">
            Save this key securely. You won't be able to see it again.
          </p>
          <div className="mt-4 flex items-center space-x-2">
            <code className="rounded bg-green-100 px-2 py-1 font-mono text-sm">
              {generatedKey}
            </code>
            <Button
              size="sm"
              variant="outline"
              onClick={() => {
                navigator.clipboard.writeText(generatedKey)
              }}
            >
              Copy
            </Button>
          </div>
          <Button
            className="mt-4"
            size="sm"
            variant="outline"
            onClick={() => setGeneratedKey('')}
          >
            Done
          </Button>
        </div>
      )}

      <form onSubmit={handleGenerate} className="space-y-4">
        <h3 className="text-lg font-medium">Generate New API Key</h3>
        <div className="flex space-x-2">
          <Input
            type="text"
            placeholder="Key name (e.g., Production API)"
            value={newKeyName}
            onChange={(e) => setNewKeyName(e.target.value)}
            required
            disabled={loading}
          />
          <Button type="submit" disabled={loading}>
            Generate
          </Button>
        </div>
      </form>

      <div>
        <h3 className="text-lg font-medium">Your API Keys</h3>
        <div className="mt-4 space-y-4">
          {keys.map((key) => (
            <div
              key={key.id}
              className="flex items-center justify-between rounded-md border p-4"
            >
              <div>
                <p className="font-medium">{key.name}</p>
                <p className="text-sm text-gray-500">
                  Created: {new Date(key.createdAt).toLocaleDateString()}
                  {key.lastUsedAt && (
                    <span>
                      {' '}
                      • Last used:{' '}
                      {new Date(key.lastUsedAt).toLocaleDateString()}
                    </span>
                  )}
                </p>
              </div>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => handleRevoke(key.id)}
              >
                Revoke
              </Button>
            </div>
          ))}
          {keys.length === 0 && (
            <p className="text-gray-500">No API keys yet</p>
          )}
        </div>
      </div>
    </div>
  )
}
```

### Rate Limiting with API Keys

Create `src/lib/auth/rate-limit.ts`:

```typescript
import { prisma } from '@/lib/prisma'

interface RateLimitResult {
  allowed: boolean
  remaining: number
  resetAt: Date
}

export async function checkRateLimit(
  apiKeyId: string,
  limit: number = 100,
  windowMs: number = 60000 // 1 minute
): Promise<RateLimitResult> {
  const now = new Date()
  const windowStart = new Date(now.getTime() - windowMs)

  // Count requests in current window
  const count = await prisma.apiRequest.count({
    where: {
      apiKeyId,
      createdAt: {
        gte: windowStart,
      },
    },
  })

  const allowed = count < limit
  const remaining = Math.max(0, limit - count - 1)
  const resetAt = new Date(now.getTime() + windowMs)

  if (allowed) {
    // Log this request
    await prisma.apiRequest.create({
      data: {
        apiKeyId,
        createdAt: now,
      },
    })
  }

  return { allowed, remaining, resetAt }
}
```

Add to schema:

```prisma
model ApiRequest {
  id        String   @id @default(cuid())
  apiKeyId  String   @map("api_key_id")
  createdAt DateTime @default(now()) @map("created_at")

  apiKey    ApiKey   @relation(fields: [apiKeyId], references: [id], onDelete: Cascade)

  @@index([apiKeyId, createdAt])
  @@map("api_requests")
}
```

Use in API route:

```typescript
import { validateApiKey } from '@/lib/auth/api-key'
import { checkRateLimit } from '@/lib/auth/rate-limit'

export async function GET(request: NextRequest) {
  const { valid, userId } = await validateApiKey(request)

  if (!valid) {
    return NextResponse.json({ error: 'Invalid API key' }, { status: 401 })
  }

  // Check rate limit
  const { allowed, remaining, resetAt } = await checkRateLimit(userId!, 100)

  if (!allowed) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      {
        status: 429,
        headers: {
          'X-RateLimit-Remaining': '0',
          'X-RateLimit-Reset': resetAt.toISOString(),
        },
      }
    )
  }

  // Process request
  const data = await fetchData(userId!)

  return NextResponse.json(data, {
    headers: {
      'X-RateLimit-Remaining': remaining.toString(),
      'X-RateLimit-Reset': resetAt.toISOString(),
    },
  })
}
```

## Password Validation

### Password Validation Schema

Create `src/lib/schemas/password.ts`:

```typescript
import { z } from 'zod'

export const passwordSchema = z
  .string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(
    /[^A-Za-z0-9]/,
    'Password must contain at least one special character'
  )

export const passwordConfirmSchema = z
  .object({
    password: passwordSchema,
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  })

export type PasswordData = z.infer<typeof passwordSchema>
export type PasswordConfirmData = z.infer<typeof passwordConfirmSchema>
```

### Password Strength Indicator

Create `src/components/auth/PasswordStrength.tsx`:

```typescript
'use client'

interface PasswordStrengthProps {
  password: string
}

export function PasswordStrength({ password }: PasswordStrengthProps) {
  const checks = {
    length: password.length >= 12,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    number: /[0-9]/.test(password),
    special: /[^A-Za-z0-9]/.test(password),
  }

  const passedChecks = Object.values(checks).filter(Boolean).length
  const strength = Math.min(100, (passedChecks / 5) * 100)

  let strengthLabel = 'Weak'
  let strengthColor = 'bg-red-500'

  if (strength >= 80) {
    strengthLabel = 'Strong'
    strengthColor = 'bg-green-500'
  } else if (strength >= 60) {
    strengthLabel = 'Good'
    strengthColor = 'bg-yellow-500'
  } else if (strength >= 40) {
    strengthLabel = 'Fair'
    strengthColor = 'bg-orange-500'
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">Password Strength</span>
        <span className="text-sm font-medium">{strengthLabel}</span>
      </div>
      <div className="h-2 w-full rounded-full bg-gray-200">
        <div
          className={`h-full rounded-full transition-all ${strengthColor}`}
          style={{ width: `${strength}%` }}
        />
      </div>
      <ul className="space-y-1 text-sm">
        <li className={checks.length ? 'text-green-600' : 'text-gray-500'}>
          {checks.length ? '✓' : '○'} At least 12 characters
        </li>
        <li className={checks.uppercase ? 'text-green-600' : 'text-gray-500'}>
          {checks.uppercase ? '✓' : '○'} One uppercase letter
        </li>
        <li className={checks.lowercase ? 'text-green-600' : 'text-gray-500'}>
          {checks.lowercase ? '✓' : '○'} One lowercase letter
        </li>
        <li className={checks.number ? 'text-green-600' : 'text-gray-500'}>
          {checks.number ? '✓' : '○'} One number
        </li>
        <li className={checks.special ? 'text-green-600' : 'text-gray-500'}>
          {checks.special ? '✓' : '○'} One special character
        </li>
      </ul>
    </div>
  )
}
```

### Signup Form with Password Validation

```typescript
'use client'

import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { passwordConfirmSchema, type PasswordConfirmData } from '@/lib/schemas/password'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { PasswordStrength } from '@/components/auth/PasswordStrength'

export default function SignupFormWithValidation() {
  const [password, setPassword] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PasswordConfirmData>({
    resolver: zodResolver(passwordConfirmSchema),
  })

  async function onSubmit(data: PasswordConfirmData) {
    // Handle signup
    console.log('Signup data:', data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <Input
          id="password"
          type="password"
          {...register('password')}
          onChange={(e) => setPassword(e.target.value)}
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
        )}
      </div>

      {password && <PasswordStrength password={password} />}

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium">
          Confirm Password
        </label>
        <Input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
        />
        {errors.confirmPassword && (
          <p className="mt-1 text-sm text-red-600">
            {errors.confirmPassword.message}
          </p>
        )}
      </div>

      <Button type="submit" className="w-full">
        Create Account
      </Button>
    </form>
  )
}
```

### Server-Side Password Validation

```typescript
"use server"

import { createClient } from '@/lib/supabase/server'
import { passwordSchema } from '@/lib/schemas/password'

export async function signupWithValidation(email: string, password: string) {
  // Validate password on server
  const validation = passwordSchema.safeParse(password)

  if (!validation.success) {
    return {
      success: false,
      error: validation.error.errors[0].message,
    }
  }

  const supabase = await createClient()
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  })

  if (error) {
    return { success: false, error: error.message }
  }

  return { success: true, data }
}
```

## Account Lockout Pattern

### Database Schema for Login Attempts

Add to `prisma/schema.prisma`:

```prisma
model LoginAttempt {
  id          String   @id @default(cuid())
  email       String
  ipAddress   String   @map("ip_address")
  success     Boolean
  attemptedAt DateTime @default(now()) @map("attempted_at")

  @@index([email, attemptedAt])
  @@index([ipAddress, attemptedAt])
  @@map("login_attempts")
}

model AccountLock {
  id          String   @id @default(cuid())
  userId      String   @unique @map("user_id")
  lockedAt    DateTime @default(now()) @map("locked_at")
  unlockAt    DateTime @map("unlock_at")
  reason      String?

  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("account_locks")
}
```

### Login Attempt Tracking

Create `src/lib/auth/login-attempts.ts`:

```typescript
import { prisma } from '@/lib/prisma'

const MAX_ATTEMPTS = 5
const LOCKOUT_DURATION_MS = 30 * 60 * 1000 // 30 minutes
const ATTEMPT_WINDOW_MS = 30 * 60 * 1000 // 30 minutes

export async function recordLoginAttempt(
  email: string,
  ipAddress: string,
  success: boolean
): Promise<void> {
  await prisma.loginAttempt.create({
    data: {
      email,
      ipAddress,
      success,
    },
  })
}

export async function checkAccountLocked(email: string): Promise<{
  locked: boolean
  unlockAt?: Date
  attemptsRemaining?: number
}> {
  // Check if account is explicitly locked
  const user = await prisma.user.findUnique({
    where: { email },
    include: { accountLock: true },
  })

  if (!user) {
    return { locked: false }
  }

  // Check for active lock
  if (user.accountLock) {
    if (user.accountLock.unlockAt > new Date()) {
      return {
        locked: true,
        unlockAt: user.accountLock.unlockAt,
      }
    } else {
      // Lock expired, remove it
      await prisma.accountLock.delete({
        where: { userId: user.id },
      })
    }
  }

  // Count failed attempts in window
  const windowStart = new Date(Date.now() - ATTEMPT_WINDOW_MS)
  const failedAttempts = await prisma.loginAttempt.count({
    where: {
      email,
      success: false,
      attemptedAt: {
        gte: windowStart,
      },
    },
  })

  if (failedAttempts >= MAX_ATTEMPTS) {
    // Lock the account
    const unlockAt = new Date(Date.now() + LOCKOUT_DURATION_MS)

    await prisma.accountLock.create({
      data: {
        userId: user.id,
        unlockAt,
        reason: 'Too many failed login attempts',
      },
    })

    return {
      locked: true,
      unlockAt,
    }
  }

  return {
    locked: false,
    attemptsRemaining: MAX_ATTEMPTS - failedAttempts,
  }
}

export async function unlockAccount(userId: string): Promise<void> {
  await prisma.accountLock.delete({
    where: { userId },
  })

  // Clear failed attempts
  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { email: true },
  })

  if (user) {
    await prisma.loginAttempt.deleteMany({
      where: {
        email: user.email,
        success: false,
      },
    })
  }
}
```

### Login with Lockout Protection

```typescript
"use server"

import { createClient } from '@/lib/supabase/server'
import { recordLoginAttempt, checkAccountLocked } from '@/lib/auth/login-attempts'
import { headers } from 'next/headers'

export async function loginWithLockout(email: string, password: string) {
  // Get IP address
  const headersList = headers()
  const ipAddress = headersList.get('x-forwarded-for') || 'unknown'

  // Check if account is locked
  const lockStatus = await checkAccountLocked(email)

  if (lockStatus.locked) {
    const minutesRemaining = Math.ceil(
      (lockStatus.unlockAt!.getTime() - Date.now()) / 60000
    )

    return {
      success: false,
      error: `Account is locked due to too many failed login attempts. Try again in ${minutesRemaining} minutes.`,
      locked: true,
    }
  }

  // Attempt login
  const supabase = await createClient()
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })

  // Record attempt
  await recordLoginAttempt(email, ipAddress, !error)

  if (error) {
    // Check if this failed attempt triggers a lock
    const newLockStatus = await checkAccountLocked(email)

    if (newLockStatus.locked) {
      return {
        success: false,
        error: `Too many failed attempts. Account is now locked for 30 minutes.`,
        locked: true,
      }
    }

    return {
      success: false,
      error: error.message,
      attemptsRemaining: newLockStatus.attemptsRemaining,
    }
  }

  return { success: true, data }
}
```

### Login Form with Lockout Feedback

```typescript
'use client'

import { useState } from 'react'
import { loginWithLockout } from './actions'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useRouter } from 'next/navigation'

export default function LoginWithLockout() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [attemptsRemaining, setAttemptsRemaining] = useState<number | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setAttemptsRemaining(null)
    setLoading(true)

    const result = await loginWithLockout(email, password)

    if (result.success) {
      router.push('/dashboard')
      router.refresh()
    } else {
      setError(result.error)
      if (result.attemptsRemaining !== undefined) {
        setAttemptsRemaining(result.attemptsRemaining)
      }
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 p-8">
        <div>
          <h2 className="text-center text-3xl font-bold">Sign in</h2>
        </div>

        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{error}</p>
            {attemptsRemaining !== null && attemptsRemaining > 0 && (
              <p className="mt-2 text-sm text-red-700">
                {attemptsRemaining} attempt{attemptsRemaining !== 1 ? 's' : ''}{' '}
                remaining before account lockout.
              </p>
            )}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium">
              Email
            </label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium">
              Password
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </Button>
        </form>

        <p className="text-center text-sm text-gray-600">
          <a
            href="/forgot-password"
            className="font-medium text-blue-600 hover:text-blue-500"
          >
            Forgot your password?
          </a>
        </p>
      </div>
    </div>
  )
}
```

### Admin: Unlock User Account

```typescript
"use server"

import { createClient } from '@/lib/supabase/server'
import { prisma } from '@/lib/prisma'
import { unlockAccount } from '@/lib/auth/login-attempts'

export async function adminUnlockAccount(userId: string) {
  // Check admin permissions
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { success: false, error: 'Unauthorized' }
  }

  const adminUser = await prisma.user.findUnique({
    where: { id: user.id },
    select: { role: true },
  })

  if (adminUser?.role !== 'ADMIN') {
    return { success: false, error: 'Insufficient permissions' }
  }

  // Unlock account
  await unlockAccount(userId)

  return { success: true }
}
```

## Reference Files

- `references/auth-patterns.md` - Comprehensive authentication patterns
- `references/middleware-guide.md` - Middleware configuration
- `references/worldcrafter-rbac.md` - Complete RBAC system with 5 roles
- `references/related-skills.md` - How this skill works with other WorldCrafter skills
- `assets/templates/` - Auth component templates

## Skill Orchestration

This skill adds authentication and authorization to existing routes, features, and Server Actions.

### Common Workflows

**Protecting Existing Routes:**
1. **worldcrafter-route-creator** - Creates page structure
2. **worldcrafter-auth-guard** (this skill) - Adds auth check to protect page

**Complete Feature with Authentication:**
1. **worldcrafter-database-setup** - Creates database tables
2. **worldcrafter-feature-builder** - Creates feature with forms and Server Actions
3. **worldcrafter-auth-guard** (this skill) - Adds auth checks to Server Actions and routes

**Implementing Login/Logout:**
1. **worldcrafter-auth-guard** (this skill only) - Creates login page, logout button, signup flow

**Role-Based Access Control:**
1. **worldcrafter-database-setup** - Adds role column to users table
2. **worldcrafter-auth-guard** (this skill) - Implements requireRole helper and admin checks

**Database + Application Auth:**
1. **worldcrafter-database-setup** - Creates RLS policies (database-level protection)
2. **worldcrafter-auth-guard** (this skill) - Adds application-level auth checks (Server Actions, routes)

### When Claude Should Use Multiple Skills

Claude will orchestrate auth-guard with other skills when:
- User wants a feature that requires authentication (feature-builder → auth-guard)
- User wants to protect simple pages (route-creator → auth-guard)
- User wants both database and application-level security (database-setup → auth-guard)
- User wants to test auth flows (auth-guard → test-generator)

**Example orchestration:**
```
User: "Create a blog feature where users can only edit their own posts"

Claude's workflow:
1. worldcrafter-database-setup:
   - Creates BlogPost model with authorId
   - Adds RLS policy: users can only update posts where authorId = auth.uid()

2. worldcrafter-feature-builder:
   - Creates blog post form
   - Creates CRUD Server Actions

3. worldcrafter-auth-guard (this skill):
   - Adds auth check to Server Actions
   - Verifies user.id matches post.authorId before updates
   - Protects /posts/new route (login required)

4. worldcrafter-test-generator:
   - Tests that unauthenticated users can't create posts
   - Tests that users can't edit others' posts
```

### Skill Selection Guidance

**Choose this skill when:**
- User explicitly mentions "protect", "authentication", "login", "auth", "permissions"
- User wants to add auth to existing code
- User wants login/logout flows
- User wants role-based access control

**Choose worldcrafter-feature-builder instead when:**
- User wants a complete feature from scratch
- Feature-builder can include auth during creation
- Better to build feature with auth from the start

**Use this skill AFTER other skills when:**
- Feature already exists, needs auth added
- Routes created by route-creator need protection
- Database setup complete, need application-level checks

**Two-Layer Security Pattern:**
- Database layer: worldcrafter-database-setup creates RLS policies
- Application layer: worldcrafter-auth-guard adds Server Action auth checks
- Both layers working together provide defense in depth

## Helper Scripts

```bash
# Add auth guard to existing page
python .claude/skills/worldcrafter-auth-guard/scripts/add_auth_guard.py src/app/dashboard/page.tsx

# Add auth check to Server Action
python .claude/skills/worldcrafter-auth-guard/scripts/add_auth_guard.py src/app/posts/actions.ts --action
```

## Security Best Practices

1. **Always validate on server** - Never trust client-side auth checks
2. **Use RLS policies** - Database-level protection as second layer
3. **Check resource ownership** - Verify user owns data before operations
4. **Use HTTP-only cookies** - Prevent XSS attacks
5. **Refresh sessions** - Use middleware to keep sessions fresh
6. **Handle errors gracefully** - Don't expose sensitive info in errors
7. **Implement rate limiting** - Protect against brute force
8. **Use secure passwords** - Enforce strong password policies

## Success Criteria

Complete authentication implementation includes:
- ✅ Protected routes redirect to login
- ✅ Server Actions check authentication
- ✅ API routes return 401 for unauthenticated
- ✅ User can login and logout
- ✅ Sessions refresh automatically
- ✅ Resource ownership verified
- ✅ RLS policies enforce permissions
- ✅ Error handling doesn't leak info
- ✅ Middleware configured correctly
