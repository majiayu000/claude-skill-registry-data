---
name: Frontend Components
description: Structure React 19+ components following best practices for organization, state management, props handling, and code readability with top-down structure and single responsibility principle. Use this skill when creating new React components, refactoring existing components, organizing component logic, managing component state, defining prop interfaces (IComponentProps with I prefix), or implementing component patterns. Apply when working on React component files (*.tsx, *.jsx), Shadcn/ui components, or any frontend component implementations. This skill ensures predictable top-down structure (imports → types/interfaces → component → hooks → derived values → JSX), proper props destructuring with defaults in function signature, manageable component size (split at >300 lines), composition via Shadcn Slot pattern (asChild prop), React 19 patterns (use() hook for promises, useActionState for forms, useOptimistic for immediate feedback), no manual useMemo/useCallback (React Compiler handles memoization), Server Components as default for data fetching, early returns for loading/error states, and components that pass the scroll test.
---

# Frontend Components

## When to use this skill:

- When creating new React components with React 19+ features
- When refactoring large components into smaller ones (>300 lines)
- When organizing component structure and code order (top-down readability)
- When defining component props with TypeScript interfaces (IComponentProps)
- When implementing state management with useState, useOptimistic, or Zustand
- When using composition patterns with Shadcn/ui Slot and asChild prop
- When handling conditional rendering and early returns
- When using React 19 Actions API (useActionState, useFormStatus) for forms
- When using the use() hook to unwrap promises in Server Components
- When extracting reusable component logic into custom hooks
- When working on component files (*.tsx, *.jsx, components/*.*)
- When reviewing component structure for readability (scroll test)
- When deciding between local state, lifted state, or global state (Zustand)
- When implementing optimistic UI updates with useOptimistic

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle frontend components.

## Instructions

For details, refer to the information provided in this file:
[frontend components](../../../agent-os/standards/frontend/components.md)
