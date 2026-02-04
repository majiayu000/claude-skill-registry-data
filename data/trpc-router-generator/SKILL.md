---
name: trpc-router-generator
description: Generate tRPC router files with procedures and validation. Triggers on "create trpc router", "generate trpc procedure", "trpc api", "typesafe api".
---

# tRPC Router Generator

Generate tRPC routers with type-safe procedures and Zod validation.

## Output Requirements

**File Output:** `*.router.ts` tRPC router files
**Format:** Valid tRPC v11
**Standards:** tRPC 11.x, Zod

## When Invoked

Immediately generate a complete tRPC router.

## Example Invocations

**Prompt:** "Create tRPC router for users"
**Output:** Complete `users.router.ts` with CRUD procedures.
