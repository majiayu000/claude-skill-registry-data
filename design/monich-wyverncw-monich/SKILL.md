---
name: monich
license: MIT
description: Build premium scroll-driven web pages and product showcases inspired by high-end app, hardware, and product interaction patterns. Use for Raycast-like, Apple-like, NVIDIA-like, RTX/GPU, SaaS, AI browser, parallax, sticky scroll, pinned reveal, Three.js GLB model, Web Audio sound effect, responsive accessibility, and performance-safe frontend requests.
---

# Monich Skill

## Purpose

This skill helps agents build premium scroll-driven websites with:

- sticky scenes
- scroll-linked animation
- parallax depth
- product/app reveals
- CSS mockups, imported assets, or Three.js GLB product models
- clean hero sections
- responsive layout
- reduced-motion support

## Use This Skill When

The user asks for:

- Raycast-like landing page
- Apple-like product showcase
- NVIDIA-like product reveal
- RTX/GPU showcase
- scroll parallax website
- sticky scroll website
- pinned scroll animation
- premium product page
- animated SaaS landing page
- AI app/browser landing page

## Do Not Copy Brands

Do not copy:

- logos
- names
- screenshots
- exact layout
- product claims
- marketing text
- brand assets

Only use general interaction patterns.

## Stack Selection

Default to React for generated websites unless the user explicitly asks for another stack. Prefer React + Vite for fast runnable demos and React + Next.js for routed, production-style, SEO-aware, or app-router projects. Other stacks such as Astro, SvelteKit, Vue, Nuxt, vanilla Web Components, or plain HTML/CSS/JS are allowed when the user requests them or the host project already uses them.

Use React + Next.js when:

- the user asks for Next.js
- the target project is already Next.js
- the page needs routing, metadata, server components, static generation, or production app structure

## Template Scanning Workflow

When this skill is activated, recursively scan the available templates before writing code.

If using this repository directly:

1. Inspect `templates/`.
2. Recursively scan every folder and file under `templates/`.
3. If present, scan every folder and file inside `templates/web-template/design-templates/`, `templates/web-template/horizontal-craft/`, and `templates/web-template/design-systems/`.
4. Read actual source/reference files inside every template/reference folder, including `.html`, `.css`, `.js`, `.jsx`, `.tsx`, `.md`, `.json`, and design-token files. Do not rely only on `SKILL.md`, `README.md`, `info.md`, or folder names.
5. Build an inventory of template names, metadata, visual style, page type, layout pattern, motion pattern, component language, color system, typography, and stack.
6. Privately compare the user's request against the inventory and choose the closest matching template or reference set for the requested website.
7. For broad or style-sensitive requests, present 2-4 closest template references to the user with a short rationale before implementation.

If using an installed skill:

1. Inspect `assets/templates/`.
2. Recursively scan every folder and file under `assets/templates/`.
3. If present, scan every folder and file inside `assets/templates/web-template/design-templates/`, `assets/templates/web-template/horizontal-craft/`, and `assets/templates/web-template/design-systems/`.
4. Read actual source/reference files inside every template/reference folder, including `.html`, `.css`, `.js`, `.jsx`, `.tsx`, `.md`, `.json`, and design-token files. Do not rely only on `SKILL.md`, `README.md`, `info.md`, or folder names.
5. Build an inventory of template names, metadata, visual style, page type, layout pattern, motion pattern, component language, color system, typography, and stack.
6. Privately compare the user's request against the inventory and choose the closest matching template or reference set for the requested website.
7. For broad or style-sensitive requests, present 2-4 closest template references to the user with a short rationale before implementation.

Templates are learning references. Do not copy-paste a full template, page, component, or large code block into the generated project. Extract the intent, structure, motion rhythm, spacing, typography, and visual system, then create fresh code for the user's stack and content.

Starter templates are implementation aids only. Do not default to the visual style of starter templates when a closer `web-template` reference exists. If building in React, Next.js, or another framework, translate the selected `web-template` reference into that stack while preserving its layout, composition, typography, palette logic, and interaction feel.

## Required Scroll Architecture

Every generated page must include:

1. Normal hero section
2. Tall scroll wrapper, 250vh to 500vh
3. Sticky scene, 100vh
4. Layered visual elements:
   - background layer
   - atmosphere/grid/glow layer
   - midground UI/spec layer
   - main product/app/object layer
   - foreground text/accent layer
5. Next section after the showcase

## Motion Timeline

Map scroll progress like:

- 0.00 to 0.20: hero locks into scene
- 0.20 to 0.45: main product/app appears
- 0.45 to 0.70: features/spec cards enter
- 0.70 to 1.00: scene transitions out

## Visual Rules

- one clear focal point
- large typography
- dark premium background by default
- one accent color
- no random neon unless asked
- no particle soup
- no unreadable microtext
- no generic AI SaaS slop
- strong spacing and hierarchy
- mobile-first fallback

## Code Rules

- Animate transform and opacity.
- Avoid top, left, width, height, margin, padding animation.
- Include prefers-reduced-motion.
- Default to React components for generated websites, but adapt to Next.js, Astro, SvelteKit, Vue, Nuxt, or plain HTML/CSS/JS when requested or when the existing project requires it.
- Read and recursively scan `templates/` or installed `assets/templates/` before choosing references.
- Read real template implementation files, especially `.html`, `.css`, and `.js`, before judging visual similarity.
- Learn and adapt from templates; do not copy-paste template code line-by-line.
- Write fresh components, data, CSS variables, class names, and content for the target project.
- Match visible page copy to the language the user spoke. If the source template contains Chinese but the user writes in English or Indonesian, rewrite headings, labels, CTAs, alt text, and microcopy into that user language.
- Set document language correctly, such as `<html lang="en">`, `<html lang="id">`, or the equivalent framework metadata.
- Use CSS-only mockups when no assets are provided.
- Use user-provided `.glb`, `.gltf`, image, or video assets when available.
- Use CSS-only mockups when no assets are available.
- Do not invent missing external assets or copy real brand assets.
- No missing image imports.
- No unused packages.
- No fake dependencies.
- Keep components readable.

## Bundled Templates

Learn from templates by recursively scanning `assets/templates/`, including every nested folder and file in `assets/templates/web-template/design-templates/`, `assets/templates/web-template/horizontal-craft/`, and `assets/templates/web-template/design-systems/` when those folders exist.

Some templates may contain Chinese-first material. Use their composition, rhythm, typography, and page-type guidance, but localize final generated content to the user's language unless the user requests Chinese.

## Output Requirements

When generating a website, include:

- file structure
- install command
- complete source code
- complete CSS
- run command
- customization notes
- accessibility/performance checklist

## Final Checklist

Before final answer, verify:

- sticky scene works
- scroll wrapper is tall enough
- layers are visible
- main focal object exists
- responsive CSS exists
- reduced-motion fallback exists
- no brand assets copied
- no missing imports
- app can run
