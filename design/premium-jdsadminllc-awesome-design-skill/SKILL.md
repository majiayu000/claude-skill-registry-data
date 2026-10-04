---
name: premium
description: Luxury brand aesthetic with refined gold/black palette, precise spacing, and exclusive feel.
---
# Premium
## Mission
Exude exclusivity through restraint — every pixel is intentional, every gap measured, and the result feels like something few can afford but many admire.
## Brand
### Colors
- `#0A0A0A` — Background (deep black)
- `#C9A96E` — Primary (champagne gold)
- `#1C1C1C` — Secondary (charcoal)
- `#F5F0E8` — Surface (ivory cream)
- `#2A2A2A` — Card (dark slate)
- `#E8DCC4` — Text (warm white)
### Typography
- Headings: **Cormorant Garamond** (serif, timeless luxe)
- Body: **Work Sans** (sans-serif, clean precision)
- Scale: xs 0.625rem / sm 0.75rem / base 0.938rem / lg 1.125rem / xl 1.5rem / 2xl 2rem / 3xl 3rem
### Spacing
- 4px grid, precisely enforced
- Section padding: 8rem vertical, 4rem horizontal (generous but not wasteful)
- Card gaps: 2.5rem
- Max content width: 72rem
### Components
- **Buttons**: Hairline 1px gold border, transparent fill, 0px radius, hover fills with gold gradient (subtle), text tracking: 0.15em
- **Cards**: Dark slate bg, 1px subtle border, precise padding (2.5rem), hover reveals hidden gold accent line
- **Nav**: Centered, serif logo, thin top and bottom borders (1px gold), links in wide letter-spacing sans-serif
- **Hero**: Full-viewport dark background, thin centered headline in Cormorant, gold horizontal rule, no CTA — just presence
- **Footer**: Dark bg, thin gold top rule, centered collage of 3-5 links in uppercase tracked-out sans-serif
### Accessibility
- Contrast ratio >= 4.5:1 — gold on dark is risky; verify every combination
- Focus ring: 1px solid #C9A96E with 3px offset, sharp
- Reduced motion: disable all hover reveals and transition animations
- Minimum font size: 0.75rem — tracking and small sizes still legible
- Gold accent never used for functional indicators (focus, error, success) — reserve for brand
### Writing Tone
Refined, reserved, aspirational. Never a period at the end of a heading. No contractions. Vocabulary is elevated but never pretentious. "Curated" over "selected." "Exceptional" over "great." Silent confidence.
## Do / Don't
### Do
- Use letter-spacing (0.1em–0.2em) on headings and labels for airy elegance
- Apply subtle CSS transitions (400ms+ ease) for hover states
- Show large, aspirational photography at full width with dark overlays
- Limit color to 6 hex values — let black and gold do the work
- Keep borders at exactly 1px — luxury is in the details
### Don't
- Use any border-radius — luxury is sharp
- Use more than two typefaces (one serif, one sans-serif)
- Mix gold hex values — one gold, perfectly consistent
- Add box-shadows — flat, precise, sharp
- Use animations under 400ms — premium moves slowly
## Quality Gates
- [ ] Only one gold hex value (#C9A96E) in entire stylesheet
- [ ] No border-radius on any element
- [ ] All hover transitions >= 400ms duration
- [ ] No box-shadows in CSS
- [ ] Letter-spacing applied to all heading and label elements
- [ ] Page layouts cleanly at 320px with proportional spacing
