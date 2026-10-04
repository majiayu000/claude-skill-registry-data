---
name: brutalism
description: Raw, unstyled honesty with monospace fonts, visible borders, and no decoration.
---
# Brutalism
## Mission
Reject decorative design in favor of raw, functional honesty — if it works, it's beautiful enough.
## Brand
### 🎨 Colors
- `#ffffff` — Page background
- `#000000` — Text and borders
- `#0000ff` — Hyperlink blue (unvisited)
- `#800080` — Hyperlink purple (visited)
- `#00ff00` — Terminal green accent
- `#ff0000` — Error red
### 🔤 Typography
- Headings: Courier Prime (Google Fonts)
- Body: Courier Prime (Google Fonts)
- Scale: xs 0.75rem, sm 0.875rem, base 1rem, lg 1.125rem, xl 1.25rem, 2xl 1.5rem, 3xl 2rem
### 📐 Spacing
- Grid: No grid — content flows vertically, single column
- Section padding: 2rem vertical, 1rem horizontal
- Card gaps: 1px (the border itself is the gap)
### 🧩 Components
- Buttons: Raw — black 2px solid border, white fill, monospace text, 0 border-radius, hover inverts to black fill/white text
- Cards: 2px solid black border, no border-radius, no shadow, 1rem internal padding, content flows top to bottom
- Nav: A simple unstyled list of links, separated by line breaks or pipes, top of page
- Hero: A single h1 with a horizontal rule beneath it — no images, no background, no gradient
- Footer: A horizontal rule followed by plain text, monospace, small
### ♿ Accessibility
- Minimum contrast ratio 7:1 — black on white everywhere
- Focus states: Default browser focus outline (visible, functional), never suppressed
- Reduced motion: No animations to disable — everything is static
- Minimum font size 0.75rem (12px)
### ✍️ Writing Tone
- Voice: Blunt, functional, slightly defiant — like a README written by someone who hates marketing
- Labels: Lowercase, descriptive, no jargon
- No emoji, no exclamation marks, no marketing adjectives
## Do / Don't
### ✅ Do
- Use semantic HTML — the browser's default rendering IS the design
- Let content determine layout — no forced grid or column structures
- Embrace visible structural elements: borders, underlines, horizontal rules
- Keep color to the minimum: black, white, link blue, visited purple
- Ship fast — if you're spending time on polish, you're doing it wrong
### ❌ Don't
- Add border-radius to anything
- Use more than 1 font family
- Add shadows, gradients, or transparency
- Suppress default browser focus outlines
- Center text — left-align everything, like a document
## Quality Gates
- [ ] Every interactive element has visible, unsuppressed browser focus styles
- [ ] No border-radius values anywhere in CSS
- [ ] Only one font family in use (monospace)
- [ ] No shadows, gradients, or backdrop-filter effects
- [ ] All text passes 7:1 contrast minimum (AAA)
- [ ] Page is functional and readable with CSS completely disabled