---
name: client-server-data-flow
description: Implement type-safe client-server data flows in Next.js applications using Supabase, TanStack Query, React Hook Form, and Zod validation. Use when building CRUD features, handling forms with validation, implementing file uploads, or creating server actions with authentication and authorization. Essential for pages requiring data mutations with proper loading states, error handling, and query cache management.
---

# Next.js + Supabase Data Flow Patterns

## Overview

Implement complete client-server data flows following this codebase's established patterns for type safety, validation, authentication, and user experience.

This skill covers the entire data flow from form submission through server validation to database operations, including file uploads, query invalidation, and proper error handling.

## When to Use This Skill

Use this skill when:

- Building CRUD features (create, read, update, delete operations)
- Implementing forms with validation and error handling
- Handling file uploads to Supabase Storage
- Creating authenticated server actions
- Setting up query invalidation patterns
- Implementing loading states and user feedback

## Core Architecture

### Data Flow Overview

```
User Input (Form)
  ↓ React Hook Form + Zod Validation
Client-Side Validation
  ↓ TanStack Query Mutation
Server Action
  ↓ Authentication Check
  ↓ Zod Validation
  ↓ Authorization Check
Database Operation (Supabase)
  ↓ Success/Error Response
Query Invalidation
  ↓ UI Update + Toast Notification
```

### Technology Stack

- **React Hook Form** - Form state and validation
- **Zod** - Schema validation (inferred from database)
- **TanStack Query** - Mutations and cache management
- **Server Actions** - Type-safe server operations
- **Supabase** - Database and authentication
- **Sonner** - Toast notifications
- **shadcn/ui** - UI components

## Implementation Workflow

### Step 1: Define Form Schema

Use Zod schemas inferred from database types:

```typescript
import { z } from "zod";
import { entityInsertSchema } from "@/schemas/database.schema";

// Pick fields from database schema
const formSchema = entityInsertSchema.pick({
  title: true,
  description: true,
  completed: true,
});

// Or extend with custom validation
const formSchema = z.object({
  title: z.string().min(1, "Required").max(200, "Too long"),
  description: z.string().max(1000, "Too long").optional(),
  completed: z.boolean(),
});

type FormData = z.infer<typeof formSchema>;
```

### Step 2: Create Server Action

Create authenticated, validated server action in `server/*.actions.ts`:

```typescript
"use server";

import { createClient } from "@/lib/supabase/server";
import { entityInsertSchema } from "@/schemas/database.schema";
import type { DatabaseTables } from "@/types";

export async function upsertEntity(
  entity: DatabaseTables["entities"]["Insert"] & { id?: string }
) {
  const supabase = await createClient();

  // 1. Authenticate
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();
  if (!user || userError) {
    return { error: "Not authenticated", data: null };
  }

  // 2. Validate with Zod
  const schema = entity.id ? entityUpdateSchema : entityInsertSchema;
  const {
    success,
    data: validated,
    error: validationError,
  } = schema.safeParse(entity);

  if (!success) {
    return { error: validationError.errors[0].message, data: null };
  }

  // 3. Set user_id
  const data = { ...validated, user_id: user.id };

  // 4. Update or Insert
  if (entity.id) {
    // Verify ownership first
    const { data: existing } = await supabase
      .from("entities")
      .select("user_id")
      .eq("id", entity.id)
      .single();

    if (existing?.user_id !== user.id) {
      return { error: "Not authorized", data: null };
    }

    return await supabase
      .from("entities")
      .update(data)
      .eq("id", entity.id)
      .select()
      .single();
  }

  return await supabase.from("entities").insert(data).select().single();
}
```

### Step 3: Create Form Component

Implement form with React Hook Form + TanStack Query:

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

export function EntityForm({ existingEntity, onSuccess }: Props) {
  const queryClient = useQueryClient();

  // 1. Initialize form
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: existingEntity?.title || "",
      description: existingEntity?.description || "",
      completed: existingEntity?.completed || false,
    },
  });

  // 2. Create mutation
  const mutation = useMutation({
    mutationFn: async (data: FormData) => {
      const dbData: DatabaseTables["entities"]["Insert"] & { id?: string } = {
        title: data.title,
        description: data.description || null,
        completed: data.completed,
        user_id: "",
      };

      if (existingEntity?.id) dbData.id = existingEntity.id;

      const result = await upsertEntity(dbData);
      if (result.error) throw new Error(result.error);
      return result.data;
    },
    onSuccess: (data) => {
      toast.success(existingEntity ? "Updated!" : "Created!");
      queryClient.invalidateQueries({ queryKey: ["entities"] });
      form.reset();
      onSuccess?.();
    },
    onError: (error) => {
      toast.error(`Error: ${error.message}`);
    },
  });

  // 3. Render form
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((data) => mutation.mutate(data))}>
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Title *</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending && <Spinner className="w-4 h-4 mr-2" />}
          {existingEntity ? "Update" : "Create"}
        </Button>
      </form>
    </Form>
  );
}
```

### Step 4: File Uploads (Browser-Side)

For file uploads, create a custom hook using Supabase client:

```typescript
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createClient } from "@/lib/supabase/client";
import imageCompression from "browser-image-compression";

export const useUploadEntityAttachments = () => {
  const queryClient = useQueryClient();
  const { profile } = useAuth();

  return useMutation({
    mutationFn: async ({
      entityId,
      files,
    }: {
      entityId: string;
      files: File[];
    }) => {
      const supabase = createClient();
      if (!profile) throw new Error("Not authenticated");

      const results = [];
      for (const file of files) {
        // 1. Compress if image
        let processed = file;
        if (file.type.startsWith("image/") && file.size > 2 * 1024 * 1024) {
          processed = await imageCompression(file, {
            maxSizeMB: 2,
            maxWidthOrHeight: 2048,
          });
        }

        // 2. Upload to storage
        const filename = `${Date.now()}-${Math.random().toString(36).slice(2)}.${file.name.split(".").pop()}`;
        const path = `${profile.id}/${entityId}/${filename}`;

        await supabase.storage
          .from("entity_attachments")
          .upload(path, processed);

        // 3. Create media record
        const { data } = await supabase
          .from("media")
          .insert({
            entity_id: entityId,
            file_path: path,
            media_type: "entity_attachment",
            owner_id: profile.id,
          })
          .select()
          .single();

        results.push(data);
      }

      return results;
    },
    onSuccess: (data) => {
      toast.success(`${data.length} file(s) uploaded!`);
      queryClient.invalidateQueries({ queryKey: ["entities"] });
    },
  });
};
```

## Delete Functionality

Add delete functionality with confirmation dialog:

```typescript
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Trash2 } from "lucide-react";

const [isDeleteDialogOpen, setIsDeleteDialogOpen] = React.useState(false);

const deleteMutation = useMutation({
  mutationFn: async () => {
    if (!existingItem?.id) throw new Error("No item to delete");
    const result = await deleteItem(existingItem.id);
    if (result.error) {
      throw new Error(
        typeof result.error === "string"
          ? result.error
          : result.error.message
      );
    }
    return result;
  },
  onSuccess: () => {
    toast.success("Item deleted!");
    queryClient.invalidateQueries({ queryKey: ["items"] });
    queryClient.invalidateQueries({ queryKey: ["item"] });
    onSuccess?.();
  },
  onError: (error) => {
    toast.error(`Delete error: ${error.message}`);
  },
});

// In form render
{existingItem && (
  <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
    <AlertDialogTrigger asChild>
      <Button
        type="button"
        variant="destructive"
        size="sm"
        disabled={isLoading}
      >
        <Trash2 className="w-4 h-4 mr-2" />
        Delete Item
      </Button>
    </AlertDialogTrigger>
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Delete Item</AlertDialogTitle>
        <AlertDialogDescription>
          Are you sure? This action cannot be undone.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel disabled={deleteMutation.isPending}>
          Cancel
        </AlertDialogCancel>
        <AlertDialogAction
          onClick={() => {
            deleteMutation.mutate();
            setIsDeleteDialogOpen(false);
          }}
          disabled={deleteMutation.isPending}
          className="bg-red-600 hover:bg-red-700"
        >
          {deleteMutation.isPending && <Spinner className="w-4 h-4 mr-2" />}
          Delete
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
)}
```

## Key Principles

1. **Type Safety**: Use inferred types from database schemas (`DatabaseTables`, `z.infer`)
2. **Authentication First**: Always verify user authentication in server actions
3. **Server-Side Validation**: Validate with Zod in server actions, not just client
4. **Authorization**: Verify ownership before update/delete operations
5. **Query Invalidation**: Invalidate relevant queries after mutations
6. **User Feedback**: Use Sonner toasts for all success/error states
7. **Loading States**: Show spinners and disable buttons during operations
8. **Browser-Side Uploads**: Upload files directly from browser to Supabase Storage
9. **Error Handling**: Return consistent `{ error, data }` structure from server actions
10. **Null Handling**: Convert between form types (undefined, Date) and database types (null, string)

## Common Patterns

### Query Invalidation After Mutations

```typescript
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ["entities"] }); // List queries
  queryClient.invalidateQueries({ queryKey: ["entity"] }); // Detail queries
  queryClient.invalidateQueries({ queryKey: ["entity", id] }); // Specific entity
};
```

### Loading State Composition

```typescript
const isLoading =
  createMutation.isPending ||
  updateMutation.isPending ||
  uploadMutation.isUploading ||
  fileProcessing;

<Button disabled={isLoading}>Submit</Button>
```

### Error Handling Pattern

```typescript
onError: (error) => {
  toast.error(`Error: ${error.message}`);
  // Optionally log to error tracking service
  console.error("Mutation failed:", error);
};
```

### Data Transformation

```typescript
// Form → Database
const dbData = {
  title: formData.title,
  description: formData.description || null, // undefined → null
  due_date: formData.due_date?.toISOString() ?? null, // Date → string
};

// Database → Form
const defaultValues = {
  title: entity?.title || "",
  description: entity?.description || "", // null → ""
  due_date: entity?.due_date ? new Date(entity.due_date) : undefined, // string → Date
};
```

## Type Generation Workflow

When modifying database schema:

1. **Update Schema**: Edit `supabase/schemas/*.sql`
2. **Create Migration**: `bun db:diff <migration_name>`
3. **Apply Migration**: `bun migrate:up`
4. **Generate Types**: `bun gen:types`
   - Updates `types/database.types.ts`
   - Updates `schemas/database.schema.ts`
5. **Use Generated Types**: Import from `@/types` and `@/schemas/database.schema`

## Complete Example

See the todo feature for a complete reference implementation:

- **Form Component**: `components/todos/todo-form.tsx`
- **Dialog Wrapper**: `components/todos/todo-dialog.tsx`
- **Server Actions**: `server/todo.actions.ts`
- **Database Schema**: `supabase/schemas/01-schema.sql`
- **Upload Hook**: `hooks/use-upload-todo-attachments.ts`

This demonstrates all patterns working together in a production-ready feature.
