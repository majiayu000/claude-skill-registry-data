---
name: bricks
description: Author Bricks Builder (WordPress) layouts, templates, and full designs as paste-ready JSON. Use for any Bricks task — sections, pages, headers/footers, query loops, ACF/dynamic data, faceted filters, conditions, interactions/animations, popups, WooCommerce templates, custom elements, or hooks. Verified against Bricks 2.3.6 source.
---

# Bricks Builder JSON Authoring

Generate complete Bricks designs as JSON that pastes or imports cleanly on the first try.

## Default Deliverable

Produce an actual `.json` file in the workspace (not inline JSON) unless the user asks otherwise. Use the project's folder convention if one exists; otherwise `bricks-json/{type}-{slug}.json`. In the final response state: the file path, which JSON format you used, and the validation checks performed.

## Workflow

0. **Clarify inputs first** — settle two things *before* writing JSON:
   - **rem base** — confirm what `1rem` equals on the target site (1rem = ? px). Ask the user; default to **16px** if unspecified (a `html { font-size: 62.5% }` reset makes it 10px). All `rem`/`clamp()` math and any px→rem conversion from a reference depends on this. → [rem base](references/style-settings.md#root-font-size-rem-base)
   - **reference URL** — if the user provides one (or names asset URLs), fetch it and reference its images/video/SVG/icons by absolute URL. → [references/external-assets.md](references/external-assets.md)
1. **Pick the format** — clipboard paste vs template import vs programmatic insert → [references/json-formats.md](references/json-formats.md)
2. **Plan structure** — semantic section → container → blocks tree; pick elements from the catalog → [references/elements.md](references/elements.md)
3. **Style with settings** — every `_` style key and its exact value shape → [references/style-settings.md](references/style-settings.md)
4. **Wire data** — dynamic tags, query loops, filters as needed (see routing table)
5. **Validate** — checklist below, then deliver

## Format Quick Reference

**Clipboard (paste into builder)** — the default for sections and page content:

```json
{
  "content": [ /* flat array of element nodes */ ],
  "source": "bricksCopiedElements",
  "sourceUrl": "https://example.com",
  "version": "2.3.6",
  "globalClasses": [ /* full class objects referenced by _cssGlobalClasses */ ],
  "globalElements": []
}
```

**Element node** (every entry in `content`):

```json
{
  "id": "abc123",
  "name": "heading",
  "parent": "xyz789",
  "children": [],
  "settings": {},
  "label": "Optional structure-panel label"
}
```

- `id`: unique 6-char alphanumeric. `parent`: parent's id, or `0` for root elements.
- The array is **flat** — hierarchy lives entirely in `parent` + `children` (ids must cross-reference exactly).
- Root elements are usually `section`; never nest a `section` inside anything.

## Task Routing

| Task | Reference |
|------|-----------|
| Format selection, clipboard/template/meta storage, programmatic insert | [references/json-formats.md](references/json-formats.md) |
| Element catalog, per-element settings, nestables | [references/elements.md](references/elements.md) |
| Style keys, value shapes (color/typography/border/shadow/gradient/transform), responsive + hover grammar | [references/style-settings.md](references/style-settings.md) |
| Section/grid/flex recipes, cards, overlays, sticky, full designs | [references/layout-recipes.md](references/layout-recipes.md) |
| Dynamic data tags `{post_title}`, args, `{echo:}` | [references/dynamic-data.md](references/dynamic-data.md) |
| ACF (incl. repeaters, groups, flexible content), Meta Box, JetEngine, Pods, CMB2 | [references/acf-providers.md](references/acf-providers.md) |
| Query loops (`hasLoop` + `query`), post/term/user queries | [references/query-loops.md](references/query-loops.md) |
| Faceted filters, AJAX pagination, load more, infinite scroll, live search | [references/query-filters.md](references/query-filters.md) |
| Show/hide conditions (`_conditions`) | [references/conditions.md](references/conditions.md) |
| Interactions, animations, scroll triggers (`_interactions`) | [references/interactions.md](references/interactions.md) |
| Popups (templates, triggers, limits, AJAX) | [references/popups.md](references/popups.md) |
| Template types, conditions, import/export, header/footer/archive/404 | [references/templates.md](references/templates.md) |
| Components, global classes, global variables, color palette | [references/components-classes.md](references/components-classes.md) |
| Theme styles, breakpoints, CSS generation order | [references/theme-styles.md](references/theme-styles.md) |
| Form element, actions, validation | [references/forms.md](references/forms.md) |
| WooCommerce templates and elements | [references/woocommerce.md](references/woocommerce.md) |
| PHP: custom elements with controls | [references/custom-elements.md](references/custom-elements.md) |
| PHP: filters and actions | [references/hooks.md](references/hooks.md) |
| External assets from a reference URL (any image/video/SVG/icon, hotlink vs re-host) | [references/external-assets.md](references/external-assets.md) |
| Asset loading, builder permissions | [references/assets-permissions.md](references/assets-permissions.md) |

Ready-to-paste examples (hero, grids, ACF loops, filtered archive, header/footer, popup…): [patterns/](patterns/) — see [patterns/INDEX.md](patterns/INDEX.md).

## Non-Negotiable Rules

1. **Flat tree integrity** — every `children` id exists as a node whose `parent` points back. No orphans, no duplicates.
2. **Verified value shapes only** — colors are objects (`{"hex": "#222"}` or `{"raw": "var(--x)"}`), typography keys are CSS property names (`"font-size"`, not `fontSize`), box-shadow offsets nest under `values`, gradients use `colors: [{color, stop}]`. When unsure, check style-settings.md — do not guess shapes.
3. **Responsive grammar** — `setting:breakpoint:pseudo` with colons: `_padding:tablet_portrait`, `_background:hover`, `_margin:mobile_portrait:hover`. Default breakpoint keys: `tablet_portrait` (991), `mobile_landscape` (767), `mobile_portrait` (478). Desktop is the bare key.
4. **Units are strings** — `"3rem"`, `"100%"`, `"24px"`. Bare numbers get `px` appended by Bricks.
5. **Spacing scale discipline** — pick a scale (or the site's global variables) and stick to it across the design.
6. **Real structure, no filler** — semantic `tag` settings on sections/blocks (`header`, `nav`, `article`, `aside`, `footer`), one `h1` per page, descending heading levels.
7. **Global classes ride along** — any id listed in an element's `_cssGlobalClasses` must have its full class object in the top-level `globalClasses` array.
8. **Don't invent settings keys** — only keys documented in the references or found in the Bricks source. Unknown keys are silently ignored and waste the user's trust.
9. **Confirm the rem base before using rem** — never assume `1rem = 16px` silently. Ask the user; default to 16px only when they don't answer. Convert any px values lifted from a reference using the confirmed base.
10. **Reference external assets by absolute `url`, never `id`** — when a reference URL or asset URLs are given, resolve every asset to an absolute URL and reference it via the media control's `url`/`external` (attachment `id`s don't resolve cross-site). Respect licensing — don't hotlink copyrighted/brand assets into production. → [references/external-assets.md](references/external-assets.md)

## Validation Checklist (run before delivering)

- [ ] JSON parses (`python3 -m json.tool file.json` or equivalent)
- [ ] Every `parent`/`children` reference resolves; ids unique, 6-char alphanumeric
- [ ] `source: "bricksCopiedElements"` + `version` present (clipboard format)
- [ ] Every `_cssGlobalClasses` id has a matching object in `globalClasses`
- [ ] Value shapes match style-settings.md (spot-check colors, typography, spacing)
- [ ] Responsive keys use valid breakpoint names
- [ ] Query loops: `hasLoop: true` + `query.objectType` present; filters point at a real query element id via `filterQueryId`
- [ ] Dynamic data tags exist for the stated field provider (e.g. `{acf_*}` matches the user's field names)
