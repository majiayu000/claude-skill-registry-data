---
type: Skill
name: design-brand-kit
description: Produces complete brand identity systems — logos (AI-generated via Gemini), color palettes, typography, imagery guidelines, and WordPress-based brand asset libraries. Use when the task asks for "brand kit", "logo design", "brand guidelines", "brand identity", "visual identity", "brand colors", or "brand assets". Covers AI-assisted logo generation, asset sizing, brand archetypes, and WordPress brand page structure.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Brand Kit Design

Use this skill when creating or updating a brand identity system, including logos, colors, typography, and brand guidelines.

## MCP Bridge First

**This skill assumes you are using the MCP bridge.** For brand asset creation, use these MCP tools:

| MCP Tool | Brand Kit Use |
|---|---|
| `generate_gemini_image_validated` | Generate logo concepts, brand imagery, mood boards |
| `resize_image` | Create favicon, social avatar, and other size variants from logos |
| `remove_background` | Make logo backgrounds transparent for overlays |
| `generate_image_alt_text_validated` | Add accessible alt text to brand assets |
| `analyze_image` | Analyze existing logos for color extraction, style analysis |

For providers beyond Gemini (DALL·E, Midjourney, Ideogram for text-in-logo), use the media worker (`http://localhost:3100/api/image/generate`) as fallback.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for brand asset workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai provider` | List configured AI image providers |
| `wp mcp-ai credential` | Manage API keys for image generation |
| `wp mcp-ai health` | Verify image generation tools are available |

## When to use this skill

Trigger when ANY of the following is true:

- Creating a new brand identity from scratch.
- Generating logo concepts or variations.
- Defining brand guidelines (colors, fonts, imagery, tone-of-voice).
- Setting up a brand asset library in WordPress.
- The task mentions "brand kit", "brand identity", "brand guidelines", or "logo design".
- Generating brand assets for social media or marketing.

## Brand kit anatomy

A complete brand kit contains:

```
Brand Kit
├── Strategy
│   ├── Brand positioning
│   ├── Target audience personas
│   ├── Brand personality & voice
│   └── Key messaging
├── Visual Identity
│   ├── Logo (primary, secondary, icon, wordmark)
│   ├── Color palette (primary, secondary, neutral, semantic)
│   ├── Typography (heading, body, accent fonts)
│   └── Imagery style (photography, illustration, iconography)
├── Applications
│   ├── Business card / stationery
│   ├── Social media templates
│   ├── Presentation deck
│   ├── Email signature
│   └── Website style guide
└── Guidelines
    ├── Usage rules (clear space, minimum size, don'ts)
    ├── File formats (SVG → vector, PNG → raster, PDF → print)
    └── Accessibility notes
```

## Logo generation with AI

### Via MCP (Gemini — Primary)

Use the Gemini image tool available in your tool list (agent-prefixed or bare)
for fast, high-quality logo concepts:

```
prompt: "Minimalist geometric lettermark logo for a fintech startup called
'NeoBank', deep navy and mint green palette, clean lines, negative space,
professional and trustworthy, vector style on white background"

model: "gemini-3.1-flash-image"
aspect_ratio: "1:1"
output_format: "svg"     ← Vectorize for scalability
```

**Tip:** Use `output_format: "svg"` to vectorize the raster output — ideal for logos that need to scale.

### Via media worker (DALL·E, Midjourney, Ideogram — Fallback)

```
POST /api/image/generate
{
  "model": "dall-e-3",
  "prompt": "Minimalist geometric fox head logo, gold and navy, clean lines,
             vector style on white background",
  "size": "1024x1024",
  "style": "natural"
}
```

For logos with embedded text, Ideogram v2 (via media worker) produces the best text rendering.

### Prompt structure for logo concepts

```
Style: [minimalist / vintage / geometric / hand-drawn / abstract]
Type: [wordmark / lettermark / icon / combination / emblem]
Industry: [tech / fashion / food / finance / creative agency]
Colors: [primary + accent palette]
Vibe: [modern / luxury / playful / trustworthy / bold]
```

### Logo variations to generate

```
1. Primary logo (full color, light background)
2. Reversed logo (white/light, dark background)
3. Icon only (favicon, app icon, social avatar)
4. Wordmark only (horizontal text lockup)
5. Monochrome (single color for watermarks)
6. Responsive (simplified for small sizes)
```

After generating the primary logo with `generate_gemini_image_validated`:

1. Use `remove_background` (MCP) to make it transparent.
2. Use `resize_image` (MCP) to create each size variant:
   - Favicon: `width: 32, height: 32, crop: true`
   - Social avatar: `width: 400, height: 400, crop: true`
   - Social header: `width: 1500, height: 500, crop: true`

### Brand asset sizing via MCP

Use `resize_image` for every size variant:

```
Favicon:      width: 32,  height: 32,  crop: true
App icon:     width: 180, height: 180, crop: true
Social avatar: width: 400, height: 400, crop: true
og:image:     width: 1200, height: 630, crop: true
Banner:       width: 1500, height: 500, crop: true
```

## WordPress brand page structure

```php
// Create a "Brand Kit" page with structured content
$brand_page = [
    'post_title'   => 'Brand Kit',
    'post_type'    => 'page',
    'post_status'  => 'publish',
    'post_content' => '<!-- wp:group -->...<!-- /wp:group -->',
    'meta_input'   => [
        '_brand_primary_color'   => '#2563EB',
        '_brand_secondary_color' => '#7C3AED',
        '_brand_font_heading'    => 'Fraunces',
        '_brand_font_body'       => 'Inter',
        '_brand_logo_id'         => $logo_attachment_id,
    ],
];
```

## Brand asset formats

| Asset | Format | Size | How to create |
|---|---|---|---|
| **Logo (print)** | SVG, EPS, PDF | Vector (infinite) | Gemini with `output_format: "svg"` |
| **Logo (web)** | SVG, PNG | 500×500px | `resize_image` (MCP) from generated logo |
| **Favicon** | ICO, PNG, SVG | 32×32, 180×180 | `resize_image` (MCP) |
| **Social avatar** | PNG, JPG | 400×400 | `resize_image` (MCP) |
| **Social header** | PNG, JPG | 1500×500 | `resize_image` (MCP) |
| **og:image** | PNG, JPG | 1200×630 | `resize_image` (MCP) |
| **Watermark** | PNG (transparent) | 500×500 | `remove_background` + `resize_image` (MCP) |

## Brand archetypes

| Archetype | Traits | Colors | Fonts | Example |
|---|---|---|---|---|
| **The Creator** | Imaginative, innovative | Bold, vibrant | Display, artistic | Adobe, Lego |
| **The Sage** | Wise, knowledgeable | Muted, earthy | Serif, classic | National Geographic |
| **The Hero** | Strong, confident | Bold, red/black | Sans-serif, heavy | Nike, Under Armour |
| **The Explorer** | Adventurous, free | Earth tones, blue | Hand-drawn, rustic | Jeep, Patagonia |
| **The Lover** | Passionate, sensual | Rich, warm | Script, elegant | Chanel, Häagen-Dazs |
| **The Jester** | Playful, fun | Bright, contrasting | Rounded, bubbly | M&M's, Old Spice |
| **The Everyman** | Reliable, down-to-earth | Neutral, blues | Sans-serif, clean | IKEA, Target |

## Generating brand assets: MCP-first pipeline

```
Step 1: Generate logo concept → generate_gemini_image_validated (MCP)
        output_format: "svg", aspect_ratio: "1:1"

Step 2: Remove background if needed → remove_background (MCP)
        method: "auto"

Step 3: Create all size variants → resize_image (MCP)
        Run for each: favicon, avatar, banner, og:image, etc.

Step 4: Generate alt text → generate_image_alt_text_validated (MCP)

Step 5: (Optional) Convert to WebP → media worker /api/image/optimize
        For web-optimized formats not yet covered by MCP tools
```

## Critical rules

- **Vector first** — logos should ALWAYS be designed as vectors. Use Gemini's `output_format: "svg"` to vectorize.
- **MCP for sizing** — use `resize_image` for all logo size variants (favicon, avatar, banner).
- **Responsive logos** — have a simplified version for small sizes.
- **Clear space** — define minimum padding around the logo (usually = height of the logo's first letter).
- **Never stretch or distort** — always scale proportionally. Lock aspect ratio.
- **Consistent asset naming** — `brand-logo-primary.svg`, `brand-logo-white.svg`, `brand-icon.svg`. Not `final-logo-v3-FINAL.svg`.
- **Color values in multiple formats** — provide HEX (#2563EB), RGB (37,99,235), CMYK (85,60,0,0), and PMS for print.

## Common mistakes

```
WRONG:
- Using the primary logo at 16×16px for a favicon (unreadable)
- JPEG logo on a non-white background (no transparency)
- Different logo versions on different platforms (consistency)
- No clear-space rules (logo gets crowded by other elements)

RIGHT:
- Separate icon mark for favicon/small uses
- SVG with transparent background for web
- Single source of truth for all brand assets (WordPress Brand Kit page)
- Published brand guidelines document with do's and don'ts
```

## What This Skill Does NOT Cover

- **Color palette generation and WCAG contrast checking** — use **`design-color-systems`**.
- **Font pairing and web font loading strategies** — use **`design-typography`**.
- **Generating social media content using the brand** — use **`design-social-content`**.
- **Image optimization (WebP, AVIF, compression)** — use **`design-image-optimization`**.
- **Video creation for brand marketing** — use **`design-video-creation`**.
- **SEO optimization of brand pages** — use **`design-seo-content`**.
- **Document generation for brand guidelines** — use **`design-document-generation`**.

## Cross-references

- Run **`design-color-systems`** to build the brand color palette.
- Run **`design-typography`** to select and pair brand fonts.
- Run **`design-image-generation`** for AI-assisted logo and asset creation.
- Run **`design-social-content`** to define brand voice and messaging.
- Use **`paper_store_*`** tools with `connection_id` to persist brand guidelines to specific spoke sites.

## References

- Brand archetypes: <https://iconicfox.com.au/brand-archetypes/>
- Logo file format guide: <https://99designs.com/blog/tips/logo-file-formats/>
- Brand guidelines examples: <https://www.canva.com/learn/brand-guidelines/>
- WordPress Brand Kit plugin concept: custom post type + meta fields
