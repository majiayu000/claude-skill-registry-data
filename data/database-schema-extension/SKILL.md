---
name: Database Schema Extension
description: Extend the Supabase PostgreSQL database schema following this project's declarative schema patterns, migration workflow, and type generation pipeline. Use when adding tables, columns, enums, RLS policies, triggers, or database functions.
---

# Database Schema Extension

This skill guides you through extending the database schema using declarative schema files, Supabase migrations, and automatic type generation.

## Quick Reference

**Key Commands:**

- `bun db:diff <migration_name>` - Generate migration from schema changes
- `bun migrate:up` - Apply migrations to local database
- `bun gen:types` - Regenerate TypeScript types and Zod schemas
- `bun db:reset` - Reset database (destructive!)

**Schema File Organization:**

```
supabase/schemas/
├── 00-extensions.sql    # PostgreSQL extensions
├── 01-schema.sql        # Tables, enums, indexes
├── 02-policies.sql      # Row Level Security policies
└── 03-functions.sql     # Database functions and triggers
```

## Complete Workflow

### Step 1: Modify Declarative Schema Files

The project uses **declarative schema files** in `supabase/schemas/`. These files define the desired state of your database, and Supabase CLI generates migrations by comparing them with your local database.

### Step 2: Follow SQL Style Guidelines

**Naming Conventions:**

- Tables: `snake_case`, plural (e.g., `todos`, `user_profiles`)
- Columns: `snake_case`, singular (e.g., `user_id`, `created_at`)
- Enums: `snake_case`, singular (e.g., `priority_level`, `user_role`). Always prefer enums over text for fixed sets.
- Foreign keys: `{singular_table_name}_id` (e.g., `user_id` references `users`)
- Indexes: `{table}_{column}_idx` (e.g., `todos_user_id_idx`)
- Policies: Descriptive text in quotes (e.g., `"Users can view their own todos"`). Keep them short and clear.

**SQL Standards:**

- **All SQL keywords in lowercase** (e.g., `create table`, `select`, `where`)
- Always use `public` schema prefix (e.g., `public.todos`)
- Add table comments: `comment on table public.todos is 'User todo items'`
- Add column comments for enums: `comment on column public.todos.priority is 'Priority level: low, medium, or high'`
- Always prefer enums over text for fixed sets.
- Use `timestamptz` for timestamps (includes timezone)
- Default timestamps: `created_at timestamptz default now() not null`
- Use `uuid` for primary keys: `id uuid default gen_random_uuid() primary key`

**Example Table Creation:**

```sql
-- Priority enum type
create type public.priority_level as enum ('low', 'medium', 'high');

-- Todos table
create table public.todos (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  title text not null,
  description text,
  completed boolean default false not null,
  priority public.priority_level,
  due_date timestamptz,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- Indexes for performance
create index todos_user_id_idx on public.todos(user_id);
create index todos_completed_idx on public.todos(completed);
create index todos_due_date_idx on public.todos(due_date);

-- Comments for documentation
comment on table public.todos is 'User todo items';
comment on column public.todos.priority is 'Priority level: low, medium, or high';
```

### Step 3: Add Row Level Security (RLS)

**Critical RLS Rules:**

1. **Always enable RLS** on new tables (even public tables)
2. **Create separate policies** for each operation (select, insert, update, delete)
3. **Specify roles explicitly** using `to authenticated` or `to anon`
4. **Add indexes** on columns used in policies (usually `user_id`)

**Policy Structure:**

```sql
-- Enable RLS
alter table public.todos enable row level security;

-- SELECT policy
create policy "Users can view their own todos"
  on public.todos for select
  to authenticated
  using (auth.uid() = user_id);

-- INSERT policy
create policy "Users can create their own todos"
  on public.todos for insert
  to authenticated
  with check (auth.uid() = user_id);

-- UPDATE policy
create policy "Users can update their own todos"
  on public.todos for update
  to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- DELETE policy
create policy "Users can delete their own todos"
  on public.todos for delete
  to authenticated
  using (auth.uid() = user_id);
```

**Key Policy Guidelines:**

- **SELECT policies**: Use `using` only (not `with check`)
- **INSERT policies**: Use `with check` only (not `using`)
- **UPDATE policies**: Use both `using` and `with check`
- **DELETE policies**: Use `using` only (not `with check`)
- **Never use `FOR ALL`**: Always separate into individual policies
- **Avoid joins**: Rewrite policies to use `IN` or `ANY` instead

**Public Access Example:**

```sql
-- Public read access
create policy "Avatar media is viewable by everyone"
  on public.media for select
  to authenticated, anon
  using (media_type = 'avatar');
```

### Step 4: Add SQL Functions and Triggers

**SQL Function Best Practices:**

1. **Default to `security invoker`** (run with caller's permissions)
2. **Set `search_path = ''`** and use fully qualified names
3. **Use explicit typing** for parameters and return values
4. **Declare as `immutable` or `stable`** when possible for optimization

**Common Pattern: `updated_at` Trigger**

```sql
-- Reuse existing function for updated_at
create trigger my_table_updated_at
  before update on public.my_table
  for each row
  execute function public.handle_updated_at();
```

The project already has `public.handle_updated_at()` function - just create the trigger!

**Custom Function Example:**

```sql
-- RPC function example
create or replace function public.get_user_stats(user_uuid uuid)
returns table (
  user_id uuid,
  total_items bigint,
  completed_items bigint
) as $$
begin
  return query
  select
    user_uuid as user_id,
    count(*) as total_items,
    count(*) filter (where completed = true) as completed_items
  from public.todos
  where user_id = user_uuid;
end;
$$ language plpgsql security invoker set search_path = '';
```

### Step 5: Generate Migration

After modifying schema files, generate a migration:

```bash
bun db:diff add_bookings_table
```

**What This Does:**

1. Compares `supabase/schemas/*.sql` with your local database
2. Generates SQL migration in `supabase/migrations/YYYYMMDDHHMMSS_add_bookings_table.sql`
3. Shows you the diff for review

**Important:** Always review the generated migration SQL before applying!

### Step 6: Review and Apply Migration

1. **Review the migration file** in `supabase/migrations/`
2. Check for:

   - Destructive operations (drop, truncate, alter column types)
   - Missing RLS policies
   - Correct foreign key relationships
   - Proper indexes

3. **Apply the migration:**

```bash
bun migrate:up
```

### Step 7: Regenerate Types

**Critical Final Step:** Always regenerate types after schema changes!

```bash
bun gen:types
```

**What This Does:**

1. Runs `bun db:types` - Generates TypeScript types from database
2. Runs `bun db:types:zod` - Generates Zod schemas from TypeScript types
3. Runs `bun remove:public:prefix` - Cleans up schema names

**Generated Files:**

- `types/database.types.ts` - TypeScript types for all tables, enums, functions
- `schemas/database.schema.ts` - Zod schemas for validation

**Usage in Code:**

```typescript
// Import types
import type { Database } from "@/types/database.types";

// Use table types
type Booking = Database["public"]["Tables"]["bookings"]["Row"];
type BookingInsert = Database["public"]["Tables"]["bookings"]["Insert"];
type BookingUpdate = Database["public"]["Tables"]["bookings"]["Update"];

// Import Zod schemas
import { bookingsInsertSchema } from "@/schemas/database.schema";

// Use in server actions
const { data: validatedData, success } = bookingsInsertSchema.safeParse(input);
```

## Troubleshooting

### Migration Conflicts

If `bun db:diff` shows unexpected changes:

1. **Check if local database is out of sync:**

   ```bash
   bun db:reset  # Resets local DB to match migrations + seed data
   ```

2. **Check if you have unapplied migrations:**

   ```bash
   bun migrate:up
   ```

### Type Generation Fails

If `bun gen:types` fails:

1. **Ensure local database is running:**

   ```bash
   bun db:start
   ```

2. **Check for SQL syntax errors in schema files**

3. **Verify all migrations are applied:**

   ```bash
   bun migrate:up
   ```

### Policy Not Working

Common issues:

1. **RLS not enabled:** `alter table public.my_table enable row level security;`
2. **Missing role specification:** Add `to authenticated` or `to anon`
3. **Missing index:** Add index on `user_id` or columns used in policy
4. **Function not wrapped in select:** Use `(select auth.uid())` not `auth.uid()`

## Workflow Checklist

When extending the database schema, follow this checklist:

- [ ] Modify appropriate schema file (`00-extensions.sql`, `01-schema.sql`, `02-policies.sql`, or `03-functions.sql`)
- [ ] Follow SQL style guide (lowercase, snake_case, schema prefix)
- [ ] Add table and column comments
- [ ] Create indexes for foreign keys and frequently queried columns
- [ ] Enable RLS on new tables
- [ ] Create separate policies for select/insert/update/delete
- [ ] Add `updated_at` trigger if table has `updated_at` column
- [ ] Run `bun db:diff <migration_name>` to generate migration
- [ ] Review generated migration SQL
- [ ] Run `bun migrate:up` to apply migration
- [ ] Run `bun gen:types` to regenerate TypeScript/Zod types
- [ ] Test new schema in application code

## Best Practices Summary

1. **Always work declaratively** - Edit schema files, let Supabase generate migrations
2. **One migration per logical change** - Don't bundle unrelated changes
3. **Review before applying** - Always check generated SQL
4. **Regenerate types immediately** - Run `bun gen:types` after every schema change
5. **Enable RLS by default** - Security first, even for "public" tables
6. **Index foreign keys** - Always add indexes on reference columns
7. **Use timestamps** - Add `created_at` and `updated_at` to most tables
8. **Comment everything** - Future you will thank present you
9. **Test locally first** - Use local database, never modify production directly
10. **Follow naming conventions** - Consistency makes collaboration easier

## References

- Project package.json scripts: `/package.json`
- Existing schema examples: `/supabase/schemas/01-schema.sql`
- RLS policy examples: `/supabase/schemas/02-policies.sql`
- Function examples: `/supabase/schemas/03-functions.sql`
