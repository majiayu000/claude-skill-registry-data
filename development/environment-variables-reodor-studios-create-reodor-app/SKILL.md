---
name: environment-variables
description: Use compile-time validated environment variables with t3-oss/env-nextjs. Ensures type-safe access to environment variables with automatic validation at build time. Use when accessing any environment variable or adding new environment configurations.
---

# Environment Variables

Use type-safe, compile-time validated environment variables with automatic validation at build time using t3-oss/env-nextjs.

## Overview

This project uses `@t3-oss/env-nextjs` to validate environment variables at build time, preventing runtime errors from missing or invalid configuration. All environment variables are defined in `env.ts` with Zod schemas and are validated when Next.js builds.

## How It Works

1. **Build-Time Validation**: `next.config.mjs` imports `env.ts`, triggering validation before the app builds
2. **Type Safety**: TypeScript provides autocomplete and type checking for all environment variables
3. **Runtime Access**: Import `env` from `@/env` to access validated variables anywhere in the app

## File Structure

```
/env.ts                    # Environment variable schema and validation
/next.config.mjs           # Imports env.ts for build-time validation
/.env.local                # Local development environment variables
/.env.example              # Template showing all required variables
```

## Usage Examples

### Accessing Environment Variables

**Before (process.env - not type-safe, no validation):**
```typescript
// ❌ No type checking, could be undefined
const apiKey = process.env.ANTHROPIC_API_KEY;
```

**After (env - type-safe, validated):**
```typescript
// ✅ Type-safe, guaranteed to exist and be valid
import { env } from "@/env";

const apiKey = env.ANTHROPIC_API_KEY; // string (validated at build time)
```

### Common Patterns

**Server-side usage (Server Actions, API Routes):**
```typescript
import { env } from "@/env";

export async function createUser() {
  const supabase = createClient<Database>(
    env.NEXT_PUBLIC_SUPABASE_URL,
    env.SUPABASE_SECRET_KEY // Server-only variable
  );
}
```

**Client-side usage (Components):**
```typescript
"use client";

import { env } from "@/env";

export function SupabaseProvider() {
  // Only NEXT_PUBLIC_* variables are available on client
  const client = createBrowserClient(
    env.NEXT_PUBLIC_SUPABASE_URL,
    env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_OR_ANON_KEY
  );
}
```

## Adding New Environment Variables

When adding a new environment variable, follow these steps:

### 1. Add to `.env.example` and `.env.local`

```bash
# .env.example
NEW_SERVICE_API_KEY=your-api-key-here
NEXT_PUBLIC_NEW_SERVICE_URL=https://api.example.com
```

### 2. Add to `env.ts` Schema

Determine if the variable is server-only or client-side (must start with `NEXT_PUBLIC_`):

**Server-only variable:**
```typescript
// env.ts
export const env = createEnv({
  server: {
    // Add new server variable
    NEW_SERVICE_API_KEY: z.string().min(1),
    // ... existing variables
  },
  client: {
    // ... existing client variables
  },
  runtimeEnv: {
    // Add to runtimeEnv
    NEW_SERVICE_API_KEY: process.env.NEW_SERVICE_API_KEY,
    // ... existing mappings
  },
});
```

**Client-side variable (NEXT_PUBLIC_*):**
```typescript
// env.ts
export const env = createEnv({
  server: {
    // ... existing server variables
  },
  client: {
    // Add new client variable
    NEXT_PUBLIC_NEW_SERVICE_URL: z.string().includes("://"),
    // ... existing client variables
  },
  runtimeEnv: {
    // Add to runtimeEnv
    NEXT_PUBLIC_NEW_SERVICE_URL: process.env.NEXT_PUBLIC_NEW_SERVICE_URL,
    // ... existing mappings
  },
});
```

### 3. Use in Your Code

```typescript
import { env } from "@/env";

const apiKey = env.NEW_SERVICE_API_KEY; // Type-safe access
```

## Validation Rules

### Common Zod Validators

```typescript
// Required string with minimum length
API_KEY: z.string().min(1)

// Optional string
OPTIONAL_KEY: z.string().optional()

// URL validation
SERVICE_URL: z.string().includes("://")

// Email validation
EMAIL: z.string().includes("@")

// Enum validation
NODE_ENV: z.enum(["development", "production", "test"])

// Number validation
PORT: z.coerce.number().min(1000).max(9999)
```

### Special Cases

**Email with optional display name:**
```typescript
DEV_EMAIL_FROM: z.string().includes("@").or(z.string().regex(/^.+\s<.+@.+>$/))
```

**Optional environment variable:**
```typescript
ADMIN_EMAIL: z.string().includes("@").optional()
```

## Build-Time Validation

When you run `bun run build` or `bun run dev`, Next.js automatically validates all environment variables:

```bash
# If validation fails:
❌ Invalid environment variables:
  ANTHROPIC_API_KEY: Required
  RESEND_API_KEY: Required
```

## Skip Validation (CI/CD)

In CI/CD environments where environment variables aren't available during build:

```bash
SKIP_ENV_VALIDATION=true bun run build
```

## Important Notes

1. **Never commit** `.env.local` or `.env.production` - these files are in `.gitignore`
2. **Always update** `.env.example` when adding new variables
3. **Server variables** are only accessible on the server (API routes, Server Components, Server Actions)
4. **Client variables** must be prefixed with `NEXT_PUBLIC_` and are exposed to the browser
5. **Build fails** if any required environment variable is missing or invalid

## Reference

- Schema definition: `env.ts`
- Build validation: `next.config.mjs` (imports `env.ts`)
- Example template: `.env.example`
- Documentation: https://env.t3.gg/docs/nextjs
