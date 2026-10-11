---
name: state-management
description: Manage frontend application state predictably across local UI state, global app state, server state, cached data, loading states, error states, empty states, form state, filter state, pagination, authentication state, URL state, navigation state, derived state, optimistic updates, cache invalidation, logout cleanup, and tenant/shop scope. Use when Codex needs to fix stale data, inconsistent UI, duplicated state, repeated API calls, incorrect filters/search/pagination, confusing loading/error behavior, parent-child state flow, modal-to-parent updates, auth state shared across screens, cache refresh after create/update/delete actions, optimistic updates, or mobile screens retaining old data after logout.
---

# State Management

Use this skill when frontend data flow, caching, state ownership, or UI consistency is part of the task.

## Core Rule

Classify the state before adding or moving it. Keep state close to where it is used, use existing project patterns, and avoid global state unless the data is truly shared across unrelated screens or app-wide behavior.

## Workflow

1. Understand the state problem:
   - affected screen or feature, data involved, user action that changes it, readers, writers, API source, persistence needs, reset needs, and whether data is stale, duplicated, missing, or inconsistent
2. Classify state types:
   - local UI, form, server, global app, URL, navigation, and derived state
3. Inspect existing state patterns:
   - `useState`, `useReducer`, context, Redux, Zustand, MobX, React Query, SWR, Apollo, Vuex, Pinia, signals, custom hooks, auth store, API cache utilities, URL query state, form libraries, local storage, or secure storage
4. Decide the correct state location:
   - local component, parent component, custom hook, server-state cache, global store, URL query, route params, or storage
5. Define ownership:
   - state name, owner, readers, writers, initial value, update trigger, reset trigger, persistence rule, and cleanup behavior
6. Avoid duplicate state:
   - do not store the same server data in component state, global store, and cache unless there is a clear reason
7. Handle server state through the existing project pattern:
   - fetching, caching, refetching, invalidating, loading, errors, empty state, pagination, filters, sorting, background refresh, optimistic updates, and conflict handling
8. Define cache or query keys:
   - include all parameters that change the result, especially user, role, shop, tenant, filters, search, sort, page, and date range
9. Define invalidation rules:
   - refresh only related queries after create, update, delete, archive, status change, assignment, payment update, login/logout, shop/tenant switch, permission change, filter reset, or successful form submission
10. Handle loading, error, and empty states:
   - distinguish initial loading, background refetch, submit loading, pagination loading, network/API errors, validation errors, unauthorized errors, and valid empty results
11. Use optimistic updates carefully:
   - only when success is likely, rollback is simple, conflict risk is low, and project patterns support it
12. Avoid storing derived state unless justified:
   - compute totals, labels, filtered lists, full names, and formatted values from source data where practical
13. Keep form draft state separate from saved server state.
14. Clear auth and scope-specific state on logout or account/shop/tenant switch.
15. Add or update tests where practical.
16. Run relevant checks discovered from project scripts or docs.
17. Summarize state types, ownership, data flow, cache keys, invalidation, UI states, cleanup, checks, risks, and follow-up recommendations.

Read `references/state-management-checklist.md` for ownership tables, cache-key examples, invalidation guidance, optimistic update rules, cleanup checks, test ideas, and the final report format.

## Non-Negotiable Rules

- Do not add global state unless truly needed.
- Do not duplicate server data across multiple stores unnecessarily.
- Do not store derived state unless justified.
- Do not ignore loading, error, or empty states.
- Do not use weak cache keys that ignore filters, user, shop, tenant, or page.
- Do not forget cache invalidation after mutations.
- Do not use optimistic updates for high-risk actions without rollback.
- Do not mix form draft state directly with saved server state.
- Do not leak previous user, shop, tenant, or private data after logout or scope switch.
- Do not introduce a new state library unless explicitly approved.
- Do not break existing state management conventions.
- Do not clear unrelated state unnecessarily.
- Do not hide failed API updates by only changing frontend state.

## Output Contract

When using this skill, provide:

1. State problem or requirement.
2. State types involved.
3. State ownership table.
4. Data flow summary.
5. Cache/query keys.
6. Update and invalidation rules.
7. Loading, error, and empty state behavior.
8. Optimistic update decision and rollback behavior if used.
9. Auth/logout and tenant/shop scope cleanup.
10. Files changed.
11. Tests/checks or manual verification.
12. Risks and follow-up recommendations.
