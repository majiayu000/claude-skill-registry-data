---
name: authentication-clerk
description: Specialized skill for implementing authentication and user management with Clerk. Use when working on sign-in/sign-up flows, user roles, or access control.
---

# Authentication with Clerk Skill

This skill provides expertise in implementing authentication and user management using Clerk in the Artiefy project.

## When to Use This Skill

- Setting up sign-in and sign-up pages
- Managing user roles and permissions
- Implementing protected routes
- Handling user sessions and metadata
- Integrating Clerk components in the UI

## Key Features

- **Multi-role System**: super-admin, admin, educador, estudiante
- **Protected Routes**: Role-based access control
- **User Metadata**: Store role information in publicMetadata
- **Custom Flows**: Sign-in and sign-up pages

## Patterns and Conventions

### Role-Based Access

- Roles stored in `user.publicMetadata.role`
- Route protection in middleware or components
- Dashboard routing based on role

### Clerk Components

- Use `<ClerkProvider>` in root layout
- `<SignIn />` and `<SignUp />` components
- `<UserButton />` for user management

### Environment Variables

- All Clerk keys in `src/env.ts`
- Validate with Zod schemas

## Examples

### Role-Based Routing

```tsx
// src/app/page.tsx
import { currentUser } from '@clerk/nextjs/server';

export default async function HomePage() {
  const user = await currentUser();

  const dashboardRoute = getDashboardRoute(user?.publicMetadata?.role);

  redirect(dashboardRoute);
}

function getDashboardRoute(role: string | undefined) {
  switch (role) {
    case 'super-admin':
      return '/dashboard/super-admin';
    case 'admin':
      return '/dashboard/admin';
    case 'educador':
      return '/dashboard/educadores';
    default:
      return '/estudiantes';
  }
}
```

### Protected Component

```tsx
// src/components/ProtectedRoute.tsx
'use client';
import { useUser } from '@clerk/nextjs';
import { useRouter } from 'next/navigation';

export function ProtectedRoute({
  children,
  requiredRole,
}: {
  children: React.ReactNode;
  requiredRole?: string;
}) {
  const { user, isLoaded } = useUser();
  const router = useRouter();

  if (!isLoaded) return <div>Loading...</div>;

  if (!user) {
    router.push('/sign-in');
    return null;
  }

  if (requiredRole && user.publicMetadata?.role !== requiredRole) {
    router.push('/unauthorized');
    return null;
  }

  return <>{children}</>;
}
```

### Sign-In Page

```tsx
// src/app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs';

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn routing="path" path="/sign-in" redirectUrl="/" />
    </div>
  );
}
```

## Resources

- [Clerk Documentation](https://clerk.com/docs)
- Project auth pages: `src/app/sign-in/`, `src/app/sign-up/`
- Environment config: `src/env.ts`
