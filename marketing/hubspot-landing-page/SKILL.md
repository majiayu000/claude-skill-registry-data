---
name: hubspot-landing-page
version: 1.1.0
description: "Build HubSpot landing page templates for the Design Manager. Use when the user wants to create, edit, or troubleshoot HubSpot landing page templates. Also use when the user mentions 'HubSpot landing page,' 'landing page template,' 'HubL template,' 'Design Manager,' or 'HubSpot CMS.' For CTA buttons, see hubspot-cta. For page conversion optimization, see page-cro."
---

# HubSpot Landing Page Templates

You are an expert HubSpot CMS developer creating coded landing page templates for upload to HubSpot's Design Manager. Every template must use HubL templating and apply the brand system. Templates can use either a **fixed layout** (default for the company — HTML structure with inline HubL fields) or **drag-and-drop** (`{% dnd_area %}`) architecture depending on the use case.

**Pair with `web-design` for craft layer.** This skill covers HubSpot template *mechanics* — HubL syntax, Design Manager, module fields, form renderer quirks, `hsfc-*` class overrides. For the design craft on top of the template — hover/focus/active states, responsive reflow, motion, accessibility, component composition, and [Company] anti-patterns — load `web-design` alongside this skill. Any page ready to ship should pass the `web-design` polish workflow before deploy.

## Critical Facts About the [Company] Setup

**The company blog does NOT live on HubSpot.** It is hosted on the main Next.js site at `[your-site]/blog`. HubSpot's built-in `blog_recent_posts()`, `blog_post_listing` module, and `related_blog_posts` HubL functions will all return empty on any HubSpot landing page because the HubSpot portal (go.[your-site]) has no blogs configured. **Do not use these functions** in [Company] HubSpot templates — verify blog location before writing blog-integration code.

**RSS feed location:** `https://[your-site]/feed.xml` (RSS 2.0, content-type `application/rss+xml`, 50 items). Use this for any "latest posts" functionality.

**Known feed limitations:**
- **No CORS headers** — browser-side `fetch()` from `go.[your-site]` → `[your-site]/feed.xml` is blocked. Must be proxied server-side (e.g., via a HubSpot CMS serverless function) or fetched at build time.
- **No image fields** — the feed has `<title>`, `<link>`, `<pubDate>`, `<description>`, `<author>`, `<category>` per item, but no `<enclosure>`, `<media:content>`, or `<itunes:image>`. For card layouts that need hero images, either scrape the post's `og:image` server-side or use text-only cards.

**Patterns for displaying recent blog posts on a HubSpot page:**
1. **Manually curated editable HubL fields** — 3 slots with image/title/date/URL, updated via page editor when new posts publish. Simple, reliable, no dependencies. Use this for one-off pages where auto-updates aren't critical.
2. **HubSpot CMS serverless function proxy** — server-side fetch of `[your-site]/feed.xml`, parse XML, optionally enrich with og:image scraping. Use `mcp__HubSpotDev__create-cms-function`. Auto-updates. Use this for pages that need to stay fresh without manual intervention.
3. **Dev team adds CORS header to feed.xml** — then client-side fetch becomes viable. Longer-term fix, depends on Next.js team.

## Before Building

**Always read these first:**
1. `/brain/brand-guide/brand-guide.md` — colors, typography, spacing, brand system
2. This skill file — HubSpot Design Manager constraints and template architecture

**If the landing page includes product claims or copy:**
Read `/brain/truth.md` and `/brain/positioning-and-messaging.md` to ensure accuracy. Never invent product facts.

Gather this context (ask if not provided):

### 1. Page Purpose
- What is this landing page for? (product launch, event registration, webinar signup, demo request, content download, waitlist, campaign landing page, other)
- What is the primary conversion goal? (form fill, CTA click, demo booking)

### 2. Content & Sections
- What sections are needed? (hero, features, social proof, form, CTA, FAQ, etc.)
- Any specific content to include? (headlines, copy, images, testimonials, logos)
- How many CTAs? What action(s)?

### 3. Template Flexibility
- Should this be a **drag-and-drop template** (`{% dnd_area %}` with reorderable sections) or a **fixed layout** (coded structure with HubL editable fields)?
- Does the marketer need to add/remove/reorder sections? → Use drag-and-drop
- Is the page structure locked down and only content changes? → Use fixed layout
- Default to **fixed layout** for structured pages (webinars, events, product launches) where design consistency matters more than editor flexibility

---

## HubSpot Design Manager: Template Architecture

### Template Annotations

Every coded template file must start with template annotations:

```html
<!--
  templateType: page
  isAvailableForNewContent: true
  label: [Company] Landing Page - [Variant Name]
  screenshotPath: ../images/template-previews/[name].png
-->
```

- `templateType: page` — used for both website pages and landing pages
- `isAvailableForNewContent: true` — makes the template selectable when creating new pages
- `label` — display name in the template picker
- `screenshotPath` — optional preview thumbnail

### Required HubL Includes

Every page template must include these in the `<head>` and before `</body>`:

```html
<head>
  {{ standard_header_includes }}
  <!-- Your styles and meta tags go here -->
</head>
<body>
  <!-- Page content -->
  {{ standard_footer_includes }}
</body>
```

- `standard_header_includes` — injects HubSpot tracking, stylesheets, and required meta tags
- `standard_footer_includes` — injects HubSpot tracking code, analytics, and required scripts

**Never put `{% %}` HubL syntax inside HTML comments.** HubSpot's linter parses HubL tags as real tags even inside `<!-- -->`, causing cascading false errors (missing `standard_header_includes`, broken `dnd_area`). Keep developer notes in skill files or use plain text descriptions in comments.

---

## Drag-and-Drop Template System

HubSpot uses a **12-column responsive grid** for drag-and-drop templates. The hierarchy is:

```
dnd_area
  └── dnd_section (full-width row)
        └── dnd_column (grid columns, width 1-12)
              └── dnd_row (nested rows within columns)
                    └── dnd_module (content modules)
```

### dnd_area — Editable Container

Wraps the entire editable region. Content editors can add, remove, and reorder sections within this area.

```jinja
{% dnd_area "main_content" label="Main Content", class="body-container" %}
  {# sections go here #}
{% end_dnd_area %}
```

**Parameters:**
- `label` (String) — sidebar label in the editor
- `class` (String) — CSS class on the wrapping div

### dnd_section — Full-Width Row

Top-level horizontal band. Each section spans the full page width.

```jinja
{% dnd_section
  background_color="#111111",
  max_width=1080,
  padding={
    "top": 64,
    "bottom": 64,
    "left": 32,
    "right": 32
  }
%}
  {# columns go here #}
{% end_dnd_section %}
```

**Parameters:**
- `background_color` (String/Dict) — hex, rgb, or rgba. e.g. `"#111111"` or `{r: 17, g: 17, b: 17, a: 1}`
- `background_image` (Dict) — `{"backgroundPosition": "MIDDLE_CENTER", "backgroundSize": "cover", "imageUrl": "..."}`
- `background_linear_gradient` (Dict) — `{"direction": "to right", "colors": ["#111111", "#EEEEEE"]}` (placeholder values — use the brand gradient colors from `brain/brand-guide/brand-guide.md`)
- `max_width` (Number) — content max width in pixels
- `margin` (Dict) — `{"top": 0, "bottom": 0}`
- `padding` (Dict) — `{"top": 64, "bottom": 64, "left": 32, "right": 32}`
- `vertical_alignment` (String) — `TOP`, `MIDDLE`, or `BOTTOM`
- `full_width` (Boolean) — whether the section stretches full viewport width

**Constraint:** Only ONE background parameter per section (color, image, OR gradient — not combined).

### dnd_column — Grid Column

Vertical divisions within a section. Uses the 12-column grid.

```jinja
{% dnd_column
  offset=0,
  width=6,
  background_color="#222222",
  padding={"top": 32, "bottom": 32, "left": 40, "right": 40}
%}
  {# rows or modules go here #}
{% end_dnd_column %}
```

**Parameters:**
- `offset` (Number) — starting grid position (0-11)
- `width` (Number) — column span (1-12)
- `background_color`, `background_image`, `background_linear_gradient` — same as section
- `margin`, `padding` (Dict) — spacing
- `vertical_alignment` (String) — `TOP`, `MIDDLE`, `BOTTOM`

### dnd_row — Nested Row

Creates a nested 12-column grid within a column.

```jinja
{% dnd_row %}
  {# nested columns and modules #}
{% end_dnd_row %}
```

**Parameters:** Same background, margin, padding, max_width, vertical_alignment as section.

### dnd_module — Content Module

Places a HubSpot module (default or custom) into the layout.

```jinja
{% dnd_module path="@hubspot/rich_text", offset=0, width=12 %}
  {% module_attribute "html" %}
    <h1>Your Heading Here</h1>
  {% end_module_attribute %}
{% end_dnd_module %}
```

**Parameters:**
- `path` (String) — module path. Default modules use `@hubspot/` prefix
- `offset` (Number) — grid position
- `width` (Number) — column span
- `horizontal_alignment` (String) — `LEFT`, `CENTER`, `RIGHT`

---

## Default Modules Reference

Use these built-in HubSpot modules in your templates:

| Module | Path | Use For |
|--------|------|---------|
| Rich Text | `@hubspot/rich_text` | Headlines, body copy, formatted content |
| Header | `@hubspot/header` | H1-H6 headings |
| Image | `@hubspot/linked_image` | Images with optional links |
| Button | `@hubspot/button` | CTA buttons |
| Form | `@hubspot/form` | HubSpot form embeds |
| Call-to-Action | `@hubspot/cta` | HubSpot CTA widgets |
| Divider | `@hubspot/divider` | Horizontal line separators |
| Spacer | `@hubspot/horizontal_spacer` | Vertical spacing |
| Icon | `@hubspot/icon` | Font Awesome icons |
| Logo | `@hubspot/logo` | Company logo |
| Logo Grid | `@hubspot/logo_grid` | Customer/partner logo grids |
| Menu | `@hubspot/menu` | Navigation menus |
| Video | `@hubspot/video` | Video embeds |
| Image Gallery | `@hubspot/gallery` | Image carousels/sliders |
| Meetings | `@hubspot/meetings` | Meeting scheduling embeds |

### Module Attribute Override

Override default module content using `module_attribute`:

```jinja
{% dnd_module path="@hubspot/rich_text" %}
  {% module_attribute "html" %}
    <h1 style="color: var(--text);">Hero Headline</h1>
    <p style="color: var(--text-muted);">Supporting subheadline copy goes here.</p>
  {% end_module_attribute %}
{% end_dnd_module %}
```

### HubL Editable Fields

For content that marketers should be able to edit without touching code:

```jinja
{# Editable text field #}
{% text "page_title" label="Page Title", value="Default Headline" %}

{# Editable rich text #}
{% rich_text "body_content" label="Body Content", html="<p>Default content</p>" %}

{# Editable image #}
{% image "hero_image" label="Hero Image", src="https://example.com/default.jpg", alt="Description" %}

{# Editable boolean #}
{% boolean "show_form" label="Show Form Section", value=true %}
```

**Personalization tokens:** don't bake tokens (`{{ contact.firstname }}`, etc.) into the `html=` default of a `rich_text` field — the token won't render correctly from the template default. Ship a plain default and insert the token via the HubSpot page editor's Insert → Personalize menu.

**CTA buttons:** Use `{% cta "field_id" label="Label" %}` for tracked CTA buttons. Create CTAs in HubSpot using the **Embedded HTML** template type (**Marketing > Lead Capture > CTAs > Embeds and Buttons > Embedded HTML**) with brand CSS. The marketer picks which CTA to use from the sidebar. For anchor links (e.g., scroll to form), use a styled `<a>` with `.btn-primary` class — these don't need CTA tracking since the conversion is the form submission. See the `hubspot-cta` skill for brand CSS, full workflow, and CTA creation details.

---

## [Company] Brand Adaptation for Landing Pages

### CSS Custom Properties Setup

Include these CSS custom properties in the template's `<style>` block for consistent brand application:

```css
:root {
  /* Fill values from brain/brand-guide/brand-guide.md */
  --canvas: /* primary background */;
  --surface: /* card/surface color */;
  --border: /* default border color */;
  --text: /* primary text */;
  --text-muted: /* secondary text */;
  --accent: /* primary accent */;
  --accent-2: /* secondary accent, if any */;
  --gradient: /* decorative gradient, if the brand has one */;
  --gradient-text: /* text-effect gradient, if the brand has one */;
  --font: /* brand font stack, from brand-guide */;
}
```

### Brand-Compliant Section Patterns

**Note on colors:** `dnd_*` parameters like `background_color` and `background_linear_gradient` require literal color values — they can't reference CSS variables. The `#111111` / `#222222` values below are obvious placeholders; substitute the actual values from `brain/brand-guide/brand-guide.md`. Inline styles inside `module_attribute` blocks *can* use `var(--token)` because the `:root` block lives in the template's `<head>`.

**Hero Section:**
```jinja
{% dnd_section
  background_color="#111111",
  max_width=1080,
  padding={"top": 80, "bottom": 64, "left": 32, "right": 32}
%}
  {% dnd_column offset=0, width=12 %}
    {% dnd_module path="@hubspot/rich_text" %}
      {% module_attribute "html" %}
        <div style="text-align: center;">
          <p style="font-size: 14px; font-weight: 400; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px;">[TAG LINE]</p>
          <h1 style="font-size: 60px; font-weight: 600; color: var(--text); line-height: 110%; letter-spacing: -1.72px; margin-bottom: 24px;">[HEADLINE]</h1>
          <p style="font-size: 18px; font-weight: 400; color: var(--text-muted); line-height: 32px; max-width: 680px; margin: 0 auto 40px;">[SUBHEADLINE]</p>
        </div>
      {% end_module_attribute %}
    {% end_dnd_module %}
    {% dnd_module path="@hubspot/button" %}
    {% end_dnd_module %}
  {% end_dnd_column %}
{% end_dnd_section %}
```

**Feature Grid (Cards):**
```jinja
{% dnd_section
  background_color="#111111",
  max_width=1080,
  padding={"top": 64, "bottom": 64, "left": 32, "right": 32}
%}
  {% dnd_column offset=0, width=4, padding={"top": 16, "right": 16, "bottom": 16, "left": 16} %}
    {% dnd_module path="@hubspot/rich_text" %}
      {% module_attribute "html" %}
        <div style="background: var(--surface); border: 1px solid var(--border); border-radius: 32px; padding: 32px 40px;">
          <h3 style="font-size: 20px; font-weight: 600; color: var(--text); line-height: 120%; margin-bottom: 16px;">[Feature Title]</h3>
          <p style="font-size: 16px; font-weight: 400; color: var(--text-muted); line-height: 120%;">[Feature description]</p>
        </div>
      {% end_module_attribute %}
    {% end_dnd_module %}
  {% end_dnd_column %}
  {# Repeat for additional feature columns #}
{% end_dnd_section %}
```

**Form Section:**
```jinja
{% dnd_section
  background_color="#222222",
  max_width=1080,
  padding={"top": 64, "bottom": 64, "left": 32, "right": 32}
%}
  {% dnd_column offset=0, width=6, vertical_alignment="MIDDLE", padding={"right": 40} %}
    {% dnd_module path="@hubspot/rich_text" %}
      {% module_attribute "html" %}
        <h2 style="font-size: 48px; font-weight: 600; color: var(--text); line-height: 110%; letter-spacing: -1.72px; margin-bottom: 24px;">[Form Headline]</h2>
        <p style="font-size: 18px; color: var(--text-muted); line-height: 32px;">[Supporting copy]</p>
      {% end_module_attribute %}
    {% end_dnd_module %}
  {% end_dnd_column %}
  {% dnd_column offset=6, width=6, padding={"left": 40} %}
    {% dnd_module path="@hubspot/form" %}
    {% end_dnd_module %}
  {% end_dnd_column %}
{% end_dnd_section %}
```

For single-field capture forms (newsletter subscribe, early-access waitlist), use a centered single-column hero layout instead of the split-column form card above — one field doesn't balance against a dense text column. Centered matches how Substack, TLDR, and Every handle the pattern.

**Social Proof / Logo Bar:**
```jinja
{% dnd_section
  background_color="#111111",
  max_width=1080,
  padding={"top": 48, "bottom": 48, "left": 32, "right": 32}
%}
  {% dnd_column offset=0, width=12 %}
    {% dnd_module path="@hubspot/rich_text" %}
      {% module_attribute "html" %}
        <p style="text-align: center; font-size: 14px; font-weight: 500; text-transform: uppercase; color: var(--text-muted); letter-spacing: 1px; margin-bottom: 32px;">Trusted by</p>
      {% end_module_attribute %}
    {% end_dnd_module %}
    {% dnd_module path="@hubspot/logo_grid" %}
    {% end_dnd_module %}
  {% end_dnd_column %}
{% end_dnd_section %}
```

**Gradient Accent Divider:**
```jinja
{% dnd_section
  background_linear_gradient={"direction": "to right", "colors": ["#111111", "#EEEEEE"]},
  padding={"top": 2, "bottom": 2}
%}
  {% dnd_column offset=0, width=12 %}
  {% end_dnd_column %}
{% end_dnd_section %}
```

The gradient colors above are placeholders. If the brand guide defines a decorative gradient, use it for dividers and non-text surfaces. If it defines a separate text-effect gradient, reserve that one for gradient text via `background-clip: text`. See `brain/brand-guide/brand-guide.md`.

---

## Landing Page Template Structure

### Fixed Layout (default for the company templates)

```
1. Template annotations (templateType, label, isAvailableForNewContent)
2. <!DOCTYPE html>
3. <html lang="en">
4. <head>
   - {{ standard_header_includes }}
   - Brand font import (see brand-guide)
   - CSS custom properties (:root block)
   - Base reset and typography styles
   - Component styles (buttons, cards, forms, HubSpot form overrides)
   - Responsive media queries (@media max-width: 768px)
5. <body>
   - Top gradient bar
   - HTML sections with inline HubL fields ({% text %}, {% rich_text %}, {% image %}, {% form %})
   - Bottom gradient bar
   - {{ standard_footer_includes }}
6. </body></html>
```

### Drag-and-Drop Layout (for general-purpose templates)

```
1. Template annotations (templateType, label, isAvailableForNewContent)
2. <!DOCTYPE html>
3. <html lang="en">
4. <head>
   - {{ standard_header_includes }}
   - Brand font import (see brand-guide)
   - CSS custom properties (:root block)
   - Base reset and typography styles
   - Component styles (buttons, cards, forms)
   - Responsive media queries (@media max-width: 768px)
5. <body style="background-color: var(--canvas); margin: 0;">
6. {% dnd_area "main_content" %}
   a. Hero section (headline, subhead, CTA)
   b. Social proof / logo bar (optional)
   c. Problem / pain point section (optional)
   d. Solution / feature sections
   e. Testimonial or quote section (optional)
   f. Form or CTA section
   g. FAQ section (optional)
   h. Final CTA section
7. {% end_dnd_area %}
8. {{ standard_footer_includes }}
9. </body></html>
```

---

## Fixed Layout Templates

For pages where the structure shouldn't change — webinars, event registrations, product launches — use a **fixed layout** instead of `{% dnd_area %}`. This gives full design control while still allowing content editing through HubSpot's sidebar.

### How Fixed Layout Works

Instead of wrapping content in `{% dnd_area %}` / `{% dnd_section %}` / `{% dnd_column %}` / `{% dnd_module %}`, you write standard HTML with HubL editable field tags inline:

```html
<section class="hero">
  <div class="page-wrap">
    <h1>{% text "page_title" label="Page Title", value="Default Headline" %}</h1>
    <div class="subtitle">{% text "subtitle" label="Subtitle", value="Default supporting copy" %}</div>
    {% rich_text "body_content" label="Body Content", html="<p>Default paragraph</p>" %}
    {% image "hero_image" label="Hero Image", src="", alt="Description" %}
    {% form "signup_form" label="Registration Form" %}
  </div>
</section>
```

Each `{% text %}`, `{% rich_text %}`, `{% image %}`, `{% boolean %}`, and `{% form %}` tag creates an editable field in HubSpot's right sidebar. Marketers edit content without touching layout.

**CRITICAL: Never put `{% text %}` inside a `<p>` tag.** HubSpot wraps every `{% text %}` field in a block-level `<div id="hs_cos_wrapper_...">`. A `<div>` inside a `<p>` is invalid HTML — browsers eject the block element, breaking layout, centering, and font-size overrides. Always use `<div>` (or `<h1>`–`<h6>`, `<span>` for inline) as the parent container for `{% text %}` tags. This applies to `{% rich_text %}` and `{% module %}` tags as well.

**The same applies to headings:** never place `{% rich_text %}` (or `{% text %}` / `{% module %}`) inside `<h1>`–`<h6>` — the injected `<div>` inside a heading is invalid HTML. For headings that need editable or personalized content, render in `<div role="heading" aria-level="1">` styled to match your heading rules; keep non-editable accent spans (e.g., gradient words) as separate fields inside the same container.

### When to Use Fixed vs Drag-and-Drop

| Approach | Use When | Tradeoff |
|----------|----------|----------|
| **Fixed layout** | Structure is locked (webinar, event, product launch). Design consistency is priority. | Marketers can edit content but not add/remove/reorder sections |
| **Drag-and-drop** (`dnd_area`) | Marketers need to add, remove, or reorder sections. General-purpose templates. | Less design control — editors can break layout |

### Fixed Layout Structure

```
1. Template annotations
2. <!DOCTYPE html>
3. <head>
   - {{ standard_header_includes }}
   - Brand font import, CSS custom properties, styles
4. <body>
   - Gradient bar (top)
   - HTML sections with inline HubL fields
   - Gradient bar (bottom)
   - {{ standard_footer_includes }}
5. </body></html>
```

Note: The `{% dnd_area %}` hierarchy is NOT used in fixed layout templates. All layout is controlled by your HTML/CSS.

---

## Template Inheritance & Partials

HubSpot supports template inheritance and partials for code reuse:

```jinja
{# Extend a parent template #}
{% extends "./base-template.html" %}

{# Include a partial/snippet #}
{% include "./partials/header.html" %}

{# Include a global partial (shared across all templates) #}
{% global_partial path="./partials/footer.html" %}
```

**Our approach:** We use the **base template + variants** pattern (duplicate and customize) instead of `{% extends %}` or `{% include %}`. Each template is a standalone file. This keeps templates self-contained and avoids dependency chains in Design Manager. See the "Base Template + Variants" section below.

---

## CSS Guidelines for HubSpot Templates

### What Works in HubSpot Pages (vs. Email)
HubSpot landing pages render in actual browsers, so you have **full CSS support**:

- Flexbox and CSS Grid — fully supported
- CSS custom properties (variables) — supported
- `border-radius` — fully supported
- `linear-gradient` — fully supported (use for the brand gradient, if the brand has one)
- `background-clip: text` — supported (for gradient text effect)
- Google Fonts via `@import` — supported
- Media queries — supported
- Transitions and animations — supported
- `backdrop-filter: blur()` — supported

### Style Block Placement

Place styles inside a `<style>` tag in the `<head>`, after `{{ standard_header_includes }}`:

```html
<head>
  {{ standard_header_includes }}
  <style>
    /* Brand font import — use the font and weights from brain/brand-guide/brand-guide.md, e.g.: */
    @import url('https://fonts.googleapis.com/css2?family=YOUR-BRAND-FONT:wght@400;500;600;700&display=swap');

    /* CSS custom properties and styles */
  </style>
</head>
```

### Responsive Breakpoints

Follow the brand guide responsive approach:

```css
/* Tablet */
@media (max-width: 1024px) {
  /* Reduce font sizes, padding */
}

/* Mobile */
@media (max-width: 768px) {
  /* Stack columns, reduce typography scale */
  h1 { font-size: 36px !important; letter-spacing: -0.8px !important; }
  h2 { font-size: 32px !important; }
  .section-padding { padding: 32px 16px !important; }
}
```

### Button Styles

The brand guide should name a default CTA color for landing pages (see `brain/brand-guide/brand-guide.md`). When a brand approves more than one accent for buttons, be deliberate about which one is the default: some accent colors read as informational rather than actionable inside a CMS content area, or compete with adjacent accents (eyebrows, tags, gradient text). Use the alternate accent when the default competes with nearby accents on the page.

```css
.btn-primary {
  display: inline-block;
  padding: 8px 24px;
  background-color: var(--accent);
  color: var(--text);
  font-family: var(--font);
  font-size: 18px;
  font-weight: 500;
  line-height: 150%;
  border: none;
  border-radius: 12px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
}
.btn-primary:hover { background-color: var(--accent-2); /* or a hover shade per brand-guide */ }

.btn-secondary {
  display: inline-block;
  padding: 8px 24px;
  background-color: var(--canvas);
  color: var(--text);
  font-family: var(--font);
  font-size: 18px;
  font-weight: 500;
  line-height: 150%;
  border: 1px solid var(--text);
  border-radius: 12px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s;
}
.btn-secondary:hover { background-color: var(--surface); }
```

### Form Styling

HubSpot has **two form renderers** with completely different CSS class hierarchies. You must override both.

#### New Renderer (hsfc-*) — Current Default

HubSpot's new form renderer (v2/Next) uses `hsfc-*` prefixed classes and CSS custom variables for spacing. The form JS injects its own stylesheet dynamically at runtime, **after** your `<style>` block loads. Key classes:

- `.hsfc-FormWrapper` — outer form wrapper
- `.hsfc-Step` — step container (even single-step forms)
- `.hsfc-Step__Content` — content area (this is where internal padding lives via `--hsf-background__padding`)
- `.hsfc-Row` — row containers (uses CSS grid)
- `[data-hsfc-id="Renderer"]` — data attribute on the renderer root

**Critical:** The `.hsfc-Step__Content` element gets padding from a CSS variable `--hsf-background__padding`. This causes form fields to appear indented inside your card. You MUST override this.

**Required fix — late-load style block:** Place form overrides in a `<style>` tag **after** `{{ standard_footer_includes }}` so they load after HubSpot's dynamic CSS:

```html
{{ standard_footer_includes }}

<style>
  /* Override HubSpot Next renderer padding variables */
  .form-card {
    --hsf-background__padding: 0px !important;
    --hsf-default-background__padding: 0px !important;
  }
  /* Target wrapper classes directly */
  .form-card .hsfc-Step__Content,
  .form-card [data-hsfc-id="Renderer"] .hsfc-Step .hsfc-Step__Content {
    padding: 0 !important;
    margin: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
  }
  .form-card .hsfc-FormWrapper,
  .form-card .hsfc-Step,
  .form-card [data-hsfc-id] {
    width: 100% !important;
    max-width: 100% !important;
    padding: 0 !important;
  }
  .form-card .hsfc-Row {
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  /* Textarea padding fix — new renderer gives 0px padding to textareas */
  .form-card .hsfc-TextareaInput {
    padding: 10px 12px !important;
  }
  /* Move reCAPTCHA below privacy text using absolute positioning */
  .form-card .hsfc-Row:has(.hsfc-ReCaptchaV2) {
    position: absolute !important;
    bottom: 32px;
    left: 32px;
    margin: 0 !important;
  }
  /* Legacy form fallback */
  .form-card .hs-form .input { margin-right: 0 !important; }
  .form-card .hs-form .hs-input { width: 100% !important; }
</style>
</body>
```

**Why late-load?** HubSpot's form JS loads its own CSS dynamically when the form renders. Styles in `<head>` get overridden by the later-loaded form CSS. Placing our overrides after `{{ standard_footer_includes }}` ensures they come last in the cascade and win.

#### Known New Renderer Bugs & Fixes

**Textarea padding:** The new renderer's `.hsfc-TextareaInput` (textarea fields) gets `0px` padding while `.hsfc-TextInput` (regular input fields) gets `12px`. Always include the textarea padding fix in the late-load style block:

```css
.form-card .hsfc-TextareaInput {
  padding: 10px 12px !important;
}
```

**reCAPTCHA positioning:** HubSpot renders the reCAPTCHA v2 badge inside the form between the last field and the submit button (`.hsfc-Row` containing `.hsfc-ReCaptchaV2`). To move it below the privacy/consent text at the bottom of the form card:

1. Add `position: relative` to `.form-card` (usually already present)
2. Increase `.form-card` bottom padding by ~76px (60px badge height + 16px gap) to make room
3. Absolutely position the reCAPTCHA row at the bottom of the card:

```css
.form-card .hsfc-Row:has(.hsfc-ReCaptchaV2) {
  position: absolute !important;
  bottom: 32px;
  left: 32px;
  margin: 0 !important;
}
```

This takes the reCAPTCHA out of the form flow (while keeping it functionally inside the `<form>` element) so the privacy text appears between the submit button and the reCAPTCHA badge.

**Never use bare `[data-hsfc-id]` as a CSS selector** in form overrides — HubSpot tags child elements (`.hsfc-Row`, `.hsfc-NavigationRow`, `.hsfc-EmailField`, etc.) with `data-hsfc-id` too, so a bare attribute selector cascades down and breaks row-level layouts. Name specific values instead: `[data-hsfc-id="Renderer"], [data-hsfc-id="Form"], [data-hsfc-id="Step"]`.

**Horizontal row layouts:** when laying out hsfc form rows horizontally with flex, explicitly set `width: auto !important` on `.hsfc-Row` and `.hsfc-NavigationRow`. HubSpot's own un-prefixed `[data-hsfc-id="Renderer"] .hsfc-Row { width: 100% }` rule will beat your `flex-basis` because CSS spec says explicit `width` wins over `flex-basis` for the main axis of a flex item.

**Hiding field labels** (placeholder-only pattern): use a broad `.form-container label, .form-container legend` selector rather than targeting `.hsfc-Label` or other specific classes. The exact class HubSpot emits can shift between portal versions — a broad selector is more resilient.

#### Legacy Renderer (hs-form / hs-input)

Some HubSpot portals still use the legacy form renderer. Keep these overrides in the `<head>` `<style>` block as fallback:

```css
.hs-form input[type="text"],
.hs-form input[type="email"],
.hs-form textarea,
.hs-form select {
  background-color: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
  font-size: 14px !important;
  padding: 12px 16px !important;
}
.hs-form input:focus,
.hs-form textarea:focus {
  border-color: var(--accent) !important;
  outline: none !important;
}
.hs-form label {
  color: var(--text-muted) !important;
  font-family: var(--font) !important;
  font-size: 14px !important;
  font-weight: 400 !important;
}
.hs-form .hs-button {
  background-color: var(--accent) !important;
  color: var(--text) !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 8px 24px !important;
  font-family: var(--font) !important;
  font-size: 18px !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  transition: all 0.3s !important;
}
.hs-form .hs-button:hover {
  background-color: var(--accent-2) !important; /* or a hover shade per brand-guide */
}
```

#### Subscription Types & Consent

When a landing-page form needs to attach a subscription type, keep the form's Privacy/Consent setting on "None (not applicable)" and use a HubSpot workflow triggered by form submission to perform the Subscribe action. The form-level legitimate-interest consent option attaches the subscription type but injects a visible GDPR disclosure blurb that fights clean landing-page UX.

---

## Base Template + Variants

All [Company] HubSpot landing page templates use a **base template** pattern. The shared foundation (head section, CSS custom properties, gradient bars, form overrides, footer includes) lives in one file, and each page type is a variant that customizes the content area.

### Existing Templates

```
marketing/templates/landing-page-templates/
├── landing-page-base-hubspot.html         ← Base (DO NOT upload — starting point only)
├── livestream-landing-page.html           ← Livestream registration variant
└── demo-request-landing-page.html         ← Demo request variant
```

### Creating a New Landing Page Variant

1. Duplicate `landing-page-templates/landing-page-base-hubspot.html`
2. Rename it (e.g., `product-launch-landing-page.html`)
3. Update the template annotations:
   - Set `isAvailableForNewContent: true`
   - Update `label` (e.g., `[Company] Landing Page - Product Launch`)
4. Replace the content between `CONTENT START` and `CONTENT END` with your page-specific sections
5. Add any variant-specific CSS classes to the `<style>` block (below the marked line)
6. Add responsive rules for any new classes in the `@media` block
7. Upload to Design Manager (see Upload Instructions below)

### What's Shared (don't modify unless updating brand)

- `<head>` section: `{{ standard_header_includes }}`, brand font import, CSS custom properties
- Reset styles (box-sizing, body defaults, img, link styles)
- Reusable CSS classes: `.page-wrap`, `.gradient-bar`, `.btn-primary`, `.btn-secondary`, `.tag`, `.card`, `.section-label`
- HubSpot form overrides (`.card .hs-form` styles)
- Top and bottom gradient bars
- `{{ standard_footer_includes }}`

### What Changes Per Variant

- The content area between `CONTENT START` and `CONTENT END`
- Variant-specific CSS classes (e.g., `.hero`, `.split-section`, `.speakers-grid` in the livestream)
- Variant-specific responsive rules
- HubL editable fields (`{% text %}`, `{% rich_text %}`, `{% image %}`, `{% form %}`, etc.)

---

## Output Format

**Output location:** `marketing/pages/[page-slug]/` — confirm the project slug with the user before creating files.

### For Each Template, Provide:

**1. Complete HubL template file**
- Production-ready with template annotations
- `{{ standard_header_includes }}` and `{{ standard_footer_includes }}` in place
- For fixed layout: HTML sections with inline HubL fields (`{% text %}`, `{% rich_text %}`, `{% image %}`, `{% form %}`)
- For drag-and-drop: `{% dnd_area %}` with sections using the `dnd_section` → `dnd_column` → `dnd_module` hierarchy
- CSS custom properties and responsive styles in `<style>` block
- Brand font import (see brand-guide)
- `<!-- EDITABLE: -->` comments marking content the marketer should customize
- `[PLACEHOLDER]` brackets for variable content

**2. Upload instructions**
- Step-by-step for uploading to Design Manager:
  1. Go to **Content > Design Manager** (or **Marketing > Files and Templates > Design Tools**)
  2. Click **File > New file**
  3. Select **HTML + HubL** as the file type
  4. In "What are you building?" select **Template**
  5. Click **Template type** and select **Page**
  6. Enter a file name and click **Create**
  7. Paste the complete template code
  8. Click **Publish** (top right)
  9. The template will appear in the template picker when creating new landing pages
  10. For fixed-layout templates: all HubL editable fields (`{% text %}`, `{% rich_text %}`, `{% image %}`, `{% form %}`) will appear in the right sidebar when editing a page
  11. For drag-and-drop templates: sections will be editable via the visual editor
- Note any images that need uploading to HubSpot File Manager first
- Note any custom modules referenced (if applicable)

**3. Customization guide**
- Which sections can be reordered/added/removed in the editor
- Which module fields are editable by marketers
- How to swap the form module for a specific HubSpot form
- How to update CTA links and button text

**4. Testing checklist**
- [ ] Preview in HubSpot page editor
- [ ] Check all drag-and-drop sections are editable
- [ ] Verify responsive behavior at 1024px and 768px breakpoints
- [ ] Confirm brand colors render correctly against the brand guide (canvas, surfaces, accents)
- [ ] Test form submission (if form section included)
- [ ] Verify all links and CTAs work
- [ ] Check page load speed (no unnecessary assets)
- [ ] Validate the brand font loads correctly
- [ ] Test in Chrome, Firefox, Safari, Edge

---

## Checklist Before Delivering

### All Templates
- [ ] Read `/brain/brand-guide/brand-guide.md`
- [ ] Template annotations present (`templateType: page`, `isAvailableForNewContent`, `label`)
- [ ] `{{ standard_header_includes }}` in `<head>`
- [ ] `{{ standard_footer_includes }}` before `</body>`
- [ ] Brand font imported (see brand-guide)
- [ ] CSS custom properties defined in `:root`, values filled from brand-guide
- [ ] Canvas background and text colors match the brand guide
- [ ] Gradient/accent used sparingly per brand-guide rules
- [ ] Primary buttons use the brand guide's default CTA color
- [ ] Card pattern uses the brand guide's surface, border, and radius values
- [ ] Max content width `1080px`
- [ ] Section padding follows brand guide (64px vertical, 32px horizontal)
- [ ] Responsive media queries for tablet (1024px) and mobile (768px)
- [ ] Typography follows brand scale (60px hero h1, 32px section headers, 18px body)
- [ ] No AI slop patterns in any copy (see CLAUDE.md)
- [ ] Product claims verified against `/brain/truth.md`

### Fixed Layout Templates (additional)
- [ ] HubL editable fields (`{% text %}`, `{% rich_text %}`, `{% image %}`, `{% form %}`) used for all marketer-editable content
- [ ] Top and bottom gradient bars present
- [ ] HubSpot form overrides included (`.card .hs-form` or `.form-card .hs-form` styles)
- [ ] If created from base template: shared elements (head, gradient bars, footer includes) preserved

### Drag-and-Drop Templates (additional)
- [ ] `{% dnd_area %}` wraps all content sections
- [ ] Sections use `{% dnd_section %}` → `{% dnd_column %}` → `{% dnd_module %}` hierarchy
- [ ] All modules use valid `@hubspot/` paths or custom module paths

---

## Common Patterns

### Site Header (matches [your-site] production)

**Canonical spec lives in `/brain/brand-guide/brand-guide.md` under "Site Header".** The header should be translucent (the canvas color at partial alpha) with `backdrop-filter: blur()`, matching your production site. Never use an opaque background if production uses a translucent one.

The header uses a sticky wrapper div (not sticky on the `<header>` itself) and `box-sizing: content-box` with an explicit height to match production dimensions. Match logo dimensions to your production site (the example below uses `143px × 32px`).

**CSS:**
```css
.site-header-sticky {
  position: sticky;
  top: 0;
  z-index: 10;
}
.site-header {
  box-sizing: content-box;
  height: 43px;
  padding: 24px 48px;
  background-color: color-mix(in srgb, var(--canvas) 40%, transparent); /* canvas at ~40% alpha — match production */
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
  box-shadow: 0px 4px 10px 0px color-mix(in srgb, var(--canvas) 30%, transparent);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.site-header-logo {
  display: block;
}
.site-header-logo img {
  width: 143px !important;
  height: 32px !important;
  max-width: none !important;
}
```

**HTML:**
```html
<div class="site-header-sticky">
  <header class="site-header">
    <a href="https://[your-site]" class="site-header-logo" aria-label="[Company] home">
      {% module "header_logo" path="@hubspot/image", label="Header Logo", img={src: "", alt: "[Company]", loading: "eager"} %}
    </a>
  </header>
</div>
```

**Why `content-box` + `height: 43px`:** The production site uses `box-sizing: content-box` on the header. With `padding: 24px 48px`, this gives a total rendered height of 91px (24 + 43 + 24). The 43px content area flex-centers the 32px logo, placing it ~29.5px from the header top — matching the production site's logo position. Using `border-box` (from the global reset) with just padding would make the header only 80px tall and position the logo 3–4px higher than production.

### Gradient Text (for hero headlines or emphasis)
```css
.gradient-text {
  background: var(--gradient-text); /* text-effect gradient from brand-guide */
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Decorative Background Blooms

If the hero uses a radial-gradient bloom or similar oversized decoration, don't put `overflow: hidden` on the hero section — it crops the bloom visibly. Instead, put `overflow-x: hidden` on `body` and fade the radial gradient to full transparency well inside its bounding box (e.g., transparent by 50% for a 1400px bloom) so the fade completes before any clipping surface.

### Tags & Pills (two variants — both 8px radius)

**Hard rule:** All tags use `border-radius: 8px`. **Never use `border-radius: 999px` (fully rounded pill shapes) — not on brand.** See `/brain/brand-guide/brand-guide.md` "Tags & Pills" for full use-case guidance.

**Variant A — Solid (`.tag`)** — filled with the accent color, bold and loud. Use for card-tier flags, "NEW"/"BETA" badges, standalone category markers where the tag is the primary attention grabber.

```css
.tag {
  display: inline-block;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--canvas);
  background-color: var(--accent);
  border-radius: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
```

**Variant B — Outlined (`.tag--outline`)** — accent border + translucent tint, subtle. Use for hero eyebrows, pre-CTA kickers, section markers where the tag should feel secondary to a nearby headline or button.

```css
.tag--outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  font-size: 11px;
  font-weight: 600;
  color: var(--accent);
  background: color-mix(in srgb, var(--accent) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--accent) 20%, transparent);
  border-radius: 8px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
}
.tag--outline svg { width: 12px; height: 12px; flex-shrink: 0; }
```

**Picking a variant:** if a CTA button is nearby, use outlined. If the tag is the loudest element in its local area, use solid.

### Section with Background Image + Overlay
```jinja
{% dnd_section
  background_image={
    "backgroundPosition": "MIDDLE_CENTER",
    "backgroundSize": "cover",
    "imageUrl": "https://your-cdn.com/bg.jpg"
  },
  padding={"top": 80, "bottom": 80, "left": 32, "right": 32}
%}
  {# Add a semi-transparent overlay via CSS on the content #}
{% end_dnd_section %}
```

---

## MCP Tools: HubSpot Dev, Figma & agent-browser

### HubSpot Dev MCP (Documentation & CMS)

Use these tools to look up HubSpot documentation and manage CMS assets:

1. **Search docs** — Use `mcp__HubSpotDev__search-docs` to find HubSpot developer documentation on template syntax, HubL tags, module paths, drag-and-drop areas, or any landing page API. Always search before guessing at module paths or field syntax.
2. **Fetch doc page** — Use `mcp__HubSpotDev__fetch-doc` immediately after searching to read the full documentation page. Never skip this step — search results are summaries, not complete docs.
3. **Create a CMS template** — Use `mcp__HubSpotDev__create-cms-template` to scaffold a new landing page template file. Set `templateType` to `page-template`.
4. **Create a CMS module** — Use `mcp__HubSpotDev__create-cms-module` to scaffold custom modules for drag-and-drop templates (e.g., an [Company] CTA Button module, a custom card grid module).
5. **List remote contents** — Use `mcp__HubSpotDev__list-cms-remote-contents` to see what templates, modules, and assets are already deployed in the HubSpot Design Manager.
6. **Create a CMS function** — Use `mcp__HubSpotDev__create-cms-function` to scaffold a serverless function if the landing page needs backend logic (e.g., a custom form handler or API proxy).

**When to use:** Before building any landing page template, search docs to verify module paths and HubL syntax. Use `create-cms-module` when building custom drag-and-drop modules. Use `list-cms-remote-contents` to check for naming conflicts before upload.

---

### Figma MCP (Design-to-Template)

When the user provides a Figma URL or references a landing page design:

1. **Pull design context** — Use `mcp__figma-remote-mcp__get_design_context` to extract the full layout, section structure, colors, typography, and spacing. Translate this into HubL template code (fixed layout with `{% text %}` / `{% rich_text %}` fields, or drag-and-drop with `{% dnd_area %}`).
2. **Take a screenshot** — Use `mcp__figma-remote-mcp__get_screenshot` to see the visual design before building. Compare your output against this screenshot.
3. **Get design variables** — Use `mcp__figma-remote-mcp__get_variable_defs` to pull color tokens, spacing values, and typography settings. Map these to the [Company] CSS custom properties (`:root` block).
4. **Get metadata** — Use `mcp__figma-remote-mcp__get_metadata` to understand the section hierarchy and component structure before pulling full design context.

**When to use:** When translating a Figma mockup into a HubSpot landing page template. The Figma design provides the visual target — your job is to reproduce it in HubL with editable fields for the marketer.

### agent-browser (Template Validation) — MANDATORY

**agent-browser inspection is REQUIRED for all design and CSS work.** Never declare a visual change done without verifying it in the browser first. This applies to:
- New templates (validate locally before upload)
- CSS fixes and tweaks (inspect the live HubSpot page after upload)
- Any change that affects layout, spacing, colors, or typography

#### Local Validation (pre-upload)

1. **Open the template** — Run `agent-browser open <file-path-or-url>` to open the HTML file in the browser. (Note: HubL tags won't render outside HubSpot, but the CSS layout, colors, typography, and responsive behavior can all be validated.)
2. **Full-page screenshot** — Run `agent-browser screenshot --full` to capture the entire page for review.
3. **Test responsive breakpoints** — Run `agent-browser set viewport <width> <height>` to test at desktop (1440px), tablet (1024px), and mobile (768px, 375px). Screenshot at each breakpoint.
4. **Test interactions** — Run `agent-browser click` to test anchor link CTAs (e.g., scroll-to-form buttons), navigation, and any interactive elements.
5. **Accessibility snapshot** — Run `agent-browser snapshot -i` to verify heading hierarchy, form labels, link text, and overall structure.
6. **Check network** — Run `agent-browser network requests` to verify font loading (the brand font), image requests, and overall resource count.

#### Live Page Inspection (post-upload) — ALWAYS DO THIS

After any CSS/design change is uploaded to HubSpot, use agent-browser to inspect the live page:

1. **Navigate to the live page** — Ask the user for the page URL and open it with `agent-browser open <url>`.
2. **Inspect computed styles** — Run `agent-browser eval` to check actual computed CSS values on the elements you changed. Compare against the expected values.
3. **Screenshot and compare** — Take screenshots at 1440px width. Compare against the reference (e.g., [your-site] production site).
4. **Check for HubSpot overrides** — HubSpot injects its own CSS (especially for forms). Use `agent-browser eval` to check if your styles are being overridden. Look for unexpected padding, margins, or widths on wrapper elements.
5. **Verify before declaring done** — Do NOT tell the user a fix is complete until you've confirmed it visually in the browser.

**Key lesson:** HubSpot's new form renderer (hsfc-*) injects CSS dynamically at runtime that overrides `<head>` styles. Always inspect the live rendered page — the local HTML file won't show HubSpot-injected CSS issues.

---

## Analytics

Use the `analytics` skill to pull real landing page performance data when optimizing or creating new pages:

- **`hubspot-pages.ts`** — Page views, form submissions, conversion rates, bounce rates, and traffic source breakdown. Identify top-performing pages and apply their patterns to new templates.

Example: Before building a new landing page, run `npx tsx .claude/skills/analytics/scripts/hubspot-pages.ts 90d` to see which pages have the highest conversion rates and what traffic sources drive the most submissions.

---

## Related Skills

- **hubspot-cta**: CTA button strategy, tracking behavior, email vs landing page patterns, custom module specs
- **hubspot-email**: Companion skill for email templates (different constraints — table-based layout, 600px max, no CSS gradients)
- **brand-design**: For visual design decisions and brand system reference
- **copywriting**: For landing page copy — headlines, CTAs, body content
- **copy-editing**: For reviewing landing page copy
- **page-cro**: For conversion rate optimization of landing pages
- **launch-strategy**: For planning what landing pages to build for a launch

---

## Learnings

<!-- Updated by /reflect in your instance. Promote stable patterns to the main skill body. Ships empty. -->
