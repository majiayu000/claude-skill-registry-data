---
name: state-management
description: "Client-side state management, normalized store schemas, selector memoization, and race-condition prevention in async flows."
---

# State Management & Store Hygiene Protocol

When managing application state in React, Vue, Svelte, or native web components, adhere to these rules.

---

## 1. Normalized State Shape

1. Treat client state stores like relational databases:
   - Normalize collections into byId objects and allIds arrays.
   - Avoid deep nested object hierarchies that cause unnecessary re-renders.
2. Separate Server State (cached server queries) from Client State (UI toggles, form drafts). Use dedicated query caching for server state.

---

## 2. Selector Memoization

1. Never compute expensive derived data inline in view components.
2. Use memoized selectors (e.g. createSelector, computed) to prevent recalculating filters or sorts on unrelated state updates.

---

## 3. Async Race Condition Prevention

1. Always cancel in-flight HTTP requests using AbortController when an input changes or a component unmounts.
2. Discard stale responses if a newer action has been dispatched before the previous request resolved.
