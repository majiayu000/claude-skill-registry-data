---
name: postgres-nanoid
description: This skill should be used when the user asks to "generate IDs", "create identifiers", "use nanoid", "add public_id", "prefixed identifiers", "short IDs", or discusses ID generation strategies, public vs internal IDs, or URL-friendly identifiers. Use nanoid for public identifiers and UUID for auth.users references.
version: 1.0.0
---

# PostgreSQL Nanoid Identifiers

This skill provides guidance for implementing nanoid-based identifiers in PostgreSQL, with a focus on Supabase integration.

> **Philosophy:** Use nanoid for public-facing identifiers (URLs, APIs, exports). Use UUID for internal references to auth.users. Prefixes provide context and prevent ID collisions across entities.

## Quick Reference

| Use Case | ID Type | Example |
|----------|---------|---------|
| Public API/URLs | nanoid with prefix | `usr_V1StGXR8_Z5jdHi` |
| Internal user reference | UUID | `auth.users.id` foreign key |
| Database primary key | Either | Prefer nanoid for new tables |
| Join tables | UUID FK | Reference auth.users directly |

## Core Principle

```
+------------------+     +------------------+
|     profiles     |     |   auth.users     |
+------------------+     +------------------+
| id (nanoid)  PK  |     | id (UUID)    PK  |
| public_id        |     |                  |
| user_id (UUID) --|---->|                  |
+------------------+     +------------------+
```

- **`public_id`**: Exposed in URLs, APIs, exports (nanoid with prefix)
- **`user_id`**: Internal reference to Supabase auth (UUID)
- **`id`**: Can be nanoid for new tables, UUID for legacy

## Standard Prefixes

| Entity | Prefix | Length | Example | Regex Pattern |
|--------|--------|--------|---------|---------------|
| User (profile) | `usr_` | 21 | `usr_V1StGXR8_Z5jdHi` | `^usr_[0-9a-zA-Z]{17}$` |
| Organization | `org_` | 21 | `org_kJ7mNpQ2xWzL9aB` | `^org_[0-9a-zA-Z]{17}$` |
| Team | `team_` | 22 | `team_uV4wX7yZaB3cD` | `^team_[0-9a-zA-Z]{17}$` |
| Customer | `cus_` | 21 | `cus_oP8qR1sTuV4wX` | `^cus_[0-9a-zA-Z]{17}$` |
| Product | `prd_` | 21 | `prd_mN3kL9pQwE7rT` | `^prd_[0-9a-zA-Z]{17}$` |
| Order | `ord_` | 21 | `ord_xYz7aBcDeF2gH` | `^ord_[0-9a-zA-Z]{17}$` |
| Invoice | `inv_` | 21 | `inv_9sK3pLmNqR5tU` | `^inv_[0-9a-zA-Z]{17}$` |
| Subscription | `sub_` | 21 | `sub_gH2iJ5kL8mN9` | `^sub_[0-9a-zA-Z]{17}$` |
| Transaction | `txn_` | 21 | `txn_aB4cD7eF0gH3` | `^txn_[0-9a-zA-Z]{17}$` |
| Session | `ses_` | 21 | `ses_rT5vU8wX2zY4` | `^ses_[0-9a-zA-Z]{17}$` |
| Project | `proj_` | 22 | `proj_aB3cD6eF9gH` | `^proj_[0-9a-zA-Z]{17}$` |
| Workspace | `ws_` | 20 | `ws_kL2mN5pQ8rS1tU` | `^ws_[0-9a-zA-Z]{17}$` |
| File | `file_` | 22 | `file_vW4xY7zA0bC` | `^file_[0-9a-zA-Z]{17}$` |
| API Key | `key_` | 21 | `key_dE3fG6hI9jK2` | `^key_[0-9a-zA-Z]{17}$` |
| Webhook | `whk_` | 21 | `whk_lM4nO7pQ0rS` | `^whk_[0-9a-zA-Z]{17}$` |

## Table Definition Pattern

```sql
-- Example: profiles table with nanoid
CREATE TABLE public.profiles (
  -- Primary key using nanoid
  id TEXT NOT NULL DEFAULT nanoid('usr_') PRIMARY KEY,

  -- Reference to Supabase auth (UUID)
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Profile data
  display_name TEXT,
  avatar_url TEXT,

  -- Timestamps
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

  -- Constraints
  CONSTRAINT profiles_id_format CHECK (id ~ '^usr_[0-9a-zA-Z]{17}$'),
  CONSTRAINT profiles_user_id_unique UNIQUE (user_id)
);

-- Index for user lookups
CREATE INDEX profiles_user_id_idx ON public.profiles(user_id);
```

## Migration Pattern

```sql
-- Migration: Add nanoid to existing table
-- Step 1: Add the column
ALTER TABLE public.customers
ADD COLUMN public_id TEXT;

-- Step 2: Generate IDs for existing rows
UPDATE public.customers
SET public_id = nanoid('cus_')
WHERE public_id IS NULL;

-- Step 3: Add constraints
ALTER TABLE public.customers
ALTER COLUMN public_id SET NOT NULL,
ADD CONSTRAINT customers_public_id_unique UNIQUE (public_id),
ADD CONSTRAINT customers_public_id_format CHECK (public_id ~ '^cus_[0-9a-zA-Z]{17}$');

-- Step 4: Set default for new rows
ALTER TABLE public.customers
ALTER COLUMN public_id SET DEFAULT nanoid('cus_');
```

## API Response Pattern

Always return nanoid in API responses, never internal UUIDs:

```typescript
// Good: Return public_id
return {
  id: profile.id,           // usr_V1StGXR8_Z5jdHi
  name: profile.display_name,
  // Never expose user_id (UUID) in API
}

// Bad: Exposing internal UUID
return {
  id: profile.user_id,      // Don't do this!
  ...
}
```

## TypeScript Types

```typescript
// Type-safe prefixed IDs
type UserId = `usr_${string}`
type OrgId = `org_${string}`
type OrderId = `ord_${string}`

interface Profile {
  id: UserId
  displayName: string
}

// Validation helper
function isValidUserId(id: string): id is UserId {
  return /^usr_[0-9a-zA-Z]{17}$/.test(id)
}
```

## When to Use What

| Scenario | Use |
|----------|-----|
| New table primary key | nanoid with prefix |
| Foreign key to auth.users | UUID |
| Public API endpoint | nanoid |
| Internal service-to-service | Either |
| URL slugs | nanoid (URL-safe by default) |
| Export/Import IDs | nanoid (human-readable) |
| Legacy table migration | Add public_id column |

## Common Mistakes

1. **Exposing auth.users UUID in APIs** - Always use nanoid public_id
2. **Inconsistent prefix lengths** - Keep random part at 17 chars
3. **Missing CHECK constraints** - Always validate format
4. **Not indexing public_id** - Add index for lookup performance
5. **Using nanoid for auth FK** - Use UUID for auth.users references

## Performance Notes

- nanoid generation: ~110,000 IDs/second
- Collision probability: Negligible at 17 random chars
- Index performance: Comparable to UUID
- Storage: ~21 bytes vs 16 bytes for UUID (minimal difference)

## Additional Resources

For detailed implementation, see reference files:
- **`references/installation.md`** - PostgreSQL function setup
- **`references/prefix-conventions.md`** - Complete prefix guidelines
