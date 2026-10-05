---
name: mk:typescript
description: Use when writing TypeScript code, fixing type errors, or configuring strict type safety. Auto-activates on .ts/.tsx files. Covers null handling, utility types, and ESLint.
source: aura-frog
original_skills:
  - typescript-expert
  - frontend-development (TS parts)
adapted_for: claude-code
keywords:
  - typescript
  - type-errors
  - strict-types
  - null-handling
  - utility-types
  - ts-eslint
when_to_use: Use when writing TypeScript or fixing type errors / configuring strict type safety. Auto-activates on .ts/.tsx files. NOT for framework-specific patterns (see mk:vue / mk:angular / mk:react-patterns).
user-invocable: true
owner: utility
criticality: medium
status: active
runtime: claude-code
---

<!-- Improvements over source skills:
- Split from 361-line monolith to SKILL.md + references/ (Phase 1: CLASS A)
- Framework-agnostic (removed React-specific patterns from frontend-development)
- Integrated with security-rules.md (no `any` types already enforced)
- Added workflow phase anchoring (Phase 3 Build)
-->

# TypeScript Expert

Strict TypeScript patterns for type safety, null handling, and modern best practices.

## When to Use

**Auto-activate on:** `.ts`, `.tsx`, `.js`, `.jsx` files, type errors, ESLint issues, "fix types", "add types", "TypeScript help"

**Explicit:** `/mk:typescript [concern]`

**Do NOT invoke for:** Vue-specific patterns (use mk:vue), visual design (use mk:frontend-design)

## Workflow Integration

Operates in **Phase 3 (Build GREEN)**. Output supports the `developer` agent.

## Process

1. **Detect concern** — type error? new code? refactor? ESLint config?
2. **Load relevant reference** — strict-null, type-safety, utility-types, or eslint
3. **Apply patterns** — implement using strict TS patterns from references
4. **Verify** — `npx tsc --noEmit` must pass with zero errors

## Core Rules (always apply)

- **NEVER** use `any` — use `unknown` + type guards (security-rules.md)
- **NEVER** use `type assertion` — use `unknown` + type guards (security-rules.md)
- **NEVER** use implicit truthiness for null checks — use explicit `=== null || === undefined`
- **ALWAYS** use strict TypeScript config: `strict: true`, `noUncheckedIndexedAccess: true`
- **ALWAYS** use `type` imports: `import type { X } from 'y'`
- **PREFER** named exports over default exports
- **PREFER** discriminated unions over type assertions

## Anti-Patterns

| Don't                         | Do Instead                                   |
| ----------------------------- | -------------------------------------------- |
| `as any` or `as unknown as X` | Proper type narrowing with guards            |
| `if (value)` for null check   | `if (value !== null && value !== undefined)` |
| `export default`              | `export const X` / `export function X`       |
| `Object` type                 | `Record<string, unknown>`                    |
| Implicit return types         | Explicit return type annotations             |
| `enum` (runtime overhead)     | `as const` satisfies or union types          |

## Output Format

```
## TypeScript: {concern}

**Files:** {list of .ts/.tsx files modified}
**Config:** {tsconfig changes if any}

### Changes Applied
{numbered list of type improvements}

### Verification
{tsc --noEmit output — must show 0 errors}
```

## References

| Reference                                                 | When to load     | Content                                                         |
| --------------------------------------------------------- | ---------------- | --------------------------------------------------------------- |
| **[strict-patterns.md](./references/strict-patterns.md)** | Type safety work | Null handling, discriminated unions, type guards, utility types |
| **[review-checklist.md](./references/review-checklist.md)** | When reviewing TypeScript code | Prioritized checklist: CRITICAL (security), HIGH (type safety, async, errors), MEDIUM (React, perf) |

## Failure Handling

| Failure                            | Recovery                                                   |
| ---------------------------------- | ---------------------------------------------------------- |
| `tsc --noEmit` fails after changes | Fix errors before proceeding — never ship with type errors |
| No tsconfig.json found             | Suggest creating one with strict config                    |
| Third-party types missing          | `npm install @types/{package}`                             |

## Gotchas

- **`as` cast silences narrowing errors and hides real bugs** — `value as User` tells TS to trust you, not validate; a malformed API response passes the cast and crashes at runtime; use a type guard or Zod parse at the boundary instead.
- **`moduleResolution: "bundler"` breaks `import type` in non-bundler contexts** — tsconfig `moduleResolution: bundler` (Vite/esbuild default) allows extensionless imports that Node.js `--esm` rejects at runtime; flip to `nodenext` for backend code or keep dual configs per target.
- **`noUncheckedIndexedAccess: true` makes every array index `T | undefined`** — enabling this flag (required by strict config) means `arr[0]` is `string | undefined` not `string`; code that was type-correct before will error until every indexed access is null-guarded.
- **Declaration merging in ambient `.d.ts` files silently adds properties to global types** — a `declare module 'express'` block in any `.d.ts` in the project augments Express's types globally; two libraries doing this with conflicting shapes cause TS2300 duplicate identifier errors that appear far from the source.
- **Template literal types create unique brands that break assignability** — `type UserId = \`user_\${string}\`` is not assignable from `string`; passing a plain `string` where `UserId` is expected fails even though values look identical at runtime; always brand at the input boundary with a parse function.
- **`enum` generates runtime JS objects, causing tree-shaking failures** — enums are not erased; a `const enum` inside a library published as `.js` is inlined at compile time but not consumable by projects that don't re-compile the source; use `as const` satisfies patterns for exported enums.
