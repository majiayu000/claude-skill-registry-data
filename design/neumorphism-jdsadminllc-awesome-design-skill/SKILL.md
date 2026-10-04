---
name: neumorphism
description: Soft UI — embossed and debossed depth, monochrome palettes, subtle shadow play, and tactile minimalism.
---
# Neumorphism
## Mission
Create interfaces that feel touchable — elements rise from and sink into their background through dual shadows, soft corners, and restrained monochrome palettes.
## Brand
### 🎨 Colors
- `#E0E5EC` — Primary (soft cool gray)
- `#A3B1C6` — Secondary (muted steel)
- `#9BA7B4` — Accent (slate blue-gray)
- `#E0E5EC` — Background (soft gray, same as primary)
- `#4A5568` — Text (dark slate)
- `#8795A1` — Muted text (mid gray)
### 🔤 Typography
- Heading: **Quicksand** (Google Fonts) — rounded, soft geometric sans
- Body: **Nunito Sans** (Google Fonts) — friendly, rounded sans-serif
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.125rem | xl 1.25rem | 2xl 1.5rem | 3xl 2rem
### 📐 Spacing
- Grid: centered single-column, max-width 720px
- Section padding: 4rem vertical, generous horizontal padding (3rem min)
- Card gaps: 2.5rem — shadows need breathing room to read as depth
### 🧩 Components
- Buttons: same background color as parent surface, raised — box-shadow: 6px 6px 12px dark-shadow, -6px -6px 12px light-shadow. Pressed state inverts shadows for debossed effect.
- Cards: raised from background via dual shadows, 16px border-radius, 2rem padding, subtle inner highlight at top edge
- Nav: debossed (inset) top bar, links appear carved into the surface, active link is raised
- Hero: centered content on raised soft platform, headline with subtle text-shadow highlight, airy spacing around
- Footer: debossed section, small text, subtle light-shadow top edge
### ♿ Accessibility
- Minimum contrast 4.5:1 for text — ensure text color works against soft gray backgrounds
- Focus states: raised button effect with contrasting ring (use a colored accent for focus only)
- Shadow-only affordance is insufficient — pair with labels, icons, or cursor changes
- Respect `prefers-reduced-motion` — disable shadow-transition animations
- Minimum body font size 16px (1rem)
### ✍️ Writing Tone
- Soft, approachable, gentle. Warm and human. Never aggressive or urgent.
- Labels in lowercase. CTAs are gentle invitations ("learn more", "try it"). No ALL CAPS.
## Do / Don't
### ✅ Do
- Use dual box-shadows on every elevated element — dark shadow bottom-right, light shadow top-left
- Match element background to parent background for the seamless raised/carved illusion
- Keep border-radius between 12-20px for soft, pillowy edges
- Use a single hue family — monochrome is essential for the effect to read
- Invert shadows for pressed/active states to simulate physical depression
### ❌ Don't
- Use colored backgrounds on elevated elements — they must match the surface behind them
- Add borders — shadows alone define edges
- Apply the effect to small or closely-spaced elements — shadows need room
- Mix bright or saturated colors — stick to soft, muted tones
- Use flat design patterns alongside neumorphic ones — pick one depth language
## Quality Gates
- [ ] All elevated elements use exactly 2 box-shadows (dark + light)
- [ ] Element backgrounds match their parent's background color
- [ ] Pressed/active states invert shadow direction (inset or reversed)
- [ ] Border-radius is between 12-20px on all components
- [ ] No borders used anywhere — shadows are the sole edge definition
- [ ] Color palette stays within a single hue family (monochrome)