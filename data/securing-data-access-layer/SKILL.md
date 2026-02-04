---
name: securing-data-access-layer
description: Teach Data Access Layer pattern to prevent CVE-2025-29927 middleware authentication bypass. Use when implementing authentication, authorization, protecting routes, or working with server actions that need auth.
allowed-tools: Read, Write, Edit, Glob, Grep, TodoWrite
version: 1.0.0
---

# Data Access Layer Pattern for Next.js 16 Authentication Security

## Critical Security Issue: CVE-2025-29927

Next.js 16 has a **critical authentication bypass vulnerability** in middleware. Middleware `NextResponse.redirect()` and `NextResponse.rewrite()` **DO NOT terminate execution**, allowing unauthorized access to protected resources.

### The Problem

```typescript
export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');

  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
}
```

This middleware appears to protect routes, but **code after the return statement still executes**. Attackers can bypass authentication by manipulating requests.

### Why This Matters

- Middleware-only authentication is **completely broken** in Next.js 16
- Protected routes, server actions, and API routes are all vulnerable
- Data breaches, unauthorized access, and privilege escalation are possible

## The Solution: Data Access Layer (DAL)

Implement a **multi-layer security strategy** with authentication verification at every access point.

### Core Pattern: verifySession()

For comprehensive input validation patterns to use alongside authentication, use the sanitizing-user-inputs skill from the typescript plugin.

Create a centralized Data Access Layer that verifies authentication before ANY data access:

```typescript
import 'server-only';
import { cookies } from 'next/headers';
import { decrypt } from '@/lib/session';
import { cache } from 'react';

export const verifySession = cache(async () => {
  const cookie = (await cookies()).get('session')?.value;
  const session = await decrypt(cookie);

  if (!session?.userId) {
    throw new Error('Unauthorized');
  }

  return { isAuth: true, userId: session.userId };
});
```

**Key features:**

- Uses `cache()` for request-level memoization (single verification per request)
- Throws error if unauthorized (fails fast)
- Returns typed session data for use in application logic
- Server-only code that cannot leak to client

### Three-Layer Security Architecture

1. **Route Protection** - Basic UX (redirect unauthorized users)
2. **Data Access Layer** - Core security (verify before data access)
3. **Server Actions** - Action-level verification (verify before mutations)

#### Layer 1: Route Protection (UX Only)

```typescript
export default async function DashboardLayout({ children }) {
  const session = await verifySession();

  if (!session.isAuth) {
    redirect('/login');
  }

  return <>{children}</>;
}
```

Verify session in layouts and pages to redirect unauthorized users. This is **UX only**, not security.

#### Layer 2: Data Access Layer (Security)

```typescript
export async function getUser() {
  const session = await verifySession();

  const data = await db.query.users.findMany({
    where: eq(users.id, session.userId),
  });

  return data;
}
```

**Always verify session before database queries.** This is your actual security boundary.

For type-safe database access patterns, use the ensuring-query-type-safety skill from prisma-6 to prevent type errors and runtime failures in your data access functions.

#### Layer 3: Server Actions (Mutation Security)

```typescript
'use server';

export async function updateProfile(formData: FormData) {
  const session = await verifySession();

  const name = formData.get('name');

  await db.update(users).set({ name }).where(eq(users.id, session.userId));

  revalidatePath('/profile');
}
```

Verify session at the start of **every server action** that modifies data.

## Implementation Checklist

When working with authenticated features:

- [ ] Create `lib/dal.ts` with `verifySession()` function
- [ ] Use `verifySession()` in ALL data fetching functions
- [ ] Use `verifySession()` in ALL server actions
- [ ] Add route protection to layouts/pages for UX (optional but recommended)
- [ ] Never rely on middleware alone for authentication
- [ ] Import 'server-only' in DAL to prevent client leaks
- [ ] Use React `cache()` for request-level memoization

## Common Patterns

### Authorization (Role-Based Access)

```typescript
export async function verifyAdmin() {
  const session = await verifySession();

  const user = await db.query.users.findFirst({
    where: eq(users.id, session.userId),
  });

  if (user?.role !== 'admin') {
    throw new Error('Forbidden');
  }

  return { userId: session.userId, role: user.role };
}
```

### Resource Ownership

```typescript
export async function getPost(postId: string) {
  const session = await verifySession();

  const post = await db.query.posts.findFirst({
    where: eq(posts.id, postId),
  });

  if (post.authorId !== session.userId) {
    throw new Error('Forbidden');
  }

  return post;
}
```

### Multi-Step Atomic Operations

If setting up PrismaClient with singleton pattern in Next.js, use the creating-client-singletons skill from prisma-6 for proper instantiation preventing connection pool exhaustion.

If implementing authenticated operations requiring atomicity (e.g., creating a post with tags, transferring ownership), use the using-interactive-transactions skill from prisma-6 for database-specific transaction patterns.

### Public + Private Data

```typescript
export async function getProfile(username: string) {
  const session = await verifySession().catch(() => null);

  const profile = await db.query.users.findFirst({
    where: eq(users.username, username),
    columns: {
      username: true,
      bio: true,
      email: session ? true : false,
    },
  });

  return profile;
}
```

## Key Takeaways

1. **CVE-2025-29927 makes middleware authentication unsafe** - redirects don't stop execution
2. **Data Access Layer is mandatory** - verify session before every data access
3. **Multi-layer security** - route protection (UX) + DAL (security) + server actions (mutations)
4. **verifySession() everywhere** - make it a habit to call this first
5. **Use React cache()** - prevents multiple verification calls per request

## References

See the `references/` directory for:

- `dal-example.md` - Complete working example with full implementation
- `cve-2025-29927.md` - Detailed vulnerability analysis and exploitation examples

## When to Use This Skill

Apply this pattern when:

- Implementing authentication in Next.js 16 applications
- Protecting routes that require user login
- Creating server actions that modify user data
- Building authorization systems (roles, permissions)
- Fetching user-specific data from databases
- Any time you see middleware being used for authentication
- Reviewing code for security vulnerabilities

This is the **most important security pattern** in Next.js 16. Use it in every authenticated application.
