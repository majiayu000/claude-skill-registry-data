---
name: backend-auth-js
description: Authentication library for Next.js applications (NextAuth.js v5). Use when building Next.js 14+ apps that need OAuth providers (GitHub, Google, etc.), credentials login, or session management. Provides adapters for Prisma, Drizzle, and other databases. Choose Auth.js over Passport.js for Next.js App Router projects.
allowed-tools: Read, Edit, Write, Bash (*)
---

# Auth.js (NextAuth.js v5)

## Overview

Auth.js (NextAuth.js v5) is the standard authentication solution for Next.js. It handles OAuth, credentials, JWT/database sessions, and integrates natively with App Router.

**Version**: next-auth@5.0.0-beta (Auth.js v5)  
**Requirements**: Next.js 14.0+

**Key Benefit**: Minimal config for OAuth providers, built-in CSRF protection, serverless-ready.

## When to Use This Skill

✅ **Use Auth.js when:**
- Building Next.js App Router applications
- Need OAuth providers (GitHub, Google, Discord, etc.)
- Want database sessions with Prisma adapter
- Building serverless/edge-compatible auth
- Need quick setup with minimal boilerplate

❌ **Use Passport.js instead when:**
- Building Express.js APIs
- Need 500+ provider strategies
- Require custom auth flows
- Not using Next.js

---

## Quick Start

### Installation

```bash
npm install next-auth@beta @auth/prisma-adapter
```

### Basic Configuration

```typescript
// auth.ts (root level)
import NextAuth from 'next-auth';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { prisma } from '@/lib/prisma';
import { verify } from 'argon2';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: 'jwt' },
  providers: [
    GitHub,
    Google,
    Credentials({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const user = await prisma.user.findUnique({
          where: { email: credentials.email as string },
        });
        if (!user?.password) return null;
        
        const valid = await verify(user.password, credentials.password as string);
        if (!valid) return null;
        
        return { id: user.id, email: user.email, name: user.name, role: user.role };
      },
    }),
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    session({ session, token }) {
      session.user.id = token.id as string;
      session.user.role = token.role as string;
      return session;
    },
  },
});
```

### Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from '@/auth';
export const { GET, POST } = handlers;
```

### Environment Variables

```env
AUTH_SECRET=your-secret-key-here  # openssl rand -base64 32
AUTH_GITHUB_ID=xxx
AUTH_GITHUB_SECRET=xxx
AUTH_GOOGLE_ID=xxx
AUTH_GOOGLE_SECRET=xxx
```

---

## Type Augmentation

**Extend session/JWT types for custom fields:**

```typescript
// types/next-auth.d.ts
import { DefaultSession } from 'next-auth';

declare module 'next-auth' {
  interface Session {
    user: { 
      id: string; 
      role: string;
    } & DefaultSession['user'];
  }
  interface User {
    role: string;
  }
}

declare module 'next-auth/jwt' {
  interface JWT {
    id: string;
    role: string;
  }
}
```

---

## Prisma Schema for Auth.js

```prisma
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  password      String?   // For credentials provider
  role          String    @default("user")
  accounts      Account[]
  sessions      Session[]
}

model Account {
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@id([provider, providerAccountId])
}

model Session {
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model VerificationToken {
  identifier String
  token      String
  expires    DateTime

  @@unique([identifier, token])
}
```

---

## Usage Patterns

### Server Component (App Router)

```typescript
// app/dashboard/page.tsx
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth();
  
  if (!session) {
    redirect('/login');
  }
  
  return <div>Welcome, {session.user.name}</div>;
}
```

### Client Component

```typescript
'use client';
import { useSession } from 'next-auth/react';

export function UserButton() {
  const { data: session, status } = useSession();
  
  if (status === 'loading') return <Skeleton />;
  if (!session) return <SignInButton />;
  
  return <span>{session.user.name}</span>;
}
```

### Middleware Protection

```typescript
// middleware.ts
import { auth } from '@/auth';

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isOnDashboard = req.nextUrl.pathname.startsWith('/dashboard');
  
  if (isOnDashboard && !isLoggedIn) {
    return Response.redirect(new URL('/login', req.nextUrl));
  }
});

export const config = {
  matcher: ['/dashboard/:path*', '/settings/:path*'],
};
```

### Sign In/Out Actions

```typescript
// app/login/page.tsx
import { signIn, signOut } from '@/auth';

export default function LoginPage() {
  return (
    <div>
      <form action={async () => {
        'use server';
        await signIn('github');
      }}>
        <button>Sign in with GitHub</button>
      </form>
      
      <form action={async () => {
        'use server';
        await signIn('credentials', { email, password });
      }}>
        {/* credentials form */}
      </form>
    </div>
  );
}
```

---

## Integration with tRPC

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { auth } from '@/auth';

export const createContext = async () => {
  const session = await auth();
  return { session, prisma };
};

const t = initTRPC.context<Context>().create();

const isAuthed = t.middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next({ ctx: { user: ctx.session.user } });
});

export const protectedProcedure = t.procedure.use(isAuthed);

// Role-based
const hasRole = (role: string) => t.middleware(({ ctx, next }) => {
  if (ctx.session?.user?.role !== role) {
    throw new TRPCError({ code: 'FORBIDDEN' });
  }
  return next();
});

export const adminProcedure = protectedProcedure.use(hasRole('admin'));
```

---

## Session Strategies

| Strategy | Storage | Use Case |
|----------|---------|----------|
| `jwt` | Cookie | Serverless, Edge, stateless |
| `database` | Prisma/DB | Need to revoke sessions |

```typescript
// JWT (default, recommended for most cases)
session: { strategy: 'jwt' }

// Database sessions
session: { strategy: 'database' }
```

---

## Rules

### Do ✅

- Use `AUTH_SECRET` environment variable (auto-detected)
- Extend types in `next-auth.d.ts` for custom fields
- Use JWT strategy for serverless deployments
- Hash passwords with argon2 or bcrypt
- Use middleware for route protection

### Avoid ❌

- Storing sensitive data in JWT (it's readable)
- Using credentials provider without password hashing
- Skipping CSRF protection (enabled by default)
- Mixing v4 and v5 patterns (breaking changes)

---

## Troubleshooting

```yaml
"Session is null in server component":
  → Ensure auth.ts exports are correct
  → Check AUTH_SECRET is set
  → Verify cookies are being sent

"OAuth callback error":
  → Check provider credentials in env
  → Verify callback URL in provider dashboard
  → Match AUTH_URL with actual URL

"Type errors on session.user":
  → Create types/next-auth.d.ts
  → Extend Session and JWT interfaces
  → Restart TypeScript server

"Credentials provider not working":
  → Must use JWT strategy with credentials
  → Check authorize function returns user object
  → Verify password comparison
```

---

## File Structure

```
app/
├── api/auth/[...nextauth]/route.ts  # Auth handlers
├── login/page.tsx                    # Login page
└── dashboard/page.tsx                # Protected page

auth.ts                               # Auth configuration
middleware.ts                         # Route protection
types/next-auth.d.ts                  # Type extensions
```

## References

- https://authjs.dev — Official documentation
- https://authjs.dev/getting-started/providers — Provider list
- https://authjs.dev/getting-started/adapters — Database adapters
