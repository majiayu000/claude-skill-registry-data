---
name: zod-docs
description: Query and manage local Zod documentation mirror (59 docs). Search Zod topics for TypeScript-first schema validation, parsing, type inference, refinements, and transformations. Use when implementing validation or answering Zod-related questions. (user)
---

# Zod Documentation Skill

Query local Zod documentation covering TypeScript-first schema validation, parsing, type inference, and advanced validation patterns.

## Overview

This skill provides access to a complete local mirror of Zod documentation (59 docs across 2 main sections). The documentation is structured, indexed, and optimized for AI/LLM consumption.

## Documentation Structure

```
docs/libs/zod/
├── _index.md                     # Navigation index
├── _meta.json                    # Metadata
├── README.md                     # Overview
├── introduction/                 # Getting started (4 docs)
├── primitives/                   # Basic types (13 docs)
├── complex-types/                # Objects, arrays, etc (17 docs)
├── refinements/                  # Custom validation (5 docs)
├── error-handling/               # Errors (4 docs)
├── advanced/                     # Advanced patterns (7 docs)
├── utilities/                    # Helper methods (6 docs)
└── integration/                  # JSON Schema, etc (2 docs)
```

## Core Concepts

### 1. Schema Definition
Location: `docs/libs/zod/introduction/defining-schemas.md`
- Creating schemas with z.object(), z.string(), etc.
- Type inference with z.infer<typeof schema>
- Parsing and validation

### 2. Primitives
Location: `docs/libs/zod/primitives/`
- String validation with .email(), .url(), .regex()
- Number validation with .min(), .max(), .int()
- Date, boolean, and other basic types
- String-specific and number-specific validations

### 3. Complex Types
Location: `docs/libs/zod/complex-types/`
- Objects with nested validation
- Arrays with .min(), .max(), .nonempty()
- Unions and discriminated unions
- Tuples, records, maps, sets
- Enums and optional/nullable values

### 4. Refinements & Transformations
Location: `docs/libs/zod/refinements/`
- Custom validation with .refine()
- Advanced validation with .superrefine()
- Data transformation with .transform()
- Input preprocessing with .preprocess()
- Chaining with .pipe()

### 5. Error Handling
Location: `docs/libs/zod/error-handling/`
- Parsing errors and error formatting
- Custom error messages with .error()
- Error maps for internationalization

## Usage Protocol

### When to Activate

Use this skill when:
1. User asks about input validation
2. Questions about TypeScript type safety
3. Need schema validation patterns
4. Form validation with Zod
5. API validation
6. tRPC/Convex integration with Zod

### Search Strategy

1. **Check Navigation First**
   ```bash
   Read: docs/libs/zod/_index.md
   Purpose: See all available documentation
   ```

2. **Section-Based Search**
   - Introduction: `docs/libs/zod/introduction/`
   - Primitives: `docs/libs/zod/primitives/`
   - Complex Types: `docs/libs/zod/complex-types/`
   - Refinements: `docs/libs/zod/refinements/`
   - Error Handling: `docs/libs/zod/error-handling/`
   - Advanced: `docs/libs/zod/advanced/`
   - Utilities: `docs/libs/zod/utilities/`
   - Integration: `docs/libs/zod/integration/`

3. **Specific Queries**
   ```bash
   # Basic validation
   Read: docs/libs/zod/introduction/basic-usage.md

   # String validation
   Read: docs/libs/zod/primitives/strings.md

   # Object validation
   Read: docs/libs/zod/complex-types/objects.md

   # Custom validation
   Read: docs/libs/zod/refinements/refinements.md

   # Error handling
   Read: docs/libs/zod/error-handling/error-handling.md
   ```

## Common Queries

### "How do I create a Zod schema?"
1. Read `docs/libs/zod/introduction/defining-schemas.md`
2. Read `docs/libs/zod/introduction/basic-usage.md`
3. Show z.object() and primitive examples

### "How do I validate email and URL?"
1. Read `docs/libs/zod/primitives/strings.md`
2. Read `docs/libs/zod/primitives/string-methods.md`
3. Show .email(), .url() validation

### "How do I validate objects?"
1. Read `docs/libs/zod/complex-types/objects.md`
2. Read `docs/libs/zod/complex-types/object-methods.md`
3. Show nested object validation and methods

### "How do I add custom validation?"
1. Read `docs/libs/zod/refinements/refinements.md`
2. Read `docs/libs/zod/refinements/superrefine.md`
3. Show .refine() and .superrefine() patterns

### "How do I transform data?"
1. Read `docs/libs/zod/refinements/transform.md`
2. Show .transform() and .preprocess() examples

### "How do I infer TypeScript types?"
1. Read `docs/libs/zod/introduction/type-inference.md`
2. Show z.infer<typeof schema> usage

### "How do I handle validation errors?"
1. Read `docs/libs/zod/error-handling/error-handling.md`
2. Read `docs/libs/zod/error-handling/error-formatting.md`
3. Show error parsing and custom messages

## Response Format

When answering Zod questions:

1. **Start with Context**
   - Briefly explain the validation need
   - Reference the source doc

2. **Provide Code Examples**
   - Show schema definition
   - Include TypeScript type inference
   - Demonstrate parsing/validation

3. **Cite Sources**
   - Format: `docs/libs/zod/[section]/[file].md`
   - Include line numbers if relevant

4. **Related Topics**
   - Link to related validation patterns
   - Suggest utility methods

## Key Zod Features

- TypeScript-first with automatic type inference
- Zero dependencies
- Works in Node.js and browsers
- Composable schemas
- Rich error messages
- Transform and preprocess data
- Integration with React Hook Form, tRPC, etc.

## Common Integration Patterns

### tRPC
```typescript
import { z } from 'zod'

const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2)
})

export const userRouter = router({
  create: publicProcedure
    .input(userSchema)
    .mutation(async ({ input }) => {
      // input is type-safe
    })
})
```

### Convex
```typescript
import { v } from 'convex/values'

// Convex uses its own validator, but Zod can validate before calling
```

### React Hook Form
```typescript
import { zodResolver } from '@hookform/resolvers/zod'

const form = useForm({
  resolver: zodResolver(schema)
})
```

## Example Response

```
User: "How do I validate an email with Zod?"