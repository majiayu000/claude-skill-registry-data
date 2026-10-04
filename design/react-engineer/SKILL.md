---
name: react-engineer
description: >
  Implements production-ready React components and application logic from behavioral
  specifications. Activate when a task requires building, refactoring, or extending React
  components using Next.js, TypeScript, and Tailwind CSS. Handles component development,
  state management, data fetching, and local verification via scripts.
metadata:
  author: Mostafa
  tags: react, nextjs, typescript, tailwind, frontend, implementation
---

# React Engineer

## Overview

Implementation-focused engineering skill. Takes behavioral specifications (from the UI/UX Architect or directly from requirements) and produces clean, type-safe, production-ready React code — then verifies it locally before delivery.

## Skill Format

Every implementation produced by this skill follows a consistent approach:

- **Spec Review**: Parse and internalize the behavioral contract before writing a single line
- **Component Architecture**: Plan the component tree, props interface, and state boundaries
- **Implementation**: Build with strict TypeScript, Next.js conventions, and Tailwind CSS
- **Verification**: Run local scripts to lint, type-check, and test before finalizing

## When to Apply

Reference this skill when:
- Building new React components from a specification or requirement
- Refactoring existing components for performance, readability, or correctness
- Implementing complex state management or data fetching patterns
- Converting designs or wireframes into working Next.js pages
- Reviewing React code for best practices and potential issues
- Integrating third-party libraries into a React/Next.js codebase

## Core Workflow

Follow this sequence for every implementation:

### 1. Parse Specifications

- Read the behavioral specification thoroughly before writing code
- Identify every interaction state, accessibility requirement, and edge case
- Flag any ambiguities — do not guess; ask or document assumptions
- Cross-reference with the existing codebase for reusable patterns

### 2. Plan Component Architecture

| Decision              | Guideline                                                       |
|-----------------------|-----------------------------------------------------------------|
| **Server vs Client**  | Default to Server Components; use `'use client'` only when needed for interactivity, browser APIs, or hooks |
| **Component Granularity** | One responsibility per component; compose rather than bloat |
| **Props Interface**   | Strict TypeScript interfaces — no `any`, no implicit types      |
| **State Boundaries**  | Lift state only as high as necessary; co-locate when possible   |
| **Data Fetching**     | Server Components for initial data; client-side for mutations   |

### 3. Implement

Apply these standards throughout:

#### TypeScript

```typescript
// ✅ Correct: Explicit interfaces, strict types
interface UserCardProps {
  user: User;
  onSelect: (id: string) => void;
  variant?: 'compact' | 'expanded';
}

// ❌ Incorrect: Loose typing
interface UserCardProps {
  user: any;
  onSelect: Function;
  variant?: string;
}
```

#### Next.js Conventions

- Use the App Router directory structure (`app/`, not `pages/`)
- Co-locate related files: `page.tsx`, `layout.tsx`, `loading.tsx`, `error.tsx`
- Use `metadata` exports for SEO on every page
- Prefer `next/image`, `next/link`, and `next/font` over raw HTML equivalents

#### Tailwind CSS

- Use design tokens and theme extensions over arbitrary values
- Prefer semantic class composition via `@apply` in component stylesheets for complex patterns
- Ensure responsive design: mobile-first with `sm:`, `md:`, `lg:` breakpoints
- Support dark mode via `dark:` variants where applicable

### 4. Verify

Before finalizing any output:

1. Search for verification scripts in `${SKILL_ROOT}/scripts/`
2. If found, execute them via `Bash` capability:

```bash
# Typical verification sequence
npx tsc --noEmit                  # Type checking
npx eslint . --ext .ts,.tsx       # Linting
npx jest --passWithNoTests        # Unit tests (if configured)
```

3. Fix any issues surfaced by the scripts before delivering the final code

## Output Contract

- Output **only** code changes and file creations — no conversational filler
- Every file must include appropriate comments explaining non-obvious decisions
- All components must be fully typed with strict TypeScript (no `any` escape hatches)
- Accessibility attributes must match the behavioral specification exactly

## Guardrails

### Do

- **DO** follow the specification exactly — do not add unrequested features
- **DO** check for existing components, hooks, and utilities before creating new ones
- **DO** handle loading, error, and empty states for every data-dependent component
- **DO** use semantic HTML elements (`<nav>`, `<main>`, `<article>`, etc.)
- **DO** include `key` props on all list-rendered elements

### Don't

- **DON'T** use `any` type — find or create the correct type
- **DON'T** use `useEffect` for data fetching in components that can be Server Components
- **DON'T** inline complex logic in JSX — extract to named functions or hooks
- **DON'T** suppress TypeScript or ESLint errors with `@ts-ignore` or `eslint-disable`
- **DON'T** hardcode strings that should be configurable or translatable

## Quick Reference

### Component Checklist

```text
☐ Props interface defined with strict TypeScript
☐ Server/Client Component boundary correctly chosen
☐ All interaction states handled (loading, error, empty, success)
☐ Accessibility attributes applied (ARIA, keyboard, focus)
☐ Responsive layout verified (mobile, tablet, desktop)
☐ Dark mode support included (if applicable)
☐ Local verification scripts executed and passing
☐ No TypeScript errors, no lint warnings
```

### Problem → Pattern Mapping

| Problem                                | Pattern                                      |
|----------------------------------------|----------------------------------------------|
| Complex form with validation           | React Hook Form + Zod schema                 |
| List with pagination/infinite scroll   | Server Component + `useInfiniteQuery`         |
| Global UI state (modals, toasts)       | Zustand store with selectors                  |
| Server-side data with mutations        | Server Actions + `revalidatePath`             |
| Optimistic UI updates                  | `useOptimistic` hook                          |
| Shared layout across routes            | Next.js `layout.tsx` nesting                  |
| SEO metadata per page                  | `generateMetadata` export                     |
