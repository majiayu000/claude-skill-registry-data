---
name: prototype-app
description: Build the frontend vertical of a feature inside the real app (routes, pages, components, remote functions) backed by an in-memory mock namespace — without touching packages/core or any backend package. Use after a /prototype is validated, when the user wants the feature clickable in the actual app before core exists.
---

# Prototype App

Build a feature's frontend vertical in the real dashboard, with the data layer faked by an **in-memory mock namespace** shaped exactly like the core slice will be. The app runs the feature for real — real routes, real layout, real components, real remote functions — but nothing below the api seam exists yet.

Hard rule: **never touch `packages/*`** (core, functions, sdk). If the feature needs core changes — new tables, permissions, namespaces — the mock absorbs them, and the needs are recorded, not implemented (see step 6).

This is the step after `/prototype`: the HTML mockups explored the UX; this makes it live in the product. If `docs/prototype/<feature>/PROTOTYPE.md` exists, it is the spec — follow its features, fields, and flows. If it doesn't, confirm scope with the user before building.

## Workflow

1. **Read the spec.** `docs/prototype/<feature>/PROTOTYPE.md` (features + data model fields) and `PLAN.md` if present (the mock should mirror its schema and API names, so promotion is a rename, not a rewrite).

2. **Study one existing slice end to end** — `lib/features/<slice>/{api,components,pages}` plus its routes — and mirror its conventions rather than inventing new ones. Reuse shared components from `$lib/components` before writing new ones.

3. **Create the mock namespace**: `apps/dashboard/src/lib/features/<feature>/api/mock.ts`. It stands in for the future `@template/core/<feature>` and must present the same surface a core slice would:

   ```ts
   // In-memory stand-in for @template/core/notification — this slice's frontend
   // was built before core; swap this import for core to promote it.
   import { z } from "zod";

   export const Info = z.object({
     id: z.string(),
     title: z.string(),
     kind: z.enum(["mention", "assignment", "system"]),
     readAt: z.string().nullable(),
   });
   export type Info = z.infer<typeof Info>;

   const rows: Info[] = [
     // seeded, realistic — the app should look lived-in on first load
   ];

   // Mirrors core's `util/fn` — `schema` and `force` are both what `remote.core()` reads.
   const fn = <S extends z.ZodType, R>(schema: S, body: (input: z.infer<S>) => R) =>
     Object.assign(async (input: z.infer<S>) => body(schema.parse(input)), {
       schema,
       force: async (input: z.infer<S>) => body(input),
     });

   export const list = fn(z.object({ q: z.string().optional() }), (input) =>
     rows.filter((row) => !input.q || row.title.includes(input.q)),
   );
   export const update = fn(Info.pick({ id: true, readAt: true }), (input) => {
     const row = rows.find((row) => row.id === input.id);
     if (row) row.readAt = input.readAt;
     return row;
   });
   ```

   Rules:
   - Field names and shapes come from the prototype's data model (or PLAN.md when it exists) — the mock is the contract core will implement.
   - Every function carries its zod schema and an unvalidated `force` via `Object.assign` — that is what `$lib/server/remote`'s `remote.core()` helper consumes, so mock and core functions are interchangeable.
   - Module-level state: lives for the dev-server process, shared across tabs, resets on restart. That's the point — no persistence code.
   - Seed data must read like real usage, not placeholders.

4. **Wire the api seam**: `api/<feature>.remote.ts`, exactly like the existing `*.remote.ts` files — `remote.core(mock.list).query()` when the schema comes from the function itself, `remote.query(schema, fn)` when it does not, and `remote.form(schema, mock.update)` (or `remote.command`) for writes — importing from `./mock` where a finished slice would import from core. Nothing outside this file and `mock.ts` may know the data is fake.

5. **Build the frontend**: components and pages in the slice (`components/`, `pages/<Feature>Page.svelte`), thin routes delegating to them:
   - **Every page in the slice opens with a prototype warning.** One `components/Prototype.svelte` banner inside the slice (it dies with the mock, so not `$lib/components`), rendered at the top of each page component: a compact strip in the app's warning/accent tokens saying something like **Prototype** — mock data, not persisted, resets on restart. The user must never mistake the vertical for a finished feature.
   - `routes/(app)/(home)/<feature>/+page.svelte` — imports the page component, nothing else.
   - Detail routes guard the param: `{#if params.id}<DetailPage id={params.id} />{/if}` (params are empty mid-navigation).
   - Add the nav link in the route group's own `+layout.svelte` (nav is layout-owned; pick a lucide icon like its neighbors).
   - Svelte 5 runes; await remote queries in markup inside the component's `<svelte:boundary>`; check `runed` before hand-rolling reactive helpers.

6. **Record what core will need.** While building, collect everything the mock papered over: tables/fields, permission resources, core namespace functions, events. If `docs/prototype/<feature>/PLAN.md` exists, add or update a **Core changes** section there; otherwise list them in your summary so they feed the future plan. Do not implement any of it.

7. **Verify and finish.** `bun typecheck` from `apps/dashboard`, then run the app and click through the feature (use the project's run skill if available). Summarize: files created, what's mock vs real, the recorded core needs, and the promotion path — implement the core slice, swap the `./mock` import in `<feature>.remote.ts` for the core import, delete `mock.ts` and the `Prototype.svelte` banner.
