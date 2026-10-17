---
name: react-accessibility-performance
description: DEPRECATED for new standalone React/TypeScript work; use react-agent-skills / react-accessibility + react-performance instead. Select only to maintain existing work during the deprecation window. Use for React accessibility, keyboard and focus behavior, render performance, memoization, and virtualization decisions.
license: MIT
---

# React Accessibility and Performance

## Purpose
Treat accessibility and rendering performance as explicit behavioral constraints instead of cleanup tasks.

## Activate when
- adding interactive controls or custom widgets;
- fixing keyboard, focus, or screen-reader behavior;
- investigating unnecessary renders;
- introducing memoization or virtualization.

## Repository inspection
Inspect semantic HTML, focus utilities, design-system primitives, profiler evidence, list sizes, data identity, and existing performance budgets.

## Decision rules
- Prefer semantic native elements.
- Keyboard and focus behavior are part of the component contract.
- Do not memoize by reflex; identify a real identity or workload problem.
- Fix state ownership and unstable identities before broad memoization.
- Justify virtualization using workload characteristics.
- Preserve accessible names, labels, visible focus, and announced state.

## Implementation procedure
1. Identify interaction and rendering workload.
2. Verify semantics before custom behavior.
3. Define focus transitions.
4. Measure render hotspots.
5. Fix ownership and identity issues before memoization.
6. Add focused accessibility and performance regression checks.

## Anti-patterns / failure modes
- clickable divs used instead of buttons;
- focus traps without recovery;
- arbitrary memoization;
- virtualization that breaks interaction semantics;
- performance claims without evidence.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`).

```tsx
import { useDeferredValue, useId, useState } from "react";

// Labeled input, announced result count, and keyboard-reachable controls.
// useDeferredValue keeps typing responsive for a list measured to be slow;
// add it after profiling, not by default.
export function ProductFilter({ products }: { products: readonly string[] }) {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const inputId = useId();
  const matches = products.filter((name) => name.toLowerCase().includes(deferredQuery.toLowerCase()));

  return (
    <div>
      <label htmlFor={inputId}>Filter products</label>
      <input id={inputId} value={query} onChange={(event) => setQuery(event.target.value)} />
      <p role="status" aria-live="polite">
        {matches.length} {matches.length === 1 ? "result" : "results"}
      </p>
      <ul>
        {matches.map((name) => (
          <li key={name}>
            <button type="button">{name}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Agent review checklist
- Are native semantics preferred?
- Are keyboard and focus transitions explicit?
- What evidence justifies memoization or virtualization?
- Are accessibility regressions tested at the owning boundary?

## Verification
Use keyboard tests, accessible-role assertions, browser/integration checks when needed, and profiler or benchmark evidence for performance claims.

## Source foundation
- React Learn: https://react.dev/learn
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- React memo: https://react.dev/reference/react/memo
