---
name: aigent
description: Design direction and browser QA for websites, landing pages, product interfaces, dashboards, decks, and immersive or 3D web pages. Use when the user asks to design, redesign, build, polish, critique, animate, or visually direct a frontend, wants references turned into a direction, or wants a rendered page checked for responsive, focus, contrast, clipping, or reduced motion problems.
---

# Aigent

This file is the entry point when the whole repo is installed as one skill (cloned into a skills folder, referenced from Cursor rules, or pointed at from `AGENTS.md`). All paths below are relative to this file.

The real guidance already lives in the repo. Load it in this order and read only what the task needs.

## 1. Start here

Read [`skills/aigent-design/SKILL.md`](skills/aigent-design/SKILL.md) and follow it. It owns the authority order, the operating model, the Variance / Motion / Density controls, the preservation contract, and the completion bar.

## 2. Then the one reference that fits

From [`skills/aigent-design/reference/`](skills/aigent-design/reference/):

- `shape.md` brief and product truth
- `inspiration.md` references and transformations
- `new-work.md` new whole surface work
- `layout.md` hierarchy, grouping, density, responsiveness
- `type.md` typography
- `color.md` palette and semantic color
- `motion.md` motion and continuity
- `media.md` image, video, 3D, and production choice
- `interface.md` product UI
- `deck.md` presentations and guided decks
- `resolve.md` rendered mechanical QA
- `vision.md` structured visual review
- `publish.md` export and deployment

For business websites (marketing, landing, service, ecommerce, editorial, membership, nonprofit) also read [`skills/aigent-business-sites/SKILL.md`](skills/aigent-business-sites/SKILL.md). It adds content architecture, truthful proof, preserve-mode redesign, and a release audit.

Add [`skills/aigent-design/reference/craft-floor.md`](skills/aigent-design/reference/craft-floor.md) before substantial implementation or final review.

## 3. Calibration and deeper material, only when relevant

- [`skills/aigent-design/visual-exemplars/`](skills/aigent-design/visual-exemplars/) strong and weak examples. Open 2 to 4, never copy them.
- [`docs/design-principles.md`](docs/design-principles.md), [`docs/3d-scroll-playbook.md`](docs/3d-scroll-playbook.md), [`docs/cinematic-scroll-deck-playbook.md`](docs/cinematic-scroll-deck-playbook.md), [`docs/mobile-qa-checklist.md`](docs/mobile-qa-checklist.md)
- [`skills/README.md`](skills/README.md) lists the specialist skills (inspiration, quality, creative production). Most users never need them directly.
- [`tokens/system.css`](tokens/system.css) neutral `ds-*` tokens and primitives, and [`templates/`](templates/) starter pages.

## Ground rules

- The target project's own product, brand, and design docs outrank anything here. Aigent's own brand (`DESIGN.md`, `PRODUCT.md`, the `aigent-*` specialist skills) is not the target project's truth.
- Never claim Taste, Resolve, or Vision ran when they did not. Their commands are in `skills/aigent-design/SKILL.md` and run through `npx github:wrg32786/aigent-design-system`.
- First render is not final. Render, inspect, fix, render again.
