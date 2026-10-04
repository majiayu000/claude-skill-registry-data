---
name: brand-tokens
description: "Manzanita Research visual identity tokens — colors, typography, and texture direction. Apply these whenever building any visual interface (web, terminal, print, slides) for a Manzanita project. Other design skills (frontend-design, tui-design) reference this as their brand layer. Use this skill when you need the specific color values, font settings, or visual identity rules for Manzanita Research, even if you're not using one of the design skills."
license: Complete terms in LICENSE.txt
---

# Manzanita Research — Visual Identity Tokens

This is the single source of truth for Manzanita's visual identity. Colors, typography, and texture direction live here. Design skills (frontend-design, tui-design) reference this file for brand-specific values — the craft guidance lives in those skills, not here.

## The Manzanita Look

Whole Earth Catalog meets Laurel Canyon. Analog warmth in digital spaces. Sun-faded, textured, unhurried. Like a workshop with good light and interesting tools on the walls.

**What it is:** Warm, editorial, handmade-feeling. Film stock over digital. Dense information presented with care. Calm confidence.

**What it is not:** Startup templates. Purple gradients. Glassmorphism. Neon accents. Pure black-on-white. Rainbow ANSI vomit. Anything built to impress in a demo GIF rather than to use every day.

## Color Palette

These are the canonical Manzanita colors. Use the semantic names, not raw hex — it makes intent clear.

| Token          | Hex       | Role                                           |
| -------------- | --------- | ---------------------------------------------- |
| cream          | `#FAF9F6` | Page backgrounds, canvas                       |
| warm-black     | `#2C2C2C` | Primary text                                   |
| bark           | `#6B3A2A` | Deep accent, manzanita bark. Borders, emphasis |
| terracotta     | `#C2714F` | Primary warm accent. CTAs, active states       |
| sage           | `#8B9E7E` | Success, healthy, linked, good states          |
| ochre          | `#C49A3C` | Highlights, warnings, gold accent              |
| rust           | `#A0522D` | Tertiary accent, error states                  |
| lavender-dried | `#9B8EA8` | Subtle accent, tags, metadata                  |
| fog            | `#E8E5DF` | Borders, dividers, subtle separators           |
| dusk           | `#5C5C5C` | Muted/secondary text                           |

### Color rules

- **Use color sparingly.** Most of the interface should be cream, warm-black, fog, and dusk. Color draws attention — use it where attention belongs.
- **Status uses the landscape palette:** sage for good, ochre for caution, rust for problems, terracotta for active/selected. These map to natural states (green growth, golden warning, red-brown danger) without the aggressive pure-red/green/blue of most UIs.
- **Never use pure red, green, or blue.** Everything is warm and muted.
- **Respect system preferences.** Support `prefers-color-scheme` on web, `NO_COLOR` in terminals. The palette works on both light and dark backgrounds — on dark, swap cream and warm-black roles.

### Tailwind config (web)

```js
colors: {
  cream: '#FAF9F6',
  'warm-black': '#2C2C2C',
  bark: '#6B3A2A',
  terracotta: '#C2714F',
  sage: '#8B9E7E',
  ochre: '#C49A3C',
  rust: '#A0522D',
  'lavender-dried': '#9B8EA8',
  fog: '#E8E5DF',
  dusk: '#5C5C5C',
}
```

### Lip Gloss constants (terminal)

```go
const (
    colorCream      = lipgloss.Color("#FAF9F6")
    colorWarmBlack  = lipgloss.Color("#2C2C2C")
    colorBark       = lipgloss.Color("#6B3A2A")
    colorTerracotta = lipgloss.Color("#C2714F")
    colorSage       = lipgloss.Color("#8B9E7E")
    colorOchre      = lipgloss.Color("#C49A3C")
    colorRust       = lipgloss.Color("#A0522D")
    colorLavender   = lipgloss.Color("#9B8EA8")
    colorFog        = lipgloss.Color("#E8E5DF")
    colorDusk       = lipgloss.Color("#5C5C5C")
)
```

## Typography

Three typefaces. Each has a specific job.

### Display: Fraunces

Variable font from Google Fonts. Warm, expressive, slightly wonky — the brand voice in type.

**Critical settings — always apply both:**

```css
font-variation-settings:
  "WONK" 1,
  "SOFT" 100;
```

Never use Fraunces without wonk and full soft. Without these it looks like a different font entirely.

**Loading from Google Fonts** (include all variable axes):

```
family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,100..900,0..100,0..1;1,9..144,100..900,0..100,0..1
```

Optical sizing (`opsz`) is automatic — don't set it manually.

**Use for:** Headlines, hero text, feature titles, anything that needs personality. Set large, with negative letter-spacing (`-0.02em`) and tight line-height (`1.1`).

### Body: Literata

Warm, bookish variable serif. Designed for long reading — looks best at 16px. Load weights 400 and 600 from Google Fonts.

**Alternatives** (if Literata isn't available): Lora, Crimson Pro, Libre Baskerville. All are warm serifs that pair well with Fraunces.

**Use for:** Body text, documentation, long-form reading. Set at `font-size: 16px` with generous line-height (`1.7`–`1.8`), comfortable measure (`max-width: 38rem`), and `text-wrap: pretty` where supported.

### Monospace: Commit Mono

Custom Manzanita build, self-hosted from `org/fonts/CommitMono-Variable.woff2`.

**OpenType features — always enable:**

```css
font-feature-settings:
  "cv01" 1,
  "cv03" 1,
  "cv04" 1,
  "cv06" 1,
  "cv11" 1,
  "ss01" 1,
  "ss02" 1,
  "ss03" 1,
  "ss04" 1,
  "ss05" 1;
```

**Use for:** Code blocks, UI labels in tool interfaces, terminal output, data tables. Anywhere precision matters.

### Fonts to avoid

Never use as primary typefaces: Inter, Roboto, Arial, Space Grotesk, Poppins, Geist Mono, system defaults. These are fine fonts — they're just not Manzanita. The whole point of the type system is warmth and character over geometric neutrality.

## Texture & Atmosphere

The Manzanita look has physical presence. It shouldn't feel like a flat digital surface.

- **Film grain overlays:** Subtle noise at 0.03–0.08 opacity. Adds warmth and breaks up flat color fields. On web, use a CSS pseudo-element or SVG filter. In image prompts, specify film stock.
- **Warm gradients:** Cream to fog, terracotta to rust. Always warm-to-warm, never cool tones.
- **Material surfaces:** Paper-like textures on containers. Slight off-white variation rather than perfectly uniform backgrounds.
- **Warm-tinted shadows:** Never pure black shadows. Use warm-black at low opacity, or bark-tinted shadows for colored elements.
- **Photography feel:** Candid, natural-light, slightly grainy. Film stock over digital. If generating images, specify: "Kodak Eastman 100T 5247 35mm film, grain, halation, faded warm colors."

## When to Use This Skill

This skill provides the raw tokens. How to apply them depends on the medium:

- **Building a web interface?** Use this + the `frontend-design` skill (React + Tailwind craft guidance)
- **Building a terminal UI?** Use this + the `tui-design` skill (Go + Bubble Tea craft guidance)
- **Writing copy?** Use the `brand-voice` skill instead — that's about language, not visuals
- **Generating images?** Use the `generate-hero-prompt` skill — it has its own visual language built in
- **Just need the hex codes or font names?** This skill is all you need
