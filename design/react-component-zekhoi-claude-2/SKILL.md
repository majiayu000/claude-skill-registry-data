---
name: react-component
description: Implement or change React components and hooks following the project's own patterns, with accessible markup, correct state and effect handling, and Testing Library tests. Use when the user asks to add, change, or fix a component, hook, form, or client-side UI behavior in a project that uses React. Do not use for server endpoints or API routes (use agent-kit:fastify-api or agent-kit:feature-implementation), for Vue, Svelte, or other frameworks, or for reviewing code (use agent-kit:code-review).
---

# React component implementation

## 1. Learn the project's patterns

- Find the React version, the framework if any (Next.js, Remix, Vite), TypeScript settings, and how components are styled (CSS modules, Tailwind, a component library).
- Read a similar existing component and its test. Follow its file layout, naming, prop typing, state management (local state, context, a store, a data-fetching library), and test style.

## 2. Implement

- Keep components small and props typed. Derive values during render instead of copying props into state; lift state only as far as needed.
- Use semantic elements: `button` for actions, `a` for navigation, `label` tied to every form input, headings in order. Interactive elements must work with the keyboard and have an accessible name; do not put click handlers on a `div`.
- Use effects only to synchronize with something outside React. Give every effect correct dependencies and a cleanup for subscriptions, timers, and in-flight requests (`AbortController`) so unmounting or changed inputs do not set stale state.
- Give list items stable keys from the data, not the array index when items can reorder.
- Handle loading, empty, and error states that the data can produce. Never render untrusted HTML with `dangerouslySetInnerHTML` without sanitizing it.
- In Next.js App Router projects, add `"use client"` only to components that need state, effects, event handlers, or browser APIs.

## 3. Test

- Test with Testing Library from the user's perspective: query by role, label, or text (`getByRole("button", { name: "Save" })`), interact with `user-event`, and assert on visible output, not implementation details or internal state. If Testing Library's automatic cleanup is not active (for example Vitest without `globals`), call `cleanup` after each test.
- Cover the main interaction, the loading, empty, and error states, and keyboard access where it matters. Mock network calls at the boundary the project already uses.
- Run the project's tests, type check, and linter.

## 4. Report

Summarize the components and hooks added or changed, the states handled, the tests and their results, and any assumptions the user should confirm, such as design details not present in the codebase.

## Examples

- Use: "Add a search box that filters the user list." "Fix the modal so Escape closes it." "Add a useDebounce hook."
- Skip: "Add a GET /users endpoint." "Review src/components/UserList.tsx." "Build this in Vue."
