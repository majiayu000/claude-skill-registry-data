---
name: crouton-ui
layer: stack
description: Build or change UI in a crouton app or package. Read the package's generated docs/llms.txt and docs/components.md to find an existing component and its props, events and slots before building anything by hand. Use for any page, block, form, list or control in crouton.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Build crouton UI from what the packages already offer

Every crouton package with a `crouton.manifest.ts` ships a generated index, and every such package that offers components ships a generated component page. Both are built from the code and checked in CI, so they are true for the version you have.

- `docs/llms.txt` — what the package is for, and its components with one line each.
- `docs/components.md` — per component: its props, events and slots.

Where they are:

- in this repo: `packages/<package>/docs/`
- in an app that installed crouton: `node_modules/@fyit/<package>/docs/`

## Steps

1. **Find the packages.** Read `extends` in the app's `nuxt.config.ts`. Each entry that starts with `@fyit/crouton-` names a package: the name up to the second `/` (`@fyit/crouton-themes/ko` → `crouton-themes`). Entries that start with `./` are the app's own layers.
2. **Read each package's `docs/llms.txt`.** It is short. Pick the component whose line matches what you need. A package without a `docs/llms.txt` has no index; skip it.
3. **Read only that component's section in `docs/components.md`** for its props, events and slots. Do not open the component's source to learn its props.
4. **Before you build a control by hand, look in two places:** those component lists, and Nuxt UI (the `U…` components). Use what exists. Build by hand only when neither has it, and say in your summary what you looked for.
5. **A new layout block:** follow the `block-authoring` skill.

## When you add or change a component in a package

- A component that another package or an app uses must be named in the package's `crouton.manifest.ts` (`provides.components`: `name` and a one-line `description`). CI fails otherwise: `node scripts/component-names.mjs --check`.
- After you change a named component's props, events or slots, or a manifest, regenerate the docs: `node scripts/gen-package-docs.mjs`. CI fails on a stale file: `node scripts/gen-package-docs.mjs --check`.
- Both commands need `pnpm install` and built packages (`pnpm build:packages`).
- Never edit `docs/llms.txt` or `docs/components.md` by hand.

## When you finish

- Run the typecheck of the package or app you changed.
- In your summary, list any doc gap you hit: a component you needed that no list mentions, or a prop whose description was missing or wrong. Fix those in the component or the manifest, not in the generated files.
