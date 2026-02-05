---
name: migrating-middleware-to-proxy
description: Teach middleware.ts to proxy.ts migration in Next.js 16. Use when migrating middleware, encountering middleware errors, or implementing request proxying.
allowed-tools: Read, Write, Edit, Glob, TodoWrite
version: 1.0.0
---

# MIGRATION: middleware.ts to proxy.ts

## Overview

Next.js 16 renames `middleware.ts` to `proxy.ts` and the `middleware` export to `proxy`. This is a **breaking change** with **security implications** (CVE-2025-29927).

## Why This Change Matters

**CVE-2025-29927**: Middleware-based authentication is fundamentally broken in Next.js. Middleware cannot reliably protect routes because:

- Middleware runs at the edge, but authentication state lives in databases/sessions
- Race conditions between middleware checks and route handlers
- Middleware can be bypassed through direct route access
- Edge runtime limitations prevent proper session verification

The rename to "proxy" clarifies that this API is for request/response manipulation, **not security**.

## Migration Steps

### 1. Rename the File

```bash
# Old location
src/middleware.ts

# New location
src/proxy.ts
```

### 2. Rename the Export

**Before (Next.js 15):**

```typescript
export function middleware(request: NextRequest) {
  return NextResponse.next();
}

export const config = {
  matcher: ['/api/:path*', '/dashboard/:path*'],
};
```

**After (Next.js 16):**

```typescript
export function proxy(request: NextRequest) {
  return NextResponse.next();
}

export const config = {
  matcher: ['/api/:path*', '/dashboard/:path*'],
};
```

### 3. Update Configuration

If using `next.config.js` or `next.config.ts`:

```typescript
const nextConfig = {
  experimental: {
  },
};
```

No configuration changes needed for proxy. The framework detects `proxy.ts` automatically.

## Security Migration

If you were using middleware for authentication, **you must migrate to route-level protection**.

### Before (Insecure)

```typescript
export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth-token');

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

### After (Secure)

**proxy.ts:**

```typescript
export function proxy(request: NextRequest) {
  const response = NextResponse.next();

  response.headers.set('x-custom-header', 'value');

  return response;
}
```

**app/dashboard/layout.tsx:**

```typescript
import { redirect } from 'next/navigation';
import { verifySession } from '@/lib/auth';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await verifySession();

  if (!session) {
    redirect('/login');
  }

  return <>{children}</>;
}
```

**Key differences:**

- Authentication logic moves to Server Components
- Session verification happens in the same runtime as data access
- No race conditions between auth check and data fetch
- Can access database/session store reliably

## Valid Use Cases for proxy.ts

Use `proxy.ts` for:

1. **Request/response header manipulation**
   ```typescript
   export function proxy(request: NextRequest) {
     const response = NextResponse.next();
     response.headers.set('x-frame-options', 'DENY');
     return response;
   }
   ```

2. **Request logging/monitoring**
   ```typescript
   export function proxy(request: NextRequest) {
     console.log(`${request.method} ${request.url}`);
     return NextResponse.next();
   }
   ```

3. **URL rewriting**
   ```typescript
   export function proxy(request: NextRequest) {
     if (request.nextUrl.pathname === '/old-path') {
       return NextResponse.rewrite(new URL('/new-path', request.url));
     }
     return NextResponse.next();
   }
   ```

4. **Geolocation routing**
   ```typescript
   export function proxy(request: NextRequest) {
     const country = request.geo?.country;
     if (country === 'US') {
       return NextResponse.rewrite(new URL('/us', request.url));
     }
     return NextResponse.next();
   }
   ```

## Do NOT Use proxy.ts For

- Authentication/authorization checks
- Session validation
- Database queries
- Complex business logic
- Rate limiting (use route handlers instead)

## Migration Checklist

- [ ] Rename `middleware.ts` to `proxy.ts`
- [ ] Rename `middleware` export to `proxy`
- [ ] Remove authentication logic from proxy
- [ ] Move authentication to Server Components/Route Handlers
- [ ] Test that routes are properly protected
- [ ] Verify edge cases (direct route access, API routes, etc.)
- [ ] Update tests that reference middleware

## Common Errors

**Error: "middleware is not exported"**

You forgot to rename the export from `middleware` to `proxy`.

**Error: "proxy is not a function"**

Ensure you're exporting a function named `proxy`, not a default export.

**Error: "Cannot access database in proxy"**

Proxy runs at the edge runtime. Move database access to route handlers or Server Components.

## Additional Resources

- CVE-2025-29927: Next.js Middleware Authentication Vulnerability
- Next.js 16 Migration Guide: Proxy API
- Next.js Security Best Practices: Route-Level Protection
