---
name: dark-mode
description: "Use to add dark mode to an existing page, section, component, or site, to improve a dark mode that already exists, or to make a dark version of a raster image. Not for brand-new UI, use ui for that."
---

# Dark mode

Dark mode keeps the same contrast relationships as light mode. It's not an inversion, and it doesn't have to preserve every detail of the light design. It has to look good.

## Steps

1. Look at the existing UI and the project's Tailwind conventions.
2. Add the dark-mode classes to the markup.
3. Audit the page for raster images that need a dark version. Photos, screenshots, product mockups, decorative backgrounds, textures, rasterized illustrations.
4. Make a dark version of each one, see below. Save it next to the original and wire it in.
5. Check both modes for contrast, missing variants, and images that still assume a light background.

## Design rules

- Default to the operating system's `prefers-color-scheme` through Tailwind's built-in `dark:` behavior. Add a manual toggle only when asked.
- Remove all shadows in dark mode with `dark:shadow-none`.
- On a dark-only site, add `scheme-only-dark` to `<html>` or the top-level element so scrollbars, form controls, and `color-scheme` render dark.

## Component rules

- Never keep large branded or colored panels in dark mode. Use the same background as the page and a light divider between sections.
- Cards sit only slightly lighter than the page, `dark:bg-gray-900` on a `dark:bg-gray-950` page, with `dark:inset-ring dark:inset-ring-white/5` for definition.
- Decorative quote marks in testimonials go very faint, `dark:text-white/5`.
- One heading color in dark mode. `white` or `gray-100` for every heading, never dark gray plus a brand color.

## Raster images

- Never use CSS filters, `invert`, `brightness`, `contrast`, `opacity`, as the final dark treatment for a raster image. Make a real file.
- Generate it with your harness's image generation, editing from the original so it's visible in context. If the original is a local file, load it first.
- Same dimensions as the original, exactly.
- Pick a background that reads as the right inversion of the original. Black or dark gray for white, dark gray for off-white, or the specific dark color the human gave. If the original background matched the site background, match the dark site background instead.
- Keep the contrast relationships. Light areas get darker, separation and readability stay.
- Keep blurs and softness. Never sharpen something that was blurry.
- Keep the foreground hues. Adjust saturation and lightness only as much as the dark background needs.
- Keep the vibe. Bright and intense stays bright and intense. Subtle and muted stays subtle and muted.
- Keep fades. Anything that faded out in the original fades out in the dark version.
- Save with a `-dark` suffix. `bg.jpg` and `bg-dark.jpg`.

## SVG

- Inline `<svg>` gets dark-mode Tailwind classes, `dark:fill-*`, `dark:stroke-*`, `dark:text-*`.
- An external SVG loaded through `<img>` gets a real dark file next to the original, `logo.svg` and `logo-dark.svg`. Never a CSS filter or opacity trick.
