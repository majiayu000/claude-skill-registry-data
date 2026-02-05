---
name: create-crud-api
description: Create API-first CRUD endpoints with validation. Use when implementing create, read, update, delete operations for any resource.
---

# Create CRUD API

Creates RESTful API endpoints following Iridium's API-first pattern with proper validation, authentication, and error handling.

## When to Use

- Implementing CRUD operations for any resource
- Creating API endpoints for data management
- Building features that need programmatic access
- User asks to "add CRUD", "create an API", or "add endpoints"

## Architecture: API-First Pattern

```
app/routes/api/[feature].ts     # API Endpoint (Business Logic)
  ↳ loader()  - GET (Read)
  ↳ action()  - POST (Create), PUT (Update), DELETE (Delete)

app/routes/[feature].tsx        # UI Route (Presentation)
  ↳ loader()  - Fetch initial data
  ↳ Component - Render UI + forms
```

## Implementation Steps

### Step 1: Define Validation Schema

**Location:** `app/lib/validations.ts`

```typescript
import { z } from 'zod';

export const createItemSchema = z.object({
    name: z.string().min(1, 'Name is required'),
    description: z.string().max(500).optional(),
});

export const updateItemSchema = createItemSchema.partial();

export type CreateItemData = z.infer<typeof createItemSchema>;
export type UpdateItemData = z.infer<typeof updateItemSchema>;
```

### Step 2: Create Model Layer Functions

**Location:** `app/models/[feature].server.ts`

```typescript
import { prisma } from '~/db.server';

export function getItem(id: string) {
    return prisma.item.findUnique({ where: { id } });
}

export function getItemsByUser(userId: string) {
    return prisma.item.findMany({
        where: { userId },
        orderBy: { createdAt: 'desc' },
    });
}

export function createItem(userId: string, data: CreateItemData) {
    return prisma.item.create({
        data: { ...data, userId },
    });
}

export function updateItem(id: string, data: UpdateItemData) {
    return prisma.item.update({
        where: { id },
        data,
    });
}

export function deleteItem(id: string) {
    return prisma.item.delete({ where: { id } });
}
```

### Step 3: Create API Endpoint

**Location:** `app/routes/api/[feature].ts`

```typescript
import type { Route } from './+types/[feature]';
import { data } from 'react-router';
import { zodResolver } from '@hookform/resolvers/zod';
import { requireUser } from '~/lib/session.server';
import { validateFormData } from '~/lib/form-validation.server';
import { createItemSchema, updateItemSchema } from '~/lib/validations';
import { getItem, createItem, updateItem, deleteItem } from '~/models/item.server';

// GET - Read
export async function loader({ request, params }: Route.LoaderArgs) {
    const user = await requireUser(request);
    const item = await getItem(params.id);

    if (!item) {
        throw new Response('Not Found', { status: 404 });
    }

    if (item.userId !== user.id) {
        throw new Response('Forbidden', { status: 403 });
    }

    return data({ item });
}

// POST/PUT/DELETE
export async function action({ request, params }: Route.ActionArgs) {
    const user = await requireUser(request);

    if (request.method === 'POST') {
        const formData = await request.formData();
        const { data: validated, errors } = await validateFormData(
            formData,
            zodResolver(createItemSchema)
        );

        if (errors) {
            return data({ errors }, { status: 400 });
        }

        const item = await createItem(user.id, validated!);
        return data({ success: true, item }, { status: 201 });
    }

    if (request.method === 'PUT') {
        const formData = await request.formData();
        const { data: validated, errors } = await validateFormData(
            formData,
            zodResolver(updateItemSchema)
        );

        if (errors) {
            return data({ errors }, { status: 400 });
        }

        // Authorization check
        const existing = await getItem(params.id);
        if (!existing || existing.userId !== user.id) {
            throw new Response('Forbidden', { status: 403 });
        }

        const item = await updateItem(params.id, validated!);
        return data({ success: true, item });
    }

    if (request.method === 'DELETE') {
        const existing = await getItem(params.id);
        if (!existing || existing.userId !== user.id) {
            throw new Response('Forbidden', { status: 403 });
        }

        await deleteItem(params.id);
        return data({ success: true });
    }

    return data({ error: 'Method not allowed' }, { status: 405 });
}
```

### Step 4: Register Route

**Location:** `app/routes.ts`

```typescript
...prefix(Paths.API, [
    route('items', 'routes/api/items.ts'),
    route('items/:id', 'routes/api/items.$id.ts'),
]),
```

## HTTP Methods

| Method | Purpose | Handler | Success Code |
|--------|---------|---------|--------------|
| GET | Read | `loader()` | 200 |
| POST | Create | `action()` | 201 |
| PUT | Update | `action()` | 200 |
| DELETE | Delete | `action()` | 200 |

## Error Response Pattern

```typescript
// Validation errors (400)
if (errors) {
    return data({ errors }, { status: 400 });
}

// Not found (404)
if (!resource) {
    throw new Response('Not Found', { status: 404 });
}

// Forbidden (403)
if (resource.userId !== user.id) {
    throw new Response('Forbidden', { status: 403 });
}

// Server error (500)
return data({ error: 'Operation failed' }, { status: 500 });
```

## Security Checklist

- [ ] Call `requireUser(request)` at start of loader/action
- [ ] Check resource ownership before update/delete
- [ ] Validate all input with Zod schemas
- [ ] Return appropriate HTTP status codes
- [ ] Use model layer, never call Prisma directly

## Anti-Patterns

- ❌ Calling Prisma directly in route files
- ❌ Skipping server-side validation
- ❌ Not checking authorization
- ❌ Returning sensitive data without filtering
- ❌ Missing error handling

## Templates

- [API Endpoint Template](./templates/crud-endpoint.ts)

## Full Reference

See `.github/instructions/crud-pattern.instructions.md` for comprehensive documentation.
