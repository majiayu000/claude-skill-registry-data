---
name: frontend-patterns
description: 'Guides React and Next.js component architecture and performance. Use when composing components, managing React state, or optimizing rendering and accessibility.'
---

# Frontend Development Patterns

Non-obvious React/Next.js rules. Standard React API usage is assumed.

## When to Activate

- Building or reviewing React components, hooks, or state
- Fetching data or choosing client versus server state
- Optimizing rendering, bundle size, or long lists
- Building forms, error handling, dialogs, or animation

## Critical Rules

- Compose with children and slots; derive values instead of mirroring them in state.
- Server data belongs in TanStack Query, SWR, or framework data APIs, not global stores.
- Effects clean up timers, listeners, subscriptions, and stale async results.
- Keys are stable data IDs, never indexes, for reorderable or removable lists.
- Memoize after profiling, not speculatively.
- Prefer native elements and Radix/Headless UI over custom ARIA widgets.
- Interactive elements need keyboard access, visible focus, and an accessible name.
- Validate on the server even when the client validates.
- Honor `prefers-reduced-motion`; animate transform/opacity only.

## References

Paths are relative to this SKILL.md's directory. Read only the file matching the task. If a file cannot be read, say so.

- [references/components-and-state.md](references/components-and-state.md)
  Read when: writing compound components, render props, custom hooks, or context reducers, or choosing a state library.
- [references/data-and-performance.md](references/data-and-performance.md)
  Read when: fixing async races, or deciding on memoization, lazy loading, or virtualization.
- [references/forms-errors-a11y.md](references/forms-errors-a11y.md)
  Read when: building forms, error boundaries, keyboard navigation, or modal focus handling.
- [references/animation.md](references/animation.md)
  Read when: adding Framer Motion list or modal transitions.

## Quick Routing

| Situation                     | Choose                            |
| ----------------------------- | --------------------------------- |
| Slot-based UI                 | Composition / compound components |
| Shared logic                  | Custom hook                       |
| Small shared state            | `useReducer` + Context            |
| Larger client state           | Zustand or Redux Toolkit          |
| Server state                  | TanStack Query or SWR             |
| Lists over a few hundred rows | `@tanstack/react-virtual`         |
| Forms                         | react-hook-form + Zod             |
| Dialog/popover/menu           | Radix or Headless UI              |

## Anti-Patterns

- Syncing state with effects when a derived value works.
- One big Context value rerendering all consumers.
- Fetching in `useEffect` without ignoring superseded requests.
- Fresh object or function literals passed to memoized children.
- `div` click handlers instead of `button` or `a`.

## Related ycc Skills

- `ycc:frontend-design` — visual direction, typography, color, and motion intent to pair with these implementation patterns
