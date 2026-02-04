---
name: zod
description: Zod 4+ validation patterns. Use when validating forms, API responses, env vars, or inferring types from schemas.
---

# Zod 4+

## String formats — top-level

```ts
// v4: top-level functions
const email = z.email()
const uuid = z.uuid()
const url = z.url()
const iso = z.iso.datetime()

// NOT z.string().email() — that's v3
```

## Record — two arguments required

```ts
// v4: key + value schemas
z.record(z.string(), z.number())

// NOT z.record(z.number()) — that's v3
```

## Objects

```ts
// Strict (no extra keys)
z.strictObject({ name: z.string() })

// Loose (allow extra keys)
z.looseObject({ name: z.string() })

// .strict() and .passthrough() still work but prefer above
```

## Error customization

```ts
// v4: unified 'error' param
z.string({ error: "Must be a string" })
z.email({ error: (issue) => `Invalid: ${issue.input}` })

// NOT 'message', 'invalid_type_error', etc. — that's v3
```

## Metadata

```ts
// v4: .meta() with object
z.string().meta({ label: "Username", description: "Your handle" })

// NOT .describe() — that's v3
```

## Unions and intersections

```ts
// v4: prefer explicit helpers
z.union([z.string(), z.number()])
z.intersection(baseSchema, extendSchema)

// NOT .or() / .and() chains — those are v3 style
```

## Accessing errors

```ts
const result = schema.safeParse(data)
if (!result.success) {
  console.log(result.error.issues)  // v4: .issues
  // NOT .errors — that's v3
}
```

## Form validation with React 19

```ts
const formSchema = z.object({
  email: z.email({ error: "Invalid email" }),
  age: z.coerce.number().min(18, { error: "Must be 18+" })
})

async function action(prev: State, formData: FormData) {
  const result = formSchema.safeParse(Object.fromEntries(formData))
  if (!result.success) {
    return { errors: result.error.issues }
  }
  // result.data is typed
}
```

## Type inference

```ts
const userSchema = z.object({
  id: z.uuid(),
  email: z.email(),
  role: z.enum(["admin", "user"])
})

type User = z.infer<typeof userSchema>
```

## Avoid

- `z.string().email()` → `z.email()`
- `z.string().uuid()` → `z.uuid()`
- `z.record(value)` → `z.record(key, value)`
- `message` param → `error` param
- `.describe()` → `.meta()`
- `.or()` / `.and()` → `z.union()` / `z.intersection()`
- `.errors` → `.issues`
