---
name: aiwf-vue-vitepress-coding
description: Use for Vue 3 components, Composition API, reactivity, TypeScript in Vue, VitePress documentation sites, Markdown routes, themes, assets, base paths, static builds, and browser validation.
---

# AIWF Vue VitePress Coding

## Core Rule

Inspect the pinned Vue, Vite, VitePress, TypeScript, package manager, site root, source directory, base path, theme, and deployment target before editing. Preserve reactivity and static-site routing instead of treating Vue files as generic HTML.

## Workflow

1. Read `package.json`, lockfile, Vite/VitePress config, `.vitepress` theme files, source Markdown, Vue components, TypeScript config, and build scripts.
2. Classify the change: Vue component behavior, reactivity, composable, theme, Markdown content, routing, asset path, build-time data, or deployment base.
3. Follow the project's API style. Keep `ref`, `reactive`, `computed`, watchers, lifecycle hooks, props, and emits aligned with the installed Vue version and local patterns.
4. For VitePress, preserve file-based routes, source-relative links, configured rewrites, clean-URL hosting assumptions, and `base` handling.
5. Run the repo-native lint, typecheck, tests, build, and browser check for visible or routing changes.

## Guardrails

- Do not introduce a second state library, CSS system, or site generator for a local fix.
- Do not mutate props or hide reactivity bugs behind forced rerenders.
- Guard browser-only APIs from server-side or build-time execution.
- Keep generated docs output and cache files out of source edits.
- Use source Markdown as the content authority; do not patch generated HTML.
- Keep code examples, links, anchors, sidebars, and version claims synchronized.
- Add `aiwf-typescript-coding`, `aiwf-css-coding`, or `aiwf-web-seo` only when the task crosses those boundaries.

## Validation

Use the repository package manager. Typical checks are the configured equivalents of `docs:build`, typecheck, lint, and a local preview. Verify at least one direct deep link when routing or base paths change.

## Primary Sources

- Vue with TypeScript: https://vuejs.org/guide/typescript/overview
- Vue Composition API: https://vuejs.org/guide/extras/composition-api-faq
- VitePress routing: https://vitepress.dev/guide/routing
- VitePress assets: https://vitepress.dev/guide/asset-handling
