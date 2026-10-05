---
name: tristian-walker-brand
description: Tristian Walker brand design system — warm, literary, adult. Author of "The Quiet Line." Burnt sienna on cream, Merriweather + Lato (The Book) and Playfair Display + Inter (The Lecture). Signature move is serif heading with one italic phrase inside. No emoji.
---

# Tristian Walker Brand

Use this skill when designing anything for **Tristian Walker** — motivational speaker, advisor, and author of *The Quiet Line*. The brand is the arbiter of self-agency, self-reliance, and personal & professional growth.

## Core files to read first
- `README.md` — full brand context, voice guide, visual foundations, iconography.
- `colors_and_type.css` — tokens and semantic classes (import this at the top of every stylesheet).
- `ui_kits/ui_kit.html` — working reference implementation of both brand worlds.

## The two worlds
- **World A · "The Book"** — Merriweather + Lato on cream (`#F8F5EF`). Warm, literary. Use for long-form, author content, book marketing.
- **World B · "The Lecture"** — Playfair Display + Inter on parchment (`#FDFCF8`) or deep ink (`#1A1A1A`). Editorial, dramatic. Use for stage-adjacent work, slide decks, speaker pages.

## Non-negotiables
- **No emoji. Ever.**
- The signature typographic move: a serif heading containing a single italic phrase in burnt sienna (`#BC744E`) — e.g. *"The foundation **is character**."*
- Warm palette only — no cool blues, no neon, no SaaS gradients.
- Eyebrow labels are ALL CAPS, tracked wide (0.15em–0.6em), sans-serif, small.
- Em-dashes with spaces. Full stops end hero taglines — the period is a design element.
- Voice is measured, reflective, adult. Honest reckoning before reframe.

## How to start
1. `@import url('colors_and_type.css');` in your stylesheet.
2. Pick World A or World B by the surface you're designing.
3. Grab components from `ui_kits/ui_kit.html` — buttons, cards, hero patterns, capture form, trust bar, glass panels, numbered segments.
4. Icons: Lucide outline, 1.5px stroke. Never emoji.
