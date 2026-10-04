---
name: frontend-design-codex
description: Create distinctive, production-grade frontend interfaces in Codex. Use when the user asks to build, redesign, restyle, modernize, or visually polish web components, pages, dashboards, apps, prototypes, games, hero sections, or existing UI, especially when they want non-generic AI aesthetics, strong typography, color, motion, layout, responsive behavior, and browser-verified implementation.
---

# Frontend Design Codex

Use this skill to turn frontend requests into working, production-oriented UI with a clear aesthetic point of view. The goal is not to decorate a default layout. The goal is to design and implement an interface that feels specific to the product, audience, and interaction model.

This skill adapts the public Claude `frontend-design` workflow to Codex. It uses Codex-native capabilities: local file edits, Image Gen when concepting is useful, Browser or Playwright verification, existing project design systems, and mechanical handoff evidence.

## Quick Workflow

1. Understand the product, audience, workflow, constraints, and success state.
2. Commit to one distinctive visual direction before coding.
3. Build a small design system: tokens, typography, spacing, components, motion, and asset treatment.
4. Implement the real usable surface in the repo's existing stack.
5. Verify in a browser on desktop and mobile sizes.
6. Iterate until the visible UI matches the chosen direction and has no obvious layout, responsiveness, typography, or interaction defects.
7. Final-answer with changed files, verification commands, browser URL, and remaining intentional deviations.

## Design Pre-Analysis

Before coding, write a compact design brief in the working notes:

- Purpose: the problem the interface solves and the primary user.
- Context: landing page, operational app, dashboard, editor, commerce flow, game, or component.
- Tone: choose one precise direction, such as editorial utility, industrial control room, playful toy-like, luxury restraint, brutalist raw, retro-futuristic, organic/natural, art deco, dense analyst workspace, or calm enterprise tool.
- Differentiator: the one visual or interaction idea a user should remember.
- Constraints: framework, existing design system, accessibility, performance, content, data shape, and responsive requirements.

If the request is a full page, app, dashboard, or visually led redesign, use Image Gen for concepting unless the user opts out, an existing design system already dictates the visual answer, or the task is a narrow UI fix.

## Visual Direction Rules

Commit to a direction that fits the domain. Do not mix several moods because they sound impressive.

- SaaS, CRM, admin, analytics, and operational tools should be dense, calm, legible, and workflow-first.
- Consumer, brand, venue, editorial, and product pages should have a strong first-viewport signal and real visual assets.
- Games and playful demos can be more expressive, illustrated, and animated, but core rules and controls must work.
- Existing products should preserve recognizable information architecture before adding visual polish.

## Style Range Matrix

This skill is not a single visual style. If the user does not specify a style and the task is visually led, consider three meaningfully different directions before choosing one. Pick the direction that best fits the product, audience, and workflow, then make the implementation coherent around that choice.

Useful direction families:

- Editorial utility: strong type hierarchy, restrained color, print-like rhythm, useful for publishing, research, documentation, and serious brand sites.
- Industrial control room: dense rows, hard dividers, status color, mono details, useful for operations, monitoring, logistics, and infrastructure tools.
- Playful toy-like: chunky controls, kinetic motion, friendly color, useful for education, kids, games, and creative demos.
- Luxury restraint: large negative space, tactile imagery, refined typography, useful for fashion, fragrance, hospitality, and premium products.
- Brutalist raw: exposed grids, sharp contrast, direct labeling, useful for experimental portfolios, events, and opinionated cultural work.
- Retro-futuristic: period-specific type, geometric panels, glow used sparingly, useful for music, games, hardware, and speculative products.
- Organic/natural: soft asymmetry, material texture, botanical or earthy color, useful for wellness, food, environment, and handmade products.
- Art deco: geometric ornament, high contrast, vertical rhythm, useful for venues, editorial campaigns, and premium event pages.
- Dense analyst workspace: compact tables, filters, inspectors, charts, and keyboard-friendly flows for professional tools.
- Clinical calm: high legibility, neutral surfaces, trustworthy states, useful for healthcare, finance, security, and compliance.

## Anti-Generic UI Rules

Avoid generic AI frontend habits. Apply at least 10 of these checks before handoff:

1. Do not default to purple-blue gradients on white backgrounds.
2. Do not default to Inter, Roboto, Arial, or system fonts when a distinctive but readable font pairing is appropriate.
3. Do not use repeated card grids as the main structure unless cards are the actual interaction model.
4. Do not add hero eyebrow labels, pill soup, fake badges, fake metrics, or logo clouds unless the brief or reference requires them.
5. Do not make every section a centered headline plus three cards.
6. Do not make dashboard data into marketing cards when tables, timelines, maps, charts, or inspectors are the real workflow.
7. Do not add decorative glows, blobs, or gradients that do not clarify hierarchy or brand.
8. Do not use stock-like generic imagery that could fit any product.
9. Do not let browser-default control typography appear in buttons, tabs, inputs, sidebars, toolbars, table cells, or status bars.
10. Do not ship inert controls in app UI; tabs, filters, selections, drawers, and primary actions need visible state.
11. Do not use tiny low-contrast text to make the design look polished while hurting readability.
12. Do not use the same type scale, radius, shadows, and palette across unrelated prompts.
13. Do not hide weak hierarchy behind excessive animation.
14. Do not use a static screenshot as app UI; keep navigation, text, controls, forms, and tables code-native.
15. Do not change a true white reference background into cream or gray unless the concept calls for it.

## Design System Extraction

Before implementation, define the local system in code or notes:

- Colors: background, surface, text, muted text, border, accent, semantic states, shadows.
- Typography: display, heading, body, label, caption, control text, weights, line heights, and fallback fonts.
- Spacing: page gutters, section rhythm, grid columns, panel padding, control heights, row density.
- Shape: radii, borders, dividers, elevation, media frame treatment.
- Components: buttons, links, tabs, filters, rows, cards only where necessary, tables, charts, forms, modals, empty states.
- Motion: page entrance, hover/focus, selection, reveal, loading, and reduced-motion behavior.
- Assets: real or generated images, product renders, icons, logos, textures, diagrams, sprites, and their crop/aspect rules.

Repeated UI must use shared tokens or reusable components. Differences should be named variants, not one-off copied styling.

## Implementation Rules

- Follow the repo's framework, routing, component, state, styling, lint, and accessibility patterns.
- For a new complex frontend without an existing stack, default to React + Vite. For a simple static proof, HTML/CSS/JS is acceptable.
- Build the real usable surface first. Do not wrap a future app in a marketing shell unless the user asked for a landing page.
- Preserve user-provided copy, required data, navigation labels, CTA labels, states, and workflows.
- Prefer existing icon libraries when they match the direction; otherwise write small, clean SVGs with consistent optical size.
- Use CSS variables or theme tokens for all recurring colors, spacing, and typography.
- Keep text readable at common desktop and mobile widths. Fix wrapping, clipping, and overlap before final handoff.
- Add accessibility basics: semantic landmarks, button labels, focus states, sufficient contrast, and `prefers-reduced-motion`.
- Keep dependencies local to the project. Do not add a package unless it materially improves the result and the user or repo allows it.

## Responsive Rules

Check at least one desktop and one mobile viewport.

- First viewport must fit without clipped primary content.
- Navigation must collapse or simplify cleanly.
- Tables, inspectors, editors, and dashboards must preserve scanning value; do not turn every dense surface into stacked cards automatically.
- Buttons and controls need stable sizes and tap targets.
- Hero or main workspace text must not overlap imagery, charts, or controls.
- Fixed or sticky headers count against viewport height.

## Motion Rules

Use motion to clarify hierarchy, state, and tangibility.

- Prefer 2-3 deliberate motions over many scattered effects.
- Good defaults: staggered entrance, state transition, hover/focus affordance, scroll-linked reveal, or active selection.
- Avoid motion that delays task completion, hides content, or causes layout shift.
- Respect `prefers-reduced-motion`.
- Verify at least one animated or interactive state in the browser.

## Browser Verification

Run the app and verify the visible product, not just the build.

1. Start the local dev server when needed and record the URL.
2. Prefer the Codex Browser plugin for local targets. Use Playwright when Browser is unavailable or when scripted screenshots are more reliable.
3. Check desktop and mobile widths.
4. Click through the core workflow: navigation, filter, tab, form, playback, selection, game control, or primary CTA.
5. Inspect typography, color, spacing, responsive behavior, icon treatment, asset loading, focus states, and motion.
6. Capture a screenshot when practical and compare it against the concept, reference, or written visual direction.
7. Keep fixing if there is clipped content, unreadable text, inert controls, placeholder visuals, stale debug UI, mobile overflow, or a generic template-like result.

## Handoff

Final response should be concise and evidence-based:

- Files changed.
- Browser URL or static file path.
- Build/test/lint commands run and their result.
- Desktop and mobile verification method.
- Core interaction path verified.
- At least five visual checks performed.
- Intentional deviations or remaining limitations.

Do not claim visual success without browser evidence when the task involves a runnable UI.
