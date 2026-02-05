---
name: react-hook-form-zod
description: |
  Build type-safe validated forms in React using React Hook Form and Zod schema validation. Single schema works on both client and server for DRY validation with full TypeScript type inference via z.infer.

  Use when: building forms with validation, integrating shadcn/ui Form components, implementing multi-step wizards, handling dynamic field arrays with useFieldArray, or fixing uncontrolled to controlled warnings, resolver errors, async validation issues.

---

# React Hook Form + Zod Validation

**Status**: Production Ready ✅
**Last Verified**: 2025-11-28
**Latest Versions**: react-hook-form@7.66.1, zod@4.1.13, @hookform/resolvers@5.2.2

---

## Quick Start

```bash
npm install react-hook-form@7.66.1 zod@4.1.13 @hookform/resolvers@5.2.2
```

**Basic Form Pattern**:
```typescript
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

type FormData = z.infer<typeof schema>

const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { email: '', password: '' }, // REQUIRED to prevent uncontrolled warnings
})

<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register('email')} />
  {errors.email && <span role="alert">{errors.email.message}</span>}
</form>
```

**Server Validation** (CRITICAL - never skip):
```typescript
// SAME schema on server
const data = schema.parse(await req.json())
```

---

## Key Patterns

**useForm Options** (validation modes):
- `mode: 'onSubmit'` (default) - Best performance
- `mode: 'onBlur'` - Good balance
- `mode: 'onChange'` - Live feedback, more re-renders
- `shouldUnregister: true` - Remove field data when unmounted (use for multi-step forms)

**Zod Refinements** (cross-field validation):
```typescript
z.object({ password: z.string(), confirm: z.string() })
  .refine((data) => data.password === data.confirm, {
    message: "Passwords don't match",
    path: ['confirm'], // CRITICAL: Error appears on this field
  })
```

**Zod Transforms**:
```typescript
z.string().transform((val) => val.toLowerCase()) // Data manipulation
z.string().transform(parseInt).refine((v) => v > 0) // Chain with refine
```

**zodResolver** connects Zod to React Hook Form, preserving type safety

---

## Registration

**register** (for standard HTML inputs):
```typescript
<input {...register('email')} /> // Uncontrolled, best performance
```

**Controller** (for third-party components):
```typescript
<Controller
  name="category"
  control={control}
  render={({ field }) => <CustomSelect {...field} />} // MUST spread {...field}
/>
```

**When to use Controller**: React Select, date pickers, custom components without ref. Otherwise use `register`.

---

## Error Handling

**Display errors**:
```typescript
{errors.email && <span role="alert">{errors.email.message}</span>}
{errors.address?.street?.message} // Nested errors (use optional chaining)
```

**Server errors**:
```typescript
const onSubmit = async (data) => {
  const res = await fetch('/api/submit', { method: 'POST', body: JSON.stringify(data) })
  if (!res.ok) {
    const { errors: serverErrors } = await res.json()
    Object.entries(serverErrors).forEach(([field, msg]) => setError(field, { message: msg }))
  }
}
```

---

## Advanced Patterns

**useFieldArray** (dynamic lists):
```typescript
const { fields, append, remove } = useFieldArray({ control, name: 'contacts' })

{fields.map((field, index) => (
  <div key={field.id}> {/* CRITICAL: Use field.id, NOT index */}
    <input {...register(`contacts.${index}.name` as const)} />
    {errors.contacts?.[index]?.name && <span>{errors.contacts[index].name.message}</span>}
    <button onClick={() => remove(index)}>Remove</button>
  </div>
))}
<button onClick={() => append({ name: '', email: '' })}>Add</button>
```

**Async Validation** (debounce):
```typescript
const debouncedValidation = useDebouncedCallback(() => trigger('username'), 500)
```

**Multi-Step Forms**:
```typescript
const step1 = z.object({ name: z.string(), email: z.string().email() })
const step2 = z.object({ address: z.string() })
const fullSchema = step1.merge(step2)

const nextStep = async () => {
  const isValid = await trigger(['name', 'email']) // Validate specific fields
  if (isValid) setStep(2)
}
```

**Conditional Validation**:
```typescript
z.discriminatedUnion('accountType', [
  z.object({ accountType: z.literal('personal'), name: z.string() }),
  z.object({ accountType: z.literal('business'), companyName: z.string() }),
])
```

---

## shadcn/ui Integration

**Note**: shadcn/ui deprecated the Form component. Use the Field component for new implementations (check latest docs).

**Legacy Form component**:
```typescript
<FormField control={form.control} name="username" render={({ field }) => (
  <FormItem>
    <FormControl><Input {...field} /></FormControl>
    <FormMessage />
  </FormItem>
)} />
```

---

## Performance

- Use `register` (uncontrolled) over `Controller` (controlled) for standard inputs
- Use `watch('email')` not `watch()` (isolates re-renders to specific fields)
- `shouldUnregister: true` for multi-step forms (clears data on unmount)

---

## Critical Rules

✅ **Always set defaultValues** (prevents uncontrolled→controlled warnings)

✅ **Validate on BOTH client and server** (client can be bypassed - security!)

✅ **Use `field.id` as key** in useFieldArray (not index)

✅ **Spread `{...field}`** in Controller render

✅ **Use `z.infer<typeof schema>`** for type inference

❌ **Never skip server validation** (security vulnerability)

❌ **Never mutate values directly** (use `setValue()`)

❌ **Never mix controlled + uncontrolled** patterns

❌ **Never use index as key** in useFieldArray

---

## Known Issues (12 Prevented)

1. **Zod v4 Type Inference** - [#13109](https://github.com/react-hook-form/react-hook-form/issues/13109) (Closed 2025-11-01): Use `z.infer<typeof schema>`. Resolved in v7.66.x+.

2. **Uncontrolled→Controlled Warning** - Always set `defaultValues` for all fields

3. **Nested Object Errors** - Use optional chaining: `errors.address?.street?.message`

4. **Array Field Re-renders** - Use `key={field.id}` in useFieldArray (not index)

5. **Async Validation Race Conditions** - Debounce validation, cancel pending requests

6. **Server Error Mapping** - Use `setError()` to map server errors to fields

7. **Default Values Not Applied** - Set `defaultValues` in useForm options (not useState)

8. **Controller Field Not Updating** - Always spread `{...field}` in render function

9. **useFieldArray Key Warnings** - Use `field.id` as key (not index)

10. **Schema Refinement Error Paths** - Specify `path` in refinement: `refine(..., { path: ['fieldName'] })`

11. **Transform vs Preprocess** - Use `transform` for output, `preprocess` for input

12. **Multiple Resolver Conflicts** - Use single resolver (zodResolver), combine schemas if needed

---

## Bundled Resources

**Templates**: basic-form.tsx, advanced-form.tsx, shadcn-form.tsx, server-validation.ts, async-validation.tsx, dynamic-fields.tsx, multi-step-form.tsx, package.json

**References**: zod-schemas-guide.md, rhf-api-reference.md, error-handling.md, performance-optimization.md, shadcn-integration.md, top-errors.md

**Docs**: https://react-hook-form.com/ | https://zod.dev/ | https://ui.shadcn.com/docs/components/form

---

**License**: MIT | **Last Verified**: 2025-11-28
