---
name: superpowers-sage:block-scaffolding
description: >
  Scaffold a new ACF Composer block: ACF block, ACF Composer, block registration,
  Gutenberg block, block view, Blade block, InnerBlocks, block.json, block scaffold,
  acf:block, custom block, block category, block icon, block supports, block variants,
  block styles, is-style, create-block, enqueue block, block CSS, block JS, custom element,
  block preview parity — full custom element architecture with scoped CSS and theme variations.
user-invocable: true
argument-hint: "<BlockClassName or block-slug>"
---

# Block Scaffolding — Custom Element Contract per Block

Scaffold a new ACF block with the full custom element architecture: scoped CSS,
theme variations, optional JS lifecycle, selective enqueue, and documentation.

**Announce at start:** "I'm using the block-scaffolding skill to create the block."

## When to use

- **Auto-invoked by `/building`**: after `lando acorn acf:block` produces a new stub
- **Standalone new block**: a block outside of a plan

## When NOT to use

- **Existing block that needs evolution** → use `/block-refactoring` instead.
- **Non-block UI component (Button, Card)** → Blade component, not ACF block.

## Input

$ARGUMENTS

Resolve to `{ClassName}` (PascalCase) and `{slug}` (kebab-case) before proceeding.

---

## Quick Start

```bash
# Generate block stub (PascalCase name required)
bash skills/block-scaffolding/scripts/create-block.sh HeroBlock
# → app/Blocks/HeroBlock.php
# → resources/views/blocks/hero-block.blade.php
```

---

## Hard Prerequisites

**P1. Slug produces a valid custom element tag** — `block-{slug}`. The `block-`
prefix guarantees the required hyphen.

**P2. Design system foundation:**
```
resources/css/design-tokens.css   — must exist
resources/views/components/ui/    — must contain button + heading
```

**P3. BaseCustomElement in theme:**
```
resources/js/core/BaseCustomElement.js   — must exist
```

---

## Operation Modes

| Mode | When | `$styles` | CSS variations |
|---|---|---|---|
| **Full** | Theme switching (light/neutral/dark) | 3 entries | 3 `.is-style-*` selectors |
| **Minimal** | Fixed appearance (footer, nav, ticker) | absent | base tokens only |

---

## Phase 0 — Generate

```bash
lando acorn acf:block {ClassName} --localize
```

Produces:
- `app/Blocks/{ClassName}.php` — controller stub (localization-ready)
- `resources/views/blocks/{slug}.blade.php` — view stub

---

## Phase 0b — Shared component inventory

Before writing the view, build a local registry of available shared components:

1. Glob `resources/views/components/*.blade.php` — list all component files
2. For each component:
   a. Read its `@props` declaration → note prop names + defaults
   b. Grep for `var(--)` patterns → note CSS variable names consumed
3. Build local registry:
   ```
   {
     "section-header": { props: ["eyebrow","title","align"] },
     "eyebrow":        { consumes: ["--eyebrow-color","--decorator-color"] },
     "button":         { consumes: ["--btn-bg","--btn-text"] }
   }
   ```

This registry drives CSS generation in S1 — variable names come from the project,
not from the skill's assumptions.

**Rule:** if the block needs eyebrow + heading markup, use `<x-section-header>` (or
the equivalent shared component) — do NOT emit `<x-eyebrow>` + `<h2>` inline.
If no suitable component exists, use inline markup and note it for future extraction.

---

## Phase 0c — Form detection (conditional)

Detect whether the block embeds an HTML Forms form. Two signals — any match triggers:

1. Plan/argument description mentions: `form`, `formulário`, `contact form`, `contato`, `html forms` (case-insensitive)
2. The planned `fields()` for this block includes an `addPostObject` with `post_type` containing `html-form`

If **triggered**, load the `sage-forms` skill and its references (`blade-form-views.md`, `hf-validation.md`, `traps.md`) before continuing. After Phase 1 S2 (controller written), run the three coordinated scaffolds below. If **not triggered**, skip this phase entirely.

### 0c.1 — Form Blade view (`resources/views/forms/{form-slug}.blade.php`)

Resolve `{form-slug}`:
- If the plan names a target `html-form` post (e.g. "contact form" → `contact`), use that slug.
- Otherwise use `{slug}-form` as placeholder and prepend `{{-- TODO: rename file to match the html-form CPT post_name --}}` at the top.

Write the form view using `<x-html-forms>` + `x-form.*` components, with one `x-form.field` per ACF field declared in S2. Submit button is `<x-button type="submit">`. Do not pass `pattern` attributes; do not use `type="tel"` (use `type="text" inputmode="tel"` for phone fields). See `skills/sage-forms/references/blade-form-views.md` for the full pattern and `references/traps.md` for the rationale.

### 0c.2 — Validation module (`resources/js/modules/hf-validation.js`)

Glob check: if `resources/js/modules/hf-validation.js` exists, **skip** — one module per project, reused across forms. If absent, write the scaffold from `skills/sage-forms/references/hf-validation.md` (the "Full Module Skeleton" section).

### 0c.3 — Block JS patch (`resources/js/blocks/{slug}.js`)

Add an import at the top:

```js
import { initHfValidation } from '../modules/hf-validation';
```

Inside the block's `init()` method, add:

```js
const form = this.querySelector('.hf-form');
if (form) {
  initHfValidation(form, {
    messages: {
      // TODO: configure per form — see skills/sage-forms/references/hf-validation.md
    },
    validators: {
      // TODO: configure per form
    },
  });
}
```

### Phase 0c non-objective

Phase 0c does NOT write validator functions or localized messages — always produces `// TODO: configure per form` stubs. Validator content varies per project and per form; this is deliberate.

---

## Phase 1 — Implement S1–S4

### S1 — `resources/css/blocks/{slug}.css`

Before generating CSS, apply the background context decision table.
Read the component's `design-guide.md` (`## Tokens → Colors` section) if available:

| Token found in design-guide Colors | Background context | CSS action |
|---|---|---|
| `bg-depth`, `bg-primary`, `bg-dark`, `bg-inverse` | Dark | Override cascade vars with `*-on-dark` equivalents |
| `bg-identity`, `bg-sage`, `bg-accent` | Identity (brand color bg) | Override cascade vars with `*-on-identity` equivalents (e.g. `var(--color-identity-fg)`) |
| `bg-bg`, `bg-surface`, `bg-muted`, absent | Light (default) | No override — inherit `:root` defaults |
| Unrecognized token | Ambiguous | Generate with `/* VERIFY: background context unknown */` |

Variable names for the cascade block come from the Phase 0b registry (what each
shared component actually consumes via `var(--)` references).

**Full mode — light section (no override):**

```css
@reference "../app.css";

block-{slug} {
  @apply block overflow-hidden;

  /* cascade — inherited by child components */
  --eyebrow-color:   var(--color-identity);
  --heading-color:   var(--color-fg);
  --body-color:      var(--color-fg);
  --decorator-color: var(--color-identity);
}
```

*(variable names from Phase 0b registry; values from `:root` defaults)*

**Full mode — dark section (`bg-depth` detected in design-guide):**

```css
@reference "../app.css";

block-{slug} {
  @apply block overflow-hidden;

  /* cascade — dark section, override :root defaults; values may differ per component — adjust per design-guide */
  --eyebrow-color:   var(--color-depth-fg);
  --heading-color:   var(--color-depth-fg);
  --body-color:      var(--color-depth-fg);
  --decorator-color: var(--color-depth-fg);
}
```

**Full mode with `$styles` variations (background changes per variation):**

```css
@reference "../app.css";

block-{slug} {
  @apply block overflow-hidden;

  /* cascade — light default */
  --eyebrow-color:   var(--color-identity);
  --heading-color:   var(--color-fg);
  --body-color:      var(--color-fg);
  --decorator-color: var(--color-identity);
}

.is-style-dark block-{slug} {
  --eyebrow-color:   var(--color-depth-fg);
  --heading-color:   var(--color-depth-fg);
  --body-color:      var(--color-depth-fg);
  --decorator-color: var(--color-depth-fg);
}
```

**Minimal mode:** omit `.is-style-*` selectors. Include the token declarations
commented out so the developer has the vocabulary available:

```css
@reference "../app.css";

block-{slug} {
  @apply block overflow-hidden;
  /* --eyebrow-color:   var(--color-identity); */
  /* --heading-color:   var(--color-fg); */
  /* --body-color:      var(--color-fg); */
  /* --decorator-color: var(--color-identity); */
}
```

**CSS rules:**
- `@apply` for all Tailwind utilities (`block`, `overflow-hidden`, `flex`, spacing, etc.)
- CSS custom properties remain native CSS — no `@apply` equivalent exists for cascade variables
- No hardcoded color values — all values reference `@theme` tokens via `var(--)`
- `@reference` not `@import` — grants token access without duplicating the stylesheet
- `.is-style-* block-{slug}` single selector — works in editor and frontend

### S2 — `app/Blocks/{ClassName}.php`

Use template: `assets/block-atomic.php.tpl` (leaf block) or `assets/block-container.php.tpl` (InnerBlocks).

Key rules:
- Always declare `$spacing` and `$supports` — editor controls users expect
- `$styles`: Full mode only — omit entirely for Minimal blocks
- `$styles` format: `['name' => 'dark']` not `['value' => 'dark']` (WP 6.x)
- `assets()` must remain empty — enqueue via `ThemeServiceProvider::boot()`
- `fields()` declares all ACF fields — never use the ACF GUI

See [`references/acf-composer-registration.md`](references/acf-composer-registration.md) for full class structure.
For InnerBlocks containers see [`references/inner-blocks.md`](references/inner-blocks.md).
For `$styles` and variant CSS see [`references/variants.md`](references/variants.md).

### S3 — `resources/js/blocks/{slug}.js`

Always generate, even for static blocks:

```js
import BaseCustomElement from '../core/BaseCustomElement.js';

export default class Block{PascalSlug} extends BaseCustomElement {
  static tagName = 'block-{slug}';

  init() {
    // Block behavior. Empty is valid for static blocks.
  }
}

BaseCustomElement.register(Block{PascalSlug});
```

Rules: class name `Block{PascalSlug}`, `static tagName` matches CSS selector,
`init()` empty = static block, `BaseCustomElement.register()` at bottom.

### S4 — `resources/views/blocks/{slug}.blade.php`

Use template: `assets/block-view.blade.php.tpl`. Key points:

```blade
@unless ($block->preview)
  <section {!! get_block_wrapper_attributes() !!}>
@endunless

<block-{slug} class="flex flex-col">
  {{-- content --}}
</block-{slug}>

@unless ($block->preview)
  </section>
@endunless
```

Rules:
- `@unless ($block->preview)` wraps `<section>` — skipped in editor
- `<block-{slug}>` is the CSS and JS root
- Structural utilities (flex, grid, gap, px) on `<block-{slug}>` or children
- No hardcoded colors, typography classes, or background utilities in the view

For editor vs frontend parity issues see [`references/edit-preview-parity.md`](references/edit-preview-parity.md).
For `block.json` and `editor_script` see [`references/block-json.md`](references/block-json.md).

---

## Phase 2 — Enqueue Guard (`ThemeServiceProvider::boot()`)

Search for `has_block` in `app/Providers/ThemeServiceProvider.php`.

**If pattern EXISTS:** add `'{slug}' => true,` to the `$blocks` array.

**If pattern DOES NOT EXIST:** implement it:

```php
add_action('wp_enqueue_scripts', function () {
    $blocks = [
        '{slug}' => true,
    ];

    foreach (array_keys($blocks) as $slug) {
        if (! has_block("acf/{$slug}")) continue;

        $cssAsset = \Roots\asset("css/blocks/{$slug}.css");
        if ($cssAsset->exists()) {
            wp_enqueue_style("block-{$slug}", $cssAsset->uri(), [], $cssAsset->version());
        }

        $jsAsset = \Roots\asset("js/blocks/{$slug}.js");
        if ($jsAsset->exists()) {
            wp_enqueue_script("block-{$slug}", $jsAsset->uri(), [], $jsAsset->version(), true);
        }
    }
}, 20);
```

---

## Phase 3 — Editor CSS

Add one `@import` per block to `resources/css/editor.css`:

```css
@import './blocks/{slug}.css';
```

---

## Phase 4 — Block README (`docs/blocks/{slug}.md`)

Document: custom element name, ACF fields table, theme variations table (Full mode),
CSS tokens table, and file dependency list (controller, view, CSS, JS, enqueue, editor CSS).

**If Phase 0c triggered**, the README additionally documents:

- Form view path: `resources/views/forms/{form-slug}.blade.php`
- Validation module path: `resources/js/modules/hf-validation.js`
- DOM events handled: `hf-success`, `hf-error`
- Pointer to the `sage-forms` skill for the integration pattern

---

## Phase 5 — Verification

### Build gates:

```bash
lando theme-build   # exit 0; block-{slug}-*.css AND .js must appear in output
lando flush         # clear Acorn/Blade/OPcache
```

### Runtime checks:
1. Screenshot at canonical width from `plan.md`
2. Verify `<link href="*/block-{slug}-*.css">` and `<script>` in DOM
3. Custom element upgraded: `document.querySelector('block-{slug}').constructor !== HTMLElement`
4. Full mode: test each variation via DevTools adding `is-style-neutral` / `is-style-dark`
   to the outer `<section>` and confirm cascade vars (e.g. `--eyebrow-color`, `--heading-color`) resolve correctly
5. `git commit -m "feat(blocks): scaffold {slug}" && git push`

---

## Critical Rules

1. **Always use `lando acorn acf:block` — never create block stubs manually.** The generator sets correct namespaces, registration hooks, and file paths.
2. **View is Blade** (`resources/views/blocks/{slug}.blade.php`). Never plain PHP.
3. **Fields via `fields()` method** — never the ACF GUI. GUI fields are lost on composer install.
4. **`get_block_wrapper_attributes()` on `<section>`** — provides accessibility, spacing, alignment, and variation classes.
5. **`assets()` stays empty** — CSS/JS enqueue belongs in `ThemeServiceProvider::boot()`.
6. **`@reference` not `@import` in block CSS** — avoids duplicating the full stylesheet.
7. **`@apply block overflow-hidden` on the custom element** — custom elements default to `inline`; `overflow-hidden` prevents bleed.
8. **Commit before declaring done** — git state is part of the Definition of Done.

---

## Anti-Drift Table

| Wrong | Correct |
|---|---|
| `<section class="b-{slug}">` + `$attributes->merge()` | `@unless preview <section {!! get_block_wrapper_attributes() !!}>` + `<block-{slug}>` |
| `.b-{slug} { ... }` | `block-{slug} { ... }` tag selector |
| `&.is-style-neutral, .is-style-neutral &` | `.is-style-neutral block-{slug}` |
| No `@apply block` on custom element | `@apply block overflow-hidden` always — custom elements default to `inline` |
| `<hero>` (no hyphen) | `<block-hero>` |
| `assets()` with enqueue | `assets()` empty — enqueue in ThemeServiceProvider |
| `@import "../app.css"` | `@reference "../app.css"` |
| `['value' => 'dark']` in `$styles` | `['name' => 'dark']` |
| Skip `$spacing` / `$supports` | Always declare both |
| `acf:block` without `--localize` | `lando acorn acf:block {Name} --localize` |
| Skip JS for static block | Generate stub with empty `init()` |
| Done without git commit | `git commit` + `git push` required |

---

## Verification

- [ ] `lando theme-build` exits 0
- [ ] Block CSS and JS files present in build output
- [ ] `<link>` and `<script>` for block assets in frontend `<head>`
- [ ] Custom element upgraded (not `HTMLElement`)
- [ ] Full mode: all three variations render correctly
- [ ] No ACF warnings in `lando wp --info` output
- [ ] `git commit` made with `feat(blocks): scaffold {slug}`

## Failure modes

### Build fails — block CSS not emitted

**Cause:** Block CSS not imported in `editor.css` or Vite entrypoint.
**Fix:** Add `@import './blocks/{slug}.css'` to `resources/css/editor.css`.

### Custom element not upgrading

**Cause:** JS not enqueued, or `BaseCustomElement.register()` missing.
**Fix:** Verify `ThemeServiceProvider::boot()` includes the slug and the JS file exists.

### Variation colors wrong on frontend

**Cause:** `<section {!! $attributes !!}>` missing — `is-style-*` class not in DOM.
**Fix:** Restore `@unless ($block->preview)` wrapper with `get_block_wrapper_attributes()`.

### ACF fields not saving

**Cause:** Fields defined in `fields()` but block registered before ACF Composer boots.
**Fix:** Ensure the block class is auto-discovered by ACF Composer (check `config/acf.php`).

For all edit/preview parity issues see [`references/edit-preview-parity.md`](references/edit-preview-parity.md).
