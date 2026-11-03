---
name: zod-to-form-react
description: "Runtime <ZodForm> renderer for Zod v4 schemas Use when: You need form rendering in storybook, playgrounds, or low-traffic admin UIs —.... Also: zod, zod-v4, react, forms, form-generation, react-hook-form, schema-driven, dynamic-forms, form-renderer, hookform-resolver, zod-form-renderer."
license: MIT
---

# @zod-to-form/react

Runtime <ZodForm> renderer for Zod v4 schemas

Choose your abstraction level: `<ZodForm>` for zero-config, `useZodForm` for custom
rendering, manual `walkSchema` for full control. Each step down trades convenience for
flexibility.

## Quick Start

```tsx
import { z } from 'zod';
import { ZodForm } from '@zod-to-form/react';

const userSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  subscribe: z.boolean().default(false)
});

export function UserForm() {
  return (
    <ZodForm
      schema={userSchema}
      mode='onSubmit'
      onSubmit={(data) => {
        console.log('submitted', data);
      }}
    >
      <button type='submit'>Save</button>
    </ZodForm>
  );
}
```

## When to Use

**Use this skill when:**
- You need form rendering in storybook, playgrounds, or low-traffic admin UIs → use `ZodForm` — where bundle overhead is acceptable and a build step would add friction
- You are prototyping before committing to CLI codegen → use `ZodForm` — `<ZodForm>` and the CLI share the same walkSchema output so the migration is mechanical
- You need direct access to the RHF `form` instance (e.g. to call `form.setValue`) → use `useZodForm`
- You are building a custom renderer on top of `FormField[]` → use `useZodForm`
- You want to colocate form state management with your own layout logic → use `useZodForm`
- ALWAYS call on form values before schema.safeParse() in runtime mode → use `normalizeFormValues` — HTML inputs produce `""` for unset optional fields, which Zod rejects; this is the single mandatory normalization step
- You are using codegen output with `validationLevel: 1` or higher and need the lite schema to run before your submit handler → use `wrapWithSchemaLite` — this is the only function that wires `schemaLite` into RHF's `handleSubmit` flow

**Do NOT use when:**
- Bundle size is critical — use CLI codegen (`@zod-to-form/cli`) instead; runtime schema walking includes the full Zod type graph traversal, which does not tree-shake (`ZodForm`)
- You need forms for complex schemas with cyclic references — the walker does not handle cycles and hits the max-depth guard silently with no error (`ZodForm`)
- You just need a working form UI — use `<ZodForm>` instead; `useZodForm` returns `fields[]` and `form`, but rendering those fields requires wiring up each field component yourself (`useZodForm`)
- CLI codegen mode — generated components call normalization internally; calling it again is safe (idempotent) but redundant (`normalizeFormValues`)
- You are using the default `zodResolver` path (no `validationLevel`) — validation is handled by RHF's resolver and adding this wrapper causes double-validation with no benefit (`wrapWithSchemaLite`)

API surface: 4 functions, 5 types, 3 constants

## NEVER

- NEVER pass `componentConfig` without a matching `components` map that covers the component names referenced — missing components are silently dropped at render time with no console error; add each name to `components` or use `defaultComponentMap` as the base
- NEVER expect controlled component prop expressions (e.g. `field.value`) to work without a `propMap` in `componentConfig` — uncontrolled mode is the default; add `propMap: { value: 'value', onChange: 'onChange' }` in field config to opt in to controlled mode
- NEVER pass a new schema object on every render — `walkSchema` is memoized by schema identity; an unstable reference causes re-walking on every render cycle; FIX: declare the schema outside the component or wrap in `useMemo`
- NEVER forget `normalizeFormValues()` before manually calling `schema.safeParse()` — the hook's internal resolver applies normalization, but manual calls do not; FIX: always call `schema.safeParse(normalizeFormValues(values))`
- NEVER mix `formRegistry` and `fields` options on the same call — when `formRegistry` is provided, `fields` is ignored entirely with no merge and no warning; FIX: pick one or merge field config into the registry manually before passing it
- NEVER rely on this for custom types (Date, File subclasses, etc.) — it only handles empty strings and FileList; FIX: normalize custom types before calling this function or in a custom resolver wrapper
- NEVER pass the full schema as `schemaLite` — it defeats the optimization and adds double-validation overhead; FIX: only pass the schema produced by `walkSchema`'s `result.schemaLite` field (never the original `z.object({...})`)
- NEVER use this with schemas that have root-level `.superRefine()` — root refinements are stripped from `schemaLite` by design and will not run through this wrapper; FIX: use full `zodResolver` path and skip `wrapWithSchemaLite` entirely

## Configuration

3 configuration interfaces — see references/config.md for details.

## Quick Reference

**Components:** `ZodForm` (Runtime React component that renders a type-safe form from a Zod v4 schema), `defaultComponentMap` (The default HTML-based component map used by `<ZodForm>` and `<FieldRenderer>`), `shadcnComponentMap` (Component map pre-wired with shadcn/ui-styled implementations)
**Hooks:** `useZodForm` (React Hook Form integration hook for Zod v4 schemas)
**Normalization:** `normalizeFormValues` (Normalize raw HTML form values for Zod parsing)
**Optimization:** `wrapWithSchemaLite` (Wraps a form `onSubmit` handler with `schemaLite` client-side validation)
**Types:** `FormField` (Intermediate representation of a single form field produced by `walkSchema`), `FormFieldOption` (An individual option in a Select, RadioGroup, or similar enum-driven component), `FormFieldConstraints` (Structural constraints extracted from Zod's `_zod), `FormMeta` (Per-schema annotation stored in a `z), `FieldTemplateProps` (Props passed to the field template component that wraps each rendered form field)
**components:** `FIELD_COMPONENT_NAMES` (User-facing field component names derived from defaultCom...)

## References

Load these on demand — do NOT read all at once:

- When calling any function → read `references/functions.md` for full signatures, parameters, and return types
- When defining typed variables or function parameters → read `references/types.md`
- When using exported constants → read `references/variables.md`
- When configuring options → read `references/config.md` for all settings and defaults

## Links

- [Repository](https://github.com/pradeepmouli/zod-to-form)
- Author: Pradeep Mouli <pmouli@mac.com> (https://github.com/pradeepmouli)