---
name: customizing-errors
description: Handle Zod validation errors with unified error API, custom messages, error formatting, and user-friendly display
---

# Handling Zod Errors

## Purpose

Comprehensive guide to error handling in Zod v4, covering the unified error API, custom error messages, error formatting, and integration with UI frameworks.

## Unified Error API

### Overview

Zod v4 unified all error customization under a single `error` parameter, replacing multiple deprecated parameters.

**v3 (deprecated):**
```typescript
z.string({ message: "Required" });
z.string({ invalid_type_error: "Must be string" });
z.string({ required_error: "Field required" });
z.object({}, { errorMap: customMap });
```

**v4 (unified):**
```typescript
z.string({ error: "Required" });
z.string({ error: "Must be string" });
z.string({ error: "Field required" });
z.object({}, { error: customMap });
```

### Error Parameter Types

**String messages:**
```typescript
z.string({ error: "This field is required" });
z.email({ error: "Please enter a valid email address" });
z.number({ error: "Must be a number" }).min(0, {
  error: "Must be positive"
});
```

**Error map functions:**
```typescript
const customErrorMap: ZodErrorMap = (issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    return { message: `Expected ${issue.expected}, got ${issue.received}` };
  }
  return { message: ctx.defaultError };
};

z.string({ error: customErrorMap });
```

## SafeParse Pattern

### Best Practice

Always use `safeParse` instead of `parse` wrapped in try/catch:

**Anti-pattern:**
```typescript
try {
  const data = schema.parse(input);
  return data;
} catch (error) {
  console.error(error);
  return null;
}
```

**Best practice:**
```typescript
const result = schema.safeParse(input);
if (!result.success) {
  console.error(result.error);
  return null;
}
return result.data;
```

**Benefits:**
- No exception overhead (better performance)
- Type-safe discriminated union
- More readable control flow
- Explicit error handling

### Type Inference

```typescript
const result = schema.safeParse(input);

if (result.success) {
  const data: z.infer<typeof schema> = result.data;
} else {
  const error: z.ZodError = result.error;
}
```

## Error Formatting

### Flatten Errors

Convert nested error structure to flat format:

```typescript
const userSchema = z.object({
  email: z.email(),
  age: z.number().min(18)
});

const result = userSchema.safeParse({
  email: 'invalid',
  age: 10
});

if (!result.success) {
  const flattened = result.error.flatten();
  console.log(flattened.fieldErrors);
}
```

**Output:**
```typescript
{
  email: ["Invalid email"],
  age: ["Number must be greater than or equal to 18"]
}
```

### Format for Forms

**React Hook Form integration:**
```typescript
const result = formSchema.safeParse(data);

if (!result.success) {
  const errors = result.error.flatten().fieldErrors;

  return {
    errors: {
      email: errors.email?.[0],
      password: errors.password?.[0]
    }
  };
}
```

### Format for API Responses

```typescript
const result = schema.safeParse(data);

if (!result.success) {
  return {
    success: false,
    errors: result.error.flatten().fieldErrors
  };
}

return {
  success: true,
  data: result.data
};
```

## Custom Error Messages

### Field-Level Errors

```typescript
const userSchema = z.object({
  email: z.email({
    error: "Please enter a valid email address"
  }),
  password: z.string({
    error: "Password is required"
  }).min(8, {
    error: "Password must be at least 8 characters"
  }),
  age: z.number({
    error: "Age must be a number"
  }).min(18, {
    error: "You must be 18 or older"
  })
});
```

### Refinement Errors

```typescript
const passwordSchema = z.string().refine(
  (password) => /[A-Z]/.test(password),
  { error: "Password must contain at least one uppercase letter" }
).refine(
  (password) => /[0-9]/.test(password),
  { error: "Password must contain at least one number" }
);
```

### Dynamic Error Messages

```typescript
const rangeSchema = (min: number, max: number) =>
  z.number().refine(
    (val) => val >= min && val <= max,
    { error: `Value must be between ${min} and ${max}` }
  );
```

## Error Maps

### Global Error Map

```typescript
import { z } from 'zod';

const customErrorMap: z.ZodErrorMap = (issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    if (issue.expected === 'string') {
      return { message: "This field must be text" };
    }
  }

  if (issue.code === z.ZodIssueCode.too_small) {
    if (issue.type === 'string') {
      return { message: `Minimum ${issue.minimum} characters required` };
    }
  }

  return { message: ctx.defaultError };
};

z.setErrorMap(customErrorMap);
```

### Schema-Specific Error Map

```typescript
const userSchema = z.object({
  email: z.email(),
  age: z.number()
}, {
  error: (issue, ctx) => {
    if (issue.path[0] === 'email') {
      return { message: "Email address is invalid" };
    }
    return { message: ctx.defaultError };
  }
});
```

### Error Code Reference

```typescript
const errorMap: z.ZodErrorMap = (issue, ctx) => {
  switch (issue.code) {
    case z.ZodIssueCode.invalid_type:
      return { message: `Expected ${issue.expected}, got ${issue.received}` };

    case z.ZodIssueCode.invalid_string:
      return { message: "Invalid format" };

    case z.ZodIssueCode.too_small:
      return { message: `Minimum ${issue.minimum} required` };

    case z.ZodIssueCode.too_big:
      return { message: `Maximum ${issue.maximum} allowed` };

    case z.ZodIssueCode.invalid_enum_value:
      return { message: `Must be one of: ${issue.options.join(', ')}` };

    case z.ZodIssueCode.custom:
      return { message: issue.message ?? "Invalid value" };

    default:
      return { message: ctx.defaultError };
  }
};
```

## Error Precedence

Zod v4 error precedence order (highest to lowest):

1. **Schema-level error parameter**
2. **Parse-level error map**
3. **Global error map** (via `z.setErrorMap()`)
4. **Locale error map**
5. **Default Zod errors**

```typescript
z.setErrorMap(globalMap);

const schema = z.string({ error: schemaLevelMap });

const result = schema.safeParse(data, { errorMap: parseLevelMap });
```

## Pretty Print Errors

### Console Output

```typescript
import { z } from 'zod';

const result = schema.safeParse(data);

if (!result.success) {
  console.error(z.prettifyError(result.error));
}
```

### Format Issues

```typescript
const result = schema.safeParse(data);

if (!result.success) {
  result.error.issues.forEach(issue => {
    console.log(`Field: ${issue.path.join('.')}`);
    console.log(`Error: ${issue.message}`);
    console.log(`Code: ${issue.code}`);
  });
}
```

## Framework Integration

Zod integrates seamlessly with popular frameworks for error handling.

**Quick patterns:**
- React Forms: Use `safeParse` + `flatten().fieldErrors`
- React Hook Form: Use `zodResolver` for automatic integration
- Next.js Server Actions: Return flattened errors to client
- Express API: Return 400 status with error details

For framework-specific examples, see the integrating-zod-frameworks skill from the zod-4 plugin.

## Best Practices

### 1. Always Use SafeParse

```typescript
const result = schema.safeParse(data);  // ✅
try { schema.parse(data) }              // ❌
```

### 2. Provide User-Friendly Messages

```typescript
z.email({ error: "Please enter a valid email address" })  // ✅
z.email()                                                  // ❌ Generic error
```

### 3. Flatten for Form Display

```typescript
const errors = result.error.flatten().fieldErrors;  // ✅
const errors = result.error.issues;                 // ❌ Complex structure
```

### 4. Use Error Maps for Consistency

```typescript
z.setErrorMap(customMap);  // ✅ Consistent across app
```

### 5. Test Error Paths

```typescript
it('shows error for invalid email', () => {
  const result = schema.safeParse({ email: 'invalid' });
  expect(result.success).toBe(false);
  if (!result.success) {
    expect(result.error.issues[0].message).toBe("Invalid email");
  }
});
```

## Migration from v3

### Error Parameters

**Before:**
```typescript
z.string({ message: "Required" });
z.string({ invalid_type_error: "Must be string" });
z.string({ required_error: "Required" });
```

**After:**
```typescript
z.string({ error: "Required" });
z.string({ error: "Must be string" });
z.string({ error: "Required" });
```

### Error Maps

**Before:**
```typescript
z.object({}, { errorMap: customMap });
```

**After:**
```typescript
z.object({}, { error: customMap });
```

## Common Patterns

### Nested Object Errors

```typescript
const addressSchema = z.object({
  street: z.string({ error: "Street required" }),
  city: z.string({ error: "City required" }),
  zip: z.string({ error: "ZIP code required" })
});

const userSchema = z.object({
  name: z.string(),
  address: addressSchema
});

const result = userSchema.safeParse(data);
if (!result.success) {
  const errors = result.error.flatten();
}
```

### Array Errors

```typescript
const schema = z.array(
  z.object({
    name: z.string({ error: "Name required" })
  })
);

const result = schema.safeParse(data);
if (!result.success) {
  result.error.issues.forEach(issue => {
    console.log(`Index ${issue.path[0]}: ${issue.message}`);
  });
}
```

### Union Errors

```typescript
const schema = z.union([
  z.string(),
  z.number()
], {
  error: "Must be either string or number"
});
```

## References

- Validation: Use the validating-schema-basics skill from the zod-4 plugin
- v4 Features: Use the validating-string-formats skill from the zod-4 plugin
- Framework integration: Use the integrating-zod-frameworks skill from the zod-4 plugin
- Testing: Use the testing-zod-schemas skill from the zod-4 plugin

**Cross-Plugin References:**

- If displaying validation errors in React forms, use the validating-forms skill for error display patterns

## Success Criteria

- ✅ Using unified `error` parameter
- ✅ SafeParse pattern for error handling
- ✅ User-friendly error messages
- ✅ Flattened errors for form display
- ✅ Error maps for consistency
- ✅ Proper error handling in UI frameworks
- ✅ Test coverage for error paths
