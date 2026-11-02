---
name: create-module
description: Use when adding new logic to a frontend project (helper, hook, composable, wrapper, store) - routes it to the right layer (utils, libs, hooks, stores, feature folder) so components stay thin, with a unit test.
---

# Create Module

The everyday authoring move: you need new code — a helper, a hook, a wrapper, some logic. This skill routes it to the right layer with a clean boundary, so logic never accretes inside UI components.

**The rule everything serves:** components render and wire events; they hold no logic. Formatting, derivation, IO, business rules, and non-trivial effects live in a typed module the component *calls*.

## 1. Audit current state

```bash
ls src/utils src/libs src/hooks src/composables src/stores src/features 2>/dev/null   # which homes exist?
grep -rn "<the thing you're about to write>" src/ 2>/dev/null            # already exists? reuse, don't duplicate
grep '"@/\*"' tsconfig.json tsconfig.app.json 2>/dev/null                 # @/ alias present?
```

Read `.claude/stack-profile.md` if present: `frontend.framework` replaces the detection in step 2; `tests.layout` (`tests-dir` default | `colocated`) decides where the unit test goes in step 7; `package_manager` replaces `pnpm`.

**Prerequisites:** `set-up-frontend-structure` (the `utils/`, `libs/`, `hooks/`|`composables/`, `stores/` folders) and the `@/` alias (`configure-typescript`). If a home folder is missing, create it flat and note the deviation.

## 2. Detect framework
React → `src/hooks/`. Vue → `src/composables/`. The other homes (`utils/`, `libs/`, `stores/`) are identical.

## 3. Classify — where does it go?

**First: whose is it?** Code that belongs to one domain goes into `src/features/<domain>/` and the same table applies *inside* it (`features/todos/hooks/`, `features/todos/api/`, …). Code two or more features use goes into the root folders. No `features/` yet and this is the second domain → create `features/` now (see `../_shared/conventions.md`).

Then walk top to bottom; the first row that fits wins.

| What you're writing | Home | The boundary it exposes |
|---|---|---|
| Pure function — deterministic, no deps, no side effects | `src/utils/` | named export, explicit input/output types |
| Wraps a third-party lib, or does IO (fetch, storage, SDK) | `src/libs/` | a small seam surface; internals stay private |
| Stateful view logic — lifecycle, reads a store/query, returns handlers | `src/hooks/` \| `src/composables/` | returns data + handlers, never internals |
| Server data: key factory, `queryOptions`, fetch functions | `features/<d>/api/` (or `src/libs/queryKeys.ts` in a one-domain app) | `queryOptions` objects + a typed fetch function |
| Shared client UI state read across unrelated parts of the tree | `src/stores/` | one store per domain; inline selectors |
| Renders UI | a component in the right atomic layer | imports only from lower layers |

If a thing both **renders and computes**, that's two modules: a thin component + an extracted hook/util.

## 4. The thin-UI rule — extract logic out of components

A component should read like a description of its output. These are smells that logic must move:

- a non-trivial `useEffect` / `watch` → a hook/composable
- a `map`/`filter`/`reduce` chain over domain data → a `utils/` pure function
- inline `fetch` / `localStorage` / SDK calls → a `libs/` seam (or a query hook)
- date/number/currency formatting → a `utils/` `Intl` helper

## 5. Author it (extracted — React + Vue)

Pure helpers in `src/utils/` (framework-agnostic, trivially testable):
```ts
// src/utils/openTodos.ts
import type { Todo } from '@/libs/queryKeys';
export const openTodos = (todos: Todo[]): Todo[] => todos.filter((t) => !t.done);
```
```ts
// src/utils/formatCount.ts
export const formatCount = (n: number, noun: string): string =>
  `${n} ${noun}${n === 1 ? '' : 's'}`;
```

The hook/composable composes the query + the pure utils:
```ts
// React — src/hooks/useTodoSummary.ts
import { useTodos } from '@/hooks/useTodos';
import { openTodos } from '@/utils/openTodos';

export function useTodoSummary() {
  const { data: todos = [] } = useTodos({ status: 'all' });
  return { openCount: openTodos(todos).length };
}
```
```ts
// Vue — src/composables/useTodoSummary.ts
import { computed } from 'vue';
import { useTodos } from '@/composables/useTodos';
import { openTodos } from '@/utils/openTodos';

export function useTodoSummary() {
  const todos = useTodos({ status: 'all' });
  const openCount = computed(() => openTodos(todos.data.value ?? []).length);
  return { openCount };
}
```

The component is now just render:
```tsx
// React — src/components/molecules/TodoSummary/TodoSummary.tsx
import { useTodoSummary } from '@/hooks/useTodoSummary';
import { formatCount } from '@/utils/formatCount';

export function TodoSummary() {
  const { openCount } = useTodoSummary();
  return <p>{formatCount(openCount, 'open todo')}</p>;
}
```
```vue
<!-- Vue — src/components/molecules/TodoSummary/TodoSummary.vue -->
<script setup lang="ts">
import { useTodoSummary } from '@/composables/useTodoSummary';
import { formatCount } from '@/utils/formatCount';
const { openCount } = useTodoSummary();
</script>
<template><p>{{ formatCount(openCount, 'open todo') }}</p></template>
```

## 6. Boundary
No layer barrels: a root module is imported by its own path (`@/utils/openTodos`, `@/hooks/useTodos`). Inside a feature, `features/<d>/index.ts` exports only what other features need; everything else stays private, and other code imports `@/features/todos`, never a file inside it. One module, one responsibility; file name matches the primary export.

## 7. Unit test
Extraction's payoff — pure logic tests with zero setup. Default location `tests/unit/`; with `tests.layout: colocated`, write `src/utils/openTodos.test.ts` and import `./openTodos`:
```ts
// tests/unit/openTodos.test.ts
import { describe, it, expect } from 'vitest';
import { openTodos } from '@/utils/openTodos';

describe('openTodos', () => {
  it('keeps only not-done todos', () => {
    const todos = [
      { id: '1', text: 'a', done: false },
      { id: '2', text: 'b', done: true },
    ];
    expect(openTodos(todos)).toEqual([{ id: '1', text: 'a', done: false }]);
  });
});
```
(`tests/unit` runs in Node — see `configure-test-stack`.)

## 8. Graduation
- A `utils/` helper that grows a third-party dependency → move it to `libs/` (it's now a wrapper, not a pure helper).
- Logic accreting inside a component → pull it into a hook (stateful) or a util (pure) the moment it stops being trivial.

## 9. Verify
```bash
pnpm typecheck                                 # the module + its consumers type-check
pnpm vitest run tests/unit/openTodos.test.ts   # the unit test passes (if configure-test-stack ran)
```

## References
- ./module-patterns.md — the thin-UI rule, the decision table, the typed-surface boundary, pure-by-default, the graduation rule, and when a feature folder beats layers.
- ../set-up-frontend-structure/SKILL.md — the folders this routes into.
- ../_shared/conventions.md — naming, barrels, `libs/` vs `utils/`, feature modules.
- ../_shared/framework-idioms.md — the Vue 3.5 / React 19 shape of the code inside each block.
