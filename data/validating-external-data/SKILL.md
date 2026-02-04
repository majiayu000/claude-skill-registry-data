---
name: validating-external-data
description: Validating external data from APIs, JSON parsing, user input, and any untrusted sources in TypeScript applications
---

# Validation: External Data

**Purpose:** Ensure runtime type safety by validating all data from external sources. TypeScript types are compile-time only and erased at runtime.

**When to use:** Any time you receive data from outside your TypeScript code - API responses, JSON files, user input, database queries, environment variables, file uploads, or any external system.

## Critical Understanding

### TypeScript Types Are Compile-Time Only

**This code has NO runtime safety:**

```typescript
interface User {
  id: string;
  email: string;
  age: number;
}

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

**Why it's unsafe:**
- `response.json()` returns `any` (or `unknown` with strict settings)
- Type assertion `as User` doesn't validate data
- If API returns `{ id: 123, email: null, age: "twenty" }`, TypeScript accepts it
- Runtime errors occur when code assumes correct types

**TypeScript types are documentation, not validation.**

### Runtime Validation is Mandatory

**Safe code validates at system boundaries:**

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  age: z.number().int().positive(),
});

type User = z.infer<typeof UserSchema>;

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();

  return UserSchema.parse(data);
}
```

**Now:**
- Data is validated at runtime
- Throws error if data doesn't match schema
- Type safety is guaranteed, not assumed
- TypeScript types match runtime reality

## System Boundaries

**External data enters at these boundaries:**

1. **HTTP APIs** - fetch requests, axios, etc.
2. **WebSocket messages** - real-time data streams
3. **File system** - reading JSON, CSV, or other files
4. **Database queries** - SQL, MongoDB, etc.
5. **Environment variables** - `process.env`
6. **User input** - forms, URL params, file uploads
7. **Third-party libraries** - plugins, SDKs
8. **Message queues** - RabbitMQ, Kafka, etc.

**Validate at every boundary. Never trust external data.**

## Validation with Zod

### Why Zod?

**Advantages:**
- TypeScript-first design
- Infer types from schemas (single source of truth)
- Composable and reusable schemas
- Excellent error messages
- Zero dependencies
- Full support for complex types

**Alternative libraries:**
- `io-ts` - More functional, steeper learning curve
- `yup` - Popular but not TypeScript-native
- `joi` - Older, less TypeScript-friendly
- `ajv` - JSON Schema validator, verbose

**Zod is the best choice for TypeScript projects.**

### Basic Zod Patterns

**Primitives:**

```typescript
import { z } from 'zod';

const stringSchema = z.string();
const numberSchema = z.number();
const booleanSchema = z.boolean();
const dateSchema = z.date();
const nullSchema = z.null();
const undefinedSchema = z.undefined();
```

**Objects:**

```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(100),
  email: z.string().email(),
  age: z.number().int().positive().max(120),
  verified: z.boolean(),
  createdAt: z.string().datetime(),
});

type User = z.infer<typeof UserSchema>;
```

**Arrays:**

```typescript
const UsersSchema = z.array(UserSchema);

type Users = z.infer<typeof UsersSchema>;
```

**Optional fields:**

```typescript
const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  nickname: z.string().optional(),
  age: z.number().nullable(),
});
```

**Default values:**

```typescript
const ConfigSchema = z.object({
  port: z.number().default(3000),
  host: z.string().default('localhost'),
});
```

## API Response Validation

### Basic Fetch Validation

```typescript
const PostSchema = z.object({
  id: z.number(),
  title: z.string(),
  body: z.string(),
  userId: z.number(),
});

type Post = z.infer<typeof PostSchema>;

async function getPost(id: number): Promise<Post> {
  const response = await fetch(
    `https://jsonplaceholder.typicode.com/posts/${id}`
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();

  return PostSchema.parse(data);
}
```

**What this does:**
1. Fetches data from external API
2. Checks HTTP status
3. Parses JSON
4. Validates structure matches schema
5. Returns typed data or throws error

### Handling Validation Errors

```typescript
async function getPost(id: number): Promise<Post | null> {
  try {
    const response = await fetch(
      `https://jsonplaceholder.typicode.com/posts/${id}`
    );

    if (!response.ok) {
      console.error(`HTTP error! status: ${response.status}`);
      return null;
    }

    const data = await response.json();

    return PostSchema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('Validation failed:', error.errors);

      error.errors.forEach((err) => {
        console.error(`${err.path.join('.')}: ${err.message}`);
      });
    } else {
      console.error('Unexpected error:', error);
    }

    return null;
  }
}
```

**ZodError provides detailed information:**
- `error.errors` - Array of validation errors
- `err.path` - Field path that failed
- `err.message` - Human-readable error message
- `err.code` - Error type code

### Safe Parsing (No Throws)

```typescript
async function getPost(id: number): Promise<Post | null> {
  const response = await fetch(
    `https://jsonplaceholder.typicode.com/posts/${id}`
  );

  const data = await response.json();

  const result = PostSchema.safeParse(data);

  if (result.success) {
    return result.data;
  } else {
    console.error('Validation failed:', result.error.errors);
    return null;
  }
}
```

**`safeParse` returns:**
- `{ success: true, data: T }` on success
- `{ success: false, error: ZodError }` on failure

**Use when:**
- You want to handle errors without try/catch
- Multiple validation attempts in a row
- Building type-safe APIs

## Complex Data Structures

### Nested Objects

```typescript
const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  zipCode: z.string().regex(/^\d{5}$/),
  country: z.string().length(2),
});

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  address: AddressSchema,
});
```

### Discriminated Unions

```typescript
const SuccessResponseSchema = z.object({
  status: z.literal('success'),
  data: z.object({
    id: z.string(),
    name: z.string(),
  }),
});

const ErrorResponseSchema = z.object({
  status: z.literal('error'),
  message: z.string(),
  code: z.number(),
});

const APIResponseSchema = z.discriminatedUnion('status', [
  SuccessResponseSchema,
  ErrorResponseSchema,
]);

type APIResponse = z.infer<typeof APIResponseSchema>;

function handleResponse(response: APIResponse) {
  if (response.status === 'success') {
    console.log(response.data.name);
  } else {
    console.error(response.message, response.code);
  }
}
```

### Recursive Schemas

```typescript
type Category = {
  id: string;
  name: string;
  subcategories: Category[];
};

const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    id: z.string(),
    name: z.string(),
    subcategories: z.array(CategorySchema),
  })
);
```

### Transform and Refine

**Transform (convert data):**

```typescript
const TimestampSchema = z.string().transform((str) => new Date(str));
```

**Refine (custom validation):**

```typescript
const PasswordSchema = z
  .string()
  .min(8)
  .refine(
    (password) => /[A-Z]/.test(password),
    { message: 'Must contain uppercase letter' }
  )
  .refine(
    (password) => /[0-9]/.test(password),
    { message: 'Must contain number' }
  );
```

## JSON File Validation

```typescript
import { readFile } from 'fs/promises';
import { z } from 'zod';

const ConfigSchema = z.object({
  database: z.object({
    host: z.string(),
    port: z.number(),
    username: z.string(),
    password: z.string(),
  }),
  server: z.object({
    port: z.number().default(3000),
    host: z.string().default('localhost'),
  }),
});

type Config = z.infer<typeof ConfigSchema>;

async function loadConfig(path: string): Promise<Config> {
  const content = await readFile(path, 'utf-8');
  const data = JSON.parse(content);

  return ConfigSchema.parse(data);
}
```

## Environment Variable Validation

```typescript
const EnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

type Env = z.infer<typeof EnvSchema>;

function validateEnv(): Env {
  const result = EnvSchema.safeParse(process.env);

  if (!result.success) {
    console.error('Invalid environment variables:');
    console.error(result.error.errors);
    process.exit(1);
  }

  return result.data;
}

export const env = validateEnv();
```

**Usage:**

```typescript
import { env } from './env';

const server = app.listen(env.PORT, () => {
  console.log(`Server running on port ${env.PORT}`);
});
```

**Benefits:**
- Type-safe environment access
- Fails fast on startup if misconfigured
- Self-documenting required environment variables
- Coercion handles string-to-number conversion

## Database Query Validation

### Raw SQL Results

```typescript
import { Pool } from 'pg';

const pool = new Pool();

const UserRowSchema = z.object({
  id: z.string(),
  email: z.string(),
  created_at: z.string(),
});

type UserRow = z.infer<typeof UserRowSchema>;

async function getUser(id: string): Promise<UserRow> {
  const result = await pool.query(
    'SELECT id, email, created_at FROM users WHERE id = $1',
    [id]
  );

  if (result.rows.length === 0) {
    throw new Error('User not found');
  }

  return UserRowSchema.parse(result.rows[0]);
}
```

**Database Safety Note:** Use parameterized queries (with `$1`, `$2` placeholders) to prevent SQL injection. For detailed patterns on safe query construction with Prisma, use the preventing-sql-injection skill from prisma-6 for database-specific sanitization patterns.

### MongoDB Results

```typescript
import { MongoClient } from 'mongodb';

const UserDocumentSchema = z.object({
  _id: z.string(),
  email: z.string(),
  name: z.string(),
});

async function getUser(id: string) {
  const client = await MongoClient.connect('mongodb://localhost');
  const db = client.db('myapp');

  const doc = await db.collection('users').findOne({ _id: id });

  if (!doc) {
    throw new Error('User not found');
  }

  return UserDocumentSchema.parse(doc);
}
```

## WebSocket Message Validation

```typescript
import { WebSocket } from 'ws';

const MessageSchema = z.discriminatedUnion('type', [
  z.object({
    type: z.literal('chat'),
    message: z.string(),
    userId: z.string(),
  }),
  z.object({
    type: z.literal('typing'),
    userId: z.string(),
  }),
]);

type Message = z.infer<typeof MessageSchema>;

const ws = new WebSocket('ws://localhost:8080');

ws.on('message', (data) => {
  try {
    const parsed = JSON.parse(data.toString());
    const message = MessageSchema.parse(parsed);

    if (message.type === 'chat') {
      console.log(`${message.userId}: ${message.message}`);
    } else {
      console.log(`${message.userId} is typing...`);
    }
  } catch (error) {
    console.error('Invalid message received:', error);
  }
});
```

## Form Data Validation

### Express/Node.js

```typescript
import express from 'express';
import { z } from 'zod';

const CreateUserSchema = z.object({
  username: z.string().min(3).max(20),
  email: z.string().email(),
  password: z.string().min(12),
});

app.post('/register', async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);

  if (!result.success) {
    res.status(400).json({
      error: 'Validation failed',
      details: result.error.errors,
    });
    return;
  }

  const user = await createUser(result.data);

  res.json({ user });
});
```

### React Forms

```typescript
import { z } from 'zod';
import { useState } from 'react';

const LoginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

function LoginForm() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const data = {
      email: formData.get('email'),
      password: formData.get('password'),
    };

    const result = LoginSchema.safeParse(data);

    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.errors.forEach((err) => {
        const field = err.path[0] as string;
        fieldErrors[field] = err.message;
      });
      setErrors(fieldErrors);
      return;
    }

    await login(result.data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" />
      {errors.email && <span>{errors.email}</span>}

      <input name="password" type="password" />
      {errors.password && <span>{errors.password}</span>}

      <button type="submit">Login</button>
    </form>
  );
}
```

## Performance Considerations

### Caching Schemas

**DON'T recreate schemas on every call:**

```typescript
function validateUser(data: unknown) {
  const schema = z.object({ id: z.string() });
  return schema.parse(data);
}
```

**DO create schemas once:**

```typescript
const UserSchema = z.object({ id: z.string() });

function validateUser(data: unknown) {
  return UserSchema.parse(data);
}
```

### Partial Validation

**Validate only needed fields:**

```typescript
const FullUserSchema = z.object({
  id: z.string(),
  email: z.string(),
  name: z.string(),
  address: z.object({
    street: z.string(),
    city: z.string(),
  }),
});

const UserIdSchema = FullUserSchema.pick({ id: true });
```

## Common Mistakes

### Mistake 1: Type Assertion Instead of Validation

```typescript
const user = (await response.json()) as User;
```

This provides ZERO runtime safety.

### Mistake 2: Validating After Using

```typescript
const data = await response.json();
console.log(data.user.email);

UserSchema.parse(data);
```

Validation must come BEFORE use.

### Mistake 3: Catching and Ignoring Errors

```typescript
try {
  return UserSchema.parse(data);
} catch {
  return {};
}
```

Silently failing validation defeats its purpose.

## Best Practices Checklist

- [ ] Validate all external data at system boundaries
- [ ] Use Zod for type-safe schemas
- [ ] Infer TypeScript types from Zod schemas (`z.infer`)
- [ ] Handle validation errors appropriately
- [ ] Log validation failures for debugging
- [ ] Never use type assertions on unvalidated data
- [ ] Cache schema instances (don't recreate)
- [ ] Validate environment variables on startup
- [ ] Use `safeParse` for non-throwing validation
- [ ] Provide user-friendly error messages

## Related Skills

**Zod v4 Features:**
- If constructing Zod schemas for external data, use the validating-schema-basics skill for type-safe schema patterns and validation best practices
- If validating email, URL, UUID formats, use the validating-string-formats skill for Zod v4 top-level format functions
- If handling validation errors, use the customizing-errors skill for safeParse pattern, error formatting, and user-friendly messages

**Prisma 6 Database Validation:**
- If validating Prisma query results as external data sources with type-safe patterns, use the ensuring-query-type-safety skill from prisma-6 for GetPayload type inference
- If constructing database queries from external data, use the preventing-sql-injection skill from prisma-6 for database-specific sanitization patterns and safe parameterization

## Resources

- [Zod Documentation](https://zod.dev/)
- [TypeScript Handbook: Type Assertions](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)
- [io-ts](https://github.com/gcanti/io-ts) (alternative)

## Summary

**Key Principles:**

1. **TypeScript types are compile-time only** - No runtime enforcement
2. **Validate at system boundaries** - APIs, files, databases, user input
3. **Use Zod for runtime validation** - Type-safe, composable, excellent errors
4. **Fail fast on invalid data** - Don't process bad data
5. **Never trust external data** - Always validate, even from "trusted" sources

**Pattern:**

```typescript
const Schema = z.object({});
type Type = z.infer<typeof Schema>;

function processExternalData(data: unknown): Type {
  return Schema.parse(data);
}
```

This ensures your TypeScript types match runtime reality, preventing the #1 cause of production bugs in TypeScript applications.
