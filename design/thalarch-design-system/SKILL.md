---
name: thalarch-design-system
description: >
  Creates or extracts a semantic visual system for websites and applications.
  Use before major frontend redesigns, multi-page sites, brand-heavy UI, or when
  an existing codebase needs its visual language made explicit. Produces a compact
  design contract covering atmosphere, color roles, typography, spacing, components,
  layout, motion, responsive behavior, imagery, and anti-patterns without forcing
  a particular framework or design tool.
---

# Thalarch Design System

A strong site should look like one product, not a sequence of independently
styled sections.

Use this skill to create a **semantic design contract** before implementation or
to reverse-engineer one from an existing frontend.

## 1. Start with product character

Define:

- product/subject;
- audience;
- primary job;
- visual atmosphere;
- density: airy / balanced / dense;
- composition: ordered / asymmetric / expressive;
- motion: restrained / fluid / cinematic;
- one distinctive design idea that belongs to this product.

Avoid design adjectives that could describe any startup.

## 2. Extract before inventing

If an existing product already has UI or brand assets, inspect first:

- theme/tokens;
- CSS variables;
- Tailwind/theme configuration;
- component library;
- typography declarations;
- spacing/radius/shadow patterns;
- icons and imagery;
- screenshots or Figma/Stitch references when available.

Preserve stable identity unless redesign is explicitly requested.

## 2.5 External design-reference atlas

When the project/user does not already provide enough visual direction and external research is
available, use `references/awesome-design-md.md`.

That reference maps `VoltAgent/awesome-design-md` into Thalarch's workflow. The source is valuable
because its analyzed `DESIGN.md` files encode design systems as structured reasoning rather than
surface screenshots.

Use it selectively:

- choose one primary reference by task fit;
- use at most one secondary reference for a clearly distinct quality;
- extract only the relevant atmosphere, hierarchy, palette roles, type character, composition,
  material/depth, imagery treatment, responsive behavior, and guardrails;
- synthesize those qualities into the current project's own design contract;
- never let a famous reference outrank the user's brand or existing project truth.

For raster/image tasks, hand the compact reference capsule to `thalarch-imagegen`; do not dump a
whole external DESIGN.md into the generation prompt.

## 3. Semantic tokens

Define roles, not arbitrary values:

### Color
- canvas / elevated surfaces;
- primary and secondary text;
- muted/supporting content;
- primary action;
- accent;
- borders/dividers;
- success/warning/error/info.

Use exact values in the implementation contract where known, but describe their
visual role too.

### Typography
Define:
- display face/character;
- body face/character;
- scale hierarchy;
- weights;
- line height;
- letter spacing;
- numeral/code treatment when relevant.

Do not default to the same fashionable font stack on every project.

### Geometry
Define:
- spacing rhythm;
- radius philosophy;
- border weight;
- shadow/depth treatment;
- container widths;
- grid/gutter behavior.

## 4. Component behavior

Describe important components semantically:

- navigation;
- buttons/actions;
- cards/containers;
- forms;
- dialogs/sheets;
- lists/tables;
- media blocks;
- domain-specific components.

For each component, define hierarchy and states instead of styling every instance
independently.

## 5. Layout system

Record:

- page frame and max widths;
- grid philosophy;
- whitespace strategy;
- alignment rules;
- section rhythm;
- when asymmetry/overlap is allowed;
- mobile reflow strategy;
- touch-target expectations.

Desktop design must not merely shrink on mobile.

## 6. Motion system

Motion must communicate hierarchy, continuity, or feedback.

Define:
- page-entry behavior;
- hover/focus/press behavior;
- section transitions;
- reduced-motion fallback;
- banned decorative motion.

Prefer a few choreographed moments over dozens of unrelated animations.

## 7. Imagery system

Define what kind of imagery belongs in the product:

- photography / illustration / 3D / abstract / none;
- crop and framing;
- contrast and saturation;
- texture/grain;
- relation to UI surfaces;
- icon/diagram language;
- whether generated imagery is allowed and where.

If generated assets are needed, hand them to `thalarch-imagegen` with this design
contract as the brand reference.

## 8. Anti-pattern contract

Write project-specific bans, such as:

- generic SaaS gradient hero;
- excessive cards-inside-cards;
- every section centered;
- decorative blobs without meaning;
- random glassmorphism;
- uniformly rounded everything;
- interchangeable AI-generated illustrations;
- multiple competing accent colors;
- fake dashboard data or placeholder lorem ipsum in final work.

Do not ban a style merely because it is popular. Ban it when it conflicts with
the product's chosen direction.

## 9. Output

For non-trivial projects, maintain a concise `DESIGN.md` or repository-appropriate
design artifact containing:

1. Product & audience
2. Visual atmosphere
3. Color roles
4. Typography
5. Geometry & spacing
6. Components
7. Layout & responsive rules
8. Motion
9. Imagery
10. Accessibility constraints
11. Anti-patterns
12. Example implementation language

If the repository already uses a design-system document, update that instead of
creating a competing source of truth.
