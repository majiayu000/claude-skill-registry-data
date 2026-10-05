---
name: beautyline-types-and-models
description: >-
  Places TypeScript types and interfaces for the Beautyline webapp domain,
  Mongoose models, and React props. Use when adding or moving types,
  refactoring shared shapes, touching src/types or src/models, or deciding
  where a new interface should live.
---

# Beautyline: types and models

## Where types go

| Kind | Location | Rule |
|------|----------|------|
| Shared domain/UI data shapes (forms, DTOs, catalog JSON) | `src/types/` | One concern per file (e.g. `course.ts`, `contact.ts`). Reuse across pages, APIs, or multiple components. |
| MongoDB persistence + Mongoose schemas | `src/models/` | Document-related interfaces (`IUser`, schemas). Do not duplicate as `src/types` unless you need a deliberately separate JSON/public shape — prefer `src/lib/public-*` mappers instead. |
| Public/serialized shapes used by `lib` helpers | `src/lib/` | Often alongside `public-course`, `public-product`, etc. Keeps DB vs API contract clear. |
| Props for a single component | Same file as the component | Private `interface ComponentNameProps` at top of file. |
| Props imported by parent or route | Same file + `export interface ComponentNameProps` | Export only when another module imports the props type. |

## Conventions

- Prefer **`interface`** for object shapes unless you need a union/`type` alias.
- **Do not** put Mongoose-only fields in `src/types/` meant for UI — keep persistence types in `models/`.
- When a type documents a form state (GDPR, validation), brief Italian JSDoc on `src/types/` exports is welcome to match existing files (`contact.ts`, `profile.ts`).
- Imports use the `@/` alias (`@/types/course`, `@/models/User`, etc.).

## Quick decision

1. Used in **multiple folders** or **API + UI** → `src/types/` or exported type from relevant `src/lib/` module.
2. **Only one component** cares → colocated `Props` interface; export if a parent wires props explicitly with that type.
