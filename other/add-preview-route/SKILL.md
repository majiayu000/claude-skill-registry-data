---
name: add-preview-route
description: Add a new component showcase, block, or template preview page and register it everywhere it must appear (navigation, command palette, route lists, SEO, source view). Use when adding anything under /components, /blocks, or /templates.
argument-hint: "<components|blocks|templates> <slug> [description]"
---

# Add a preview route: $ARGUMENTS

Preview pages render inside the editor's iframe (`?preview`, `preview` layout) and must respond to the theme being edited. Use Nuxt UI components and semantic tokens (`bg-(--ui-bg-elevated)`, `text-(--ui-text-muted)`, `color="primary"`), never raw palette classes like `bg-blue-500`.

## 1. Create the content

**Component showcase** (`/components/<slug>`, data-driven via `app/pages/components/[slug].vue`):

- Create `app/components/showcase/components/<PascalSlug>.vue`. It's resolved by `import.meta.glob` from the kebab-case slug. Reuse `ShowcaseSpecimen` / `ShowcaseSpecimenGrid` like the existing showcases.
- Register it in `COMPONENT_CATEGORIES` in `app/utils/navigation/components.ts` (label, icon, description, `to: "/components/<slug>"`).

**Block** (`/blocks/<slug>`, data-driven via `app/pages/blocks/[slug].vue`):

- Variants live in `app/components/blocks/components/<Name>.vue`. Each block page is `app/components/blocks/content/<PascalSlug>.vue`, fed by `app/data/blocks/<slug>.ts`, which imports every variant **and** its `?raw` source (shown in the block's code view) plus an AI `prompt`.
- Register it in `BLOCK_CATEGORIES` in `app/utils/navigation/blocks.ts`.

**Template** (`/templates/<slug>`):

- Create `app/pages/templates/<slug>.vue` as a full, self-contained page (users copy this file from the source view, so keep it clean and idiomatic). Don't use `definePageMeta({ layout })`; `app.vue` picks layouts.
- Register it in `TEMPLATE_CATEGORIES` in `app/utils/navigation/templates.ts`.
- Source view picks it up automatically via `modules/source-code-embed.ts`. Restart `pnpm dev` to refresh the embedded map.

## 2. Register the route

- `shared/constants/routes.ts`: add the path to `COMPONENT_ROUTES` / `BLOCK_ROUTES` / `TEMPLATE_ROUTES`. These drive the sitemap, prerendering, and `noindex`. `tests/unit/shared/routes.test.ts` fails if nav and route lists disagree.
- `app/utils/seoDescriptions.ts`: add a `PAGE_DESCRIPTIONS` entry (and `PAGE_TITLES` if the generic "<Label> Component/Block/Template" title isn't right).
- The command palette and breadcrumbs read the navigation modules, so no extra work is needed there.

## 3. Verify

- `pnpm vitest run tests/unit/shared/routes.test.ts tests/unit/utils/navigation.test.ts tests/unit/utils/seoDescriptions.test.ts`
- `/run-app`: open the route in the editor, change the primary color and radius and confirm the preview reacts, toggle dark mode, use the command palette to find it, and for templates check the source view.
- `/dev-workflow`.
