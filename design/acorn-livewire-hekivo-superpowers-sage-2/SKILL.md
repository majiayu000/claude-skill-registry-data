---
name: acorn-livewire
description: Use when creating, wiring or fixing a Livewire 4 component in an Acorn app - make:livewire --class, app/Livewire, wire:model modifiers (.live, .blur, .debounce), wire:key, attributes (#[Locked]/#[Computed]/#[Validate]/#[On]), lifecycle hooks, @livewireScripts, the /livewire-<hash>/update route, installing livewire/livewire on Radicle. For errors that start after a deploy (419, RangeError, stale HTML) use roots-debugging; for JSON endpoints use acorn-routes-api; for Alpine-only UI use tailwind-vite-assets.
---

# Livewire 4 under Acorn

Livewire runs inside the Acorn application that your profile boots. There is no `roots/acorn-livewire` package: you install `livewire/livewire` next to Acorn and Acorn discovers its service provider. Livewire 4 changed several v3 habits (endpoint URLs, `wire:model` modifiers, the generator default), so check the version first and read [references/state-patterns.md](references/state-patterns.md) before writing modifiers.

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.composer}}`, `{{runner.test}}`, `{{runner.cache}}`) come from the session context. On Lando they default to `lando wp`, `lando wp acorn`, `lando composer`, the project's test tooling and its cache-clear tooling. Run Composer from the Acorn base path (for an mu-plugin, pass `--working-dir=<app path>` when the runner starts at the repo root).

## When to use

- Server-validated forms, multi-step wizards, filters or search that query WordPress on input.
- Wiring Livewire into a profile for the first time (Radicle has no Livewire by default).
- A component does not mount, an action does nothing, the update request fails (404, 419, 500), or the page breaks right after a deploy.

Not for: client-only UI (tabs, toggles, motion; use Alpine through `tailwind-vite-assets`), read-only data for a template (View Composer, `acorn-stack`), public JSON for JS (`acorn-routes-api`).

## Inputs required

1. Active profile, Acorn base path and PSR-4 namespace (session context).
2. Livewire version from the app's `composer.lock` (`livewire/livewire`). This skill targets 4.x; for 3.x stop and say so.
3. `config/livewire.php` in the base path, if published: `class_namespace`, `view_path`, `make_command.type`, `inject_assets`, `release_token`.
4. The boot call (`Application::configure()...->boot()`): provider list and `withRouting(...)` arguments.
5. Whether the page that renders the component sits behind a full-page or edge cache.

### Profile differences

| Item | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Installed by default | no | often (check `composer.lock`) | no |
| Where Composer runs | theme folder | plugin folder | project root |
| Provider | auto-discovered from the theme's `vendor/composer/installed.json` (`extra.laravel.providers`) | auto-discovered from the plugin's vendor; many projects also list `\Livewire\LivewireServiceProvider::class` in `withProviders()` so a custom Livewire route provider can follow it | auto-discovered from the root vendor; app providers stay in `composer.json` `extra.acorn.providers` |
| Boot file to touch | `functions.php` | the plugin's boot or configurator class | the tracked Acorn boot mu-plugin (write-guarded: show the diff and let the user apply it) |
| Default class namespace | `App\Livewire` | must match the plugin namespace: set `class_namespace` | `App\Livewire` |
| Layout for the directives | `resources/views/layouts/app.blade.php` in the theme | the plugin's layout, or each template that renders components | the theme layout under the root `resources/views` |

## Procedure

1. **Check what exists.** Read `composer.lock`, `config/livewire.php` and the boot call. If Livewire is already installed, skip to step 4.
2. **Install** (only when the user asked for Livewire):
   - `{{runner.composer}} require livewire/livewire` in the base path.
   - Livewire needs `APP_KEY`. Check it without printing it: `{{runner.wp}} eval 'var_dump((bool) config("app.key"));'`. If false, run `{{runner.acorn}} key:generate` or ask the user to set it in the environment.
   - If the provider is not picked up, rebuild the package manifest: `{{runner.acorn}} package:discover`.
3. **Wire routing and assets.**
   - Add `wordpress: true` to `withRouting(...)` as the Roots Livewire guide asks. Know the side effect: every WordPress page then runs the `wordpress` middleware group, a copy of `web` (session start, queued cookies). Check that cached pages do not start carrying a session `Set-Cookie`.
   - Put `@livewireStyles` in `<head>` and `@livewireScripts` before `</body>` of every layout that can render a component. Auto-injection (`inject_assets`, default `true`) listens to Laravel's `RequestHandled` event and only rewrites bodies that pass through the HTTP kernel with `</html>` in them: Acorn routes yes, WordPress-rendered templates no. The directives render once per request, so keeping both is safe.
   - Publish the config only when you need to change it: `{{runner.acorn}} vendor:publish --tag=livewire:config`. On `acorn-mu-plugin` set `class_namespace` to `<Namespace>\Livewire`.
4. **Generate the component with a class.** Livewire 4's generator defaults to a single-file component (`resources/views/components/⚡name.blade.php`, config `make_command.type` = `sfc`). When the project uses classes:
   ```bash
   {{runner.acorn}} make:livewire PricingCalculator --class
   # app/Livewire/PricingCalculator.php + resources/views/livewire/pricing-calculator.blade.php
   ```
   Or set `'make_command' => ['type' => 'class']` in `config/livewire.php` once. Then `{{runner.cache}}`.
5. **Write the class** with these rules (details in [references/state-patterns.md](references/state-patterns.md)):
   - Public properties are the snapshot: scalars and arrays only, IDs instead of `WP_Post`/`WP_Term`, never secrets.
   - `#[Locked]` for values set at mount that the client must not change; `#[Computed]` for derived data; validation in `#[Validate]` or `rules()`.
   - `booted()` for per-request context that must exist before any action (language, current site). Update requests are Acorn routes answered on `parse_request`: `init` has run; `template_redirect`, `wp_head` and `the_content` never run.
   - Check capabilities inside actions (`current_user_can()`): any visitor can call any public method.
6. **Write the view** with exactly one root element, `wire:key` on loop items, `wire:target` on every loading state, and `wire:ignore` around DOM owned by Alpine or third-party widgets ([references/alpine-interop.md](references/alpine-interop.md)).
7. **Embed it** in Blade: `<livewire:pricing-calculator :plan="$plan" />` or `@livewire('pricing-calculator', ['plan' => $plan], key($id))`. The name is the kebab-case class path (`Forms\Contact` becomes `forms.contact`).
8. **Plan for cached HTML.** If the page is edge- or page-cached, the first render is shared by every visitor: render neutral defaults and push per-visitor state after load with one action or one `Livewire.dispatch()`. Changing the set or order of public properties, or `APP_KEY`, breaks pages still served from cache; plan a purge with the release and consider a release token ([references/common-errors.md](references/common-errors.md)).
9. **Uploads** need decisions first (disk, multiple replicas, media library): [references/file-uploads.md](references/file-uploads.md).

## Verification

- `{{runner.acorn}} route:list --path=livewire` lists `POST livewire-<hash>/update`, `GET livewire-<hash>/livewire.js` or `livewire.min.js` (minified when `app.debug` is false), the source maps and, when uploads are used, `upload-file` and `preview-file`. A project can replace the script and update routes with `Livewire::setScriptRoute()` / `setUpdateRoute()`; the update route name must end in `livewire.update`.
- In the browser, the Network tab shows `POST /livewire-<hash>/update` returning 200 and the console has no `[wire:model="x"] property does not exist` warning.
- The rendered HTML contains the Livewire `<script>` once, and its update URI has no unexpected path prefix (multilingual plugin, subdirectory install).
- Component tests instantiate the class directly, or use `Livewire::test()` when the project's test setup boots Acorn; run them with `{{runner.test}}`.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Component markup renders but nothing reacts | Livewire script missing on a WordPress-rendered page (auto-injection does not reach it) | Add `@livewireScripts` / `@livewireStyles` to the layout |
| `Unable to find component` | Class outside `class_namespace`, wrong kebab name, or a stray `⚡` single-file component | Fix the namespace or name; regenerate with `--class`; dump autoload in the base path |
| `POST …/update` returns 404 in curl but works in the browser | `RequireLivewireHeaders` aborts with 404 when the `X-Livewire` header is missing | Not a routing bug; test from the browser or send the header |
| 404 on `/livewire-<hash>/…` from cached pages | `APP_KEY` changed (the hash derives from it), or a language or subdirectory prefix reached the URL | Keep the key identical on every instance; purge cached HTML; pin the root URL if a plugin rewrites `home_url()` |
| 419 "This page has expired" | Acorn's `web` group runs no CSRF check; 419 here means release-token mismatch, a corrupt snapshot checksum (`APP_KEY` differs), a client write to a `#[Locked]` property, or a type error on a typed property | Reload a fresh copy; align `APP_KEY`; do not raise session lifetime |
| `RangeError: Maximum call stack size exceeded` in `dataSet` right after a deploy | Cached HTML carries a snapshot whose public-property order or set no longer matches the class | Purge the cache; avoid reordering public properties; use a release token |
| A field change never reaches `updated()` | v4 `wire:model.blur` / `.change` / `.enter` only sync the client value; no request is sent | Use `.live.blur`, or call an action |
| Values flip back or DOM is clobbered | Several `$wire.prop = …` writes in flight, missing `wire:key`, or no `wire:ignore` on third-party DOM | One batched action; add keys; add `wire:ignore` |
| Strings switch language after the first interaction | The update URL carries no language context | Capture the language at mount (`#[Locked]`) and switch to it in `booted()` |

More symptoms and diagnostics: [references/common-errors.md](references/common-errors.md).

## Escalation

- The cause is not Livewire (500 on every request, Acorn does not boot, assets 404): `roots-debugging`.
- The fix needs a cache purge, a key rotation or an edge configuration change: stop and ask; those are operational decisions.
- Livewire 3 in the lock file, or a request to upgrade from 3 to 4: report the version and ask before migrating.
- A pure JSON need with no server-rendered UI: `acorn-routes-api`.

<!-- verified:
vendor/livewire/livewire/src/Mechanisms/HandleRequests/EndpointResolver.php:15 — prefix '/livewire-' . substr(sha256(app.key . 'livewire-endpoint'), 0, 8); :25 /update; :33 livewire.js | livewire.min.js
vendor/livewire/livewire/src/Mechanisms/FrontendAssets/FrontendAssets.php:25-27 — minified script route unless app.debug; :113 styles render once per request
vendor/livewire/livewire/src/Features/SupportAutoInjectedAssets/SupportAutoInjectedAssets.php:24,55,65 — injection on RequestHandled, only when body contains </html>, honours inject_assets
vendor/roots/acorn/src/Roots/Acorn/Application/Concerns/Bootable.php:179-206 — wordpress catch-all route; :243-244 other routes handled on parse_request; :253-284 WordPress output flushed at shutdown outside the response body
vendor/roots/acorn/src/Roots/Acorn/Configuration/Middleware.php:88 — PreventRequestForgery commented out in web; :100 wordpress group = web
vendor/roots/acorn/src/Roots/Acorn/PackageManifest.php:84 — extra.acorn ?? extra.laravel discovered; Application.php:255-273 composer paths = base path, content root, theme, active plugins
vendor/livewire/livewire/composer.json:47-50 — extra.laravel.providers LivewireServiceProvider
vendor/livewire/livewire/config/livewire.php:72 make_command.type 'sfc'; :182 inject_assets true; :250 release_token 'a'
vendor/livewire/livewire/src/Features/SupportConsoleCommands/Commands/MakeCommand.php:64,92 — default type from config, --class option
vendor/livewire/livewire/src/Mechanisms/HandleRequests/HandleRequests.php:99-111 — update route forced into web + RequireLivewireHeaders, name ends livewire.update; :211 TypeError -> 419
CorruptComponentPayloadException.php:30, CannotUpdateLockedPropertyException.php:20, LivewireReleaseTokenMismatchException.php:12 — 419 responses
vendor/livewire/livewire/dist/livewire.js:15565-15650 — wire:model modifiers split around .live (4.3.5)
roots-docs acorn/using-livewire-with-wordpress.md — composer require, key:generate, withRouting(wordpress: true), directives in layout
radicle-app facts checked against a licensed local Radicle project; not reproduced here
-->
