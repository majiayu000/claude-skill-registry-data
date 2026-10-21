---
name: acorn-stack
description: Use when changing how Acorn boots or is wired on a Sage theme, Acorn mu-plugin or Radicle root - Application::configure(), withProviders(), withRouting(), ACORN_BASEPATH, base_path(), provider register() vs boot(), where providers are registered (functions.php, config/app.php, composer.json extra.acorn.providers), config publishing, optimize:clear, "'acorn' is not a registered wp command". For generating providers, blocks or composers use acorn-scaffolding; for hook timing use wp-hooks-lifecycle; for unexplained breakage use roots-debugging.
---

# Acorn stack (theme, mu-plugin, project root)

Acorn is the same library in all three profiles. What changes is **where it boots, which directory it treats as `base_path()`, and where providers are listed**. Read the profile, namespace and Acorn base path from the session context before touching anything.

Runner placeholders come from the session context: `{{runner.wp}}` (WP-CLI), `{{runner.acorn}}` (WP-CLI `acorn` subcommand), `{{runner.composer}}`, `{{runner.node}}`, `{{runner.test}}`, `{{runner.cache}}` (the project's cache-clear wrapper, if any). On a Lando project the defaults are `lando wp`, `lando wp acorn`, `lando composer`, a Node tooling command such as `lando npm` or `lando yarn`, and whatever cache tooling `.lando.yml` defines. Never run WP-CLI, Composer, PHP or Node on the host for project work.

## When to use

- Adding or changing a service provider, binding, View Composer, Blade component or config file.
- Deciding where a piece of logic lives (provider, composer, component, bootstrap file, service class).
- Acorn does not boot, boots with the wrong base path, or `{{runner.acorn}}` is missing.
- A change is not picked up and you suspect an Acorn cache (config, routes, views, packages, ACF Composer manifest).

Not for: scaffolding new artifacts (`acorn-scaffolding`), hook placement and timing (`wp-hooks-lifecycle`), Livewire (`acorn-livewire`), routes and middleware (`acorn-routes-api`), triage of errors (`roots-debugging`).

## Inputs required

1. Profile (`sage-theme`, `acorn-mu-plugin`, `radicle-app`), the Acorn base path and the PSR-4 namespace mapped to `app/` (session context; confirm with the command in step 0).
2. The Composer project that requires `roots/acorn` (theme folder, plugin folder, or project root). Its `composer.json` decides the namespace and which packages are discovered.
3. What is being added or changed, and whether it needs the container (DI, config) or is a plain WordPress hook.

### Profiles at a glance

| Concern | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Base path | Theme folder, inferred from the theme's `composer.json` | Plugin folder: the plugin must define `ACORN_BASEPATH` or pass a path to `Application::configure($path)` | Project root: `ACORN_BASEPATH` defined in `bedrock/application.php` |
| Boot call | `functions.php` calls `Application::configure()->withProviders([...])->boot()` while the theme loads (after `setup_theme`, before `after_setup_theme`) | Main plugin file defers the boot to `after_setup_theme`, often through a small configurator class | A committed mu-plugin boots on `after_setup_theme` |
| Provider list | `withProviders([...])` in `functions.php` (Sage ships `App\Providers\ThemeServiceProvider`) | `withProviders([...])` in the boot code or configurator class | `composer.json` → `extra.acorn.providers` |
| Namespace | `App\` | Project namespace from the plugin's `composer.json` | `App\` |
| Blade templates for WordPress pages | `SageServiceProvider` filters the template hierarchy | No Sage filters: the plugin hooks `template_include` / `*_template_hierarchy` itself, or only renders views from blocks, shortcodes and routes | Root `resources/views`; the theme folder holds only `index.php` and `style.css` |
| `{{runner.acorn}}` available | Only while the theme is active | Always (mu-plugins cannot be deactivated) | Always |
| Usually installed | ACF Composer, Poet only if required | ACF Composer, Poet, Livewire are common | No ACF, no Poet, no Livewire by default |

Deep dive: [references/boot-and-paths.md](references/boot-and-paths.md).

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

### 0) Confirm the runtime facts, do not assume them

```bash
{{runner.wp}} eval 'echo base_path(), PHP_EOL, app()->getNamespace(), PHP_EOL, storage_path(), PHP_EOL;'
{{runner.acorn}} about
```

If `base_path()` points at the theme on an `acorn-mu-plugin` project, the plugin is missing `ACORN_BASEPATH` (see Failure modes). If `{{runner.acorn}}` prints `'acorn' is not a registered wp command`, the theme or plugin that boots Acorn is not active or crashed before booting.

### 1) Decide where the code goes

| Logic | Location | Native mechanism |
|---|---|---|
| Plain `add_action` / `add_filter`, no dependencies | Bootstrap files: Sage `app/setup.php`, `app/filters.php`; mu-plugin bootstrap files required by the main file; Radicle theme config or a provider | WordPress Plugin API |
| Hooks that need services or config | A provider's `boot()` | `Illuminate\Support\ServiceProvider` |
| Container bindings | A provider's `register()` | `singleton`, `bind`, `instance` |
| Business logic, API clients | `app/Services/` (or a domain folder), bound in a provider when it needs config | Container auto-resolution of type-hinted constructors |
| Data for an existing template | View Composer in `app/View/Composers/` | Auto-discovered by Acorn's `ViewServiceProvider` |
| Reusable markup with props | Blade component (`app/View/Components/` + `resources/views/components/`, or anonymous view only) | Blade `<x-…>` convention |
| Editor-placed section | Block (see `acorn-scaffolding`) | ACF Composer or `register_block_type` |
| Settings that differ per environment | `config/<file>.php` reading `env()` | Acorn config repository |

Hook placement details per profile live in `wp-hooks-lifecycle`. Search `app/`, the bootstrap files and the existing providers before adding a class.

### 2) Providers

1. Generate with `{{runner.acorn}} make:provider ExampleServiceProvider` (or follow `acorn-scaffolding`).
2. `register()`: bindings only. `boot()`: hooks, view composers, anything that resolves services. Never `add_action` in `register()` or in the constructor.
3. Register it where this profile reads providers (table above). The generator only appends to a bootstrap providers file (`<bootstrap path>/providers.php`, by default inside `storage/framework/`) when one already exists, which is rare, so assume it did not.
4. Base class: `Illuminate\Support\ServiceProvider` for feature providers. Only a Sage theme's main provider extends `Roots\Acorn\Sage\SageServiceProvider` (it adds the template-hierarchy filters). Do not extend it in an mu-plugin or Radicle project.
5. A provider that throws during `register()`/`boot()` is **skipped**, the exception is reported to the log, and it is re-thrown after boot only in `local`/`development`/`testing` web requests. On production the feature silently disappears: check the log.

Full rules, discovery and examples: [references/providers-and-container.md](references/providers-and-container.md).

### 3) Views, composers, components

- Views resolve from `config('view.paths')`, by default `resources/views` under the base path.
- View Composers: extend `Roots\Acorn\View\Composer`, live anywhere under `app/View/Composers/`, set `protected static $views = [...]`. Acorn discovers them; no manual wiring. Data from `with()` does **not** overwrite data already passed to the view; `override()` does.
- Blade components: class components in `app/View/Components/` resolve by name (`<x-product-card>`); anonymous components are files in `resources/views/components/`. `config/view.php` → `components` is only for aliases.
- Escape once: `{{ $value }}` already escapes; never wrap `esc_*()` inside it (`wp-security-escaping`).

Details: [references/views-composers-components.md](references/views-composers-components.md).

### 4) Config, storage, publishing

- Every file in the base path's `config/` is loaded; Acorn ships defaults for `app`, `cache`, `database`, `logging`, `view` and others, so publish only what you change: `{{runner.acorn}} vendor:publish --tag=<tag>` or `{{runner.acorn}} acorn:init storage`.
- `storage_path()` is `<base>/storage` when that folder exists, otherwise `wp-content/cache/acorn` (created on demand). Compiled views, caches and logs live there.
- An mu-plugin with no `config/`, `resources/` or `storage/` folder of its own falls back to the **active theme's** folder of that name before the default. Create the folders in the plugin.

### 5) Caches: know which layer you are clearing

| Layer | Files | Rebuild | Clear |
|---|---|---|---|
| Config, routes | `<storage>/framework/cache/{config,routes-v7}.php` | `{{runner.acorn}} optimize` | `{{runner.acorn}} optimize:clear` |
| Provider and package manifests | `<storage>/framework/cache/{services,packages}.php` | `{{runner.acorn}} package:discover` | delete the files |
| Compiled Blade | `<storage>/framework/views/` | `{{runner.acorn}} view:cache` | `{{runner.acorn}} view:clear` |
| ACF Composer manifest + generated `block.json` | `<storage>/framework/cache/acf-composer/` | `{{runner.acorn}} acf:cache` (also run by `optimize`) | `{{runner.acorn}} acf:clear` (also run by `optimize:clear`) |
| Laravel cache store | per `config/cache.php` (file, Redis…) | n/a | `{{runner.acorn}} cache:clear` (also run by `optimize:clear`) |
| WordPress object cache | Redis/Memcached drop-in | n/a | `{{runner.wp}} cache flush` |

Rules:

- Treat `optimize:clear` and `optimize` as a pair. `optimize:clear` alone also deletes the ACF Composer manifest and flushes the Laravel cache store; at least one production mu-plugin returned 500 on every request until the manifest was rebuilt.
- While a cache exists, edits to what it holds are **ignored**: cached config ignores `config/*.php` and `.env` edits; a cached ACF Composer manifest ignores edits to `fields()` and to block properties.
- Prefer `{{runner.cache}}` when the project defines one; it usually chains the steps in the right order.

Details: [references/caches-and-config.md](references/caches-and-config.md).

## Verification

```bash
{{runner.wp}} eval 'echo base_path(), PHP_EOL, app()->getNamespace(), PHP_EOL;'
{{runner.wp}} eval 'var_dump(app()->getProvider(App\Providers\ExampleServiceProvider::class) !== null);'   # use your namespace
{{runner.acorn}} list            # your commands and generators are present
{{runner.acorn}} route:list      # when routes changed
{{runner.cache}}                 # or: {{runner.acorn}} optimize:clear && {{runner.acorn}} optimize
{{runner.test}}
```

Then load the affected page and read `storage/logs/` (or `wp-content/cache/acorn/logs/`) for `Skipping provider` lines. Report what you ran and what you saw.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `'acorn' is not a registered wp command` | The theme or plugin that boots Acorn is inactive, or it fatals before `boot()` | Activate the theme (`sage-theme`); check the PHP error log; confirm `vendor/autoload.php` exists in the Composer project that owns Acorn |
| `base_path()` is the theme on an mu-plugin project | No `ACORN_BASEPATH` and no path passed to `configure()`; inference falls through to the theme's `composer.json` or `app/` | Define `ACORN_BASEPATH` in the main plugin file before booting, or call `Application::configure($pluginPath)` |
| Provider never runs | Not listed where this profile reads providers, or skipped after an exception | Add it to `withProviders()` / `extra.acorn.providers` / `config/app.php`; search the log for `Skipping provider` |
| Package provider not found after `composer require` | Stale package manifest, or the package lives in a Composer project Acorn does not scan | `{{runner.acorn}} package:discover`; mu-plugin packages are found only because the base path points at the plugin |
| Composer data missing in the view | Class outside `app/View/Composers/`, does not extend `Roots\Acorn\View\Composer`, or `$views` does not match the view name | Fix the class; `{{runner.acorn}} view:clear` |
| Config or `.env` edit ignored | Config cache from `optimize` | `{{runner.acorn}} config:clear` then `optimize` |
| ACF field or block property edit ignored | ACF Composer manifest still holds the old definition | `{{runner.acorn}} acf:cache` (or `optimize`) |
| 500 on every request right after `optimize:clear` | Project depends on the ACF Composer manifest or a cached config | `{{runner.acorn}} optimize`; afterwards always run the pair |
| Hook registered in `register()` behaves oddly | Container not booted; other providers not registered yet | Move it to `boot()` |
| Sage template filters missing in an mu-plugin | `SageServiceProvider` belongs to the theme profile | Hook `template_include` in the plugin's own provider |

## Escalation

Stop and ask when: the base path or namespace in the session context disagrees with step 0; a provider must be ordered relative to others and you cannot tell why; the change needs `optimize` behaviour on a remote environment; a fix would edit `wp-config.php`, `.env`, `bedrock/*.php` or files under `vendor/`; or the profile is none of the three.

<!-- verified:
vendor/roots/acorn/src/Roots/Acorn/Configuration/Concerns/Paths.php:16-27 — inferBasePath order APP_BASE_PATH, ACORN_BASEPATH, theme composer.json, theme app/, closest composer.json, fallback;
Paths.php:85-101 — findPath tries app path, basePath(type), get_theme_file_path(type); :115-129 storage fallback wp-content/cache/acorn;
Application.php:69-84 (acorn 6.2.0) — configure() builds withPaths/withKernels/withEvents/withCommands/withProviders/withMiddleware/withExceptions;
ApplicationBuilder.php:140-150,167-170 — withProviders merges into bootstrap providers path; boot() calls bootAcorn immediately (no hook);
Application/Concerns/Bootable.php:41-57,79-110 — WP-CLI registers the `acorn` command only when Acorn booted;
Application.php:247-275 — package discovery scans base path, content root, template, stylesheet and active_plugins dirs;
PackageManifest.php:62-97 — reads extra.acorn / extra.laravel providers including the root composer.json;
Application.php:320-339 — config app.providers + package providers registered; :307-313,367-391 — failing providers skipped and reported;
View/ViewServiceProvider.php:169-197 — composers auto-discovered in app/View/Composers; View/Composer.php:61-90 — with() does not overwrite view data, override() does;
Illuminate/Foundation/Console/OptimizeClearCommand.php:59-70 — clear runs config, cache, compiled, events, routes, views + package tasks;
log1x/acf-composer 3.4.6 src/Providers/AcfComposerServiceProvider.php:67-73 — optimizes acf:cache / acf:clear; src/Composer.php:109-117 — fields read from manifest when cached;
refs/roots-sage/functions.php:35-39 — Sage boots at include time with withProviders; refs/roots-docs/acorn/installation.md:126-128 — inactive booter error;
wp/wp-settings.php:705,741-757 — setup_theme, theme functions.php, after_setup_theme order (WP 7.1.3)
-->
