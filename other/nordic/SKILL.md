---
name: nordic
description: Scandinavian minimalism with light wood tones, clean lines, and functional coziness.
---
# Nordic
## Mission
Deliver serene, functional clarity through Scandinavian design principles — where every element earns its place and warmth comes from restraint.
## Brand
### 🎨 Colors
- `#F5F0EB` — Background (warm off-white)
- `#2C3E50` — Primary (deep slate)
- `#A8D8B9` — Accent (sage green)
- `#D4A574` — Secondary (light oak)
- `#E8DCC8` — Surface (linen)
- `#1A1A2E` — Text (near-black)
### 🔤 Typography
- Headings: **Inter** (sans-serif, clean geometric)
- Body: **Crimson Text** (serif, warm readable)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2rem / 3xl 3rem
### 📐 Spacing
- 8px grid system
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 1.5rem
- Max content width: 72rem
### ��� Components
- **Buttons**: Flat, no shadows, 2px border-radius, hover darkens 10%, focus ring 2px offset
- **Cards**: White or linen surface, subtle 1px border (#E0D8CC), no shadow, 8px radius
- **Nav**: Sticky top, transparent bg with backdrop-blur, simple text links, no icons
- **Hero**: Large breathing room, single statement, no carousel — one image or none
- **Footer**: Minimal, 3-4 links max, light separator line
### ♿ Accessibility
- Contrast ratio ≥ 4.5:1 for all body text
- Focus ring: 2px solid #2C3E50 with 2px offset, visible on all interactive elements
- `prefers-reduced-motion` disables all transitions
- Minimum font size: 0.75rem (12px)
- All images require meaningful alt text
### ✍️ Writing Tone
Calm, direct, unhurried. Short sentences. No exclamation marks. Labels use sentence case. Scandinavian directness — say what you mean and stop.
## Do / Don't
### ✅ Do
- Use generous whitespace as an active design element
- Limit each view to one clear call-to-action
- Favor natural materials (wood tones, stone grays, linen textures) in imagery
- Keep navigation shallow — max two levels
- Let photography breathe at full width with ample padding
### ❌ Don't
- Use drop shadows heavier than 2px blur
- Add decorative elements that serve no function
- Use more than two typefaces on any page
- Overload the hero with multiple CTAs or carousels
- Clutter footers with sitemaps or social icon grids
## Quality Gates
- [ ] Color palette limited to 6 defined hex values — no unlisted colors in production CSS
- [ ] All interactive elements have visible focus states
- [ ] Page weight under 500KB (images optimized, no heavy frameworks)
- [ ] Navigation works with keyboard only (Tab, Enter, Escape)
- [ ] Content reads naturally at320px viewport width
- [ ] Every image has descriptive alt text and serves a purpose