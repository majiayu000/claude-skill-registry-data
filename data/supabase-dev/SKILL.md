---
name: supabase-dev
description: Supabase development guidelines for Next.js applications. Use when working with Supabase Auth SSR, database migrations, RLS policies, database functions, Edge Functions, or declarative schema management. Covers @supabase/ssr patterns, PostgreSQL best practices, and Deno-based Edge Functions.
---

# Supabase Development

## Quick Reference

- **Auth SSR**: See [bootstrap-auth.md](references/bootstrap-auth.md) for Next.js Auth setup
- **Migrations**: See [create-migration.md](references/create-migration.md) for migration file conventions
- **RLS Policies**: See [create-rls-policies.md](references/create-rls-policies.md) for Row Level Security
- **DB Functions**: See [create-db-functions.md](references/create-db-functions.md) for PostgreSQL functions
- **Edge Functions**: See [writing-edge-functions.md](references/writing-edge-functions.md) for Deno functions
- **Declarative Schema**: See [declarative-database-schema.md](references/declarative-database-schema.md) for schema management
- **SQL Style**: See [postgres-sql-style-guide.md](references/postgres-sql-style-guide.md) for SQL conventions

## Critical Auth Patterns

Always use `@supabase/ssr` with `getAll`/`setAll` cookie methods:

```typescript
// Browser client - src/shared/api/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}

// Server client - src/shared/api/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createClient() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll(); },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options));
          } catch { /* Server Component - middleware handles this */ }
        },
      },
    },
  );
}
```

**Never use**: `@supabase/auth-helpers-nextjs`, individual `get`/`set`/`remove` cookie methods.

## Database Essentials

### Migration Naming
```
YYYYMMDDHHmmss_short_description.sql
# Example: 20240906123045_create_profiles.sql
```

### Table Creation
```sql
create table public.books (
  id bigint generated always as identity primary key,
  title text not null,
  author_id bigint references public.authors (id)
);
alter table public.books enable row level security;
comment on table public.books is 'A list of all the books in the library.';
```

### RLS Policy Pattern
```sql
-- Separate policies for each operation
create policy "Users can view their own data"
  on public.profiles for select
  to authenticated
  using ((select auth.uid()) = user_id);

create policy "Users can update their own data"
  on public.profiles for update
  to authenticated
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
```

### Function Pattern
```sql
create or replace function public.my_function()
returns text
language plpgsql
security invoker
set search_path = ''
as $$
begin
  return 'result';
end;
$$;
```
