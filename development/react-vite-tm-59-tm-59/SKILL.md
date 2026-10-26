---
name: react-vite
description: Use when building or maintaining a React single-page app with Vite — project setup, routing, state, static pre-rendered content for search engines and ads review, environment variables, testing with Vitest and Testing Library, and deploying the static build. Also use when a React page is blank before JavaScript runs, when upgrading React or Vite major versions, or when migrating off Create React App.
---

# React + Vite

Default: Vite's `react-ts` template, React function components and hooks, React Router when there is more than one screen, Vitest + Testing Library, static hosting of `dist/`.

## Setup

1. `npm create vite@latest app -- --template react-ts`.
2. Scripts: `dev`, `build` (`tsc -b && vite build`), `preview`, `test` (`vitest run`).
3. Only variables prefixed `VITE_` reach client code, and they are **public** once built. Never put secrets there.

## Content that must exist without JavaScript

A client-rendered SPA ships an almost empty `index.html`. Crawlers, link previews and ad reviewers may see no content.

- Put a meaningful static body in `index.html` (or generate static pages at build time): what the page is for, how to use it, links to articles and policy pages. Let React mount into a separate element.
- Give every static page its own `<title>`, `description`, canonical URL and Open Graph tags.
- Generate `sitemap.xml` at build time from the real list of pages (and their last-modified dates from git), not by hand.
- Add a build-time check that fails when a page lacks a title, description or canonical link.

## State and data

- Local component state first; lift state up when two siblings need it; add a store (Context + reducer, Zustand) only for truly global state.
- Fetch with an effect plus abort controller, or a data library (TanStack Query) once caching and retries matter.
- Derive values during render instead of syncing them into extra state.

## Testing

- Testing Library queries by role and label (`getByRole('button', { name: /play/i })`), not by class names.
- Mock network at the fetch boundary (MSW or a stub).
- One Playwright smoke test per route that fails on console errors.

## Upgrades

- Upgrade `react` and `react-dom` together, and `@types/react*` with them; mismatched versions produce peer dependency errors (`ERESOLVE`).
- Create React App (`react-scripts`) is no longer maintained and pins old TypeScript; migrate to Vite rather than fighting its constraints.
- Read the framework's migration guide for each major version; run the codemods it provides.

## Verification loop

1. `npm run build` (type-check + bundle) succeeds.
2. `npm test` passes.
3. `npm run preview` and view the page with JavaScript disabled: the static content is still there.
4. Check bundle size and the largest chunks (with a bundle visualiser such as `rollup-plugin-visualizer`) after adding dependencies.

## Pitfalls

- **Strict mode double-invokes effects in development;** an effect that breaks when run twice has a missing cleanup.
- **Stale closures:** handlers capturing old state; use functional updates (`setX(x => x + 1)`).
- **Keys:** use stable IDs, not array indexes, for lists that reorder.
- **Client-side routes on static hosts** need a fallback to `index.html` (a `_redirects` or `staticwebapp.config.json` rule), or deep links return 404.
- **Ads and third-party scripts** inside React components re-run on every mount; load them once and only on pages with real content.
