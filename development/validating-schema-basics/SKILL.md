---
name: validating-schema-basics
description: Validate code for Zod v4 compatibility by detecting deprecated APIs and ensuring adherence to v4 patterns
---

# Validating Zod v4 Compatibility

## Purpose

This skill helps identify and fix deprecated Zod v3 patterns that are incompatible with v4, ensuring code uses current APIs and avoiding future breaking changes.

## Problem

Zod v4 introduced breaking changes that make v3 code non-functional or deprecated:

1. **String format methods moved to top-level functions** - Most common breaking change
2. **Error customization API unified** - Old parameters deprecated
3. **Merge method removed** - Must use extend instead
4. **Refinement architecture changed** - Different error handling

Code using deprecated patterns will break in future Zod releases.

## Validation Checks

### 1. Deprecated String Format Methods

**Anti-pattern:**
```typescript
const emailSchema = z.string().email();
const uuidSchema = z.string().uuid();
const datetimeSchema = z.string().datetime();
const urlSchema = z.string().url();
```

**Correct v4 pattern:**
```typescript
const emailSchema = z.email();
const uuidSchema = z.uuid();
const datetimeSchema = z.iso.datetime();
const urlSchema = z.url();
```

**Detection pattern:**
```bash
grep -n "z\.string()\.email(" file.ts
grep -n "z\.string()\.uuid(" file.ts
grep -n "z\.string()\.datetime(" file.ts
```

### 2. Deprecated Error Customization

**Anti-pattern:**
```typescript
z.string({ message: "Required" });
z.string({ invalid_type_error: "Must be string" });
z.string({ required_error: "Field required" });
z.object({}, { errorMap: customErrorMap });
```

**Correct v4 pattern:**
```typescript
z.string({ error: "Required" });
z.string({ error: "Must be string" });
z.string({ error: "Field required" });
z.object({}, { error: customErrorMap });
```

**Detection pattern:**
```bash
grep -n "message:" file.ts | grep -v "error:"
grep -n "invalid_type_error:" file.ts
grep -n "required_error:" file.ts
grep -n "errorMap:" file.ts
```

### 3. Deprecated Merge Method

**Anti-pattern:**
```typescript
const combined = schemaA.merge(schemaB);
```

**Correct v4 pattern:**
```typescript
const combined = schemaA.extend(schemaB.shape);
```

**Detection pattern:**
```bash
grep -n "\.merge(" file.ts
```

### 4. Missing String Transformations

**Anti-pattern:**
```typescript
const trimmed = input.trim();
const validated = z.string().parse(trimmed);
```

**Correct v4 pattern:**
```typescript
const validated = z.string().trim().parse(input);
```

**Detection pattern:**
Check for manual trim/toLowerCase/toUpperCase before validation.

## Validation Process

### Step 1: Scan for Deprecated APIs

Run pattern matching across TypeScript files:

```bash
find . -name "*.ts" -o -name "*.tsx" | while read file; do
  if grep -q "from ['\"]zod['\"]" "$file"; then
    echo "Checking: $file"

    grep -n "z\.string()\.email(" "$file" && echo "  ❌ Use z.email()"
    grep -n "z\.string()\.uuid(" "$file" && echo "  ❌ Use z.uuid()"
    grep -n "z\.string()\.datetime(" "$file" && echo "  ❌ Use z.iso.datetime()"
    grep -n "\.merge(" "$file" && echo "  ❌ Use .extend()"
    grep -n "message:" "$file" | grep -v "error:" && echo "  ❌ Use error parameter"
  fi
done
```

### Step 2: Check Package Dependencies

Ensure Zod v4 installed:

```bash
grep "\"zod\"" package.json
```

Should show `"zod": "^4.0.0"` or higher.

### Step 3: Review Type Inference

Verify type extraction uses correct syntax:

```typescript
type User = z.infer<typeof userSchema>;
type UserInput = z.input<typeof userSchema>;
type UserOutput = z.output<typeof userSchema>;
```

### Step 4: Validate Error Handling

Check safeParse pattern usage:

```typescript
const result = schema.safeParse(data);
if (!result.success) {
  console.error(result.error.flatten());
  return;
}
const validData = result.data;
```

## Common Migration Patterns

### String Formats

| v3 Pattern | v4 Pattern |
|------------|------------|
| `z.string().email()` | `z.email()` |
| `z.string().uuid()` | `z.uuid()` |
| `z.string().datetime()` | `z.iso.datetime()` |
| `z.string().url()` | `z.url()` |
| `z.string().ipv4()` | `z.ipv4()` |
| `z.string().jwt()` | `z.jwt()` |
| `z.string().base64()` | `z.base64()` |

### Error Customization

| v3 Pattern | v4 Pattern |
|------------|------------|
| `{ message: "..." }` | `{ error: "..." }` |
| `{ invalid_type_error: "..." }` | `{ error: "..." }` |
| `{ required_error: "..." }` | `{ error: "..." }` |
| `{ errorMap: fn }` | `{ error: fn }` |

### Schema Composition

| v3 Pattern | v4 Pattern |
|------------|------------|
| `a.merge(b)` | `a.extend(b.shape)` |
| `z.intersection(a, b)` | `a.and(b)` |
| `z.union([a, b])` | `z.union([a, b])` (unchanged) |

## Remediation Steps

### 1. Update String Formats

Find and replace:
```bash
sed -i '' 's/z\.string()\.email()/z.email()/g' file.ts
sed -i '' 's/z\.string()\.uuid()/z.uuid()/g' file.ts
sed -i '' 's/z\.string()\.datetime()/z.iso.datetime()/g' file.ts
```

### 2. Update Error Parameters

Replace error customization:
```bash
sed -i '' 's/message:/error:/g' file.ts
sed -i '' 's/invalid_type_error:/error:/g' file.ts
sed -i '' 's/required_error:/error:/g' file.ts
```

### 3. Update Merge to Extend

```bash
sed -i '' 's/\.merge(/\.extend(/g' file.ts
```

### 4. Verify Changes

Run tests after migration:
```bash
npm test
```

## Integration with Review Plugin

This skill can be invoked by the review plugin when reviewing Zod-related code:

```bash
/review zod-compatibility
```

The skill will check for all deprecated patterns and provide remediation guidance.

## References

- Full migration guide: Use the migrating-v3-to-v4 skill from the zod-4 plugin
- String formats: Use the validating-string-formats skill from the zod-4 plugin
- Error handling: Use the customizing-errors skill from the zod-4 plugin

**Cross-Plugin References:**

- If validating external data sources, use the validating-external-data skill for understanding runtime validation requirements
- If applying schema validation patterns to database queries, use the ensuring-query-type-safety skill from prisma-6 for type-safe Prisma queries with proper input validation

## Success Criteria

- ✅ Zero deprecated API usage in codebase
- ✅ All string formats use top-level functions
- ✅ Error customization uses unified `error` parameter
- ✅ Schema composition uses `extend` instead of `merge`
- ✅ Tests pass after migration
- ✅ TypeScript compilation succeeds without type errors
