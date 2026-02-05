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

## Detailed Documentation

- [react-patterns.md](react-patterns.md) - React patterns (useEffect alternatives, Suspense, state management)
- [frontend-standards.md](frontend-standards.md) - Directory structure, TanStack Router/Query, xterm.js, styling
