---
name: dxt
version: 1.0.0
description: |
  Manage DXPR Theme settings via drush dxt:* commands.
  Configure layout, header, colors, fonts, typography, block design,
  page title, and custom CSS/JS — all from the CLI. Use when asked to
  "change the theme", "update colors", "change color palette",
  "set font size", "configure header", "modify layout",
  "generate palette", "set page layout", or any DXPR Theme
  configuration task. Proactively invoke this skill instead of
  editing Drupal config YAML directly.
  For color palette changes: use dxt:palette:set to set all colors
  in one command, or dxt:config:set color_palette_<key> for individual
  colors. Do NOT try to set the serialized color_palette directly.
---

## Preamble (run first)

```bash
echo "=== DXPR THEME CONTEXT ==="

echo ""
echo "=== AVAILABLE SECTIONS ==="
drush dxt:config:list --sections-only 2>/dev/null || echo "SECTIONS: unavailable"

echo ""
echo "=== PALETTE WITH BOOTSTRAP MAPPING ==="
drush dxt:palette:get 2>/dev/null || echo "PALETTE: unavailable (try dxt:config:list --section=colors)"

echo ""
echo "=== CURRENT FONTS ==="
drush dxt:config:list --section=fonts 2>/dev/null || echo "FONTS: unavailable"

echo ""
echo "=== CURRENT HEADER ==="
drush dxt:config:get header_top_layout 2>/dev/null || echo "HEADER: unavailable"
drush dxt:config:get header_style 2>/dev/null

echo ""
echo "=== CURRENT TYPOGRAPHY ==="
drush dxt:config:get body_font_size 2>/dev/null || echo "TYPOGRAPHY: unavailable"
drush dxt:config:get h1_font_size 2>/dev/null
drush dxt:config:get scale_factor 2>/dev/null
```

**After reading preamble output:**

- Use section list to know which categories of settings exist
- Before changing settings in any section, ALWAYS run `drush dxt:config:list --section=<section> --detail` first to see every setting's valid values, ranges, and current state
- DO NOT guess values — read the schema first
- Use `dxt:config:get <key>` for individual setting details including valid options

## Theme vs Content Responsibility

DXPR Theme (dxt) owns the site's visual baseline: heading weight, text colors, backgrounds, font sizes, spacing. Page content markup (dxb) inherits these defaults automatically. Always configure the theme FIRST to establish the correct baseline, so content markup stays clean and semantic. If headings need to be bold, set `headings_bold=1` here — don't add `fw-bold` to every heading in content.

## Workflow

1. **Discover** — Read preamble output for current state
2. **Introspect** — ALWAYS run `drush dxt:config:list --section=<section> --detail` before modifying settings in that section
3. **Change** — `drush dxt:config:set <key> <value>` (validates and rebuilds CSS)
4. **Bulk change** — `drush dxt:config:import settings.yml` (validates all before applying)
5. **Verify** — `drush dxt:config:get <key>` to confirm

## Commands

### Configuration

```bash
# Get a setting with schema metadata
drush dxt:config:get header_top_layout
drush dxt:config:get body_font_size --theme=my_subtheme

# Set a setting (validates, rebuilds CSS)
drush dxt:config:set header_top_layout centered
drush dxt:config:set body_font_size 16
drush dxt:config:set boxed_layout 0

# List settings
drush dxt:config:list --sections-only
drush dxt:config:list --section=header --detail
drush dxt:config:list --keys-only

# Export/import
drush dxt:config:export --file=/tmp/theme.yml
drush dxt:config:import /tmp/theme.yml
drush dxt:config:import /tmp/theme.yml --dry-run

# Reset to defaults
drush dxt:config:reset --section=typography
drush dxt:config:reset --dry-run
```

### Color Palette

```bash
# Get current palette with Bootstrap class mapping
drush dxt:palette:get

# Set entire palette in one command (all key=#hex pairs)
drush dxt:palette:set base=#6C3CE1 basetext=#ffffff link=#6C3CE1 \
  accent1=#00D4FF accent1text=#0A1628 accent2=#F0F4FF accent2text=#1E293B \
  text=#334155 headings=#0A1628 card=#F0F4FF cardtext=#0A1628 \
  footer=#0A1628 footertext=#CBD5E1 secheader=#0F1D35 secheadertext=#ffffff \
  header=#ffffff headertext=#0A1628 headerside=#0A1628 headersidetext=#F0F4FF \
  pagetitle=#0F1D35 pagetitletext=#ffffff graylight=#94A3B8 \
  graylighter=#E2E8F0 silver=#F8FAFC body=#FFFFFF

# Set individual palette color
drush dxt:config:set color_palette_base "#6C3CE1"
drush dxt:config:set color_palette_accent1 "#00D4FF"

# AI-generated palette (requires Drupal AI module)
drush dxt:generate:palette "Modern tech startup with blue accents"
drush dxt:generate:palette "Warm bakery" --apply
```

**Palette color keys:** base, basetext, link, accent1, accent1text, accent2, accent2text, text, headings, card, cardtext, footer, footertext, secheader, secheadertext, header, headertext, headerside, headersidetext, pagetitle, pagetitletext, graylight, graylighter, silver, body.

### How the Palette Maps to Bootstrap

The DXPR Theme palette overrides Bootstrap's CSS variables. This is how palette keys connect to the Bootstrap classes that content markup (dxb) uses:

**Bootstrap color classes (directly overridden):**

| Palette Key | CSS Variable | Bootstrap Classes | Usage |
|---|---|---|---|
| `base` + `basetext` | `--bs-primary` | `btn-primary`, `bg-primary`, `text-primary`, `border-primary` | Main brand color, primary buttons, primary backgrounds |
| `accent1` + `accent1text` | `--bs-secondary` | `btn-secondary`, `bg-secondary` | Secondary brand color — often the CTA/action button color |
| `silver` | `--bs-light` | `bg-light` | Light background for alternating sections |
| `headings` | `--bs-dark` | `bg-dark`, `text-dark` | Dark color (heading color) |

**Inherited defaults (no class needed in markup):**

| Palette Key | CSS Variable | Effect |
|---|---|---|
| `text` | `--bs-body-color` | All body text inherits this color |
| `headings` | `--bs-heading-color` | h1-h6 inherit this color |
| `body` | `--bs-body-bg` | Page background |
| `link` | `--bs-link-color` | All `<a>` tags inherit this color |
| `accent1` | `--bs-link-hover-color` | Link hover color |
| `graylighter` | `--bs-border-color` | Default border color |

**Theme region colors (applied automatically by DXPR Theme, not via Bootstrap classes):**

| Palette Key | Applied to |
|---|---|
| `header` + `headertext` | Main header/navbar region |
| `secheader` + `secheadertext` | Secondary header region (announcement bar) |
| `footer` + `footertext` | Footer region |
| `pagetitle` + `pagetitletext` | Page title region |

**Key insight for content authors:** `btn-primary` = `base` color, `btn-secondary` = `accent1` color. If the design calls for blue brand buttons AND yellow CTA buttons, set `base=#0072DB` and `accent1=#FFE100`, then use `btn-primary` for blue buttons and `btn-secondary` for yellow CTA buttons. The palette controls what Bootstrap classes look like — never use `btn-warning` to get yellow.

### AI Generation

```bash
# Generate font selections
drush dxt:generate:fonts "Clean editorial style"
drush dxt:generate:fonts "Bold tech branding" --apply
```

### Per-Node Page Layout

```bash
# Get node theme fields
drush dxt:page:get 42

# Set per-node overrides
drush dxt:page:set 42 --layout=fullwidth
drush dxt:page:set 42 --hide-regions=navigation,footer
drush dxt:page:set 42 --content-width=2-3
```

### Subtheme Creation

```bash
drush dxt:subtheme:create my_theme --theme-name="My Theme"
```

### AI Setup

```bash
drush dxt:setup-ai
drush dxt:setup-ai --host=claude
```

<!-- SETTINGS_SCHEMA_START (auto-generated — do not edit manually) -->
## Settings Sections

| Section | Key Examples | Description |
|---|---|---|
| block-design | block_preset, block_card, block_background, ... | Block styling, titles, dividers, regions |
| colors | color_scheme | Color scheme and palette values |
| custom-css | custom_css_site, custom_javascript_site | Sitewide CSS and JavaScript injection |
| fonts | body_font_face, body_font_face_selector, headings_font_face, ... | Font families and CSS selectors |
| header | header_top_layout, header_style, header_top_bg_opacity, ... | Header layout, sticky, colors, mobile, menu styling |
| layout | boxed_layout, sticky_footer, boxed_layout_boxbg, ... | Page layout, grid, backgrounds, full-width regions |
| page-title | page_title_breadcrumbs, page_title_breadcrumbs_align, page_title_breadcrumbs_separator, ... | Page title region, breadcrumbs, background |
| typography | body_line_height, body_font_size, nav_font_size, ... | Font sizes, line heights, scale, dividers |
<!-- SETTINGS_SCHEMA_END -->
