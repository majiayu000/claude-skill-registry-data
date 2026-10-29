---
name: vite-patterns
description: "Use when configuring or optimizing Vite (laravel-vite-plugin) asset bundling in a Laravel app — entrypoints, the @vite Blade directive, HMR, env vars, aliases, manifests, code splitting, and production builds."
license: MIT
metadata:
  author: "Petr Král (pekral.cz)"
---

## Constraints
- Apply `@rules/laravel/laravel.md`
- Apply `@rules/laravel/livewire.md` and `@rules/laravel/filament.md` when bundling assets for those layers
- Apply `@rules/php/core-standards.md` for any PHP touched (Blade config exposure, service providers)
- This stack uses `laravel-vite-plugin` only. Never introduce React/Vue plugins, SSR frameworks, library mode, Bun, or Next.js.
- Secrets never go into `VITE_`-prefixed vars — those are inlined into the public bundle.
- Keep examples to `npm`, `php artisan serve`, and `npm run dev` / `npm run build`.

## Scope
Asset bundling and dev-server patterns for Laravel apps using the official
`laravel-vite-plugin`. Covers `vite.config.js`, the `@vite` Blade directive,
HMR in development, env vars, aliases, manifests, production builds, code
splitting, and bundling for Livewire / Filament / Alpine.

## Modes

This skill runs in one of two modes, selected by the caller via `MODE` (default `configure`):

- **`configure` (default)** — full Vite work: edit `vite.config.js`, wire entrypoints and the `@vite` directive into Blade, set up HMR, aliases, env exposure, the manifest, and the production build. Every section below behaves as written unless it is explicitly flagged for `MODE=cr`.
- **`cr` (read-only lens — invoked by `@skills/code-review/SKILL.md`, `code-review-github`, `code-review-jira`, and `code-review-bugsnag` when the diff touches an asset build surface)** — **never modify a config file, a Blade layout, or any other project file, never author a test, never stage / commit / push, never run fixers or checkers, and never chain a follow-up review.** Scope the analysis to the lines added or modified by the PR diff and return the findings as markdown only, carrying the reproducer fields the CR folds into its standard Critical / Moderate buckets.
Every instruction below that would touch a file — add, wire, alias, split, expose, or any other such verb — is emitted as a written proposal carrying a concrete config or Blade snippet, never applied to the project.

> **What this lens owns in a CR:** how the bundle is built and loaded — entrypoint declaration and the `@vite` directive that loads it, HMR and dev-server configuration, `VITE_`-prefixed env exposure, `resolve.alias` paths, the manifest and cache-busting, and code splitting in the production build. It **defers the markup a view renders** — component composition, state placement, accessibility semantics, and design tokens — to the three frontend lenses (`@skills/frontend-patterns/SKILL.md`, `@skills/frontend-a11y/SKILL.md`, `@skills/design-system/SKILL.md`), and never raises a finding one of them owns.
> It **defers what the changed `<head>` promises a crawler** — the canonical, the robots directive, the on-page tags, and the JSON-LD payload — to `@skills/seo/SKILL.md` with `MODE=cr`. Those two meet on the preload and the asset a layout loads first: this lens owns how that bundle is built and split, the SEO lens owns whether the head asks for the largest contentful element early enough, and neither restates the other.
> The lens judges the Vite setup the project already has. **Never raise a finding whose only fix is to adopt a plugin or a framework the project does not use** — React, Vue, an SSR framework, library mode, or Bun: the toolchain is a project decision, not a defect on the diff.

## Use when
- Setting up or editing `vite.config.js` with the `laravel()` plugin.
- Wiring entrypoints and the `@vite([...])` directive into Blade layouts.
- Getting HMR / hot reload working in local development.
- Exposing config to the client via `VITE_` env vars or Blade-side config.
- Adding `resolve.alias` paths, code splitting, or dynamic imports.
- Understanding the manifest, cache-busting, and the production build.
- Bundling JS/CSS that Livewire, Filament, or Alpine depend on.
- Building assets in CI before deploy.

## How it works

- **Dev mode** (`npm run dev`) runs a Vite dev server that serves source files
  as native ESM and pushes HMR updates. The `laravel-vite-plugin` writes a
  `public/hot` file; the `@vite` directive detects it and points `<script>` /
  `<link>` tags at the dev server instead of built files.
- **Build mode** (`npm run build`) bundles, hashes, and writes assets to
  `public/build/` plus a `manifest.json`. `@vite` reads the manifest and emits
  the hashed URLs. Cache-busting is automatic via the content hash in filenames.
- **Env vars** prefixed `VITE_` are statically inlined into the client bundle
  via `import.meta.env`. Everything else stays server-side.

## vite.config.js — the laravel() plugin

```js
// vite.config.js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
            ],
            refresh: true, // full-page reload on Blade/route/PHP changes
        }),
    ],
});
```

- `input` lists every entrypoint. Add more for admin panels or per-section
  bundles (`resources/js/admin.js`).
- `refresh: true` triggers a full reload when Blade views, routes, or PHP
  config change. Pass an array of globs to watch extra paths:

```js
laravel({
    input: ['resources/js/app.js'],
    refresh: ['resources/views/**', 'app/Livewire/**'],
}),
```

## The @vite Blade directive

Load entrypoints in your layout `<head>`:

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html>
<head>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    {{ $slot }}
</body>
</html>
```

- No `@viteReactRefresh` is needed — this is a Blade/Livewire/Alpine stack, not
  React. Do not add it.
- In dev, `@vite` emits a script pointing at the running dev server. In
  production it resolves hashed URLs from the manifest. Same directive, both
  modes — you write it once.
- For assets referenced from JS (images, fonts), import them so Vite fingerprints
  them; for Blade-referenced static assets use `Vite::asset('resources/...')`.

## @vite + Tailwind

Tailwind v4 compiles through its Vite plugin plus the CSS entrypoint:

```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    plugins: [
        laravel({ input: ['resources/css/app.css', 'resources/js/app.js'], refresh: true }),
        tailwindcss(),
    ],
});
```

```css
/* resources/css/app.css */
@import "tailwindcss";
```

```js
// resources/js/app.js
import './bootstrap';
```

`@vite(['resources/css/app.css', ...])` handles HMR for Tailwind classes in dev
and outputs a hashed, purged stylesheet in the production build.

## HMR / hot reload in development

Run two processes:

```bash
php artisan serve      # serves the Laravel app
npm run dev            # Vite dev server + HMR
```

- The dev server writes `public/hot`. Add `public/hot` and `public/build` to
  `.gitignore`.
- Edits to JS/CSS hot-swap without a full reload; with `refresh` enabled,
  Blade/PHP edits trigger a full-page reload.
- Behind a custom domain or container, expose the host and the HMR port:

```js
laravel({ input: ['resources/js/app.js'], refresh: true }),
// server config:
server: {
    host: '0.0.0.0',
    hmr: { host: 'localhost' },
},
```

## Environment variables

Only `VITE_`-prefixed vars reach the client bundle via `import.meta.env`:

```js
// resources/js/app.js
const apiUrl = import.meta.env.VITE_API_URL;
const mode   = import.meta.env.MODE; // 'development' | 'production'
```

```dotenv
# .env
VITE_API_URL="${APP_URL}/api"
```

- `VITE_` is **not** a security boundary — these values are inlined into the
  shipped JS. Put only public values (public URLs, feature flags, public keys)
  here. API tokens, DB credentials, and signing keys stay server-side.
- For values the client needs but that depend on per-request state, prefer
  passing them from Blade instead of baking them at build time:

```blade
<script>
    window.AppConfig = @json(['locale' => app()->getLocale(), 'csrf' => csrf_token()]);
</script>
```

## Aliases (resolve.alias)

```js
import { fileURLToPath, URL } from 'node:url';

export default defineConfig({
    plugins: [laravel({ input: ['resources/js/app.js'], refresh: true })],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./resources/js', import.meta.url)),
        },
    },
});
```

Then `import Foo from '@/components/Foo';`. Keep the alias list small — add an
entry only when a real import path needs it.

## Manifest & production build

```bash
npm run build
```

- Outputs hashed files to `public/build/assets/` plus `public/build/manifest.json`.
- `@vite` reads the manifest to emit the correct hashed URLs — no manual
  versioning. The content hash in each filename is the cache-busting mechanism;
  changed files get new hashes, unchanged files keep theirs so browsers reuse
  cached copies.
- Commit neither `public/build` nor `public/hot`; build assets in deploy/CI.

## Code splitting & dynamic import

Vite splits dynamically imported modules into separate chunks automatically:

```js
// load a heavy module only when needed
button.addEventListener('click', async () => {
    const { renderChart } = await import('./chart.js');
    renderChart(data);
});
```

Group stable vendor code into its own chunk to improve cache reuse across deploys:

```js
build: {
    rollupOptions: {
        output: {
            manualChunks: {
                vendor: ['alpinejs', 'axios'],
            },
        },
    },
},
```

Avoid splitting every dependency into its own chunk — that produces many tiny
requests. Group by stability instead.

## Prefetching

For routes/modules likely needed soon, hint the browser with a dynamic import
behind an idle callback so the chunk is fetched ahead of interaction:

```js
requestIdleCallback?.(() => import('./chart.js'));
```

This warms the chunk cache without blocking the initial render.

## Bundling for Livewire / Filament / Alpine

- **Alpine**: in a Livewire app, Livewire already bundles and starts Alpine — register custom
  Alpine components in an `alpine:init` listener and never import or start a second copy.
  Only on a view that loads no Livewire, import Alpine and start it once:

```js
// resources/js/app.js — only for views without Livewire
import Alpine from 'alpinejs';
window.Alpine = Alpine;
Alpine.start();
```

- **Livewire**: Livewire ships its own JS; keep your `@vite` bundle additive
  (custom Alpine components, hooks) and let Livewire manage its own assets per
  `@rules/laravel/livewire.md`. Do not bundle a second Alpine copy — Livewire
  already includes one; if you import Alpine yourself, follow Livewire's
  guidance to avoid a duplicate instance.
- **Filament**: Filament publishes and serves its own compiled assets; use a
  Filament theme + its asset pipeline for panel styling rather than forcing it
  through your app entrypoint (`@rules/laravel/filament.md`). Reserve your Vite
  bundle for front-end (non-panel) views.

## Building for production in CI

```bash
npm ci
npm run build   # writes public/build + manifest.json
```

Run `npm run build` in CI before deploying; ship `public/build/`. Missing
manifest entries surface at render time as a `Vite manifest not found`
exception, so the build step must succeed before the app boots in production.

## Done when
- `vite.config.js` declares every entrypoint via the `laravel()` plugin with
  `refresh` configured for the watched paths.
- Layouts load assets through `@vite([...])`; no `@viteReactRefresh` present.
- `npm run dev` + `php artisan serve` give working HMR locally; `public/hot` and
  `public/build` are gitignored.
- Only `VITE_`-prefixed (public) vars are inlined client-side; secrets stay server-side.
- `npm run build` produces a hashed `public/build/` + `manifest.json`, and CI
  runs the build before deploy.
- Livewire/Filament keep their own asset pipelines; Alpine is started exactly once.

## Output Humanization
- Use [blader/humanizer](https://github.com/blader/humanizer) for all skill outputs to keep the text natural and human-friendly.
