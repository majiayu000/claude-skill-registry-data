---
compatibility: |
    Cross-platform skill format for Claude Code, Codex CLI, Cursor, ChatGPT, and similar coding agents.
description: |
    Build React, Next.js, Framer, Motion, or MCP app interfaces with a liquid-glass visual system and reusable code library. Trigger when the user wants Apple-style liquid glass, advanced glassmorphism, frosted translucent UI with refraction/reflection, SVG displacement-map distortion, gooey or glassy controls, Framer-style liquid-glass motion, or wants to port liquid-glass inspiration into production code for chat UIs, tool panels, command docks, sidebars, modals, players, and dashboards in MCP or agentic apps. Do not trigger for ordinary flat UI, generic CSS cleanup, non-glass branding work, or backend-only MCP server tasks.
metadata:
    focus: production liquid-glass systems for MCP apps and web apps
    merged_from: liquid-glass + liquid-glass-mcp-ui
    targets:
        - codex
name: liquid-glass-mcp-ui-kit
---

# Liquid Glass MCP UI Kit

This merges two strengths into one skill:
- a **production strategy layer** for deciding how much glass, motion, and distortion an app can actually carry
- a **reference/code library** with copyable TSX, HTML, CSS, SVG, and animation recipes

Use it to build liquid-glass interfaces that look premium without turning a tool UI into unreadable jelly.

## Start here

1. Decide whether the user needs a **full visual system**, **one hero component**, or just a **single effect**.
2. Pick the lightest implementation tier that can achieve the requested look.
3. Reuse the bundled templates before inventing a new effect from scratch.
4. Keep dense MCP content on calmer inner plates even when the outer shell is flashy.
5. Stop once the requested UI is coherent, readable, and responsive.

## Pick the right implementation tier

### Tier 1 — production default
Use layered CSS, `backdrop-filter`, gradients, subtle highlights, and Motion transforms.

Choose this when:
- the user wants the liquid-glass aesthetic but not physically accurate lensing
- the UI has many cards, drawers, lists, or panels
- the app must stay responsive across desktop and mobile

Best files:
- `references/layer-system.md`
- `references/implementation-playbook.md`
- `references/framer-motion.md`
- `assets/templates/LiquidGlassButton.tsx`
- `assets/templates/LiquidGlassPanel.tsx`
- `assets/templates/LiquidGlassDock.tsx`
- `assets/templates/liquid-glass.css`

### Tier 2 — premium hero surfaces
Use inline SVG filters, displacement maps, alpha warps, and selective animated distortion.

Choose this when:
- the user explicitly wants refractive edges, lens warping, ripples, or WWDC-style distortion
- only a few surfaces need the effect
- the effect should feel more like a glass object than a frosted panel

Best files:
- `references/svg-filters.md`
- `references/codepen-demos.md`
- `assets/templates/LiquidGlassFilter.tsx`
- `assets/templates/liquid-glass-template.html`
- `scripts/generate-filter.js`

### Tier 3 — library or shader route
Use a dedicated package or WebGL only when the user wants the heaviest effect, the component is a hero piece, or the requested behavior maps directly to an existing library.

Choose this when:
- the user wants maximum realism and is okay with extra dependency and rendering cost
- the app centers on one or two showcase surfaces
- fast prototyping with a library is more valuable than zero-dependency purity

Best files:
- `references/react-components.md`
- `assets/templates/LiquidGlassCard.tsx`

## What makes good liquid glass in MCP apps

### Use glass to frame workflow, not bury it
The best MCP interfaces usually reserve the strongest glass for:
- composer shells and command docks
- floating action rows
- inspectors, drawers, menus, or modals
- selected result cards or media controls

Dense logs, JSON, tables, code, or provenance details should sit on a more stable inner plate.
That keeps the app readable while preserving the premium shell.

### Use motion as feedback, not a screensaver
Good defaults:
- hover lift: `y: -1` to `-3`
- hover scale: `1.01` to `1.03`
- tap scale: `0.97` to `0.99`
- tilt: usually under `6deg`
- pointer sheen: subtle radial highlight, spring-smoothed

If the effect competes with typing, reading, or debugging, dial it back.

### Prefer token systems over one-off magic numbers
Unify blur, radius, highlight opacity, border opacity, glow, and distortion scale.
That makes it easy to build a family of panels, buttons, docks, pills, toggles, and drawers that feel related.

## Recommended workflow

### When generating production code
1. Choose the tier.
2. Pick a base surface template or library route.
3. Establish tokens first.
4. Build one canonical surface.
5. Derive specialized pieces from that base.
6. Add Motion feedback only where it helps affordance.
7. Check contrast, reduced motion, and browser fallback.
8. Stop when the requested UI is done.

### When the user wants inspiration translated into code
Do not mirror every flashy visual flourish from demos. Extract:
- layer structure
- motion grammar
- highlight placement
- filter parameters
- interaction style

Then recompose them into the user’s real app structure.

## Reference map

### Core architecture and judgment
- `references/implementation-playbook.md` — practical design and implementation rules
- `references/mcp-app-recipes.md` — opinionated layouts for chat, dashboard, palette, and media-style MCP apps
- `references/source-catalog.md` — extracted takeaways from FreeFrontend, LogRocket, Framer, Motion, and React libraries

### Effect mechanics
- `references/layer-system.md` — the 4-layer CSS architecture and state system
- `references/svg-filters.md` — displacement, lens, specular, and reflection pipelines
- `references/framer-motion.md` — Motion recipes for mouse tracking, hover morphs, filter animation, toggles, and panel transitions
- `references/codepen-demos.md` — large raw demo patterns and reference code

### Reusable templates
- `assets/templates/LiquidGlassButton.tsx` — Motion-driven pill/button with pointer sheen
- `assets/templates/LiquidGlassPanel.tsx` — inspector/result panel pattern for tool UIs
- `assets/templates/LiquidGlassDock.tsx` — floating MCP command dock
- `assets/templates/LiquidGlassFilter.tsx` — zero-dependency React + SVG filter component
- `assets/templates/LiquidGlassCard.tsx` — library-backed drop-in card component
- `assets/templates/liquid-glass-template.html` — standalone HTML demo
- `assets/templates/liquid-glass.css` — base CSS surface tokens

### Utility scripts
- `scripts/scaffold_liquid_glass.py` — copy starter templates into a project
- `scripts/generate-filter.js` — generate SVG filter strings from parameters

## Default decisions

When the user does not specify implementation depth:
- start with **Tier 1**
- use **Tier 2** for one or two hero surfaces
- use **Tier 3** only if the user explicitly asks for maximum realism or a known library

When the user asks for a Framer-like result:
- build a stable layout first
- then add pointer sheen, spring smoothing, hover compression, and optional drag

When the user asks for an MCP interface:
- prioritize composer, dock, action row, inspector, and selected results
- keep logs, tables, code, and provenance on calmer inner surfaces

## Output rules

When this skill is used to generate code or UI proposals:
- deliver one coherent system, not unrelated effect snippets
- explain the selected tier if it is not obvious
- mention fallback or performance constraints when using heavy SVG, library, or shader approaches
- keep the number of premium distorted surfaces intentionally small unless the user explicitly wants a maximal concept piece

## Example routing

**Use this skill:**
- “build a liquid glass chat shell for my MCP app with a floating prompt dock”
- “turn this Framer liquid glass idea into real React + Motion code”
- “make the inspector and tool result panels look like Apple liquid glass”
- “I need an SVG displacement-map button with subtle refraction”

**Do not use this skill:**
- “clean up my Tailwind classes”
- “design a flat analytics dashboard”
- “debug my MCP websocket server”
- “make the backend stream faster”
