---
name: integrating-zod-frameworks
description: Integrate Zod v4 with React Hook Form, Next.js, Express, tRPC, and other frameworks for type-safe validation
---

# Integrating Zod with Frameworks

## Purpose

Comprehensive guide to integrating Zod v4 validation with popular frameworks including React Hook Form, Next.js Server Actions, Express APIs, tRPC, and more.

## Supported Frameworks

Zod integrates seamlessly with:

**Frontend Frameworks:**
- React Hook Form - Automatic validation with `zodResolver`
- Next.js Server Actions - Type-safe form validation
- React Query - Mutation input validation

**Backend Frameworks:**
- Express - Middleware validation for REST APIs
- Fastify - Pre-handler validation
- tRPC - End-to-end type safety with `.input()`
- GraphQL (Pothos) - Schema validation plugin

**Database/ORM:**
- Prisma - If validating Prisma query inputs with Zod schemas matching Prisma model types, use the validating-query-inputs skill from prisma-6 for comprehensive schema patterns with type inference.

## Quick Start Patterns

### React Hook Form

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const formSchema = z.object({
  email: z.email().trim().toLowerCase(),
  password: z.string().min(8)
});

type FormData = z.infer<typeof formSchema>;

function Form() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(formSchema)
  });

  return (
    <form onSubmit={handleSubmit(data => console.log(data))}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      <button type="submit">Submit</button>
    </form>
  );
}
```

### Next.js Server Actions

```typescript
'use server';

const schema = z.object({
  email: z.email().trim().toLowerCase()
});

export async function createUser(formData: FormData) {
  const result = schema.safeParse({
    email: formData.get('email')
  });

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  return { data: await db.create(result.data) };
}
```

### Express Middleware

```typescript
import express from 'express';

function validate<T extends z.ZodTypeAny>(schema: T) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ error: result.error.flatten() });
    }
    req.body = result.data;
    next();
  };
}

const userSchema = z.object({ email: z.email() });

app.post('/users', validate(userSchema), async (req, res) => {
  const user = await createUser(req.body);
  res.json(user);
});
```

### tRPC

```typescript
import { initTRPC } from '@trpc/server';

const t = initTRPC.create();

const createUserInput = z.object({
  email: z.email().trim().toLowerCase(),
  name: z.string().trim().min(1)
});

export const appRouter = t.router({
  createUser: t.procedure
    .input(createUserInput)
    .mutation(async ({ input }) => {
      return await db.users.create({ data: input });
    })
});
```

## Best Practices

### 1. Define Schemas at Module Level

```typescript
const schema = z.object({...});  // ✅ Reusable

function handler() {
  const schema = z.object({...});  // ❌ Recreated
}
```

### 2. Use Type Inference

```typescript
type FormData = z.infer<typeof formSchema>;  // ✅
interface FormData { ... }  // ❌ Duplicates schema
```

### 3. Transform User Input

```typescript
z.email().trim().toLowerCase()  // ✅ Normalize
z.email()  // ❌ No normalization
```

### 4. Use SafeParse for User Input

```typescript
const result = schema.safeParse(userInput);  // ✅
try { schema.parse(userInput) }  // ❌
```

### 5. Provide User-Friendly Errors

```typescript
z.email({ error: "Invalid email" })  // ✅
z.email()  // ❌ Generic error
```

### 6. Validate at Boundaries

```typescript
export async function createUser(data: unknown) {
  const validated = schema.parse(data);  // ✅
}

export async function createUser(data: User) {
  await db.create(data);  // ❌ No validation
}
```

## Framework-Specific Tips

### React Hook Form

- Use `zodResolver` for automatic integration
- Use `valueAsNumber` for number inputs
- Define schemas at module level for performance

### Next.js

- Validate in Server Actions with `safeParse`
- Use `z.stringbool()` for checkbox values
- Return flattened errors for form display

### Express

- Create reusable validation middleware
- Validate body, query, and params separately
- Return 400 status for validation errors

### tRPC

- Use `.input()` with Zod schemas
- Type inference automatic across client/server
- Validation happens before procedure execution

### GraphQL

- Use Pothos validation plugin
- Schema validation runs before resolvers
- Consistent error format

## References

- v4 Features: Use the validating-string-formats skill from the zod-4 plugin
- Error handling: Use the customizing-errors skill from the zod-4 plugin
- Testing: Use the testing-zod-schemas skill from the zod-4 plugin
- Transformations: Use the transforming-string-methods skill from the zod-4 plugin

**Cross-Plugin References:**

**React 19 Integration:**
- If implementing comprehensive form validation, use the validating-forms skill for client and server validation strategies
- If implementing Server Actions, use the implementing-server-actions skill for async server function patterns with Zod

**Next.js 16 Integration:**
- If securing Server Actions, use the securing-server-actions skill for authentication and input validation patterns

**Prisma 6 Integration:**
- If validating Prisma query inputs with Zod, use the validating-query-inputs skill from prisma-6 for complete validation pipeline patterns: External Input → Zod Validation → Prisma Operation

## Success Criteria

- ✅ Schemas integrated with framework validation
- ✅ Type inference working across boundaries
- ✅ User-friendly error messages in UI
- ✅ SafeParse for user input validation
- ✅ String transformations applied
- ✅ Validation at entry points
- ✅ Reusable validation patterns
