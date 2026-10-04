---
name: cult-ui
description: Install animated shadcn-compatible components from the Cult UI registry. 75+ components across marketing, onboarding, buttons, cards, interactive elements, visual effects, and typography. Use when adding polished UI components to any shadcn/Next.js project.
version: 1.0.0
user-invocable: false
---

# Cult UI — shadcn Component Registry

75+ animated components that drop into any shadcn project via CLI.

## Registry

```
"@cult-ui": "https://cult-ui.com/r/{name}.json"
```

## Install a Component

```bash
npx shadcn@beta add @cult-ui/{component-name}
```

Multiple at once:
```bash
npx shadcn@beta add @cult-ui/texture-card @cult-ui/texture-button @cult-ui/dynamic-island
```

Search:
```bash
npx shadcn@beta search @cult-ui --query "texture"
```

## Project Setup (first time only)

1. Ensure shadcn is initialized: `pnpm dlx shadcn@latest init`
2. Add registry to `components.json`:
   ```json
   {
     "registries": {
       "@cult-ui": "https://cult-ui.com/r/{name}.json"
     }
   }
   ```
3. Required deps: `tailwindcss@latest`, `clsx`, `tailwind-merge`, `motion`

## Available Components

### Marketing & Landing
hero-dithering, hero-color-panels, hero-heatmap, hero-liquid-metal, logo-carousel, tweet-grid, gradient-heading

### Guided Experiences
onboarding, feature-carousel, loading-carousel

### Buttons & Controls
neumorph-button, family-button, texture-button, cosmic-button, gradient-button-group

### Cards & Containers
expandable-screen, expandable-card, minimal-card, browser-window, distorted-glass, texture-card

### Layout & Forms
morph-surface, direction-aware-tabs, side-panel, code-block

### Interactive Elements
dynamic-island, color-picker, polls, terminal-animation, macos-dock

### Media
3d-carousel, video-player, dither-image

### Typography
pixel-heading, pixel-paragraph, typewriter, animated-number

### Visual Effects
grid-beam, fractal-grid, shader-lens-blur, svg-shapes

## When to Use

- Building a landing page and need polished hero sections or marketing blocks
- Adding interactive UI elements (Dynamic Island, dock, polls)
- Need animated typography or visual effects
- Want pre-built onboarding flows or feature carousels
- Any shadcn project that needs components beyond the base library

## Docs

Full catalog and live previews: https://cult-ui.com/docs
