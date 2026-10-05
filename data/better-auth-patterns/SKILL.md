---
name: Better Auth Patterns
description: >-
  Auto-enforce Better Auth implementation patterns. Activates when setting up
  authentication, configuring providers, creating auth forms, or implementing
  session management in React applications.
version: 1.0.0
---

# Better Auth Patterns

This skill enforces Better Auth best practices for authentication in React applications.

## Server Configuration

### Basic Setup
```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth'
import { prismaAdapter } from 'better-auth/adapters/prisma'
import { prisma } from './prisma'

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: 'postgresql',
  }),

  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },

  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // Extend daily
  },
})

export type Auth = typeof auth
```

### Social Providers
```typescript
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  // ... database config

  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      scopes: ['email', 'profile'],
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
      scopes: ['user:email'],
    },
    discord: {
      clientId: process.env.DISCORD_CLIENT_ID!,
      clientSecret: process.env.DISCORD_CLIENT_SECRET!,
    },
  },
})
```

### Two-Factor Authentication
```typescript
import { twoFactor } from 'better-auth/plugins/two-factor'

export const auth = betterAuth({
  // ... base config

  plugins: [
    twoFactor({
      issuer: 'MyApp',
      totpWindow: 1,
      backupCodes: {
        enabled: true,
        count: 10,
      },
    }),
  ],
})
```

### Passkeys (WebAuthn)
```typescript
import { passkey } from 'better-auth/plugins/passkey'

export const auth = betterAuth({
  // ... base config

  plugins: [
    passkey({
      rpId: 'myapp.com',
      rpName: 'My App',
      origin: 'https://myapp.com',
      attestation: 'none',
      authenticatorSelection: {
        authenticatorAttachment: 'platform',
        userVerification: 'preferred',
        residentKey: 'preferred',
      },
    }),
  ],
})
```

## Client Setup

### Create Auth Client
```typescript
// auth/client.ts
import { createAuthClient } from 'better-auth/react'
import type { Auth } from '@/lib/auth'

export const authClient = createAuthClient<Auth>({
  baseURL: import.meta.env.VITE_API_URL,
  // Optional: Custom fetch for headers
  fetch: async (url, options) => {
    return fetch(url, {
      ...options,
      credentials: 'include',
    })
  },
})

// Export typed methods
export const {
  signIn,
  signUp,
  signOut,
  useSession,
  getSession,
  resetPassword,
  verifyEmail,
  // Social
  signInWithGoogle,
  signInWithGithub,
  // 2FA
  enable2FA,
  disable2FA,
  verify2FA,
  // Passkeys
  registerPasskey,
  signInWithPasskey,
} = authClient
```

### Session Hook
```typescript
// auth/hooks.ts
import { useSession } from './client'

export function useAuth() {
  const { data: session, isPending, error } = useSession()

  return {
    user: session?.user ?? null,
    session: session?.session ?? null,
    isAuthenticated: !!session?.user,
    isLoading: isPending,
    error,
  }
}

export function useRequireAuth() {
  const auth = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!auth.isLoading && !auth.isAuthenticated) {
      navigate({ to: '/login' })
    }
  }, [auth.isLoading, auth.isAuthenticated])

  return auth
}
```

## Auth Components

### Login Form
```typescript
import { useForm } from '@tanstack/react-form'
import { zodValidator } from '@tanstack/zod-form-adapter'
import { signIn } from '@/auth/client'
import { z } from 'zod'

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1, 'Password is required'),
})

export function LoginForm() {
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()

  const form = useForm({
    defaultValues: { email: '', password: '' },
    validatorAdapter: zodValidator(),
    validators: { onChange: loginSchema },
    onSubmit: async ({ value }) => {
      setError(null)
      const result = await signIn.email(value)

      if (result.error) {
        setError(result.error.message)
        return
      }

      navigate({ to: '/dashboard' })
    },
  })

  return (
    <form onSubmit={(e) => { e.preventDefault(); form.handleSubmit() }}>
      {error && <div className="error">{error}</div>}

      <form.Field
        name="email"
        children={(field) => (/* email input */)}
      />

      <form.Field
        name="password"
        children={(field) => (/* password input */)}
      />

      <form.Subscribe
        selector={(state) => state.isSubmitting}
        children={(isSubmitting) => (
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Signing in...' : 'Sign In'}
          </button>
        )}
      />
    </form>
  )
}
```

### Social Login Buttons
```typescript
import { signInWithGoogle, signInWithGithub } from '@/auth/client'

export function SocialLoginButtons() {
  const handleGoogleLogin = async () => {
    await signInWithGoogle({
      callbackURL: '/dashboard',
    })
  }

  const handleGithubLogin = async () => {
    await signInWithGithub({
      callbackURL: '/dashboard',
    })
  }

  return (
    <div className="flex flex-col gap-2">
      <button onClick={handleGoogleLogin} className="btn-social">
        <GoogleIcon /> Continue with Google
      </button>
      <button onClick={handleGithubLogin} className="btn-social">
        <GithubIcon /> Continue with GitHub
      </button>
    </div>
  )
}
```

### 2FA Setup
```typescript
import { enable2FA, verify2FA } from '@/auth/client'
import { useState } from 'react'

export function TwoFactorSetup() {
  const [qrCode, setQrCode] = useState<string | null>(null)
  const [secret, setSecret] = useState<string | null>(null)
  const [code, setCode] = useState('')
  const [backupCodes, setBackupCodes] = useState<string[]>([])

  const handleEnable = async () => {
    const result = await enable2FA()
    if (result.data) {
      setQrCode(result.data.qrCode)
      setSecret(result.data.secret)
    }
  }

  const handleVerify = async () => {
    const result = await verify2FA({ code })
    if (result.data) {
      setBackupCodes(result.data.backupCodes)
    }
  }

  if (backupCodes.length > 0) {
    return (
      <div>
        <h3>Save your backup codes</h3>
        <ul>
          {backupCodes.map((code, i) => (
            <li key={i}>{code}</li>
          ))}
        </ul>
      </div>
    )
  }

  if (qrCode) {
    return (
      <div>
        <img src={qrCode} alt="2FA QR Code" />
        <p>Secret: {secret}</p>
        <input
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter 6-digit code"
        />
        <button onClick={handleVerify}>Verify</button>
      </div>
    )
  }

  return (
    <button onClick={handleEnable}>Enable 2FA</button>
  )
}
```

### Passkey Registration
```typescript
import { registerPasskey, signInWithPasskey } from '@/auth/client'

export function PasskeyManager() {
  const [error, setError] = useState<string | null>(null)

  const handleRegister = async () => {
    setError(null)
    const result = await registerPasskey({
      name: 'My Device',
    })

    if (result.error) {
      setError(result.error.message)
    }
  }

  const handleSignIn = async () => {
    setError(null)
    const result = await signInWithPasskey()

    if (result.error) {
      setError(result.error.message)
    }
  }

  return (
    <div>
      {error && <div className="error">{error}</div>}
      <button onClick={handleRegister}>Register Passkey</button>
      <button onClick={handleSignIn}>Sign in with Passkey</button>
    </div>
  )
}
```

## Router Integration

### Root Route with Session
```typescript
// routes/__root.tsx
import { createRootRouteWithContext } from '@tanstack/react-router'
import { getSession } from '@/auth/client'

export const Route = createRootRouteWithContext<RouterContext>()({
  beforeLoad: async () => {
    const session = await getSession()
    return { session: session?.data ?? null }
  },
})
```

### Protected Route Layout
```typescript
// routes/_auth.tsx
import { createFileRoute, redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/_auth')({
  beforeLoad: async ({ context, location }) => {
    if (!context.session) {
      throw redirect({
        to: '/login',
        search: { redirect: location.pathname },
      })
    }
  },
})
```

### Guest-Only Routes
```typescript
// routes/_guest.tsx
import { createFileRoute, redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/_guest')({
  beforeLoad: async ({ context }) => {
    if (context.session) {
      throw redirect({ to: '/dashboard' })
    }
  },
})
```

## Official Plugins

Better Auth includes first-class plugins for enterprise and security features:

### 1. Two-Factor Authentication (2FA / TOTP)
```typescript
// lib/auth.ts
import { betterAuth } from 'better-auth'
import { twoFactor } from 'better-auth/plugins'

export const auth = betterAuth({
  // ... database
  plugins: [
    twoFactor({
      issuer: 'MyApp',
    }),
  ],
})

// Client setup: import { twoFactorClient } from 'better-auth/client/plugins'
// createAuthClient({ plugins: [twoFactorClient()] })
```

### 2. Passkeys / WebAuthn
```typescript
import { betterAuth } from 'better-auth'
import { passkey } from 'better-auth/plugins'

export const auth = betterAuth({
  plugins: [
    passkey({
      rpID: process.env.RP_ID || 'localhost',
      rpName: 'MyApp',
      origin: process.env.BETTER_AUTH_URL || 'http://localhost:3000',
    }),
  ],
})
```

### 3. Organizations / Multi-Tenancy (B2B SaaS)
```typescript
import { betterAuth } from 'better-auth'
import { organization } from 'better-auth/plugins'

export const auth = betterAuth({
  plugins: [
    organization({
      allowUserToCreateOrganization: true,
      roles: ['owner', 'admin', 'member'],
    }),
  ],
})
```

### 4. API Keys & Admin Panel
```typescript
import { betterAuth } from 'better-auth'
import { apiKey, admin } from 'better-auth/plugins'

export const auth = betterAuth({
  plugins: [
    apiKey(),
    admin({
      defaultRole: 'user',
      adminRole: 'admin',
    }),
  ],
})
```

## Conventions

1. **Server config in lib/** - Keep auth config at `lib/auth.ts`
2. **Client in auth/** - Export typed client from `auth/client.ts`
3. **Route protection** - Use pathless layouts (`_auth.tsx`)
4. **Session in context** - Load session in `__root.tsx`
5. **Error handling** - Always check `result.error`
6. **Type safety** - Use `Auth` type from server config

## Anti-Patterns

```typescript
// ❌ WRONG: Untyped client
const authClient = createAuthClient({})

// ✅ CORRECT: Typed client
const authClient = createAuthClient<Auth>({})

// ❌ WRONG: No error handling
const result = await signIn.email(data)
navigate('/dashboard')

// ✅ CORRECT: Check for errors
const result = await signIn.email(data)
if (result.error) {
  setError(result.error.message)
  return
}
navigate('/dashboard')

// ❌ WRONG: Client-side session check only
if (localStorage.getItem('session')) { ... }

// ✅ CORRECT: Server-validated session
const { data: session } = useSession()
if (session) { ... }
```
