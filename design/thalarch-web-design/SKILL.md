---
name: thalarch-web-design
description: >
  Designs and implements distinctive, production-grade websites, landing pages, dashboards, web
  apps, and frontend components. Use when the user asks to build, redesign, beautify, or
  substantially restyle a web interface. Infers the brief before styling, establishes a
  product-specific aesthetic direction/design system, uses image-to-code when visual references
  are central, and requires responsive browser evidence instead of generic AI-template output.
---

# Thalarch Web Design

Build websites like a small design studio that also owns the production code.
The result must have a point of view **and** work.

## 1. Design Read — read the room first

Before coding or picking a visual system, infer:

- page/product kind;
- audience and trust expectations;
- primary job/action of the page;
- vibe words in the request;
- supplied screenshots/sites/brand references and their role;
- existing logo/colors/type/photography/components;
- technical/framework constraints;
- accessibility, regulatory, performance and content constraints.

Create a compact internal `Design Read` that says what this is, who it is for, and what visual
language is justified.

Ask at most one focused clarification only when two plausible design directions would materially
change the result. Otherwise make a concrete, reversible design ruling and proceed.

Accessibility, regulated/public-sector requirements, existing brand rules and explicit user
constraints override aesthetic novelty.

## 2. Set qualitative design dials

Before implementation calibrate three qualitative dimensions:

- **variance** — strict/symmetric ↔ expressive/asymmetric;
- **motion** — static/functional ↔ cinematic/kinetic;
- **density** — gallery/airy ↔ information-dense/productive.

Choose values from the actual brief; do not use fixed numeric presets as universal truth.

Examples:

- trust-first/regulated → lower variance and motion, controlled density;
- premium consumer/brand → medium-high variance, selective motion, lower density;
- creative portfolio/cultural site → higher variance and motion with disciplined hierarchy;
- dense admin/product UI → lower decorative variance, higher information density, strong states.

These dials guide choices; they never override usability.

## 3. Anti-default discipline

Do not fall into automatic LLM patterns unless the product genuinely calls for them:

- purple/blue glow as the default “AI” aesthetic;
- centered hero + three equal cards + logo strip + CTA;
- glassmorphism everywhere;
- giant rounded containers around every section;
- card-inside-card nesting;
- random badges/pills/tiny system labels;
- generic copy and fake statistics;
- one fashionable font used for every category;
- animation on everything;
- arbitrary framework/component-library replacement.

Ask: **could this become another company's site by swapping only logo and text?** If yes, the
visual thesis is too generic.

## 4. Choose system vs aesthetic honestly

Before inventing primitives, inspect the repository for an existing design system/component
library. Preserve it unless the task explicitly replaces it.

If the brief clearly maps to an official design system already used/required by the product,
prefer the current official package and tokens for the proven project version rather than hand-
recreating its components.

If the direction is an aesthetic rather than an official system — editorial, brutalist,
cinematic, glass, bento, dark-tech, etc. — implement it honestly with the project's existing stack.
Do not pretend a trend is an official design system.

One coherent system beats mixing several design libraries.

## 5. Design system before sprawl

For multi-section or multi-page work, load `thalarch-design-system`.

Define/extract semantic roles for:

- color;
- typography;
- spacing;
- radius/borders/shadows;
- layout widths/grid;
- motion;
- imagery;
- component states;
- accessibility constraints.

Do not give each section an independent visual language.

## 6. Typography

Typography is structure, not decoration.

- Choose typefaces appropriate to subject/brand and legally/technically available.
- Prefer project-provided/licensed fonts before casually adding new ones.
- Control line length, line height, weight, tracking and responsive scale.
- Use display/body contrast only when it supports the concept.
- Avoid font mixing solely to create “visual interest”.
- Audit large italic/display text for clipping and line-box issues.
- Use fallback/loading behavior that avoids destructive layout shift.

No font family is universally banned or universally premium; fit and existing brand win.

## 7. Color and material

- Build a palette with clear functional roles.
- Restrain accent count unless the brand requires more.
- Keep warm/cool neutral logic coherent.
- Use gradients, blur, glass, texture, glow, grain or shadows only when they support the chosen
  material language.
- Maintain readable contrast and visible focus states.
- Keep lighting/shadow direction coherent.
- Treat dark mode as designed, not inverted.

## 8. Spatial composition

Use layout intentionally:

- asymmetry when it improves hierarchy;
- strong alignment anchors;
- controlled grid-breaking moments;
- whitespace appropriate to the content density;
- responsive CSS Grid/flex based on actual layout needs;
- `dvh`/modern viewport behavior where full-height mobile sections require it;
- optical alignment when mathematical centering looks wrong.

Avoid novelty that destroys scanning or interaction clarity.

## 9. Content and states

Real content structure is part of design.

- one clear primary action per context when possible;
- believable copy/data rather than lorem ipsum/fake generic filler;
- real or intentionally disabled destinations — no dead `#` links as final output;
- loading, empty, error, success and long-content states where the product can reach them;
- active navigation/current-state cues where relevant;
- direct, useful error copy.

Do not invent legal/compliance UI unless the product/jurisdiction actually requires it.

## 10. Imagery and image-to-code strategy

Decide first whether the site needs imagery or a visual reference workflow.

Possible paths:

- repository/user-provided assets;
- real product screenshots;
- generated raster artwork through `thalarch-imagegen`;
- deterministic SVG/diagram/code visuals;
- CSS/Canvas/WebGL when justified;
- `thalarch-image-to-code` when matching a screenshot/mockup/generated reference is central.

For open-ended high-art-direction websites, generated section concepts can help **when** they make
the design more concrete. Do not make image generation mandatory for every visual task.

When references are used, label their roles and extract a visual contract before coding. Use large,
readable section/detail references rather than one unreadable mega-board.

Generated assets are independently reviewed before integration.

## 11. Motion

Use motion for hierarchy, feedback and continuity.

Prefer:

- a composed entry sequence;
- meaningful hover/focus/pressed feedback;
- restrained scroll choreography;
- motion tied to user intent;
- transform/opacity-style cheap animation when appropriate;
- `prefers-reduced-motion` support.

Do not add a motion library when native CSS or the repository's existing stack is sufficient.

## 12. Responsive behavior

Design and verify at least:

- compact/mobile;
- normal desktop;
- one stress case such as wide desktop, long labels or dense content.

Check navigation, reordering, tap targets, text wrap, overflow, image crop/focal point, sticky/fixed
elements, mobile browser chrome and safe areas when relevant.

Mobile is recomposition, not desktop squeezed to 390px.

Also inspect the first viewport on a modest laptop-sized screen; premium design should not depend on
a giant monitor to keep the hero readable.

## 13. Accessibility and trust

Implement real semantics:

- landmarks/headings;
- keyboard operation;
- visible focus;
- labels;
- contrast;
- reduced motion;
- meaningful alt text;
- skip-to-content or equivalent when the site's structure warrants it;
- no essential interaction hidden behind hover only.

Destructive/error states must be understandable before and after activation.

## 14. Performance discipline

Inspect image dimensions/format/weight, font loading, layout shift, unnecessary JS, animation cost,
filters/shadows on hot paths and responsive image behavior.

Do not sacrifice the concept for a synthetic benchmark, but do not ship multi-megabyte decorative
assets or perpetual expensive effects without justification.

For measured performance work, route to `thalarch-performance`.

## 15. Implementation

Respect the existing framework, styling method, dependency versions and component patterns.

Before importing a package, verify it exists or that adding it is genuinely justified. Do not
hallucinate imports from a fashionable stack.

Prefer semantic tokens, small reusable components, real interactions and minimal dependency growth.

## 16. Browser proof and iterative fidelity

After implementation use `thalarch-browser-qa` and relevant visual review.

When a target/reference exists, use `thalarch-image-to-code` checkpoints:

1. render real page;
2. capture target viewport;
3. compare composition/type/spacing/material/crop;
4. fix largest mismatch first;
5. rerender;
6. verify compact + desktop and primary interactions.

A build passing is not visual proof. A generated mockup is not implementation proof.

If browser tooling cannot run, appearance/interaction claims remain `UNVERIFIED`.

## 17. Design quality gate

Before completion ask:

- Does the visual language follow the Design Read?
- Could it belong to another product after a logo swap?
- Is the primary action obvious?
- Is there one coherent visual thesis/system?
- Are typography and spacing doing hierarchy work?
- Is every decorative technique justified?
- Does mobile feel authored?
- Are product states/accessibility handled?
- Are images integrated rather than pasted in?
- Does the real browser result match the design intent/reference?

If the first real-browser inspection changes the design direction substantially, update the design
contract and rerun review rather than pretending the original plan still describes the result.
