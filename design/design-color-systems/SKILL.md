---
type: Skill
name: design-color-systems
description: Produces accessible color palettes and CSS design-token implementations for brands and websites. Use when the task asks for "color palette", "brand colors", "color scheme", "WCAG contrast", "dark mode colors", "design tokens", or "CSS custom properties for colors". Covers color theory, WCAG 2.2 contrast compliance, dark mode, AI palette extraction, and color psychology.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# Color Systems

Use this skill when designing or reviewing color palettes, implementing them in code, or ensuring accessibility compliance.

## MCP Tool Discovery

The plugin provides visual analysis tools usable across agent contexts:

| Color Task | Tool Name Pattern |
|---|---|
| Extract palettes from images | `analyze_image` — query for dominant colors |
| Generate palette swatches | `nv_oos_*_agent_generate_gemini_image_validated` or bare |
| Web search for color trends | `nv_oos_*_agent_web_search_validated` or bare |
| Cross-site color sync | `remote_wp_connection` — push brand colors to spoke sites |

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for design workflows. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai health` | Verify tool and provider availability |
| `wp mcp-ai provider` | Check configured AI providers |

## When to use this skill

Trigger when ANY of the following is true:

- Creating a new color palette for a brand, website, or design project.
- Implementing color tokens / design tokens in CSS.
- Auditing color contrast for WCAG compliance.
- Adding dark mode or multiple theme support.
- Extracting colors from images or generating complementary palettes.
- The task mentions "color scheme", "palette", "brand colors", or "accessibility contrast".

## Color theory foundations

### Color relationships

```
Primary        → Main brand color (60% usage)
Secondary      → Complementary accent (30% usage)
Accent         → CTAs, highlights (10% usage)
Neutral        → Text, backgrounds, borders
Semantic       → Success (green), Error (red), Warning (amber), Info (blue)
```

### Palette types

| Type | Structure | Example |
|---|---|---|
| **Monochromatic** | One hue, varying saturation/lightness | Spotify green ecosystem |
| **Analogous** | 2-3 adjacent hues on color wheel | Calm, cohesive brands (wellness, nature) |
| **Complementary** | Opposite hues (blue + orange) | High contrast, energetic (sports, entertainment) |
| **Triadic** | 3 evenly spaced hues | Vibrant, balanced (education, family) |
| **Neutral + Pop** | Grays + one bold accent | Modern, sophisticated (tech, luxury) |

## WCAG contrast requirements

| Level | Normal Text | Large Text (18px+ bold or 24px+) | UI Components |
|---|---|---|---|
| **AA (minimum)** | 4.5:1 | 3:1 | 3:1 |
| **AAA (enhanced)** | 7:1 | 4.5:1 | 3:1 |

**Test contrast**: <https://webaim.org/resources/contrastchecker/>

### Common failing combinations

```
❌ #CCCCCC text on #FFFFFF — 1.6:1 (fail AA)
✅ #767676 text on #FFFFFF — 4.5:1 (pass AA)

❌ #999999 text on #FFFFFF — 2.85:1 (fail AA large text threshold)
✅ #595959 text on #FFFFFF — 7:1 (pass AAA)
```

## CSS custom properties implementation

### Design tokens

```css
:root {
  /* ── Brand palette ── */
  --color-primary:        #2563EB;
  --color-primary-light:  #3B82F6;
  --color-primary-dark:   #1D4ED8;

  --color-secondary:      #7C3AED;
  --color-accent:         #F59E0B;

  /* ── Neutrals ── */
  --color-neutral-50:     #FAFAFA;
  --color-neutral-100:    #F5F5F5;
  --color-neutral-200:    #E5E5E5;
  --color-neutral-300:    #D4D4D4;
  --color-neutral-400:    #A3A3A3;
  --color-neutral-500:    #737373;
  --color-neutral-600:    #525252;
  --color-neutral-700:    #404040;
  --color-neutral-800:    #262626;
  --color-neutral-900:    #171717;

  /* ── Semantic ── */
  --color-success:        #16A34A;
  --color-warning:        #D97706;
  --color-error:          #DC2626;
  --color-info:           #2563EB;

  /* ── Applied tokens ── */
  --color-text:           var(--color-neutral-900);
  --color-text-muted:     var(--color-neutral-500);
  --color-bg:             #FFFFFF;
  --color-bg-muted:       var(--color-neutral-50);
  --color-border:         var(--color-neutral-200);
}
```

### Dark mode

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-text:         var(--color-neutral-100);
    --color-text-muted:   var(--color-neutral-400);
    --color-bg:           var(--color-neutral-900);
    --color-bg-muted:     var(--color-neutral-800);
    --color-border:       var(--color-neutral-700);
  }
}

/* Manual toggle */
[data-theme="dark"] {
  --color-text:         var(--color-neutral-100);
  --color-bg:           var(--color-neutral-900);
  /* ... */
}
```

## AI-assisted palette work (MCP)

### Extract palette from an image

Use `analyze_image` (MCP) to identify dominant colors, color mood, and palette composition from any image:

```
analyze_image with prompt: "Extract the dominant color palette from this
image. List hex values for primary, secondary, accent, and neutral colors."
```

### Generate mood boards

Use the Gemini image tool in your tool list (agent-prefixed or bare) to create color palette swatches and mood boards:

```
prompt: "A warm, earthy brand palette for an organic coffee company —
         rich browns, cream, sage green accent, modern and minimal.
         Display as organized color swatches with hex labels."
```

## Color psychology quick reference

| Color | Associations | Best For |
|---|---|---|
| **Blue** | Trust, stability, professionalism | Finance, tech, healthcare |
| **Green** | Growth, nature, health | Wellness, environment, education |
| **Red** | Energy, urgency, passion | Food, entertainment, sales |
| **Purple** | Luxury, creativity, wisdom | Beauty, spirituality, premium |
| **Orange** | Friendly, confident, warm | E-commerce CTAs, youth brands |
| **Yellow** | Optimism, clarity, warmth | Children, creativity, warnings |
| **Black** | Sophistication, power, elegance | Luxury, fashion, tech |
| **White** | Clean, minimal, pure | Healthcare, minimalism, modern |

## Critical rules

- **60-30-10 rule** — 60% dominant (backgrounds), 30% secondary (UI elements), 10% accent (CTAs).
- **Test contrast for ALL text** — especially muted/secondary text, which often fails.
- **Don't rely on color alone** — use icons, underlines, or patterns for colorblind users.
- **Define neutral scale first** — a good gray scale (8–10 steps) is more important than brand colors.
- **Use HSL for programmatic manipulation** — `hsl(var(--hue), 80%, 50%)` makes theming trivial.
- **Extract palettes with AI** — use `analyze_image` (MCP) to pull color schemes from reference images.

## Common mistakes

```css
/* WRONG — hardcoded colors everywhere */
.button { background: #2563EB; color: white; }
.card { border: 1px solid #E5E5E5; background: white; }

/* RIGHT — design tokens */
.button { background: var(--color-primary); color: var(--color-bg); }
.card { border: 1px solid var(--color-border); background: var(--color-bg); }

/* WRONG — low contrast muted text */
.caption { color: #CCCCCC; } /* 1.6:1 on white — fails AA */

/* RIGHT — accessible muted text */
.caption { color: var(--color-text-muted); } /* from token system */
```

## What This Skill Does NOT Cover

- **Logo design and brand mark creation** — use **`design-brand-kit`**.
- **Font selection and typography pairing** — use **`design-typography`**.
- **Full brand guideline document generation** — use **`design-document-generation`**.
- **Image generation or editing** — use **`design-image-generation`**.
- **WordPress theme development or block styling** — use **`wp-plugin-architecture`**.
- **Social media content creation** — use **`design-social-content`**.
- **UI component library building (React/Vue components)** — this skill is CSS-focused; component frameworks are out of scope.

## Cross-references

- Run **`design-brand-kit`** to define the full brand identity including colors.
- Run **`design-typography`** to pair fonts with the color palette.
- Run **`design-image-generation`** to create visuals using the brand palette — check your tool list for the Gemini image tool.
- Run **`wp-plugin-options-storage`** to store color tokens in WordPress settings.
- Run **`mcp-ai-wpoos-plugin`** for `remote_wp_connection` — push color palettes from Hub to spoke sites.

## References

- WCAG 2.2 contrast: <https://www.w3.org/TR/WCAG22/#contrast-minimum>
- WebAIM contrast checker: <https://webaim.org/resources/contrastchecker/>
- Coolors palette generator: <https://coolors.co/>
- Adobe Color: <https://color.adobe.com/>
- OKLCH color space (modern CSS): <https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch>
