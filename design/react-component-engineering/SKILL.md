---
name: react-component-engineering
description: DEPRECATED for new standalone React/TypeScript work; use react-agent-skills / react-component-engineering instead. Select only to maintain existing work during the deprecation window. Use when designing React component boundaries, props, composition, rendering contracts, and reusable UI architecture.
license: MIT
---

# React Component Engineering

## Purpose
Keep components small, explicit, composable, and aligned with a user-visible responsibility.

## Activate when
- creating or refactoring React components;
- designing props and composition;
- deciding controlled versus uncontrolled interfaces;
- reducing prop drilling or coupling.

## Repository inspection
Inspect component conventions, styling, routing/layout ownership, data-fetching infrastructure, design-system primitives, accessibility utilities, and test patterns.

## Decision rules
- Prefer semantic components with one clear responsibility.
- Prefer composition over boolean-prop explosion.
- Keep reusable components independent of application-specific data fetching where practical.
- Use controlled inputs when the parent owns state; use uncontrolled inputs when local DOM ownership is deliberate.
- Make loading, error, empty, and success states explicit.
- Keep important side effects outside purely presentational components.

## Implementation procedure
1. Define the component contract.
2. Separate data and state ownership from presentation.
3. Keep props minimal and intention-revealing.
4. Use composition for structural variation.
5. Add focused observable tests.
6. Verify keyboard and screen-reader behavior for interactive UI.

## Anti-patterns / failure modes
- components with unrelated responsibilities;
- dozens of boolean props;
- context used to hide ordinary dependency flow;
- reusable components tightly coupled to one endpoint;
- tests that assert internal implementation.

## Reference example

Type-checked with `tsc --strict` (plus `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes`).

```tsx
import type { ReactNode } from "react";

// Composition instead of a growing set of boolean props (isDanger, hasIcon, ...).
type CardProps = { title: string; actions?: ReactNode; children: ReactNode };

export function Card({ title, actions, children }: CardProps) {
  return (
    <section aria-labelledby={`${title}-heading`}>
      <header>
        <h2 id={`${title}-heading`}>{title}</h2>
        {actions}
      </header>
      {children}
    </section>
  );
}

// Controlled input: the parent owns the value; the component owns no copy.
type SearchFieldProps = { value: string; onChange: (value: string) => void };

export function SearchField({ value, onChange }: SearchFieldProps) {
  return (
    <label>
      Search
      <input type="search" value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}
```

## Agent review checklist
- Does the component have one coherent responsibility?
- Is state/data ownership explicit?
- Could composition replace flag-driven branching?
- Are observable interaction and accessibility behaviors tested?

## Verification
Run focused component tests, typecheck, lint, and relevant application integration tests.

## Source foundation
- React Learn: https://react.dev/learn
- React Reference: https://react.dev/reference/react
