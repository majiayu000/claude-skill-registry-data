---
name: astro-architect
version: 1.0.0
description: Astro 6+ standards — islands architecture with zero JS by default, Content Layer collections with loader + Zod schema validation, `<script>` processing, `getStaticPaths`, Actions and Sessions for forms, Server Islands for dynamic islands, per-adapter deployment. Use when scaffolding or reviewing an Astro site, wiring content collections, or auditing where client JS leaked into a static page.
---

# Astro Architecture

Targets **Astro 6+** with **TypeScript strict**, zero-JS-by-default output.
Builds on [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md) for design
tokens and a11y; this skill covers the Astro-specific layers — rendering model,
content collections, scripts, routing, forms, deployment. Concrete skeletons in
[RECIPES.md](RECIPES.md); pinned dependencies in [STACK.md](STACK.md).

## 1. The rendering model — the one rule that governs everything else

Astro components (`.astro`) render to HTML **at build time** and ship zero
JavaScript unless you explicitly opt in. This is the framework's whole thesis;
every rule below is downstream of it.

- **Default to `.astro` components.** Reach for a framework component only when
  the interaction genuinely cannot be expressed as an event handler on the
  server-rendered HTML.
- **Every `<script>` you write ships to the browser.** Astro bundles and dedupes
  `<script>` tags, but it does not make them free. Two `onclick` attributes are
  cheaper than one hydrated island.
- **Astro components can be islands themselves.** `<script>` inside a `.astro`
  file is processed, bundled, hoisted, and deduplicated — it is not inline
  markup. This is usually the cheapest interactivity available.

Skeleton: [RECIPES § Script processing](RECIPES.md#script-processing).

### Prefer these, in order

1. CSS `:checked` / `:target` / `:hover` — zero JS, zero hydration.
2. `<details>` / `<dialog>` — native, accessible, free.
3. A processed `<script>` in the `.astro` file — bundled, deduped, no framework.
4. A framework island with `client:visible` / `client:idle` — the real cost.
5. `client:load` — last resort. Every `client:load` is on the critical path.

**The common failure mode:** a static content site ships 200 KB of React because
one dropdown needed `useState`. Reach for level 3 first.

## 2. Content collections — Content Layer API

Collections are defined in **`src/content.config.ts`** (note: *content* config,
not the legacy per-directory `config.ts`). Each collection needs a **loader**
(required) and a **schema** (optional but load-bearing).

```ts
import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.md' }),
  schema: z.object({
    name: z.string(),
    lang: z.string(),
    summary: z.string(),
    status: z.enum(['active', 'wip', 'archived']),
    category: z.enum(['tooling', 'robotics']),
    updated: z.coerce.date(),
    pinned: z.boolean().default(false),
  }),
});

export const collections = { projects };
```

**Import Zod from `astro/zod`, not `zod`.** The bundled version is pinned to
match Astro's schema resolution. A bare `zod` import can produce duplicate
instance errors at build.

- **A schema is a build-time contract.** A typo in `category: tools` fails the
  build instead of silently rendering an empty filter. On a small collection
  feeding multiple views, this is the highest-value line in the file.
- **`z.coerce.date()` for dates.** YAML parses unquoted dates inconsistently
  across parsers; coercion normalizes them to `Date`.
- **Import order is fixed:** `astro:content` → `astro/loaders` → `astro/zod`.
- **Legacy `src/content/<name>/config.ts` is deprecated.** Migrate to the Content
  Layer before adding new collections; don't mix both for the same data.

Full patterns and remote loaders: [RECIPES § Content collections](RECIPES.md#content-collections).

### Querying

- **`getCollection('projects')`** returns entries **unsorted** — always sort
  explicitly. `updated` as a `Date` needs `.sort((a, b) => b.data.updated - a.data.updated)`.
- **Filter in the query, not after.** `getCollection('projects', ({ data }) => data.pinned)` returns a type-narrowed result and avoids loading bodies you don't render.
- **`render(entry)`** turns an entry into a component. In Astro 5+, this replaced `entry.render()` on the entry itself.
- **`getEntry('projects', id)`** fetches one entry; use it for lookup-by-id rather than filtering the whole collection.
- **`getStaticPaths()`** is only required in `[slug]` routes — and in a static build it must return every path you want generated.

Skeleton: [RECIPES § Collection with schema + dynamic route](RECIPES.md#collection-with-schema--dynamic-route).

## 3. Scripts

- **Processed `<script>`** — bundled, deduped, hoisted, TypeScript-aware. The default.
- **`is:inline`** — left completely alone. No bundling, no TS, no processing. Required for the pre-paint theme flash guard (below) and for anything that must run before CSS applies.
- **A theme flash guard must be `is:inline` in `<head>`.** An external or bundled script may run after first paint, which defeats the purpose:

```astro
<script is:inline>
  (function () {
    var t = localStorage.getItem('theme') || 'tokyo-night';
    document.documentElement.setAttribute('data-theme', t);
  })();
</script>
```

- **`define:vars`** passes server values into an inline script; the script is then treated as `is:inline` and cannot import anything.
- **A `<script>` in `src/components/` is hoisted and rendered once per page**, regardless of how many times the component is used. Do not rely on per-instance initialization — that's what islands are for.

## 4. Routing

- **`src/pages/` is file-based.** `about.astro` → `/about`; `projects/[slug].astro` → `/projects/[slug]`; `index.astro` → `/`.
- **`src/layouts/` is convention, not a framework concept.** A layout is just a component you import and wrap around.
- **`[...slug]` is a rest parameter**; `[slug]` is a single segment.
- **Route priority is static-first:** `about.astro` wins over `[slug].astro` for `/about`.
- **`Astro.params`** carries route params; **`Astro.props`** carries component props. **`Astro.url`**, **`Astro.redirect()`**, and **`Astro.response`** cover the rest of the request surface.
- **Endpoints** — any `.ts` file in `src/pages/` exporting `GET`/`POST` becomes an API route. Skip these unless you need a webhook or a non-HTML response.

Skeleton: [RECIPES § Dynamic route with getStaticPaths](RECIPES.md#collection-with-schema--dynamic-route).

## 5. Forms and Actions

**Actions** are Astro's typed RPC layer. They replace hand-written API routes
for form handling.

```ts
// src/actions/index.ts
import { defineAction } from 'astro:actions';
import { z } from 'astro/zod';

export const server = {
  subscribe: defineAction({
    input: z.object({ email: z.string().email() }),
    handler: async (input) => {
      // server-only: never leak this into the bundle
      await subscribeToList(input.email);
      return { ok: true };
    },
  }),
};
```

- **Actions require an on-demand rendering route.** They don't work in a fully static build without an adapter.
- **Validate at the boundary with Zod**, same discipline as [rest-api-architect §7](../../protocols/rest-api-architect/SKILL.md#7-error-contracts--rfc-9457-problem-details).
- **Re-verify auth inside the handler.** The calling context is not trust.
- **`Astro.getActionResult()`** to read the result in a page; `isInputValid()` narrows the error case.
- **For a static site, a plain HTML `<form>` to a third-party (Formspree, Buttondown) beats adding a server runtime.** Only adopt Actions if you're already on-demand.

## 6. Server Islands

Server Islands render dynamic content *within* an otherwise static page: the
page ships as static HTML, and the marked island fetches its own data at
runtime. This is the correct tool when one region of a page needs live data and
the rest does not.

- **`server:defer` on a framework component** defers only that component.
- **Requires an adapter.** Same constraint as Actions.
- **Don't reach for it on a static site.** If the whole page is static, a
  build-time value is strictly better: no request, no loading state, no failure
  mode.

## 7. Sessions

`context.session` is a typed key-value store backed by an adapter. Read and
write it from Actions and middleware; not from `.astro` frontmatter in a fully
static build.

- **Sessions are cookies.** Size them like cookies — keep them small and store
  large state server-side.
- **Sessions and Actions share a lifecycle**: `context.session?.get(key)` / `.set(key, value)`.

## 8. Rendering modes and adapters

`output` in `astro.config.mjs`:

- **`static` (default)** — pre-render everything. Deploy to any CDN. No runtime.
- **`server`** — on-demand by default; opt individual routes back to static with `export const prerender = true`.
- **Hybrid** — `output: 'server'` plus `prerender` on the routes that don't need a runtime. This is the usual production shape for a site with one dynamic corner.

**Adding SSR means adding a runtime.** That's a real operational cost — a
process to keep alive, cold starts, a place for secrets to live. For a portfolio
or docs site, stay `static` and use Actions only if you accept the adapter.

- **`astro.config.mjs` needs `site:`** for correct canonical URLs, sitemap
  generation, and RSS feeds. Set it at scaffold time; retrofitting means
  auditing every absolute URL.

Skeleton: [RECIPES § Hybrid rendering config](RECIPES.md#hybrid-rendering-config).

## 9. Styling

- **Scoped `<style>` in `.astro` is the default** — compiled, hashed selectors,
  no runtime. Prefer it for component-local styles.
- **`is:global`** escapes the scoping.
- **CSS custom properties for design tokens**, with theme variants on a
  `[data-theme]` attribute selector. This is what makes runtime theme switching
  possible without re-rendering:

```css
:root, [data-theme='tokyo-night'] { --bg: #1a1b26; --fg: #c0caf5; --accent: #7aa2f7; }
[data-theme='nord']               { --bg: #2e3440; --fg: #d8dee9; --accent: #88c0d0; }
```

- **A theme switcher needs no framework.** Write the attribute to
  `document.documentElement`, read it back in CSS. Don't hydrate a picker.
- **Tailwind is optional**, not a default. Astro's scoped styles plus custom
  properties cover most content sites without a utility-class vocabulary.

## 10. Images and fonts

- **`<Image>` from `astro:assets`** processes and optimizes local images at
  build. Import the file, don't reference it by string path — that's what lets
  Astro know the dimensions.
- **Remote images need `image.domains` (or `remotePatterns`)** in the config.
- **Set explicit `width`/`height`** or use the `<Image>` component's output —
  prevents layout shift.
- **Fonts:** `astro:assets` has a `getImage`-adjacent font API in recent
  versions, but for most projects self-hosting via `@font-face` in a global
  stylesheet beats the framework path. Never `@import` a font from a CDN in CSS
  — it blocks render.

## 11. Testing

- **Vitest** for unit tests. Astro exposes a container API (`astro/container`)
  for rendering a component to a string without a browser.
- **Playwright** for end-to-end against `astro preview` (built output), not
  `astro dev` — dev-only behavior can mask real hydration bugs.
- **Content collection schemas are tested by the build.** If the schema is
  strict, a malformed entry fails CI before any test runs. That's most of the
  value a test would add for a content site.

## 12. Deployment

- **Static output** → any CDN. Netlify, Vercel, Cloudflare Pages, GitHub Pages, or plain object storage.
- **On-demand output** → pick the adapter matching your host, and own the runtime.
- **Cloudflare Pages / Netlify / Vercel all auto-detect Astro** — no build config needed beyond `build.command: astro build` and `output: dist`.

## 13. Cross-skill ties

- [ui-ux-architect](../../frontend/ui-ux-architect/SKILL.md) — design tokens, component states, WCAG. Owns the token layer Astro's CSS custom properties consume.
- [hugo-architect](../hugo-architect/SKILL.md) — the other content-first static generator; useful when comparing approaches on a greenfield content site.
- [react-architect](../react-architect/SKILL.md) — only for islands that genuinely need a component framework.
- [rest-api-architect](../../protocols/rest-api-architect/SKILL.md) — applies to `src/pages/*.ts` endpoints and Action handlers.
- [docker-architect](../../infra/docker-architect/SKILL.md) — for self-hosted on-demand deployments.
- [observability-architect](../../infra/observability-architect/SKILL.md) — only when on-demand rendering is in play.
- [security-reviewer](../../quality/security-reviewer/SKILL.md) — Actions and endpoints are the attack surface.