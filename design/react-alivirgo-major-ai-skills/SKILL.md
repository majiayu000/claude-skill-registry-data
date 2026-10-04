---
name: react
description: "Build accessible React interfaces with function components, hooks, and deliberate state ownership; troubleshoot effects, list keys, and interactive behavior."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["react", "hooks", "components", "frontend", "a11y", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# React UI Engineering AI Skill Guide

## Overview & Engine Architecture

React models UI as a tree of function components that return elements. State updates schedule re-renders; hooks let components subscribe to state, context, and lifecycle-like effects. Agents keep components pure where possible, minimize effect churn, choose controlled vs uncontrolled inputs deliberately, and ship accessible markup (labels, roles, keyboard support).

```
Component tree
  -> render (pure-ish)
      -> hooks state / context
          -> commit to DOM
              -> effects run
```

## When to use this skill

- Building UI components and forms
- Refactoring prop-drilling into composition or context (sparingly)
- Fixing effect infinite loops and stale closures
- Improving accessibility of interactive controls

## Operational directives

1. Derive values during render instead of mirroring props into state.
2. List `useEffect` dependencies correctly; do not empty the array to "run once" if you read changing values.
3. Give stable unique `key`s (IDs), never array index for reorderable lists.
4. Prefer composition (`children`) over boolean prop sprawl.
5. Interactive controls need keyboard access and visible focus.

## Patterns

Controlled input:

```tsx
function Search({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <label>
      Search
      <input value={value} onChange={(e) => onChange(e.target.value)} />
    </label>
  );
}
```

Avoid effect for derived state:

```tsx
// Bad: syncing fullName into state from props
// Good:
const fullName = `${user.first} ${user.last}`;
```

## Common bugs

| Bug | Cause | Fix |
| --- | --- | --- |
| Infinite re-render | Effect sets state that retriggers effect | Remove cycle; derive or gate |
| Stale event handler | Missing deps / wrong memo | Fix deps or use functional updates |
| Lost input focus | Unstable keys remounting | Stable keys; don't remount parents |
| a11y fail | Click-only div buttons | Use `<button>` / proper roles |

## Best practices

- Colocate state with the lowest common consumer.
- Use error boundaries for recoverable UI regions.
- Test behavior with Testing Library (role/text queries).
- Keep side effects (network) in dedicated hooks or server layers.

## Limitations

- Concurrent features and framework integrations (Next.js) change data-fetching defaults.
- Global state libraries (Redux, Zustand) need team conventions beyond this skill.
- CSS strategy (CSS modules, Tailwind, etc.) is orthogonal.

## Related skills

- `@nextjs` - React within App Router constraints
- `@typescript` - typing props and hooks
- `@playwright` - end-to-end UI verification
