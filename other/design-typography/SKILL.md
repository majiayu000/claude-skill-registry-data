---
type: Skill
name: design-typography
description: Design and implement typography systems for web and brand projects. Covers font pairing, type scales, variable fonts, web font loading strategies (font-display, subsetting), CSS typography best practices, and WordPress theme typography integration. Use when selecting fonts, building type scales, loading web fonts, configuring theme.json typography, or fixing font performance issues.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Typography Systems

Use this skill when designing or implementing typography for brands, websites, or design projects.

> **Note:** Typography is primarily a design-theory and CSS-implementation skill.
> MCP tools support the visual side — use the Gemini image tool in your tool list
> (agent-prefixed or bare) to create typographic posters and mood boards, and
> `analyze_image` to identify fonts from screenshots. For cross-site font
> management, use `remote_wp_connection` to push typography settings from Hub to
> spoke sites.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for design workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai health` | Verify tool and provider availability |
| `wp mcp-ai provider` | Check configured AI providers |

## When to use this skill

Trigger when ANY of the following is true:

- Selecting or pairing fonts for a brand or website.
- Implementing a type scale in CSS.
- Loading web fonts with optimal performance.
- Working with variable fonts.
- The task mentions "font", "typography", "type scale", "heading styles", or "font pairing".
- Configuring WordPress theme typography (theme.json or customizer).

## Font pairing principles

### Contrast with harmony

```
Pair fonts that differ in ONE key dimension while sharing others:

Display (headlines)  +  Body (paragraphs)
─────────────────────────────────────────
Serif                +  Sans-serif          ← Classic pairing
Sans-serif           +  Serif               ← Modern, clean
Geometric sans       +  Grotesk sans        ← Subtle contrast
Script/display       +  Simple sans         ← Statement + readability
Monospace            +  Proportional         ← Code/tech aesthetic
```

### Proven pairings

| Headings | Body | Vibe |
|---|---|---|
| **Playfair Display** | **Source Sans 3** | Editorial, elegant |
| **DM Serif Display** | **DM Sans** | Modern luxury |
| **Bebas Neue** | **Roboto** | Bold, urban |
| **Cormorant Garamond** | **Proza Libre** | Literary, classic |
| **Inter** | **Inter** (single family) | Clean, tech |
| **Space Grotesk** | **Space Grotesk** | Contemporary |
| **Fraunces** | **Commissioner** | Creative, warm |
| **Cabinet Grotesk** | **Satoshi** | Modern brand |

## Type scales

### Major Third (1.250) — most common

```css
:root {
  --text-xs:     0.75rem;   /* 12px */
  --text-sm:     0.875rem;  /* 14px */
  --text-base:   1rem;      /* 16px */
  --text-lg:     1.125rem;  /* 18px */
  --text-xl:     1.25rem;   /* 20px */
  --text-2xl:    1.5rem;    /* 24px */
  --text-3xl:    1.875rem;  /* 30px */
  --text-4xl:    2.25rem;   /* 36px */
  --text-5xl:    3rem;      /* 48px */
  --text-6xl:    3.75rem;   /* 60px */
}
```

### Perfect Fourth (1.333) — dramatic, editorial

```css
:root {
  --text-base:   1rem;      /* 16px */
  --text-lg:     1.333rem;  /* 21px */
  --text-xl:     1.777rem;  /* 28px */
  --text-2xl:    2.369rem;  /* 38px */
  --text-3xl:    3.157rem;  /* 51px */
  --text-4xl:    4.209rem;  /* 67px */
}
```

### Fluid type (clamp)

```css
/* Scales smoothly between mobile and desktop without breakpoints */
h1 {
  font-size: clamp(2rem, 1rem + 5vw, 4rem);
}

h2 {
  font-size: clamp(1.5rem, 0.8rem + 3vw, 2.5rem);
}

body {
  font-size: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
}
```

## Web font loading

### Font face declaration

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;         /* Critical for performance */
  unicode-range: U+0000-00FF; /* Subset to Latin if applicable */
}
```

### font-display strategies

| Value | Behavior | Best For |
|---|---|---|
| **swap** | Show fallback immediately, swap when loaded | Body text, UI (no FOIT) |
| **block** | Invisible for 3s, then fallback | Minimal — avoid |
| **fallback** | Invisible for 100ms, then fallback | Headings (brief FOIT ok) |
| **optional** | Use fallback if font isn't cached | Non-critical text, perf-first |

**Golden rule**: `font-display: swap` for body text. Only use `optional` for truly non-essential decorative fonts.

### Performance checklist

```
✅ Use WOFF2 format (30% smaller than WOFF)
✅ Subset to needed characters (Latin, no Cyrillic if not needed)
✅ Preload critical fonts: <link rel="preload" as="font" crossorigin />
✅ Self-host fonts (no Google Fonts CDN for privacy + performance)
✅ Use variable fonts (one file instead of 4–6 weights)
✅ Cache fonts with long max-age (1 year)
```

## Variable fonts

```css
@font-face {
  font-family: 'InterVariable';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-stretch: 75% 125%;
  font-style: oblique 0deg 12deg;
}

h1 {
  font-family: 'InterVariable', sans-serif;
  font-weight: 800;
  font-variation-settings: 'opsz' 32; /* Optical size for large text */
}

.caption {
  font-family: 'InterVariable', sans-serif;
  font-weight: 400;
  font-variation-settings: 'opsz' 12; /* Optical size for small text */
}
```

### Popular variable fonts (all on Google Fonts)

```
Inter            → UI, body, general purpose
Fraunces         → Editorial, brand, display
Recursive        → Mono to sans axis, playful
Newsreader       → Long-form reading, news
Roboto Flex      → Full axis range, highly customizable
Source Serif 4   → Body copy, reading comfort
```

## WordPress typography (theme.json)

```json
{
  "settings": {
    "typography": {
      "fontFamilies": [
        {
          "fontFamily": "'InterVariable', sans-serif",
          "name": "Inter",
          "slug": "inter"
        },
        {
          "fontFamily": "'FrauncesVariable', serif",
          "name": "Fraunces",
          "slug": "fraunces"
        }
      ],
      "fontSizes": [
        { "name": "Small", "slug": "small", "size": "0.875rem" },
        { "name": "Base", "slug": "base", "size": "1rem" },
        { "name": "Large", "slug": "large", "size": "1.25rem" },
        { "name": "XL", "slug": "xl", "size": "1.5rem" },
        { "name": "2XL", "slug": "2-xl", "size": "2rem" },
        { "name": "3XL", "slug": "3-xl", "size": "3rem" }
      ]
    }
  }
}
```

## Typography visualization with AI (MCP)

While typography implementation is CSS-driven, MCP tools can help visualize type choices:

- **Generate type specimen posters:** Use the Gemini image tool in your tool list to create posters showing font pairings in context.
- **Analyze font usage:** Use `analyze_image` to identify fonts in screenshots or reference images.
- **Create mood boards:** Use the Gemini image tool in your tool list to generate typographic mood boards showing text hierarchy examples.

```
# Generate a type specimen for a font pairing
prompt: "Typography specimen poster showing 'Playfair Display' for headings
and 'Source Sans 3' for body text. Include sample headings, paragraph text,
and pull quotes. Elegant editorial layout, black text on cream background."
```

## What This Skill Does NOT Cover

- Color system design and palette generation → `design-color-systems`
- Full brand identity definition (logos, imagery, voice) → `design-brand-kit`
- Logo design, mark creation, or iconography
- Layout and grid system design (CSS Grid, Flexbox patterns)
- Icon font selection and icon-set curation
- Print typography specifications (ink traps, paper stock, imposition)
- Font licensing and commercial usage rights

## Critical rules

- **Maximum 2 font families** — one for headings, one for body. Three is pushing it; more is a mess.
- **Line-height: 1.5–1.75 for body** — tighter for headings (1.1–1.3), looser for long-form reading.
- **Max line length: 60–75 characters** — use `max-width: 65ch` on text containers.
- **Use relative units** — `rem` for font-size, `em` for spacing within components, avoid `px`.
- **Optical sizing matters** — variable fonts with `opsz` axis improve readability at small sizes and elegance at large sizes.

## Common mistakes

```css
/* WRONG — px-based, no fallback, multiple families */
body { font-size: 16px; font-family: 'Playfair Display', 'Lato', 'Open Sans', serif; }

/* RIGHT — rem-based, 2-family max, system fallback */
body { font-size: 1rem; font-family: 'InterVariable', -apple-system, BlinkMacSystemFont, sans-serif; }
h1, h2, h3 { font-family: 'FrauncesVariable', Georgia, serif; }

/* WRONG — no fluid scaling */
h1 { font-size: 48px; } /* giant on mobile */

/* RIGHT — fluid clamp */
h1 { font-size: clamp(2rem, 1rem + 5vw, 3.75rem); }
```

## Cross-references

- Run **`design-color-systems`** to pair colors with typography choices.
- Run **`design-brand-kit`** to define the full brand identity.
- Run **`wp-plugin-assets-loading`** to properly enqueue web fonts in WordPress.
- Run **`design-image-generation`** to create typographic visuals — check your tool list for the Gemini image tool.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` — push typography config from Hub to spoke sites.

## References

- Google Fonts variable fonts: <https://fonts.google.com/variablefonts>
- Fontpair: <https://www.fontpair.co/>
- Modern fluid typography: <https://utopia.fyi/>
- Web font loading best practices: <https://web.dev/font-best-practices/>
- Variable fonts guide: <https://variablefonts.io/>
