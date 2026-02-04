---
name: customrule
description: This is a new rule
---

# TypeScript Migration Rules for 9jang Project

## Architecture Standard
- We are using a Monorepo structure with `pnpm workspaces`.
- Centralized Data Source: All API schemas and types MUST reside in `packages/shared/src/schemas`.
- Never define types locally if they represent API entities; always use `z.infer<typeof Schema>` from the shared package.

## TypeScript Best Practices
- **No `any`**: Use `unknown` with type guards if a type is truly uncertain.
- **Zod Integration**: Use Zod for runtime validation at the API service layer. 
- **Tiptap Extensions**: When migrating extensions, use "Module Augmentation" to register custom commands and attributes in `@tiptap/core`.

## Migration Strategy
- When converting Vue components, prioritize `<script setup lang="ts">`.
- For large composables (e.g., usePrintPreview), break down the logic into smaller, typed internal functions.
- Ensure all path aliases use `@/` for frontend and `@9jang/shared` for shared types.