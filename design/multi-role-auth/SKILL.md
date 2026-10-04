---
name: multi-role-auth
description: >
  Scaffold multi-role authentication: NextAuth.js with admin/guest/owner/customer
  roles in Next.js, or Laravel Breeze with roles in Laravel. Includes RBAC
  middleware, permission constants, role-based route guards, and UI components.
  Triggers when user asks to add multi-role auth, role-based access, RBAC,
  admin guest customer roles, or permission guards.
---

# Multi-Role Auth Agent

## Roles

| Role | Description |
|---|---|
| admin | Full access to all admin routes |
| owner | Property-level access (their hotels only) |
| guest | Logged-in customers (their own bookings) |
| customer | Public-facing users (onboarding leads) |

## Next.js/NextAuth v5 Setup

```typescript
// prisma/schema.prisma (add to User model)
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  role      UserRole @default(CUSTOMER)
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

enum UserRole {
  ADMIN
  OWNER
  GUEST
  CUSTOMER
}
```

```typescript
// lib/auth.ts (NextAuth config)
import NextAuth from 'next-auth';
import Credentials from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Credentials({
      credentials: { email: {}, password: {} },
      async authorize(creds) {
        const user = await prisma.user.findUnique({ where: { email: creds.email } });
        if (!user || !await bcrypt.compare(creds.password, user.password)) return null;
        return { id: user.id, email: user.email, name: user.name, role: user.role };
      }
    })
  ],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.role = (user as any).role;
      return token;
    },
    session({ session, token }) {
      if (session.user) (session.user as any).role = token.role;
      return session;
    }
  }
});
```

```typescript
// middleware.ts
export { auth as middleware };

export const config = {
  matcher: ['/admin/:path*', '/guest/:path*']
};
```

```typescript
// lib/rbac.ts
export const PERMISSIONS = {
  admin: ['*'],
  owner: ['hotels:read', 'hotels:write', 'bookings:read', 'bookings:write', 'rooms:read'],
  guest: ['bookings:read', 'bookings:cancel'],
  customer: ['onboard:write'],
} as const;

export function can(role: keyof typeof PERMISSIONS, action: string): boolean {
  const perms = PERMISSIONS[role];
  return perms.includes('*' as any) || perms.includes(action as any);
}
```

```tsx
// components/RoleGate.tsx
interface RoleGateProps {
  roles: UserRole[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function RoleGate({ roles, children, fallback = null }: RoleGateProps) {
  const { data: session } = useSession();
  if (!session?.user || !roles.includes((session.user as any).role)) return <>{fallback}</>;
  return <>{children}</>;
}

// Usage: <RoleGate roles={['admin', 'owner']}><AdminButton /></RoleGate>
```

```tsx
// components/RequireRole.tsx
export function RequireRole({ role, children }: { role: UserRole }) {
  const { data: session } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (session && (session.user as any).role !== role) router.push('/unauthorized');
  }, [session, role]);

  return session ? <>{children}</> : null;
}
```

## Laravel Breeze + Spatie Permission Setup

```bash
composer require spatie/laravel-permission
php artisan permission:seed
# Creates: Admin, Owner, Guest, Customer roles
# Creates: all-permissions, create-bookings, manage-rooms, etc.
```

```php
// app/Models/User.php
class User extends Authenticatable
{
    use HasRoles;

    public function hasRole(string $role): bool
    {
        return $this->roles()->where('name', $role)->exists();
    }
}
```

```php
// app/Http/Middleware/CheckRole.php
class CheckRole
{
    public function handle(Request $request, Closure $next, string $role)
    {
        if (!$request->user()?->hasRole($role)) {
            abort(403);
        }
        return $next($request);
    }
}
```

```php
// routes/web.php
Route::middleware(['auth', 'role:admin'])->prefix('admin')->group(function () {
    Route::resource('bookings', BookingController::class);
    Route::resource('rooms', RoomController::class);
});
```

## Seeder

```typescript
// prisma/seed.ts
await prisma.user.createMany({
  data: [
    { email: 'admin@example.com', name: 'Admin', role: 'ADMIN', password: await bcrypt.hash('admin123', 12) },
    { email: 'owner@example.com', name: 'Owner', role: 'OWNER', password: await bcrypt.hash('owner123', 12) },
    { email: 'guest@example.com', name: 'Guest', role: 'GUEST', password: await bcrypt.hash('guest123', 12) },
  ]
});
```
