---
name: supabase
description: Supabase Auth, Realtime subscriptions, Edge Functions, Row Level Security, and Storage
layer: domain
category: database
triggers:
  - "supabase"
  - "supabase auth"
  - "supabase realtime"
  - "edge functions"
  - "row level security"
  - "RLS"
  - "supabase storage"
inputs:
  - requirements: Auth, database, realtime, storage, or edge function needs
  - framework: Next.js | React | SvelteKit (optional)
  - auth_providers: Email, OAuth, magic link, phone (optional)
outputs:
  - client_setup: Supabase client configuration
  - rls_policies: Row Level Security policy definitions
  - auth_flow: Authentication implementation
  - realtime_subscriptions: Real-time data subscription setup
  - edge_functions: Deno-based edge function implementations
linksTo:
  - postgresql
  - authentication
  - nextjs
  - react
linkedFrom:
  - cook
  - authentication
  - data-modeling
preferredNextSkills:
  - postgresql
  - authentication
fallbackSkills:
  - postgresql
riskLevel: medium
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects:
  - May create database tables and RLS policies
  - May configure auth providers
  - May deploy edge functions
---

# Supabase Skill

## Purpose

Build applications with Supabase as the backend platform. This skill covers authentication (email, OAuth, magic link), database access with Row Level Security, real-time subscriptions, file storage, and Edge Functions. Supabase is an open-source Firebase alternative built on PostgreSQL.

## Key Concepts

### Supabase Architecture

```
CLIENT (browser/app)
  |
  v
SUPABASE CLIENT SDK
  |
  +-- Auth       -> GoTrue (JWT-based authentication)
  +-- Database   -> PostgREST (auto-generated REST API from PostgreSQL)
  +-- Realtime   -> Realtime server (WebSocket subscriptions)
  +-- Storage    -> S3-compatible object storage with RLS
  +-- Functions  -> Deno Edge Functions

SECURITY MODEL:
  - Every request carries a JWT (from Auth)
  - PostgREST passes JWT claims to PostgreSQL
  - RLS policies use auth.uid() to check ownership
  - Client can ONLY access data that RLS policies allow
```

## Patterns

### Client Setup

```typescript
// lib/supabase/client.ts (browser client)
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}

// lib/supabase/server.ts (server client for Next.js)
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export async function createServerSupabaseClient() {
  const cookieStore = await cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll(); },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) => {
            cookieStore.set(name, value, options);
          });
        },
      },
    },
  );
}
```

### Authentication

```typescript
// Sign up with email
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'securepassword',
  options: {
    data: { full_name: 'Jane Doe' }, // Custom user metadata
  },
});

// Sign in with email
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'securepassword',
});

// OAuth sign in
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'github',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`,
  },
});

// Magic link
const { error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: { emailRedirectTo: `${window.location.origin}/auth/callback` },
});

// Get current user
const { data: { user } } = await supabase.auth.getUser();

// Sign out
await supabase.auth.signOut();
```

### Row Level Security (RLS)

```sql
-- Enable RLS on a table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can read all published posts
CREATE POLICY "Public posts are viewable"
  ON posts FOR SELECT
  USING (published = true);

-- Users can only read their own drafts
CREATE POLICY "Users can view own drafts"
  ON posts FOR SELECT
  USING (auth.uid() = author_id AND published = false);

-- Users can insert their own posts
CREATE POLICY "Users can create posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = author_id);

-- Users can update their own posts
CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = author_id)
  WITH CHECK (auth.uid() = author_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = author_id);

-- Admin can do anything (using custom claims)
CREATE POLICY "Admins have full access"
  ON posts FOR ALL
  USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );

-- Organization-based access
CREATE POLICY "Org members can access org data"
  ON projects FOR SELECT
  USING (
    org_id IN (
      SELECT org_id FROM memberships
      WHERE user_id = auth.uid()
    )
  );
```

### Realtime Subscriptions

```typescript
// Subscribe to changes on a table
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    {
      event: '*',         // INSERT | UPDATE | DELETE | *
      schema: 'public',
      table: 'posts',
      filter: 'author_id=eq.user_123',  // Optional filter
    },
    (payload) => {
      console.log('Change:', payload.eventType, payload.new);
      // Update local state
    },
  )
  .subscribe();

// Presence (who is online)
const room = supabase.channel('room-1');
room
  .on('presence', { event: 'sync' }, () => {
    const state = room.presenceState();
    console.log('Online:', Object.keys(state));
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await room.track({ user_id: userId, name: userName });
    }
  });

// Cleanup
supabase.removeChannel(channel);
```

### Database Queries

```typescript
// Select with filters
const { data, error } = await supabase
  .from('posts')
  .select('id, title, content, author:users(name, avatar_url)')
  .eq('published', true)
  .order('created_at', { ascending: false })
  .range(0, 19);  // Pagination: first 20 rows

// Insert
const { data, error } = await supabase
  .from('posts')
  .insert({ title: 'New Post', content: 'Hello', author_id: userId })
  .select()
  .single();

// Update
const { data, error } = await supabase
  .from('posts')
  .update({ title: 'Updated Title' })
  .eq('id', postId)
  .select()
  .single();

// Delete
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId);

// RPC (call PostgreSQL functions)
const { data, error } = await supabase.rpc('search_posts', {
  query: 'typescript',
  limit_count: 10,
});
```

### Storage

```typescript
// Upload file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/profile.jpg`, file, {
    cacheControl: '3600',
    upsert: true,
  });

// Get public URL
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/profile.jpg`);

// Download file
const { data, error } = await supabase.storage
  .from('documents')
  .download('report.pdf');
```

## Best Practices

1. **Always enable RLS** -- tables without RLS are publicly accessible via the API
2. **Use the server client for mutations** -- server components have the service role key for admin operations
3. **Test RLS policies thoroughly** -- write tests that verify unauthorized access is denied
4. **Use `auth.uid()` in policies** -- not `current_user` or custom session variables
5. **Create database functions for complex queries** -- RPC calls are faster than chained client filters
6. **Unsubscribe from realtime channels** -- prevent memory leaks in React useEffect cleanup
7. **Use storage policies** -- apply RLS-like rules to file uploads and downloads
8. **Handle auth state changes** -- use `onAuthStateChange` to react to sign-in/sign-out
9. **Type your queries** -- generate types with `supabase gen types typescript`
10. **Use migrations** -- `supabase db diff` and `supabase migration` for schema changes

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| RLS not enabled | Data publicly accessible | `ALTER TABLE x ENABLE ROW LEVEL SECURITY` |
| Using anon key server-side | Cannot bypass RLS for admin ops | Use service role key on server |
| Not cleaning up subscriptions | Memory leaks, stale listeners | `removeChannel()` in useEffect cleanup |
| Missing auth callback route | OAuth redirect fails | Create `/auth/callback` handler |
| Stale JWT on server | Unauthorized errors | Refresh session before server queries |
| No types generated | No type safety on queries | Run `supabase gen types typescript` |
