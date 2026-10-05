---
name: zod
description: Zod — schema validation, type inference, parsing, refinement, transforms, integration.
---

## zod

### Schema Definitions
- Primitives: `z.string()`, `z.number()`, `z.boolean()`, `z.bigint()`, `z.date()`, `z.null()`, `z.undefined()`.
- Objects: `z.object({ name: z.string() })` — nested, optional `.optional()`, nullable `.nullable()`.
- Arrays/Tuples: `z.array(z.string())`, `z.tuple([z.string(), z.number()])`.
- Unions/Discriminated: `z.union([...])`, `z.discriminatedUnion('type', [...])` for tagged unions.
- Literal/Enum: `z.literal('foo')`, `z.enum(['A', 'B'])`, `z.nativeEnum(ColorEnum)`.

### Type Inference
- `z.infer<typeof schema>` — extract TS type from schema; `z.input<T>` / `z.output<T>` for input/output variants.
- `z.ZodType<T>` — class generic for extending or wrapping schemas.

### Parsing
- `schema.parse(data)` — throws `ZodError` on failure; `schema.safeParse(data)` — returns `{ success, data, error }`.
- `schema.parseAsync(data)` / `schema.safeParseAsync(data)` for async refinements.
- Partial/deep partial: `schema.partial()`, `.deepPartial()`, `.pick({ k: true })`, `.omit({ k: true })`.

### Refinement & Transform
- `.refine((val) => val.length > 5, "too short")` — custom sync/async validation.
- `.superRefine((val, ctx) => { ctx.addIssue(...) })` — multi-issue additions.
- `.transform((val) => val.toUpperCase())` — post-parse value transformation.
- `.preprocess((val) => typeof val === 'string' ? JSON.parse(val) : val)` — pre-parse hooks.

### Integration
- React Hook Form: `zodResolver(z.object({...}))` from `@hookform/resolvers/zod`.
- tRPC: schemas as procedure input/output validators.
- OpenAPI generation via `zod-to-json-schema` or `@anatine/zod-openapi`.
