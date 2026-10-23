---
name: modular-scroll-page
description: Build a brand-neutral cinematic page from the modular scroll starter while preserving semantic tokens, native motion contracts, accessibility, and a product-specific visual world.
---

# Modular Scroll Page

Start from `templates/modular-scroll-starter/`.

## Read

- project `PRODUCT.md`
- project `DESIGN.md`
- `docs/project-context.md`
- `skills/cinematic-web-director/SKILL.md`
- `tokens/system.css`
- `modules/motion.js`

## Preserve

- semantic `ds-*` API
- complete content without JavaScript
- one `h1`
- skip link and focus treatment
- reduced motion
- mobile layout
- theme independence
- small native motion helpers

## Replace

- all demonstration copy
- visual world
- palette and typography
- media
- composition
- signature interaction

Do not recolor the starter and call it a new brand.

## Escalate carefully

Add GSAP, Spline, Three.js, or video only after the page direction identifies a concrete need.

## Verify

Run:

```bash
npm run audit -- path/to/page tokens/system.css
npm run smoke
```

Check 1440px, 390px, reduced motion, keyboard focus, and slow media.
