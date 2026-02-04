---
name: nextjs-16-app-router-structure
description: >
  Standard project structure, routing, and component patterns for
  Next.js 16 App Router applications, so that layouts, pages, and
  data fetching stay consistent across projects.
---

# Next.js 16 App Router Structure Skill

## When to use this Skill

Use this Skill whenever you are:

- Creating or modifying a Next.js 16+ project that uses the App Router.
- Adding or reorganizing routes, layouts, or nested segments under /app.
- Deciding between server and client components.
- Setting up shared UI like navigation bars, sidebars, and footers.
- Implementing loading, error, or not-found states for routes.

This Skill is generic and must work for any Next.js App Router project,
not just a single repo.

## Project assumptions

- Framework: Next.js 16+ with the App Router enabled.
- Language: TypeScript is preferred by default.
- Styling: Tailwind CSS is recommended but not required; structure
  must not depend on a specific CSS solution.
- Build: Uses the standard Next.js build and dev commands
  (`next dev`, `next build`, `next start`).

Do not assume any specific backend or API stack unless the user provides it.

## File and folder conventions

- Use the `/app` directory as the main routing entrypoint.
- At minimum, the root route should have:
  - `app/layout.tsx` – root layout with `<html>` and `<body>`.
  - `app/page.tsx` – main landing page for `/`.
- For additional routes:
  - Use nested folders: `app/<segment>/page.tsx`.
  - Use `layout.tsx` inside folders that need shared UI for a route group.
- Co-locate components where it makes sense:
  - Shared, reusable UI components → `app/(components)` or `/components`.
  - Route-specific components → inside that route folder.
- Use route groups `(group-name)` to organize complex apps without changing the URL when needed.

## Server and client component rules

- Default to **Server Components** for all pages and layouts unless:
  - The component needs browser-only APIs (window, document, localStorage).
  - The component needs interactive state (useState, useEffect, etc.).
- Only mark components with `"use client"` when there is a clear reason.
- Never put `"use client"` at the top of large layout files that render
  mostly static or server-fetched content; instead, isolate client
  components and import them into server components.

## Routing, layouts, and navigation

- Every major section of the app should use a layout:
  - root `app/layout.tsx` for global structure, fonts, and providers.
  - child `layout.tsx` files for areas that share navigation or sidebars.
- Use the Next.js `<Link>` component for internal navigation.
- For auth-protected areas, prefer a separate segment (e.g. `app/(app)/...`)
  or a layout that checks session state before rendering children.

## Loading, error, and not-found states

- For any route that performs async data fetching, provide:
  - `loading.tsx` – skeleton or spinner while data is loading.
  - `error.tsx` – error boundary for route-specific failures.
- Use `not-found.tsx` when a route needs a custom 404 page.

Each of these files should be small, focused components that can be reused
or styled consistently across the app.

## Data fetching and API usage

- Prefer using **Server Components** with async functions for data fetching
  when possible.
- For client-side data fetching, use a dedicated abstraction (e.g. a
  custom hook or API client module) instead of calling `fetch` inline
  in many places.
- Keep base URLs and API configuration in a single place (e.g. `lib/api.ts`)
  and import from there.

## Environment variables and configuration

- Use typed, centralized access to environment variables:
  - Shared config file (e.g. `lib/config.ts`) that reads from `process.env`.
- Never access environment variables directly in many scattered files.
- Clearly separate server-only env vars and client-safe env vars.

## Things to avoid

- Mixing unrelated concerns in a single large file; prefer small, focused
  components and layouts.
- Deeply nested route hierarchies without clear layout purposes.
- Overusing `"use client"` and turning everything into a client component
  without need.
- Hard-coding API URLs or magic strings all over the codebase.

## References inside the repo

Whenever possible, this Skill should use project-local references if
they exist, for example:

- `@/app/layout.tsx` – root layout
- `@/app/page.tsx` – home page
- `@/lib/api.ts` – API client module
- `@/components/...` – shared components

If these files are missing, propose creating them using the structure
described above instead of inventing a completely new layout.
