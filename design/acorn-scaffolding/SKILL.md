---
name: acorn-scaffolding
description: Use when generating a new artifact in an Acorn project - a Gutenberg block (ACF Composer acf:block, InnerBlocks, $styles, or a native block.json block via make:block), a post type or taxonomy (Poet config/poet.php, config/post-types.php), an ACF field group, partial or options page (acf:field, acf:options), a provider, View Composer, Blade component or command (make:provider, make:composer, make:component). For changing existing Acorn code use acorn-stack; for ACF hooks use acf-native; for block CSS and JS use tailwind-vite-assets.
---

# Scaffolding in Acorn projects

Generate first, then edit. Every generator below resolves paths and the namespace from Acorn's base path and the PSR-4 entry for `app/`, so it writes into the theme, the mu-plugin or the project root depending on the profile. Read the profile, namespace and installed packages from the session context.

Runner placeholders (`{{runner.wp}}`, `{{runner.acorn}}`, `{{runner.composer}}`, `{{runner.node}}`, `{{runner.test}}`, `{{runner.cache}}`) come from the session context. On Lando they default to `lando wp`, `lando wp acorn`, `lando composer`, the project's Node tooling command and its cache-clear tooling. Never run WP-CLI, Composer, PHP or Node on the host.

## When to use

- "Create a block", "new ACF block", "scaffold a block", "register a block", "add InnerBlocks", "add a style variant".
- "Add a custom post type / taxonomy", "register a CPT".
- "New field group / options page / partial".
- "New service provider / composer / component / console command".

Not for: editing existing classes (`acorn-stack`), ACF save/validation behaviour (`acf-native`), Livewire components (`acorn-livewire`), routes and controllers (`acorn-routes-api`), asset pipelines (`tailwind-vite-assets`).

## Inputs required

1. Profile, Acorn base path, namespace (session context).
2. Which generators exist: `{{runner.acorn}} list` (look for `acf:*`, `make:block`, project-specific `make:*` or prefixed commands). Projects often ship custom stubs in `<base>/stubs/`; generators pick them up automatically.
3. Installed packages in the Composer project that owns Acorn: `{{runner.composer}} show --working-dir=<base path> | grep -E 'acf-composer|poet|acorn-post-types|livewire'`.
4. Names: `{ClassName}` in PascalCase (`PricingTeaser`), `{slug}` in kebab-case (`pricing-teaser`).

### What to generate, per profile

| Artifact | `sage-theme` | `acorn-mu-plugin` | `radicle-app` |
|---|---|---|---|
| Block | ACF Composer `acf:block` when `log1x/acf-composer` is installed | Same; projects often extend a base block class through custom stubs | Native block: PHP `register_block_type()` with a Blade `render_callback`, editor UI in JSX; use the project's `make:block` command when `{{runner.acorn}} list` shows it |
| CPT / taxonomy | Poet: entries in `config/poet.php` | Poet entries, or one class per CPT if the project has that convention (and its own generator) | `roots/acorn-post-types`: entries in `config/post-types.php` |
| Field group, partial, options page | `acf:field`, `acf:partial`, `acf:options` | Same | Not available by default (no ACF): use block attributes or `register_post_meta()` |
| Service provider | `make:provider`, then add it to `withProviders()` in `functions.php` | `make:provider`, then add it to the boot code / configurator class | `make:provider`, then add it to `composer.json` `extra.acorn.providers` and run `package:discover` |
| View Composer | `make:composer` (auto-discovered) | Same | Same |
| Blade component | `make:component` | Same | Same |
| Console command | `make:command`, then register it in a provider | Same | Same |

## Procedure

Commands: write every command with the runner value from the session context filled in (for example `lando wp acorn optimize:clear`), never a bare `wp`/`composer`/`php`/`npm`, never the placeholder, never "prefix with lando if you use it". Commands that run in CI or a deploy script go in a separate block labelled with where they run.

### 1) Reuse check (always)

Search before creating: existing blocks in `app/Blocks/` (or wherever the project registers them), components in `resources/views/components/`, partials in `app/Fields/Partials/`, CPTs in `config/poet.php`, `config/post-types.php` or the CPT class folder. A new field, a `$styles` variant or a component prop is cheaper than a new block.

### 2) ACF Composer block (`sage-theme`, `acorn-mu-plugin`)

1. `{{runner.acorn}} acf:block {ClassName}` once per block (add `--localize` for translatable name/description). It prompts for description, category, post types and supports; without a TTY pass `--no-interaction` and fill those properties in the class afterwards. The generator writes the class and view in the app's namespace (`ns` in the session context; confirm it in the generated file). Then edit the generated files: show the properties and methods you change as a diff, not a hand-written replacement of the whole class.
2. Class `app/Blocks/{ClassName}.php`: set `$name`, explicit `$slug`, `$description`, `$category`, `$icon`, `$keywords`, `$post_types`, `$supports`, `$spacing`, `$example`, and `$styles` only when there are visual variants. Fields in `fields()` with `Builder::make($this->slug)`; data for the view in `with()`, shaped in small protected methods you can unit test. Reference: [references/acf-composer-blocks.md](references/acf-composer-blocks.md).
3. View `resources/views/blocks/{slug}.blade.php`: one root element that prints `{{ $attributes }}` (block-support classes, `is-style-*`, anchor, spacing). In the editor preview `$attributes` is empty and WordPress's wrapper carries those classes: [references/variants-and-parity.md](references/variants-and-parity.md).
4. Container blocks: `<InnerBlocks />` in the view plus `'jsx' => true` in `$supports`; `$template` format and locking in [references/inner-blocks.md](references/inner-blocks.md).
5. Assets: keep `assets()` empty unless you have read the rule below; load block CSS/JS the way the project already does (see `tailwind-vite-assets`).
6. Rebuild the ACF Composer manifest: `{{runner.acorn}} acf:cache` (or `{{runner.cache}}`). Once a manifest exists, class property and `fields()` edits are ignored until it is rebuilt: [references/block-json-manifest.md](references/block-json-manifest.md).

`assets()` rule (ACF Composer 3.4.6): in wp-admin it is called on `enqueue_block_assets` for **every** registered block; on the front end it is attached to `enqueue_block_assets` while the block renders, which only works when blocks render before `wp_head()` (block themes). In Blade/classic layouts that action has already fired, so front-end enqueues from `assets()` never run. Use a `wp_enqueue_scripts` callback with `has_block('acf/{slug}')`, `block.json` style handles, or the project's asset manager.

### 3) Native block (`radicle-app`, or any profile without ACF Composer)

Run the project's generator if it exists (`{{runner.acorn}} make:block {Name}`), otherwise create the three parts by hand: a PHP registration with `register_block_type('<namespace>/{slug}', [... 'render_callback' => …])` in a provider's `init` hook, a Blade view that the callback renders with `view('blocks.{slug}', …)->render()`, and an editor script (JSX) built by the project's Vite config. Attributes replace ACF fields. Reference: [references/native-blocks.md](references/native-blocks.md).

### 4) CPT or taxonomy

Follow the profile's registry (table above); never call `register_post_type()` from a random file when the project has a registry. Poet and acorn-post-types both take Extended CPTs arguments (`labels`/`names`, `admin_cols`, `admin_filters`, `show_in_rest`…). Set `show_in_rest => true` for anything edited in the block editor. Reference: [references/post-types.md](references/post-types.md).

After adding: `{{runner.acorn}} optimize:clear && {{runner.acorn}} optimize` (config is cached), then `{{runner.wp}} rewrite flush`.

### 5) ACF field group, partial, options page

`{{runner.acorn}} acf:field {Name}`, `acf:partial {Name}`, `acf:options {Name}` (`Name/Sub` creates subfolders). Location rules, partials and the `setLocation()` trap: [references/acf-fields.md](references/acf-fields.md). Validation, required logic and save hooks belong to `acf-native`.

### 6) Provider, composer, component, command

```bash
{{runner.acorn}} make:provider ExampleServiceProvider    # then register it (profile table)
{{runner.acorn}} make:composer SingleCaseStudy           # set protected static $views
{{runner.acorn}} make:component PricingBadge             # --view for an anonymous component
{{runner.acorn}} make:command SyncPrices                  # then $this->commands([...]) in a provider
```

Check every generated file: namespace matches the session context, base class is right (`Illuminate\Support\ServiceProvider`, `Roots\Acorn\View\Composer`, `Illuminate\View\Component`), `declare(strict_types=1);` if the surrounding code uses it. Lifecycle rules for providers: `acorn-stack`.

## Verification

```bash
{{runner.cache}}                         # or: {{runner.acorn}} optimize:clear && {{runner.acorn}} optimize
{{runner.acorn}} list                    # new command present
{{runner.wp}} eval 'var_dump(WP_Block_Type_Registry::get_instance()->is_registered("acf/pricing-teaser"));'
{{runner.wp}} eval 'var_dump(post_type_exists("case-study"), taxonomy_exists("industry"));'
{{runner.test}}
```

Then in a browser: insert the block on a draft, fill the fields, switch every style, save, reload the editor, and compare with the front-end preview. For CPTs, open the admin list and a single URL. Report what you checked; committing is the user's call.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Block missing from the inserter | Empty `$name` (compose returns early), class outside a discovered folder, `$post_types` excludes this post type, or a stale manifest | Fix the class; `{{runner.acorn}} acf:cache` |
| Class property edits (styles, supports, icon) ignored | Block registered from the generated `block.json` | `{{runner.acorn}} acf:cache` |
| Field edits ignored | Field group served from the ACF Composer manifest | `{{runner.acorn}} acf:cache` |
| `Block type [acf/x] is already registered` | Two classes share a slug, or a stale manifest after a branch switch | Unique `$slug`; rebuild the manifest |
| Field group key `group_d41d8cd9…` / fields not attached | `$fields = Builder::make(...)->setLocation(...)` returns a `LocationBuilder` | Keep `$fields` as the builder; call `setLocation()` on its own line |
| Variant colours apply only in the editor or only on the front end | Selector matches only one of the two places the `is-style-*` class lands | Use `.is-style-x &, &.is-style-x` on the root |
| Literal `<InnerBlocks` in front-end HTML | Tag not self-closed (`/>`) or `jsx` support missing | Self-close the tag; `'jsx' => true` |
| Default inner blocks wrong | `$template` written as `[['core/heading', [...]]]` | Use `['core/heading' => [...]]` or `[['core/heading' => [...]]]` |
| Front-end block CSS never loads | Enqueued from `assets()` in a classic/Blade layout | Enqueue on `wp_enqueue_scripts` with `has_block()` or via the asset manager |
| Provider generated but never runs | Not added to the profile's provider list | Register it (profile table) |
| CPT 404 on single URLs | Rewrite rules not flushed | `{{runner.wp}} rewrite flush` |

## Escalation

Stop and ask when: a generator writes outside the expected base path; the project has its own generator or stub that contradicts this skill (follow the project, but confirm); a slug or rewrite of an existing block or CPT would change (stored content and URLs break); a new block category or a new provider ordering is needed; Radicle has no `make:block` and no existing native block to copy from.

<!-- verified:
log1x/acf-composer 3.4.6 src/Console/BlockMakeCommand.php:18-20,60-100,157-161 — acf:block {name*} --localize --force, prompts, stub resolution;
src/Console/MakeCommand.php:282-289 — custom stubs from <base>/stubs/acf-composer;
src/Block.php:585-608 — compose(): blank name returns null, slug from name, register from block.json when it exists;
src/Block.php:754-765 — jsonPath under the manifest dir; src/Block.php:461-468 — getHtmlAttributes() empty in preview;
src/Block.php:778-805 — front-end assets() attached to enqueue_block_assets during render; src/AcfComposer.php:194-208 — admin calls assets() for every block;
src/Block.php:364-387 — $styles normalisation; src/Block.php:559-579 — $template map/list-of-maps format, innerBlocks key;
src/Composer.php:109-117 — fields read from manifest; stoutlogic/acf-builder src/FieldsBuilder.php:721-730 — setLocation returns LocationBuilder;
wp/wp-includes/default-filters.php:615 + script-loader.php:2527 — enqueue_block_assets fires inside wp_enqueue_scripts; template-canvas.php:10-17 — block themes render before wp_head;
advanced-custom-fields-pro 6.8.10 pro/blocks.php:1227-1237 — InnerBlocks placeholder regex needs `/>`;
log1x/poet 2.1.0 src/Poet.php:68-77 — registers on init priority 4 (poet.hookPriority);
roots/acorn-post-types 1.0.0 src/AcornPostTypesServiceProvider.php:38-40 — registers on init priority 100; src/AcornPostTypes.php:46-71 — post_types / taxonomies keys
-->
