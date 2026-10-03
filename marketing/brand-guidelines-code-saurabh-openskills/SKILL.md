---
name: brand-guidelines
description: Apply brand voice, tone, colors, typography, and visual style consistently across any artifact. Use when the user wants to ensure a document, presentation, email, website, or any content matches their brand identity — including color palette, font choices, tone of voice, imagery guidelines, and design standards. Also use when the user says "make it on-brand", "apply our brand style", or shares brand guidelines to follow.
---

# Brand Guidelines

Brand is not decoration — it is recognition. Every time a user encounters your product, email, presentation, or doc, they either build trust or erode it. Consistency builds trust. Inconsistency erodes it.

This skill applies brand identity across any artifact: presentations, documents, emails, landing pages, marketing copy, UI components, or any written content. It covers both visual identity (colors, fonts, spacing) and verbal identity (voice, tone, word choices).

---

## Brand Guidelines Principles

- **Consistency is the work.** One perfectly on-brand artifact is easy. Applying the same standards to the 50th artifact in a quarter is the actual challenge. Document decisions so they can be applied without re-inventing each time.
- **Brand is a system, not a vibe.** "Make it feel premium" is not actionable. "Use Playfair Display at 40pt for headlines, #1A1A2E for text, and never use more than two typeface weights on a page" is actionable.
- **Voice is harder than colors.** Anyone can apply a hex code. Writing in a consistent voice — warm but not casual, authoritative but not cold — requires explicit rules and examples.
- **Exceptions must be deliberate.** Breaking brand rules is sometimes right (a playful social post, a technical doc for developers). But it must be a conscious choice, not an accident.
- **When in doubt, ask for the guidelines.** Never invent brand colors or voice. If the user hasn't shared guidelines, ask. A wrong brand color is worse than no color.

---

## Step 0: Gather Brand Assets

Before applying anything, collect:

1. **Color palette** — primary, secondary, accent, neutral, semantic (success/error/warning)
2. **Typography** — headline font, body font, monospace font, sizes, weights, line heights
3. **Logo** — file format, clear space rules, do/don't use cases
4. **Voice and tone guidelines** — adjectives that describe the brand voice, examples of good/bad copy
5. **Imagery style** — photography direction, illustration style, icon style
6. **Spacing and layout rules** — grid system, margins, component spacing

If the user has a brand guide document, ask them to share it. If they only have partial guidelines, ask the targeted questions above and document what they provide.

---

## Visual Identity Application

### Color System

Define and apply colors as a semantic system — never use raw hex values scattered throughout:

```
PRIMARY PALETTE
━━━━━━━━━━━━━━
Primary:     #[hex]  — Main CTAs, key UI elements, headlines
Primary Dark:#[hex]  — Hover states, dark mode accents
Primary Light:#[hex] — Backgrounds, subtle highlights

SECONDARY PALETTE
━━━━━━━━━━━━━━━━
Secondary:   #[hex]  — Supporting elements, secondary CTAs
Accent:      #[hex]  — Highlights, callouts, badges

NEUTRAL PALETTE
━━━━━━━━━━━━━━
Text Primary:  #[hex]  — Body text, labels
Text Secondary:#[hex]  — Captions, metadata, muted text
Background:    #[hex]  — Page/slide background
Surface:       #[hex]  — Cards, panels, modal backgrounds
Border:        #[hex]  — Dividers, input borders

SEMANTIC COLORS
━━━━━━━━━━━━━━
Success: #[hex]  — Confirmations, completed states
Warning: #[hex]  — Caution states, pending items
Error:   #[hex]  — Errors, destructive actions
Info:    #[hex]  — Informational states, tips
```

**Contrast requirements (WCAG AA minimum):**
- Normal text (< 18pt): 4.5:1 contrast ratio against background
- Large text (≥ 18pt or 14pt bold): 3:1 contrast ratio
- UI components and icons: 3:1 contrast ratio

Check contrast: https://webaim.org/resources/contrastchecker/

### Typography System

```
TYPEFACE STACK
━━━━━━━━━━━━━
Heading:    [Font Name], [fallback], sans-serif
Body:       [Font Name], [fallback], serif
Monospace:  [Font Name], [fallback], monospace

TYPE SCALE
━━━━━━━━━━
Display:    48–64px / 1.1 line-height / -0.02em tracking
H1:         36–40px / 1.15 line-height / -0.01em tracking
H2:         28–32px / 1.2 line-height / -0.01em tracking
H3:         22–24px / 1.25 line-height / 0em tracking
H4:         18–20px / 1.3 line-height / 0em tracking
Body Large: 18px / 1.6 line-height / 0em tracking
Body:       16px / 1.6 line-height / 0em tracking
Body Small: 14px / 1.5 line-height / 0em tracking
Caption:    12px / 1.4 line-height / 0.02em tracking

FONT WEIGHTS
━━━━━━━━━━━
Use maximum 2 weights per design:
Regular (400): body text
Medium (500):  labels, UI elements
SemiBold (600):subheadings
Bold (700):    headlines, emphasis
```

### Applying to Presentations (PPTX)

```python
from pptx.dml.color import RGBColor
from pptx.util import Pt

# Brand colors (never use # prefix in pptxgenjs)
BRAND = {
    "primary":     RGBColor(0x1A, 0x1A, 0x2E),
    "accent":      RGBColor(0xE9, 0x4F, 0x37),
    "light":       RGBColor(0xF8, 0xF9, 0xFA),
    "text":        RGBColor(0x21, 0x25, 0x29),
    "text_muted":  RGBColor(0x6C, 0x75, 0x7D),
}

def apply_brand_text(run, style: str = "body"):
    """Apply brand typography to a text run."""
    if style == "heading":
        run.font.name = "Poppins"       # or brand heading font
        run.font.bold = True
        run.font.color.rgb = BRAND["text"]
    elif style == "body":
        run.font.name = "Lora"          # or brand body font
        run.font.bold = False
        run.font.color.rgb = BRAND["text"]
    elif style == "accent":
        run.font.name = "Poppins"
        run.font.bold = True
        run.font.color.rgb = BRAND["accent"]
```

### Applying to HTML/CSS

```css
/* Brand Design Tokens */
:root {
  /* Colors */
  --color-primary:       #1A1A2E;
  --color-primary-dark:  #0F0F1A;
  --color-accent:        #E94F37;
  --color-background:    #FFFFFF;
  --color-surface:       #F8F9FA;
  --color-text:          #212529;
  --color-text-muted:    #6C757D;
  --color-border:        #DEE2E6;

  /* Typography */
  --font-heading:        'Poppins', Arial, sans-serif;
  --font-body:           'Lora', Georgia, serif;

  /* Spacing scale (4px base) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-heading);
  color: var(--color-primary);
  line-height: 1.2;
}

body, p, li {
  font-family: var(--font-body);
  color: var(--color-text);
  line-height: 1.6;
}
```

---

## Verbal Identity (Voice & Tone)

Visual brand is only half the work. Voice consistency is what makes written content feel on-brand.

### Defining Brand Voice

Document voice along four axes. Rate each 1–5:

| Axis | 1 | 5 |
|---|---|---|
| **Formal ↔ Casual** | Legal/corporate | Conversational/friendly |
| **Serious ↔ Playful** | Clinical precision | Wit and humor |
| **Authoritative ↔ Humble** | Expert pronouncements | Collaborative, asking |
| **Technical ↔ Accessible** | Deep jargon | Plain language |

Example: Stripe = Formal(3) Serious(3) Authoritative(4) Technical(3) — precise but human, expert but not arrogant.

### Voice Application Rules

For each brand voice, create explicit do/don't rules:

```
BRAND VOICE: [Company Name]
━━━━━━━━━━━━━━━━━━━━━━━━━
We are:   [3 adjectives]
We aren't:[3 adjectives]

DO:
✅ Use active voice: "We help teams ship faster" not "Teams are helped to ship faster"
✅ Lead with user benefit: "You get X" not "We provide X"
✅ Be specific: "Reduces deploy time by 40%" not "Significantly faster"
✅ Use contractions: "you'll", "we're", "it's" — sounds human
✅ Address the reader as "you" — direct, personal

DON'T:
❌ Use filler superlatives: "amazing", "incredible", "game-changing"
❌ Use passive voice in marketing copy
❌ Start sentences with "We are excited to announce..."
❌ Use jargon without explanation in user-facing copy
❌ Use ALL CAPS for emphasis — use bold instead
❌ Use more than one exclamation point per page
```

### Tone Adaptation by Context

Brand voice stays constant. Tone adapts to context:

| Context | Tone shift | Example |
|---|---|---|
| Marketing copy | More energetic, aspirational | "Ship with confidence." |
| Error messages | More direct, helpful, calm | "Your session expired. Sign in again to continue." |
| Onboarding | Warmer, encouraging | "You're almost ready — just one more step." |
| Technical docs | More precise, less personality | "The API returns a 401 status code when..." |
| Crisis / incident | Calm, factual, direct | "We identified an issue affecting X users at HH:MM UTC." |

---

## Brand Audit Checklist

Run this on any artifact before delivering:

### Visual
- [ ] All colors are from the brand palette — no off-brand hex values
- [ ] All fonts are brand-specified fonts (or approved fallbacks)
- [ ] Font sizes follow the type scale — no arbitrary sizes
- [ ] Contrast ratios meet WCAG AA on all text
- [ ] Logo used correctly — correct version, correct clear space
- [ ] No unapproved color combinations (e.g., accent on accent)
- [ ] Spacing follows the grid/scale — no random padding values
- [ ] Images match the brand photography/illustration direction

### Verbal
- [ ] Voice matches the brand voice profile (formal/casual, serious/playful)
- [ ] No banned words or phrases (per do/don't list)
- [ ] CTAs are specific and active ("Start your free trial" not "Get started")
- [ ] No filler superlatives ("amazing", "revolutionary", "game-changing")
- [ ] Contractions used appropriately for the voice
- [ ] Technical terms defined or linked on first use
- [ ] All copy reviewed for tone match to context

### Consistency
- [ ] Same terminology used throughout — no synonym drift ("workspace" vs "project" vs "board")
- [ ] Product names spelled and capitalized correctly every time
- [ ] Date/number formats consistent (US vs EU, $1,000 vs $1.000)

---

## Brand Style Reference Card

When guidelines are provided by the user, document them here for reference:

```markdown
## [Company] Brand Quick Reference

### Colors
| Name | Hex | Use |
|---|---|---|
| Primary | #______ | [use case] |
| Accent | #______ | [use case] |
| Background | #______ | [use case] |
| Text | #______ | [use case] |

### Typography
| Element | Font | Size | Weight |
|---|---|---|---|
| Headline | | | |
| Subheading | | | |
| Body | | | |
| Caption | | | |

### Voice
- Tone: [adjectives]
- Do: [key dos]
- Don't: [key don'ts]

### Logo Rules
- Minimum size: [px or mm]
- Clear space: [measurement]
- Approved on: [white / dark / brand color]
- Never: [common misuses]
```

---

## Definition of Done — Brand Guidelines

- [ ] Brand palette documented with named tokens and hex values
- [ ] Typography stack documented with sizes, weights, and line heights
- [ ] Voice profile documented with do/don't examples
- [ ] Tone adaptation defined for at least 3 key contexts
- [ ] All artifacts pass the visual brand audit checklist
- [ ] All copy passes the verbal brand audit checklist
- [ ] Consistency audit done — no synonym drift, no off-brand terminology
- [ ] Brand style reference card updated with any new decisions
