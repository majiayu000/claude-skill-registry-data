---
name: portfolio
description: Creative showcase with large imagery, minimal chrome, and work-first hierarchy.
---
# Portfolio
## Mission
Get out of the way and let the work speak — a frame so minimal and refined that attention flows entirely to the content.
## Brand
### Colors
- `#FAFAFA` — Background (near-white)
- `#111111` — Primary (near-black)
- `#666666` — Secondary (mid-gray)
- `#E5E5E5` — Surface (light gray)
- `#FFFFFF` — Card (pure white)
- `#000000` — Text (true black)
### Typography
- Headings: **DM Serif Display** (editorial, refined)
- Body: **Inter** (functional, clean)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2.5rem / 3xl 4rem
### Spacing
- 4px baseline grid
- Section padding: 8rem vertical, 3rem horizontal
- Card/project gaps: 3rem
- Max content width: 90rem (wide for impact)
### Components
- **Buttons**: Outline style, transparent bg, 1px solid border, no radius, hover fills with #111111
- **Cards**: Full-bleed imagery, minimal overlay on hover (title only), no borders, no shadows
- **Nav**: Ultra-minimal, logo only or single-word link, fixed position, transparent bg, text only
- **Hero**: Full-viewport project image, video, or animation, optional small title overlayed bottom-left. No CTA — the work is the CTA.
- **Footer**: Almost invisible — thin 1px top rule, small gray text, max 3 links
### Accessibility
- Contrast ratio >= 4.5:1 (grayscale palette passes easily)
- Focus ring: 2px solid #111111 with 2px offset, no radius
- Reduced motion: disable image/video autoplay and any scroll animations
- Minimum font size: 0.875rem
- All project images require descriptive alt text — this is a portfolio
### Writing Tone
Confident, understated. Let the work do the talking. Minimal copy. Project titles only where possible. Fewer words = more impact. No exclamation points. No marketingese.
## Do / Don't
### Do
- Let images go full-bleed with zero padding
- Use generous whitespace (3rem+ between projects) to create breathing room
- Keep navigation to 1-3 items maximum — hide everything else
- Lazy-load images with lo-res placeholders to maintain layout
- Design for cursor hover — show project details only on mouseover
### Don't
- Add drop shadows, gradients, or decorative backgrounds
- Show more than one project or image above the fold
- Use more than 4 words in navigation
- Crowd the footer with links, sitemaps, or social grids
- Force autoplay video or audio without a visible pause button
## Quality Gates
- [ ] Navigation has 3 or fewer items
- [ ] At least one full-bleed image above the fold
- [ ] No drop shadows or gradients anywhere in CSS
- [ ] All images have alt text
- [ ] Page loads under 1.5 MB with lazy-loaded images
- [ ] Works at 320px with stacked project images
