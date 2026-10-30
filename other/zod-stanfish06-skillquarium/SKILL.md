---
name: zod
description: Define and validate runtime schemas with Zod in TypeScript or JavaScript. Use for parsing external payloads, forms, environment variables, discriminated unions, transformations, validation errors, or Zod 3-to-4 compatibility.
---

# Zod

Inspect the installed Zod version, import paths, tsconfig, and existing schemas.
Use the project's installed major version; do not introduce a second major to
copy an example. The examples here target Zod 4. Enable TypeScript `strict`
mode for reliable inferred types.

## Parse at the boundary

Treat external JSON, form values, environment variables, and tool output as
`unknown`. A TypeScript annotation or `as` assertion does not validate them.
Define the schema once and infer the application type from it.

```ts
import * as z from "zod";

const CreateItem = z.strictObject({
  name: z.string().trim().min(1),
  quantity: z.number().int().positive(),
});
type CreateItem = z.infer<typeof CreateItem>;

const result = CreateItem.safeParse(input);
if (!result.success) {
  return Response.json(
    { errors: z.flattenError(result.error) },
    { status: 400 },
  );
}
await saveItem(result.data);
```

`parse` throws on invalid input; `safeParse` returns a union narrowed by
`success`. Select the form that fits the caller. Handle a validation failure
before calling side effects, and return only the error detail appropriate for
the consumer; avoid logging whole credential-bearing payloads.

Choose unknown-key behavior explicitly: `z.object` strips unknown keys,
`z.strictObject` rejects them, and `z.looseObject` preserves them. Do not
silently change an established API's acceptance policy while adding validation.

## Coercion and transformations

Use coercion only for boundaries that supply strings or another known format.
`z.coerce.number()` follows JavaScript `Number` conversion, including empty
strings becoming zero. `z.coerce.boolean()` follows `Boolean`, so the string
`"false"` becomes `true`. These are not parsers for a textual boolean protocol.

For a query parameter with a defined syntax, validate that syntax before
conversion. Zod 4's `z.stringbool()` handles supported boolean strings.

```ts
const Query = z.strictObject({
  limit: z.string().regex(/^[1-9]\d*$/)
    .pipe(z.coerce.number<string>().int().max(100)),
  enabled: z.stringbool(),
});
const query = Query.parse({ limit: "12", enabled: "false" });
// { limit: 12, enabled: false }
type QueryInput = z.input<typeof Query>;
type QueryOutput = z.output<typeof Query>;
```

`z.infer` is the output type. Use `z.input` and `z.output` separately when
a default, coercion, transform, or codec changes the accepted and produced types.
Use `safeParseAsync` / `parseAsync` when any refinement or transform is async.
A synchronous parse cannot run an asynchronous validation.

## Unions, composition, and compatibility

- Use `z.discriminatedUnion("kind", [...])` when a literal field selects the
  payload shape. Narrow the parsed result by that field before accessing
  variant-specific properties.
- Reuse shared schemas with composition rather than defining a separate manual
  TypeScript interface that can drift. Recheck defaults, unknown-key behavior,
  and refinement behavior when extending an existing schema.
- Resolve a v3/v4 mismatch against the installed version and official migration
  guide. Zod 4 exposes top-level format helpers such as `z.email()` and
  error helpers such as `z.flattenError`; do not assume their presence in v3.
- `z.toJSONSchema` cannot represent every runtime schema, including arbitrary
  transforms. Inspect unsupported constructs and the target consumer's supported
  JSON Schema subset before using the output for an API or model tool.

## Verify boundary behavior

Test valid input, malformed input, the chosen unknown-key policy, and a case
where coercion or a union could accept the wrong shape. If validation gates a
side effect, verify invalid input never reaches it. Run the project's typecheck
as well as runtime tests.

[scripts/smoke.ts](scripts/smoke.ts) is a small executable example covering
strict objects, discriminated unions, textual number/boolean parsing, async
refinements, and inferred input/output types. Copy it into an isolated directory
that can resolve the project's installed `zod`, then run it with the project's
TypeScript runtime and typechecker. It performs no network calls. For Bun:

```bash
bun smoke.ts
# Run the project's typecheck command with smoke.ts included.
```

## Primary references

- [Basic parsing, errors, and inference](https://zod.dev/basics)
- [Schema API and coercion](https://zod.dev/api)
- [Error formatting](https://zod.dev/error-formatting)
- [JSON Schema](https://zod.dev/json-schema)
- [Zod 4 migration guide](https://zod.dev/v4/changelog)

Source reviewed: `colinhacks/zod@afdac65e0f80c0ccf9e8909da97c411567908b57`,
`packages/docs/content/basics.mdx` and the official API documentation.
