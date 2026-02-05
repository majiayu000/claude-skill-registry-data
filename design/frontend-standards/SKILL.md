---
name: frontend-standards
description: React patterns and frontend best practices for this project. Use when implementing React components, hooks, routes, styling, or client-side logic in packages/client.
---

# Frontend Standards

## Key Principles

- **Avoid useEffect** - Use TanStack Query, useSyncExternalStore, or event handlers instead
- **Prefer Suspense** - For loading states and async boundaries
- **useSyncExternalStore** - For external state subscriptions (WebSocket, global stores)
- **Server is the source of truth** - Don't maintain conflicting client state

## Tech Stack

- React 18, TanStack Router, TanStack Query, Tailwind CSS, xterm.js, Valibot

## React Best Practices

- **Suspense Usage** - Prefer Suspense for async operations over manual isLoading flags
- **useEffect Discipline** - Challenge every useEffect: could it be derived value, event handler, or useMemo?
- **Icon Components** - SVG icons belong in `Icons.tsx`, not inline in View components
- **External State** - Use `useSyncExternalStore` for singleton/global state, not useEffect subscriptions
- **Query Key Management** - Use consistent key factories, ensure complete invalidation

## Detailed Documentation

- [react-patterns.md](react-patterns.md) - React patterns (useEffect alternatives, Suspense, state management)
- [frontend-standards.md](frontend-standards.md) - Directory structure, TanStack Router/Query, React best practices, styling
