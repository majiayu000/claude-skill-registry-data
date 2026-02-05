---
name: add-auth
description: Add BetterAuth protection to routes and actions. Use when protecting routes, requiring authentication, or implementing role-based access.
---

# Add Auth

Adds authentication and authorization to routes using BetterAuth and Iridium's session utilities.

## When to Use

- Protecting routes that require login
- Adding role-based access control
- User asks to "protect route", "add authentication", or "require login"

## Authentication Utilities

### Server-Side (in loaders/actions)

```typescript
import { requireUser, requireRole, requireAdmin } from '~/lib/session.server';
```

| Function | Purpose |
|----------|---------|
| `requireUser(request)` | Require any authenticated user |
| `requireRole(request, ['ADMIN', 'EDITOR'])` | Require specific roles |
| `requireAdmin(request)` | Require admin only |

### Client-Side (for UI only)

```typescript
import { useAuthenticatedContext } from '~/hooks/useAuthenticatedContext';
import { useUserRole } from '~/hooks/useUserRole';
```

**Note:** Client checks are for UI only. Never rely on them for security.

## Pattern 1: Middleware Protection (Layout Level)

**Best for:** Groups of routes that all require auth

```typescript
// app/routes/authenticated.tsx
import type { Route } from './+types/authenticated';
import { Outlet } from 'react-router';
import { authMiddleware } from '~/middleware/auth';

export const middleware: Route.MiddlewareFunction[] = [authMiddleware];

export default function AuthenticatedLayout() {
    return <Outlet />;
}
```

Then in `routes.ts`:

```typescript
layout('routes/authenticated.tsx', [
    route('dashboard', 'routes/dashboard.tsx'),
    route('profile', 'routes/profile.tsx'),
    route('settings', 'routes/settings.tsx'),
]),
```

## Pattern 2: Route-Level Protection

**Best for:** Individual routes

```typescript
// app/routes/dashboard.tsx
import type { Route } from './+types/dashboard';
import { requireUser } from '~/lib/session.server';

export async function loader({ request }: Route.LoaderArgs) {
    const user = await requireUser(request);

    // User is guaranteed to exist here
    const data = await getUserData(user.id);

    return { user, data };
}

export default function Dashboard({ loaderData }: Route.ComponentProps) {
    const { user } = loaderData;
    return <h1>Welcome, {user.name}</h1>;
}
```

## Pattern 3: Role-Based Protection

```typescript
import { requireRole, requireAdmin } from '~/lib/session.server';

// Require specific roles (hierarchical: USER → EDITOR → ADMIN)
export async function loader({ request }: Route.LoaderArgs) {
    const user = await requireRole(request, ['ADMIN', 'EDITOR']);
    // Only admins and editors reach here
}

// Require admin only
export async function loader({ request }: Route.LoaderArgs) {
    const user = await requireAdmin(request);
    // Only admins reach here
}
```

## Pattern 4: Action Protection

```typescript
export async function action({ request }: Route.ActionArgs) {
    const user = await requireUser(request);

    // User is authenticated
    if (request.method === 'POST') {
        await createItem(user.id, formData);
    }

    if (request.method === 'DELETE') {
        // Additional authorization check
        const item = await getItem(formData.get('id'));
        if (item.userId !== user.id) {
            throw new Response('Forbidden', { status: 403 });
        }
        await deleteItem(item.id);
    }
}
```

## Pattern 5: Client-Side UI Conditionals

```typescript
import { useAuthenticatedContext } from '~/hooks/useAuthenticatedContext';
import { useUserRole } from '~/hooks/useUserRole';

export default function Dashboard() {
    const { user } = useAuthenticatedContext();
    const { isAdmin, isEditor } = useUserRole();

    return (
        <div>
            <h1>Welcome, {user.email}</h1>

            {isAdmin && (
                <Link to="/admin">Admin Panel</Link>
            )}

            {(isAdmin || isEditor) && (
                <Link to="/content">Manage Content</Link>
            )}
        </div>
    );
}
```

## Authentication Forms

**Authentication uses client-side `authClient`**, not server actions:

```typescript
import { authClient } from '~/lib/auth-client';
import { useNavigate } from 'react-router';

const navigate = useNavigate();

const onSubmit = async (data: SignInData) => {
    const { error } = await authClient.signIn.email({
        email: data.email,
        password: data.password,
    });

    if (!error) {
        navigate('/dashboard');
    }
};
```

## Security Checklist

- [ ] Use `requireUser/requireRole` in ALL protected loaders
- [ ] Use `requireUser/requireRole` in ALL protected actions
- [ ] Check resource ownership before update/delete
- [ ] Client-side checks are for UI only, not security
- [ ] API routes must manually authenticate (no middleware)

## Anti-Patterns

- ❌ Relying on client-side auth checks for security
- ❌ Missing auth check in actions
- ❌ Not checking resource ownership
- ❌ Using server actions for sign-in/sign-up (use authClient)
- ❌ Forgetting that API routes don't have middleware

## Examples

- [Protected Route](./examples/protected-route.tsx)
- [Protected Action](./examples/protected-action.ts)

## Full Reference

See `.github/instructions/better-auth.instructions.md` for comprehensive documentation.
