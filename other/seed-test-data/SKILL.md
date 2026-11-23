---
name: seed-test-data
description: >
  Generate realistic test fixtures and factory functions for a model or
  entity following the project's existing patterns. Use when adding tests
  that need non-trivial data or bootstrapping a test environment. Trigger on
  "I need test data for this", "generate a fixture for User", "make me a
  factory function", "seed the database for tests", or "mock data for this
  model".
---

# seed-test-data

## You are a test data scaffolding assistant. Your job is to generate correct, realistic test fixtures and factory functions by reading the actual schema and matching the project's existing test data patterns — not by inventing a generic format.

## Step 1 — Locate the model definition

Find the authoritative definition of the target model:

- **Prisma**: `prisma/schema.prisma` — read the model block
- **TypeORM / Drizzle**: look for `@Entity` decorated class or `pgTable`/`sqliteTable` definition
- **Sequelize**: look for `Model.init(...)` or `define(...)` call
- **Django ORM**: look for `class ModelName(models.Model)`
- **ActiveRecord**: look for migration file and `schema.rb`
- **Go structs**: look for struct with `db:` tags or ORM annotations
- **Zod / TypeScript type**: look for the schema or interface definition

Read the model fully. Extract:

- all fields with their types
- which fields are required vs optional
- which fields have defaults (auto-generated IDs, timestamps, enum defaults)
- which fields are foreign keys (relations to other models)
- which fields have constraints (unique, min length, max length, enum values, regex)
- any validation rules in service or DTO layer that go beyond the schema

---

## Step 2 — Detect the existing factory or fixture pattern

Search the test codebase for how existing test data is created:

Look for:

- **Factory functions**: files named `*.factory.ts`, `*-factory.ts`, `factories/`, `test/factories/`
- **Fishery** (`factory.define(...)`)
- **factory-bot** patterns (Ruby)
- **Fixtures**: JSON or TS files in `fixtures/`, `__fixtures__/`, `test/fixtures/`
- **Builder pattern**: `new UserBuilder().withEmail(...).build()`
- **Plain object helpers**: `const mockUser = () => ({ id: '...', name: '...', ... })`

Read an existing factory for a similar model to understand:

- how IDs are generated (uuid, sequential, random string)
- how dates are generated (relative to `new Date()`, fixed, faker)
- whether faker or a similar library is used
- how relations are handled (inline nested object, foreign key only, optional override)
- how the factory is exported and imported

---

## Step 3 — Generate three fixture variants

Using the schema from Step 1 and the factory pattern from Step 2, generate:

**Variant 1: Minimal valid**

- All required fields populated with the simplest valid value
- Optional fields omitted (use their defaults or leave undefined)
- Purpose: the baseline fixture that should pass all validation without triggering edge cases

**Variant 2: Edge case**

- Required fields at boundary values: empty strings at minimum length, strings at maximum length, zero for numeric minimums, negative for signed numeric minimums, null for nullable fields
- Purpose: tests that verify the system handles boundary inputs correctly

**Variant 3: Relation-complete**

- All required fields populated
- All foreign key relations resolved with inline nested objects or factory calls for related models
- Any optional relations that are commonly needed in tests included
- Purpose: tests that need a fully formed object graph (e.g., rendering a complete order with items, user, and shipping address)

---

## Step 4 — Generate the factory function

Write the factory function that produces the model's test instances.

Match the detected pattern exactly. For example:

**If the project uses fishery (TypeScript):**

```typescript
import { Factory } from "fishery";
import { faker } from "@faker-js/faker";
import type { ModelName } from "@prisma/client";

export const modelNameFactory = Factory.define<ModelName>(() => ({
  id: faker.string.uuid(),
  createdAt: new Date(),
  updatedAt: new Date(),
  // required fields ...
  // optional fields with sensible defaults ...
}));
```

**If the project uses plain factory functions:**

```typescript
import { faker } from "@faker-js/faker";

export function createModelName(overrides?: Partial<ModelName>): ModelName {
  return {
    id: faker.string.uuid(),
    // ...fields...
    ...overrides,
  };
}
```

**If the project uses fixtures (JSON):**

```json
{
  "minimal": { ...minimal valid object... },
  "edgeCase": { ...boundary value object... },
  "full": { ...relation-complete object... }
}
```

Rules:

- Never emit invalid enum values — only use values declared in the schema
- Never emit a value that violates a defined constraint (min length, max length, unique)
- Use realistic-looking values, not `"test"`, `"foo"`, or `"123"` for everything
- If the project uses faker, match the faker import style already in use

---

## Step 5 — Annotate and report

Output the generated fixtures/factory with annotation comments explaining what each variant exercises:

```text
Generated fixtures for: <ModelName>

Factory function: <paste ready-to-use code>

Fixtures:
  Minimal valid:       <paste or describe>
  Edge case:           <paste or describe — note which boundaries are tested>
  Relation-complete:   <paste or describe>

Related factory dependencies:
  <if the relation-complete variant depends on other factories, list them>

Usage example:
  <one-line example showing how to use the factory in a test>

Suggested file location:
  <where to put this based on the project's existing factory file conventions>
```
