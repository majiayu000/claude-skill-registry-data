---
name: routing-state
category: frontend
description: Use when adding routes or deciding where state lives - carry resource ids and navigation-surviving state in the URL, keep route components thin, and lift shared state to a hook not a global store
tech_stack: React
---
# Routing & State

## Overview

Where state lives decides whether a view is deep-linkable and refresh-safe. The recurring defects are navigation-surviving state (a selected tab, a filter) trapped in component state that resets on refresh, and fat route components.

**Core principle:** If it should survive a refresh or be shareable by URL, it lives in the URL.

## Rules

- **`react-router-dom`** for navigation; URL params carry resource ids so views are deep-linkable and refresh-safe.
- **State that survives navigation** (filters, selected tab, search) lives in the URL search params — not component state.
- **Lift shared state into a custom hook** when multiple pages need it; avoid a global store for what two components can share via props.
- **Route components stay thin:** data loading + layout only; behavior lives in child components and hooks.

## Worked Example

```tsx
// ❌ selected filter lost on refresh, not shareable
const [status, setStatus] = useState("all");

// ✅ filter in the URL — refresh-safe, shareable, back-button works
const [params, setParams] = useSearchParams();
const status = params.get("status") ?? "all";
const setStatus = (s: string) => setParams(prev => { prev.set("status", s); return prev; });
```

Now `/board?status=in_progress` deep-links to the filtered view and survives a refresh.

## Common Mistakes

- A filter/tab in `useState` that resets on refresh and can't be shared.
- A global store for state two sibling components could pass via props.
- A route component packed with behavior instead of delegating to children/hooks.

## Red Flags

- A shareable view state that isn't in the URL.
- A new global store for a two-component concern.
- A route component you scroll to read.
