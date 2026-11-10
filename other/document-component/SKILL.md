---
name: document-component
description: Document a design system's Vue component with a page, live examples and a props table, using yarn component-docs. Use when asked to document, or add a page for, a component of a system in src/systems/.
---

# Document a component

The [Systems README](../../README.md#component-pages) is the contract: file names, the page's order, how examples and props are read, and the documentation checks. Read it first.

## Before you start

1. Find the system, `src/systems/<key>/`, and read its `AGENTS.md`. Only an Admin or one of the system's maintainers changes a system: `yarn studio whoami` says who you are.
2. The component needs a component file first: `components/<name>/<name>.vue` (or a flat `components/<Name>.vue`). For a component the app takes from a library (Endless Studios uses Nuxt UI's `UButton` and `UCard`), the file is a thin `<script setup>` wrapper that declares the props screens use, with a doc comment on each, and passes them on. Keep existing source, examples and pages.

## Create the files

3. Run `yarn component-docs <system> <component>` to see what it would add, then again with `--yes`. It creates the missing `<name>.examples.vue` and `<name>.md` from templates, moves a flat component into its own folder with an `index.ts`, and never overwrites a file.

## Fill them in

4. The page, `<name>.md`: a `title`, a one-line `description`, and a `## When to use` section. Add `source` (one sentence: the library and version it comes from, or the app revision it was copied from) and `docs` (the library's page for it) when it comes from elsewhere. Add other sections only when they help: variants, parts, accessibility, how screens use it.
5. The examples, `<name>.examples.vue`: one `<Example name="…">` per variant, size or state worth seeing, named in PascalCase (`WithIcons` shows as "With icons"). Write each as a screen would, with the system's own components (`<UButton>` in Endless Studios), so **Show code** can be copied into a view. Don't wrap examples in frames or themes: the page renders each one alone in the system's own preview document. Replace every `undefined` the template left for a required prop.
6. Props come from the component file's `defineProps`: give each prop a doc comment (`/** … */`) and defaults in `withDefaults`, so the table explains them.

## Check

7. Open `/systems/<system-id>/components/<name>` (the system's permanent ID, from `system.ts`'s `studioId`). Every example should render; one that throws shows its error in its own frame. Look at each example; previews render light only, whatever colour modes the system declares.
8. The dev server's start and `yarn build` warn about documentation gaps, the first five per system; a system with `docs: 'strict'` fails the build until they're fixed.

Report the files you created and anything the component can't show yet. Don't call it done while examples hold placeholders.
