---
name: zod-4
description: Write, review and migrate Zod 4 schemas (zod@4.x, checked against 4.6.7) for runtime validation at trust boundaries such as HTTP bodies, query strings, form posts, env config, webhooks, queue messages and LLM output. Covers the Zod 3 to 4 changes that fail silently (required_error, invalid_type_error and errorMap ignored, ZodError.errors removed, .default() short-circuiting vs .prefault(), exhaustive z.record enum keys, stricter z.uuid(), required z.unknown() keys), custom messages and per-field error maps, coercion footguns (z.coerce.boolean, empty strings), string formats and safe URL checks, and refinements that must run next to field errors. Use when code imports zod, when adding validation to an API, form, config loader or webhook handler, when a zod upgrade breaks types or tests, or when you see Zod 3 idioms like z.string().email(), .flatten(), .merge(), z.nativeEnum or z.function().args().
license: MIT
---

# Zod 4

Zod 4 is the current major (`zod@4.6.7` as of November 2026). Most Zod examples on the web and in
model training data are Zod 3, and many Zod 3 idioms still compile or run on Zod 4 while doing
something different. Everything below was checked against zod 4.6.7 and zod.dev.

## 1. Know which Zod you are writing

```sh
node -p "require('zod/package.json').version"   # or: npm ls zod
```

| Installed | Write | Notes |
| --- | --- | --- |
| `zod@4.x` | `import * as z from 'zod'` (or `import { z } from 'zod'`) | Root is Zod 4. `zod/v4` is the same API. |
| `zod@4.x`, legacy code | port to the root API | `zod/v3` is a frozen copy of the v3 API. Use it only as a temporary comparison tool, never as the fix. |
| `zod@3.25.x` | match the repo | Zod 4 was previewed at `zod/v4` in 3.25. Don't mix both APIs in one module. |
| library on top of zod | `zod/v4/core` | Works with both Zod and Zod Mini. See zod.dev/library-authors. |

`zod/mini` (also published as `@zod/mini` since 4.5) is a functional, tree-shakable API:
`z.string().check(z.minLength(5))` instead of methods. Don't use classic method chains on mini schemas.

## 2. Boundary rules

1. Parse untrusted data once, at the boundary, and pass the inferred type inward. Never `as`-cast
   `JSON.parse`, `req.body`, `process.env`, queue payloads or model output.
2. In request handlers use `safeParse` and turn issues into a response. Throwing is fine at startup
   (config), but collect every issue first so one deploy fixes everything.
3. `z.object` strips unknown keys. That is the right default for inputs: `{ plan: 'enterprise' }` in a
   profile-update body disappears instead of reaching your update. Use `z.strictObject` when an extra key
   means a client bug (internal APIs), `z.looseObject` when you must forward unknown fields.
   Never make third-party webhook schemas strict: providers add fields without notice.
4. Coerce only transports that are strings by nature (query strings, env, form posts). JSON bodies
   already carry numbers and booleans; coercing them hides client bugs.
5. Async refinements or transforms require `parseAsync`/`safeParseAsync`; sync `parse` throws
   "Encountered Promise during synchronous parse".
6. Issues do not include the input value unless you pass `{ reportInput: true }`. Keep it that way
   for anything that can hold secrets, and don't interpolate raw values into your own messages.
7. Bound the work on hostile input: `.max()` on arrays and strings, a body-size limit, and
   `schema.validate(data)` (4.6) when you only need a yes/no answer.

## 3. Zod 3 habits that break on Zod 4

The dangerous rows are the silent ones: the code runs and returns the wrong thing.

| Zod 3 habit | Zod 4 | If you keep the habit |
| --- | --- | --- |
| `z.string({ required_error, invalid_type_error })` | `error: (iss) => …` guarded by `iss.code` (section 4) | **silently ignored**, default messages (TS error) |
| `{ errorMap: (iss, ctx) => ({ message }) }` | `error: (iss) => string \| undefined` | **silently ignored** (TS error) |
| `{ message: '…' }` | `{ error: '…' }` or a plain string argument | still works, deprecated |
| `err.errors` | `err.issues` | `undefined`, then `TypeError` |
| `err.flatten()`, `err.format()` | `z.flattenError(err)`, `z.treeifyError(err)` | still work, deprecated |
| `err.formErrors` | `z.flattenError(err).formErrors` | `undefined` |
| `.transform(f).default(inputValue)` | `.prefault(inputValue)` or `.default(outputValue)` | **default returned as-is**, transform skipped, wrong type |
| `objectSchema.default({})` to get inner defaults | `.prefault({})` or a complete default | **returns `{}`**, inner defaults never run |
| `z.record(z.enum([...]), v)` for a partial map | `z.partialRecord(z.enum([...]), v)` | **every enum key is now required** |
| `z.record(valueSchema)` | `z.record(z.string(), valueSchema)` | TS error (4.6.7 still tolerates it at runtime: don't rely on that) |
| `z.string().uuid()` for UUID-shaped ids | `z.guid()`; `z.uuid()` only for RFC 9562 ids | **rejects non-RFC ids** (variant bits must be `10`) |
| `z.unknown()` / `z.any()` field treated as optional | add `.optional()` | **missing key fails** (since 4.4.0) |
| `z.coerce.boolean()` with the key absent | `.default(false)` | **error** "expected nonoptional" (v3 gave `false`) |
| `.Enum.x`, `.Values.x` | `.enum.x` | `undefined`, then `TypeError` |
| `z.nativeEnum(E)` | `z.enum(E)` | works, deprecated |
| `z.string().ip()`, `.cidr()` | `z.union([z.ipv4(), z.ipv6()])`, `z.cidrv4()`, `z.cidrv6()` | `TypeError` at module load |
| `z.function().args(A).returns(B)` | `z.function({ input: [A], output: B }).implement(fn)` | `TypeError` at module load |
| `.refine(fn, (val) => ({ message }))` | `.refine(fn, { error: (iss) => \`… ${iss.input}\` })` | **message lost**, "Invalid input" |
| `ctx.path` in `superRefine` | not available | `undefined` |
| `.strict()`, `.passthrough()` | `z.strictObject()`, `z.looseObject()` | still work (legacy, kept) |
| `A.merge(B)` | `A.extend(B.shape)` or `z.object({ ...A.shape, ...B.shape })` | works; throws if `A` has refinements (4.4.0) |
| `z.string().email()`, `.url()`, `.uuid()`, `.datetime()` | `z.email()`, `z.url()`, `z.uuid()`, `z.iso.datetime()` | still work, deprecated; mind check order (section 5) |
| `.nonempty()` giving `[T, ...T[]]` | `z.tuple([T], T)` | type is now `T[]` |
| `.deepPartial()` | `z.deepPartial(schema)` (4.5+) | method removed |
| `z.ZodTypeAny`, `ZodEffects`, `schema._def` | `z.ZodType`, `schema._zod.def` | internals moved |

Full before/after code, grep patterns and the 4.x minor-release changes are in
[the migration reference](references/migration-v3-to-v4.md).

## 4. Error messages

Precedence, highest first: check-level (`.min(5, 'msg')`), schema-level (`z.string('msg')` or
`{ error }`), per-parse (`schema.parse(x, { error })`), global (`z.config({ customError })`), locale.
In Zod 3 a per-parse error map beat the schema; in Zod 4 the schema wins.

**A schema-level `error` also covers the schema's own checks.** `z.string('Name must be text').min(2)`
reports "Name must be text" for `'a'`. The migration guide's pattern for `required_error` therefore
clobbers every length and format message on that schema unless you guard by code:

```ts
const Username = z
  .string({
    error: (iss) => {
      if (iss.code !== 'invalid_type') return undefined // undefined = fall through to the default
      return iss.input === undefined ? 'Username is required' : 'Username must be text'
    },
  })
  .min(3)
  .max(24) // keeps "Too big: expected string to have <=24 characters"
```

Turning issues into the shapes clients want:

```ts
// Dot-path map for forms and APIs: { nickname: [...], 'delivery.zip': [...], 'tags.2': [...] }
export function issuesByPath(error: z.ZodError): Record<string, string[]> {
  const out: Record<string, string[]> = {}
  for (const issue of error.issues) {
    const key = issue.path.map(String).join('.')
    ;(out[key] ??= []).push(issue.message)
  }
  return out
}
```

- `z.flattenError(err)` keys only the **first** path segment: a `delivery.zip` issue lands under
  `fieldErrors.delivery`. Use it only for flat schemas.
- `z.treeifyError(err)` mirrors the schema (`properties`, `items`, `errors`); read it with `?.`.
- `z.prettifyError(err)` is for logs and CLIs, not for clients.
- Errors from `safeParse` are `z.ZodError`. Errors thrown by a `z.function().implement()` wrapper are
  `z.core.$ZodError` and are **not** `instanceof z.ZodError`; catch with `instanceof z.core.$ZodError`.

More (error map signature, i18n with `z.locales`, `iss.schema` metadata, treeify walkers) in
[the error reference](references/error-messages.md).

## 5. Strings and formats

- Formats are top-level schemas: `z.email()`, `z.url()`, `z.httpUrl()`, `z.uuid()`, `z.guid()`,
  `z.ipv4()`, `z.ipv6()`, `z.cidrv4()`, `z.e164()`, `z.jwt()`, `z.base64()`, `z.iso.datetime()`,
  `z.iso.date()`, and more. Each accepts a message: `z.email('That address looks wrong')`.
- **Normalise before you validate.** Checks run in order, and a format schema checks first:
  `z.email().trim()` rejects `'  kim@example.org '`. Write
  `z.string().trim().toLowerCase().pipe(z.email())`.
- **`z.url()` is permissive**: anything `new URL()` accepts, including `javascript:`, `mailto:` and
  `file:`. For links you will fetch, redirect to or render:
  - `z.url({ protocol: /^https$/ })`: https only.
  - `z.httpUrl()`: http or https with a domain hostname (rejects `localhost` and bare IPs).
  - Connection strings: `z.url({ protocol: /^amqps?$/ })` for a broker URL, and so on.
- `z.uuid()` is RFC 9562 (version 1-8, variant `10`, plus nil and max). `z.guid()` is any
  8-4-4-4-12 hex string. `z.uuidv4()`, `z.uuidv7()` pin a version.
- `z.iso.datetime()` rejects offsets and local times by default. Webhook timestamps with `+01:00`
  need `z.iso.datetime({ offset: true })`; seconds are required unless `precision: -1`.
- `z.email()` uses a pragmatic regex; `z.email({ pattern: z.regexes.html5Email })` matches browsers.

## 6. Numbers, booleans and coercion

`z.coerce.number()` is `Number(input)` and `z.coerce.boolean()` is `Boolean(input)`:

| Input | `z.coerce.number()` | `z.coerce.boolean()` |
| --- | --- | --- |
| `''` | `0` | `false` |
| `'false'` / `'0'` | NaN error / `0` | **`true`** / **`true`** |
| `' 42 '`, `'0x10'`, `'1e3'` | `42`, `16`, `1000` | `true` |
| `null` | `0` | `false` |

- Booleans from strings: `z.stringbool()` (case-insensitive; truthy `true 1 yes on y enabled`,
  falsy `false 0 no off n disabled`; anything else is an error; customise with `{ truthy, falsy }`).
  It rejects `''`, so map `''` to `undefined` first when empty means "unset".
- Integers from strings: if hex and exponents must not sneak in, use
  `z.string().regex(/^-?\d+$/).transform(Number).pipe(z.int().min(1))` or the `stringToInt` codec.
- Empty means unset (env vars, HTML forms): `z.preprocess((v) => (v === '' ? undefined : v), inner)`;
  `inner` can carry `.optional()` or `.default()`.
- `z.number()` rejects `NaN` and `±Infinity`. `.int()` and `z.int()` reject unsafe integers; use
  `z.int32()` or `z.bigint()` for other ranges.

## 7. Objects, defaults and optional keys

- `.default(v)`: if the input is `undefined`, return `v` **without parsing it**; `v` must match the
  output type. `.prefault(v)`: parse `v` as if it were the input (Zod 3's `.default`).
- Object defaults: `.default({})` returns `{}`. Use `.prefault({})` so inner `.default()`s run, or
  `.default(() => ({ ...complete }))`. Defaults now also apply inside `.optional()` fields.
- `z.unknown()`, `z.any()` and `z.undefined()` keys are required since 4.4.0; add `.optional()`.
  `.exactOptional()` allows an absent key but not an explicit `undefined`.
- Refinements live inside the schema in Zod 4. On a refined object, `.pick()`, `.omit()` and
  `.partial()` throw, `.extend()` throws when it overwrites a key (use `.safeExtend()`), and
  `.merge()` throws. Build shapes first, refine last.
- Compose with spread for the clearest strictness and the cheapest type-checking:
  `z.strictObject({ ...Base.shape, ...Extra.shape })`.

## 8. Refinements that must run next to field errors

Object-level `.refine()`/`.superRefine()` are skipped once a field has a non-continuable issue
(missing or wrong type). Format and length failures don't block them; an empty required field mapped to `undefined` does.
A form that shows every error at once needs `when`, and `when` must check the values it needs:
it also fires when the body is `null` or a string.

```ts
const Fields = z.object({
  guest: z.string().min(1),
  checkIn: z.iso.date(),
  checkOut: z.iso.date(),
})
const Dates = Fields.pick({ checkIn: true, checkOut: true })

export const Booking = Fields.refine((b) => b.checkOut > b.checkIn, {
  error: 'Check-out must be after check-in',
  path: ['checkOut'],
  // Runs even when `guest` is missing, but only once both dates parse.
  when: (payload) => Dates.safeParse(payload.value).success,
})
```

A `when` that only inspects `payload.issues` paths will run the refinement on `null`, a string or
an object with missing fields, and your callback will throw a `TypeError` instead of reporting.

`.superRefine((val, ctx) => ctx.addIssue({...}))` still works and accepts `when` since 4.4.0.
`.check((ctx) => ctx.issues.push({...}))` is the low-level form.

## 9. Unions, enums and records

- Tagged payloads (webhooks, queue messages): `z.discriminatedUnion('type', [...])`. An unknown tag yields
  one `invalid_union` issue at `['type']`, not one issue per option.
- `z.xor([...])` (4.2+) requires exactly one option to match; make object options strict or they
  overlap.
- `z.enum(['a', 'b'])`, `z.enum(MyTsEnum)` or `z.enum({ A: 'a' } as const)`; read values with
  `.enum.a` and `.options`; derive with `.exclude()`/`.extract()`. `z.literal(['a', 'b'])` takes
  several values.
- `z.record(keys, values)` always takes two schemas; enum keys are exhaustive.
  `z.partialRecord` for optional keys, `z.looseRecord` to pass non-matching keys through.

## 10. Types

- `z.infer<typeof S>` is the output type; `z.input<typeof S>` is what callers send. `z.coerce.*`
  and `z.preprocess` inputs are `unknown`. Form libraries usually want `z.input`.
- Generic helpers take `z.ZodType` (not `ZodTypeAny`):
  `function parseWith<T extends z.ZodType>(s: T, data: unknown): z.output<T> { return s.parse(data) }`.
- Type predicates in `.refine()` were ignored in 4.0-4.2 and narrow the output type again since
  4.3.0 (`z.string().refine((s): s is 'a' => s === 'a')` outputs `'a'`). The zod.dev migration guide
  still describes the 4.0 behaviour.

## 11. Upgrading a codebase from Zod 3

1. Confirm the installed version and keep the lockfile change in the same commit.
2. Run the type checker. Most removed APIs surface there: `required_error`, `errorMap`, `.errors`,
   `.formErrors`, `.Enum`/`.Values`, `.ip()`, `z.function().args()`, function second argument to
   `.refine()`, `.default()` values of the wrong type, single-argument `z.record`.
3. Grep for what types don't catch (plain JS, `any`, behaviour changes):
   `rg -n "required_error|invalid_type_error|errorMap|\.errors\b|formErrors|\.default\(\{\}\)|z\.record\(z\.enum|z\.(unknown|any)\(\)|\.uuid\(|z\.coerce\.|ctx\.path|instanceof (z\.)?ZodError" src`
4. Port each site with the table in section 3. Preserve custom messages with code-guarded `error`
   functions; preserve defaults with `.prefault()`; keep shape-only UUID checks with `z.guid()`.
5. Prove behaviour is unchanged: run the tests, then feed representative bad inputs through old and
   new schemas and compare codes, paths and custom messages (default wording changed in Zod 4, so
   don't diff those). `import { z as z3 } from 'zod/v3'` lets you run the old schema side by side
   while you compare; delete it afterwards.
6. Don't "fix" the upgrade by importing `zod/v3`, downgrading, or adding `@ts-expect-error`.

## 12. Anti-patterns

| Don't | Do |
| --- | --- |
| `JSON.parse(body) as Event` | `Event.safeParse(JSON.parse(body))` inside a try for the JSON error |
| `z.coerce.boolean()` for env or form flags | `z.stringbool()` with `''` mapped to `undefined` |
| `z.coerce.number().default(4)` with empty env vars | `''` to `undefined`, then `.default(4)` |
| `z.url()` for a redirect or callback target | `z.url({ protocol: /^https$/ })` or `z.httpUrl()` |
| `z.email().trim()` | `z.string().trim().pipe(z.email())` |
| `z.string({ error: 'X is required' }).min(3)` | guard the schema-level message by `iss.code` |
| `error.errors.map(...)`, `.flatten()` for nested forms | `error.issues` with dot paths |
| object `.refine()` for a cross-field rule the UI must always show | `.refine(fn, { path, when })` with a value check |
| `strictObject` for a third-party webhook | `z.object` (strip) or `z.looseObject` |
| interpolating `iss.input` of a secret into a message | generic messages; `reportInput` stays off |

## References

- [Migration details, grep patterns and 4.x release changes](references/migration-v3-to-v4.md)
- [Error customisation and formatting](references/error-messages.md)
- [Boundary recipes: env, forms, query strings, webhooks, JSON Schema, codecs](references/boundary-recipes.md)
- [Sources checked](references/sources.md)
