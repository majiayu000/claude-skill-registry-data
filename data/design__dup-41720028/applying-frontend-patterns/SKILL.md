---
name: applying-frontend-patterns
description: >
  Framework-agnostic frontend component design patterns. Triggers: React, Vue, Angular,
  コンポーネント, パターン, hooks, カスタムフック, container, presentational, 分離,
  状態管理, state management, composition, HOC, render props
allowed-tools: Read, Grep, Glob, Task
---

# Frontend Patterns

## Purpose

Component design patterns for maintainable frontend architecture. Patterns are universal; implementations differ by framework.

## Core Patterns Overview

| Pattern | Concept | When to Use |
| --- | --- | --- |
| Container/Presentational | Separate logic from UI | Data fetching + display |
| Custom Hooks (React) | Reusable stateful logic | Shared behavior across components |
| Composition | Build complex from simple | Flexible, reusable components |
| State Management | Organize application data | Local → Shared → Global |

## Container/Presentational Pattern

**Key Principle**: Separate concerns

| Container (Logic) | Presentational (UI) |
| --- | --- |
| Fetches data | Receives data via props |
| Manages state | Stateless (ideally) |
| Handles events | Calls callback props |
| No styling | All styling lives here |

**Application Rule**:

1. Start with Presentational (UI only, props-driven)
2. Add Container when logic is needed
3. Extract to custom hooks when reusable

## Hooks Guidelines (React)

| Hook | Use For | Pitfall to Avoid |
| --- | --- | --- |
| useEffect | Side effects | Missing dependencies |
| useMemo | Expensive computations | Premature optimization |
| useCallback | Stable function refs | Over-memoization |
| Custom hooks | Reusable logic | Not starting with `use` |

**Dependencies Rule**: Always include all values used inside the effect.

## State Management Strategy

| Scope | Tool (React) | Example |
| --- | --- | --- |
| Local | useState | Form input, toggle |
| Shared | Context | Theme, auth status |
| Global | Zustand/Redux | App-wide cache |

**Granularity Rule**: Split large state objects into separate states.

## Composition Patterns

| Pattern | Use Case |
| --- | --- |
| children | Wrapper components, cards, modals |
| render props | Dynamic rendering based on data |
| HOC | Cross-cutting concerns (auth, logging) |

## Framework Comparison

| Pattern | React | Vue | Angular |
| --- | --- | --- | --- |
| Separation | Container/Presentational | Composition API | Smart/Dumb |
| State | useState, Context | ref, reactive | Services |
| Side effects | useEffect | watch, onMounted | ngOnInit |
| Slots | children | slots | ng-content |

## When NOT to Use Patterns

- Simple one-off components
- Prototypes (YAGNI)
- No reuse expected

**Rule**: Add patterns when pain is felt, not anticipated.

## References

### Principles (rules/)

- [@~/.claude/rules/development/CONTAINER_PRESENTATIONAL.md](~/.claude/rules/development/CONTAINER_PRESENTATIONAL.md) - Component separation pattern

### Skill References

- [@./references/container-presentational.md](./references/container-presentational.md) - Detailed separation guide

### Related Skills

- `frontend-design` (official) - Visual design quality (typography, color, animation)
- `enhancing-progressively` - CSS-first progressive enhancement
- `integrating-storybook` - Component visualization

### Used by Commands

- `/code --frontend` - React component implementation
- `/audit` - Frontend pattern verification

### See Also

- `/example-skills:frontend-design` - Official skill for distinctive UI aesthetics
