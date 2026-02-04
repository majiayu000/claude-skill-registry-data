---
name: better-auth
description: Implement authentication using better-auth library in web applications. Use this skill when users need to add signup, signin, signout, session management, or user profile features. Triggers on requests for authentication, login systems, user registration, OAuth integration, or protecting routes with auth.
---

# Better Auth

## Overview

Better-auth is a modern TypeScript authentication library that provides email/password auth, OAuth providers, and session management. This skill guides implementation in React/Docusaurus projects with PostgreSQL (Neon) backends.

## Quick Start Workflow

### 1. Install Dependencies

```bash
npm install better-auth
```

### 2. Environment Setup

Create/update `.env`:
```env
BETTER_AUTH_SECRET=<generate with: openssl rand -base64 32>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:pass@host/db
```

### 3. Server Configuration

Create `lib/auth.ts`:
```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
  },
  // Add custom user fields for personalization
  user: {
    additionalFields: {
      programmingLevel: { type: "string" },
      hardwareBackground: { type: "string" },
      learningGoals: { type: "string" },
    },
  },
});
```

### 4. API Route Handler

For Express/FastAPI backend, mount at `/api/auth/*`:
```typescript
import { toNodeHandler } from "better-auth/node";
import { auth } from "./lib/auth";

app.all("/api/auth/*", toNodeHandler(auth));
```

### 5. Client Setup

Create `lib/auth-client.ts`:
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

export const { useSession, signIn, signOut, signUp } = authClient;
```

### 6. Database Migration

Generate and run migrations:
```bash
npx @better-auth/cli generate
npx @better-auth/cli migrate
```

## Common Tasks

### Signup with Custom Fields

```typescript
const handleSignup = async (formData: SignupData) => {
  const { data, error } = await authClient.signUp.email({
    email: formData.email,
    password: formData.password,
    name: formData.name,
    // Custom fields for personalization
    programmingLevel: formData.programmingLevel,
    hardwareBackground: formData.hardwareBackground,
    learningGoals: formData.learningGoals,
  });

  if (error) throw new Error(error.message);
  return data;
};
```

### Session Hook Usage

```tsx
import { useSession } from "@/lib/auth-client";

function UserProfile() {
  const { data: session, isPending } = useSession();

  if (isPending) return <Loading />;
  if (!session) return <LoginPrompt />;

  return <div>Welcome, {session.user.name}</div>;
}
```

### Protected Component Pattern

```tsx
function ProtectedFeature({ children }) {
  const { data: session, isPending } = useSession();

  if (isPending) return <Skeleton />;
  if (!session) return <SignInButton />;

  return children;
}
```

### Sign Out

```typescript
const handleSignOut = async () => {
  await authClient.signOut();
  window.location.href = "/";
};
```

## User Background Questions

For personalization, collect these during signup:

1. **Programming Experience**
   - Beginner (< 1 year)
   - Intermediate (1-3 years)
   - Advanced (3+ years)

2. **Hardware/Robotics Background**
   - None
   - Hobbyist (Arduino, Raspberry Pi)
   - Professional (industrial robotics)

3. **Learning Goals**
   - Career transition
   - Academic study
   - Personal interest
   - Professional upskilling

## Resources

### references/
- `setup-guide.md` - Detailed setup instructions for different frameworks
- `database-schema.md` - User table schema with custom fields

### scripts/
- `setup-auth.py` - Automated setup script for better-auth

### assets/
- `components/` - React components for Login, Signup, Profile forms
