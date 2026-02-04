---
name: embedded-banking-architecture
description: Core architecture patterns for embedded-components monorepo. Use when creating new components, organizing code structure, or following 2025 React/TypeScript patterns. Keywords - component creation, file structure, hooks, utils, TypeScript, React patterns, monorepo, architecture.
compatibility: Designed for VS Code with TypeScript, React 18.x, requires embedded-components/ARCHITECTURE.md
metadata:
  version: "2.0.0"
  author: jpmorgan-payments
  lastUpdated: "2025-12-24"
  priority: critical
---

# Embedded Banking Architecture

## Overview

This skill provides the core architecture patterns for the embedded-components monorepo. **ALWAYS review `embedded-components/ARCHITECTURE.md` before generating any component code** - it is the source of truth.

## Repository Structure

Active development is in the `embedded-components/` package:

```
/
├── app/                    # Showcase web application (not active)
│   ├── client/            # Frontend React application
│   └── server/            # Backend server
├── embedded-components/    # Main UI component library (ACTIVE)
│   ├── src/               # Source code
│   ├── .storybook/        # Storybook configuration
│   └── public/            # Static assets and MSW worker
└── embedded-finance-sdk/   # TypeScript SDK utilities (not active)
```

## ⚠️ CRITICAL: Follow ARCHITECTURE.md

**All code generation MUST follow the patterns defined in `embedded-components/ARCHITECTURE.md`.**

Before generating any component code:
1. Read `embedded-components/ARCHITECTURE.md` for complete patterns
2. Follow the decision tree for code placement
3. Use the correct directory structure
4. Export minimal public API only

## Core Architecture Principles

### 1. Individual Hook/Util Files

- ✅ Each hook/util in its own file: `useHookName.ts`, `utilName.ts`
- ✅ Always use `hooks/` and `utils/` directories, even for single files
- ✅ Tests colocated: `useHookName.test.tsx` next to `useHookName.ts`
- ❌ NO monolithic files like `ComponentName.hooks.tsx`

### 2. Type Colocation

- **Central `.types.ts`**: ONLY public API (exported component props)
- **Component files**: Internal component props/interfaces
- **Hook files**: Hook options, return types
- **Util files**: Inline parameter types

```typescript
// ✅ Public API only
// ComponentName.types.ts
export interface ComponentNameProps { ... }

// ✅ Internal types colocated
// components/SubComponent.tsx
interface SubComponentProps { ... }

// hooks/useHook.ts
interface UseHookOptions { ... }
export function useHook(options: UseHookOptions) { ... }
```

### 3. No Aggregation Barrels

- ❌ NO `components/index.ts` exporting all components
- ✅ Direct imports for tree-shaking
- ✅ Barrel exports ONLY for: `hooks/index.ts`, `utils/index.ts`, component root `index.ts`

## Standard Component Structure

```
ComponentName/
├── index.ts                          # Public API exports only
├── ComponentName.tsx                 # Main component
├── ComponentName.test.tsx            # Colocated test
├── ComponentName.types.ts            # Public types ONLY
├── ComponentName.constants.ts        # Constants
│
├── hooks/                            # Individual files (flat)
│   ├── useData.ts
│   ├── useData.test.tsx
│   ├── useForm.ts
│   ├── useForm.test.tsx
│   └── index.ts                      # Barrel export
│
├── utils/                            # Individual files (flat)
│   ├── helper.ts
│   ├── helper.test.ts
│   └── index.ts                      # Barrel export
│
├── components/                       # NO index files
│   ├── SubCard/
│   │   ├── SubCard.tsx
│   │   └── SubCard.test.tsx
│   └── SubSkeleton/
│       ├── SubSkeleton.tsx
│       └── SubSkeleton.test.tsx
│
├── forms/                            # Only if .schema.ts exists
│   └── CreateForm/
│       ├── CreateForm.tsx
│       ├── CreateForm.test.tsx
│       └── CreateForm.schema.ts      # Zod schema
│
└── stories/
    └── ComponentName.story.tsx
```

## Import Patterns

```typescript
// ✅ CORRECT - Direct imports (tree-shakeable)
import { ComponentCard } from "./components/ComponentCard";
import { ComponentSkeleton } from "./components/ComponentSkeleton";
import { useComponentData } from "./hooks"; // Can use barrel for convenience

// ❌ WRONG - Aggregation barrel (prevents tree-shaking)
import { ComponentCard, ComponentSkeleton } from "./components"; // No index.ts!
```

## Code Organization Decision Tree

```
New Code?
  ├─→ Hook?
  │   ├─→ Used by 2+ components? → src/lib/hooks/useHookName.ts
  │   └─→ Used by 1 component? → ComponentName/hooks/useHookName.ts
  │
  ├─→ Utility?
  │   ├─→ Used by 2+ components? → src/lib/utils/utilName.ts
  │   └─→ Used by 1 component? → ComponentName/utils/utilName.ts
  │
  ├─→ Component?
  │   ├─→ Used by 2+ features? → src/components/ComponentName/
  │   └─→ Used by 1 feature? → ComponentName/components/SubComponent/
  │
  ├─→ Form?
  │   ├─→ Has .schema.ts? → ComponentName/forms/FormName/
  │   └─→ No schema? → ComponentName/components/DialogName/
```

## Public API Pattern

**Minimal, explicit exports in component root `index.ts`:**

```typescript
/**
 * ComponentName - Public API
 */

// Main component
export { ComponentName } from './ComponentName';

// Public types only
export type { ComponentNameProps } from './ComponentName.types';

// ❌ DON'T export internals:
// - Hooks, sub-components, utils, constants
```

## Technology Stack

- React 18.x with TypeScript (strict mode)
- Radix UI primitives for base components
- Tailwind CSS with `eb-` prefix for styling
- Tanstack React Query v5 for data fetching
- Zod for validation
- MSW for API mocking
- Storybook 8.x for component development

## Component Locations

New components MUST be placed in `embedded-components/src/core/` following the architecture pattern.

## Anti-Patterns to Avoid

❌ Aggregation barrel exports (`components/index.ts`)  
❌ Generic names in specific places (`RecipientCard.tsx` in `LinkedAccountWidget`)  
❌ All types in central file (only public API)  
❌ Forms without schemas (use `components/` instead)  
❌ Using `&&` in PowerShell (use `;` instead)  
❌ Missing `eb-` prefix on Tailwind classes  

## Key Principles

✅ Individual files for hooks/utils with colocated tests  
✅ Direct imports for components (no aggregation barrels)  
✅ Type colocation - only public API in `.types.ts`  
✅ Minimal public API - export only what consumers need  
✅ Start specific - move to shared only when used by 2+ components  
✅ Forms = schemas - no schema? It's a component, not a form

## References

- See `embedded-components/ARCHITECTURE.md` for complete patterns
- See `AGENTS.md` for agent-specific instructions
- See `.github/copilot/skills/component-testing/` for testing patterns
- See `.github/copilot/skills/styling-guidelines/` for CSS patterns
