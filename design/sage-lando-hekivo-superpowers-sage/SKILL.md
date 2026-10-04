---
name: superpowers-sage:sage-lando
description: >
  Sage theme with Acorn (Laravel IoC for WordPress) and Lando — lando start,
  lando info, lando acorn, Service Providers, View Composers, Blade components,
  ACF Composer blocks and fields, Poet CPT config/poet.php, AppServiceProvider,
  ViewServiceProvider, resources/views/, resources/css/app.css @theme Tailwind v4,
  resources/js/app.js, content/themes/{theme}/, lando yarn dev, lando yarn build,
  Blade @extends @section @include @component, Bedrock directory structure,
  lando wp, composer require, lando composer
user-invocable: false
---

# Roots Sage + Acorn + Lando

## When to use

- Setting up or modifying a Lando-based WordPress development environment
- Creating ACF blocks, field groups, partials, or options pages
- Building Blade components, view composers, or layouts
- Configuring Vite, Tailwind v4, or frontend assets
- Registering custom post types, taxonomies, or service providers
- Running Acorn or ACF Composer generators
- Troubleshooting Sage/Acorn/Lando issues

## Inputs required

- The project root path (contains `.lando.yml` and root `composer.json`)
- The theme directory path (contains theme `composer.json` and `app/` directory)
- The specific domain: blocks, fields, components, providers, frontend, or environment setup
- For generators: the name (and optional subdirectory) for the class being created

## Procedure

### 0) Triage

Determine the task domain:

1. **Environment setup / Lando** — read `references/lando-setup.md`, then go to step 1
2. **ACF blocks, fields, partials, options** — read `references/acf-composer.md`, then go to step 2
3. **Blade templates, components, composers** — read `references/blade-templates.md`, then go to step 3
4. **Frontend (Vite, Tailwind, CSS/JS)** — read `references/frontend-stack.md`, then go to step 4
5. **Service providers, services, bindings** — read `references/service-providers.md`, then go to step 5
6. **CPTs, taxonomies, navigation** — read `references/routing-and-cpts.md`, then go to step 6
7. **Testing** — read `references/testing.md`, then go to step 7
8. **Debugging** — read `references/troubleshooting.md`, then go to step 8
9. **WordPress plugin installation via Composer** — read `references/wordpress-composer.md`, then go to step 9

### 1) Understand the project structure

Confirm the project follows this layout:

```
project-root/
├── .lando.yml                    # Lando config — recipe: wordpress
├── .env                          # WP_HOME, DB credentials
├── composer.json                 # Root: roots/wordpress, WP core + plugins
├── wp/                           # WordPress core (managed by Composer)
├── content/
│   ├── plugins/                  # WordPress plugins
│   └── themes/
│       └── {theme}/
│           ├── composer.json     # Theme: roots/acorn, log1x/* packages
│           ├── package.json      # Theme: vite, tailwind, etc.
│           ├── vite.config.js
│           ├── app/
│           │   ├── Providers/
│           │   │   └── ThemeServiceProvider.php
│           │   ├── Services/       # Business logic classes
│           │   ├── View/
│           │   │   ├── Composers/  # View composers (auto-discovered)
│           │   │   └── Components/ # Blade components
│           │   ├── Blocks/         # ACF Gutenberg blocks
│           │   ├── Fields/         # ACF field groups
│           │   │   └── Partials/   # Reusable field partials
│           │   ├── Options/        # ACF options pages
│           │   ├── Console/
│           │   │   └── Commands/   # Custom Acorn CLI commands
│           │   ├── setup.php       # Theme support, nav menus, sidebars
│           │   ├── actions.php     # Global add_action calls
│           │   ├── filters.php     # Global add_filter calls
│           │   └── helpers.php     # Global helper functions
│           ├── config/
│           │   └── poet.php        # CPTs, taxonomies, block categories
│           ├── stubs/              # Custom generator stubs (auto-detected)
│           └── resources/
│               ├── views/          # Blade templates (.blade.php)
│               │   ├── layouts/    # Layout templates (app.blade.php)
│               │   ├── partials/   # Shared partials
│               │   ├── sections/   # Page sections
│               │   ├── components/ # Component views
│               │   └── blocks/     # ACF block views
│               ├── css/
│               ├── js/
│               └── fonts/
```

**Critical:** Two separate `composer.json` files exist. Root manages WordPress core and plugins; theme manages PHP dependencies (Acorn, ACF Composer, etc.). Always use `lando theme-composer` for theme packages.

### 2) Decide what to create using the decision guides

#### Composer vs Component vs Block

| Criteria                           | View Composer                                 | Blade Component                        | ACF Block                              |
| ---------------------------------- | --------------------------------------------- | -------------------------------------- | -------------------------------------- |
| **Purpose**                        | Inject data into existing WP templates        | Reusable UI piece with props/slots     | Editor-managed content block           |
| **Who controls content?**          | Developer (code)                              | Developer (props in templates)         | Content editor (Gutenberg UI)          |
| **Tied to WP template hierarchy?** | Yes (`front-page`, `single-post`)             | No — used anywhere via `<x-name>`      | No — placed in editor                  |
| **Has its own view file?**         | No — attaches to existing views               | Yes — `resources/views/components/`    | Yes — `resources/views/blocks/`        |
| **Has ACF fields?**                | No                                            | No                                     | Yes — defines editor UI                |
| **When to use**                    | Page-specific data (hero content on homepage) | Repeated UI (cards, buttons, sections) | Content editors need to add/arrange it |

#### Where to put logic

| Type of logic                                | Where it goes                        | Why                                      |
| -------------------------------------------- | ------------------------------------ | ---------------------------------------- |
| Theme support, menus, sidebars               | `setup.php`                          | WordPress bootstrap, runs once           |
| Simple `add_action` / `add_filter`           | `actions.php` / `filters.php`        | Global hooks, no dependencies            |
| Business logic (API calls, data processing)  | `Services/` class, bound in provider | Testable, injectable, reusable           |
| Hooks that depend on services                | `ThemeServiceProvider::boot()`       | Container is ready, dependencies resolve |
| Data for a specific template                 | View Composer                        | Auto-discovered, clean separation        |
| CPTs, taxonomies                             | `config/poet.php`                    | Declarative, no boilerplate              |
| Complex CPT registration (REST fields, meta) | Service Provider                     | When Poet's config isn't enough          |

#### `setup.php` vs `actions.php` vs `filters.php` vs ServiceProvider

- **`setup.php`** — `after_setup_theme` hook only: `add_theme_support()`, `register_nav_menus()`, image sizes, content width. No business logic.
- **`actions.php`** — Simple, self-contained `add_action()` calls that don't need injected services. If a hook needs a service, move it to a provider.
- **`filters.php`** — Same as above but for `add_filter()`. Query modifications, excerpt length, etc.
- **ServiceProvider `boot()`** — Any hook that depends on container-bound services, or complex logic that benefits from dependency injection.

### 3) Use generators — never create files manually

**Never create class files or view files manually.** Acorn and ACF Composer provide generators that scaffold the correct stub with proper namespace, base class, and paired view.

#### Acorn generators (`make:*`)

- `lando acorn make:component {Name}` — class + view in `app/View/Components/` + `resources/views/components/`
- `lando acorn make:composer {Name}` — view composer in `app/View/Composers/`
- `lando acorn make:provider {Name}` — service provider in `app/Providers/`
- `lando acorn make:command {Name}` — console command in `app/Console/Commands/`

Pass `Category/Name` for nested directories. Use `--inline`, `--view`, `--path` on `make:component`.

#### ACF Composer generators (`acf:*`)

- `lando acorn acf:block {Name}` — block class + view (interactive prompts)
- `lando acorn acf:field {Name}` — field group class
- `lando acorn acf:partial {Name}` — reusable field partial
- `lando acorn acf:options {Name}` — options page class
- `lando acorn acf:widget {Name}` — widget class + view

All accept `--force`. `acf:block --localize` for i18n stub. Bootstrap stubs: `lando acorn acf:stubs`.

For full generator details and custom stubs, see [`references/acf-composer.md`](references/acf-composer.md).

### 4) Run common Lando commands as needed

| Command                                   | Purpose                               |
| ----------------------------------------- | ------------------------------------- |
| `lando start`                             | Start environment                     |
| `lando acorn view:clear`                  | Clear compiled Blade cache            |
| `lando acorn optimize`                    | Cache config/routes                   |
| `lando acorn optimize:clear`              | Clear all caches                      |
| `lando acorn route:list`                  | List registered routes                |
| `lando acorn acf:sync`                    | Sync ACF field groups from code to DB |
| `lando theme-composer require vendor/pkg` | Add theme PHP package                 |
| `lando theme-yarn add pkg`                | Add theme JS package                  |
| `lando vite`                              | Start HMR dev server                  |
| `lando vite-build`                        | Build production assets               |
| `lando pint`                              | Fix PHP code style                    |

### 5) Read reference files before generating code

Read the relevant reference file **before generating code** in that domain:

| File                                                                   | When to read                                                                               |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [`references/lando-setup.md`](references/lando-setup.md)               | Setting up or modifying the Lando environment, `.env`, server configs                      |
| [`references/frontend-stack.md`](references/frontend-stack.md)         | Vite configuration, Tailwind v4, HMR, asset compilation, CSS/JS structure                  |
| [`references/acf-composer.md`](references/acf-composer.md)             | Creating blocks, field groups, partials, options pages, Builder API                        |
| [`references/service-providers.md`](references/service-providers.md)   | Container bindings, services, facades, dependency injection                                |
| [`references/blade-templates.md`](references/blade-templates.md)       | Composers, components, Sage directives, template hierarchy, layouts                        |
| [`references/routing-and-cpts.md`](references/routing-and-cpts.md)     | Custom post types, taxonomies (Poet), navigation menus (Navi)                              |
| [`references/testing.md`](references/testing.md)                       | Setting up Pest, writing tests, mocking WordPress functions                                |
| [`references/troubleshooting.md`](references/troubleshooting.md)       | Debugging common issues with Blade, ACF, Vite, Lando, autoloading                          |
| [`references/wordpress-composer.md`](references/wordpress-composer.md) | Installing WordPress plugins via Composer from `wp-packages.org` and local `.zip` packages |

## Verification

- Generator was used instead of manually creating files
- Class extends the correct base class (e.g., `SageServiceProvider`, not `ServiceProvider`)
- Hooks are in `boot()`, not `register()`
- Theme packages installed via `lando theme-composer`, not `lando composer`
- The relevant reference file was read before generating domain-specific code
- `lando acorn view:clear` run after Blade template changes if views appear stale
- `lando pint` run to fix code style

## Failure modes

### Problem: Extending `ServiceProvider` directly

- Cause: Using Laravel's base `ServiceProvider` instead of the Sage-aware one
- Fix: Extend `SageServiceProvider` in all theme service providers

### Problem: Hooks placed in `register()` instead of `boot()`

- Cause: Misunderstanding the container lifecycle
- Fix: Move all `add_action` / `add_filter` calls to `boot()`. The container is not ready during `register()`.

### Problem: Wrong Composer context

- Cause: Running `lando composer require` at project root for a theme dependency, or vice versa
- Fix: Root `composer.json` manages WP core + plugins. Theme `composer.json` manages Acorn, ACF Composer, etc. Use `lando theme-composer` for theme packages.

### Problem: `wp acorn` fails inside Lando

- Cause: Missing `--path=/app/wp` flag
- Fix: Always specify the WordPress path when running `wp acorn` in Lando

### Problem: Using raw ACF API instead of ACF Composer

- Cause: Calling `acf_add_local_field_group()` directly
- Fix: Use `Log1x\AcfComposer\Builder` via ACF Composer classes generated with `acf:block`, `acf:field`, etc.

### Problem: Blade components created in wrong directory

- Cause: Putting component classes in `Composers/` or vice versa
- Fix: Components go in `View/Components/`, composers go in `View/Composers/`

### Problem: Business logic in global PHP files

- Cause: Writing logic directly in `actions.php`, `filters.php`, or `setup.php`
- Fix: Create a `Services/` class, bind it in a provider, and call it from hooks in `boot()`

### Problem: Raw `register_post_type()` or `register_taxonomy()`

- Cause: Not using the declarative approach
- Fix: Use `log1x/poet` via `config/poet.php`. Only use a Service Provider for complex registrations that exceed Poet's capabilities.

### Problem: Manually creating component/block/field files

- Cause: Writing class and view files by hand
- Fix: Always use generators (`make:component`, `acf:block`, `acf:field`). They scaffold both class and view with correct namespace and base class.

### Problem: Tailwind configured via `tailwind.config.js`

- Cause: Using Tailwind v3 patterns
- Fix: Tailwind v4 is CSS-first. Configure via `@theme` directive in CSS files, not a JS config.

### Problem: Mixing root and theme Composer dependencies

- Cause: Installing a theme package at root or a root package in the theme
- Fix: Each `composer.json` is independent. Never cross-install.

## Escalation

- Stop and ask if the project structure does not match the expected layout above
- Stop and ask if the generator fails or produces unexpected output
- Stop and ask if unsure whether logic belongs in a Service Provider vs `actions.php`/`filters.php`
- Stop and ask if the task requires a pattern not covered by any reference file

---

## Canonical Lando Command Reference

See [references/lando-command-reference.md](references/lando-command-reference.md).
