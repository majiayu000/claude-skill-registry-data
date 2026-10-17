---
name: layout-art-direction
description: Reviews or develops the graphic layout and art direction of a web page, interface, demo, portfolio piece, or marketing surface. Use when a design feels generic, overly grid-driven, visually flat, mechanically spaced, template-like, or composed without a clear focal point, hierarchy, rhythm, narrative, or intentional relationship between typography, imagery, and interface elements.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access and optional screenshot or browser access.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: designers-frontend-developers-and-creative-developers
  tags:
    - art-direction
    - layout
    - graphic-design
    - composition
    - visual-hierarchy
    - responsive-design
    - typography
    - ui-polish
  status: draft
  side_effects: none
---

# Layout Art Direction

## Purpose

Create or review layouts so they feel intentionally composed rather than merely arranged inside a technically correct grid. Turn the relationship between content hierarchy, focal points, typography, imagery, negative space, scale, alignment, rhythm, layering, and responsive behavior into an implementable art-direction plan.

The grid should provide structure, but the grid itself should not become the design.

## Core principle

Every significant visual decision must establish hierarchy, support meaning, direct attention, clarify interaction, create rhythm, reinforce character, improve comprehension, or preserve a deliberate responsive composition.

Do not recommend arbitrary asymmetry, overlap, rotation, decoration, animation, or broken-grid effects merely to look different. Intentional does not mean busy.

## When to use this skill

Use this skill when:

- A page feels like unrelated blocks placed into grid columns.
- Every section uses the same container, spacing, or card pattern.
- Headings, images, cards, and actions have similar visual weight.
- A polished interface still feels generic, flat, or template-driven.
- The user wants stronger art direction, graphic-design thinking, or a distinctive editorial, cinematic, poster-like, premium, playful, technical, or brand-specific character.
- Typography and imagery feel added after the layout rather than composed with it.
- A desktop design loses its character when reduced to a mobile column.
- Decorative elements do not contribute to hierarchy or narrative.

Do not use this skill when:

- The request is only for a logo, full brand identity, component interaction, or CSS Grid explanation.
- Accessibility compliance, motion, design-system architecture, or implementation is the primary problem and a more specific skill applies.
- A dense operational interface already uses a restrained grid to support clarity and efficiency.

## Inputs to inspect

Inspect the smallest useful set of available inputs:

- Screenshots, mockups, live captures, design files, motion recordings, references, moodboards, imagery, icons, logos, and brand guidance.
- Page purpose, audience, primary action, headings, body copy, metadata, navigation, captions, labels, and content priority.
- Relevant HTML, templates, components, CSS, design tokens, layout primitives, breakpoints, container queries, image logic, and motion.
- Existing constraints, required content, supported devices and inputs, and established visual language.

Determine what the page communicates, what viewers should remember, what they should do next, and whether the experience is expressive, informational, transactional, or operational. State assumptions when this context is unavailable.

## Design diagnosis

Identify why the current design feels unintentional before suggesting changes. Look for:

- **Flat hierarchy:** several elements compete for first attention; every section is equally loud; primary and secondary actions look alike.
- **Mechanical grid usage:** equal-width columns, default centering, repeated card grids, and technically aligned elements without meaningful visual relationships.
- **Uniform rhythm:** similar gaps and section padding throughout, with no density changes, pauses, reveals, or conclusion.
- **Weak focal control:** no dominant anchor, passive imagery, disconnected headline and action, or decoration that steals attention.
- **Disconnected typography:** text fills available boxes; type scale does not map to importance; line length and breaks lack intent.
- **Passive imagery:** standard rectangles, poor crops, conflicting subject direction, identical aspect ratios, or inconsistent treatments.
- **Decorative noise:** gradients, glass, glow, grain, borders, and shadows added without a shared function.
- **Responsive collapse:** mobile merely stacks desktop; reading and visual order conflict; focal relationships disappear without replacement.

## Workflow

### 1. Define the communication goal

Complete this sentence:

```txt
This page should make [audience] understand or feel [primary message] and then take [primary action].
```

Record the emotional quality, appropriate level of expression, and practical constraints. Do not begin with unsupported adjectives such as “modern,” “premium,” or “bold.”

### 2. Create a content hierarchy

Classify content as:

1. **Primary anchor:** the one element or relationship defining the first impression.
2. **Supporting signals:** content that explains, proves, or reinforces the anchor.
3. **Navigation and action:** elements needed to move or act.
4. **Background information:** necessary content that must not compete for attention.

Mark content as essential, supportive, optional, redundant, or misplaced. Do not solve weak hierarchy only with font size.

### 3. Write a creative thesis

Write one concise statement describing the primary composition model, dominant visual relationship, pacing, intended character, and at least one restraint. It must guide implementation rather than merely name a mood.

### 4. Select one primary composition model

Choose one dominant model, such as an editorial spread, poster, cinematic frame, exhibition wall, product catalog, technical schematic, field guide, timeline, split narrative, modular dashboard, archive, evidence board, architectural plan, magazine feature, stage, or spatial canvas.

Secondary sections may vary but must remain part of the same visual system.

### 5. Establish Anchor, Echo, and Restraint

- **Anchor:** choose one dominant compositional idea per major viewport.
- **Echo:** repeat two or three recognizable alignment, annotation, crop, scale, overlap, border, or rule ideas.
- **Restraint:** define what the design deliberately avoids so the anchor remains dominant.

Echo should create coherence, not a component pasted everywhere.

### 6. Build the visual path

For each region, identify the entry point, dominant element, supporting element, directional cue, action or transition, and exit toward the next region. Use scale, contrast, whitespace, image direction, alignment, and repetition rather than relying only on scroll position.

### 7. Design the page rhythm

Treat the page as a sequence, not a stack. Vary density, scale, column width, alignment, image presence, text length, background, depth, motion intensity, and negative space. Useful sequences include loud → quiet → detailed → resolved and claim → evidence → comparison → action.

### 8. Choose intentional layout moves

Consider asymmetric ratios, controlled broken-grid alignment, overlap, edge-aligned type, cropping, full-bleed media, annotation rails, scale contrast, offset starts, persistent spines, directional rules, or deliberate empty regions only when they support the thesis.

For every major move, report:

```txt
Move:
Purpose:
Content affected:
Expected visual effect:
Responsive adaptation:
Implementation risk:
```

### 9. Direct typography and imagery

Define compositional roles for display headings, section headings, body copy, labels, metadata, captions, annotations, actions, and numerals. Specify scale contrast, line length and breaks, alignment, relationship to imagery and edges, and responsive behavior.

For every major image, define narrative purpose, focal subject, crop, subject direction, negative-space needs, aspect ratio, edge behavior, caption relationship, color treatment, and desktop/mobile behavior. Use art-directed sources or alternate crops when needed. Verify any overlaid text across the full image range.

### 10. Direct color, surface, depth, and motion

Specify the dominant background, supporting surface, accent role, text hierarchy, rules, image treatment, interaction states, and one primary depth model. Avoid mixing shadows, glass, borders, glow, grain, and gradients without a shared rationale.

Motion may clarify hierarchy, sequence, spatial relationships, state changes, or visual continuity, but must not compensate for weak static composition. State its trigger, target, purpose, duration character, reduced-motion behavior, and whether the layout works without it.

### 11. Translate direction into resilient implementation

Connect the direction to semantic structure, Grid named lines or areas, nested grids, subgrid, intrinsic sizing, `minmax()`, `clamp()`, container queries, logical properties, controlled negative margins, `object-position`, aspect ratios, stacking contexts, tokens, fluid type, and art-directed `<picture>` sources as appropriate.

Do not conflict with DOM order, position the whole composition absolutely, hardcode heights around text, hide essential mobile content, or create overlaps that fail with translation or user content.

### 12. Design responsive compositions

For each major breakpoint or container state, define the anchor, reading and visual order, crop, alignment, overlap, type, rhythm, preserved motif, and removed or replaced treatment. Mobile may use a different composition while retaining the same thesis. Verify 200% zoom, long translations, logical DOM order, and motion independence.

### 13. Validate the composition

Run these checks:

- **Three-second scan:** topic, entry point, primary action, and dominant idea are apparent.
- **Squint and grayscale:** hierarchy survives loss of detail and color.
- **Removal:** identity survives removal of decoration.
- **Repetition and restraint:** recurring ideas are coherent and quiet space protects the anchor.
- **Content stress:** long or translated text, missing images, extra items, empty/loading/error states, and user content survive.
- **Accessibility:** heading and DOM order, focus, keyboard access, reflow, contrast, readability, reduced motion, alternatives, and control names work.
- **Distinctiveness:** composition retains a point of view without logo, palette, and photography.

## Output format

Return:

```md
## Art-direction summary

**Page purpose:** ...
**Primary audience:** ...
**Primary action:** ...
**Creative thesis:** ...
**Primary composition model:** ...

## Current diagnosis

| Priority | Symptom | Evidence | Impact |
|---|---|---|---|

## Content hierarchy

- Primary anchor:
- Supporting signals:
- Navigation and action:
- Background information:

## Anchor, Echo, and Restraint

- Anchor:
- Echo:
- Restraint:

## Composition strategy

Describe the visual path, balance, pacing, and relationships.

## Layout map

| Region | Role | Dominant element | Composition move | Alignment and scale | Responsive behavior |
|---|---|---|---|---|---|

## Typography and image direction

| Element or region | Purpose | Treatment | Responsive adaptation |
|---|---|---|---|

## Color, surface, depth, and motion

- Background and accent:
- Surface and depth model:
- Interaction states:
- Motion and reduced-motion behavior:

## Implementation guidance

- Layout primitives:
- Suggested CSS techniques:
- Content-order constraints:
- Tokens and resilience risks:

## Priority changes

### High priority
### Medium priority
### Optional experiments

## Avoid

- ...

## Validation

- [ ] One primary anchor is clear.
- [ ] Layout moves have explicit reasons.
- [ ] Typography and imagery are composed together.
- [ ] Mobile preserves the thesis and logical order.
- [ ] Content survives stress cases.
- [ ] The composition works without motion or decoration.
```

## Recommendation rules

Recommendations must be specific, tied to communication or hierarchy, implementable, responsive, coherent, accessible, and honest about risk. Replace vague advice such as “make it dynamic,” “break the grid,” or “add visual interest” with a reasoned instruction naming the affected content and responsive adaptation.

## Quality bar

The task is complete only when:

- Page purpose, audience, action, content hierarchy, and current problem are explicit.
- A concise creative thesis and one primary composition model are provided.
- Anchor, Echo, and Restraint define a coherent family of visual ideas.
- The visual path, rhythm, typography, imagery, and major layout moves receive specific direction and rationale.
- Responsive behavior is treated as composition, not automatic stacking.
- Accessibility, content resilience, and implementation risks are addressed.
- The design remains coherent when decorative styling is removed.

## Edge cases

- **Dense applications:** efficiency, stable navigation, grouping, purposeful alignment, and progressive disclosure may be the art direction; do not force editorial asymmetry.
- **Existing systems:** extend established tokens and components only when current primitives cannot express the hierarchy.
- **Limited content:** use proportion, whitespace, type, and focal relationships rather than inventing sections.
- **Missing imagery:** create a type- or shape-led direction and state what imagery would be needed.
- **User content and internationalization:** avoid fixed heights, critical line breaks, and fragile overlaps; provide fallbacks.
- **Accessibility conflicts:** preserve comprehension, reading order, focus, contrast, and reflow, then find another compositional method.
- **Appropriate generic grids:** keep conventional grids when they support comparison, scanning, repeated records, density, or operational efficiency.

## Related skills

- ui-design-direction-builder
- ui-ux-polish-review
- motion-ui-director
- responsive-layout-qa
- universal-design-heuristic-review
