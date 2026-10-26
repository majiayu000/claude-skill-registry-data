---
name: new-module
description: Scaffold a new feature slice in src/features/<name> with the canonical structure — public-API index, ui screen, model (Zod schema + Zustand store), lib, and colocated tests. Use whenever work needs a new feature module, the user says "new feature/module/slice", or /plan-feature's task T0 calls for it. Never hand-roll slice layouts.
argument-hint: [slice-name-kebab-case]
allowed-tools: Read Write Edit Glob Bash(npm run new:feature*) Bash(npm run lint*) Bash(npm run typecheck*) Bash(npm test*)
---

## Task

Scaffold `src/features/$ARGUMENTS/` by **running the generator, then mirroring the canonical slice** `src/features/tasks/` — read it first; it is the template.

1. **Generate the skeleton:** run `npm run new:feature -- $ARGUMENTS`. This creates:

```
src/features/$ARGUMENTS/
  index.ts                         ← public API (exports the screen; keep minimal)
  ui/$ARGUMENTS-screen.tsx         ← screen shell built from @/shared/ui (Screen, AppText, …)
  ui/                              ← (add more components here)
  model/                          ← (empty — add schema + store, below)
  lib/                            ← (pure helpers)
  __tests__/$ARGUMENTS-screen.test.tsx  ← render smoke test
```

2. **Add the model**, mirroring `src/features/tasks/model/`:
   - `model/schema.ts` — Zod schema for the slice's core entity + inferred types. Everything entering the slice (input, storage rehydration, network) validates through it (Constitution Art. IX).
   - `model/store.ts` — a Zustand store; subscribe via selectors, never store derived data (`docs/architecture/state-management.md`). For a painted-door experiment, the store's action is a no-op + counter that cannot mutate real state (`docs/process/painted-door.md`).
   - `__tests__/store.test.ts` — one real assertion per action.

3. **Rules that make the scaffold correct (not just present):**
   - `index.ts` is the entire public surface; deep imports from outside the slice fail ESLint (`boundaries/*`). No cross-feature or upward imports.
   - UI uses `className` + NativeWind only (`cn()` for conditionals), shared primitives from `src/shared/ui`, a designed empty state, and a `testID` (kebab-case, feature-prefixed) on every interactive/assertable element.
   - No route is created here; routes are thin composition in `src/app/` and belong to the feature's tasks.
   - User-facing copy uses typographic apostrophes (’) — docs-lint scans UI text.

4. **Finish:** run `npm run lint && npm run typecheck && npm test` (all green with the stubs), then list the created files and the next task from the spec's `tasks.md`.
