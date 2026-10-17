---
name: expressive-grid-planner
description: Plans expressive, content-driven layout systems by translating an approved creative concept, visual system, content hierarchy, and responsive requirements into flexible grid directions. Use when a website, landing page, editorial experience, portfolio, campaign, or brand page needs stronger composition than a default 12-column layout, including asymmetric, modular, ratio-based, nested, or compound grid strategies without producing CSS or final interface designs.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: planner
  audience: web-designers-and-creative-directors
  tags:
    - grid
    - layout
    - composition
    - art-direction
    - responsive-design
    - editorial-design
    - compound-grid
    - visual-hierarchy
  status: draft
  side_effects: none
---

# Expressive Grid Planner

## Purpose

Translate an approved creative direction, visual system, and real content requirements into a flexible structural layout system.

Treat the grid as a regulator for hierarchy, proportion, relationships, rhythm, whitespace, balance, tension, consistency, and variation—not merely a set of alignment columns. The same grid should support multiple meaningful compositions without forcing content into one repeated template.

This skill plans layout behavior. It may define conceptual columns, modules, horizontal fields, shared anchors, ratios, spans, empty fields, structural exceptions, and responsive transformation. It must not produce final mockups, exact dimensions or breakpoints, design tokens, CSS Grid, Flexbox, Tailwind classes, components, or frontend code.

## Core principles

Begin with content and relationships:

```txt
content
-> hierarchy
-> relationships
-> structural requirements
-> grid
-> composition
```

Balance structure with freedom. Elements may span columns, use secondary structures, leave fields empty, shift alignment, overlap boundaries, or escape the grid when this improves meaning and the underlying order remains perceptible.

The grid informs composition; it does not dictate a template.

## When to use this skill

Use this skill when:

- A creative direction and visual system have already been selected.
- The user asks for an expressive grid, composition system, structural layout direction, or responsive layout grammar.
- Default centered sections, equal-width cards, or a conventional 12-column grid produce repetitive results.
- Content needs stronger hierarchy, asymmetry, controlled density, or meaningful whitespace.
- Several content types need compatible but different structures.
- The desktop direction is expressive, but smaller viewports lose its relationships or character.
- A visual system defines composition principles but not the structural rules that enact them.

Do not use this skill when:

- The communication problem, concept, visual system, or content is too unresolved to support structural decisions.
- The user wants broad page-concept exploration; use `layout-direction-explorer`.
- The user wants to develop or critique full art direction beyond grid architecture; use `layout-art-direction`.
- The user only wants review of an existing layout; use `layout-principles-review`.
- The task is final interface design, component design, CSS implementation, exact breakpoints, spacing tokens, or Tailwind configuration.

## Inputs to inspect

Inspect the smallest useful set of available material:

- Approved direction: essential meaning, narrative lens, audience transformation, content progression, tension, and conversion path.
- Visual system: thesis, core principles, composition, framing, typography and imagery behavior, expression levels, invariants, and variables.
- Real content: headings, body copy, images, video, diagrams, products, services, statistics, quotes, captions, metadata, navigation, and actions.
- Existing structure: sitemap, wireframes, current pages, templates, component inventory, existing grid, screenshots, or design-system constraints.
- Practical constraints: viewport range, readable text widths, CMS behavior, localization, unknown content lengths, dynamic content, image availability, accessibility, and implementation complexity.

Before planning, establish:

```txt
Actual content:
Primary and secondary priorities:
Required sequence:
Essential relationships:
Repeated or variable content:
Dominant imagery or media:
Responsive relationships to preserve:
Concept or visual-system behavior the layout should express:
```

If real content is unavailable, produce provisional directions and name the assumptions that could change them. Placeholder rectangles are not sufficient evidence for a final grid strategy.

## Workflow

### 1. Restate the compositional objective

Translate the approved direction into spatial terms:

```txt
The layout should make <content or meaning>
feel <spatial characteristic>
by using <relationship or compositional behavior>
while preserving <usability constraint>.
```

Reject objectives that reduce to “look cool and asymmetric.”

### 2. Inventory the content

Create:

| Content | Type | Importance | Length sensitivity | Repeatability | Required relationship |
|---|---|---:|---|---|---|

Classify content as `primary`, `secondary`, `supporting`, or `utility`. Identify what attracts attention first, what follows, what remains quiet, what needs isolation, and what repeats.

### 3. Map relationships and focal weight

Record relationships such as `belongs with`, `supports`, `contrasts`, `explains`, `proves`, `precedes`, `follows`, `interrupts`, or `annotates`.

Then define:

```txt
Primary focal element:
Secondary focal element:
Supporting field:
Quiet field:
Likely visual center of gravity:
```

Do not express hierarchy only through type size. Area, position, isolation, whitespace, contrast, alignment, imagery, and density also create importance.

### 4. Write structural requirements

Separate requirements into:

```txt
Must support:
Should support:
May support:
```

Include semantic order, readable line lengths, image roles, caption relationships, variable content, CMS limits, and responsive transformation.

### 5. Test the simplest viable structure

Begin with a single field or a simple two-, three-, four-, or six-column structure. Ask which useful content widths and relationships it enables.

Only introduce more complexity when it materially improves hierarchy, flexibility, meaning, or production efficiency. Twelve columns are neither mandatory nor inherently wrong.

### 6. Evaluate relevant grid families

Consider only families justified by the content:

- Even-column grids for repeated content and shared alignment.
- Asymmetric grids for unequal hierarchy, annotation fields, tension, or directional flow.
- Ratio-based structures when brand geometry, product proportions, imagery, or hierarchy suggests useful proportions.
- Modular grids when horizontal and vertical relationships both need control.
- Nested grids when a region requires a denser local structure inside the primary system.
- Compound grids when incompatible content types need different but coordinated structures.

For compound structures, identify primary and secondary grids, shared outer margins or axes, horizontal fields, and the reason for combination. Do not use mathematical ratios as proof of beauty or complexity as proof of sophistication.

Read [references/grid-strategy-guide.md](references/grid-strategy-guide.md) when the task needs detailed selection prompts, structural diagrams, responsive tests, strategy examples, or anti-pattern diagnosis.

### 7. Plan whitespace, density, balance, and tension

Treat empty space as a structural field that can separate ideas, create emphasis, pace chapters, improve readability, or balance density. Do not assume empty space is automatically elegant.

Describe the intended rhythm, such as:

```txt
dense -> open -> dense
quiet -> build -> focal moment -> release
```

Decide where stability supports trust or clarity and where controlled tension supports editorial emphasis, transformation, or campaign energy. Tension must remain anchored by perceivable order.

### 8. Translate narrative into section behavior

Create:

| Section | Narrative role | Dominant content | Structural behavior | Density | Expression |
|---|---|---|---|---|---|

Use the same grid to create meaningful variation through spans, empty fields, insets, reversals of visual weight, secondary structures, or restrained exceptions. Repeat a section structure only when repetition communicates something useful.

### 9. Define structural exceptions

For each proposed grid escape, record:

| Element | Normal behavior | Exception | Reason | Expected effect | Risk |
|---|---|---|---|---|---|

Possible exceptions include bleed, overlap, entering an empty field, bridging structures, or extending beyond a viewport edge. Reserve them for emphasis, transition, tension, or focus. If everything breaks the grid, no break remains meaningful.

### 10. Integrate typography, imagery, captions, and annotations

Verify that:

- Body copy has usable line lengths and room for content expansion.
- Display type may span boundaries without compromising reading.
- Imagery has explicit roles such as dominant, supporting, evidence, or decorative.
- Image scale varies deliberately rather than reflecting one CMS component.
- Captions remain clearly associated even when placed beside, above, inset, or in an annotation field.
- Narrow fields hold labels, chapter markers, metadata, dates, coordinates, or sources only when useful.

### 11. Produce distinct directions when exploration is useful

Generate two or three directions only when the brief benefits from comparison. Each must embody a different structural strategy, not merely a different column count.

For each direction, describe:

```txt
Thesis:
Primary and secondary structure:
Horizontal fields and shared anchors:
Composition behavior:
Dominant and quiet regions:
Whitespace and density behavior:
Grid exceptions:
Best suited to:
Risks:
```

Use lightweight ASCII diagrams when they clarify proportion, hierarchy, or relationships without implying exact dimensions.

Compare candidates on content fit, hierarchy, concept and visual-system alignment, variation, readability, responsive resilience, CMS tolerance, production complexity, and distinctiveness. Recommend the simplest adequate direction when selection is in scope. If the user requests exploration only, do not choose a winner.

### 12. Plan responsive transformation

Preserve relationships rather than coordinates. Define what must survive before describing wide, medium, and narrow behavior.

Possible transformations include:

- Columns collapse or modules merge.
- Side annotations become inline.
- Horizontal sequences become vertical while preserving order.
- Overlaps separate.
- Secondary grids deactivate.
- Decorative fields disappear.
- Whitespace reduces proportionally.
- Image crops and visual weight change.
- Visual placement changes while semantic order remains logical.

Medium layouts need an intentional composition rather than an awkward desktop compromise. Narrow layouts may use indentation, alternating alignment, varied image widths, chapter markers, negative space, or type-scale contrast; do not default automatically to undifferentiated full-width stacking.

### 13. Protect semantic order and accessibility

Plan a conceptual document order, then describe any different visual placement. Never let layout produce a confusing sequence for screen readers, keyboard navigation, zoomed views, or CSS-disabled contexts.

Check that the direction supports:

- Logical headings and reading order
- Reflow without clipped or overlapping text
- Zoom and larger text
- Localization and content expansion
- Clear caption and annotation relationships
- Touch usability
- A discoverable visual pathway that does not require users to solve where to read next

### 14. Stress-test and simplify

Test:

- Headlines or translations around 30% longer
- Longer testimonials and body copy
- Short or missing optional content
- Portrait, landscape, missing, or substituted imagery
- Irregular repeated counts such as three, six, or eleven items
- Sparse and dense sections
- CMS-authorable variations

Remove structures, modules, or alignments that do not materially improve hierarchy, flexibility, meaning, or efficiency. The final grid must be explainable to another designer without reference to visual fashion.

## Output format

Return:

```md
## Layout Brief

Project:
Approved concept:
Visual-system principles:
Page or content type:
Primary content goal:
Primary focal content:
Secondary content:
Key relationships:
Responsive constraints:

## Content Inventory

| Content | Type | Importance | Length sensitivity | Relationship |
|---|---|---:|---|---|

## Hierarchy

Primary:
Secondary:
Supporting:
Utility:

## Compositional Objective

...

## Structural Requirements

Must support:
Should support:
May support:

## Grid Direction A — <name>

### Thesis
...

### Structure

Primary grid:
Secondary grid:
Horizontal fields:
Shared anchors:

### Composition behavior
...

### Dominant and quiet regions
...

### Whitespace and density
...

### Structural exceptions
...

### Best suited to
...

### Risks
...

### Structural diagram
...

## Grid Direction B — <name>

...

## Direction Comparison

| Criterion | Direction A | Direction B | Direction C |
|---|---|---|---|
| Content fit | | | |
| Concept alignment | | | |
| Hierarchy | | | |
| Variation | | | |
| Readability | | | |
| Responsive resilience | | | |
| CMS tolerance | | | |
| Complexity | | | |
| Distinctiveness | | | |

## Recommended Structure

Direction:
Why:
What to preserve:
What to simplify:
What still needs testing:

## Section Layout Plan

| Section | Narrative role | Dominant content | Grid behavior | Density | Expression |
|---|---|---|---|---|---|

## Responsive Transformation

### Wide

Structure:
Primary relationships:
Expression:
Structural exceptions:

### Medium

Structure changes:
Relationships preserved:
Elements simplified:

### Narrow

Source order:
Composition:
Relationships preserved:
Optional elements removed:

## Accessibility and Resilience

Reading order:
Text-width concerns:
Reflow:
Zoom and content expansion:
Localization:
Touch:

## Handoff

Recommended structural direction:
Layout principles to preserve:
Elements requiring visual prototyping:
Responsive questions:
Content dependencies:
Accessibility risks:
Recommended next workflow:
```

Omit empty directions when only one structure is warranted. Mark assumptions and unresolved content rather than fabricating precision.

## Quality bar

The task is complete only when:

- Actual content, hierarchy, and important relationships shape the structure.
- The compositional objective traces to the approved concept and visual system.
- The simplest viable grid was considered before more complex options.
- Asymmetry, ratios, modules, horizontal fields, nesting, or compound structures have explicit reasons when used.
- Compound structures share anchors and serve genuinely different content needs.
- Whitespace, density, visual weight, balance, and tension are intentional.
- Structural exceptions are rare and justified.
- One grid can generate varied section compositions without becoming a repeated template.
- Typography, imagery, captions, and annotations remain usable and related.
- Wide, medium, and narrow behavior preserves meaning rather than coordinates.
- Mobile retains art direction without compromising source order or comprehension.
- The direction survives reflow, zoom, localization, missing media, and content-length variation.
- Distinct directions are supplied only when exploration is useful.
- Complexity is removed when it does not improve hierarchy, flexibility, meaning, or efficiency.
- No exact dimensions, breakpoints, final mockups, CSS, utility classes, components, tokens, or frontend code are produced.

## Edge cases

- Existing 12-column design system: preserve it when required; create expression through unequal spans, empty columns, nested grids, offsets, horizontal fields, bleed, and variable composition.
- Rigid CMS: distinguish fixed, variable, and editor-controlled structure; do not recommend a system the publishing environment cannot maintain.
- Frequently changing content: favor flexible relationships over exact line counts, image orientations, or paragraph lengths.
- Ecommerce: use expression for storytelling, campaigns, collections, and product context without destabilizing core shopping interactions.
- Application UI: favor predictability in repeated workflows; reserve expression for onboarding, overviews, reports, empty states, or editorial surfaces.
- Long-form editorial: protect reading continuity while using annotation fields, image structures, pull quotes, chapter breaks, and caption relationships.
- Portfolio: vary project composition while preserving shared structural anchors.
- Very little content: prefer a simple asymmetric frame over unjustified compound complexity.
- Very dense content: organize hierarchy, grouping, and reading order before adding expression.
- Conflict with the visual system: let the grid serve the approved system rather than compete with it.

## Related skills

Use before this skill when appropriate:

- `design-problem-framer`
- `graphic-universe-builder`
- `story-led-website-concept`
- `design-direction-decision`
- `brand-derived-visual-system`

Use alongside or after this skill when appropriate:

- `layout-direction-explorer`
- `layout-art-direction`
- `responsive-behavior-planner`
- `layout-principles-review`

