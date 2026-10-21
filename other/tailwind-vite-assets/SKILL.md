---
name: tailwind-vite-assets
description: Use when working on the front-end build of a Roots/Acorn project - vite.config.js, laravel-vite-plugin, @roots/vite-plugin, Tailwind 4 (@theme, @source, @reference), design tokens, Vite::asset and @vite URLs (including from an mu-plugin), public/build, manifest.json, public/hot, HMR through Lando, editor.css, "styles missing", "assets 404". For block registration in PHP use acorn-scaffolding; for container networking use lando-wp.
---

# Tailwind 4 and Vite assets

The build is Vite with `laravel-vite-plugin`; Acorn reads the generated manifest through the `Vite` facade and the `@vite` Blade directive. Tailwind 4 is configured in CSS. There is no `tailwind.config.js`.

Runner placeholders (`{{runner.node}}`, `{{runner.acorn}}`, `{{runner.wp}}`, `{{runner.cache}}`) come from the session context. `{{runner.node}}` is the project's package-manager runner, so `{{runner.node}} run build` means the project's own `build` script (on Lando the default is the `lando npm` or `lando yarn` tooling, or a command in a separate Node service; see `lando-wp`).

## When to use

- Creating or fixing `vite.config.js`, entries, the build base, or the dev server.
- Writing or debugging Tailwind CSS (tokens, utilities that do not apply, scanning, scoping).
- Resolving asset URLs in PHP or Blade; images and fonts through Vite.
- "Styles missing", 404 on `build/` files, requests to a dev-server host, HMR not connecting, block editor styles absent.

Native-first: before adding a build step, check whether WordPress already covers it: `theme.json` for editor settings, `block.json` fields (`style`, `editorStyle`, `viewScript`) for block assets, `add_editor_style`, `wp_enqueue_style` and `wp_enqueue_script` for the rest. Vite produces the files; these WordPress mechanisms still decide where and when they load.

## Inputs required

1. Profile and Acorn base path (session context). The Vite config lives at the base path.
2. Node runner and where Node runs (same container as PHP, or a separate service).
3. Whether an editor entry exists (`editor.css`, `editor.js`) and whether `theme.json` is generated.
4. Dev server host and published port, if the user wants HMR.

### Per-profile build facts

| | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Vite config | theme root | plugin root | project root |
| Output | `<theme>/public/build/` | `<plugin>/public/build/` | `public/build/` (inside the webroot) |
| Production `base` | the theme's public URL path plus `public/build/` (Sage's default targets a Bedrock theme path; adjust for plain WordPress) | the plugin's URL path plus `public/build/`; dev server uses `/` | `/build/` |
| Acorn URL source | default `theme` manifest, which already points at the active theme | publish `config/assets.php` with your own manifest whose `path` ends in `/build` | project `config/assets.php`; confirm `path` ends in `/build` |
| Node location | PHP container or a Node service | PHP container (reference project) | a separate Node service |
| HMR port | Vite default 5173 unless taken | Vite default 5173 | a port published by the Node service (pick one unused by other Lando apps) |
| `theme.json` from Tailwind | `wordpressThemeJson` in the Sage template | not applicable (no theme) | block-theme dependent |

Why the `/build` rule matters for plugins: Acorn's Vite middleware rewrites a manifest to the active theme's `public/build` URL unless that manifest's `path` already ends with `/build`. A plugin that keeps the default `theme` manifest, or a manifest path without that suffix, gets asset URLs under `/wp-content/themes/...` and 404s. Verified by reading `ViteMiddleware` and by calling `Vite::asset()` in a plugin context.

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando yarn build`, `lando wp acorn optimize:clear`), never a bare `npm`/`yarn`/`wp`, never the placeholder, never "prefix with lando if you use it". Build or cache commands that run in CI or a deploy script go in a separate block labelled with where they run.

1. **Read before editing.** Open `vite.config.js`, `package.json`, `resources/css/app.css`, `config/assets.php` (if any) and the layout that calls `@vite`.
2. **Entries.** List every file the browser or editor loads as an entry in `laravel({ input: [...] })`: `resources/css/app.css`, `resources/js/app.js`, and, when used, `editor.css`, `editor.js`. Anything not listed is not in the manifest and `Vite::asset()` throws "Unable to locate file in Vite manifest".
3. **Plugins in the config.** `tailwindcss()` from `@tailwindcss/vite`; `laravel({...})`; `wordpressPlugin()` from `@roots/vite-plugin` when scripts import `@wordpress/*` (it maps them to the global `wp.*` and writes `editor.deps.json`); `wordpressThemeJson()` only on themes that generate `theme.json` from Tailwind.
4. **Base and output.** Set `base` to the public URL of the build folder for this profile (table above). Leave `buildDirectory` and `publicDirectory` at the defaults (`build`, `public`) so Acorn's defaults match.
   - Plugin (`acorn-mu-plugin`): the manifest in the plugin's `config/assets.php` has exactly two keys, `path` and `url`, both ending in `build` (for example `'path' => MY_PLUGIN_PATH.'public/build', 'url' => MY_PLUGIN_URL.'public/build'`). Do not add `assets` or `bundles` keys: Vite reads its own `manifest.json`, and a listed file that does not exist yet makes manifest loading throw. Full example: [references/vite-config.md](references/vite-config.md).
5. **Tailwind in CSS.** Start from the single import `@import "tailwindcss";` or the split imports of `theme.css` and `utilities.css` (see scoping in [references/tailwind-v4.md](references/tailwind-v4.md)). Declare tokens in `@theme`, scanning paths with `@source`, and use `@reference` in per-component CSS. Do not create `tailwind.config.js`.
6. **Use the assets.**
   - Blade layout: `@vite(['resources/css/app.css', 'resources/js/app.js'])`.
   - A single URL in Blade or PHP: `Vite::asset('resources/images/logo.svg')`; contents: `Vite::content('resources/css/editor.css')`; dev server running: `Vite::isRunningHot()`.
   - Images and fonts referenced from Blade must be listed under `assets: [...]` in the `laravel()` options (for example `resources/images/**`), otherwise they are not copied into the build.
   - Editor styles: inject the editor stylesheet through `block_editor_settings_all` or `add_editor_style`; load editor scripts only in the editor screen.
7. **Dev server.** `{{runner.node}} run dev`, with host `0.0.0.0`, a fixed port, `strictPort`, HMR host/port the browser can reach, and `APP_URL` set to the site URL so CORS allows the page origin. Details and Lando wiring: [references/dev-server.md](references/dev-server.md).
8. **Production build.** `{{runner.node}} run build`. Confirm `manifest.json` and the hashed files exist under the output folder, then `{{runner.cache}}`.
9. **Report** the config change, the command you ran and what the manifest now contains.

Per-profile config examples: [references/vite-config.md](references/vite-config.md).

## Verification

- `public/build/manifest.json` (inside the build folder) lists every entry you rely on.
- With the dev server stopped, `public/hot` does not exist; a page source shows hashed URLs under the build base, and those URLs return 200 (`curl -sI <url>`).
- `{{runner.wp}} eval 'echo \Illuminate\Support\Facades\Vite::asset("resources/css/app.css");'` prints a URL under the profile's build base (for a plugin, `/wp-content/mu-plugins/<plugin>/public/build/assets/...`, not `/themes/`). Run it after `{{runner.node}} run build` and `{{runner.cache}}`.
- With the dev server running, the page source shows dev-server URLs and a CSS edit appears without a reload.
- A utility class you added in a Blade file is present in the built CSS (search the output for its generated selector).
- Editor check: open a post in the block editor and confirm the editor stylesheet applies.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Page asks for files on a dev-server host that is down | Stale `public/hot` after the server stopped | Delete the file or stop the server cleanly; rebuild |
| 404 on `.../build/assets/app-*.css` and the URL contains `/themes/<theme>/` on a plugin | No plugin manifest (Acorn's default `theme` manifest is used) or its `path` does not end with `/build`, so the middleware swaps in the theme URL | Publish `config/assets.php` with only `path` and `url`, both ending in `build`; set the production `base` to the plugin's build URL path; rebuild with `{{runner.node}} run build` and clear caches with `{{runner.cache}}` |
| `Unable to locate file in Vite manifest` | File not in `input` or `assets`, or the build is older than the code | Add the entry, rebuild |
| `Vite manifest not found` | No build yet on this machine or wrong output folder | Run the build; check `publicDirectory` and `buildDirectory` |
| A utility such as `font-heading` has no effect | Token declared with the v3 name `--font-family-*` | Use `--font-*` (for example `--font-heading`); a `--font-family-*` token generates no utility |
| `max-w-sm` renders 8px wide | A `--spacing-sm` token exists and wins over the container scale | Use a distinct name (`--container-narrow` with `max-w-narrow`) or a `--max-width-*` token; declaring `--container-sm` does not help |
| `text-xl` ignored on `h2` | Unlayered `h2 { font-size }` beats layered utilities | Put base typography in `@layer base`, or use a modifier class at the same level |
| Classes built by string concatenation have no styles | Tailwind's scanner reads full class names only | Use complete class names, a class map, or a CSS variable set inline |
| Per-component CSS doubles the bundle size | `@import "../app.css"` copies the whole stylesheet | Use `@reference "../app.css";` |
| HMR connects but styles do not change | Browser cannot reach the HMR host/port | Set `hmr.host` and `hmr.port` to a published address; see the dev-server reference |
| Build fails only on one Node version | An old Node or an incompatible plugin version | Align Node with the `engines` field; if a plugin is incompatible, say so and ask before dropping it |

## Escalation

- A new global CSS rule that affects markup you do not own (theme, plugin, third-party blocks): propose scoping first, then ask.
- Changing the Node major version, adding a bundler plugin, or changing the public base affects every deploy: show the diff and wait for approval.
- Container networking, ports and DNS: hand over to `lando-wp`.

<!-- verified: node_modules/laravel-vite-plugin/dist/index.js:55-61 — default dev CORS: localhost, APP_URL, *.test;
refs/roots-sage/vite.config.js:7-9,11-45 — Sage config: base '/app/themes/sage/public/build/', laravel input app/editor css+js, assets images/fonts, wordpressPlugin, wordpressThemeJson, aliases;
refs/roots-sage/resources/css/app.css:1-4 — @import "tailwindcss" theme(static) and @source lines; no tailwind.config.js in the template;
refs/roots-sage/app/setup.php:11-50 — block_editor_settings_all injection, editor.deps.json via Vite::content, Vite::withEntryPoints, isRunningHot;
refs/roots-acorn/src/Roots/Acorn/Assets/Vite.php:17-20 — assetPath uses asset()->uri() and replaces /build/build/ with /build/;
refs/roots-acorn/src/Roots/Acorn/Assets/Middleware/ViteMiddleware.php:20-30 — manifest rewritten to get_theme_file_uri('public/build') unless path ends with /build;
refs/roots-acorn/config/assets.php — default manifest 'theme' with theme file path/uri;
refs/roots-acorn/src/Illuminate/Foundation/Vite.php:49,237-239,886-896,1221-1224 — default buildDirectory 'build', hotFile public_path('/hot'), asset(), isRunningHot();
lando wp eval in the reference acorn-mu-plugin project — Vite::asset() in the mu-plugin returned /wp-content/themes/<theme>/public/build/... (middleware rewrite confirmed);
the mu-plugin's config/assets.php — plugin manifest path public (no /build suffix), which triggers the rewrite;
the mu-plugin's vite.config.js — base '/wp-content/mu-plugins/<plugin>/public/build/' on build, '/' in dev; hmr host localhost:5173;
node_modules/laravel-vite-plugin/dist/index.d.ts:14-26 — publicDirectory 'public', buildDirectory 'build', hot file default;
radicle-app facts checked against a licensed local Radicle project; not reproduced here;
node_modules/@roots/vite-plugin/README.md — @wordpress/* to wp.* externals, editor.deps.json, theme.json from Tailwind, editor CSS HMR;
tailwindcss 4.3.3 compile() runs (scratchpad tw-test*.mjs) — max-w-sm resolves --spacing-sm before --container-sm; --font-family-x makes no utility; prefix(tw), important, and theme(static) behave as described -->
