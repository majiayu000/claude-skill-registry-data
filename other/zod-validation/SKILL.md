---
name: zod-validation
description: This skill activates when writing form validation, request validation, or Zod schemas in Hono. It provides patterns for validating JSON bodies, query parameters, path parameters, and headers with proper error handling.
---

# Zod Validation in Hono

Patterns for request validation using Zod and @hono/zod-validator.

## Setup

```bash
bun add zod @hono/zod-validator
```

## Basic Validation

### JSON Body

```typescript
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email('Invalid email address'),
  name: z.string().min(1, 'Name is required').max(100),
  age: z.number().int().positive().optional(),
})

app.post('/users',
  zValidator('json', createUserSchema),
  async (c) => {
    const data = c.req.valid('json')
    // data is typed as { email: string; name: string; age?: number }
    return c.json(data, 201)
  }
)
```

### Query Parameters

```typescript
const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(['asc', 'desc']).default('desc'),
  search: z.string().optional(),
})

app.get('/users',
  zValidator('query', paginationSchema),
  async (c) => {
    const { page, limit, sort, search } = c.req.valid('query')
    // All values are properly typed and coerced
    return c.json({ page, limit, sort, search })
  }
)
```

### Path Parameters

```typescript
const userParamsSchema = z.object({
  id: z.string().uuid('Invalid user ID format'),
})

app.get('/users/:id',
  zValidator('param', userParamsSchema),
  async (c) => {
    const { id } = c.req.valid('param')
    return c.json({ id })
  }
)
```

### Headers

```typescript
const authHeaderSchema = z.object({
  authorization: z.string().startsWith('Bearer '),
  'x-request-id': z.string().uuid().optional(),
})

app.get('/protected',
  zValidator('header', authHeaderSchema),
  async (c) => {
    const headers = c.req.valid('header')
    return c.json({ authenticated: true })
  }
)
```

### Form Data

```typescript
const uploadSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
  // File validation happens separately
})

app.post('/upload',
  zValidator('form', uploadSchema),
  async (c) => {
    const { title, description } = c.req.valid('form')
    return c.json({ title, description })
  }
)
```

## Schema Patterns

### Reusable Field Schemas

```typescript
// validators/common.ts
export const emailSchema = z.string().email('Invalid email')
export const uuidSchema = z.string().uuid('Invalid ID format')
export const dateSchema = z.coerce.date()

export const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
})
```

### Create/Update Pattern

```typescript
// validators/user.schema.ts
export const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  password: z.string().min(8),
  role: z.enum(['user', 'admin']).default('user'),
})

// Partial for updates (all fields optional)
export const updateUserSchema = createUserSchema.partial()

// Omit for specific updates
export const updatePasswordSchema = createUserSchema.pick({
  password: true,
}).extend({
  currentPassword: z.string(),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
})

// Infer TypeScript types
export type CreateUser = z.infer<typeof createUserSchema>
export type UpdateUser = z.infer<typeof updateUserSchema>
```

### Nested Objects

```typescript
const addressSchema = z.object({
  street: z.string(),
  city: z.string(),
  country: z.string(),
  zip: z.string(),
})

const orderSchema = z.object({
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().positive(),
  })).min(1, 'At least one item required'),
  shippingAddress: addressSchema,
  billingAddress: addressSchema.optional(),
})
```

### Conditional Validation

```typescript
const paymentSchema = z.discriminatedUnion('method', [
  z.object({
    method: z.literal('card'),
    cardNumber: z.string().length(16),
    cvv: z.string().length(3),
  }),
  z.object({
    method: z.literal('paypal'),
    paypalEmail: z.string().email(),
  }),
  z.object({
    method: z.literal('bank'),
    accountNumber: z.string(),
    routingNumber: z.string(),
  }),
])
```

### Custom Refinements

```typescript
const registrationSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords must match',
  path: ['confirmPassword'],
})

const dateRangeSchema = z.object({
  startDate: z.coerce.date(),
  endDate: z.coerce.date(),
}).refine(data => data.endDate > data.startDate, {
  message: 'End date must be after start date',
  path: ['endDate'],
})
```

### Transform

```typescript
const userInputSchema = z.object({
  email: z.string().email().toLowerCase().trim(),
  name: z.string().trim(),
  tags: z.string().transform(s => s.split(',').map(t => t.trim())),
})
```

## Custom Error Handling

### Custom Error Hook

```typescript
import { zValidator } from '@hono/zod-validator'

const customValidator = <T extends z.ZodType>(
  target: 'json' | 'query' | 'param' | 'header' | 'form',
  schema: T
) => {
  return zValidator(target, schema, (result, c) => {
    if (!result.success) {
      const errors = result.error.issues.map(issue => ({
        field: issue.path.join('.'),
        message: issue.message,
      }))

      return c.json({
        error: 'Validation failed',
        details: errors,
      }, 400)
    }
  })
}

// Usage
app.post('/users',
  customValidator('json', createUserSchema),
  async (c) => {
    const data = c.req.valid('json')
    return c.json(data)
  }
)
```

### Validation Error Response Format

```typescript
// Standard error format
{
  "error": "Validation failed",
  "details": [
    { "field": "email", "message": "Invalid email address" },
    { "field": "name", "message": "Name is required" }
  ]
}
```

## Multiple Validators

Chain validators for different request parts:

```typescript
app.put('/users/:id',
  zValidator('param', userParamsSchema),
  zValidator('json', updateUserSchema),
  async (c) => {
    const { id } = c.req.valid('param')
    const data = c.req.valid('json')

    return c.json({ id, ...data })
  }
)
```

## Type Export Pattern

```typescript
// validators/user.schema.ts
import { z } from 'zod'

export const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string(),
})

export const updateUserSchema = createUserSchema.partial()

export const userParamsSchema = z.object({
  id: z.string().uuid(),
})

export const userQuerySchema = z.object({
  page: z.coerce.number().default(1),
  limit: z.coerce.number().default(20),
})

// Export inferred types
export type CreateUser = z.infer<typeof createUserSchema>
export type UpdateUser = z.infer<typeof updateUserSchema>
export type UserParams = z.infer<typeof userParamsSchema>
export type UserQuery = z.infer<typeof userQuerySchema>
```

## Best Practices

1. **Always use `zValidator`** for all request inputs
2. **Use `z.coerce`** for query params (they're always strings)
3. **Provide clear error messages** in schema definitions
4. **Export inferred types** for use elsewhere
5. **Create reusable field schemas** for common patterns
6. **Use `.partial()`** for update schemas
7. **Use `.refine()`** for cross-field validation
8. **Set sensible defaults** with `.default()`
