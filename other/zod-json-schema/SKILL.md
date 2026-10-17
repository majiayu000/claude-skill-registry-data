---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: zod-json-schema
description: >
  Best practices for generating JSON Schema from Zod v4 schemas using z.toJSONSchema().
  Covers target versions, metadata registries, override callbacks, io modes,
  transform handling, regen-check tests, and serving schemas as HTTP routes.
  Load this skill when converting Zod schemas to JSON Schema or building
  schema generation scripts.
---

# Zod JSON Schema

Zod v4 has native `z.toJSONSchema()` for converting Zod schemas to JSON Schema.
This skill covers the options, gotchas, and patterns for using it correctly.

## Basic usage

```ts
import { z } from 'zod'

const schema = z.object({
  name: z.string(),
  age: z.number(),
})

z.toJSONSchema(schema)
// { type: 'object', properties: { name: { type: 'string' }, age: { type: 'number' } }, ... }
```

## Options reference

```ts
z.toJSONSchema(schema, {
  target: 'draft-7',        // 'draft-04' | 'draft-07' | 'draft-2020-12' | 'openapi-3.0'
  metadata: z.globalRegistry, // extract .meta({ id }) schemas into definitions/
  reused: 'inline',         // 'inline' (default) | 'ref'
  unrepresentable: 'any',   // 'throw' (default) | 'any'
  io: 'input',              // 'input' | 'output' (default)
  cycles: 'ref',            // 'ref' (default) | 'throw'
  override: (ctx) => { },   // mutate ctx.jsonSchema inline during traversal
})
```

## Target version

draft-07 uses `definitions/` for shared schemas. draft-2020-12 uses `$defs/`.
When generating schemas for IDE autocomplete (JSON/YAML language servers), draft-07
has the widest compatibility.

```ts
z.toJSONSchema(schema, { target: 'draft-7' })
```

Zod v4 with `target: 'draft-7'` automatically adds `$schema: "http://json-schema.org/draft-07/schema#"`
to the output. No need to prepend it manually.

## Named definitions with `.meta({ id })`

Register schemas with `.meta({ id: 'Name' })` and pass `metadata: z.globalRegistry`
to extract them as `definitions/Name`. Use `reused: 'inline'` to avoid auto-generated
`__schema0` names for unnamed reused schemas.

```ts
export const iconSchema = z
  .union([z.string(), iconObjectSchema])
  .describe('The icon to be displayed')
  .meta({ id: 'iconSchema' })

const configSchema = z.object({
  icon: iconSchema.optional(),
})

z.toJSONSchema(configSchema, {
  target: 'draft-7',
  metadata: z.globalRegistry,
  reused: 'inline',
})
// icon property references: { $ref: "#/definitions/iconSchema" }
```

### Strip redundant `id` from definitions

Zod copies all `.meta()` fields into the JSON Schema output, including `id`.
This is redundant since the `definitions/` key already identifies the schema.
The Zod author recommends stripping it with `override` ([colinhacks/zod#4578](https://github.com/colinhacks/zod/issues/4578)).

```ts
z.toJSONSchema(configSchema, {
  target: 'draft-7',
  metadata: z.globalRegistry,
  reused: 'inline',
  override: (ctx) => {
    if ('id' in ctx.jsonSchema) {
      delete ctx.jsonSchema.id
    }
  },
})
```

### `allOf` wrappers around `$ref`

When `.optional()` is called on a schema with `.meta({ id })`, Zod emits
`{ allOf: [{ $ref: "#/definitions/X" }] }` instead of `{ $ref }`.
This is valid JSON Schema; every tool handles it correctly.
Do not bother unwrapping it unless you have a specific downstream consumer that breaks.

## External `$ref` via `.meta()` for IDE autocomplete

`.meta()` fields are copied verbatim into the JSON Schema output. Use `.meta({ $ref: '...' })`
to inject an external `$ref` URL that points to a remote schema. IDEs fetch the remote
schema and use it for autocomplete suggestions (e.g. a list of valid icon names).

```ts
const lucideIconNameSchema = z
  .string()
  .meta({ $ref: 'https://example.com/schemas/lucide-icons.json' })

const fontawesomeIconNameSchema = z
  .string()
  .meta({ $ref: 'https://example.com/schemas/fontawesome-icons.json' })

export const iconSchema = z
  .union([lucideIconNameSchema, fontawesomeIconNameSchema, z.string(), iconObjectSchema])
  .describe('The icon to be displayed')
  .meta({ id: 'iconSchema' })
```

This produces a union where the first two branches carry external `$ref` URLs:

```json
{
  "anyOf": [
    { "type": "string", "$ref": "https://example.com/schemas/lucide-icons.json" },
    { "type": "string", "$ref": "https://example.com/schemas/fontawesome-icons.json" },
    { "type": "string" },
    { "type": "object", "properties": { "name": { ... } } }
  ]
}
```

The remote schema at that URL should be a JSON Schema with an `enum` array listing
all valid values. IDEs like VS Code fetch it and offer those values as autocomplete.

Serve the remote schemas with CORS headers so browser-based editors can fetch them:

```ts
import lucideIconsSchema from './generated/lucide-icons-schema.json' with { type: 'json' }

app.get('/schemas/lucide-icons.json', () =>
  Response.json(lucideIconsSchema, { headers: { 'access-control-allow-origin': '*' } }),
)
```

## Handling transforms with `io: "input"`

`z.transform()` is unrepresentable in JSON Schema because JSON Schema describes
data shape, not runtime behavior. By default, `z.toJSONSchema()` represents the
**output** type (after transforms), which for transforms means `{}` (any) with
`unrepresentable: 'any'`.

Use `io: "input"` to represent the **input** type instead. This is what you want
when the schema describes what users write (config files, frontmatter, API payloads).

```ts
const widthSchema = z.union([z.string(), z.number()]).transform(String)

const schema = z.object({
  width: widthSchema.optional(),
})

// Default (output): width becomes {} because transform is unrepresentable
z.toJSONSchema(schema, { unrepresentable: 'any' })
// { properties: { width: {} } }

// With io: "input": width becomes anyOf string|number (the input union)
z.toJSONSchema(schema, { unrepresentable: 'any', io: 'input' })
// { properties: { width: { anyOf: [{ type: "string" }, { type: "number" }] } } }
```

## The `override` callback

`override` runs for every schema node during traversal. Mutate `ctx.jsonSchema` directly.
Use it for things Zod doesn't have options for.

```ts
z.toJSONSchema(schema, {
  unrepresentable: 'any',
  override: (ctx) => {
    // Support z.date() as ISO datetime strings
    if (ctx.zodSchema._zod.def.type === 'date') {
      ctx.jsonSchema.type = 'string'
      ctx.jsonSchema.format = 'date-time'
    }
  },
})
```

`override` runs **after** Zod's default conversion. For unrepresentable types,
set `unrepresentable: 'any'` alongside `override`, otherwise Zod throws before
the callback is reached.

## Descriptions with `.describe()`

`.describe()` text is preserved verbatim in the JSON Schema `description` field.
Use it on every field that users or agents will see. Keep descriptions concise,
one sentence, starting with a noun or verb.

```ts
z.object({
  title: z.string().optional().describe('The page title displayed in the sidebar and browser tab'),
  hidden: z.boolean().optional().describe('Hide the page from sidebar navigation and search results'),
})
```

For multiline descriptions, use `dedent`:

```ts
import dedent from 'string-dedent'

z.string().describe(dedent`
  Path to an OpenAPI specification file (JSON or YAML), or an array
  of paths. Endpoints from the spec are auto-generated as pages
  grouped by tag
`)
```

## `.passthrough()` for extensible schemas

When your schema should accept unknown fields without validation errors (e.g. config
files where users might paste extra fields from another tool), chain `.passthrough()`.
This emits `additionalProperties: {}` in the JSON Schema.

```ts
const configSchema = z.object({
  name: z.string(),
  colors: colorsSchema.optional(),
}).passthrough()
```

## `z.partialRecord()` for optional key subsets

`z.record(z.enum([...]), z.string())` makes every enum key **required** in the output.
Use `z.partialRecord()` when users should only provide a subset.

```ts
const socialPlatforms = ['x', 'github', 'discord', 'linkedin'] as const

// Every platform is required
z.record(z.enum(socialPlatforms), z.string())

// Each platform is optional (what you usually want)
z.partialRecord(z.enum(socialPlatforms), z.string())
```

## Regen-check test

Add a test that regenerates the schema and compares to what's on disk.
This catches cases where someone edits the Zod schema but forgets to run the
generation script.

```ts
import { test } from 'vitest'
import fs from 'node:fs'
import path from 'node:path'
import { z } from 'zod'
import { mySchema } from './schema.ts'

test('schema.json matches source schemas', () => {
  const onDisk = fs.readFileSync(path.join(import.meta.dirname, 'schema.json'), 'utf-8')

  const generated = z.toJSONSchema(mySchema, {
    target: 'draft-7',
    metadata: z.globalRegistry,
    reused: 'inline',
    unrepresentable: 'any',
    override: (ctx) => {
      if ('id' in ctx.jsonSchema) delete ctx.jsonSchema.id
    },
  })

  const expected = JSON.stringify(generated, null, 2) + '\n'

  if (onDisk !== expected) {
    throw new Error('schema.json is out of sync. Run: pnpm generate-schema')
  }
})
```

## Generation script pattern

A complete schema generation script with multiple schemas:

```ts
import { z } from 'zod'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { configSchema } from '../src/schema.ts'
import { frontmatterSchema } from '../src/lib/frontmatter.ts'

const here = path.dirname(fileURLToPath(import.meta.url))

function stripMetaId(ctx: { jsonSchema: Record<string, unknown> }) {
  if ('id' in ctx.jsonSchema) {
    delete ctx.jsonSchema.id
  }
}

function writeSchema(schema: unknown, filePath: string) {
  fs.writeFileSync(filePath, JSON.stringify(schema, null, 2) + '\n')
  console.log(`✓ wrote ${path.relative(process.cwd(), filePath)}`)
}

// Config schema — complex, with named definitions
writeSchema(
  z.toJSONSchema(configSchema, {
    target: 'draft-7',
    metadata: z.globalRegistry,
    reused: 'inline',
    unrepresentable: 'any',
    override: stripMetaId,
  }),
  path.join(here, '..', 'src', 'schema.json'),
)

// Frontmatter schema — simpler, io: "input" for transform fields
writeSchema(
  z.toJSONSchema(frontmatterSchema, {
    target: 'draft-7',
    unrepresentable: 'any',
    io: 'input',
  }),
  path.join(here, '..', 'src', 'frontmatter-schema.json'),
)
```

## Serving schemas as HTTP routes

Import the generated JSON and serve it with CORS headers so editors and agents
can fetch the schema at a well-known URL.

```ts
import schema from './schema.json' with { type: 'json' }
import frontmatterSchema from './frontmatter-schema.json' with { type: 'json' }

const corsJson = (data: unknown) =>
  Response.json(data, { headers: { 'access-control-allow-origin': '*' } })

app.get('/docs.json', () => corsJson(schema))
app.get('/frontmatter.json', () => corsJson(frontmatterSchema))
```

Users reference the schema URL in their config files for IDE autocomplete:

```jsonc
{
  "$schema": "https://example.com/docs.json",
  "name": "My Project"
}
```

For YAML frontmatter in MDX files, the `$schema` key in the YAML block points
agents to the available fields (editors need the `remark-lint-frontmatter-schema`
plugin to actually validate it):

```yaml
---
"$schema": https://example.com/frontmatter.json
title: Getting Started
icon: rocket
---
```

## AJV validation

Validate the generated schema itself is well-formed:

```ts
import Ajv from 'ajv'

const ajv = new Ajv({ allErrors: true, strict: false })
const valid = ajv.validateSchema(schema) // true if the schema is valid draft-07
```
