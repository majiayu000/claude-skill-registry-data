---
name: ak-elementor-studio
description: >
  AK Elementor Studio — built by Abanoub Khalil (akstudio.me). Converts ANY input — HTML/CSS/JS code, screenshots, images (PNG, JPG, WebP), PDFs, Figma exports, design mockups, wireframes, or any visual file — into fully structured Elementor page JSON templates importable into WordPress. Activate this skill whenever the user: uploads a design image or screenshot and wants it built in WordPress, shares HTML/CSS/JS to convert to Elementor, pastes code or attaches a file and mentions Elementor, WordPress, or page builder, says anything like "convert this to Elementor", "build this in WordPress", "turn this design into a page", "make this Elementor template", "recreate this layout in Elementor", "import this into WordPress", or uploads a PDF/image of a webpage, landing page, mockup, or UI design. This skill handles ALL input types: code, images, PDFs, mixed inputs, and even verbal descriptions of layouts.
---

# AK Elementor Studio
### by [Abanoub Khalil](https://akstudio.me) — Senior WordPress & Webflow Developer

---

## RULE #1 — THE MOST IMPORTANT RULE IN THIS SKILL

```
HTML WIDGET = JAVASCRIPT <script> TAGS ONLY.

The html widget has exactly one valid use:
  → Embedding a <script> tag for JavaScript behavior

That is ALL. Nothing else ever goes in the html widget.
Not headings. Not text. Not badges. Not nav links.
Not cards. Not layouts. Not pricing. Not timelines.
Not icons. Not stats. Not ANY visual content.

Every visual element has a native Elementor widget. Use it.
```

---

## RULE #2 — ABSOLUTE JSON RULES

```
1. NO COMMENTS — /* */ and // both break JSON parsing
   ❌ { /* hero */ "id": "a1b2c3d4" }    ✅ { "id": "a1b2c3d4" }

2. NO TRAILING COMMAS
   ❌ { "a": 1, "b": 2, }               ✅ { "a": 1, "b": 2 }

3. IDs = UNIQUE 8-CHAR HEX ONLY
   ❌ "id": "hero_section"              ✅ "id": "a1b2c3d4"

4. EVERY ELEMENT MUST HAVE "elements": []
   ❌ { "widgetType": "heading", "settings": {} }
   ✅ { "widgetType": "heading", "settings": {}, "elements": [] }

5. isInner RULE
   Direct children of "content": []        → "isInner": false
   Containers nested inside containers      → "isInner": true
   Widgets (inside any container)           → "isInner": false

6. HEX COLORS ONLY — never color names
   ❌ "background_color": "white"       ✅ "background_color": "#FFFFFF"
```

---

## STEP 0 — Pre-Flight Interview

Ask all in ONE message. Never skip.

```
👋 Quick details before I start:

1. SITEMAP — Pages? (I generate one .json per page)

2. ELEMENTOR VERSION — Free or Pro?
   Pro: Theme Builder header/footer, custom CSS, sticky, scroll effects
   Free: header/footer = regular sections inside each page

3. CUSTOM POST TYPES — Any CPTs?
   (Services, Portfolio, Plugins, Team, Testimonials → I'll generate ACF JSON)

4. OUTPUT FORMAT
   a) Individual .json files — import one-by-one via Templates → Saved Templates (always works, Free + Pro)
   b) Elementor native export ZIP — import via Elementor → Tools → Import Kit (no extra plugin needed)
   c) Envato Template Kit ZIP — requires "Template Kit Import" plugin installed on WordPress
   d) Individual .json + ACF field group files

5. BRAND — Hex color codes + Google Fonts?
   (Or I extract from the design)
```

---

## STEP 1 — Input Detection

| Input | Pipeline |
|---|---|
| HTML/CSS/JS | Code Pipeline |
| PNG/JPG/WebP/screenshot/mockup/Figma | Visual Pipeline |
| PDF | PDF Pipeline |
| Words only | Description Pipeline |
| Existing Elementor JSON | Edit Pipeline |
| Mixed | Both pipelines, merged |

---

## COMPLETE WIDGET REFERENCE — Native Widgets for Every Element

### Text & Numbers
| Element | Widget |
|---|---|
| h1 / h2 / h3 / h4 / h5 / h6 | `heading` |
| Paragraph / body text | `text-editor` |
| Animated counter (500+, 10K) | `counter` |
| Progress / skill bar | `progress` |

### Actions
| Element | Widget |
|---|---|
| Button / CTA / link-as-button | `button` |
| FAQ / collapsible rows | `accordion` |
| Tab navigation | `tabs` |
| Alert / info banner | `alert` |

### Media
| Element | Widget |
|---|---|
| Photo / image | `image` |
| YouTube / Vimeo / video | `video` |
| Image grid | `image-gallery` |
| Image slider / carousel | `image-carousel` |

### Cards & Lists
| Element | Widget |
|---|---|
| Icon + title + description | `icon-box` |
| Bulleted list with icons | `icon-list` |
| Photo + title + text | `image-box` |
| Customer quote | `testimonial` |

### Layout Helpers
| Element | Widget |
|---|---|
| Horizontal line / separator | `divider` |
| Vertical blank space | `spacer` |

### Utilities
| Element | Widget |
|---|---|
| Social media icons | `social-icons` |
| Map embed | `google-maps` |
| Plugin/form shortcode | `shortcode` |

---

## SOLVING COMPLEX ELEMENTS WITHOUT html WIDGET

### Navigation Bar
```
Structure: flex container (row, space-between)
  └── image widget          ← logo
  └── icon-list widget      ← nav links (set icon to "none", each item = a page link)
      OR multiple button widgets (size: xs, style: link/ghost, one per nav item)
  └── button widget         ← CTA button
```

### Badge / Status Pill / Tag
```
Option A: button widget
  text: "FULL-TIME", size: "xs", border_radius: 100px
  button_text_color: "#00D4C8", button_background_color: "rgba(0,212,200,0.1)"
  no link href (or link to "#")

Option B: alert widget
  type: "success" / "info" / "warning"
  alert_title: "WordPress Developer"
  (style with custom CSS if Pro)
```

### Career Timeline / Work History Entry
```
Structure: inner container (column, border-left: 2px solid accent)
  └── inner container (row, gap: 8px)   ← date + status row
      └── text-editor widget            ← "OCT 2024 — PRESENT"
      └── button widget (xs, pill)      ← "FULL-TIME" badge
  └── heading widget (h3/h4)            ← "Senior WordPress & Webflow Developer"
  └── text-editor widget                ← "InVitro Capital — Cairo, Egypt"
  └── text-editor widget                ← description paragraph
  └── inner container (row, wrap)       ← tech tags row
      └── button widget (xs, ghost)     ← "WordPress"
      └── button widget (xs, ghost)     ← "Webflow"
      └── button widget (xs, ghost)     ← "CMS"
```

### Contact Info Panel
```
Structure: styled container (background: #141628, border-radius: 12px, padding: 32px)
  └── inner container (row) per info row:
      └── text-editor widget    ← label "LOCATION" (small, muted)
      └── text-editor widget    ← value "Cairo, Egypt"
  └── inner container (row) per clickable row:
      └── text-editor widget    ← label "EMAIL"
      └── button widget         ← "hello@akstudio.me" (style: link, href: mailto:)
  └── alert widget              ← "Currently available" status
  └── button widget             ← "Book a discovery call" CTA
```

### Skill Depth / Progress Bars
```
Structure: container (column)
  └── text-editor widget   ← "SKILL DEPTH" heading
  └── per skill: inner container (row)
      └── text-editor     ← "WP" label
      └── progress widget ← percent: 95, type: line, bar_color: accent
      └── text-editor     ← "Expert" label
```

### Pricing Card
```
Structure: inner container (column, background: #141628, border-radius: 12px, padding: 40px)
  └── text-editor widget    ← plan tier label
  └── heading widget (h2)   ← "$99" price
  └── text-editor widget    ← "/month" period
  └── divider widget
  └── icon-list widget      ← feature list (checkmark icons)
  └── button widget         ← "Get Started" CTA (full width)
```

### Testimonial Card
```
Use testimonial widget (handles everything natively):
  image: avatar URL, name: "Client Name", title: "CEO, Company"
  content: "Quote text here"

OR custom layout:
  inner container (column)
    └── icon-list widget (1 item, star icon × 5)  ← star rating
    └── text-editor widget                         ← quote text
    └── inner container (row)
        └── image widget (border-radius: 50%)      ← avatar
        └── inner container (column)
            └── heading widget (h5)                ← name
            └── text-editor widget                 ← title/company
```

### Logo Cloud / Partner Logos
```
Use image-carousel widget:
  slides: [logo1, logo2, logo3, logo4, logo5]
  slides_to_show: 5, autoplay: yes, navigation: none
  image_size: medium
```

### Footer Column Structure
```
Column 1 (brand col):
  └── image widget          ← logo
  └── text-editor widget    ← tagline
  └── social-icons widget   ← LinkedIn, GitHub, Twitter

Columns 2-4 (link cols):
  └── heading widget (h5)   ← "Quick Links" / "Services" / "Contact"
  └── icon-list widget      ← links (icon: none or arrow, one per link)

Bottom bar:
  └── container (row, space-between)
      └── text-editor       ← "© 2025 Abanoub Khalil"
      └── text-editor       ← privacy / terms links (inline <a> tags)
```

---

## Code Pipeline

### Step 1 — Inventory
For every element: name it, declare its native widget, explain why. If you considered html widget, apply the JS-only self-check first.

### Step 2 — Widget Assignment
Zero visual content in html widget. Apply the Complete Widget Reference above.

### Step 3 — CSS Extraction
Map CSS → Elementor settings (`references/style-map.md`). CSS variables → resolve to hex.

### Step 4 — JSON Build
Section by section. Validate as you write.

### Step 5 — Output
One `.json` per page. No comments. All IDs unique 8-char hex.

---

## Visual Pipeline

### Phase 1 — Inventory (top to bottom)

```
NAVBAR:
  Logo: [position / type: image or text]
  Nav links: [list each] → icon-list items OR button widgets
  CTA button(s): [text / color hex]
  Background: [#HEX or transparent]

HERO:
  BG: [solid #HEX / gradient #X→#Y Ndeg / image overlay / video]
  Layout: [centered / text-left+image-right]
  Min-height: [100vh / fixed px]
  Elements:
    [badge?] → alert widget or button widget (xs, pill)
    [h1] → heading widget
    [h3/subtitle] → heading widget
    [description] → text-editor widget
    [CTA buttons] → button widgets
    [image] → image widget

SECTION N:
  Purpose: [features / stats / about / timeline / contact panel / testimonials / CTA]
  Layout: [1-col / 2-col / 3-col / 4-col]
  Background: [#HEX]
  Per column: list native widget for each element

FOOTER: [N columns, content per column]
```

### Phase 2 — Colors
Extract hex for: primary, secondary, accent, heading text, body text, muted, light bg, dark bg, card bg, border.
→ Full reference table in `references/visual-analysis.md`

### Phase 3 — Typography
Heading font, body font, label font — family, weight, desktop/tablet/mobile sizes.

### Phase 4 — Layout Mapping
Use container grid in `references/section-patterns.md`.

### Phase 5 — Widget Assignment
Apply Complete Widget Reference. Zero html widgets for visual content.

### Phase 6 — Spacing
Section pad: 60-80px standard, 100-120px hero. Card pad: 24-32px. Gap: 20-30px.

### Phase 7 — Analysis Summary + JSON

```markdown
## 🔍 Visual Analysis — [Page]

**Pages detected:** [list]
**Style:** [Dark/Light/Bold/Minimal]

| Token | Value |
|---|---|
| Primary | #______ |
| Accent | #______ |
| Heading text | #______ |
| Body text | #______ |
| Background | #______ |
| Heading font | Inter 700 |

**Widget map:**
1. Navbar → image + icon-list + button
2. Hero → alert (badge) + heading + text-editor + button + image
3. Stats → N× counter widgets
4. Timeline → N× [text-editor + button (badge) + heading + text-editor + button row] per entry
5. Contact panel → styled container + text-editor rows + button links + alert + button
6. Footer → image + text-editor + social-icons + icon-list columns

**html widgets used:** [List ONLY <script> JS uses. If none: "None."]

**Assumptions:** [list all approximations]
**⚠️ After import:** replace placeholder images, update nav links
```

---

## PDF Pipeline
Single PDF → Visual Pipeline. Multi-page → one template per page. Selectable text → extract exact copy.

## Description Pipeline
Ask page type. Apply Widget Reference. Use defaults: primary `#1A1A2E`, accent `#005AFF`, font `Inter`.

## Edit Pipeline
Parse → locate → change → re-output full valid JSON → summarize.

---

## Core Schemas

### Section Container
```json
{
  "id": "a1b2c3d4",
  "elType": "container",
  "isInner": false,
  "settings": {
    "content_width": "full",
    "flex_direction": "column",
    "flex_align_items": "center",
    "flex_justify_content": "flex-start",
    "flex_gap": { "unit": "px", "column": "30", "row": "30", "isLinked": true },
    "padding": { "unit": "px", "top": "80", "right": "60", "bottom": "80", "left": "60", "isLinked": false },
    "padding_tablet": { "unit": "px", "top": "50", "right": "30", "bottom": "50", "left": "30", "isLinked": false },
    "padding_mobile": { "unit": "px", "top": "40", "right": "20", "bottom": "40", "left": "20", "isLinked": false },
    "background_background": "classic",
    "background_color": "#FFFFFF"
  },
  "elements": []
}
```

### Inner Container (column)
```json
{
  "id": "b2c3d4e5",
  "elType": "container",
  "isInner": true,
  "settings": {
    "width": { "unit": "%", "size": 50 },
    "width_tablet": { "unit": "%", "size": 100 },
    "width_mobile": { "unit": "%", "size": 100 },
    "flex_direction": "column",
    "flex_align_items": "flex-start",
    "padding": { "unit": "px", "top": "20", "right": "20", "bottom": "20", "left": "20", "isLinked": true }
  },
  "elements": []
}
```

### Widget
```json
{
  "id": "c3d4e5f6",
  "elType": "widget",
  "widgetType": "heading",
  "isInner": false,
  "settings": {},
  "elements": []
}
```

---

## CSS → Elementor (Quick Reference)
Full table in `references/style-map.md`.

```json
"padding": { "unit": "px", "top": "80", "right": "60", "bottom": "80", "left": "60", "isLinked": false }
"_padding": { "unit": "px", "top": "0", "right": "0", "bottom": "20", "left": "0", "isLinked": false }
"_margin": { "unit": "px", "top": "0", "right": "auto", "bottom": "30", "left": "auto", "isLinked": false }
"typography_typography": "custom", "typography_font_family": "Inter",
"typography_font_size": { "unit": "px", "size": 48 },
"typography_font_size_tablet": { "unit": "px", "size": 36 },
"typography_font_size_mobile": { "unit": "px", "size": 24 },
"typography_font_weight": "700",
"typography_line_height": { "unit": "em", "size": 1.3 },
"typography_letter_spacing": { "unit": "px", "size": -0.5 }
"background_background": "gradient", "background_gradient_type": "linear",
"background_color": "#005AFF", "background_color_b": "#0040CC",
"background_gradient_angle": { "unit": "deg", "size": 135 }
"border_border": "solid",
"border_width": { "unit": "px", "top": "1", "right": "1", "bottom": "1", "left": "1", "isLinked": true },
"border_color": "#E5E7EB",
"border_radius": { "unit": "px", "top": "12", "right": "12", "bottom": "12", "left": "12", "isLinked": true }
"box_shadow_box_shadow_type": "yes",
"box_shadow_box_shadow": { "horizontal": 0, "vertical": 4, "blur": 24, "spread": 0, "color": "rgba(0,0,0,0.08)" }
```

---

## Responsive
```json
"width": { "unit": "%", "size": 33 },
"width_tablet": { "unit": "%", "size": 50 },
"width_mobile": { "unit": "%", "size": 100 }
```

---

## Multi-Page Output
1. One `.json` per page
2. Elementor Pro → `header.json` + `footer.json` (type: `"header"` / `"footer"`)
3. Elementor Free → header/footer as regular container sections inside each page

---

## ✅ Import Methods — Tested & Verified

⚠️ CRITICAL: Three completely different ZIP formats exist. Using the wrong one causes
"Couldn't use the .zip file" in Elementor's importer. Match the format to the method.

---

### Method 1 — Individual .json per template (ALWAYS WORKS — Free + Pro)
```
Recommended default. No plugins required. Works on any Elementor version.

Steps:
  1. Elementor → Templates → Saved Templates → Import Templates (↑ icon)
  2. Upload one .json file at a time → Import Now
  3. Repeat for each page (global-styles first, then header/footer, then pages)
  4. Create a WordPress page → Edit with Elementor
     → folder icon (My Templates) → find template → Insert

Each .json file envelope format (single template):
{
  "version": "0.4",
  "title": "Page Name",
  "type": "page",          ← "page" | "header" | "footer" | "kit-styles"
  "content": [...],        ← the elements array from your page JSON
  "page_settings": {},
  "settings": {}
}
```

---

### Method 2 — Elementor Native Export ZIP (no extra plugin needed)
```
Works via: Elementor → Tools → Import Kit
Does NOT require Template Kit Import plugin.
This is what Elementor exports natively when you use Tools → Export Kit.

⚠️ Do NOT confuse manifest.json with Envato's kit.json — they are different formats.

ZIP structure:
kit-export.zip
├── manifest.json                    ← required, exact format below
├── ak-header/
│   └── template.json
├── ak-footer/
│   └── template.json
├── ak-home/
│   └── template.json
└── ak-about/
    └── template.json                (one folder per template, folder name is arbitrary)

manifest.json format:
{
  "name": "Kit Name",
  "title": "Kit Name",
  "description": "...",
  "author": "Abanoub Khalil",
  "version": "1.0.0",
  "elementor_version": "3.0.0",
  "created": "2025-01-01",
  "thumbnail": "",
  "site": "https://akstudio.me",
  "plugins": [
    { "name": "Elementor", "slug": "elementor", "pluginFile": "elementor/elementor.php", "version": "3.0.0" },
    { "name": "Elementor Pro", "slug": "elementor-pro", "pluginFile": "elementor-pro/elementor-pro.php", "version": "3.0.0" }
  ],
  "templates": [
    { "name": "Header", "title": "Header", "thumbnail": "", "url": "",
      "export_date": "2025-01-01", "source": "", "type": "header", "subtype": "header",
      "id": 1001, "author": "Abanoub Khalil", "path": "ak-header/" },
    { "name": "Footer", "title": "Footer", "thumbnail": "", "url": "",
      "export_date": "2025-01-01", "source": "", "type": "footer", "subtype": "footer",
      "id": 1002, "author": "Abanoub Khalil", "path": "ak-footer/" },
    { "name": "Home", "title": "Home", "thumbnail": "", "url": "",
      "export_date": "2025-01-01", "source": "", "type": "page", "subtype": "page",
      "id": 1003, "author": "Abanoub Khalil", "path": "ak-home/" }
  ],
  "site-settings": { "settings": {} }
}

Each folder's template.json uses the same envelope as Method 1 above.

Import steps:
  1. Elementor → Tools → Import Kit → upload ZIP
  2. Select which templates to import → Import
  3. Assign header/footer via Theme Builder → Conditions
```

---

### Method 3 — Envato Template Kit ZIP (requires Template Kit Import plugin)
```
⚠️ ONLY use this format when the client explicitly has the "Template Kit Import" plugin.
⚠️ Do NOT use with Elementor's native Tools → Import — it WILL FAIL with "Couldn't use the .zip file".

Requires plugin: "Template Kit Import" (free, wordpress.org)
Import via: WordPress Admin → Tools → Template Kit → Upload ZIP

ZIP structure:
kit-name.zip
├── kit.json                         ← Envato manifest (completely different from manifest.json)
└── templates/
    ├── global-styles.json
    ├── header.json
    ├── footer.json
    ├── home.json
    └── about.json

kit.json format:
⚠️ Key is "authorURL" (camelCase) — NOT "author_url" (snake_case will silently break validation)
{
  "name": "Kit Name",
  "slug": "kit-slug",
  "version": "1.0.0",
  "author": "Abanoub Khalil",
  "authorURL": "https://akstudio.me",
  "templates": [
    { "name": "Global Styles", "file": "templates/global-styles.json", "type": "kit-styles", "thumbnail": "" },
    { "name": "Home",          "file": "templates/home.json",          "type": "page",        "thumbnail": "" },
    { "name": "Header",        "file": "templates/header.json",        "type": "header",      "thumbnail": "" },
    { "name": "Footer",        "file": "templates/footer.json",        "type": "footer",      "thumbnail": "" }
  ],
  "requiredPlugins": [
    { "name": "Elementor", "slug": "elementor", "source": "wordpress" }
  ]
}

Import steps:
  1. Install "Template Kit Import" plugin from wordpress.org
  2. Tools → Template Kit → Upload Template Kit ZIP File
  3. Import Global Kit Styles FIRST (sets colors + fonts site-wide)
  4. Import each template in order
  5. Pages → Add New → Edit with Elementor → folder icon → View Installed Kit → Insert
```

---

### DEFAULT OUTPUT RECOMMENDATION
```
When user asks for a kit ZIP with no plugin context → produce Method 2 (Elementor native export)
When user asks for individual files                → produce Method 1 envelopes
When user mentions "Template Kit Import plugin"    → produce Method 3 (Envato format)
When in doubt                                      → produce Method 1 — it never fails
```

---

## Global Kit Styles (global-styles.json)
Always generate with actual brand values. Import FIRST before any page templates.

```json
{
  "title": "Global Kit Styles",
  "type": "kit-styles",
  "version": "0.4",
  "page_settings": {},
  "content": [],
  "settings": {
    "system_colors": [
      { "_id": "primary",   "title": "Primary",   "color": "#005AFF" },
      { "_id": "secondary", "title": "Secondary",  "color": "#1A1A2E" },
      { "_id": "text",      "title": "Text",       "color": "#08091E" },
      { "_id": "accent",    "title": "Accent",     "color": "#00C87A" }
    ],
    "custom_colors": [
      { "_id": "c_bg_dark",  "title": "BG Dark",  "color": "#0A0D1A" },
      { "_id": "c_card",     "title": "Card",      "color": "#141628" },
      { "_id": "c_muted",    "title": "Muted",     "color": "#6B7280" },
      { "_id": "c_border",   "title": "Border",    "color": "#1A1D33" }
    ],
    "system_typography": [
      { "_id": "primary",   "title": "Primary",
        "typography_typography": "custom", "typography_font_family": "Inter",
        "typography_font_weight": "700", "typography_font_size": { "unit": "px", "size": 48 },
        "typography_line_height": { "unit": "em", "size": 1.15 },
        "typography_letter_spacing": { "unit": "px", "size": -1 } },
      { "_id": "secondary", "title": "Secondary",
        "typography_typography": "custom", "typography_font_family": "Inter",
        "typography_font_weight": "600", "typography_font_size": { "unit": "px", "size": 24 },
        "typography_line_height": { "unit": "em", "size": 1.3 } },
      { "_id": "text",      "title": "Text",
        "typography_typography": "custom", "typography_font_family": "Inter",
        "typography_font_weight": "400", "typography_font_size": { "unit": "px", "size": 16 },
        "typography_line_height": { "unit": "em", "size": 1.75 } },
      { "_id": "accent",    "title": "Accent",
        "typography_typography": "custom", "typography_font_family": "Inter",
        "typography_font_weight": "500", "typography_font_size": { "unit": "px", "size": 13 },
        "typography_letter_spacing": { "unit": "px", "size": 1 },
        "typography_text_transform": "uppercase" }
    ],
    "custom_typography": [],
    "default_generic_fonts": "Inter, sans-serif"
  }
}
```

---

## Output Checklist

- [ ] **ZERO html widgets for any visual content** — html = `<script>` JS only
- [ ] Nav links → `icon-list` or `button` widgets (NOT html)
- [ ] Badges/tags → `alert` or `button` (xs, pill) widgets (NOT html)
- [ ] Timeline entries → `heading` + `text-editor` + `button` widgets (NOT html)
- [ ] Contact panels → styled containers + `text-editor` + `button` widgets (NOT html)
- [ ] Pricing cards → `heading` + `icon-list` + `button` in styled container (NOT html)
- [ ] Zero JSON comments (`/* */` or `//`)
- [ ] Every element: unique 8-char hex `id`
- [ ] Every element: `"elements": []`
- [ ] Top-level containers: `"isInner": false`
- [ ] Nested containers: `"isInner": true`
- [ ] All colors: hex only (no CSS variable names, no color words)
- [ ] Placeholder images: `https://placehold.co/WxH/BGHEX/TEXTHEX?text=Label`
- [ ] Responsive: `_tablet` + `_mobile` suffixes on font sizes, padding, widths
- [ ] One `.json` per page
- [ ] `global-styles.json` with brand colors + fonts
- [ ] JSON envelope applied to every output file (version, title, type, content, page_settings, settings)
- [ ] Import method stated in response — default to Method 1 when unclear
- [ ] ⚠️ Pro-only features flagged (sticky, Theme Builder, custom CSS, scroll effects)

---

## Pro vs Free

```
⚠️ PRO ONLY:
  type: "header" / "footer" | custom_css per element | Scroll/Motion Effects
  Popup Builder | Form Widget | Sticky | Dynamic Tags

✅ FREE ALTERNATIVES:
  header/footer → container sections inside each page
  Forms → shortcode widget + WPForms or CF7
  Animations → Entrance Animations (free, Advanced tab)
```

---

## Reference Files

- `references/widget-map.md` — Full JSON schemas for all 22 native widgets + ACF CPT field sets
- `references/style-map.md` — CSS → Elementor JSON mappings (spacing, typography, backgrounds, overflow, position, overlay)
- `references/visual-analysis.md` — Color extraction, typography tree, layout detection for images/PDFs
- `references/section-patterns.md` — 15+ pre-built section JSON patterns using only native widgets

---

## About This Skill

**AK Elementor Studio** by **Abanoub Khalil** — Senior WordPress & Webflow Developer, Cairo, Egypt.
🌐 [akstudio.me](https://akstudio.me) · 💼 7+ years · Elementor Pro · Webflow · ACF · PHP · GSAP
🏢 InVitro Capital — AllCare.ai, AllRx.ai · 🔧 13+ live freelance projects, Egypt & MENA
