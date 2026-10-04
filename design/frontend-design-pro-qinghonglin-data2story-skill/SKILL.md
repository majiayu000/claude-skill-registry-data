---
name: frontend-design-pro
description: "Shared UI/visual-design rule library for building polished, distinctive, multimedia-rich self-contained HTML stories. The Data2Story Designer and Programmer read it to choose a visual language (theme, type pairing, layout, components, motion) and implement it so every blog looks intentional and editorial, never templated. Use when designing or reshaping a story's look, picking fonts/colors/themes, building a hero/chart/card/map/audio component, adding motion or an interactive, or fixing a visual defect (invisible chart, overflow, broken media, AI-slop look). Not a pipeline stage — a design source consulted by other roles."
allowed-tools: Read
---

# Frontend Design

A shared design system for building **beautiful, distinctive, multimedia-rich** HTML stories. This is not a pipeline stage; it is a library the **Designer** reads to choose a visual language and the **Programmer** reads to implement it, so output looks like an editorial product, not a default template.

## When to use

- **Designer**: before writing `page_rhythm` and per-section visuals, pick a theme and component vocabulary from here. Borrow tokens, layout, and component recipes; record the chosen theme in `designer.json` `page_rhythm`.
- **Programmer**: implement the chosen theme's tokens as CSS `:root` variables and build each visual with the matching component recipe and motion/accessibility rules here.

## Core principles

1. **Editorial, not generic.** Avoid the default-AI look (bootstrap blue, purple gradient hero, everything centered, one system font, evenly-spaced soulless cards). Commit to one bold idea per story. See [`references/themes.json`](references/themes.json) → `anti_patterns`.
2. **Rich media by default.** A story should use multiple channels well — charts, images, video, audio, interactives/maps — each presented with craft, not dumped in. See [`references/media_presentation.json`](references/media_presentation.json).
3. **One system, themed per story.** All color/type/space/shadow flow from CSS `:root` tokens so the whole page is coherent and re-themeable. See [`references/design_tokens.json`](references/design_tokens.json) for tokens and [`references/typography.json`](references/typography.json) for concrete `file://`-safe font-pairing stacks.
4. **Structure carries the reading.** A clear content column, deliberate full-bleed moments, and consistent section rhythm. See [`references/layout.json`](references/layout.json).
5. **Motion and access are part of the design.** Subtle scroll reveals and transitions, always respecting `prefers-reduced-motion`, AA contrast, focus states, and "never autoplay sound." See [`references/motion.json`](references/motion.json) for motion tokens, choreography, accessibility, and the anti-slop checklist.
6. **Self-contained.** Single HTML file; allowed CDNs only (Vega-Embed, Leaflet, optionally D3/PDF.js); inline data; works on `file://`.

## References

- **[`references/design_tokens.json`](references/design_tokens.json)** — color roles, data-color scales, fluid type scale, spacing/radius/shadow, themed via `:root`.
- **[`references/layout.json`](references/layout.json)** — content column, full-bleed breakout, section rhythm, responsive grid, sticky patterns.
- **[`references/components.json`](references/components.json)** — recipes: hero/teaser, stat callouts, card deck, pull quote, chart/map frames, audio players, scrollytelling, before/after, guess-reveal, data table, references footer.
- **[`references/media_presentation.json`](references/media_presentation.json)** — how to present each channel (image, video, audio, chart, map, instance) richly, and the "all five channels by default" doctrine.
- **[`references/themes.json`](references/themes.json)** — ready-made distinctive themes (token presets) and the anti-patterns to avoid.
- **[`references/interaction_playbook.json`](references/interaction_playbook.json)** — the deep interaction/craft playbook: craft principles, centerpiece doctrine, the universal engine (state + render + steps[]), and recipes for explorables/scrollytelling/guess-reveal.
- **[`references/pitfalls.json`](references/pitfalls.json)** — the 错题本 (mistakes-never-to-repeat ledger): real bugs from shipped runs, each with how a role detects it. Read before building.
- **[`references/exemplars/cinematic_flagship.md`](references/exemplars/cinematic_flagship.md)** — a proven cinematic-blog blueprint with copy-paste recipes (pick-a-side hero, accuracy scorecard, cinemagraph hero, continuous backdrop, publish-gate manifest).
- **[`references/abstract_excellence.json`](references/abstract_excellence.json)** — the positive flagship playbook for the dry / abstract / computational topic (chart-led / statistical / non-photographic): reframe hook, signature annotated chart, the reader's own position, disciplined typography, and the runnable-verify layer. Read whenever the topic resolves `is_visual=false` (especially `is_computational=true`) — the analogue of the cinematic recipes for stories with no photographable subject.
- **[`references/typography.json`](references/typography.json)** — font-pairing catalog, `file://`-safe font stacks, and the ban list of generic/default type choices.
- **[`references/finish.json`](references/finish.json)** — the editorial finish layer: the small polish details that lift a page from competent to crafted.
- **[`references/motion.json`](references/motion.json)** — motion tokens, choreography, micro-interactions, accessibility, reduced-motion, performance, and the anti-slop checklist.
- **[`references/quality_rubric.json`](references/quality_rubric.json)** — the shared design-quality rubric authors are scored against.

A story is well-designed when it commits to one clear visual identity, uses several media channels with craft, reads cleanly on mobile and desktop, and could not be mistaken for a default template.
