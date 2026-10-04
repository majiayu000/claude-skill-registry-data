---
name: superpowers-sage:block-refactoring
description: >
  Refactor ACF Composer blocks — evolve blocks along 4 axes: rendering model,
  field composition, block variants $styles, InnerBlocks adoption; legacy block
  migration, ACF Composer v2 to v3, block phase classification, atomic vs container,
  block evolution report, get_block_wrapper_attributes, $styles, $innerBlocks,
  refactor without breaking existing content, block refactoring report
user-invocable: true
argument-hint: "<BlockClassName or block-slug>"
---

# Block Refactoring — Evolution of Existing Blocks

Analyze and improve an existing block after its first implementation. Four axes of
evolution: design drift detection, CSS coverage analysis, variation expansion, and
gap/migration detection.

**Announce at start:** "I'm using the block-refactoring skill to evolve the block."

## When to use

- Block shipped in a previous PR and design has evolved since
- CSS bundle includes rules/tokens that are no longer used
- New design tokens exist in `app.css`/`design-tokens.md` that the block could leverage
- Legacy block still uses v1 pattern (`.b-{slug}` class, dual selector, no custom element)
- You suspect implementation diverged from design reference during initial build

## When NOT to use

- **Creating a new block from scratch** → use `/block-scaffolding` instead
- **Project-wide convention audit** → use `/reviewing`
- **Non-block UI component** → Blade components are not ACF blocks

## Input

$ARGUMENTS

Resolve to `{ClassName}` and `{slug}`. If not provided, ask.

---

See [references/evolution-axes.md](references/evolution-axes.md) for the 4 evolution axes.

Refactoring NEVER rebuilds from scratch. For a full re-scaffold, delegate to `/block-scaffolding` as a fallback.

---

## Procedure

### Phase 0 — Resolve block identity and locate files

From the argument, identify:
- `{ClassName}` — e.g. `HeroSection`
- `{slug}` — e.g. `hero-section`
- 5 target files (one may be absent on legacy blocks):
  - `app/Blocks/{ClassName}.php`
  - `resources/views/blocks/{slug}.blade.php`
  - `resources/css/blocks/{slug}.css`
  - `resources/js/blocks/{slug}.js` (may not exist — legacy)
  - `resources/css/editor.css` (check for `@import './blocks/{slug}.css'`)

Read all present files.

### Phase 0b — Shared component inventory

Glob `resources/views/components/*.blade.php` in the target project (if a path is known, otherwise skip this step).

Build a component inventory table:

| Component slug | File | Likely use |
|---|---|---|
| `section-header` | `section-header.blade.php` | `<x-eyebrow>` + `<h2>` pairing |
| `button` | `button.blade.php` | `<a>` or `<button>` with utility classes |
| `card` | `card.blade.php` | Repeated card structure |

Keep this table in context — G9 in Axis 4 will reference it to report concrete component names instead of generic suggestions.

If `resources/views/components/` does not exist or is empty, note "No shared components found" and proceed.

### Phase 1 — Classify current pattern version

Inspect the view file and the CSS file:

| Signal | Version |
|---|---|
| View has `<block-{slug}>` custom element | **v2** |
| View uses `$attributes->merge()` on a `<section class="b-{slug}">` | **v1** |
| CSS scoped to `block-{slug}` tag selector | **v2** |
| CSS scoped to `.b-{slug}` class selector | **v1** |
| CSS has dual selector `&.is-style-*, .is-style-* &` | **v1** |
| CSS has single selector `.is-style-* block-{slug}` | **v2** |
| JS file at `resources/js/blocks/{slug}.js` | **v2** |

Mark the block's current version (`v1` / `v2` / `mixed`) before proceeding.

---

### AXIS 1 — Design drift detection

**Prerequisites:** a design reference must be available. Check in order:
1. MCP design tool with the project's file open (Pencil / Paper / Figma / Stitch)
2. `docs/plans/*/assets/section-{slug}-ref.png` on disk
3. `docs/plans/*/assets/section-{slug}-spec.md` on disk

If none available, report `drift: NOT_VERIFIED` and skip to Axis 2.

**Execution:**
1. Dispatch `visual-verifier` agent with:
   - `url`: current environment's URL for a page rendering the block
   - `selector`: `block-{slug}` (v2) or `.b-{slug}` (v1)
   - `ref`: the reference path found above
   - `spec`: spec file path if available
2. Collect: MATCH | DRIFT | MISSING | FAIL_ARBITRARY_VALUES
3. If DRIFT: capture the exact divergences (typography size, color hex, spacing px) for
   Phase 6 report

For detailed axis procedures (CSS coverage, variation expansion, gap checks G1–G8), see [`references/evolution-axes.md`](references/evolution-axes.md).

#### G9. Component reuse gap

Grep the view for co-occurring `<x-eyebrow` and `<h2` inline — these should use
`<x-section-header>` instead. Also grep for `<a` elements carrying button utility
classes (e.g. `btn-`, `rounded-`, `px-`, `py-`, `font-`) — these should be
`<x-button>`.

Each instance where a component from the Phase 0b inventory exists but is not used: flag as IMPROVEMENT, naming the component (e.g., "use `<x-section-header>` instead of inline `<x-eyebrow>` + `<h2>`").

#### G10. CSS custom property cascade not used

**Detection** — check the view for any of:
- `match($tone)` expressions returning Tailwind class strings
  (e.g. `match($tone) { 'fg' => 'text-fg', 'dark' => 'text-depth-fg' }`)
- Props declared as `tone="fg"` / `tone="dark"` / `variant="*-dark"` encoding
  color context in PHP and passing it to child components
- Hardcoded color utility classes (`text-depth-fg`, `text-identity`, `text-white`)
  applied directly on semantic elements (`h2`, `p`, `span`) instead of via
  inherited CSS variables

Colors must cascade from custom properties in the block's CSS; the view must not
encode color context via conditional logic or hardcoded utilities.
Each instance is CRITICAL.

**When detected, generate corrected CSS for the Phase 6 report:**
1. Run inline component inventory: glob `resources/views/components/*.blade.php`,
   grep each for `var(--)` patterns → build local variable name registry
   (same logic as block-scaffolding Phase 0b; runs inline here, not delegated)
2. Read `design-guide.md` `## Tokens → Colors` to determine background context:
   - If `design-guide.md` exists at `docs/plans/*/components/*/design-guide.md`
     → apply decision table
   - If `design-guide.md` is absent → treat as Ambiguous; generate with
     `/* VERIFY: design-guide.md not found — confirm background context */`
3. Apply decision table:
   | Token found | Background | CSS action |
   |---|---|---|
   | `bg-depth`, `bg-primary`, `bg-dark`, `bg-inverse` | Dark | Override cascade vars with `*-on-dark` equivalents |
   | `bg-identity`, `bg-sage`, `bg-accent` | Identity (brand color bg) | Override cascade vars with `*-on-identity` equivalents (e.g. `var(--color-identity-fg)`) |
   | `bg-bg`, `bg-surface`, `bg-muted`, absent | Light (default) | No override — inherit `:root` defaults |
   | Unrecognized token | Ambiguous | Generate with `/* VERIFY: background context unknown */` |
4. Include generated CSS in Phase 6 report (see report-format.md G10 section template)

#### G11. nl2br on non-textarea fields

For each `nl2br(esc_html($var))` call in the view, trace the variable back to its
ACF field definition in `app/Blocks/{ClassName}.php`. If the field uses `addText()`
(single-line text), `nl2br()` is a no-op at best and misleading at worst. Flag as
IMPROVEMENT — remove `nl2br()` or change the field to `addTextarea()` / `addWysiwyg()`.

---

## Phase 6 — Report and propose

See [references/report-format.md](references/report-format.md) for the refactoring report format.

---

## Phase 7 — Apply approved changes

After user approves proposals, apply in order: CSS removals → variation expansions → gap fixes. Run `lando theme-build && lando flush` to verify.

---

## Phase 8 — Verification

Use Playwright MCP to screenshot at canonical width and verify all variations. Then:

```
git commit -m "refactor(blocks): {slug} — {summary of applied changes}"
```

---

## Anti-drift — don't reintroduce

See `/block-scaffolding` anti-drift table — same rules apply during refactor. Every
proposal in Phase 6 should, after applied, produce code that would pass `/block-scaffolding`
as if the block were being created today.
