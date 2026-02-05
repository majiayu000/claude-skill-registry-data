---
name: reviewing-patterns
description: Review Zod schemas for correctness, performance, and v4 best practices
review: true
---

# Reviewing Zod Schemas

## Purpose

Comprehensive code review checklist for Zod schemas ensuring v4 compliance, type safety, performance, and maintainability.

## Review Checklist

### 1. API Compatibility

#### Check for Deprecated v3 Patterns

**String format methods:**
```typescript
z.string().email()      // ❌ Deprecated
z.string().uuid()       // ❌ Deprecated
z.string().datetime()   // ❌ Deprecated

z.email()               // ✅ Correct v4
z.uuid()                // ✅ Correct v4
z.iso.datetime()        // ✅ Correct v4
```

**Error customization:**
```typescript
z.string({ message: "Required" })               // ❌ Deprecated
z.string({ invalid_type_error: "Wrong type" })  // ❌ Deprecated
z.string({ required_error: "Missing" })         // ❌ Deprecated

z.string({ error: "Required" })                 // ✅ Correct v4
```

**Schema composition:**
```typescript
schemaA.merge(schemaB)          // ❌ Deprecated
schemaA.extend(schemaB.shape)   // ✅ Correct v4
```

### 2. String Transformations

#### Check for Missing Transformations

**User input should always be trimmed:**
```typescript
z.string()              // ❌ Missing trim
z.string().trim()       // ✅ Correct
```

**Email and username normalization:**
```typescript
z.email()                           // ❌ Missing normalization
z.email().trim().toLowerCase()      // ✅ Correct
```

**Code/identifier normalization:**
```typescript
z.string()                          // ❌ Missing normalization
z.string().trim().toUpperCase()     // ✅ Correct for codes
```

**Manual vs. declarative transformations:**
```typescript
const trimmed = input.trim();
z.string().parse(trimmed);          // ❌ Manual transformation

z.string().trim().parse(input);     // ✅ Declarative
```

### 3. Type Safety

#### Type Inference

**Check proper type extraction:**
```typescript
type User = typeof userSchema;              // ❌ Wrong
type User = z.infer<typeof userSchema>;     // ✅ Correct
```

**Transform pipelines:**
```typescript
const schema = z.string().transform(s => parseInt(s));

type Input = z.input<typeof schema>;    // string
type Output = z.output<typeof schema>;  // number
```

**Branded types for nominal typing:**
```typescript
const userId = z.string();              // ❌ Not branded
const userId = z.string().brand<'UserId'>();  // ✅ Branded
```

### 4. Error Handling

#### Parse vs. SafeParse

**Anti-pattern:**
```typescript
try {
  const data = schema.parse(input);
} catch (error) {
  console.error(error);
}
```

**Best practice:**
```typescript
const result = schema.safeParse(input);
if (!result.success) {
  console.error(result.error.flatten());
  return;
}
const data = result.data;
```

#### Error Messages

**Check for user-friendly errors:**
```typescript
z.string()                              // ❌ Default error
z.string({ error: "Name is required" }) // ✅ Custom error
```

**Complex error maps:**
```typescript
const userSchema = z.object({
  email: z.email({ error: "Please enter a valid email address" }),
  age: z.number({ error: "Age must be a number" }).min(18, {
    error: "Must be 18 or older"
  })
});
```

### 5. Performance

#### Schema Reuse

**Anti-pattern:**
```typescript
function validateUser(data: unknown) {
  const schema = z.object({ email: z.email() });
  return schema.parse(data);
}
```

**Best practice:**
```typescript
const userSchema = z.object({ email: z.email() });

function validateUser(data: unknown) {
  return userSchema.parse(data);
}
```

#### Array Validation

**Anti-pattern:**
```typescript
items.forEach(item => schema.parse(item));
```

**Best practice:**
```typescript
const arraySchema = z.array(schema);
arraySchema.parse(items);
```

Zod v4 bulk validation is 7x faster than item-by-item parsing.

#### Passthrough vs. Strict

**Understand cost implications:**
```typescript
z.object({}).strict()       // Strips unknown keys (cost)
z.object({}).passthrough()  // Keeps unknown keys (faster)
```

Use `.passthrough()` when you don't need to strip unknown properties.

### 6. Schema Design

#### Appropriate Schema Types

**Check for correct schema selection:**
```typescript
z.string().refine(s => s === 'true' || s === 'false')   // ❌ Complex
z.stringbool()                                           // ✅ Built-in v4 type
```

**Union vs. Discriminated Union:**
```typescript
z.union([typeA, typeB])                 // ❌ Slower parsing

z.discriminatedUnion('type', [          // ✅ Faster
  z.object({ type: z.literal('a'), ...typeA }),
  z.object({ type: z.literal('b'), ...typeB })
])
```

**Optional vs. Nullable vs. Nullish:**
```typescript
z.string().optional()       // string | undefined
z.string().nullable()       // string | null
z.string().nullish()        // string | null | undefined
```

Use the most specific type for your use case.

#### Schema Composition

**Extend for adding fields:**
```typescript
const base = z.object({ id: z.string() });
const extended = base.extend({
  name: z.string(),
  email: z.email()
});
```

**Pick/Omit for subsets:**
```typescript
const userSchema = z.object({
  id: z.string(),
  email: z.email(),
  password: z.string()
});

const publicUserSchema = userSchema.omit({ password: true });
const loginSchema = userSchema.pick({ email: true, password: true });
```

### 7. Validation Logic

#### Refinements

**Check refinement usage:**
```typescript
z.string().refine(val => val.length > 5)    // ❌ Missing error

z.string().refine(
  val => val.length > 5,
  { error: "Must be at least 6 characters" }
)                                           // ✅ With error
```

**Async refinements:**
```typescript
z.string().email().refine(
  async (email) => {
    return await checkEmailUnique(email);
  },
  { error: "Email already exists" }
)
```

#### Transformations

**Check transformation order:**
```typescript
z.string().transform(s => s.toUpperCase()).trim()   // ❌ Wrong order
z.string().trim().transform(s => s.toUpperCase())   // ✅ Correct order
```

Transformations run after validation, built-in methods run first.

**Type-safe transformations:**
```typescript
const schema = z.string().transform(s => parseInt(s));

type Output = z.output<typeof schema>;  // number
```

### 8. Security

#### Input Validation

**Check entry point validation:**
```typescript
function handleFormSubmit(formData: FormData) {
  const data = {
    email: formData.get('email'),
    password: formData.get('password')
  };

  const result = loginSchema.safeParse(data);
  if (!result.success) {
    return { errors: result.error };
  }

  await login(result.data);
}
```

**Avoid validation bypass:**
```typescript
function processUser(user: User) {
  await saveToDb(user);
}

processUser({ email: 'test@example.com' });     // ❌ No validation
```

**Always validate at boundaries:**
```typescript
function processUser(data: unknown) {
  const result = userSchema.safeParse(data);
  if (!result.success) throw new Error('Invalid user');

  await saveToDb(result.data);
}
```

#### SQL Injection Prevention

**Zod validates type/shape, NOT malicious content:**
```typescript
z.string()  // Allows: "'; DROP TABLE users; --"
```

**Combine with sanitization:**
```typescript
import { sanitize } from 'sanitization-library';

const schema = z.string().transform(s => sanitize(s));
```

### 9. Testing

#### Schema Tests

**Test valid inputs:**
```typescript
describe('userSchema', () => {
  it('accepts valid user', () => {
    const result = userSchema.safeParse({
      email: 'test@example.com',
      username: 'john'
    });
    expect(result.success).toBe(true);
  });
});
```

**Test invalid inputs:**
```typescript
it('rejects invalid email', () => {
  const result = userSchema.safeParse({
    email: 'not-an-email',
    username: 'john'
  });
  expect(result.success).toBe(false);
  if (!result.success) {
    expect(result.error.issues[0].path).toEqual(['email']);
  }
});
```

**Test transformations:**
```typescript
it('trims and lowercases email', () => {
  const schema = z.email().trim().toLowerCase();
  const result = schema.safeParse('  TEST@EXAMPLE.COM  ');

  expect(result.success).toBe(true);
  if (result.success) {
    expect(result.data).toBe('test@example.com');
  }
});
```

## Review Process

### Step 1: Automated Checks

Run validation skill:
```bash
/review zod-compatibility
```

Checks for:
- Deprecated v3 APIs
- Missing string transformations
- Parse + try/catch anti-patterns

### Step 2: Manual Review

Review each schema for:
1. Appropriate schema types
2. Error message quality
3. Performance optimizations
4. Type safety
5. Security considerations

### Step 3: Test Coverage

Ensure tests cover:
- Valid input scenarios
- Invalid input scenarios
- Edge cases
- Transformation behavior
- Error message correctness

## Common Issues

### Issue 1: Missing Trim on User Input

**Problem:** Whitespace causes validation failures

**Fix:**
```typescript
z.string().min(1)               // ❌ "   " passes
z.string().trim().min(1)        // ✅ "   " fails
```

### Issue 2: Not Using SafeParse

**Problem:** Exceptions for invalid data

**Fix:**
```typescript
try { schema.parse(data) }      // ❌ Exception-based
const result = schema.safeParse(data)  // ✅ Result-based
```

### Issue 3: Schema Defined Inside Function

**Problem:** Schema recreated on every call

**Fix:**
```typescript
function validate(data: unknown) {
  const schema = z.object({...});   // ❌ Recreated
  return schema.parse(data);
}

const schema = z.object({...});     // ✅ Module-level
function validate(data: unknown) {
  return schema.parse(data);
}
```

### Issue 4: Wrong Type Extraction

**Problem:** Using schema type directly

**Fix:**
```typescript
type User = typeof userSchema;          // ❌ ZodObject type
type User = z.infer<typeof userSchema>; // ✅ Inferred type
```

## Integration with Review Plugin

This skill integrates with the review plugin via `review: true` frontmatter.

Invoke with:
```bash
/review zod
```

Or explicitly:
```bash
/review zod-schemas
```

## References

- Compatibility validation: Use the validating-schema-basics skill from the zod-4 plugin
- v4 Features: Use the validating-string-formats skill from the zod-4 plugin
- Error handling: Use the customizing-errors skill from the zod-4 plugin
- Performance: Use the optimizing-performance skill from the zod-4 plugin
- Testing: Use the testing-zod-schemas skill from the zod-4 plugin

**Cross-Plugin References:**

- If reviewing TypeScript type safety alongside Zod schemas, use the reviewing-type-safety skill for comprehensive type validation patterns
- If reviewing security concerns, use the reviewing-security skill for automated vulnerability scanning patterns

## Success Criteria

- ✅ No deprecated v3 APIs
- ✅ String transformations used appropriately
- ✅ safeParse pattern for error handling
- ✅ Schema defined at module level
- ✅ User-friendly error messages
- ✅ Type inference correct
- ✅ Comprehensive test coverage
- ✅ Security validated at entry points
