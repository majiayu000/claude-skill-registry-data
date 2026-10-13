---
name: coding-standards
description: Project coding conventions for the CODER agent. Load before any implementation task to ensure consistent style and patterns.
---

# Coding Standards

## General
- TypeScript by default unless project is plain JS
- Functional style preferred over class-heavy OOP
- Small functions — one responsibility per function
- Explicit types — avoid `any`
- Named exports over default exports (exceptions: pages, layouts)

## Vue 3 (Mateus's primary stack)
- Always `<script setup>` — never Options API
- Composables in `composables/` — prefix with `use`
- Props typed with `defineProps<{...}>()`
- Emits typed with `defineEmits<{...}>()`
- Tailwind for styling — no inline styles

## Node/Express
- Async/await — no raw `.then()` chains
- Error handling with try/catch at controller level
- Validation at route level before controller
- No logic in route files — keep routes thin

## MongoDB/Mongoose
- Schema validation at model level
- Lean queries where possible
- Never expose `_id` directly — use `id` transform

## File structure
- Feature-based, not type-based
- `components/` → reusable only
- `views/` or `pages/` → route-level components
- `services/` → API calls and external integrations

## Naming
- Components: PascalCase
- Composables: camelCase with `use` prefix
- Files: kebab-case
- Constants: SCREAMING_SNAKE_CASE

## Before writing code
1. Read the existing file if editing
2. Check for similar patterns already in the codebase
3. Follow what's there — don't introduce new patterns without noting it
