---
name: set-up-forms
description: Use when adding forms and validation to a frontend project — wires React Hook Form (React) or VeeValidate (Vue) with Zod schema-first validation, where one schema is the single source of truth for shape, rules, and inferred types, with accessible fields and submit wired to a TanStack Query mutation.
---

# Set Up Forms

## 1. Audit current state

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # frontend.framework, package_manager
grep -E '"(react-hook-form|vee-validate|formik|zod|valibot|@hookform/resolvers|@vee-validate/zod)"' package.json 2>/dev/null
```

Read `frontend.framework` (react → React Hook Form, vue → VeeValidate) and `package_manager` (commands below use pnpm). Detect an existing form/validation lib. **Prerequisites:** `set-up-state-management` (form submit calls its `useMutation` hook) and `@/` alias.

## 2. Decide what to do
- No form lib → full setup.
- Formik or uncontrolled ad-hoc forms → migrate deliberately to the schema-first pattern below.
- Form lib + Zod present → confirm the schema-first + accessibility rules (`forms-patterns.md`).

## 3. Detect framework
React → **React Hook Form** + `@hookform/resolvers`. Vue → **VeeValidate** + `@vee-validate/zod`. Both validate with **Zod** (4.x). Why this pairing: `forms-patterns.md`.

## 4. Install

### React
```bash
pnpm add react-hook-form zod @hookform/resolvers
```

### Vue
```bash
pnpm add vee-validate zod @vee-validate/zod
```
`@vee-validate/zod` 4.15 declares `zod@^3.24` as its peer, so pnpm warns with Zod 4. The runtime and type inference below were checked against zod 4.6 with vee-validate 4.15.1 (a parse error maps to the schema message; `values` is typed). If a project treats peer warnings as errors, install `zod@^3.25` instead — the schema file is identical. VeeValidate 5 (beta) reads any Standard Schema directly and drops `@vee-validate/zod`: migrate then.

## 5. Schema first — one source of truth

The Zod schema defines the shape, the rules, and (via `z.infer`) the type. Nothing is declared twice.

```ts
// src/libs/schemas/todo.ts
import { z } from 'zod';

export const createTodoSchema = z.object({
  text: z.string().min(1, 'Enter a todo').max(280, 'Keep it under 280 chars'),
});

export type CreateTodoInput = z.infer<typeof createTodoSchema>;
```

## 6. React — React Hook Form + zodResolver

```tsx
// src/components/molecules/CreateTodoForm/CreateTodoForm.tsx
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { createTodoSchema, type CreateTodoInput } from '@/libs/schemas/todo';
import { useCreateTodo } from '@/hooks/useCreateTodo';

export function CreateTodoForm() {
  const createTodo = useCreateTodo();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<CreateTodoInput>({ resolver: zodResolver(createTodoSchema) });

  const onSubmit = handleSubmit(async (data) => {
    await createTodo.mutateAsync(data); // server state via TanStack Query
    reset();
  });

  return (
    <form onSubmit={onSubmit} noValidate>
      <label htmlFor="todo-text">Todo</label>
      <input
        id="todo-text"
        aria-invalid={errors.text ? true : undefined}
        aria-describedby={errors.text ? 'todo-text-error' : undefined}
        {...register('text')}
      />
      {errors.text && (
        <p id="todo-text-error" role="alert" className="text-sm text-red-600">
          {errors.text.message}
        </p>
      )}
      <button type="submit" disabled={isSubmitting}>Add</button>
    </form>
  );
}
```

## 7. Vue — VeeValidate + toTypedSchema

```vue
<!-- src/components/molecules/CreateTodoForm/CreateTodoForm.vue -->
<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import { createTodoSchema } from '@/libs/schemas/todo';
import { useCreateTodo } from '@/composables/useCreateTodo';

const createTodo = useCreateTodo();
const { defineField, handleSubmit, errors, isSubmitting } = useForm({
  validationSchema: toTypedSchema(createTodoSchema),
});
const [text, textAttrs] = defineField('text');

const onSubmit = handleSubmit(async (values) => {
  await createTodo.mutateAsync(values);
});
</script>

<template>
  <form novalidate @submit="onSubmit">
    <label for="todo-text">Todo</label>
    <input
      id="todo-text"
      v-model="text"
      v-bind="textAttrs"
      :aria-invalid="errors.text ? true : undefined"
      :aria-describedby="errors.text ? 'todo-text-error' : undefined"
    />
    <p v-if="errors.text" id="todo-text-error" role="alert" class="text-sm text-red-600">
      {{ errors.text }}
    </p>
    <button type="submit" :disabled="isSubmitting">Add</button>
  </form>
</template>
```

## 8. Verify
```bash
pnpm typecheck
```
Expected: 0 errors — the form's values type is inferred from the schema and matches the mutation input. Submitting an empty field shows the schema's message; a valid submit calls the mutation and resets.

## References
- ./forms-patterns.md — schema-first rationale, accessibility rules, form-state-is-UI-state, submit→mutation, Valibot alternative.
- ../_shared/glossary.md — server state vs UI state (a form's in-progress values are UI state).
- ../_shared/conventions.md — `@/` alias, molecule classification.
- ../../landing/set-up-lead-capture/SKILL.md — public lead/signup forms (spam defenses, consent at capture, destination seam); this skill owns authenticated in-app forms.
