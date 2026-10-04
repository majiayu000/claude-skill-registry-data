---
name: component-design
description: Design React/Next.js component APIs with clear Server/Client boundaries, composable patterns, and proper seam placement. Use when designing new components, refactoring existing ones, or deciding between Server/Client Component boundaries.
trigger: 需要设计可复用的组件
input: 设计稿或需求
output: 组件设计文档
next: styling-tailwind
dependencies: ui-ux-pro-max
---

# Component Design (Next.js)

Guiding principles for designing React components in Next.js App Router — focusing on API surface, composition, and the Server/Client boundary.

## Core Principles

### 1. Server Component by Default

Prefer Server Components unless you need interactivity (hooks, event handlers, browser APIs). Every component that can be a Server Component should be one.

```
app/page.tsx         → Server Component (data fetching, layout)
app/page.tsx         → Client Component only if interactive
components/button.tsx → Client Component (has state/events)
```

### 2. Push Client Boundaries Down

When you need a Client Component, make it as thin as possible. Wrap the interactive part in a Client boundary and keep everything else on the server.

```tsx
// ✅ Good: Server Component wraps minimal Client piece
// page.tsx (Server)
import { Comments } from './comments'
import { CommentList } from './comment-list'

export default function Page() {
  return (
    <div>
      <CommentList />           {/* Server: data fetching, rendering */}
      <Comments />              {/* Client: interactivity only */}
    </div>
  )
}
```

### 3. Interface First

Before writing implementation, define the component's **public interface**:

- Props (required vs optional, types)
- Children composition model (slots, render props, compound components)
- Ref forwarding strategy
- Loading, empty, error states

### 4. Test Through the Interface

If testing requires reaching into internal state or private methods, the interface is wrong. The public API should be the only test surface.

## Server/Client Component Decision Tree

```
Does the component need hooks, events, or browser APIs?
├─ No  → Server Component ✅
└─ Yes → Client Component
         ├─ Can the interactive part be isolated?
         │   ├─ Yes → Extract into a thin Client wrapper, keep rest Server ✅
         │   └─ No  → Make the whole thing Client, but keep it focused
         └─ Do you need to pass Server data to it?
             ├─ Yes → Pass as props from the Server parent
             └─ No  → Fetch inside the Client Component
```

## Seam Placement

A **seam** is where you can alter behavior without editing in that place. Good seams in Next.js:

| Seam | Purpose |
|------|---------|
| `layout.tsx` | Persistent shell, shared UI across routes |
| `loading.tsx` | Streaming fallback per route segment |
| `error.tsx` | Error boundary per route segment |
| `not-found.tsx` | 404 boundary per route segment |
| Component props | Polymorphism via different prop combinations |
| Slot props (`children`, named slots) | Composition over configuration |

## Checklist

- [ ] Can this be a Server Component? If yes, make it one
- [ ] Is the Client boundary as thin as possible?
- [ ] Are all states covered? (loading, empty, error, edge cases)
- [ ] Is the interface the only test surface?
- [ ] Is the component composable or configurable? (prefer composition)
- [ ] Does the naming reflect what it does, not how it renders?
- [ ] Could I delete this component without callers breaking unpredictably? (deletion test)