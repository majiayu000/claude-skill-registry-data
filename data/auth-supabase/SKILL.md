---
name: auth-supabase
description: Implements standard Supabase authentication flows including signup, login, password reset, OAuth providers, email verification, and session management with complete security best practices
---

# Supabase Authentication Implementation Standards

This skill provides comprehensive guidelines for implementing authentication using Supabase, covering all authentication patterns, security practices, and environment configuration.

## 🚨 CRITICAL REQUIREMENTS - MUST READ FIRST

### Package Versions - MANDATORY (Security Critical)

**✅ REQUIRED VERSIONS (Latest Stable):**
```json
{
  "dependencies": {
    "@supabase/supabase-js": "^2.89.0",      
    "@supabase/ssr": "^0.8.0",             
    "next": "^16.1.1"                       
  }
}
```

**❌ DEPRECATED PACKAGES - DO NOT USE:**
```json
{
  "@supabase/auth-helpers-nextjs": "...",   // ❌ DEPRECATED
  "@supabase/auth-helpers-react": "...",    // ❌ DEPRECATED  
  "@supabase/auth-ui-react": "..."          // ❌ Optional, not required
}
```

**🔒 Security Rule:**
- Always use `@supabase/ssr` for Next.js 13+ App Router
- Never use deprecated `auth-helpers` packages
- Update packages monthly: `npm update @supabase/supabase-js @supabase/ssr`

### Next.js 14 Server Actions - MANDATORY PATTERN

**❌ ANTI-PATTERN - NEVER DO THIS:**
```typescript
// ❌ WRONG - Server action inside client component
'use client';

export default function LoginPage() {
  async function login(formData: FormData) {
    'use server';  // ❌ Mixed directives cause issues
    // ...
  }
}
```

**✅ REQUIRED PATTERN - ALWAYS USE THIS:**
```typescript
// app/actions/auth.ts
'use server';  // ✅ Dedicated file for all auth actions

import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function loginAction(formData: FormData) {
  const supabase = await createClient()
  
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { error } = await supabase.auth.signInWithPassword(data)

  if (error) {
    return { error: error.message }
  }

  redirect('/dashboard')
}

export async function signUpAction(formData: FormData) {
  const supabase = await createClient()
  
  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
    options: {
      data: {
        full_name: formData.get('full_name') as string,
      },
    },
  }

  const { error } = await supabase.auth.signUp(data)

  if (error) {
    return { error: error.message }
  }

  redirect('/auth/confirm')
}

export async function logoutAction() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  redirect('/login')
}

// app/(auth)/login/page.tsx
'use client';  // ✅ Separate client component file

import { loginAction } from '@/app/actions/auth'
import { useState } from 'react'

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null)

  return (
    <form action={async (formData) => {
      const result = await loginAction(formData)
      if (result?.error) {
        setError(result.error)
      }
    }}>
      {/* Form fields */}
    </form>
  )
}
```

**📁 MANDATORY File Structure:**
```
app/
├── actions/
│   └── auth.ts              ✅ All auth server actions here
├── lib/
│   └── supabase/
│       ├── client.ts         ✅ Browser client
│       ├── server.ts         ✅ Server client  
│       └── middleware.ts     ✅ Middleware client
├── (auth)/
│   ├── login/
│   │   └── page.tsx         ✅ Client component
│   ├── register/
│   │   └── page.tsx         ✅ Client component
│   └── callback/
│       └── route.ts         ✅ Route handler
└── middleware.ts            ✅ Session refresh
```

**🔒 RULES:**
1. All auth server actions → `app/actions/auth.ts` with `'use server'`
2. All auth pages → Client components with `'use client'`
3. NO mixing of directives in same file
4. Use `async/await` for all Supabase calls

## Initial Setup Checklist

### Environment Variables

**Required Variables (.env.local):**

```bash
# Supabase Core
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Supabase Service Role (Server-side only - NEVER expose to client)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# Application URLs
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_REDIRECT_URL=http://localhost:3000/auth/callback

# Email Configuration (Optional - for custom SMTP)
SUPABASE_SMTP_HOST=smtp.sendgrid.net
SUPABASE_SMTP_PORT=587
SUPABASE_SMTP_USER=apikey
SUPABASE_SMTP_PASS=your-sendgrid-api-key
SUPABASE_SMTP_SENDER_EMAIL=noreply@yourdomain.com
SUPABASE_SMTP_SENDER_NAME=Your App Name
```

**Production Variables:**

```bash
NEXT_PUBLIC_SITE_URL=https://yourdomain.com
NEXT_PUBLIC_REDIRECT_URL=https://yourdomain.com/auth/callback
```

### Supabase Dashboard Configuration

1. **Authentication Settings** (`Authentication > Settings`)
   - [ ] Set Site URL: `https://yourdomain.com`
   - [ ] Add redirect URLs:
     - `http://localhost:3000/auth/callback` (development)
     - `https://yourdomain.com/auth/callback` (production)
   - [ ] Enable email confirmations (recommended)
   - [ ] Configure session timeout (default: 1 week)

2. **Email Templates** (`Authentication > Email Templates`)
   - [ ] Customize confirmation email
   - [ ] Customize password reset email
   - [ ] Customize magic link email (if using)
   - See `templates/email-templates.md` for examples

3. **OAuth Providers** (if using social auth)
   - [ ] Google: Add Client ID and Secret
   - [ ] GitHub: Add Client ID and Secret
   - [ ] Others as needed

## Supabase Client Initialization

### Next.js App Router Implementation

**Create Supabase client utilities:**

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

```typescript
// lib/supabase/server.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value, ...options })
          } catch (error) {
            // Handle cookie setting in Server Component
          }
        },
        remove(name: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value: '', ...options })
          } catch (error) {
            // Handle cookie removal in Server Component
          }
        },
      },
    }
  )
}
```

```typescript
// lib/supabase/middleware.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function updateSession(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value,
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value: '',
            ...options,
          })
        },
      },
    }
  )

  await supabase.auth.getUser()

  return response
}
```

**Middleware configuration:**

```typescript
// middleware.ts
import { updateSession } from '@/lib/supabase/middleware'

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

## Authentication Flows

### 1. Sign Up Flow

**✅ REQUIRED IMPLEMENTATION:**

```typescript
// app/actions/auth.ts
'use server';

import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function signUpAction(formData: FormData) {
  const supabase = await createClient()

  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
    options: {
      data: {
        full_name: formData.get('full_name') as string,
      },
      emailRedirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/auth/callback`,
    },
  }

  const { error } = await supabase.auth.signUp(data)

  if (error) {
    return { error: error.message }
  }

  redirect('/auth/confirm')
}
```

**Sign Up Component (REQUIRED PATTERN):**

```tsx
// app/(auth)/register/page.tsx
'use client';

import { signUpAction } from '@/app/actions/auth'
import { useState } from 'react'

export default function SignUpPage() {
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-bold text-start mb-6">
          Create Account
        </h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-4 text-start">
            {error}
          </div>
        )}
        
        <form 
          action={async (formData) => {
            setLoading(true)
            const result = await signUpAction(formData)
            setLoading(false)
            
            if (result?.error) {
              setError(result.error)
            }
          }}
          className="space-y-4"
        >
          <div>
            <label 
              htmlFor="full_name" 
              className="block text-start mb-2 font-medium"
            >
              Full Name
            </label>
            <input
              id="full_name"
              name="full_name"
              type="text"
              dir="auto"
              className="w-full ps-4 pe-4 py-3 text-start rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="Enter your full name"
              required
            />
          </div>

          <div>
            <label 
              htmlFor="email" 
              className="block text-start mb-2 font-medium"
            >
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              dir="auto"
              className="w-full ps-4 pe-4 py-3 text-start rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="Enter your email"
              required
            />
          </div>

          <div>
            <label 
              htmlFor="password" 
              className="block text-start mb-2 font-medium"
            >
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              dir="auto"
              className="w-full ps-4 pe-4 py-3 text-start rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="Create a password"
              required
              minLength={8}
            />
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### 2. Login Flow

**✅ REQUIRED IMPLEMENTATION:**

```typescript
// app/actions/auth.ts (add to existing file)
'use server';

export async function loginAction(formData: FormData) {
  const supabase = await createClient()

  const data = {
    email: formData.get('email') as string,
    password: formData.get('password') as string,
  }

  const { error } = await supabase.auth.signInWithPassword(data)

  if (error) {
    return { error: error.message }
  }

  redirect('/dashboard')
}
```

**Login Component (REQUIRED PATTERN):**

```tsx
// app/(auth)/login/page.tsx
'use client';

import { loginAction } from '@/app/actions/auth'
import { useState } from 'react'
import Link from 'next/link'

export default function LoginPage() {
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-bold text-start mb-6">
          Sign In
        </h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg mb-4 text-start">
            {error}
          </div>
        )}
        
        <form 
          action={async (formData) => {
            setLoading(true)
            const result = await loginAction(formData)
            setLoading(false)
            
            if (result?.error) {
              setError(result.error)
            }
          }}
          className="space-y-4"
        >
          <div>
            <label 
              htmlFor="email" 
              className="block text-start mb-2 font-medium"
            >
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              dir="auto"
              className="w-full ps-4 pe-4 py-3 text-start rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="Enter your email"
              required
            />
          </div>

          <div>
            <label 
              htmlFor="password" 
              className="block text-start mb-2 font-medium"
            >
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              dir="auto"
              className="w-full ps-4 pe-4 py-3 text-start rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              placeholder="Enter your password"
              required
              minLength={8}
            />
          </div>

          <div className="flex items-center justify-between">
            <Link 
              href="/auth/forgot-password"
              className="text-sm text-blue-600 hover:underline"
            >
              Forgot password?
            </Link>
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <p className="text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <Link href="/register" className="text-blue-600 hover:underline">
              Sign up
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}
```

### 3. Password Reset Flow

```typescript
// app/actions/auth.ts (add to existing file)
'use server';

export async function requestPasswordResetAction(formData: FormData) {
  const supabase = await createClient()
  const email = formData.get('email') as string

  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/auth/reset-password`,
  })

  if (error) {
    return { error: error.message }
  }

  return { success: true }
}

export async function resetPasswordAction(formData: FormData) {
  const supabase = await createClient()
  const password = formData.get('password') as string

  const { error } = await supabase.auth.updateUser({
    password: password,
  })

  if (error) {
    return { error: error.message }
  }

  redirect('/login?message=Password updated successfully')
}
```

### 4. OAuth Login (Google, GitHub, etc.)

```typescript
// app/auth/oauth/route.ts
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const supabase = await createClient()
  const provider = request.nextUrl.searchParams.get('provider') as 'google' | 'github'

  const { data, error } = await supabase.auth.signInWithOAuth({
    provider,
    options: {
      redirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/auth/callback`,
    },
  })

  if (error) {
    redirect('/login?error=Could not authenticate')
  }

  if (data.url) {
    redirect(data.url)
  }
}
```

**OAuth Button Component:**

```tsx
<a href="/auth/oauth?provider=google">
  Sign in with Google
</a>

<a href="/auth/oauth?provider=github">
  Sign in with GitHub
</a>
```

### 5. Auth Callback Handler

```typescript
// app/auth/callback/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import { NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = await createClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  // Redirect to dashboard or origin URL
  return NextResponse.redirect(`${requestUrl.origin}/dashboard`)
}
```

### 6. Logout Flow

```typescript
// app/auth/logout/actions.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function logout() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  redirect('/login')
}
```

## Session Management

### Check Authentication Status

```typescript
// Server Component
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ProtectedPage() {
  const supabase = await createClient()
  
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return <div>Welcome, {user.email}!</div>
}
```

```typescript
// Client Component
'use client'

import { createClient } from '@/lib/supabase/client'
import { useEffect, useState } from 'react'
import type { User } from '@supabase/supabase-js'

export default function ClientComponent() {
  const [user, setUser] = useState<User | null>(null)
  const supabase = createClient()

  useEffect(() => {
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)
    }

    getUser()

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null)
      }
    )

    return () => subscription.unsubscribe()
  }, [supabase])

  return <div>{user ? `Logged in as ${user.email}` : 'Not logged in'}</div>
}
```

## Security Best Practices

### 1. Row Level Security (RLS)

**Enable RLS on all tables:**

```sql
-- Enable RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Users can only see their own profile
CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

-- Users can only update their own profile
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id);
```

### 2. Password Requirements

```typescript
// Enforce strong passwords
const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character')
```

### 3. Rate Limiting

**Configure in Supabase Dashboard:**
- `Authentication > Settings > Rate Limits`
- Recommended: 10 requests per 10 seconds per IP

### 4. Email Verification

```typescript
// Require email verification before access
const { data: { user } } = await supabase.auth.getUser()

if (user && !user.email_confirmed_at) {
  redirect('/auth/verify-email')
}
```

### 5. CSRF Protection

```typescript
// Use Supabase's built-in CSRF protection via cookies
// Already handled by @supabase/ssr package
```

## Error Handling

```typescript
// Comprehensive error handling
export async function handleAuthError(error: any) {
  const errorMessages: Record<string, string> = {
    'Invalid login credentials': 'Email or password is incorrect',
    'Email not confirmed': 'Please verify your email address',
    'User already registered': 'An account with this email already exists',
    'Password should be at least 8 characters': 'Password must be at least 8 characters long',
  }

  return errorMessages[error.message] || 'An unexpected error occurred. Please try again.'
}
```

## Testing Checklist

**🚨 CRITICAL CHECKS - Must Pass All:**
- [ ] Using `@supabase/ssr` package (NOT deprecated `auth-helpers`)
- [ ] Package versions: `@supabase/supabase-js` >= 2.39.0
- [ ] All server actions in `app/actions/auth.ts` with `'use server'`
- [ ] Auth pages use `'use client'` (login, register)
- [ ] NO files with both `'use client'` AND `'use server'`
- [ ] All form labels have `block text-start` classes
- [ ] All form inputs have `dir="auto"` attribute
- [ ] All form inputs use `ps-*` `pe-*` (NOT `px-*`, `pl-*`, `pr-*`)
- [ ] Error messages displayed with proper RTL alignment
- [ ] Loading states implemented for all forms

**✅ Functional Tests:**
- [ ] Sign up with valid credentials works
- [ ] Sign up with duplicate email shows appropriate error
- [ ] Sign up with weak password shows validation error
- [ ] Email confirmation link works
- [ ] Login with verified account works
- [ ] Login with unverified account blocked (if required)
- [ ] Login with wrong password shows error
- [ ] Password reset email sent successfully
- [ ] Password reset link works and expires appropriately
- [ ] OAuth providers redirect correctly
- [ ] OAuth callback handles success/error states
- [ ] Logout clears session properly
- [ ] Protected routes redirect unauthenticated users
- [ ] Session persists across page refreshes
- [ ] Session expires after configured timeout
- [ ] Multiple simultaneous sessions handled correctly
- [ ] RLS policies prevent unauthorized data access

**🔍 Code Quality Checks:**
```bash
# Verify no deprecated packages
grep -r "@supabase/auth-helpers" package.json  # Must be 0 results

# Verify correct package
grep -r "@supabase/ssr" package.json           # Must find it

# Verify no mixed directives
grep -l "'use client'" app/actions/*.ts        # Must be 0 results
grep -l "'use server'" app/\(auth\)/**/*.tsx   # Must be 0 results

# Verify RTL classes
grep -r "px-" app/\(auth\)                     # Must be 0 results
grep -r "pl-" app/\(auth\)                     # Must be 0 results
grep -r "pr-" app/\(auth\)                     # Must be 0 results
grep -r "text-left" app/\(auth\)               # Must be 0 results
```

## Common Pitfalls to Avoid

1. **Exposing service role key** - Never use on client side
2. **Not setting redirect URLs** - Causes OAuth failures
3. **Forgetting email confirmation** - Users can't log in
4. **Not handling errors** - Poor user experience
5. **Missing RLS policies** - Security vulnerability
6. **Hardcoding URLs** - Breaks in different environments
7. **Not refreshing sessions** - Users logged out unexpectedly
8. **Weak password requirements** - Security risk
9. **No rate limiting** - Vulnerable to brute force
10. **Not testing OAuth flows** - Production failures

## Email Template Customization

See `templates/email-templates.md` for complete email template examples and customization guidelines.

## Additional Resources

- [Supabase Auth Documentation](https://supabase.com/docs/guides/auth)
- [Supabase Auth Helpers for Next.js](https://supabase.com/docs/guides/auth/auth-helpers/nextjs)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)

---

**Security Note:** Always audit your RLS policies, keep Supabase packages updated, and never expose service role keys to client-side code.