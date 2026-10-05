---
name: rbac
description: Role-based access control — roles, permissions, policies, middleware guards, database schema, and authorization patterns for web applications
layer: utility
category: security
triggers:
  - "rbac"
  - "role based access"
  - "permissions"
  - "authorization"
  - "access control"
  - "admin role"
  - "user roles"
  - "middleware guard"
  - "permission check"
inputs:
  - Application role hierarchy
  - Resource types and actions
  - Current auth system (session, JWT, etc.)
  - Framework (Next.js, Express, etc.)
outputs:
  - RBAC database schema
  - Permission checking middleware/guards
  - Role assignment API
  - UI permission gating components
  - Policy evaluation engine
linksTo:
  - authentication
  - better-auth
  - api-designer
  - database-indexing
linkedFrom:
  - owasp
  - security-scanner
preferredNextSkills:
  - authentication
  - owasp
fallbackSkills:
  - api-designer
riskLevel: high
memoryReadPolicy: always
memoryWritePolicy: selective
sideEffects:
  - Creates database tables and relationships
  - Adds middleware to request pipeline
  - May block user access if misconfigured
---

# RBAC (Role-Based Access Control) Skill

## Purpose

Authorization determines what authenticated users can do. RBAC maps users to roles, roles to permissions, and permissions to resource actions. This skill covers schema design, middleware implementation, UI gating, and common authorization patterns.

## Key Concepts

### RBAC Model

```
User  ──M:N──  Role  ──M:N──  Permission
                                   │
                              Action + Resource
                              ("create:post", "delete:user")
```

### Permission Granularity Levels

| Level | Example | Complexity | Use When |
|-------|---------|------------|----------|
| **Role-only** | `isAdmin` | Low | Small apps, 2-3 roles |
| **Role + Permission** | `admin` has `users:delete` | Medium | Most apps |
| **ABAC (Attribute-based)** | `can delete IF owner OR admin` | High | Multi-tenant, fine-grained |
| **ReBAC (Relationship-based)** | `can edit IF member of org` | High | Google Docs-style sharing |

### Decision Framework

```
How many roles? (2-5)
  └─ Role-only checks are sufficient

Do different roles need different actions on same resource?
  └─ Role + Permission model

Do permissions depend on data relationships (ownership, team membership)?
  └─ ABAC or ReBAC (consider Oso, Cerbos, or OpenFGA)
```

## Workflow

### Step 1: Database Schema

```sql
-- Core RBAC tables
CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(50) UNIQUE NOT NULL,      -- 'admin', 'editor', 'viewer'
  description TEXT,
  is_system BOOLEAN DEFAULT false,        -- Prevent deletion of built-in roles
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE permissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  action VARCHAR(50) NOT NULL,            -- 'create', 'read', 'update', 'delete'
  resource VARCHAR(100) NOT NULL,         -- 'post', 'user', 'billing'
  description TEXT,
  UNIQUE (action, resource)
);

CREATE TABLE role_permissions (
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
  PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
  assigned_at TIMESTAMPTZ DEFAULT now(),
  assigned_by UUID REFERENCES users(id),
  PRIMARY KEY (user_id, role_id)
);

-- Indexes for fast permission lookups
CREATE INDEX idx_user_roles_user ON user_roles (user_id);
CREATE INDEX idx_role_permissions_role ON role_permissions (role_id);

-- Seed default roles
INSERT INTO roles (name, description, is_system) VALUES
  ('admin', 'Full system access', true),
  ('editor', 'Can create and edit content', true),
  ('viewer', 'Read-only access', true);

-- Seed permissions
INSERT INTO permissions (action, resource) VALUES
  ('create', 'post'), ('read', 'post'), ('update', 'post'), ('delete', 'post'),
  ('create', 'user'), ('read', 'user'), ('update', 'user'), ('delete', 'user'),
  ('read', 'analytics'), ('manage', 'billing'), ('manage', 'settings');

-- Assign permissions to roles
-- Admin: everything
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r CROSS JOIN permissions p WHERE r.name = 'admin';

-- Editor: CRUD on posts, read users
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.name = 'editor'
  AND ((p.resource = 'post') OR (p.action = 'read' AND p.resource = 'user'));

-- Viewer: read only
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id FROM roles r, permissions p
WHERE r.name = 'viewer' AND p.action = 'read';
```

### Step 2: Permission Check Function

```typescript
// lib/auth/permissions.ts
import { db } from '@/lib/db';

export type Permission = `${string}:${string}`; // "action:resource"

/**
 * Check if a user has a specific permission.
 * Results should be cached per request (not globally — permissions can change).
 */
export async function hasPermission(
  userId: string,
  permission: Permission
): Promise<boolean> {
  const [action, resource] = permission.split(':');

  const result = await db.$queryRaw<{ count: bigint }[]>`
    SELECT COUNT(*) as count
    FROM user_roles ur
    JOIN role_permissions rp ON rp.role_id = ur.role_id
    JOIN permissions p ON p.id = rp.permission_id
    WHERE ur.user_id = ${userId}::uuid
      AND p.action = ${action}
      AND p.resource = ${resource}
  `;

  return Number(result[0].count) > 0;
}

/**
 * Get all permissions for a user (for client-side gating).
 */
export async function getUserPermissions(userId: string): Promise<Permission[]> {
  const results = await db.$queryRaw<{ action: string; resource: string }[]>`
    SELECT DISTINCT p.action, p.resource
    FROM user_roles ur
    JOIN role_permissions rp ON rp.role_id = ur.role_id
    JOIN permissions p ON p.id = rp.permission_id
    WHERE ur.user_id = ${userId}::uuid
  `;

  return results.map((r) => `${r.action}:${r.resource}` as Permission);
}

/**
 * Get user's roles.
 */
export async function getUserRoles(userId: string): Promise<string[]> {
  const results = await db.$queryRaw<{ name: string }[]>`
    SELECT r.name
    FROM user_roles ur
    JOIN roles r ON r.id = ur.role_id
    WHERE ur.user_id = ${userId}::uuid
  `;

  return results.map((r) => r.name);
}
```

### Step 3: Next.js Middleware Guard

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth/session';

// Define protected routes and required permissions
const routePermissions: Record<string, Permission> = {
  '/admin': 'read:admin',
  '/admin/users': 'read:user',
  '/admin/settings': 'manage:settings',
  '/dashboard/posts/new': 'create:post',
};

export async function middleware(request: NextRequest) {
  const session = await getSession(request);

  if (!session?.user) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Check route-level permissions
  const pathname = request.nextUrl.pathname;
  for (const [route, permission] of Object.entries(routePermissions)) {
    if (pathname.startsWith(route)) {
      const allowed = await hasPermission(session.user.id, permission);
      if (!allowed) {
        return NextResponse.redirect(new URL('/unauthorized', request.url));
      }
      break;
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*', '/dashboard/:path*'],
};
```

### Step 4: API Route Guard

```typescript
// lib/auth/guards.ts
import { NextRequest, NextResponse } from 'next/server';

type HandlerFn = (request: NextRequest, context: any) => Promise<NextResponse>;

export function requirePermission(permission: Permission) {
  return function guard(handler: HandlerFn): HandlerFn {
    return async (request, context) => {
      const session = await getSession(request);

      if (!session?.user) {
        return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
      }

      const allowed = await hasPermission(session.user.id, permission);
      if (!allowed) {
        return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
      }

      return handler(request, context);
    };
  };
}

// Usage in API route
// app/api/admin/users/route.ts
export const DELETE = requirePermission('delete:user')(
  async (request: NextRequest) => {
    const { userId } = await request.json();
    await db.user.delete({ where: { id: userId } });
    return NextResponse.json({ success: true });
  }
);
```

### Step 5: React Permission Gate Component

```tsx
// components/permission-gate.tsx
'use client';

import { createContext, useContext, type ReactNode } from 'react';
import type { Permission } from '@/lib/auth/permissions';

interface AuthContext {
  permissions: Permission[];
  roles: string[];
}

const AuthContext = createContext<AuthContext>({ permissions: [], roles: [] });

export function AuthProvider({
  children,
  permissions,
  roles,
}: {
  children: ReactNode;
  permissions: Permission[];
  roles: string[];
}) {
  return (
    <AuthContext.Provider value={{ permissions, roles }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

export function useHasPermission(permission: Permission): boolean {
  const { permissions } = useAuth();
  return permissions.includes(permission);
}

export function useHasRole(role: string): boolean {
  const { roles } = useAuth();
  return roles.includes(role);
}

// Declarative permission gate
export function Can({
  permission,
  children,
  fallback = null,
}: {
  permission: Permission;
  children: ReactNode;
  fallback?: ReactNode;
}) {
  const allowed = useHasPermission(permission);
  return allowed ? <>{children}</> : <>{fallback}</>;
}

// Usage
function PostActions({ postId }: { postId: string }) {
  return (
    <div className="flex gap-2">
      <Can permission="update:post">
        <button className="rounded-lg px-4 py-3 text-sm bg-indigo-600 text-white
                          transition-all duration-200 hover:bg-indigo-700
                          focus-visible:ring-2 focus-visible:ring-offset-2">
          Edit
        </button>
      </Can>
      <Can permission="delete:post">
        <button className="rounded-lg px-4 py-3 text-sm bg-red-600 text-white
                          transition-all duration-200 hover:bg-red-700
                          focus-visible:ring-2 focus-visible:ring-offset-2">
          Delete
        </button>
      </Can>
    </div>
  );
}
```

### Step 6: Ownership-Based Authorization (ABAC Extension)

```typescript
// For "can edit own posts" style rules
interface PolicyContext {
  userId: string;
  resource: {
    type: string;
    ownerId?: string;
    teamId?: string;
  };
  action: string;
}

type Policy = (context: PolicyContext) => Promise<boolean>;

const policies: Record<string, Policy> = {
  'update:post': async (ctx) => {
    // Admin can update any post
    if (await hasRole(ctx.userId, 'admin')) return true;
    // Editors can update their own posts
    if (await hasRole(ctx.userId, 'editor') && ctx.resource.ownerId === ctx.userId) return true;
    return false;
  },

  'delete:post': async (ctx) => {
    // Only admin can delete
    return hasRole(ctx.userId, 'admin');
  },

  'update:user': async (ctx) => {
    // Users can update themselves, admins can update anyone
    if (ctx.resource.ownerId === ctx.userId) return true;
    return hasRole(ctx.userId, 'admin');
  },
};

export async function authorize(context: PolicyContext): Promise<boolean> {
  const key = `${context.action}:${context.resource.type}`;
  const policy = policies[key];

  if (!policy) {
    // Default deny — no policy means no access
    return false;
  }

  return policy(context);
}
```

## Common Pitfalls

1. **Checking roles instead of permissions** — `if (role === 'admin')` is fragile. Check permissions: `if (can('delete:user'))`. When you add a new "super-editor" role, you just assign permissions — no code changes.
2. **Client-side only checks** — UI gates are UX conveniences, not security. Always enforce permissions on the server (API routes, middleware). A hidden button can still be called via curl.
3. **Not caching per-request** — Permission checks hit the database. Cache the user's permission set once per request (not globally, since permissions can change between requests).
4. **Hardcoding permission strings** — Use a typed enum or const object for permission strings. Typos in `"delte:user"` silently deny access.
5. **Missing default deny** — If no policy matches, the answer must be "deny." Never default to allow.
6. **Forgetting to check ownership** — RBAC alone says "editors can update posts." You also need "but only THEIR posts." Combine RBAC with ownership checks.
7. **Not auditing permission changes** — Log who assigned/revoked roles and when. This is critical for security audits.

## Best Practices

- **Principle of Least Privilege**: Start with minimal permissions, add as needed
- **Default deny**: No policy = no access
- **Separate authn from authz**: Authentication (who are you?) and authorization (what can you do?) are different concerns
- **Permission format**: `action:resource` (e.g., `create:post`, `manage:billing`)
- **Cache permissions per-request**: Load once at the start of the request, reuse throughout
- **Audit log**: Record all role/permission changes with who, what, when
- **Seed system roles**: Mark built-in roles as `is_system = true` to prevent accidental deletion
- **Test permissions**: Write tests that verify each role can/cannot access specific resources
