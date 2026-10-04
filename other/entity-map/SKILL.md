---
name: product-map
description: Canonical enumeration of project Prisma models, API routes, components, user stories, and EIS docs. Use before creating any docs/wiki/ page to verify the source object exists. Triggers on "entities", "which prisma models", "list endpoints", "wiki bootstrap", "does <Entity> exist", "enumerate domain", "product-wiki plugin".
---

# Entity Map

Authoritative enumeration of project domain objects. **Never invent entities.** If a model, endpoint, component, story, or EIS is not listed in one of the authoritative sources below, it does not exist yet — do not create a wiki page for it.

## Config File Lookup

Before probing any paths, check whether the project has a config file at `.claude/plugins/product-wiki/entity-map.json`. If that file exists, read it — it may override any of the default probe paths below.

## Authoritative Sources (in precedence order)

1. **Prisma schema** — ground truth for entity names and fields. Probe in this order and use the first that exists:
   - `src/prisma/schema.prisma`
   - `prisma/schema.prisma`
2. **API routes** — ground truth for HTTP endpoints. Probe in this order and use the first that exists:
   - `src/app/api/**/route.ts`
   - `app/api/**/route.ts`
3. **UI components** — ground truth for components. Probe in this order:
   - `src/components/`
   - `components/`
4. **User stories index** — ground truth for user stories:
   - `docs/reference/stories/INDEX.md`
5. **EIS documents** — ground truth for EIS (Event / Integration Spec) documents:
   - `docs/eis/EIS-*.md`

## How to Enumerate

### Entities (Prisma models)

Probe for the schema file using the order above. Then:
```
Grep pattern: "^model\s+(\w+)\s*\{"  in the located schema file
```

### Endpoints

Glob the API routes directory using the probe order above:
```
Glob: src/app/api/**/route.ts   (or app/api/**/route.ts if the src/ variant is absent)
```
Each file's path (minus the `api/` prefix and `/route.ts` suffix) is the endpoint path. Methods (`GET`, `POST`, `PATCH`, `DELETE`) are exported as named functions inside each `route.ts`.

### Components

Glob the components directory using the probe order above:
```
Glob: src/components/**/*.tsx   (or components/**/*.tsx)
```

### User stories
```
Read: docs/reference/stories/INDEX.md
Glob: docs/reference/stories/US-*.md
```

### EIS documents
```
Glob: docs/eis/EIS-*.md
```

## Wiki Page Mapping Rule

| Source object         | Wiki page path                                        |
|-----------------------|-------------------------------------------------------|
| Prisma model `Foo`    | `docs/wiki/entities/Foo.md`                           |
| Endpoint `GET /x/y`   | `docs/wiki/endpoints/get-x-y.md` (lowercase, `/` -> `-`) |
| Story `US-123`        | `docs/wiki/stories/US-123.md`                         |
| EIS `EIS-045`         | `docs/wiki/eis/EIS-045.md`                            |

One page per source object. No speculative pages.

## Currency Rule

The Prisma schema (whichever path resolves) is the single source of truth for entity names and field shapes. When a wiki page references a field, **quote the schema** (include the field name, type, and any `@default` / `@db` decorators). Re-read the schema at the start of every wiki update — do not rely on memory.

## Never Hallucinate

If an agent considers writing a wiki page for an entity/endpoint/story/EIS that does not appear in the authoritative sources above, it must **stop** and either (a) find the source file, or (b) decline to create the page. Speculative wiki pages corrupt the map.
