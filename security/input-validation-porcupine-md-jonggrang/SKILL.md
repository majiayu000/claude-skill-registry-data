---
name: input-validation
description: Validate and sanitize all API inputs. Zod schemas, error responses, security considerations.
type: pattern
tier: library
domains: [api, security]
trigger: "validation, sanitize, input, zod, schema, request body, query params"
---

## Validate Everything from External Sources

```typescript
// Every request body, query param, and path param is untrusted input.
// Validate at the boundary before it touches your domain logic.
```

## Zod Schema Patterns

```typescript
import { z } from 'zod';

// Base schemas (reusable)
const EmailSchema = z.string().email().max(255).toLowerCase().trim();
const PasswordSchema = z.string().min(8).max(128);
const UUIDSchema = z.string().uuid();

// Request body schema
const CreateUserSchema = z.object({
  email: EmailSchema,
  password: PasswordSchema,
  name: z.string().min(1).max(100).trim(),
  role: z.enum(['admin', 'user', 'viewer']).default('user'),
});

// Query params (all strings from URL, need coercion)
const PaginationSchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sortBy: z.enum(['createdAt', 'name', 'email']).default('createdAt'),
  sortDir: z.enum(['asc', 'desc']).default('desc'),
});

// Path params
const UserParamsSchema = z.object({
  id: UUIDSchema,
});
```

## Middleware Approach (Express)

```typescript
// Generic validation middleware
function validate<T extends z.ZodType>(schema: T, source: 'body' | 'query' | 'params') {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req[source]);
    if (!result.success) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid input',
          fields: result.error.flatten().fieldErrors,
        },
      });
    }
    req[source] = result.data;  // replace with parsed/coerced data
    next();
  };
}

// Usage
router.post('/users',
  validate(CreateUserSchema, 'body'),
  asyncHandler(async (req, res) => {
    const { email, password, name, role } = req.body; // already validated
    const user = await userService.create({ email, password, name, role });
    res.status(201).json(user);
  })
);
```

## Security Checklist

```typescript
// ✓ Strip unknown fields (Zod does this by default with .strip())
const SafeSchema = z.object({ name: z.string() }).strip();
const result = SafeSchema.parse({ name: 'Alice', __proto__: 'polluted' });
// result = { name: 'Alice' } — __proto__ stripped

// ✓ Max length on all strings (prevents DoS)
z.string().max(1000)

// ✓ Sanitize HTML if storing user content
import DOMPurify from 'isomorphic-dompurify';
const safe = DOMPurify.sanitize(userInput);

// ✓ Never trust client-supplied IDs for ownership
// BAD: trusts client's userId
await db.post.delete({ where: { id: body.postId, authorId: body.userId } });
// GOOD: uses authenticated user's ID
await db.post.delete({ where: { id: body.postId, authorId: req.user.id } });
```

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "fields": {
      "email": ["Invalid email address"],
      "password": ["String must contain at least 8 character(s)"]
    }
  }
}
```

Always return field-level errors so clients can show inline validation.
