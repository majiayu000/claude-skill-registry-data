---
name: maximalist
description: Abundant, dense, rich layering, pattern on pattern.
---
# Maximalist
## Mission
Embrace abundance — layer patterns, textures, colors, and typography into dense, energetic compositions that reward exploration and feel unapologetically rich.
## Brand
### 🎨 Colors
- `#ff6b35` — Burnt orange (primary)
- `#004e64` — Deep teal (secondary)
- `#ffd166` — Marigold (accent)
- `#c44536` — Brick red (accent)
- `#2e294e` — Aubergine (background)
- `#efc3e6` — Orchid pink (highlight)
### 🔤 Typography
- **Heading:** Abril Fatface (bold, decorative display) or Playfair Display Black
- **Body:** Meryweather (serif, readable) or Libre Baskerville
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1rem, lg: 1.125rem, xl: 1.25rem, 2xl: 2rem, 3xl: 3.5rem — large jumps for impact
### 📐 Spacing
- Dense: 0.5rem–1.5rem gaps between elements
- Section padding: 3–5rem vertical, 1.5rem horizontal
- Card gaps: 1rem (tight, overlapping possible)
- Border radius: varies — mix of 0, 8, 16, 50% (eclectic)
### 🧩 Components
- **Buttons:** Bold fills, decorative borders (double, dashed, patterned), oversized at 32px+ tall, collage-like hover effects
- **Cards:** Overlapping arrangement, mixed patterns, decorative frames, multiple typography styles within one card
- **Nav:** Dense with decorative dividers, mixed type treatments, patterned background strip
- **Hero:** Pattern-on-pattern layering, large display type overlapping imagery, multiple accent colors, decorative borders
- **Footer:** Dense link clusters, decorative elements, patterned background, oversized social icons
### ♿ Accessibility
- All text must pass 4.5:1 contrast — maximalist density must not sacrifice legibility
- Clear visual hierarchy must exist despite density (size, color, position)
- Focus states: thick (3px) high-contrast outline that cuts through patterns
- Reduced motion: static patterns only, no parallax, no animated backgrounds
- Minimum touch target: 44x44px despite dense layout
### ✍️ Writing Tone
Expressive, bold, unapologetic. Exclamation points allowed. Run-on sentences for effect? Yes — when it serves the rhythm. Rich vocabulary. Direct address to the reader. Maximalist copy matches maximalist visuals.
## Do / Don't
### ✅ Do
- Layer 2–3 background patterns with different opacity and scale for depth
- Mix typography families intentionally — 3–5 families can work with clear hierarchy
- Use decorative borders, ornamental dividers, and pattern frames as structural elements
- Vary component shapes — mix circles, rectangles, organic blobs within the same view
- Create visual paths through the density with strategic use of contrast and scale
### ❌ Don't
- Sacrifice readability for decoration — every text element must be legible at its rendered size
- Dump decoration without structure — maximalism needs an organizing principle, not chaos
- Use low-contrast patterns that blur into illegiblity
- Animate dense patterns — they're visually overwhelming already; motion adds cognitive load
- Apply maximalism to utility interfaces (settings, forms, data tables) — reserve for brand/browsing surfaces
## Quality Gates
- [ ] All text passes 4.5:1 contrast regardless of the background pattern beneath it
- [ ] A clear visual hierarchy exists — a first-time viewer can identify the primary action in < 2 seconds
- [ ] No auto-playing pattern or background animation
- [ ] Touch targets remain 44x44px minimum despite dense layout
- [ ] Patterns and decorative elements don't exceed 1MB total page weight
- [ ] Reduced-motion mode replaces all animated patterns with static equivalents