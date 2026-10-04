---
name: pastel
description: Soft muted colors with gentle gradients, calming aesthetics, and approachable warmth.
---
# Pastel
## Mission
Create gentle, inviting digital spaces where color whispers instead of shouts — soft hues that lower tension and make every interaction feel safe.
## Brand
### 🎨 Colors
- `#FFF5F5` — Background (blush white)
- `#B8C9E8` — Primary (powder blue)
- `#F0C4D8` — Accent (rose pink)
- `#C5E0C5` — Secondary (mint green)
- `#FDEBD0` — Surface (peach cream)
- `#4A4A5A` — Text (soft charcoal)
### 🔤 Typography
- Headings: **Nunito** (rounded sans-serif, friendly)
- Body: **Quicksand** (rounded sans-serif, approachable)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2rem / 3xl 2.5rem
### 📐 Spacing
- 8px grid with generous breathing room
- Section padding: 6rem vertical, 2.5rem horizontal
- Card gaps: 2rem
- Max content width: 68rem
### 🧩 Components
- **Buttons**: Fully rounded (50px radius), pastel fill with 10% darker hover, no shadows, smooth 300ms transition
- **Cards**: Rounded (16px radius), soft pastel bg, no border, subtle gradient top-to-bottom, gentle hover lift (4px translateY)
- **Nav**: Transparent bg, rounded pill-shaped links on hover, centered or left-aligned
- **Hero**: Large soft gradient background (radial or linear), centered headline, optional floating illustration
- **Footer**: Rounded top corners, soft pastel bg, minimal links, gentle wave divider
### ♿ Accessibility
- Contrast ratio ≥ 4.5:1 for text on pastel backgrounds — verify each combination
- Focus ring: 3px solid lavender (#B8C9E8) with 2px offset, fully rounded
- Reduced motion: disable all hover lifts and background gradient animations
- Minimum font size: 0.875rem (14px)
- Pastels alone are insufficient for data viz — always add pattern or label for color-blind users
### ✍️ Writing Tone
Warm, encouraging, inclusive. Use "we" and "you" naturally. Emojis welcome in moderation (✨ 🌸). Exclamation points allowed sparingly. Never condescending.
## Do / Don't
### ✅ Do
- Use CSS gradients as backgrounds — radial for heroes, linear for cards
- Round everything: buttons (50px), cards (16px), inputs (12px), modals (20px)
- Layer pastels with white space — never pack pastel-on-pastel without separation
- Add playful illustrations or blob shapes as decorative elements
- Use generous line-height (1.6–1.8) for body text
### ❌ Don't
- Use pastels for small text or icons without sufficient contrast checking
- Combine more than 4 pastel colors on a single view
- Use sharp corners (0px radius) anywhere
- Pair pastels with dark, heavy shadows — keep shadows soft and tinted
- Overlap pastel shapes without distinct borders or white space
## Quality Gates
- [ ] Every text/pastel combination passes 4.5:1 contrast ratio
- [ ] Corner radii are consistent: buttons=50px, cards=16px, inputs=12px
- [ ] No border-radius: 0 on any component
- [ ] Gradients are present on hero or card backgrounds
- [ ] Focus rings are fully rounded and visible
- [ ] Page is calm and readable at320px — no overflow or truncation