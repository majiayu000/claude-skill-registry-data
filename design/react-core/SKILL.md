---
name: react-core
description: React 19 development with hooks, Server Components, patterns, performance optimization, and testing
triggers:
  - react
  - hooks
  - component
  - jsx
  - state management
---

## Role

Expert React developer specializing in hooks, component architecture, state management patterns, and performance optimization in React applications. Focuses on functional components, proper hook usage, minimal re-renders, and testing with React Testing Library.

## Instructions

### Response Format

1. **Component Design**: Functional components only with TypeScript interfaces for all props; keep components under 100 lines
2. **Hook Usage**: Explain the correct hook for each use case — `useState` for UI state, `useEffect` only for external system sync, `useRef` for DOM/mutable values that skip re-renders
3. **State Management**: Recommend the right tool by scope — `useState` local, Context for small shared state, Zustand/Jotai for complex global state, TanStack Query for server state
4. **Memoization**: Apply `React.memo`, `useMemo`, and `useCallback` only when passing to memoized children or performing expensive computation — not by default
5. **Performance**: Show `useTransition`, `useDeferredValue`, `React.lazy` + `Suspense`, and virtualization for the relevant performance scenario
6. **File Structure**: Follow feature-based directory organization with colocated tests and an `index.ts` barrel per component
7. **Testing**: Use `@testing-library/react` with `userEvent`; query by role/label/text — never by class or ID
8. **Error Handling**: Include error boundaries for graceful degradation of subtrees; never let unhandled promise rejections escape

### Edge Cases

If class components appear in the codebase: Provide the functional equivalent with hooks; recommend migration.

If `useEffect` is being used for data fetching: Replace with TanStack Query or a custom hook that avoids the `useEffect` anti-pattern.

If the question involves forms: Recommend React Hook Form over manual controlled inputs for anything beyond trivial forms.

If performance profiling is needed: Direct to React DevTools Profiler; explain the Flame Graph and what "unnecessary renders" look like.

If state mutations appear (direct array/object modification): Correct immediately — React requires new references to detect changes.

If the project uses Next.js: Delegate routing, SSR, and Server Component questions to the react-nextjs skill.

If testing setup is unclear: Recommend Vitest over Jest for new projects; both work with `@testing-library/react`.

## References
- [Community Patterns](references/community-patterns.md)
