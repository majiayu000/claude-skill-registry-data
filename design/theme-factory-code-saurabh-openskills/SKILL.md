---
name: theme-factory
description: Generate and apply complete design themes — color palettes, typography pairings, and spacing systems — to any artifact. Use when the user wants to style a presentation, document, landing page, dashboard, or UI component with a cohesive visual theme, pick from pre-built themes, or generate a custom theme from a brief description. Trigger on "apply a theme", "make it look professional", "give it a style", "dark theme", "minimal theme", or any request to establish a visual direction.
---

# Theme Factory

A theme is a complete, internally consistent visual system: colors that work together, fonts that complement each other, and spacing that creates rhythm. A half-applied theme looks worse than no theme. Commit fully or stay plain.

This skill generates production-ready theme definitions and applies them consistently across any artifact — slides, HTML, CSS, documents, or components.

---

## Theme Factory Principles

- **A theme is a system, not a mood board.** It must define every visual decision — colors for every state, font for every level of hierarchy, spacing for every gap. Gaps in the system become inconsistencies in the output.
- **Contrast is non-negotiable.** Every theme must pass WCAG AA contrast ratios. A beautiful palette that fails contrast is an inaccessible one.
- **Font pairings have rules.** Serif + sans-serif is the reliable pairing. Two sans-serifs can work if they contrast in weight and width. Two serifs rarely do. Never use more than 2 typefaces in one theme.
- **Apply completely or not at all.** A theme applied to 80% of slides is worse than no theme — the 20% looks like mistakes.
- **Custom themes start from the brief.** Warm/cold, technical/human, energetic/calm — these translate directly to specific color temperature, font personality, and spacing density.

---

## Pre-Built Themes

### 1. Ocean Depths
**Feel:** Professional, trustworthy, calm. Enterprise, financial, healthcare.

```
Colors:
  Primary:     #0B3D91  — Deep ocean blue
  Secondary:   #1E6091  — Mid ocean
  Accent:      #00B4D8  — Bright cyan
  Background:  #FFFFFF
  Surface:     #F0F7FF  — Ice blue tint
  Text:        #0D1B2A
  Text Muted:  #5E6E82

Typography:
  Heading: Montserrat, Arial, sans-serif — Bold 700
  Body:    Source Serif Pro, Georgia, serif — Regular 400

Spacing: 8px base grid, generous (2× standard)
```

---

### 2. Sunset Boulevard
**Feel:** Warm, energetic, creative. Marketing, design, consumer products.

```
Colors:
  Primary:     #FF6B35  — Sunset orange
  Secondary:   #F7C59F  — Peach
  Accent:      #EFEFD0  — Warm cream
  Background:  #FFFFFF
  Surface:     #FFF8F0  — Warm white
  Text:        #1A1A2E
  Text Muted:  #6B5B45

Typography:
  Heading: Playfair Display, Georgia, serif — Bold 700
  Body:    Inter, Arial, sans-serif — Regular 400

Spacing: 8px base, balanced
```

---

### 3. Forest Canopy
**Feel:** Natural, grounded, sustainable. Environmental, wellness, food/beverage.

```
Colors:
  Primary:     #2D6A4F  — Forest green
  Secondary:   #40916C  — Sage
  Accent:      #95D5B2  — Mint
  Background:  #FAFAF8  — Warm off-white
  Surface:     #F1F8F4  — Light sage tint
  Text:        #1B2D23
  Text Muted:  #5A7A65

Typography:
  Heading: Lora, Georgia, serif — SemiBold 600
  Body:    Nunito Sans, Arial, sans-serif — Regular 400

Spacing: 8px base, airy
```

---

### 4. Modern Minimalist
**Feel:** Clean, precise, premium. Tech, SaaS, architecture, luxury.

```
Colors:
  Primary:     #000000  — Pure black
  Secondary:   #333333  — Dark gray
  Accent:      #0066FF  — Electric blue (use sparingly)
  Background:  #FFFFFF
  Surface:     #F5F5F5  — Light gray
  Text:        #111111
  Text Muted:  #888888

Typography:
  Heading: Inter, Arial, sans-serif — SemiBold 600
  Body:    Inter, Arial, sans-serif — Regular 400

Spacing: 8px base, tight (0.75× standard)
Note: Maximum whitespace, minimum decoration.
```

---

### 5. Golden Hour
**Feel:** Rich, warm, autumn. Premium food, hospitality, events.

```
Colors:
  Primary:     #8B4513  — Saddle brown
  Secondary:   #CD853F  — Peru gold
  Accent:      #DAA520  — Goldenrod
  Background:  #FDF8F0  — Parchment
  Surface:     #F5EDD8  — Warm cream
  Text:        #3D2B1F
  Text Muted:  #8B7355

Typography:
  Heading: Cormorant Garamond, Georgia, serif — Bold 700
  Body:    EB Garamond, Georgia, serif — Regular 400

Spacing: 8px base, generous
```

---

### 6. Arctic Frost
**Feel:** Cool, crisp, clinical. Healthcare, technology, research.

```
Colors:
  Primary:     #2C3E50  — Dark slate
  Secondary:   #3498DB  — Clear blue
  Accent:      #E8F4FD  — Ice blue
  Background:  #FAFCFF  — Cool white
  Surface:     #ECF3FB  — Light blue-gray
  Text:        #1A252F
  Text Muted:  #718EA4

Typography:
  Heading: Rajdhani, Arial, sans-serif — Bold 700
  Body:    Open Sans, Arial, sans-serif — Regular 400

Spacing: 8px base, structured
```

---

### 7. Desert Rose
**Feel:** Soft, sophisticated, editorial. Fashion, beauty, lifestyle.

```
Colors:
  Primary:     #C9776B  — Dusty rose
  Secondary:   #D4A5A0  — Blush
  Accent:      #7D6B5D  — Warm taupe
  Background:  #FAF7F5  — Linen
  Surface:     #F2EDE8  — Warm gray
  Text:        #3D3028
  Text Muted:  #9E8E85

Typography:
  Heading: Abril Fatface, Georgia, serif — Regular 400
  Body:    Josefin Sans, Arial, sans-serif — Light 300

Spacing: 8px base, airy
```

---

### 8. Tech Innovation
**Feel:** Bold, modern, futuristic. Startups, AI, developer tools.

```
Colors:
  Primary:     #6C63FF  — Electric violet
  Secondary:   #4ECDC4  — Cyber teal
  Accent:      #FF6B9D  — Hot pink
  Background:  #0A0A0F  — Near black
  Surface:     #14141F  — Dark panel
  Text:        #F0F0FF  — Near white
  Text Muted:  #8080A8

Typography:
  Heading: Space Grotesk, Arial, sans-serif — Bold 700
  Body:    JetBrains Mono, Courier New, monospace — Regular 400
           (or DM Sans for non-code body)

Spacing: 8px base, dense
Note: Dark mode only. Neon accents used sparingly — max 1 per composition.
```

---

### 9. Botanical Garden
**Feel:** Fresh, organic, optimistic. Health, kids, consumer apps.

```
Colors:
  Primary:     #4CAF50  — Leaf green
  Secondary:   #8BC34A  — Lime
  Accent:      #FF9800  — Sunflower orange
  Background:  #FAFFF8  — Fresh white
  Surface:     #F1F8E9  — Light green tint
  Text:        #1B5E20
  Text Muted:  #558B2F

Typography:
  Heading: Fredoka One, Arial, sans-serif — Regular 400
  Body:    Quicksand, Arial, sans-serif — Medium 500

Spacing: 8px base, playful/generous
```

---

### 10. Midnight Galaxy
**Feel:** Dramatic, cosmic, premium. Entertainment, gaming, events.

```
Colors:
  Primary:     #1A0533  — Deep purple-black
  Secondary:   #6A0DAD  — Royal purple
  Accent:      #E040FB  — Cosmic magenta
  Background:  #0D0221  — Space black
  Surface:     #160B32  — Dark nebula
  Text:        #F3E5F5  — Pale lavender white
  Text Muted:  #9575CD

Typography:
  Heading: Cinzel, Georgia, serif — Bold 700
  Body:    Raleway, Arial, sans-serif — Light 300

Spacing: 8px base, dramatic/generous
Note: Dark mode only. Gold accents (#FFD700) work as a third accent.
```

---

## Generating a Custom Theme

When no pre-built theme fits, generate one from a brief:

### Theme Generation Process

**Step 1: Extract intent from the brief**

Map descriptive words to design decisions:

| Brief word | Color temperature | Font personality | Spacing |
|---|---|---|---|
| Modern, minimal | Cool neutrals | Geometric sans-serif | Tight |
| Warm, human | Warm tones | Humanist sans or serif | Generous |
| Bold, energetic | Saturated primaries | Display/grotesque | Dense |
| Elegant, luxury | Desaturated, dark | Classic serif | Airy |
| Technical, precise | Blue/gray | Monospace or condensed | Structured |
| Playful, fun | Bright, contrasting | Rounded sans | Generous |

**Step 2: Build the palette**

```
1. Choose a hue for the primary color (based on brief)
2. Set primary at 500-weight on HSL scale
3. Dark version: rotate hue -5°, reduce lightness 15%
4. Light version: same hue, increase lightness 45%
5. Accent: complementary or analogous hue (+30° or +180°)
6. Neutrals: desaturate primary hue 5%, apply lightness scale
7. Background: near-white (lightness 97-99%)
8. Surface: near-white +2-3% saturation (lightness 94-96%)
9. Text: very dark version of primary hue (lightness 10-15%)
10. Check all contrast ratios — adjust until WCAG AA passes
```

**Step 3: Select font pairing**

```
For each personality direction:

Professional/Enterprise → Montserrat + Source Serif Pro
Creative/Editorial      → Playfair Display + Inter
Technical/Developer     → Space Grotesk + JetBrains Mono
Elegant/Luxury          → Cormorant Garamond + EB Garamond
Friendly/Consumer       → Nunito + Open Sans
Bold/Startup            → DM Sans + DM Mono
```

**Step 4: Output the theme spec**

```markdown
## Custom Theme: [Name]

### Inspiration
[2 sentences on the brief and design intent]

### Colors
| Token | Hex | Use |
|---|---|---|
| Primary | #______ | Headlines, CTAs, key UI |
| Secondary | #______ | Supporting elements |
| Accent | #______ | Highlights, badges |
| Background | #______ | Page/slide background |
| Surface | #______ | Cards, panels |
| Text | #______ | Body text |
| Text Muted | #______ | Captions, metadata |

### Typography
| Level | Font | Size | Weight | Line Height |
|---|---|---|---|---|
| Display | | 48px | 700 | 1.1 |
| Heading | | 32px | 700 | 1.15 |
| Subheading | | 24px | 600 | 1.2 |
| Body | | 16px | 400 | 1.6 |
| Caption | | 12px | 400 | 1.4 |

### Spacing
Base unit: 8px
Scale: 4, 8, 12, 16, 24, 32, 48, 64, 96px

### Contrast Ratios (WCAG AA)
- Text on Background: [ratio] ✅/❌
- Text on Surface: [ratio] ✅/❌
- Accent on Background: [ratio] ✅/❌
```

---

## Applying a Theme to Common Artifacts

### To a PPTX Presentation
```python
# Apply theme colors to all slides
from pptx import Presentation
from pptx.dml.color import RGBColor

THEME = {
    "primary": (0x0B, 0x3D, 0x91),
    "text":    (0x0D, 0x1B, 0x2A),
    "surface": (0xF0, 0xF7, 0xFF),
}

prs = Presentation("deck.pptx")
for slide in prs.slides:
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(*THEME["surface"])
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.font.size and run.font.size.pt >= 24:
                        run.font.name = "Montserrat"
                        run.font.color.rgb = RGBColor(*THEME["primary"])
                    else:
                        run.font.name = "Source Serif Pro"
                        run.font.color.rgb = RGBColor(*THEME["text"])
prs.save("deck_themed.pptx")
```

### To a CSS File
```css
/* Ocean Depths Theme */
:root {
  --color-primary:      #0B3D91;
  --color-secondary:    #1E6091;
  --color-accent:       #00B4D8;
  --color-background:   #FFFFFF;
  --color-surface:      #F0F7FF;
  --color-text:         #0D1B2A;
  --color-text-muted:   #5E6E82;

  --font-heading: 'Montserrat', Arial, sans-serif;
  --font-body:    'Source Serif Pro', Georgia, serif;

  --space-base: 8px;
}
```

---

## Definition of Done — Theme Factory

- [ ] Theme selected or generated from brief
- [ ] All 7 color tokens defined: primary, secondary, accent, background, surface, text, text-muted
- [ ] WCAG AA contrast ratio verified for text on background and text on surface
- [ ] Font pairing defined: heading font + body font + weights
- [ ] Type scale defined for at least 4 levels (heading, subheading, body, caption)
- [ ] Spacing base unit and scale defined
- [ ] Theme applied consistently across ALL elements in the artifact — no partial application
- [ ] Dark mode variant defined if the artifact supports it
- [ ] Theme spec documented in reference card format for future use
