---
name: add-server-action
description: Scaffold a Next.js server action with auth guard, Supabase mutation, and revalidation
disable-model-invocation: true
---

# Add Server Action Skill

## Purpose

Generate a Next.js Server Action that authenticates the user, performs a Supabase mutation, and revalidates the relevant path — following the Arch Systems pattern.

## Process

### 1. Ask for action details

- **file location** — Where to create the action file (e.g. `apps/portal/app/(departments)/[department]/breakdowns/actions.ts`)
- **action names and types** — List of actions with:
  - Name (e.g. `createBreakdown`, `updateDelay`)
  - Operation: `insert` | `update` | `delete` | `soft-delete`
  - Table name (e.g. `breakdowns`, `operational_delays`)
  - Input fields and types
- **revalidation path** — Path to revalidate after mutation (e.g. `/engineering/breakdowns`)
- **access control** — Who can perform this action? (e.g. `admin`, `supervisor`, `operator`, any authenticated user)
- **soft delete** — Should delete set a `deleted_at` timestamp instead of removing the row?

### 2. Generate the action file

Create the `actions.ts` file with `"use server"` directive:

```typescript
"use server";

import { createServerSupabaseClient } from "@repo/supabase/server";
import { revalidatePath } from "next/cache";

// --- INSERT action ---
export async function <actionName>(formData: FormData) {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    throw new Error("Unauthorized");
  }

  // Extract and validate required fields
  const <field1> = formData.get("<field1>") as string;
  const <field2> = formData.get("<field2>") as string;

  if (!<field1> || !<field2>) {
    return { error: "Missing required fields" };
  }

  const { error } = await supabase
    .from("<table>")
    .insert({
      <field1>,
      <field2>,
      // department_id from hidden field or context
    });

  if (error) {
    throw new Error(error.message);
  }

  revalidatePath("<revalidationPath>");
  return { success: true };
}

// --- UPDATE action ---
export async function <actionName>Update(formData: FormData) {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    throw new Error("Unauthorized");
  }

  const id = formData.get("id") as string;
  // ... extract updatable fields

  const { error } = await supabase
    .from("<table>")
    .update({
      // ... fields to update
    })
    .eq("id", id);

  if (error) {
    throw new Error(error.message);
  }

  revalidatePath("<revalidationPath>");
  return { success: true };
}

// --- SOFT DELETE action ---
export async function <actionName>Delete(formData: FormData) {
  const supabase = await createServerSupabaseClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    throw new Error("Unauthorized");
  }

  const id = formData.get("id") as string;

  const { error } = await supabase
    .from("<table>")
    .update({ deleted_at: new Date().toISOString() })
    .eq("id", id);

  if (error) {
    throw new Error(error.message);
  }

  revalidatePath("<revalidationPath>");
  return { success: true };
}
```

### 3. Usage in client components

Server actions can be called from client components in two ways:

**Option A: FormData-based (no `useTransition` needed)**

```tsx
<form action={createBreakdown}>
  <input type="hidden" name="department_id" value={departmentId} />
  {/* ... form fields with name attributes */}
  <button type="submit">Submit</button>
</form>
```

**Option B: Programmatic with `useTransition` (for validation, conditional logic)**

```tsx
"use client";
import { useTransition } from "react";
import { createBreakdown } from "./actions";

function MyComponent() {
  const [isPending, startTransition] = useTransition();

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append("field1", value1);
    startTransition(async () => {
      await createBreakdown(formData);
    });
  };
}
```

### 4. Verify

1. Test the action with valid data
2. Test that unauthenticated users get "Unauthorized" error
3. Test that required field validation works
4. Test that the page revalidates after the action
5. Commit changes

## Patterns to Follow

- **Always** start with `"use server"` directive
- **Always** authenticate: `const { data: { user } } = await supabase.auth.getUser(); if (!user) throw new Error("Unauthorized");`
- **Always** use `createServerSupabaseClient()` from `@repo/supabase/server` — NEVER `@supabase/supabase-js` directly
- Use `revalidatePath()` after mutations to refresh server component data
- For soft deletes, set `deleted_at` timestamp rather than actually deleting rows
- For role-based access, check the user's role via `supabase.from("employees").select("role").eq("auth_id", user.id).single()`
