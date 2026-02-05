---
name: create-crud-api
description: Create API-first CRUD endpoints with validation. Use when implementing create, read, update, delete operations for any resource.
---

# Create CRUD API

## When to Use

- Implementing CRUD operations for any resource
- Creating API endpoints for data management
- User asks to "add CRUD", "create an API", or "add endpoints"

## Architecture

```
app/routes/api/[feature].ts     # Business Logic
  loader()  → GET (Read)
  action()  → POST/PUT/DELETE

app/models/[feature].server.ts  # Database Operations
app/lib/validations.ts          # Zod Schemas
```

## Quick Start

### 1. Schema

```typescript
// app/lib/validations.ts
export const createItemSchema = z.object({
    name: z.string().min(1, 'Name is required'),
});
export type CreateItemData = z.infer<typeof createItemSchema>;
```

### 2. Model Layer

```typescript
// app/models/item.server.ts
import { prisma } from '~/db.server';

export function getItem(id: string) {
    return prisma.item.findUnique({ where: { id } });
}

export function createItem(userId: string, data: CreateItemData) {
    return prisma.item.create({ data: { ...data, userId } });
}
```

### 3. API Endpoint

```typescript
// app/routes/api/items.ts
import { requireUser } from '~/lib/session.server';
import { validateFormData } from '~/lib/form-validation.server';

export async function loader({ request }: Route.LoaderArgs) {
    const user = await requireUser(request);
    return data({ items: await getItemsByUser(user.id) });
}

export async function action({ request }: Route.ActionArgs) {
    const user = await requireUser(request);

    if (request.method === 'POST') {
        const formData = await request.formData();
        const { data: validated, errors } = await validateFormData(
            formData, zodResolver(createItemSchema)
        );
        if (errors) return data({ errors }, { status: 400 });

        const item = await createItem(user.id, validated!);
        return data({ item }, { status: 201 });
    }

    // Handle PUT, DELETE similarly...
}
```

### 4. Register Route

```typescript
// app/routes.ts
...prefix(Paths.API, [
    route('items', 'routes/api/items.ts'),
]),
```

## Security Checklist

- [ ] Call `requireUser(request)` at start
- [ ] Check resource ownership before update/delete
- [ ] Validate all input with Zod schemas
- [ ] Use model layer (never call Prisma directly)

## HTTP Methods

| Method | Purpose | Success Code |
|--------|---------|--------------|
| GET | Read | 200 |
| POST | Create | 201 |
| PUT | Update | 200 |
| DELETE | Delete | 200 |

## Templates

- [CRUD Endpoint Template](./templates/crud-endpoint.ts)

## Full Reference

See `.github/instructions/crud-pattern.instructions.md` for:
- Error response patterns
- Pagination
- Filtering and sorting
- Complex authorization
