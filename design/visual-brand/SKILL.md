---
name: visual-brand
description: Extract brand visual system from a website or brand assets into a structured style guide
tags: [brand, design, visual-identity, style-guide, creative]
---

# Visual Brand Extractor

Analyzes a website or brand assets to extract the complete visual identity system. Identifies colors, typography, logo usage, photography style, icon language, spacing patterns, and UI component styles. Outputs a structured brand style guide JSON that other creative skills (`ad-creative-brief`, `slide-creator`, `landing-page-copy`) can consume for brand-consistent output.

## Prerequisites

- `agency.config.json` in the project root
- Target website URL or set of brand asset files (logos, screenshots, PDFs)
- Browser automation access (Claude-in-Chrome MCP) for live site analysis
- Optional: existing brand guidelines document for validation

## Phase 0: Intake

1. Read `agency.config.json` from the project root.
2. Extract `agency.name`, `agency.domain` for context on whether this is self-analysis or client analysis.
3. Extract `services[]` to understand what brand contexts are relevant (e.g., Shopify themes, landing pages).
4. Collect inputs from the user:
   - **Target**: website URL, or list of asset file paths
   - **Scope**: full brand audit, or specific elements only (colors, fonts, etc.)
   - **Context**: is this for a client project, competitor analysis, or internal use?

## Phase 1: Color Extraction

Analyze the target for all color usage:

**Primary colors:**
- Identify the dominant brand color (used in CTAs, headers, logo)
- Extract exact hex, RGB, and HSL values

**Secondary colors:**
- Supporting palette colors (used in backgrounds, accents, hover states)
- Extract all values

**Neutral palette:**
- Background colors (white, off-white, grays)
- Text colors (body text, headings, muted text)
- Border and divider colors

**Semantic colors:**
- Success, error, warning, info colors if present
- Sale/discount highlight colors

**Color relationships:**
```
COLOR PALETTE:
---
Primary:     #XXXXXX (rgb) -- usage: CTAs, headers, logo
Secondary:   #XXXXXX (rgb) -- usage: accents, hover states
Accent:      #XXXXXX (rgb) -- usage: highlights, badges

Neutrals:
- Background: #XXXXXX
- Surface:    #XXXXXX
- Border:     #XXXXXX
- Text:       #XXXXXX
- Muted:      #XXXXXX

Semantic:
- Success:    #XXXXXX
- Error:      #XXXXXX
- Warning:    #XXXXXX
```

Verify contrast ratios between text and background colors meet WCAG AA (4.5:1 for body text, 3:1 for large text). Flag any violations.

## Phase 2: Typography Analysis

Extract the complete type system:

**Font families:**
- Heading font: family name, weight(s), source (Google Fonts, Adobe, custom)
- Body font: family name, weight(s), source
- Accent/display font if used
- Monospace font if present (code blocks, pricing)

**Type scale:**
```
TYPOGRAPHY:
---
Heading font: [Family] -- weights: [300, 400, 700]
Body font:    [Family] -- weights: [400, 500, 600]

Scale:
- H1: [size]px / [line-height] / [weight] / [letter-spacing]
- H2: [size]px / [line-height] / [weight] / [letter-spacing]
- H3: [size]px / [line-height] / [weight] / [letter-spacing]
- H4: [size]px / [line-height] / [weight] / [letter-spacing]
- Body: [size]px / [line-height] / [weight]
- Small: [size]px / [line-height] / [weight]
- Caption: [size]px / [line-height] / [weight]

Mobile overrides:
- H1: [size]px
- H2: [size]px
- Body: [size]px
```

**Text styling patterns:**
- Uppercase usage (headings, labels, navigation)
- Letter-spacing patterns
- Text decoration (underlines on links, strikethroughs on prices)

## Phase 3: Logo and Imagery

**Logo analysis:**
```
LOGO:
---
Type: [wordmark / lettermark / icon+wordmark / abstract / mascot]
Orientation: [horizontal / vertical / icon-only variant]
Colors: [list of colors used]
Clear space: [approximate padding around logo]
Min size: [smallest observed usage]
Background usage: [light bg only / dark bg only / both with variants]
```

**Photography style:**
- Subject matter (lifestyle, product-only, people, abstract)
- Color treatment (vibrant, muted, desaturated, warm, cool)
- Composition patterns (centered, rule-of-thirds, overhead, close-up)
- Background style (solid, gradient, environmental, transparent)

**Illustration and icon style:**
- Icon type (outlined, filled, duotone, hand-drawn)
- Icon weight (thin, regular, bold)
- Corner style (rounded, sharp)
- Color application (mono, brand-colored, multi-color)
- Source library if identifiable (Heroicons, Feather, Phosphor, custom)

## Phase 4: Spacing and Layout

**Spacing system:**
```
SPACING:
---
Base unit: [4px / 8px]
Scale: [4, 8, 12, 16, 24, 32, 48, 64, 96, 128]

Section padding: [top/bottom]
Container max-width: [px]
Grid columns: [12 / flexible]
Gutter width: [px]
Card padding: [px]
Button padding: [vertical horizontal]
Input padding: [vertical horizontal]
```

**Component patterns:**
- Border radius (none, small, medium, large, full)
- Shadow styles (none, subtle, medium, elevated)
- Divider style (line, space, gradient)

## Phase 5: UI Component Audit

Catalog key component styles:

**Buttons:**
```
BUTTONS:
- Primary: [bg color, text color, border-radius, padding, font-weight, hover state]
- Secondary: [outline/ghost style details]
- Tertiary: [text-only link style]
- Size variants: [sm, md, lg if present]
```

**Cards:**
- Border vs shadow vs flat
- Image placement (top, left, background)
- Content padding
- Hover behavior

**Navigation:**
- Style (horizontal, hamburger, sidebar)
- Active state treatment
- Dropdown style

**Forms:**
- Input border style
- Focus state color
- Label placement (above, inline, floating)
- Error state style

## Phase 6: Output

Return the complete brand style guide as structured JSON:

```json
{
  "brand_style_guide": {
    "target": "[URL or asset source]",
    "extracted_date": "[ISO date]",
    "colors": {
      "primary": { "hex": "#XXXXXX", "rgb": "r,g,b", "usage": "description" },
      "secondary": { "hex": "#XXXXXX", "rgb": "r,g,b", "usage": "description" },
      "accent": { "hex": "#XXXXXX", "rgb": "r,g,b", "usage": "description" },
      "neutrals": {
        "background": "#XXXXXX",
        "surface": "#XXXXXX",
        "border": "#XXXXXX",
        "text": "#XXXXXX",
        "muted": "#XXXXXX"
      },
      "semantic": {
        "success": "#XXXXXX",
        "error": "#XXXXXX",
        "warning": "#XXXXXX"
      },
      "contrast_issues": []
    },
    "typography": {
      "heading_font": { "family": "", "weights": [], "source": "" },
      "body_font": { "family": "", "weights": [], "source": "" },
      "scale": {
        "h1": { "size": "", "line_height": "", "weight": "", "letter_spacing": "" },
        "h2": { "size": "", "line_height": "", "weight": "", "letter_spacing": "" },
        "h3": { "size": "", "line_height": "", "weight": "", "letter_spacing": "" },
        "body": { "size": "", "line_height": "", "weight": "" },
        "small": { "size": "", "line_height": "", "weight": "" }
      }
    },
    "logo": {
      "type": "",
      "orientations": [],
      "colors": [],
      "clear_space": "",
      "min_size": "",
      "background_usage": ""
    },
    "imagery": {
      "photography_style": "",
      "color_treatment": "",
      "composition": "",
      "icon_style": "",
      "icon_source": ""
    },
    "spacing": {
      "base_unit": "",
      "scale": [],
      "section_padding": "",
      "container_max_width": "",
      "grid_columns": "",
      "border_radius": "",
      "shadow_style": ""
    },
    "components": {
      "buttons": {},
      "cards": {},
      "navigation": {},
      "forms": {}
    }
  }
}
```

Also provide a human-readable summary:
```
BRAND STYLE GUIDE SUMMARY -- [Target]
---
Visual personality: [2-3 adjective description, e.g. "clean, modern, premium"]
Primary brand color: [hex] ([color name])
Heading font: [family]
Body font: [family]
Overall feel: [1 sentence description]
Notable patterns: [key observations]
Accessibility: [pass/fail + issues]
```

## Example Usage

**Trigger phrases:**
- "Extract the brand style from kibisports.com"
- "Analyze this website's visual identity"
- "Build a brand style guide from these assets"
- "What fonts and colors does this brand use?"
- "Create a visual system document for this client"

```
User: Extract the visual brand from shop.kibisports.com
Assistant: [navigates to site, captures color palette, fonts, spacing, component styles, outputs brand_style_guide JSON]
```

```
User: I need the brand colors and fonts for a client pitch
Assistant: [requests URL or assets, analyzes visual system, outputs structured guide focused on colors and typography]
```
