---
name: dithered
description: Pixel-dither texture with retro-computing 1-bit aesthetic
---
# Dithered
## Mission
Celebrate the texture of early computing — pixel-dither patterns, 1-bit color depth, and the warm imperfection of retro digital art.
## Brand
### 🎨 Colors
- `#1A1A1A` — Primary background (dark pixel canvas)
- `#E8E3D9` — Primary text / light surface (warm paper)
- `#4A4A4A` — Mid-tone (50% dither gray)
- `#8B8B8B` — Light tone (25% dither gray)
- `#2D2D2D` — Dark tone (75% dither gray)
- `#C4B998` — Warm accent (amber terminal)
### 🔤 Typography
- Heading font: VT323 (Google Fonts — terminal monospace)
- Body font: IBM Plex Mono (Google Fonts)
- Type scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.125rem / xl 1.5rem / 2xl 2rem / 3xl 2.5rem
### 📐 Spacing
- Grid: 8px baseline grid (pixel-perfect alignment)
- Section padding: 4rem top/bottom
- Card gap: 1rem (multiple of 8px)
### 🧩 Components
- Buttons: Sharp 0px corners, 2px solid border, dither-pattern fill on hover, monospace text
- Cards: Solid border (2px), no shadows, dither-pattern background stripes, 0px radius
- Nav: Minimal, pixel-art logo or plain monospace text, 2px bottom border
- Hero: Large pixel-art or dithered image, monospace heading, scanline overlay effect
- Footer: Thin rule (2px), monospace links, "RETURN TO TOP" with ASCII arrow
### ♿ Accessibility
- All text passes 4.5:1 contrast (monochrome palette makes this straightforward)
- Focus rings: 2px solid border in amber accent, 0px offset (retro terminal style)
- Reduced motion: disable scanline animations and blinking cursors
- Minimum font size 0.75rem
### ✍️ Writing Tone
- Retro-computing vernacular — "LOADING...", "EXECUTE", "READ MORE >"
- Terse, terminal-like microcopy
- Labels in uppercase monospace; use angle brackets for actions: <SUBMIT>
## Do / Don't
### ✅ Do
- Apply dither-pattern textures to backgrounds, image treatments, and hover states
- Use 1-bit image treatments — convert photos to dithered B&W using Bayer or Floyd-Steinberg patterns
- Maintain pixel-perfect alignment to an 8px grid
- Add scanline overlays (CSS repeating-linear-gradient) for CRT authenticity
- Use ASCII art or pixel-art icons as decorative elements
### ❌ Don't
- Use anti-aliased fonts — monospace pixel fonts only
- Apply border-radius anywhere — everything is sharp-cornered
- Add gradients — dither patterns replace smooth transitions
- Use shadows — depth comes from dither density, not elevation
- Mix in modern design tropes (glassmorphism, soft shadows, rounded corners)
## Quality Gates
- All element dimensions are multiples of 8px
- No border-radius used anywhere on the page
- At least one dither-pattern texture applied (background, image, or hover)
- All text passes 4.5:1 contrast
- Page respects prefers-reduced-motion (disable scanlines and blinks)
- No anti-aliased fonts — all fonts are pixel/monospace family