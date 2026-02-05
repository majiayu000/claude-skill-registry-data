---
name: zod
description: |
  Zod schema validation and TypeScript integration for runtime type safety.
  Use when: Validating API payloads, form inputs, environment variables, or any external data boundaries where TypeScript types alone cannot guarantee safety.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Zod Skill

Runtime validation library for TypeScript. Use at system boundaries where data enters your application: API responses, form inputs, environment variables, URL params, localStorage. TypeScript types disappear at runtime—Zod provides the actual validation.

## Quick Start

### Installation

```bash
# Frontend
cd frontend && npm install zod @hookform/resolvers

# Backend
cd backend && npm install zod
```

### Basic Schema

```typescript
import { z } from 'zod';

// Define schema
const ProductSchema = z.object({
  id: z.number(),
  name: z.string().min(1),
  price: z.number().positive(),
  salePrice: z.number().positive().nullable(),
  categories: z.array(z.string()),
  isNew: z.boolean().default(false),
});

// Infer TypeScript type from schema
type Product = z.infer<typeof ProductSchema>;

// Validate data
const product = ProductSchema.parse(apiResponse); // throws on invalid
const result = ProductSchema.safeParse(data);     // returns { success, data/error }
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `.parse()` | Throws ZodError on failure | `schema.parse(data)` |
| `.safeParse()` | Returns result object | `{ success: boolean, data?, error? }` |
| `z.infer<>` | Extract TS type from schema | `type User = z.infer<typeof UserSchema>` |
| `.transform()` | Modify value after validation | `.transform(s => s.toLowerCase())` |
| `.refine()` | Custom validation logic | `.refine(n => n % 2 === 0, 'Must be even')` |

## Common Patterns

### Environment Variables

Replace the current manual validation in `backend/src/config/env.ts`:

```typescript
import { z } from 'zod';

const envSchema = z.object({
  PORT: z.coerce.number().default(4000),
  DB_HOST: z.string().default('localhost'),
  DB_PORT: z.coerce.number().default(5432),
  DB_NAME: z.string().default('luxia'),
  DB_USER: z.string().default('postgres'),
  DB_PASSWORD: z.string().min(1, 'DB_PASSWORD is required'),
  JWT_SECRET: z.string().min(32, 'JWT_SECRET must be at least 32 chars'),
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
});

export const env = envSchema.parse(process.env);
```

### Form Validation with react-hook-form

```typescript
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const checkoutSchema = z.object({
  name: z.string().min(2, 'Name is too short'),
  email: z.string().email('Invalid email'),
  phone: z.string().optional(),
  address: z.string().min(10, 'Address is required'),
});

type CheckoutForm = z.infer<typeof checkoutSchema>;

const { register, handleSubmit, formState: { errors } } = useForm<CheckoutForm>({
  resolver: zodResolver(checkoutSchema),
});
```

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **react-hook-form** skill for form integration
- See the **typescript** skill for type inference patterns
- See the **express** skill for API validation
- See the **tanstack-query** skill for API response validation