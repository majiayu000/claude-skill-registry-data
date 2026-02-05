---
name: wasp-auth
description: Complete Wasp authentication setup and user management. Use when implementing auth, setting up login/signup, or working with user authentication. Includes minimal User model, auth configuration, helper functions, and protected routes.
triggers:
  [
    "auth",
    "authentication",
    "login",
    "signup",
    "user",
    "protected route",
    "getEmail",
    "password",
  ]
version: 1.0
last_updated: 2025-10-18
allowed_tools: [Edit, Bash, Read]
---

# Wasp Authentication Skill

## Quick Reference

**When to use this skill:**

- Setting up authentication
- Implementing login/signup
- Working with user data
- Creating protected routes
- Accessing email/username fields

## Critical Rules

**CRITICAL:** User model typically ONLY needs `id` field
**NEVER add:** `email`, `emailVerified`, `password`, `username` to User model (Wasp manages these)
**ALWAYS use:** `getEmail(user)` and `getUsername(user)` helpers to access auth fields

## Complete Auth Setup Workflow

### 1. User Model (Minimal)

**File:** `app/schema.prisma`

```prisma
model User {
  id Int @id @default(autoincrement())
  // Auth fields (email, password, etc.) managed by Wasp in separate tables
  // Add only NON-AUTH fields here:
  // profileImageUrl String?
  // timeZone String? @default("UTC")
}
```

**CRITICAL RULES:**

- ✅ User model ONLY needs `id` field for auth
- ❌ NEVER add: `email`, `emailVerified`, `password`, `username`
- ✅ These are managed by Wasp in `Auth` and `AuthIdentity` tables
- ✅ Exception: Advanced pattern if you need email on User for queries (see below)

### 2. Auth Configuration

**File:** `app/main.wasp`

```wasp
app myApp {
  wasp: { version: "^0.18.0" },
  title: "My App",

  auth: {
    userEntity: User,  // Links to your User model

    methods: {
      // Username/password authentication
      usernameAndPassword: {},

      // Email/password with verification
      email: {
        fromField: {
          name: "My App",
          email: "noreply@myapp.com"
        },
        emailVerification: {
          clientRoute: EmailVerificationRoute
        },
        passwordReset: {
          clientRoute: PasswordResetRoute
        }
      },

      // OAuth providers (requires env vars)
      google: {},
      github: {},
    },

    onAuthFailedRedirectTo: "/login",
  },

  emailSender: {
    provider: Dummy  // Dev: prints to console
    // provider: SMTP  // Production: SendGrid, MailGun, etc.
  }
}

// Required routes for email auth
route EmailVerificationRoute {
  path: "/auth/verify-email",
  to: EmailVerificationPage
}
page EmailVerificationPage {
  component: import { EmailVerification } from "@src/auth/EmailVerificationPage.tsx"
}

route PasswordResetRoute {
  path: "/auth/reset-password",
  to: PasswordResetPage
}
page PasswordResetPage {
  component: import { PasswordReset } from "@src/auth/PasswordResetPage.tsx"
}
```

### 3. Auth Pages

Use Wasp's pre-built components:

```typescript
// src/auth/LoginPage.tsx
import { LoginForm } from 'wasp/client/auth'

export function LoginPage() {
  return (
    <div className="container mx-auto max-w-md">
      <h1>Login</h1>
      <LoginForm />
    </div>
  )
}

// src/auth/SignupPage.tsx
import { SignupForm } from 'wasp/client/auth'

export function SignupPage() {
  return (
    <div className="container mx-auto max-w-md">
      <h1>Sign Up</h1>
      <SignupForm />
    </div>
  )
}
```

### 4. Protected Routes

**Client-side protection:**

```typescript
import { useAuth } from 'wasp/client/auth'
import { Redirect } from 'wasp/client/router'

export function ProtectedPage() {
  const { data: user, isLoading, error } = useAuth()

  if (isLoading) return <div>Loading...</div>

  if (error || !user) {
    return <Redirect to="/login" />
  }

  // User is authenticated
  return <div>Protected content for {user.id}</div>
}
```

**Server-side protection (operations):**

```typescript
import { HttpError } from "wasp/server";
import type { MyQuery } from "wasp/server/operations";

export const myQuery: MyQuery = async (args, context) => {
  // ✅ ALWAYS check auth first
  if (!context.user) throw new HttpError(401);

  // Safe to proceed
  return context.entities.Task.findMany({
    where: { userId: context.user.id },
  });
};
```

### 5. Accessing Auth Fields

**CRITICAL:** User object structure differs between AuthUser and User entity

#### Client-Side (AuthUser)

```typescript
import { useAuth, getEmail, getUsername } from 'wasp/client/auth'

export function ProfileComponent() {
  const { data: user } = useAuth()

  // ✅ CORRECT - Use helpers
  const email = getEmail(user)      // string | null
  const username = getUsername(user) // string | null

  // ❌ WRONG - Direct access FAILS
  console.log(user.email)     // UNDEFINED!
  console.log(user.username)  // UNDEFINED!

  // ✅ NULL SAFETY (REQUIRED)
  if (email) {
    return <div>Email: {email}</div>
  }

  return <div>No email</div>
}
```

#### Server-Side (Operations)

```typescript
import { getEmail, getUsername } from "wasp/auth";
import { HttpError } from "wasp/server";

export const myQuery = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  // ✅ CORRECT - Use helpers
  const email = getEmail(context.user); // string | null
  const username = getUsername(context.user); // string | null

  // ✅ NULL SAFETY (REQUIRED)
  if (!email) {
    throw new HttpError(400, "Email required");
  }

  // Safe to use email
  console.log(email);
};
```

## Advanced: Email on User Model

**IF you need email field on User entity for queries:**

### A. Add to schema.prisma

```prisma
model User {
  id    Int     @id @default(autoincrement())
  email String? @unique  // Add this
}
```

### B. Populate via userSignupFields

**File:** `app/main.wasp`

```wasp
auth: {
  userEntity: User,
  methods: {
    email: {
      userSignupFields: import { getEmailUserFields } from "@src/auth/userSignupFields"
    }
  }
}
```

**File:** `src/auth/userSignupFields.ts`

```typescript
import { defineUserSignupFields } from "wasp/auth/providers/types";
import { z } from "zod";

const userDataSchema = z.object({
  email: z.string().email(),
});

export const getEmailUserFields = defineUserSignupFields({
  email: (data) => {
    const userData = userDataSchema.parse(data);
    return { email: userData.email };
  },
});
```

### C. Run Migration

```bash
wasp db migrate-dev "Add email to User"
../scripts/safe-start.sh  # RESTART for types (multi-worktree safe)
```

## Password Security

**NEVER save passwords as plain text**

```typescript
// ❌ WRONG - Plain text password (INSECURE!)
await context.entities.User.create({
  data: {
    email: args.email,
    password: args.password  // SECURITY VULNERABILITY!
  }
})

// ✅ CORRECT - Use Wasp auth (handles hashing automatically)
// Configure in main.wasp:
auth: {
  methods: {
    usernameAndPassword: {},  // Wasp handles password hashing
    email: {}                 // Wasp handles password hashing
  }
}
```

**Rule:** Use Wasp auth system. NEVER implement password storage manually.

## Common Auth Errors

### Error: user.email is undefined

**Cause:** Trying to access email directly instead of using helper

**Fix:**

```typescript
// ❌ WRONG
const email = user.email;

// ✅ CORRECT
import { getEmail } from "wasp/client/auth";
const email = getEmail(user);
```

### Error: Cannot read property 'email' of null

**Cause:** Not checking for null before accessing auth fields

**Fix:**

```typescript
const email = getEmail(user)
if (!email) {
  // Handle missing email
  return <div>Email not available</div>
}
// Safe to use email
```

### Error: Auth not working

**Diagnostic steps:**

1. Verify auth config in main.wasp
2. Check userEntity matches User model name in schema.prisma
3. Verify .env.server has required variables (for OAuth)
4. Check Wasp server logs for auth errors
5. Restart `../scripts/safe-start.sh` (multi-worktree safe)

## Environment Variables (OAuth)

**For Google OAuth:**

```bash
# .env.server
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
```

**For GitHub OAuth:**

```bash
# .env.server
GITHUB_CLIENT_ID="your-github-client-id"
GITHUB_CLIENT_SECRET="your-github-client-secret"
```

## Critical Rules Checklist

✅ DO:

- Use minimal User model (id only)
- Use helper functions (getEmail, getUsername)
- Check for null before using auth fields
- Use Dummy email provider for development
- Restart after auth config changes
- Always check `if (!context.user)` in operations
- Use Wasp auth for password hashing

❌ NEVER:

- Add email/password fields to User model (unless using advanced pattern)
- Access user.email directly (use getEmail helper)
- Forget null checks for auth fields
- Assume all users have all auth methods
- Save passwords as plain text
- Skip auth check in operations

## Quick Setup Checklist

Initial auth setup:

- [ ] Create minimal User model (id only) in schema.prisma
- [ ] Configure auth in main.wasp
- [ ] Create LoginPage and SignupPage
- [ ] Set up email routes (if using email auth)
- [ ] Configure email provider (Dummy for dev)
- [ ] Run migration: `wasp db migrate-dev "Add auth"`
- [ ] Restart `../scripts/safe-start.sh` (multi-worktree safe)
- [ ] Test login/signup flow

## References

- Complete guide: `docs/TROUBLESHOOTING-GUIDE.md` (Auth section)
- Wasp auth docs: https://wasp.sh/docs/auth/overview
