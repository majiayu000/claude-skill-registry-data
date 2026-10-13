---
name: add-web-page
description: Add a page, route or UI component to the web app (apps/web) or a primitive to packages/ui. Use when the user wants a new screen, a new section of settings, a form, or a reusable component on the web.
argument-hint: <route or component name>
---

# Add a web page or component

The web app renders and nothing else: data comes from `@repo/client` hooks, text from
`packages/i18n`, primitives from `packages/ui`. `.claude/rules/web.md` has the rules.

## A page

1. **Data first.** If the page reads or writes anything new, the procedure and its hook
   come first (the add-feature skill). Pages never call `fetch`.
2. **Module.** `apps/web/src/modules/<feature>/pages/<page>.tsx` (a client component
   when it uses hooks: `"use client"`), its parts in `components/`, and the page exported
   from `apps/web/src/modules/<feature>/index.ts`. Copy the shape of
   `apps/web/src/modules/dashboard/`.
3. **Route.** `apps/web/src/app/(app)/<route>/page.tsx` for signed-in pages (or
   `(auth)` for sign-in flows), two lines like `apps/web/src/app/(app)/dashboard/page.tsx`:
   `export const generateMetadata = pageTitle("<namespace>.<key>")` and
   `export default <Page>`. Dynamic segments use `PageProps<"/route/[id]">` and
   `await params`.
4. **Access.** A new top-level signed-in path goes in `APP_PATHS` in
   `apps/web/src/lib/routes.ts`, or the proxy won't send signed-out users to sign in.
   Links in the header or settings navigation: `apps/web/src/modules/shell/` or
   `apps/web/src/app/(app)/settings/layout.tsx`.
5. **Text.** Every string, including `aria-label`, `alt`, placeholders and the page title,
   in every `packages/i18n/messages/*.json` (the add-translation skill). Errors render as
   `t(errorMessageKey(error), errorParams(error))`.
6. **Forms.** Validate with the contract's input schema, as
   `apps/web/src/modules/dashboard/components/todo-list.tsx` does; shared fields are in
   `apps/web/src/components/form-fields.tsx`.
7. **Weight.** Server components for static content; lazy-load heavy client code.
8. **Tests.** Pure hooks and helpers as `src/**/*.test.ts`. The user flow as a
   Playwright spec in `apps/web/e2e/<feature>.spec.ts`, with the helpers in
   `apps/web/e2e/support.ts` and `expectAccessible(page)` on each screen.

## A component

- Used by one module: `apps/web/src/modules/<feature>/components/`.
- Used by two modules, or a missing primitive: `packages/ui/src/components/<name>.tsx`
  (`bunx shadcn@latest add <name> --cwd packages/ui` for one from the registry) with
  `<name>.stories.tsx` beside it, a `play` function if it's interactive
  (`.claude/rules/ui.md`).

## Done when

- `bun run lint` (render-only and boundary checks), `bun run check-types`,
  `bun run test` pass.
- `bun run test:e2e --app web e2e/<feature>.spec.ts` passes (stop `bun dev` first),
  and `bun run --cwd apps/web budget` after it stays within the budget.
- For a `packages/ui` component: `bun run --cwd packages/ui test:stories`, and
  `test:visual:update` for its new screenshots.
- The `frontend-reviewer` and `i18n-checker` agents report nothing blocking.
