---
name: validation-boundary
description: "Validate at the boundary with Zod schemas and branded types. Business functions trust validated input."
version: 1.0.0
libraries: ["zod"]
---

# Validation at the Boundary

## Core Principle

Validation is a **boundary concern**. Check passports once at the border, not at every street corner.

```
External Input (HTTP, CLI, Queue)  <- untrusted
       |
       v
Boundary Layer (validate with Zod) <- reject bad data here
       |
       v
Business Functions fn(args, deps)  <- args ALREADY valid by contract
```

## Parse, Don't Validate

**Validation** checks data and returns true/false.
**Parsing** transforms data into a new, richer type.

```typescript
// Validation mindset: "Is this email valid?"
function isValidEmail(s: string): boolean { ... }

// Parsing mindset: "Give me an Email, or fail"
function parseEmail(s: string): Email { ... }
```

With parsing, you have an `Email` type that CANNOT be invalid by construction.

## Required Behaviors

### 1. Define Schemas with Zod

```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;
```

### 2. Use Branded Types for Stronger Guarantees

```typescript
const EmailSchema = z.string().email().brand<'Email'>();
const UserIdSchema = z.string().uuid().brand<'UserId'>();

type Email = z.infer<typeof EmailSchema>;   // string & { __brand: 'Email' }
type UserId = z.infer<typeof UserIdSchema>; // string & { __brand: 'UserId' }

// Now TypeScript prevents accidental raw strings
function sendEmail(to: Email, subject: string) { ... }

sendEmail("alice@example.com", "Hello");  // ERROR: string not assignable to Email
sendEmail(EmailSchema.parse("alice@example.com"), "Hello");  // OK
```

#### When to Use Branded Types vs Plain Types

| Use Branded Types | Use Plain Types |
|-------------------|-----------------|
| IDs that look alike (`userId`, `orderId`) | Internal-only types |
| Security-sensitive values (tokens, keys) | Simple strings with no confusion risk |
| Values that MUST go through validation | Prototyping / early development |
| Cross-boundary data | Types only used in one function |

**Rule of thumb:** If mixing up two string parameters would cause a bug, brand them.

### 3. Validate at HTTP/Queue/CLI Boundaries

```typescript
app.post('/users', async (req, res) => {
  // 1. Validate at the boundary
  const parsed = CreateUserSchema.safeParse(req.body);

  if (!parsed.success) {
    return res.status(400).json(formatZodError(parsed.error));
  }

  // 2. Call business function with valid, typed data
  const user = await userService.createUser(parsed.data);

  return res.status(201).json(user);
});
```

### 4. Business Functions Trust the Contract

NO validation inside business functions. They trust args are already valid:

```typescript
// CORRECT - No validation, trust the contract
async function createUser(
  args: CreateUserInput,  // Already validated!
  deps: CreateUserDeps
): Promise<User> {
  const user = { id: crypto.randomUUID(), ...args };
  await deps.db.saveUser(user);
  return user;
}

// WRONG - Validation mixed with business logic
async function createUser(args: { name: string; email: string }, deps) {
  if (!args.name || args.name.length < 2) {
    throw new Error('Name must be at least 2 characters');  // DON'T DO THIS
  }
  // ...
}
```

### 5. Standardize Validation Error Responses

```typescript
type ValidationErrorResponse = {
  error: 'VALIDATION_FAILED';
  message: string;
  issues: Array<{
    path: string;
    message: string;
    code: string;
  }>;
};

function formatZodError(error: z.ZodError): ValidationErrorResponse {
  return {
    error: 'VALIDATION_FAILED',
    message: 'Request validation failed',
    issues: error.issues.map(issue => ({
      path: issue.path.join('.'),
      message: issue.message,
      code: issue.code,
    })),
  };
}
```

## Two Layers of Validation

| Type | Where | What | Tool |
|------|-------|------|------|
| **Schema Validation** | Boundary | Shape, types, format, ranges | Zod |
| **Domain Validation** | Business function | Business rules (email exists, has permission) | Database lookups |

```typescript
// Schema validation (boundary)
const TransferSchema = z.object({
  fromAccount: z.string().uuid(),
  toAccount: z.string().uuid(),
  amount: z.number().positive(),
});

// Domain validation (business function)
async function validateTransfer(args: TransferInput, deps: TransferDeps) {
  const account = await deps.db.getAccount(args.fromAccount);
  if (account.balance < args.amount) {
    return err('INSUFFICIENT_FUNDS');  // Business rule, not schema
  }
  // ...
}
```

## Common Patterns

### Coercion (Query Parameters)

```typescript
const PaginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

// "?page=2&limit=50" -> { page: 2, limit: 50 }
```

### Partial Updates (PATCH)

```typescript
const UpdateUserSchema = z.object({
  name: z.string().min(2).optional(),
  email: z.string().email().optional(),
});
```

### Transforms

```typescript
const CreatePostSchema = z.object({
  title: z.string().transform(s => s.trim()),
  slug: z.string().transform(s => s.toLowerCase().replace(/\s+/g, '-')),
});
```

### Express Middleware

```typescript
function validateBody<T>(schema: z.ZodSchema<T>) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);

    if (!result.success) {
      return res.status(400).json(formatZodError(result.error));
    }

    req.body = result.data;
    next();
  };
}

app.post('/users', validateBody(CreateUserSchema), async (req, res) => {
  const user = await userService.createUser(req.body);
  res.status(201).json(user);
});
```

## Quick Reference

| Question | Answer |
|----------|--------|
| Where validate shape/format? | Boundary (Zod schema) |
| Where validate business rules? | Business function |
| Should fn(args, deps) validate args? | NO. Trust the contract |
| Error for invalid input? | HTTP 400 (client error) |
