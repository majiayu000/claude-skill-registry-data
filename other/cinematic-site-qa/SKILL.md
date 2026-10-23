---
name: cinematic-site-qa
description: Run the final mechanical and visual QA for cinematic websites, including assets, catalogs, accessibility, responsive behavior, motion, video seeking, 3D performance, and production fallbacks.
---

# Cinematic Site QA

QA the built page, not the intention.

## Static checks

```bash
npm run check
npm run assets
npm run catalogs
npm run audit -- path/to/page path/to/shared.css
```

## Browser matrix

Minimum:

- desktop 1440 × 1000
- mobile 390 × 844
- reduced motion
- keyboard only
- slow network
- failed media or WebGL
- page reload at a deep anchor
- forward and reverse scroll

## Inspect

### Clarity

- first viewport explains the offer, artifact, or task
- primary action is visible
- real proof appears early

### Media

- poster loads
- desktop and mobile variants are correct
- later assets are lazy
- scrub media seeks
- range requests work
- 3D pauses offscreen
- fallbacks preserve meaning

### Accessibility

- focus visible
- semantic controls
- contrast
- no essential information only in motion
- no autoplay audio
- touch targets usable
- zoom and text expansion do not break layout

### Performance

- no horizontal overflow
- bounded pixel ratio
- no excessive `will-change`
- no layout thrash
- initial asset budget understood
- console and network errors resolved

### Taste

- one dominant idea
- no generic card scaffold
- motion has a job
- media belongs to the product world
- the result could not be relabeled for an unrelated product

Record failures with file, state, impact, and the smallest shared fix.
