---
name: nuxt-architecture
description: Foundational architecture for Nuxt 4 + Vue 3 + Nuxt UI applications. Use when starting new projects, understanding project structure, or making architectural decisions about directory organization, technology choices, and pattern selection.
---

# Nuxt Architecture

Domain-driven, type-safe, composable-first architecture prioritizing separation of concerns.

## Core Philosophy

**[philosophy.md](references/philosophy.md)** - Foundational principles, separation of concerns, when to use each pattern

## Project Structure

**[structure.md](references/structure.md)** - Directory layout, naming conventions, file organization

## Technology Stack

| Layer | Technology |
|-------|------------|
| Framework | Nuxt 4 (SPA mode, SSR disabled) |
| UI | Vue 3 Composition API |
| Components | Nuxt UI v4 + Tailwind CSS 4 |
| State | Composables with `ref`/`useState` |
| HTTP | Custom fetch via Sanctum/ofetch |
| Auth | Laravel Sanctum (`nuxt-auth-sanctum`) |
| Real-time | Laravel Echo (`nuxt-laravel-echo`) |

## Standard Layout

```
app/
├── components/     # Vue components by type (Tables/, Forms/, Modals/)
├── composables/    # Custom Vue composables
├── constants/      # channels.ts, events.ts, permissions.ts
├── enums/          # TypeScript enums with behavior
├── features/       # Domain modules (queries/, mutations/, actions/)
├── models/         # Domain model classes
├── pages/          # File-based routing
├── repositories/   # Data access layer
├── types/          # TypeScript definitions
└── values/         # Value objects
```

## Pattern Flow

```
Component → Action → Mutation → Repository → API
              ↓
         Query (reactive data fetching)
```

Actions orchestrate business logic. Mutations handle pure API calls. Queries provide reactive data. Repositories abstract API access.
