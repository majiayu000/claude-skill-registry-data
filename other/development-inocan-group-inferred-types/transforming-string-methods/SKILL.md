---
name: transforming-string-methods
description: Write type-safe transformations with Zod including string methods, custom transforms, codecs, and pipelines
---

# Writing Zod Transformations

## Purpose

Comprehensive guide to writing transformations in Zod v4, covering built-in string methods, custom transforms, codecs, and transformation pipelines.

## Built-In String Transformations

### Trim, Lower Case, Upper Case

```typescript
const schema = z.string().trim();           // Remove whitespace
const schema = z.string().toLowerCase();    // Convert to lowercase
const schema = z.string().toUpperCase();    // Convert to uppercase
```

**Use cases:**
- Trim: User input fields (always trim)
- Lower: Email/username normalization
- Upper: Product codes, currency codes

**Chaining:**
```typescript
const emailSchema = z.email().trim().toLowerCase();
```

**Execution order:** Transformations execute left-to-right

### Best practice: Transform before validation

```typescript
z.string().trim().min(1)      // ✅ Trim then validate
z.string().min(1).trim()      // ❌ Validate then trim (wrong order)
```

## Custom Transformations

### Basic Transform

```typescript
const schema = z.string().transform(s => s.toUpperCase());

type Input = z.input<typeof schema>;    // string
type Output = z.output<typeof schema>;  // string
```

### Type-Changing Transform

```typescript
const schema = z.string().transform(s => parseInt(s));

type Input = z.input<typeof schema>;    // string
type Output = z.output<typeof schema>;  // number
```

### Transform with Validation

```typescript
const schema = z.string()
  .regex(/^\d+$/, { error: "Must be numeric string" })
  .transform(s => parseInt(s))
  .refine(n => n > 0, { error: "Must be positive" });
```

**Order:** Validation → Transformation → Refinement

### Transform Objects

```typescript
const userSchema = z.object({
  firstName: z.string(),
  lastName: z.string()
}).transform(user => ({
  ...user,
  fullName: `${user.firstName} ${user.lastName}`
}));
```

### Transform Arrays

```typescript
const schema = z.string()
  .transform(s => s.split(','))
  .transform(arr => arr.map(s => s.trim()))
  .transform(arr => arr.filter(s => s.length > 0));
```

## Codecs (Bidirectional Transforms)

### Date Codec

```typescript
const dateCodec = z.codec({
  decode: z.iso.datetime().transform(s => new Date(s)),
  encode: z.date().transform(d => d.toISOString())
});

const decoded = dateCodec.parse('2024-01-01T00:00:00Z');  // Date object
const encoded = dateCodec.encode(new Date('2024-01-01'));  // string
```

### Safe Codec

```typescript
const result = dateCodec.safeDecode('invalid-date');
if (!result.success) {
  console.error(result.error);
}
```

### Base64 Codec

```typescript
const base64Codec = z.codec({
  decode: z.base64().transform(s => Buffer.from(s, 'base64')),
  encode: z.instanceof(Buffer).transform(b => b.toString('base64'))
});
```

## Transformation Pipelines

### Sequential Transformations

```typescript
const schema = z.string()
  .trim()
  .toLowerCase()
  .transform(s => s.split(' '))
  .transform(words => words.filter(w => w.length > 0))
  .transform(words => words.join('-'));
```

### Pipe Method

```typescript
const stringToNumber = z.string()
  .regex(/^\d+$/)
  .transform(s => parseInt(s));

const positiveNumber = z.number().min(1);

const schema = stringToNumber.pipe(positiveNumber);
```

**Type inference:**
```typescript
type Input = z.input<typeof schema>;    // string
type Output = z.output<typeof schema>;  // number
```

## Overwrite vs Transform

**Transform (additive):**
```typescript
z.object({ firstName, lastName }).transform(data => ({
  ...data,
  fullName: `${data.firstName} ${data.lastName}`
}));
```
Output has all fields: firstName, lastName, fullName

**Overwrite (destructive):**
```typescript
z.object({ firstName, lastName }).overwrite(data => ({
  fullName: `${data.firstName} ${data.lastName}`
}));
```
Output has only new fields: fullName

## Async Transformations

### Basic Async Transform

```typescript
const schema = z.string().transform(async (email) => {
  const user = await fetchUser(email);
  return user;
});

const result = await schema.parseAsync('user@example.com');
```

### Async Refinement

```typescript
const emailSchema = z.email().refine(
  async (email) => {
    const exists = await checkEmailExists(email);
    return !exists;
  },
  { error: "Email already exists" }
);
```

## Best Practices

### 1. Transform Before Validation

```typescript
z.string().trim().min(1)      // ✅ Trim then validate
z.string().min(1).trim()      // ❌ Validate then trim
```

### 2. Use Built-In Methods

```typescript
z.string().trim().toLowerCase()              // ✅ Built-in
z.string().transform(s => s.trim().toLowerCase())  // ❌ Manual
```

### 3. Keep Transformations Pure

```typescript
const schema = z.string().transform(s => s.toUpperCase());  // ✅ Pure

let count = 0;
const schema = z.string().transform(s => {
  count++;  // ❌ Side effect
  return s.toUpperCase();
});
```

### 4. Use Codecs for Serialization

```typescript
const dateCodec = z.codec({
  decode: z.iso.datetime().transform(s => new Date(s)),
  encode: z.date().transform(d => d.toISOString())
});  // ✅ Bidirectional
```

### 5. Type-Safe Transformations

```typescript
const schema = z.string().transform(s => parseInt(s));
type Output = z.output<typeof schema>;  // ✅ Type-safe
```

### 6. Handle Edge Cases

```typescript
const schema = z.string()
  .transform(s => s.split(','))
  .transform(arr => arr.map(s => s.trim()))
  .transform(arr => arr.filter(s => s.length > 0));  // ✅ Handle empty
```

## Migration from v3

**String Transformations (New in v4):**
```typescript
const validated = z.string().trim().parse(input);  // ✅ v4 declarative
```

**Codecs (New in v4):**
```typescript
const codec = z.codec({
  decode: z.iso.datetime().transform(s => new Date(s)),
  encode: z.date().transform(d => d.toISOString())
});  // ✅ v4 bidirectional
```

## References

- v4 Features: Use the validating-string-formats skill from the zod-4 plugin
- Error handling: Use the customizing-errors skill from the zod-4 plugin
- Performance: Use the optimizing-performance skill from the zod-4 plugin
- Testing: Use the testing-zod-schemas skill from the zod-4 plugin

## Success Criteria

- ✅ Using built-in string transformations
- ✅ Transform before validation
- ✅ Pure transformation functions
- ✅ Type-safe with z.input/z.output
- ✅ Codecs for bidirectional transforms
- ✅ Proper transformation order
- ✅ Edge cases handled
- ✅ Performance optimized
