---
name: zod-v4
description: Expert guidance on Zod v4 validation library including breaking changes from v3, migration patterns, core API usage, and common validation patterns. Use when working with Zod schemas, validation, type inference, or migrating from Zod v3.
---

# Zod v4 Expert Guidance

## Overview

This skill provides comprehensive guidance on using Zod v4, TypeScript's leading validation library. It covers breaking changes from v3, migration patterns, core API usage, and real-world validation patterns.

## When to Use This Skill

Use this skill when:

- Writing validation schemas with Zod v4
- Migrating code from Zod v3 to v4
- Implementing form validation, API response validation, or config validation
- Working with TypeScript type inference from Zod schemas
- Debugging Zod validation errors
- Designing type-safe data models
- Creating recursive or complex nested schemas

## Quick Reference

| Task                    | Reference Document                                                 |
| ----------------------- | ------------------------------------------------------------------ |
| Migrating from Zod v3   | [references/migration-from-v3.md](references/migration-from-v3.md) |
| Core API and primitives | [references/core-api.md](references/core-api.md)                   |
| Real-world patterns     | [references/common-patterns.md](references/common-patterns.md)     |

## Key Breaking Changes in v4

**CRITICAL:** Always review these when working with Zod v4:

1. **Error customization**: Use `error` parameter instead of `message`, `invalid_type_error`, `required_error`
2. **String formats**: Moved to top-level functions (e.g., `z.email()` not `z.string().email()`)
3. **Function schemas**: Completely redesigned API using `z.function({ input, output }).implement()`
4. **Error handling**: Use `.issues` instead of `.errors`, `z.treeifyError()` for formatting
5. **Object methods**: Use `z.strictObject()` and `z.looseObject()` instead of `.strict()` and `.passthrough()`
6. **Extending schemas**: Use shape spreading (`z.object({ ...Base.shape, ... })`) instead of `.merge()` or `.extend()`
7. **Records**: Must specify both key and value schemas: `z.record(keySchema, valueSchema)`
8. **Defaults in optional fields**: Now apply even inside optional fields (behavioral change)
9. **Number validation**: Infinity rejected by default, `.int()` enforces safe range

See [references/migration-from-v3.md](references/migration-from-v3.md) for complete migration guide.

## Common Patterns

### Basic Validation

```typescript
import { z } from 'zod/v4';

// Simple schema
const userSchema = z.object({
  name: z.string().min(1),
  email: z.email(),
  age: z.number().int().positive(),
});

// Parse with error handling
const result = userSchema.safeParse(data);
if (!result.success) {
  console.error(result.error.issues);
}
```

### Type Inference

```typescript
// Automatically infer TypeScript type from schema
type User = z.infer<typeof userSchema>;
// { name: string; email: string; age: number }
```

### Custom Validation

```typescript
const passwordSchema = z
  .string()
  .min(8, { error: 'Password must be at least 8 characters' })
  .regex(/[A-Z]/, { error: 'Must contain uppercase letter' })
  .regex(/[0-9]/, { error: 'Must contain number' });
```

## Best Practices

1. **Always use `.safeParse()` for user input** - Never let validation errors crash your app
2. **Leverage type inference** - Don't manually type what Zod can infer
3. **Use top-level format validators** - `z.email()` not `z.string().email()` (v4 pattern)
4. **Prefer `z.strictObject()`** - Catch typos and unexpected fields
5. **Keep refinements simple** - Complex business logic should be separate
6. **Reuse schemas** - Define once, reference everywhere
7. **Document complex schemas** - Use TypeScript JSDoc comments

## Workflow

When working with Zod:

1. **Define schemas** - Start with the shape of your data
2. **Add validations** - Layer on constraints (min, max, regex, etc.)
3. **Add custom errors** - Make validation messages user-friendly
4. **Infer types** - Use `z.infer<typeof schema>` for TypeScript types
5. **Parse safely** - Use `.safeParse()` and handle errors gracefully
6. **Test edge cases** - Validate your validation logic

## Resources

- **Migration Guide**: [references/migration-from-v3.md](references/migration-from-v3.md)
- **Core API Reference**: [references/core-api.md](references/core-api.md)
- **Common Patterns**: [references/common-patterns.md](references/common-patterns.md)
- **Official Docs**: https://zod.dev/v4

---

## Custom Instructions

<!--
USER: Add your own custom directions and information below this line.
You can include:
- Project-specific validation patterns
- Team conventions for error messages
- Custom schema factories or utilities
- Integration patterns with your stack (React Hook Form, tRPC, etc.)
- Common gotchas specific to your codebase
-->
