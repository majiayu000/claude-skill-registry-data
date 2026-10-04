---
name: supabase-sql
description: >
  Write, design, optimize, and debug SQL specifically for Supabase's PostgreSQL engine. Covers schema design, queries, Row Level Security (RLS) policies, migrations, query optimization, and Supabase-specific patterns (Auth triggers, Storage path tables, Realtime publications). Trigger when: the user asks to write or edit a SQL query; design a new table or modify an existing schema; optimize a slow query or fix a missing index; write or debug RLS policies; work with Supabase Auth, Storage, or Realtime; paste a Supabase error message or slow query log; asks "how do I store X in my database?" Always explain the SQL in plain English alongside the code — never dump raw code. Key capabilities: golden rules for Supabase table design (uuid IDs, timestamps, snake_case naming); full RLS policy templates for common patterns (own-data access, public read, authenticated write); explain analyze for finding missing indexes; migration-safe patterns for adding columns without downtime. Also for: writing database trigger functions (e.g. auto-creating a profile on user signup), designing junction tables for many-to-many relationships, and understanding when to use jsonb vs. separate columns. Beginner-friendly — defines SQL terms when introduced.
---

# Supabase SQL Skill

## Core Philosophy
Always explain what the SQL does in plain English alongside the code.
The user is a beginner — never assume SQL knowledge. Define terms when introduced.

---

## 1. Schema Design

### Golden Rules for Supabase Tables
- Every table needs an `id` column (use `uuid` with a default, not integers)
- Always include `created_at` and `updated_at` timestamps
- Use `references` to link tables together (foreign keys)
- Name tables in **snake_case**, plural (e.g. `user_profiles`, `blog_posts`)

### Standard Table Template
```sql
create table public.table_name (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  -- your columns here
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### Common Column Types
| Data | Supabase Type | Example |
|---|---|---|
| Short text | `text` | name, email, slug |
| Long text | `text` | description, content |
| Number (whole) | `integer` or `bigint` | count, age |
| Number (decimal) | `numeric` | price, rating |
| True/False | `boolean` | is_published, is_active |
| Date + time | `timestamptz` | created_at, scheduled_at |
| JSON data | `jsonb` | metadata, settings |
| File path | `text` | Supabase Storage path |

### Always explain relationships:
- **One-to-many**: One user has many posts → `posts.user_id` references `users.id`
- **Many-to-many**: Users join via a junction table (e.g. `team_members`)

---

## 2. Writing Queries

### SELECT (Reading Data)
```sql
-- Get all rows
select * from posts;

-- Get specific columns
select id, title, created_at from posts;

-- Filter rows
select * from posts where is_published = true;

-- Sort results
select * from posts order by created_at desc;

-- Limit results
select * from posts limit 10;

-- Combine filters
select * from posts
where is_published = true
  and created_at > '2024-01-01'
order by created_at desc
limit 20;
```

### JOIN (Combining Tables)
```sql
-- Get posts WITH their author's name
select
  posts.title,
  posts.created_at,
  profiles.display_name as author_name
from posts
join profiles on profiles.id = posts.user_id;
```
> 💡 Think of JOIN like a VLOOKUP — it pulls matching data from another table.

### INSERT (Adding Data)
```sql
insert into posts (title, content, user_id)
values ('My First Post', 'Hello world!', 'user-uuid-here');
```

### UPDATE (Editing Data)
```sql
update posts
set title = 'Updated Title', updated_at = now()
where id = 'post-uuid-here';
```

### DELETE (Removing Data)
```sql
delete from posts where id = 'post-uuid-here';
```
> ⚠️ Always include a `where` clause on DELETE — without it, you delete everything.

---

## 3. Row Level Security (RLS)

### What is RLS?
RLS is Supabase's way of controlling who can see or change data.
Without RLS, anyone with your API key can read/write everything.
Think of it as a security guard checking every database request.

### Always do this when creating a table:
```sql
-- Step 1: Enable RLS on the table
alter table public.posts enable row level security;

-- Step 2: Create policies (rules for who can do what)
```

### Most Common RLS Policies

**Users can only see their own data:**
```sql
create policy "Users can view own posts"
on public.posts for select
using (auth.uid() = user_id);
```

**Users can only edit their own data:**
```sql
create policy "Users can update own posts"
on public.posts for update
using (auth.uid() = user_id);
```

**Anyone (including logged-out) can read:**
```sql
create policy "Public can view published posts"
on public.posts for select
using (is_published = true);
```

**Only authenticated users can insert:**
```sql
create policy "Authenticated users can create posts"
on public.posts for insert
with check (auth.uid() = user_id);
```

### RLS with Auth (linking to Supabase Auth)
- `auth.uid()` → the ID of the currently logged-in user
- `auth.role()` → returns `'authenticated'` or `'anon'`

### RLS Debugging Checklist
- [ ] Is RLS enabled on the table? (`alter table X enable row level security`)
- [ ] Is there a policy for the operation failing (select/insert/update/delete)?
- [ ] Does the policy use `auth.uid()` correctly?
- [ ] Are you testing as an authenticated user, not anon?

---

## 4. Supabase-Specific Features

### Storage — Saving File Paths
Supabase Storage stores files, but the database stores the *path* to the file:
```sql
create table public.avatars (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade,
  storage_path text not null, -- e.g. 'avatars/user-id/photo.jpg'
  created_at timestamptz default now()
);
```

### Realtime — Which Tables to Enable
Only enable Realtime on tables that need live updates (it adds overhead):
```sql
-- In Supabase Dashboard → Database → Replication
-- Or via SQL:
alter publication supabase_realtime add table posts;
```

### Auth — User Profiles Pattern
Supabase Auth handles login, but store extra user info in a separate table:
```sql
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  avatar_url text,
  bio text,
  updated_at timestamptz default now()
);

-- Auto-create profile when user signs up
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id)
  values (new.id);
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
```

### Edge Functions — Calling from SQL
Edge Functions are serverless — they call your DB, not the other way around.
No special SQL needed; just make sure RLS policies allow the service role.

---

## 5. Query Optimization

### Finding Slow Queries
```sql
-- See what indexes exist on a table
select indexname, indexdef
from pg_indexes
where tablename = 'your_table_name';

-- Check query performance (run in SQL editor)
explain analyze
select * from posts where user_id = 'some-uuid';
```
> 💡 Look for "Seq Scan" in the output — that means no index is being used (slow).

### Adding Indexes (Speed Up Lookups)
```sql
-- Index a column you filter by often
create index on posts (user_id);
create index on posts (created_at desc);

-- Index for text search
create index on posts using gin(to_tsvector('english', title));
```
> Add indexes on columns you use in `where`, `order by`, or `join` conditions.

### Optimization Checklist
- [ ] Avoid `select *` — only select columns you need
- [ ] Add indexes on foreign key columns (e.g. `user_id`)
- [ ] Add indexes on columns used in `where` filters
- [ ] Use `limit` on all list queries
- [ ] Avoid running queries inside loops — use JOINs instead

---

## 6. Migrations (Making Changes Safely)

Always use migrations instead of editing tables directly in production:
```sql
-- Adding a new column
alter table posts add column view_count integer default 0;

-- Renaming a column (careful — breaks existing code)
alter table posts rename column body to content;

-- Adding a NOT NULL constraint safely
alter table posts add column status text default 'draft' not null;
```

---

## Output Format for SQL Responses

Always structure SQL help as:
1. **What this does** — plain English explanation (1-2 sentences)
2. **The SQL** — clean, commented code block
3. **Where to run it** — Supabase Dashboard → SQL Editor, or as a migration
4. **Watch out for** — any gotchas, side effects, or follow-up steps needed
```