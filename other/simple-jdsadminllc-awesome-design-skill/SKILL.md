---
name: simple
description: Bare essentials only — one column, maximum legibility, nothing extra. Content is the only feature.
---
# Simple
## Mission
Remove everything that isn't the content. Single-column layout, maximum readable line length, generous whitespace, and typography that disappears so the words can speak.
## Brand
### 🎨 Colors
- `#1A1A1A` — Near-black text
- `#FFFFFF` — Background
- `#F5F5F5` — Subtle surface/divider
- `#666666` — Secondary text
- `#0066CC` — Links only (no accent color system)
- `#E8E8E8` — Border
### 🔤 Typography
- Heading font: Georgia (serif)
- Body font: Georgia (serif)
- Type scale: `0.875rem` / `1rem` / `1.125rem` / `1.25rem` / `1.5rem` / `2rem` / `2.5rem`
### 📐 Spacing
- Grid system: single column, `max-width: 680px`, centered
- Section padding: `3rem` vertical (separated by `1px` horizontal rules or whitespace)
- Card gaps: none — no cards, just flowing content sections
### 🧩 Components
- Buttons: Minimal — `1px` solid border, transparent background, fill on hover, no rounded corners or slight `0.125rem`
- Cards: Not used — content lives in flowing sections, not boxed containers
- Nav: Simple text links, often just a home link + dark mode toggle, no sticky nav
- Hero: Article title (`h1`) + date + optional subtitle, no hero image unless it's the content
- Footer: Single line: copyright + optional RSS/email link
### ♿ Accessibility
- Contrast: black text on white = 17:1 (AAA); gray secondary text tested at 4.5:1 minimum
- Focus states: `2px` black outline with `2px` offset, standard and visible
- Reduced motion: no animations to reduce
- Font size minimums: `1rem` body text (16px equivalent)
### ✍️ Writing Tone
- Direct, clear, concise — write like you're explaining to a friend
- No jargon, no marketing, no filler words
- Labels: descriptive and literal — "Reply," "Read more," "Previous post"
## Do / Don't
### ✅ Do
- Keep line length between 55–75 characters per line
- Use a single column with `max-width: 680px` and `margin: 0 auto`
- Set `line-height: 1.6` for body text and `1.3` for headings
- Add `1rem` minimum paragraph spacing
- Use only one accent (link color) — everything else is grayscale
### ❌ Don't
- Add sidebars, multi-column layouts, or grid systems
- Use icons — text labels are clearer and faster to parse
- Add sticky elements, popups, or overlays
- Use more than two font weights (regular + bold)
- Include hero sections, call-to-action banners, or pricing tables
## Quality Gates
- [ ] Content column stays between 55–75 characters at all viewport widths
- [ ] Page reads top-to-bottom without any visual interruptions
- [ ] No JavaScript required for content rendering
- [ ] Print stylesheet matches screen layout (single column)
- [ ] All text passes WCAG AAA contrast (7:1 minimum)
- [ ] Page weight under 50KB total (HTML + CSS + fonts)