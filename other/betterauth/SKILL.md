---
name: betterauth
description: BetterAuth integration patterns — setup, session management, OAuth providers, middleware protection, and security best practices for authentication in TypeScript/Next.js applications.
license: MIT
metadata:
  author: Satcomx00-x00
  version: 1.0.0
---

# betterauth

BetterAuth integration patterns — setup, session management, OAuth providers, middleware protection, and security best practices for authentication in TypeScript/Next.js applications.

## Instructions

Apply these practices when integrating BetterAuth into your application:

### Setup & Configuration

Create a single authoritative auth instance and export typed helpers from it:

```ts
// lib/auth.ts
import { betterAuth } from 'better-auth';
import { prismaAdapter } from 'better-auth/adapters/prisma';
import { db } from './db';

export const auth = betterAuth({
  database: prismaAdapter(db, { provider: 'postgresql' }),
  emailAndPassword: { enabled: true },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7,        // 7 days
    updateAge: 60 * 60 * 24,             // refresh session if older than 1 day
    cookieCache: { enabled: true, maxAge: 60 * 5 }, // 5-minute client cache
  },
  trustedOrigins: [process.env.NEXT_PUBLIC_APP_URL!],
});

// Export typed client helpers
export type Session = typeof auth.$Infer.Session;
```

### API Route Handler

Mount the BetterAuth catch-all handler at `app/api/auth/[...all]/route.ts`:

```ts
// app/api/auth/[...all]/route.ts
import { auth } from '@/lib/auth';
import { toNextJsHandler } from 'better-auth/next-js';

export const { GET, POST } = toNextJsHandler(auth);
```

### Client-Side Auth Client

Create a single client instance to use across Client Components:

```ts
// lib/auth-client.ts
import { createAuthClient } from 'better-auth/react';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL!,
});

export const { signIn, signOut, signUp, useSession } = authClient;
```

### Session Access

**Server Component:**
```ts
import { auth } from '@/lib/auth';
import { headers } from 'next/headers';

export async function getServerSession() {
  const session = await auth.api.getSession({ headers: await headers() });
  return session;
}
```

**Client Component:**
```tsx
'use client';
import { useSession } from '@/lib/auth-client';

export function UserAvatar() {
  const { data: session, isPending } = useSession();
  if (isPending) return <Skeleton />;
  if (!session) return null;
  return <img src={session.user.image ?? ''} alt={session.user.name} />;
}
```

### Route Protection

Protect routes at the middleware layer to avoid unnecessary page renders for unauthenticated users:

```ts
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';

const PROTECTED = ['/dashboard', '/settings', '/api/protected'];

export async function middleware(req: NextRequest) {
  const isProtected = PROTECTED.some(path => req.nextUrl.pathname.startsWith(path));
  if (!isProtected) return NextResponse.next();

  const session = await auth.api.getSession({ headers: req.headers });
  if (!session) {
    const loginUrl = new URL('/login', req.url);
    loginUrl.searchParams.set('callbackUrl', req.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = { matcher: ['/dashboard/:path*', '/settings/:path*', '/api/protected/:path*'] };
```

### Role-Based Access Control (RBAC)

Use BetterAuth's `access` plugin or store roles in the user record and enforce them in Server Components / Server Actions:

```ts
// Utility to enforce roles server-side
import { redirect } from 'next/navigation';
import { getServerSession } from '@/lib/auth';

export async function requireRole(role: string) {
  const session = await getServerSession();
  if (!session) redirect('/login');
  if (session.user.role !== role) redirect('/403');
  return session;
}

// Usage in a Server Component
export default async function AdminPage() {
  const session = await requireRole('admin');
  return <AdminDashboard user={session.user} />;
}
```

### OAuth Providers

- Register the callback URL with each provider: `{APP_URL}/api/auth/callback/{provider}`
- Store `clientId` and `clientSecret` in environment variables — never hardcode them
- Request only the OAuth scopes you actually need (principle of least privilege)
- Handle provider errors gracefully — OAuth flows can fail; show a friendly error page

### Security Best Practices

- **CSRF**: BetterAuth uses `SameSite=Lax` cookies by default; do not downgrade this
- **HTTPS only**: set `secure: true` on cookies in production — enforce via `NODE_ENV` check
- **Secret rotation**: use a strong, random `secret` (≥ 32 chars); rotate it without downtime using a secondary secret during transition
- **Email verification**: enable `requireEmailVerification` before allowing access to sensitive resources
- **Rate limiting**: apply rate limiting to auth endpoints (`/api/auth/sign-in`, `/api/auth/sign-up`) to prevent brute-force and credential stuffing
- **Audit log**: log successful sign-ins and sign-outs with IP, user agent, and timestamp

```ts
// lib/auth.ts — production hardening additions
export const auth = betterAuth({
  // ...
  advanced: {
    useSecureCookies: process.env.NODE_ENV === 'production',
    defaultCookieAttributes: {
      sameSite: 'lax',
      httpOnly: true,
    },
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    minPasswordLength: 12,
  },
  hooks: {
    after: [
      {
        matcher: ctx => ctx.path === '/sign-in/email',
        handler: async ctx => {
          // Audit log
          await auditLog.create({ action: 'sign_in', userId: ctx.context.session?.userId, ip: ctx.request.headers.get('x-forwarded-for') });
        },
      },
    ],
  },
});
```

### Database Schema

BetterAuth requires specific tables. Generate them with the CLI:

```bash
npx better-auth generate   # generates migration SQL
npx better-auth migrate    # applies the migration (Prisma / Drizzle adapters auto-migrate)
```

Core tables created: `user`, `session`, `account`, `verification`.

## Examples

```tsx
// Sign-in form (Client Component)
'use client';
import { signIn } from '@/lib/auth-client';
import { useState } from 'react';

export function SignInForm() {
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const { error } = await signIn.email({
      email: form.get('email') as string,
      password: form.get('password') as string,
      callbackURL: '/dashboard',
    });
    if (error) setError(error.message);
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" required />
      <input name="password" type="password" required />
      {error && <p role="alert">{error}</p>}
      <button type="submit">Sign in</button>
      <button type="button" onClick={() => signIn.social({ provider: 'github', callbackURL: '/dashboard' })}>
        Sign in with GitHub
      </button>
    </form>
  );
}
```

## References

- [BetterAuth Documentation](https://www.better-auth.com/docs)
- [BetterAuth Next.js Guide](https://www.better-auth.com/docs/integrations/next-js)
- [BetterAuth GitHub](https://github.com/better-auth/better-auth)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
