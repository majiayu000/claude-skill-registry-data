---
name: using-runtime-checks
description: Teaches how to validate external data at runtime using Zod and other validation libraries in TypeScript. Use when working with APIs, JSON parsing, user input, or any external data source where runtime validation is needed.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
version: 1.0.0
---

<role>
This skill teaches runtime validation patterns using libraries like Zod to bridge the gap between TypeScript's compile-time types and runtime realities. Critical for preventing runtime errors from unvalidated external data.
</role>

<when-to-activate>
This skill activates when:

- Working with API responses or external data
- Parsing JSON from unknown sources
- Handling user input or form data
- Integrating with third-party services
- User mentions validation, Zod, io-ts, runtime checks, or external data
</when-to-activate>

<overview>
**Critical Insight**: TypeScript types are erased at compile time. At runtime, you have no type safety for external data.

```typescript
const data: User = await fetch("/api/user").then(r => r.json());
```

This compiles, but if the API returns `{ username: string }` instead of `{ name: string }`, your code crashes at runtime.

**Solution**: Runtime validation libraries that:
1. Validate data structure at runtime
2. Provide TypeScript types automatically
3. Generate helpful error messages

**Recommended Library**: Zod (modern, TypeScript-first, best DX)
</overview>

<workflow>
## Runtime Validation Flow

**Step 1: Define Schema**

Create a schema describing the expected shape:
```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().int().positive()
});
```

**Step 2: Extract TypeScript Type**

```typescript
type User = z.infer<typeof UserSchema>;
```

**Step 3: Validate at Runtime**

```typescript
const data = await fetch("/api/user").then(r => r.json());

const result = UserSchema.safeParse(data);

if (result.success) {
  const user: User = result.data;
  console.log(user.name);
} else {
  console.error("Validation failed:", result.error);
}
```

**Step 4: Handle Validation Errors**

```typescript
if (!result.success) {
  const issues = result.error.issues.map(issue => ({
    path: issue.path.join("."),
    message: issue.message
  }));
  throw new ValidationError("Invalid user data", issues);
}
```
</workflow>

<examples>
## Example 1: API Response Validation

**Setup**

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  role: z.enum(["admin", "user", "guest"]),
  createdAt: z.string().datetime()
});

type User = z.infer<typeof UserSchema>;
```

**Validation**

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const data: unknown = await response.json();

  const result = UserSchema.safeParse(data);

  if (!result.success) {
    throw new Error(`Invalid user data: ${result.error.message}`);
  }

  return result.data;
}
```

---

## Example 2: Form Input Validation

```typescript
const LoginFormSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  rememberMe: z.boolean().optional()
});

type LoginForm = z.infer<typeof LoginFormSchema>;

function validateLoginForm(formData: unknown): LoginForm {
  return LoginFormSchema.parse(formData);
}

const form = {
  email: "user@example.com",
  password: "securepassword123"
};

try {
  const validated = validateLoginForm(form);
  await login(validated);
} catch (error) {
  if (error instanceof z.ZodError) {
    error.issues.forEach(issue => {
      console.error(`${issue.path.join(".")}: ${issue.message}`);
    });
  }
}
```

---

## Example 3: Nested Object Validation

```typescript
const AddressSchema = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string().length(2),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/)
});

const UserWithAddressSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  address: AddressSchema,
  billingAddress: AddressSchema.optional()
});

type UserWithAddress = z.infer<typeof UserWithAddressSchema>;
```

---

## Example 4: Array Validation

```typescript
const TagSchema = z.string().min(1).max(20);

const PostSchema = z.object({
  id: z.string(),
  title: z.string().min(1).max(200),
  content: z.string(),
  tags: z.array(TagSchema).min(1).max(10),
  metadata: z.record(z.string(), z.unknown())
});

type Post = z.infer<typeof PostSchema>;

async function fetchPosts(): Promise<Post[]> {
  const response = await fetch("/api/posts");
  const data: unknown = await response.json();

  const PostsSchema = z.array(PostSchema);
  return PostsSchema.parse(data);
}
```

---

## Example 5: Advanced Patterns

**Union Types**: Use discriminated unions for API responses with success/error states.

**Transforms**: Convert strings to dates or coerce query parameters to numbers.

**Refinements**: Add custom validation logic for complex business rules (e.g., password strength).

**Partial Schemas**: Create update schemas from full schemas using `.partial()`.

See `references/zod-patterns.md` for complete examples of unions, transforms, refinements, and partial schemas.
</examples>

<progressive-disclosure>
## Reference Files

For complete patterns see `references/`:

- `references/zod-patterns.md` - Complete Zod API reference
- `references/error-handling.md` - Validation error handling strategies
- `references/performance.md` - Validation performance optimization

For related skills:

- **Type Guards**: Use the using-type-guards skill for manual type narrowing
- **Unknown vs Any**: Use the avoiding-any-types skill for why validation is needed
- **External Data**: Use the validating-external-data skill for specific data source patterns

**Cross-Plugin References:**

- If constructing Zod schemas for runtime validation, use the validating-schema-basics skill for type-safe Zod v4 schema patterns
- If handling validation errors, use the customizing-errors skill for error formatting and custom messages
</progressive-disclosure>

<constraints>
**MUST:**

- Validate all external data at runtime (APIs, JSON, user input)
- Use `safeParse` for error handling, not `parse` (unless throwing is desired)
- Handle validation errors gracefully with user-friendly messages
- Validate before type assertions

**SHOULD:**

- Use Zod for new projects (best TypeScript integration)
- Define schemas close to usage
- Reuse schemas for related structures
- Transform data during validation when beneficial

**NEVER:**

- Trust external data without validation
- Use type assertions (`as Type`) on unvalidated data
- Ignore validation errors
- Validate in multiple places (validate at boundaries)
- Skip validation for "trusted" sources (trust issues change)
</constraints>

<installation>
## Installing Zod

```bash
npm install zod

pnpm add zod

yarn add zod
```

TypeScript configuration:
```json
{
  "compilerOptions": {
    "strict": true
  }
}
```
</installation>

<validation>
## Validation Implementation Checklist

**Schema Definition**: Match expected structure, use appropriate validators, add custom refinements.

**Error Handling**: Use `safeParse`, log errors with context, provide user-friendly messages.

**Type Safety**: Derive types with `z.infer`, avoid manual assertions after validation.

**Performance**: Reuse schemas, validate at boundaries only, avoid redundant checks.

**Testing**: Test valid data, invalid data, and edge cases.

See `references/error-handling.md` for error handling patterns and `references/performance.md` for optimization techniques.
</validation>

<alternatives>
## Other Validation Libraries

**io-ts** (functional programming style)
```typescript
import * as t from "io-ts";

const UserCodec = t.type({
  id: t.string,
  name: t.string,
  email: t.string
});

type User = t.TypeOf<typeof UserCodec>;
```

**Yup** (common with Formik)
```typescript
import * as yup from "yup";

const userSchema = yup.object({
  name: yup.string().required(),
  email: yup.string().email().required()
});
```

**AJV** (JSON Schema)
```typescript
import Ajv from "ajv";

const ajv = new Ajv();
const validate = ajv.compile({
  type: "object",
  properties: {
    name: { type: "string" },
    email: { type: "string", format: "email" }
  },
  required: ["name", "email"]
});
```

**Recommendation**: Use Zod for new TypeScript projects. Best DX and type inference.
</alternatives>

<common-patterns>
## Common Patterns

**Validation Middleware**: Validate request bodies in Express/framework handlers before processing.

**Safe JSON Parse**: Combine JSON.parse with schema validation for type-safe parsing.

**Configuration Validation**: Validate environment variables and config at startup.

See `references/zod-patterns.md` for complete implementations and additional patterns.
</common-patterns>
