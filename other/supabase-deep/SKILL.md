---
name: supabase-deep
description: Deep Supabase reference — auth flows, RLS patterns, edge functions, realtime, storage, Next.js SSR integration.
---

# Supabase Deep Reference

> Local repo: `repos/supabase-docs`
> Use `grep -r "keyword" repos/supabase-docs/apps/` to search docs content.

---

## 1. Auth Patterns

### Email/Password Signup + Login

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password-123',
  options: {
    data: {
      full_name: 'Jane Doe',
      avatar_url: 'https://example.com/avatar.png',
    },
    emailRedirectTo: 'https://myapp.com/auth/callback',
  },
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password-123',
})
```

### Magic Link

```typescript
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: 'https://myapp.com/auth/callback',
  },
})
```

### OAuth (Google / GitHub / Apple)

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google', // or 'github', 'apple'
  options: {
    redirectTo: 'https://myapp.com/auth/callback',
    scopes: 'email profile', // provider-specific scopes
    queryParams: {
      access_type: 'offline',    // Google: get refresh token
      prompt: 'consent',         // Google: force consent screen
    },
  },
})
```

### @supabase/ssr for Next.js App Router

**Install:**
```bash
npm install @supabase/supabase-js @supabase/ssr
```

**Browser Client (Client Components):**
```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

**Server Client (Server Components, Route Handlers, Server Actions):**
```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Called from Server Component — ignore.
            // Middleware will refresh the session.
          }
        },
      },
    }
  )
}
```

### Middleware Auth Check (Using getClaims — NOT getSession)

> **CRITICAL**: Never trust `getSession()` on the server — the JWT payload
> can be spoofed by the client. Always use `getClaims()` (or `getUser()` which
> makes a network call to Supabase Auth) for server-side auth verification.

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // IMPORTANT: Use getClaims() — cryptographically verified from the JWT.
  // Do NOT use getSession() — it reads unverified data from the cookie.
  const { data: claims, error } = await supabase.auth.getClaims()

  if (error || !claims) {
    // No valid session — redirect to login
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  // Optional: check role from claims
  // const role = claims.claims?.user_role
  // if (role !== 'admin') { redirect to unauthorized }

  return supabaseResponse
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|login|auth|api/auth).*)',
  ],
}
```

### Session Management & onAuthStateChange

```typescript
'use client'
import { useEffect } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export function AuthListener() {
  const supabase = createClient()
  const router = useRouter()

  useEffect(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_IN') {
        router.refresh()
      }
      if (event === 'SIGNED_OUT') {
        router.push('/login')
      }
      if (event === 'TOKEN_REFRESHED') {
        // Session was refreshed — new tokens set automatically
      }
      if (event === 'PASSWORD_RECOVERY') {
        router.push('/reset-password')
      }
    })

    return () => subscription.unsubscribe()
  }, [supabase, router])

  return null
}
```

### Protected API Routes

```typescript
// app/api/protected/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()

  // Use getUser() for API routes — makes a network call to verify
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { data } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single()

  return NextResponse.json(data)
}
```

---

## 2. Row Level Security (RLS)

### Enable RLS

```sql
-- ALWAYS enable RLS on every table that holds user data
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Force RLS even for table owner (important for service role testing)
ALTER TABLE public.posts FORCE ROW LEVEL SECURITY;
```

### Basic SELECT Policy (Read Own Rows)

```sql
CREATE POLICY "Users can view own posts"
  ON public.posts
  FOR SELECT
  USING (auth.uid() = user_id);
```

### Public SELECT Policy (Anyone Can Read)

```sql
CREATE POLICY "Public posts are viewable by everyone"
  ON public.posts
  FOR SELECT
  USING (is_published = true);
```

### INSERT Policy

```sql
CREATE POLICY "Users can create own posts"
  ON public.posts
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

### UPDATE Policy (Own Rows Only)

```sql
CREATE POLICY "Users can update own posts"
  ON public.posts
  FOR UPDATE
  USING (auth.uid() = user_id)       -- which rows they can see to update
  WITH CHECK (auth.uid() = user_id); -- what the row must look like after update
```

### DELETE Policy

```sql
CREATE POLICY "Users can delete own posts"
  ON public.posts
  FOR DELETE
  USING (auth.uid() = user_id);
```

### Service Role Bypass in Edge Functions

```typescript
// In Edge Functions, use the service_role key to bypass RLS
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabaseAdmin = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!  // bypasses RLS
)

// This query ignores all RLS policies
const { data } = await supabaseAdmin
  .from('posts')
  .select('*')
```

### Junction Table Policies (Many-to-Many)

```sql
-- Example: team_members junction table
CREATE TABLE public.team_members (
  team_id UUID REFERENCES public.teams(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT DEFAULT 'member',
  PRIMARY KEY (team_id, user_id)
);

ALTER TABLE public.team_members ENABLE ROW LEVEL SECURITY;

-- Users can view teams they belong to
CREATE POLICY "Team members can view their team membership"
  ON public.team_members
  FOR SELECT
  USING (auth.uid() = user_id);

-- Only team admins can add members
CREATE POLICY "Team admins can add members"
  ON public.team_members
  FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.team_members
      WHERE team_id = team_members.team_id
        AND user_id = auth.uid()
        AND role = 'admin'
    )
  );

-- RLS on the teams table using the junction
CREATE POLICY "Users can view their teams"
  ON public.teams
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.team_members
      WHERE team_members.team_id = teams.id
        AND team_members.user_id = auth.uid()
    )
  );
```

### Common RLS Mistakes

1. **Forgetting to enable RLS** — table is wide open to any authenticated user with the anon key
2. **Overly permissive SELECT** — `USING (true)` lets anyone read all rows
3. **Missing WITH CHECK on UPDATE** — user could change `user_id` to hijack another user's row
4. **Not testing with anon key** — always test policies using the anon key, not service role
5. **Recursive policies** — a policy on table A that queries table A causes infinite recursion. Use `security definer` functions instead.
6. **Forgetting RLS on junction tables** — the junction table itself needs policies too

---

## 3. Edge Functions

### Create & Deploy

```bash
# Create a new function
supabase functions new my-function

# Deploy
supabase functions deploy my-function

# Deploy all functions
supabase functions deploy

# Set secrets (environment variables)
supabase secrets set STRIPE_SECRET_KEY=sk_live_xxx
supabase secrets set RESEND_API_KEY=re_xxx
```

### Basic Edge Function

```typescript
// supabase/functions/my-function/index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { corsHeaders } from '../_shared/cors.ts'

Deno.serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    )

    // Get the authenticated user
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })
    }

    const body = await req.json()

    // Do work...
    const { data, error } = await supabase
      .from('tasks')
      .insert({ title: body.title, user_id: user.id })
      .select()
      .single()

    return new Response(JSON.stringify(data), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }
})
```

### Shared CORS Headers

```typescript
// supabase/functions/_shared/cors.ts
export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers':
    'authorization, x-client-info, apikey, content-type',
}
```

### Invoke from Client

```typescript
const { data, error } = await supabase.functions.invoke('my-function', {
  body: { title: 'New Task' },
})
```

### Use Cases
- **Webhook handlers** — receive Stripe/Resend/GitHub webhooks
- **Scheduled functions** — cron jobs via `pg_cron` or Supabase dashboard
- **Third-party API calls** — proxy to OpenAI, Stripe, etc. keeping keys server-side
- **Complex business logic** — anything that shouldn't run client-side

---

## 4. Realtime

### Subscribe to Database Changes

```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function RealtimeMessages({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([])
  const supabase = createClient()

  useEffect(() => {
    // Initial fetch
    supabase
      .from('messages')
      .select('*')
      .eq('room_id', roomId)
      .order('created_at')
      .then(({ data }) => setMessages(data ?? []))

    // Subscribe to new inserts
    const channel = supabase
      .channel(`room-${roomId}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `room_id=eq.${roomId}`,
        },
        (payload) => {
          setMessages((prev) => [...prev, payload.new as Message])
        }
      )
      .on(
        'postgres_changes',
        {
          event: 'DELETE',
          schema: 'public',
          table: 'messages',
          filter: `room_id=eq.${roomId}`,
        },
        (payload) => {
          setMessages((prev) =>
            prev.filter((m) => m.id !== payload.old.id)
          )
        }
      )
      .subscribe()

    // Cleanup on unmount
    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId, supabase])

  return (
    <ul>
      {messages.map((m) => (
        <li key={m.id}>{m.content}</li>
      ))}
    </ul>
  )
}
```

### Presence (Who's Online)

```typescript
const channel = supabase.channel('room-1')

// Track presence
channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState()
    console.log('Online users:', Object.keys(state))
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences)
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences)
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user_id: user.id,
        username: user.email,
        online_at: new Date().toISOString(),
      })
    }
  })
```

### Broadcast (Ephemeral Messages — No DB)

```typescript
// Send
channel.send({
  type: 'broadcast',
  event: 'cursor-move',
  payload: { x: 100, y: 200, user_id: 'abc' },
})

// Receive
channel.on('broadcast', { event: 'cursor-move' }, (payload) => {
  console.log('Cursor moved:', payload)
})
```

### Reconnection Handling

```typescript
channel.subscribe((status, err) => {
  if (status === 'SUBSCRIBED') {
    console.log('Connected')
  }
  if (status === 'CHANNEL_ERROR') {
    console.error('Channel error — will auto-reconnect:', err)
  }
  if (status === 'TIMED_OUT') {
    console.error('Connection timed out — will auto-reconnect')
  }
  if (status === 'CLOSED') {
    console.log('Channel closed')
  }
})
```

---

## 5. Storage

### Create Bucket & Set Policies

```sql
-- Create a private bucket (via SQL or dashboard)
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', false);

-- Allow authenticated users to upload their own avatar
CREATE POLICY "Users can upload own avatar"
  ON storage.objects
  FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- Allow users to view their own avatar
CREATE POLICY "Users can view own avatar"
  ON storage.objects
  FOR SELECT
  USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- Allow users to update/delete their own avatar
CREATE POLICY "Users can update own avatar"
  ON storage.objects
  FOR UPDATE
  USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can delete own avatar"
  ON storage.objects
  FOR DELETE
  USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );
```

### Upload with RLS

```typescript
// Upload file — path includes user_id as folder for RLS
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${user.id}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true, // overwrite if exists
    contentType: file.type,
  })
```

### Signed URLs for Private Content

```typescript
// Generate a signed URL valid for 1 hour (3600 seconds)
const { data, error } = await supabase.storage
  .from('avatars')
  .createSignedUrl(`${user.id}/avatar.png`, 3600)

// data.signedUrl → use in <img src={...} />

// Batch signed URLs
const { data, error } = await supabase.storage
  .from('documents')
  .createSignedUrls(
    ['user1/doc.pdf', 'user1/report.pdf'],
    3600
  )
```

### Public URL (for Public Buckets)

```typescript
const { data } = supabase.storage
  .from('public-images')
  .getPublicUrl('hero.png')

// data.publicUrl → permanent public URL
```

### File Type & Size Validation

```typescript
const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB
const ALLOWED_TYPES = ['image/png', 'image/jpeg', 'image/webp']

function validateFile(file: File): string | null {
  if (!ALLOWED_TYPES.includes(file.type)) {
    return `Invalid file type. Allowed: ${ALLOWED_TYPES.join(', ')}`
  }
  if (file.size > MAX_FILE_SIZE) {
    return `File too large. Maximum size: ${MAX_FILE_SIZE / 1024 / 1024}MB`
  }
  return null
}

// Also configure server-side limits in bucket settings:
// supabase.storage.createBucket('avatars', {
//   public: false,
//   fileSizeLimit: 5242880,          // 5MB
//   allowedMimeTypes: ['image/png', 'image/jpeg', 'image/webp'],
// })
```
