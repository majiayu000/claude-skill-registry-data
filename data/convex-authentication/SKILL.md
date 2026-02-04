---
name: convex-authentication
description: Set up and manage user authentication using Convex Auth with login, signup, password reset, and user profile initialization. Use when implementing auth flows, managing user sessions, initializing user profiles, or handling authentication state.
compatibility: Requires Convex Auth 0.0.90+, Next.js App Router, ConvexAuthNextjsProvider
metadata:
  author: PictionAI
  category: backend, auth
  frameworks: Convex, @convex-dev/auth, Next.js 16
---

# Convex Authentication

## Overview

This skill implements complete user authentication using Convex Auth built-in system, including signup with profile initialization, login, password reset, and session management integrated with Next.js 16.

## Architecture

### Auth Flow

```
1. User signs up with email + password
   ↓
2. Profile initialized in users table
   (username, email, avatar_url, total_score, games_played)
   ↓
3. Auth token created
   ↓
4. User logged in, can access protected routes
   ↓
5. Can login/logout, update password
```

### Convex Auth Integration

**Note**: Uses `@convex-dev/auth` 0.0.90, NOT custom auth.

```typescript
// convex/auth.ts
import { ConvexAuth } from "@convex-dev/auth/server";
import { password } from "@convex-dev/auth/providers";

export const auth = new ConvexAuth({
  providers: [password],
});
```

### Database Schema

```typescript
// Users table (extends Convex auth)
export const users = defineTable({
  // Auth fields (built-in):
  // - email: string (unique)
  // - password: string (hashed)
  // - isEmailVerified: boolean

  // Extended fields:
  username: v.string(), // Display name
  avatar_url: v.optional(v.string()), // Profile image
  total_score: v.number(), // Cumulative score
  games_played: v.number(), // Total games
  created_at: v.number(), // Signup timestamp
})
  .index("by_email", ["email"])
  .index("by_username", ["username"]);
```

## Authentication Provider Setup

### Convex Auth Config

```typescript
// convex/auth.config.ts
import { defineAuth } from "@convex-dev/auth/server";
import { password } from "@convex-dev/auth/providers";

export default defineAuth({
  providers: [
    password({
      minPasswordLength: 8,
      maxPasswordLength: 128,
    }),
  ],
  callbacks: {
    async onSignUp(req) {
      // Called after successful signup
      // User record created automatically
      return req.identity;
    },
    async onSignIn(req) {
      // Called on successful login
      return req.identity;
    },
  },
});
```

## Signup Mutation with Profile Initialization

### signUpUser Mutation

```typescript
export const signUpUser = mutation({
  args: {
    email: v.string(),
    password: v.string(),
    username: v.string(),
  },
  handler: async (ctx, args) => {
    // 1. Validate input
    if (args.username.length < 3 || args.username.length > 30) {
      throw new Error("Username must be 3-30 characters");
    }

    // 2. Check username uniqueness
    const existing = await ctx.db
      .query("users")
      .withIndex("by_username", (q) => q.eq("username", args.username))
      .first();

    if (existing) {
      throw new Error("Username already taken");
    }

    // 3. Create auth account (handled by Convex Auth)
    // 4. Initialize user profile
    const userId = (await ctx.auth.getUserIdentity())?.tokenIdentifier;

    if (!userId) {
      throw new Error("Failed to create user account");
    }

    // 5. Store profile data
    const now = Date.now();
    await ctx.db.insert("users", {
      email: args.email,
      username: args.username,
      avatar_url: null,
      total_score: 0,
      games_played: 0,
      created_at: now,
    });

    return {
      success: true,
      userId,
      username: args.username,
    };
  },
});
```

## Zod Validation Schema

```typescript
// lib/schemas.ts
import { z } from "zod";

export const signUpSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .max(128, "Password too long"),
  username: z
    .string()
    .min(3, "Username must be at least 3 characters")
    .max(30, "Username must be at most 30 characters")
    .regex(
      /^[a-zA-Z0-9_-]+$/,
      "Username can only contain letters, numbers, underscore, hyphen"
    ),
});

export const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(1, "Password required"),
});

export const updatePasswordSchema = z.object({
  currentPassword: z.string(),
  newPassword: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .refine(
      (pwd) => /[A-Z]/.test(pwd),
      "Password must contain uppercase letter"
    )
    .refine((pwd) => /[0-9]/.test(pwd), "Password must contain number"),
});
```

## Custom Hooks

### useAuthenticatedUser

```typescript
// hooks/useAuth.ts
import { useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";

interface AuthProfile {
  user_id: string;
  username: string;
  email: string;
  avatar_url?: string;
  total_score: number;
  games_played: number;
}

export function useAuthenticatedUser() {
  const profile = useQuery(api.queries.profiles.getCurrentUserProfile);

  return {
    profile: profile as AuthProfile | null | undefined,
    isLoading: profile === undefined,
    isAuthenticated: profile !== null && profile !== undefined,
  };
}

export function useAuthContext() {
  const profile = useAuthenticatedUser();

  return {
    userId: profile.profile?.user_id,
    username: profile.profile?.username,
    email: profile.profile?.email,
    isAuthenticated: profile.isAuthenticated,
    isLoading: profile.isLoading,
  };
}
```

### getCurrentUserProfile Query

```typescript
export const getCurrentUserProfile = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();

    if (!identity) {
      return null;
    }

    const user = await ctx.db
      .query("users")
      .withIndex("by_email", (q) => q.eq("email", identity.email!))
      .first();

    return user
      ? {
          user_id: user._id,
          username: user.username,
          email: identity.email,
          avatar_url: user.avatar_url,
          total_score: user.total_score,
          games_played: user.games_played,
        }
      : null;
  },
});
```

## React Components

### AuthProvider Wrapper

```typescript
// app/layout.tsx
import { ConvexAuthNextjsProvider } from "@convex-dev/auth/nextjs";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html>
      <body>
        <ConvexAuthNextjsProvider>
          <ConvexProvider>{children}</ConvexProvider>
        </ConvexAuthNextjsProvider>
      </body>
    </html>
  );
}
```

### SignUp Form

```typescript
// components/auth/sign-up-form.tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { signUpSchema } from "@/lib/schemas";
import { useConvexAuth } from "@convex-dev/auth/react";

export function SignUpForm() {
  const form = useForm({
    resolver: zodResolver(signUpSchema),
    defaultValues: {
      email: "",
      password: "",
      username: "",
    },
  });

  const { signUp } = useConvexAuth();

  async function onSubmit(values: z.infer<typeof signUpSchema>) {
    try {
      await signUp("password", {
        email: values.email,
        password: values.password,
        username: values.username,
      });

      // Navigate to success page
      window.location.href = "/auth/sign-up-success";
    } catch (error) {
      form.setError("email", {
        message: error instanceof Error ? error.message : "Signup failed",
      });
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <FormField
        control={form.control}
        name="email"
        render={({ field }) => <EmailInput {...field} />}
      />
      <FormField
        control={form.control}
        name="username"
        render={({ field }) => <UsernameInput {...field} />}
      />
      <FormField
        control={form.control}
        name="password"
        render={({ field }) => <PasswordInput {...field} />}
      />
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

### Login Form

```typescript
// components/auth/login-form.tsx
export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(loginSchema),
  });

  const { logIn } = useConvexAuth();

  async function onSubmit(values: z.infer<typeof loginSchema>) {
    try {
      await logIn("password", {
        email: values.email,
        password: values.password,
      });

      window.location.href = "/gioca";
    } catch (error) {
      form.setError("email", {
        message: "Invalid email or password",
      });
    }
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
      <button type="submit">Log In</button>
    </form>
  );
}
```

## Session Management

### Check Auth Status

```typescript
export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuthenticatedUser();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Redirect to="/auth/login" />;
  }

  return <>{children}</>;
}
```

### Logout

```typescript
export function LogoutButton() {
  const { logOut } = useConvexAuth();

  const handleLogout = async () => {
    await logOut();
    window.location.href = "/";
  };

  return <button onClick={handleLogout}>Logout</button>;
}
```

## Password Reset Flow

### Request Password Reset

```typescript
export const requestPasswordReset = mutation({
  args: { email: v.string() },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_email", (q) => q.eq("email", args.email))
      .first();

    if (!user) {
      // Don't reveal if user exists
      return { success: true };
    }

    // Generate reset token (send via email)
    // Store token in database with expiry

    return { success: true };
  },
});
```

### Update Password

```typescript
export const updatePassword = mutation({
  args: {
    currentPassword: v.string(),
    newPassword: v.string(),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    // Verify current password before updating
    // Update with new password hash

    return { success: true };
  },
});
```

## Environment Variables

```bash
# .env.local
CONVEX_DEPLOYMENT=dev
NEXT_PUBLIC_CONVEX_URL=https://xxx.convex.cloud

# Auth specific
CONVEX_AUTH_CALLBACK=http://localhost:3000  # For development
```

## Common Patterns

### Get current user ID

```typescript
const { userId } = useAuthContext();
```

### Redirect non-authenticated users

```typescript
useEffect(() => {
  if (!isAuthenticated && !isLoading) {
    router.push("/auth/login");
  }
}, [isAuthenticated, isLoading, router]);
```

### Update user score after game

```typescript
const updateScore = useMutation(api.mutations.profiles.updateUserScore);

await updateScore({
  user_id: userId,
  points: 150,
});
```

## Best Practices

✅ Always validate email format server-side
✅ Hash passwords (Convex Auth does this automatically)
✅ Check username uniqueness before signup
✅ Use protected routes for authenticated pages
✅ Log auth events for security monitoring
✅ Implement rate limiting on auth endpoints
✅ Use secure HTTP-only cookies for tokens
✅ Validate password strength requirements

## See Also

- `convex/auth.ts` - Auth configuration
- `convex/auth.config.ts` - Auth providers setup
- `convex/queries/profiles.ts` - User profile queries
- `components/auth/` - Auth UI components
- Convex Auth docs: https://docs.convex.dev/auth/overview
