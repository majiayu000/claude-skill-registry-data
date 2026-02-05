---
name: zod-extract
description: Find inline Zod schemas and move them to validations/ directory
---

# Zod Extract

Find Zod schemas defined outside `validations/` and centralize them.

## Instructions

1. Search for Zod usage patterns outside `validations/` directory
2. For each inline schema found:
   - Determine the appropriate validation file (existing or new)
   - Generate the export with proper naming
   - Generate the inferred type export
   - Update the original file to import from `validations/`
3. Update barrel export in `validations/index.ts`

## What to look for

Zod patterns outside `validations/`:

```typescript
// Inline schema definitions
const schema = z.object({ ... })
const userSchema = z.object({ ... })

// Inline in function calls
.input(z.object({ ... }))
zodResolver(z.object({ ... }))

// Partial/extended schemas that should be centralized
schema.partial()
schema.extend({ ... })
schema.pick({ ... })
schema.omit({ ... })
```

## Naming Convention

| Context | Schema Name | Type Name |
|---------|-------------|-----------|
| Create form | `createUserSchema` | `CreateUserInput` |
| Update form | `updateUserSchema` | `UpdateUserInput` |
| Query params | `userQuerySchema` | `UserQuery` |
| Filter/search | `userFilterSchema` | `UserFilter` |
| tRPC input | `[action][Entity]Schema` | `[Action][Entity]Input` |

## Output Pattern

### validations/[entity].ts

```typescript
import { z } from 'zod'

export const createUserSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(1, 'Name is required'),
})

export const updateUserSchema = createUserSchema.partial()

export type CreateUserInput = z.infer<typeof createUserSchema>
export type UpdateUserInput = z.infer<typeof updateUserSchema>
```

### validations/index.ts

```typescript
export * from './user'
export * from './booking'
// ... etc
```

### Updated source file

```typescript
// Before
const schema = z.object({
  email: z.string().email(),
  name: z.string().min(1),
})

// After
import { createUserSchema } from '@/validations'
```

## Common Cases

### tRPC Router Input

```typescript
// Before - server/api/routers/user/index.ts
export const userRouter = router({
  create: publicProcedure
    .input(z.object({
      email: z.string().email(),
      name: z.string(),
    }))
    .mutation(...)
})

// After
import { createUserSchema } from '@/validations'

export const userRouter = router({
  create: publicProcedure
    .input(createUserSchema)
    .mutation(...)
})
```

### React Hook Form

```typescript
// Before - components/UserForm.tsx
const form = useForm({
  resolver: zodResolver(z.object({
    email: z.string().email(),
    name: z.string().min(1),
  })),
})

// After
import { createUserSchema } from '@/validations'

const form = useForm({
  resolver: zodResolver(createUserSchema),
})
```

### Query Parameters

```typescript
// Before - app/users/page.tsx
const searchParams = z.object({
  page: z.coerce.number().default(1),
  search: z.string().optional(),
}).parse(params)

// After
import { userQuerySchema } from '@/validations'

const searchParams = userQuerySchema.parse(params)
```

## Exceptions

Keep inline when:
- One-off validation in a test file
- Truly local validation that will never be reused
- Extending/picking from an already-centralized schema in the same file

## Output Format

```
## Zod Extract Report

### Found 3 inline schemas

1. components/UserForm.tsx:12
   - Schema: z.object({ email, name })
   - Suggested: createUserSchema in validations/user.ts
   - Action: Create new file

2. server/api/routers/booking/index.ts:25
   - Schema: z.object({ date, userId })
   - Suggested: createBookingSchema in validations/booking.ts
   - Action: Add to existing file

3. app/search/page.tsx:8
   - Schema: z.object({ q, page })
   - Suggested: searchQuerySchema in validations/search.ts
   - Action: Create new file

### Ready to extract?

I can make these changes now, or you can review first.
```
