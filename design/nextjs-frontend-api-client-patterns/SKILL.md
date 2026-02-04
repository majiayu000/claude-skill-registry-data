---
name: nextjs-frontend-api-client-patterns
description: >
  Standard patterns for HTTP/API clients in Next.js 16+ App Router
  frontends: where to put the client, how to type it, how to handle
  errors, and how to attach auth headers in a reusable way.
---

# Next.js Frontend API Client Patterns Skill

## When to use this Skill

Use this Skill whenever you are:

- Creating or modifying the code that calls a backend API from a Next.js
  16+ App Router frontend.
- Designing how the frontend talks to any HTTP/REST/JSON API
  (FastAPI, Node, Go, etc.).
- Adding new API functions (getTasks, createTodo, updateProfile, etc.).
- Improving error handling, typing, or auth token handling for API calls.

This Skill must work for **any** Next.js App Router project that calls a
backend over HTTP, not just a single repo.

## Core goals

- All API calls go through **one central client module** instead of being
  scattered `fetch` calls across the app.
- API requests and responses are **strongly typed** with TypeScript.
- Error handling is **consistent** and predictable for UI components.
- Auth headers (e.g. JWT Bearer tokens) are attached in one place,
  not manually per call.
- The pattern is **reusable** across many projects with minimal changes.

## File and module conventions

- Place the main client in a dedicated module, for example:

  - `src/lib/api.ts` or
  - `app/(lib)/api.ts`

  Adjust the exact path to match the project, but keep a **single, obvious**
  API entrypoint.

- Export functions from this module with clear names, such as:

  - `getTasks()`, `createTask(payload)`, `updateTask(id, payload)`,
    `deleteTask(id)`, etc.
  - `getUserProfile()`, `updateUserProfile(payload)`, etc.

- Do not call `fetch` or low-level HTTP functions directly from pages
  or components unless there is a very strong reason. Prefer calling
  the functions exposed by the API client module.

## HTTP client choices

- Default to the **built-in `fetch`** API in Next.js:

  - Use `fetch` in server components for server-side data fetching.
  - Use `fetch` or a small wrapper in client components when
    client-side fetching is required (e.g. in hooks).

- If a third-party client (axios, ky, etc.) is used, it must be
  configured in a single place and then imported from there.
  Do not configure clients in multiple files.

## Typing requests and responses

- For each API function, define TypeScript types or interfaces that
  describe:

  - The request payload (if any).
  - The expected response shape.

- Prefer importing shared types from a central `types` module if the
  project has one; otherwise, define local types next to the API
  client code.

- Do not use `any` for API responses. If the schema is not yet stable,
  start with minimal but meaningful types (e.g. `Task`, `User`, `ApiError`).

## Error handling patterns

- Wrap API calls in helper functions that translate low-level HTTP errors
  into a consistent error shape for the UI.

- Define a simple error model, for example:

  - `{ message: string; status?: number; details?: unknown }`

- On non-2xx HTTP status codes:

  - Parse the response body (if JSON) and map it to the error model.
  - Throw or return a predictable error object that components can use
    to show messages.

- Do not scatter `try/catch` with custom logic in every component.
  Centralize error interpretation inside the API client.

## Auth and headers

- Do not manually attach auth headers (e.g. `Authorization: Bearer ...`)
  in every component.

- Provide a single place in the API client where headers are built:

  - For example, a helper that receives a token or session and returns
    the appropriate `headers` object.
  - Or a wrapper function that reads the token from a trusted source
    (e.g. cookies, session object) and attaches it.

- Keep the pattern **generic**:

  - The Skill should not assume a specific auth provider name.
  - It may refer to “JWT Bearer token in the Authorization header” as
    a common pattern.

## Server vs client usage

- For **Server Components**:

  - Prefer direct `fetch` calls with server-side environment variables
    and base URLs.
  - Use the same API client module, but ensure any client-only code
    (window, localStorage) is not used.

- For **Client Components**:

  - Expose simple, typed functions or hooks (e.g. `useTasks`) that call
    the central API client and manage loading/error state.

- Do not mix server-only and client-only logic in the same file.
  Keep server and client concerns clearly separated.

## Base URL and configuration

- Store the API base URL and other configuration in a single place:

  - e.g. `lib/config.ts` with:

    - `API_BASE_URL`
    - any feature flags or environment-dependent settings.

- Never hard-code full URLs all over the codebase.
- Central configuration makes it easy to switch between local, staging,
  and production backends.

## Caching and revalidation (optional)

- When using Next.js data fetching in server components, respect the
  project’s chosen caching strategy:

  - `cache: "no-store"` for always-fresh data.
  - `next: { revalidate: N }` for periodic revalidation.

- Keep these options close to the API client so behaviour is consistent
  for all callers.

## Things to avoid

- Copy-pasting raw `fetch` calls into many components with slightly
  different error handling and headers.
- Returning raw `Response` objects from the API client; prefer returning
  typed data or throwing a clear error.
- Mixing multiple different HTTP client libraries in the same project.
- Hard-coding tokens, secrets, or environment-specific URLs in
  components or pages.

## References inside the repo

Whenever possible, this Skill should align with the project’s existing
conventions, for example:

- `@/lib/api.ts` or similar central API client module.
- `@/lib/config.ts` or `.env`-backed configuration helpers.
- Shared types under `@/types` or `@/lib/types`.

If these files are missing, propose creating them using the patterns
described above instead of inventing a completely new API access style.
