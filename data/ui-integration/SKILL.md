---
name: UI Integration
description: This skill should be used when the user asks to "add server action", "implement Supabase query", "connect to backend", "add database integration", "implement RLS", "use server actions", "add data mutation", "implement CRUD operations", "revalidate path", "add authentication check", or needs guidance on server-side integration, defense-in-depth security, or type-safe database queries with Supabase.
version: 0.1.0
---

# UI Integration for Next.js with Supabase

## Overview

UI Integration handles the server-side integration layer of Next.js applications with Supabase backends. This skill covers implementing Server Actions, writing type-safe Supabase queries, enforcing RLS policies with explicit auth checks, and properly revalidating data after mutations.

**Key principles:**
- Defense-in-depth: Always combine RLS policies with explicit auth checks
- Use "use server" for all server actions
- Revalidate paths after mutations for fresh data
- Generate and use TypeScript types for database queries
- Handle errors gracefully with proper error boundaries

## Skill-scoped Context

**Official Documentation:**
- Next.js Server Actions: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
- Supabase JavaScript Client: https://supabase.com/docs/reference/javascript/introduction
- Supabase Row Level Security: https://supabase.com/docs/guides/auth/row-level-security
- Next.js Revalidation: https://nextjs.org/docs/app/building-your-application/caching#revalidatepath

## Workflow

### Step 1: Define Server Actions

Create server actions in dedicated files or inline with "use server":

```tsx
// app/actions/posts.ts
"use server";

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";
import { z } from "zod";

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
});

export async function createPost(formData: FormData) {
  const supabase = await createClient();

  // Explicit auth check (defense-in-depth)
  const { data: { user }, error: authError } = await supabase.auth.getUser();
  if (authError || !user) {
    return { error: "Unauthorized" };
  }

  // Validate input
  const rawData = {
    title: formData.get("title"),
    content: formData.get("content"),
  };

  const parsed = createPostSchema.safeParse(rawData);
  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  // Insert with user_id (RLS will also enforce this)
  const { data, error } = await supabase
    .from("posts")
    .insert({
      title: parsed.data.title,
      content: parsed.data.content,
      user_id: user.id,
    })
    .select()
    .single();

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/posts");
  return { data };
}
```

### Step 2: Implement Supabase Queries

Write type-safe queries using generated types:

```tsx
// lib/supabase/queries.ts
import { createClient } from "@/lib/supabase/server";
import type { Database } from "@/lib/supabase/database.types";

type Post = Database["public"]["Tables"]["posts"]["Row"];

export async function getPosts(): Promise<Post[]> {
  const supabase = await createClient();

  const { data, error } = await supabase
    .from("posts")
    .select("*")
    .order("created_at", { ascending: false });

  if (error) {
    console.error("Error fetching posts:", error);
    return [];
  }

  return data;
}

export async function getPostById(id: string): Promise<Post | null> {
  const supabase = await createClient();

  const { data, error } = await supabase
    .from("posts")
    .select("*")
    .eq("id", id)
    .single();

  if (error) {
    console.error("Error fetching post:", error);
    return null;
  }

  return data;
}
```

### Step 3: Add Error Handling

Implement proper error handling in server actions:

```tsx
"use server";

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";

export type ActionResult<T> =
  | { success: true; data: T }
  | { success: false; error: string };

export async function deletePost(postId: string): Promise<ActionResult<void>> {
  const supabase = await createClient();

  // Auth check
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    return { success: false, error: "You must be logged in to delete posts" };
  }

  // Verify ownership before delete (explicit check + RLS)
  const { data: post } = await supabase
    .from("posts")
    .select("user_id")
    .eq("id", postId)
    .single();

  if (!post || post.user_id !== user.id) {
    return { success: false, error: "You can only delete your own posts" };
  }

  const { error } = await supabase
    .from("posts")
    .delete()
    .eq("id", postId);

  if (error) {
    return { success: false, error: error.message };
  }

  revalidatePath("/posts");
  return { success: true, data: undefined };
}
```

### Step 4: Connect to UI

Connect server actions to client components:

```tsx
// app/posts/new/page.tsx
import { createPost } from "@/app/actions/posts";
import { PostForm } from "@/components/post-form";

export default function NewPostPage() {
  return (
    <main className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-4">Create New Post</h1>
      <PostForm action={createPost} />
    </main>
  );
}
```

```tsx
// components/post-form.tsx
"use client";

import { useFormStatus } from "react-dom";
import { useActionState } from "react";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button
      type="submit"
      disabled={pending}
      className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
    >
      {pending ? "Creating..." : "Create Post"}
    </button>
  );
}

export function PostForm({
  action
}: {
  action: (formData: FormData) => Promise<{ error?: string; data?: unknown }>;
}) {
  const [state, formAction] = useActionState(action, null);

  return (
    <form action={formAction} className="space-y-4">
      {state?.error && (
        <div className="bg-red-100 text-red-700 p-3 rounded" role="alert">
          {typeof state.error === "string" ? state.error : "Validation failed"}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block font-medium">
          Title
        </label>
        <input
          type="text"
          id="title"
          name="title"
          required
          className="mt-1 block w-full rounded border px-3 py-2"
        />
      </div>

      <div>
        <label htmlFor="content" className="block font-medium">
          Content
        </label>
        <textarea
          id="content"
          name="content"
          required
          rows={5}
          className="mt-1 block w-full rounded border px-3 py-2"
        />
      </div>

      <SubmitButton />
    </form>
  );
}
```

## Defense-in-Depth Security

### RLS Policy + Explicit Auth Check

Always implement both layers of security:

**1. RLS Policy (Database Level):**

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Users can only read their own posts
CREATE POLICY "Users can read own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

-- Users can only insert posts with their user_id
CREATE POLICY "Users can create own posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can only update their own posts
CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can only delete their own posts
CREATE POLICY "Users can delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);
```

**2. Explicit Auth Check (Application Level):**

```tsx
"use server";

import { createClient } from "@/lib/supabase/server";

export async function updatePost(postId: string, title: string, content: string) {
  const supabase = await createClient();

  // ALWAYS check auth explicitly - don't rely solely on RLS
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Unauthorized" };
  }

  // Verify ownership explicitly
  const { data: existingPost } = await supabase
    .from("posts")
    .select("user_id")
    .eq("id", postId)
    .single();

  if (!existingPost || existingPost.user_id !== user.id) {
    return { error: "Forbidden: You don't own this post" };
  }

  // Now perform the update - RLS provides additional protection
  const { data, error } = await supabase
    .from("posts")
    .update({ title, content, updated_at: new Date().toISOString() })
    .eq("id", postId)
    .select()
    .single();

  if (error) {
    return { error: error.message };
  }

  return { data };
}
```

## Type-Safe Database Queries

### Generate Types

Generate TypeScript types from your Supabase schema:

```bash
npx supabase gen types typescript --project-id YOUR_PROJECT_ID > lib/supabase/database.types.ts
```

### Use Generated Types

```tsx
import { createClient } from "@/lib/supabase/server";
import type { Database } from "@/lib/supabase/database.types";

type Tables = Database["public"]["Tables"];
type Post = Tables["posts"]["Row"];
type PostInsert = Tables["posts"]["Insert"];
type PostUpdate = Tables["posts"]["Update"];

export async function createPost(post: PostInsert): Promise<Post | null> {
  const supabase = await createClient();

  const { data, error } = await supabase
    .from("posts")
    .insert(post)
    .select()
    .single();

  if (error) {
    console.error("Error creating post:", error);
    return null;
  }

  return data;
}
```

## Revalidation Patterns

### Path Revalidation

```tsx
import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  // ... create post logic

  // Revalidate the posts list page
  revalidatePath("/posts");

  // Revalidate a specific post page
  revalidatePath(`/posts/${postId}`);

  // Revalidate all pages under /posts
  revalidatePath("/posts", "layout");
}
```

### Tag Revalidation

```tsx
import { revalidateTag } from "next/cache";

// In your fetch function, tag the request
export async function getPosts() {
  const supabase = await createClient();

  const { data } = await supabase
    .from("posts")
    .select("*");

  return data;
}

// In data fetching component
import { unstable_cache } from "next/cache";

const getCachedPosts = unstable_cache(
  async () => getPosts(),
  ["posts"],
  { tags: ["posts"] }
);

// In server action, revalidate by tag
export async function createPost(formData: FormData) {
  // ... create post logic

  revalidateTag("posts");
}
```

## Complete CRUD Example

```tsx
// app/actions/todos.ts
"use server";

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";
import { z } from "zod";

const todoSchema = z.object({
  text: z.string().min(1, "Todo text is required").max(500),
});

export async function getTodos() {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return [];

  const { data, error } = await supabase
    .from("todos")
    .select("*")
    .eq("user_id", user.id)
    .order("created_at", { ascending: false });

  if (error) {
    console.error("Error fetching todos:", error);
    return [];
  }

  return data;
}

export async function createTodo(formData: FormData) {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { error: "Unauthorized" };

  const parsed = todoSchema.safeParse({ text: formData.get("text") });
  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  const { error } = await supabase
    .from("todos")
    .insert({ text: parsed.data.text, user_id: user.id });

  if (error) return { error: error.message };

  revalidatePath("/todos");
  return { success: true };
}

export async function toggleTodo(id: string, completed: boolean) {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { error: "Unauthorized" };

  const { error } = await supabase
    .from("todos")
    .update({ completed })
    .eq("id", id)
    .eq("user_id", user.id); // Explicit ownership check

  if (error) return { error: error.message };

  revalidatePath("/todos");
  return { success: true };
}

export async function deleteTodo(id: string) {
  const supabase = await createClient();

  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { error: "Unauthorized" };

  const { error } = await supabase
    .from("todos")
    .delete()
    .eq("id", id)
    .eq("user_id", user.id); // Explicit ownership check

  if (error) return { error: error.message };

  revalidatePath("/todos");
  return { success: true };
}
```

## Supabase Client Setup

### Server Client

```tsx
// lib/supabase/server.ts
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import type { Database } from "./database.types";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Handle cookies in Server Components
          }
        },
      },
    }
  );
}
```

### Client-Side Client

```tsx
// lib/supabase/client.ts
import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "./database.types";

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

## Best Practices

**DO:**
- Always check authentication in server actions
- Combine RLS policies with explicit ownership checks
- Use Zod for input validation on both client and server
- Generate and use TypeScript types from Supabase
- Revalidate paths after mutations
- Handle errors gracefully and return meaningful messages
- Use useActionState for form state management

**DON'T:**
- Rely solely on RLS without application-level checks
- Trust client-side data without server validation
- Forget to revalidate after data mutations
- Expose internal error messages to users
- Skip ownership verification for update/delete operations
- Use client components for data fetching

## Quick Reference

### Server Action Template

```tsx
"use server";

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";

export async function myAction(formData: FormData) {
  const supabase = await createClient();

  // 1. Auth check
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { error: "Unauthorized" };

  // 2. Validate input
  // 3. Perform database operation
  // 4. Revalidate path
  // 5. Return result
}
```

### Common Query Patterns

| Operation | Pattern |
|-----------|---------|
| Select all | `.from("table").select("*")` |
| Select with filter | `.from("table").select("*").eq("column", value)` |
| Select single | `.from("table").select("*").eq("id", id).single()` |
| Insert | `.from("table").insert(data).select().single()` |
| Update | `.from("table").update(data).eq("id", id)` |
| Delete | `.from("table").delete().eq("id", id)` |
| Order | `.order("created_at", { ascending: false })` |
| Limit | `.limit(10)` |

## Implementation Workflow

To add backend integration:

1. Create or update Supabase table with RLS policies
2. Generate TypeScript types from Supabase schema
3. Create server client setup in lib/supabase/server.ts
4. Define server actions with "use server" directive
5. Add explicit auth checks in every server action
6. Validate input with Zod schemas
7. Implement database queries with proper error handling
8. Add revalidatePath after mutations
9. Connect to UI components via form actions or callbacks
10. Test authentication and authorization thoroughly
