---
name: migrating-v3-to-v4
description: Complete migration guide from Zod v3 to v4 covering all breaking changes and upgrade patterns
---

# Migrating to Zod v4

## Purpose

Comprehensive guide for migrating existing Zod v3 codebases to v4, covering all breaking changes, migration patterns, and testing strategies.

## Migration Overview

Zod v4 introduced major performance improvements and API refinements:

- **100x reduction** in TypeScript instantiations
- **14x faster** string parsing
- **57% smaller** bundle size
- Simplified API surface with consistent patterns

Breaking changes are intentional improvements that require code updates.

## Breaking Changes

### 1. String Format Methods → Top-Level Functions

**Impact:** Affects ~90% of Zod users using email/uuid/url validation

**Before (v3):**
```typescript
const emailSchema = z.string().email();
const uuidSchema = z.string().uuid();
const datetimeSchema = z.string().datetime();
const urlSchema = z.string().url();
const ipSchema = z.string().ipv4();
const jwtSchema = z.string().jwt();
```

**After (v4):**
```typescript
const emailSchema = z.email();
const uuidSchema = z.uuid();
const datetimeSchema = z.iso.datetime();
const urlSchema = z.url();
const ipSchema = z.ipv4();
const jwtSchema = z.jwt();
```

**Migration script:**
```bash
find ./src -name "*.ts" -o -name "*.tsx" | xargs sed -i '' \
  -e 's/z\.string()\.email()/z.email()/g' \
  -e 's/z\.string()\.uuid()/z.uuid()/g' \
  -e 's/z\.string()\.datetime()/z.iso.datetime()/g' \
  -e 's/z\.string()\.url()/z.url()/g' \
  -e 's/z\.string()\.ipv4()/z.ipv4()/g' \
  -e 's/z\.string()\.ipv6()/z.ipv6()/g' \
  -e 's/z\.string()\.jwt()/z.jwt()/g' \
  -e 's/z\.string()\.base64()/z.base64()/g'
```

### 2. Error Customization → Unified `error` Parameter

**Impact:** Affects error handling and user-facing validation messages

**Before (v3):**
```typescript
z.string({ message: "Required field" });
z.string({ invalid_type_error: "Must be a string" });
z.string({ required_error: "This field is required" });
z.object({}, { errorMap: customErrorMap });
```

**After (v4):**
```typescript
z.string({ error: "Required field" });
z.string({ error: "Must be a string" });
z.string({ error: "This field is required" });
z.object({}, { error: customErrorMap });
```

**Migration pattern:**
All error-related parameters now use single `error` field that accepts strings or error map functions.

### 3. Schema Merge → Extend

**Impact:** Affects schema composition patterns

**Before (v3):**
```typescript
const baseSchema = z.object({ id: z.string() });
const extendedSchema = baseSchema.merge(
  z.object({ name: z.string() })
);
```

**After (v4):**
```typescript
const baseSchema = z.object({ id: z.string() });
const extendedSchema = baseSchema.extend({
  name: z.string()
});
```

**Migration script:**
```bash
find ./src -name "*.ts" | xargs sed -i '' \
  -e 's/\.merge(z\.object(\([^)]*\)))/\.extend(\1)/g'
```

### 4. Refinements → New Architecture

**Impact:** Custom validation logic and error messages

**Before (v3):**
```typescript
z.string().refine((val) => val.length > 5, {
  message: "Too short"
});
```

**After (v4):**
```typescript
z.string().refine((val) => val.length > 5, {
  error: "Too short"
});
```

Error customization in refinements also uses unified `error` parameter.

### 5. String Transformations (New in v4)

**Not a breaking change, but highly recommended:**

**Before (v3 pattern):**
```typescript
const schema = z.string();
const result = schema.parse(input.trim().toLowerCase());
```

**After (v4 recommended):**
```typescript
const schema = z.string().trim().toLowerCase();
const result = schema.parse(input);
```

Benefits:
- Declarative transformation pipeline
- Type-safe and composable
- Better error messages
- Automatic type inference

## Migration Process

### Step 1: Upgrade Package

```bash
npm install zod@^4.0.0
```

Or with specific version:
```bash
npm install zod@4.0.0
```

### Step 2: Run Compatibility Check

Use validation skill to identify deprecated patterns:

```bash
/review zod-compatibility
```

Or manually scan:
```bash
grep -r "z\.string()\.email(" ./src
grep -r "z\.string()\.uuid(" ./src
grep -r "\.merge(" ./src
grep -r "message:" ./src | grep -v "error:"
```

### Step 3: Apply Automated Migrations

Run migration scripts:

```bash
./migrate-string-formats.sh
./migrate-error-params.sh
./migrate-merge-to-extend.sh
```

### Step 4: Handle Manual Migrations

Some patterns require manual review:

**Complex error maps:**
```typescript
const customErrorMap: ZodErrorMap = (issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    return { message: "Invalid type!" };
  }
  return { message: ctx.defaultError };
};

z.string({ errorMap: customErrorMap });
```

**Migration:**
```typescript
const customErrorMap: ZodErrorMap = (issue, ctx) => {
  if (issue.code === z.ZodIssueCode.invalid_type) {
    return { message: "Invalid type!" };
  }
  return { message: ctx.defaultError };
};

z.string({ error: customErrorMap });
```

**Nested schema merges:**
```typescript
const a = z.object({ x: z.string() });
const b = z.object({ y: z.number() });
const c = a.merge(b);
```

**Migration:**
```typescript
const a = z.object({ x: z.string() });
const b = z.object({ y: z.number() });
const c = a.extend({ y: z.number() });
```

### Step 5: Add String Transformations

Identify manual string operations and migrate to built-in methods:

**Before:**
```typescript
const emailSchema = z.email();
const processEmail = (input: string) => {
  const trimmed = input.trim().toLowerCase();
  return emailSchema.parse(trimmed);
};
```

**After:**
```typescript
const emailSchema = z.email().trim().toLowerCase();
const processEmail = (input: string) => {
  return emailSchema.parse(input);
};
```

### Step 6: Run Tests

Comprehensive test suite after migration:

```bash
npm test
```

Check for:
- Schema validation logic still works
- Error messages display correctly
- Type inference remains correct
- No runtime errors from API changes

### Step 7: Update Documentation

Update code comments and docs referencing Zod APIs:
- Remove references to deprecated methods
- Update examples to v4 patterns
- Document new string transformation methods

## Common Migration Issues

### Issue 1: Type Errors After String Format Migration

**Problem:**
```typescript
const emailSchema = z.string().email();
type Email = z.infer<typeof emailSchema>;
```

After migration:
```typescript
const emailSchema = z.email();
type Email = z.infer<typeof emailSchema>;
```

**Solution:** Type inference still works, but type is now more specific to email strings.

### Issue 2: Custom Error Maps Not Working

**Problem:** Error map using old parameter names

**Solution:** Update error map to use unified `error` parameter and ensure function signature matches ZodErrorMap type.

### Issue 3: Merge Breaking Complex Compositions

**Problem:** Nested merges don't translate directly to extend

**Solution:** Use multiple extend calls or restructure schema:
```typescript
const result = base.extend(ext1.shape).extend(ext2.shape);
```

### Issue 4: Tests Fail with Different Error Messages

**Problem:** v4 error messages may differ from v3

**Solution:** Update test assertions to match new error format or use error codes instead of messages:
```typescript
expect(result.error.issues[0].code).toBe(z.ZodIssueCode.invalid_type);
```

## Testing Strategy

### Unit Tests

Test schema validation logic:

```typescript
import { z } from 'zod';

describe('User schema validation', () => {
  const userSchema = z.object({
    email: z.email().trim().toLowerCase(),
    username: z.string().trim().min(3)
  });

  it('validates correct user data', () => {
    const result = userSchema.safeParse({
      email: '  USER@EXAMPLE.COM  ',
      username: '  john  '
    });

    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.email).toBe('user@example.com');
      expect(result.data.username).toBe('john');
    }
  });

  it('rejects invalid email', () => {
    const result = userSchema.safeParse({
      email: 'not-an-email',
      username: 'john'
    });

    expect(result.success).toBe(false);
  });
});
```

### Integration Tests

Test form validation with transformed data:

```typescript
const formSchema = z.object({
  email: z.email().trim().toLowerCase(),
  password: z.string().min(8)
});

const handleSubmit = async (formData: FormData) => {
  const result = formSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password')
  });

  if (!result.success) {
    return { errors: result.error.flatten() };
  }

  await createUser(result.data);
};
```

### Type Tests

Verify type inference works correctly:

```typescript
const schema = z.email().trim();
type Email = z.infer<typeof schema>;

const email: Email = 'test@example.com';
```

## Migration Checklist

- [ ] Upgrade Zod package to v4
- [ ] Run compatibility validation
- [ ] Migrate string format methods to top-level functions
- [ ] Update error customization to use `error` parameter
- [ ] Replace `.merge()` with `.extend()`
- [ ] Add string transformations where applicable
- [ ] Update error maps and refinements
- [ ] Run full test suite
- [ ] Update documentation and examples
- [ ] Review type inference correctness
- [ ] Test error handling in production-like scenarios
- [ ] Update CI/CD pipelines if needed

## Performance Gains

After migration, expect:

- **Faster TypeScript compilation** - 100x reduction in type instantiations
- **Faster runtime parsing** - 14x improvement for string validation
- **Smaller bundle size** - 57% reduction
- **Better error messages** - Clearer validation feedback

Monitor performance improvements:
```bash
npm run build -- --stats
```

Compare bundle size before/after migration.

## References

- Validation skill: Use the validating-schema-basics skill from the zod-4 plugin
- v4 Features: Use the validating-string-formats skill from the zod-4 plugin
- Error handling: Use the customizing-errors skill from the zod-4 plugin

## Success Criteria

- ✅ All v3 deprecated APIs replaced with v4 equivalents
- ✅ Tests pass with 100% success rate
- ✅ No TypeScript compilation errors
- ✅ Error messages display correctly in UI
- ✅ Type inference works as expected
- ✅ Performance improvements measurable
- ✅ Documentation updated to reflect v4 patterns
