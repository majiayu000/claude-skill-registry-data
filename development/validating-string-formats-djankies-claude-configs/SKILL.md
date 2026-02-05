---
name: validating-string-formats
description: Guide to Zod v4 new features including top-level string formats, string transformations, codecs, and stringbool
---

# Using Zod v4 Features

## Purpose

Comprehensive guide to new features introduced in Zod v4 that improve developer experience, performance, and type safety.

## Top-Level String Format Functions

### Overview

Zod v4 moved string format validations to top-level functions for **14x faster** parsing.

**All optimized formats:**
- `z.email()` - Email validation
- `z.uuid()` - UUID validation  
- `z.iso.datetime()` - ISO datetime
- `z.url()` - URL validation
- `z.ipv4()` / `z.ipv6()` - IP addresses
- `z.jwt()` - JWT tokens
- `z.base64()` - Base64 strings
- `z.hash('sha256')` - Hash strings

**Quick example:**
```typescript
const emailSchema = z.email().trim().toLowerCase();
const uuidSchema = z.uuid();
const datetimeSchema = z.iso.datetime();
```

**With custom error:**
```typescript
const emailSchema = z.email({
  error: "Please enter a valid email address"
});
```

## String Transformation Methods

### Trim, Lower Case, Upper Case

```typescript
z.string().trim()           // Remove whitespace
z.string().toLowerCase()    // Convert to lowercase
z.string().toUpperCase()    // Convert to uppercase
```

**Chaining:**
```typescript
const emailSchema = z.email().trim().toLowerCase();
```

**Execution order:** Transformations execute left-to-right.

## StringBool Type

Parse string representations of booleans:

```typescript
const boolSchema = z.stringbool();

boolSchema.parse('true');   // true
boolSchema.parse('false');  // false
boolSchema.parse('1');      // true
boolSchema.parse('0');      // false
```

**Use case:** Query parameters and form data

```typescript
const querySchema = z.object({
  active: z.stringbool(),
  verified: z.stringbool()
});
```

## Codec Type

Bidirectional transformations for encode/decode:

```typescript
const dateCodec = z.codec({
  decode: z.string().transform(s => new Date(s)),
  encode: z.date().transform(d => d.toISOString())
});

const decoded = dateCodec.parse('2024-01-01T00:00:00Z');
const encoded = dateCodec.encode(new Date());
```

**Safe operations:**
```typescript
const result = dateCodec.safeDecode('invalid-date');
if (!result.success) {
  console.error(result.error);
}
```

## Performance Optimizations

### Bulk Array Validation (7x faster)

```typescript
const arraySchema = z.array(itemSchema);
const items = arraySchema.parse([...]);
```

### Passthrough for Performance

```typescript
const schema = z.object({
  id: z.string()
}).passthrough();  // 10-20% faster, keeps extra fields
```

## Best Practices

### 1. Use Top-Level Functions

```typescript
z.email()           // ✅ 14x faster
z.string().email()  // ❌ Deprecated
```

### 2. Chain Transformations

```typescript
z.email().trim().toLowerCase()  // ✅ Declarative
```

### 3. Leverage StringBool

```typescript
z.stringbool()      // ✅ For "true"/"false" strings
z.boolean()         // ✅ For actual booleans
```

### 4. Brand IDs

```typescript
z.string().brand<'UserId'>()
z.string().brand<'OrderId'>()
```

### 5. Codecs for Serialization

```typescript
const dateCodec = z.codec({
  decode: z.iso.datetime().transform(s => new Date(s)),
  encode: z.date().transform(d => d.toISOString())
});
```

## Migration from v3

**String Formats:**
```typescript
z.email()          // ✅ v4
z.string().email() // ❌ v3
```

**Error Customization:**
```typescript
z.string({ error: "Required" })  // ✅ v4
z.string({ message: "Required" }) // ❌ v3
```

**Schema Composition:**
```typescript
schemaA.extend(schemaB.shape)  // ✅ v4
schemaA.merge(schemaB)         // ❌ v3
```

## References

- Validation: Use the validating-schema-basics skill from the zod-4 plugin
- Migration: Use the migrating-v3-to-v4 skill from the zod-4 plugin
- Transformations: Use the transforming-string-methods skill from the zod-4 plugin
- Performance: Use the optimizing-performance skill from the zod-4 plugin

## Success Criteria

- ✅ Using top-level format functions
- ✅ String transformations for user input
- ✅ StringBool for query params
- ✅ Codecs for date serialization
- ✅ Branded types for nominal typing
- ✅ Bulk array validation
- ✅ Discriminated unions for faster parsing
