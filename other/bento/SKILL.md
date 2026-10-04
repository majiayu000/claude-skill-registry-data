---
name: bento
description: Apple-style bento grid with modular cards, frosted glass touches, and soft depth.
---
# Bento
## Mission
Organize content into a flexible, visually satisfying modular grid that feels premium and Apple-like — cards of varying sizes snap together like a bento box.
## Brand
### 🎨 Colors
- `#f5f5f7` — Background light
- `#1d1d1f` — Background dark
- `#ffffff` — Card surface light
- `#2d2d2f` — Card surface dark
- `#0071e3` — Accent blue
- `#86868b` — Muted text
### 🔤 Typography
- Headings: SF Pro Display (system, fallback: Inter)
- Body: SF Pro Text (system, fallback: Inter)
- Scale: xs 0.75rem, sm 0.8125rem, base 1rem, lg 1.0625rem, xl 1.5rem, 2xl 2rem, 3xl 3rem
### 📐 Spacing
- Grid: CSS Grid with auto-fit and dense packing, 16px gaps
- Section padding: 80px vertical, 24px horizontal (centered, max-width 1024px)
- Card gaps: 16px between all cards
### 🧩 Components
- Buttons: Pill-shaped (full border-radius), 12px-24px padding, solid accent fill or frosted glass outline
- Cards: 20px border-radius, 24-32px internal padding, subtle backdrop-filter blur on glass variants, 1px semi-transparent border
- Nav: Fixed top, frosted glass (`backdrop-filter: saturate(180%) blur(20px)`), centered logo, minimal link count (3-5 items max)
- Hero: Large centered headline, supporting subheadline, one prominent CTA, optional product image/showcase
- Footer: Clean column layout, 5-7 links max per column, small muted text, light background
### ♿ Accessibility
- Minimum contrast ratio 4.5:1 for body text
- Focus states: Blue ring with 2px offset on all interactive elements
- Reduced motion: Disable card hover lifts and scale transforms
- Minimum font size 0.75rem (12px)
### ✍️ Writing Tone
- Voice: Warm, confident, human — like a knowledgeable friend explaining something
- Labels: Sentence case, action-oriented
- No exclamation marks; enthusiasm comes from clarity, not punctuation
## Do / Don't
### ✅ Do
- Vary card sizes within the grid — some 1x1, some 2x1, some 2x2
- Use subtle frosted glass on at most 1-2 hero cards per page
- Keep card count to 6-12 per section for visual rhythm
- Pair cards with rich imagery or iconography at card-level
- Use soft, subtle shadows (`box-shadow` with low opacity, large blur)
### ❌ Don't
- Make every card the same size — that defeats the bento concept
- Apply frosted glass to more than 20% of card surfaces
- Use bright, saturated colors — keep the palette muted and elegant
- Add borders thicker than 1px
- Use drop shadows darker than `rgba(0,0,0,0.08)`
## Quality Gates
- [ ] Cards use at least 2 different aspect ratios within each section
- [ ] Frosted glass cards have sufficient text contrast against any background image
- [ ] Grid reflows gracefully on mobile (cards stack, maintain visual hierarchy)
- [ ] Focus rings visible on all interactive card elements
- [ ] No card has a border thicker than 1px
- [ ] Section padding is consistent (80px) except where intentionally varied