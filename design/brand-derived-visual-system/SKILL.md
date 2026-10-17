---
name: brand-derived-visual-system
description: Derives a compact, project-specific visual system from an approved creative concept and authentic brand, product, process, history, or research material. Use when a website or digital brand needs a coherent visual grammar for typography, imagery, composition, shape, motion, and expressive intensity without creating a coded component library or heavyweight design-system specification.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: generator
  audience: web-designers-and-creative-directors
  tags:
    - visual-system
    - creative-direction
    - art-direction
    - brand-language
    - visual-grammar
    - design-principles
    - brand-expression
  status: draft
  side_effects: none
---

# Brand-Derived Visual System

## Purpose

Turn an approved creative direction into a compact, reusable visual grammar derived from authentic project material.

Identify the smallest set of visual principles that can make the project recognizable across layouts, content types, screen sizes, channels, and levels of expression. Explain why the project looks and behaves this way, how the language may vary, and what must remain recognizable.

This skill creates a visual grammar, not a coded product design system. It may define composition, shape, framing, typography behavior, color roles, imagery, graphic devices, texture, motion, and expressive intensity. It must not create components, design tokens, CSS, Storybook, component states, APIs, or frontend architecture.

## Core principle

Derive before decorating:

```txt
project source
-> conceptual meaning
-> visual principle
-> system rule
-> flexible applications
```

Avoid starting with a fashionable treatment and retrofitting a project rationale. Every important system decision should trace back to project evidence.

## When to use this skill

Use this skill when:

- A creative concept or direction has already been selected.
- The user asks for a visual system, visual language, visual grammar, brand-expression system, or art-direction system.
- Strong source material exists, but individual screens or channels feel inconsistent.
- Brand guidelines do not adequately explain digital expression.
- A campaign needs a distinctive expression that remains connected to a parent brand.
- A team needs to distinguish essential visual ingredients from optional ones.
- One identity must work at quiet, standard, and expressive intensities.

Do not use this skill when:

- The project problem, concept, or direction is still unresolved.
- The request is broad visual research or comparison between competing concepts.
- The task is an audit of an existing execution rather than generation of a new grammar.
- The user needs a component library, tokens, CSS architecture, exact grid, implementation code, or final production design.
- The request is only typography selection, color specification, or motion implementation.

## Inputs to inspect

Inspect the smallest useful set of available material:

- Approved concept: thesis, essential meaning, audience, narrative lens, desired character, evidence, rationale, and constraints.
- Graphic-universe research: project vocabulary, reference clusters, visual atoms, meaningful metaphors, category clichés, and project-owned opportunities.
- Existing identity: logo, wordmark, symbols, palette, typography, imagery, illustration, iconography, patterns, campaigns, signage, motion, digital products, and brand rules.
- Project-specific material: product form or behavior, materials, process, diagrams, data structures, language, archive, history, geography, architecture, and environments.
- Practical constraints: channels, content types, viewport range, production budget, available assets, accessibility, localization, CMS, and parent-brand restrictions.

Before continuing, establish:

```txt
Approved concept:
Meaning to communicate:
Existing brand connection:
Fixed assets or rules:
Authentic project-specific sources:
Required content and channels:
Practical constraints:
```

If the concept is unresolved, report the missing decision and route the work to concept selection. Do not invent a visual system to hide an unclear concept.

## Workflow

### 1. Restate the direction

Summarize the concept, essential meaning, audience, desired character, narrative mechanism, evidence, and constraints.

Write a system brief:

```txt
The visual system must communicate <meaning>
by consistently expressing <qualities>
without compromising <constraints>.
```

### 2. Inventory authentic sources

List material that could generate the visual language. Do not assume the logo must be the source.

| Source | Type | Connection to concept | Visual potential | Authenticity |
|---|---|---|---|---|

Consider identity, product, process, environment, history, language, information structure, and graphic-universe findings.

### 3. Rank source strength

Evaluate each candidate for:

- Authenticity: it genuinely belongs to the project.
- Meaning: it reinforces the approved concept.
- Distinctiveness: competitors could not credibly own it as easily.
- Flexibility: it can generate different applications.
- Simplicity: the principle can be explained and remembered.
- Extensibility: it survives across formats and channels.
- Restraint: it remains recognizable without dominating every composition.

Classify candidates as `primary`, `supporting`, `experimental`, or `reject`. Prefer one primary source and one or two supporting sources.

### 4. Write the system thesis

Use:

```txt
The system derives <visual behavior> from <project source>
to communicate <meaning>.
```

Reject theses that reduce to aesthetic labels such as "bold, modern, and minimal."

### 5. Derive the core principles

Create approximately three to five memorable principles. Each principle must describe behavior, not appearance.

For each principle, record:

```txt
Principle:
Project origin:
Meaning:
Affects:
Do:
Do not:
```

Useful principle shapes include "Frame rather than contain," "Show transformation instead of decoration," and "Let technical detail become graphic detail." Treat these as reasoning examples, not reusable style presets.

### 6. Separate consistency from freedom

Define invariants and variables:

| System element | Invariant | Variable | Why |
|---|---|---|---|

Then classify each ingredient:

| Element | Role | Required / Optional / Experimental | Appropriate when | Avoid when |
|---|---|---|---|---|

Do not make every ingredient mandatory. A system that repeats one exact recipe is a template, not a flexible visual language.

### 7. Define the visual grammar

Describe directional behavior for:

- Composition and spatial relationships
- Shape language
- Framing and boundaries
- Typography roles and hierarchy
- Identity, functional, and expressive color roles
- Imagery subject, crop, distance, light, texture, and relationship to text
- Graphic devices
- Texture and material
- Iconography and illustration, when relevant

Define relationships rather than exact grids, typefaces, color values, or complete icon sets unless the user explicitly requests those decisions.

Read [references/visual-grammar-guide.md](references/visual-grammar-guide.md) when the task needs detailed prompts for these dimensions, motion, application testing, source patterns, or anti-pattern diagnosis.

### 8. Derive the motion grammar

Extract verbs already present in the concept, product, or process, such as `assemble`, `focus`, `connect`, `expand`, `compress`, `reveal`, `align`, or `transform`.

For each proposed behavior, record its source, meaning, possible uses, and misuse condition. Classify motion as:

- Functional: communicates state, hierarchy, relationship, or change.
- Narrative: supports progression, transformation, or reveal.
- Signature: a restrained, recognizable project-specific behavior.
- Decorative: optional atmosphere that carries no essential meaning.

Specify what moves, what remains stable, what triggers motion, how often signature motion appears, and what replaces it under reduced motion. Never make critical meaning depend exclusively on animation.

### 9. Define expression levels

Create three intensities that remain recognizably one system:

- Quiet: long-form reading, legal content, forms, documentation, dense information, and secondary pages.
- Standard: ordinary marketing, product explanation, services, and case studies.
- Expressive: heroes, launches, chapter openings, campaigns, and major proof moments.

| Dimension | Quiet | Standard | Expressive |
|---|---|---|---|
| Typography | | | |
| Composition | | | |
| Imagery | | | |
| Graphic devices | | | |
| Texture | | | |
| Motion | | | |

Expression levels amplify or remove ingredients; they do not create three separate identities.

### 10. Stress-test the grammar

Test representative content and formats without fully designing them:

- Hero and high-expression moment
- Long-form or legal page with most expressive devices removed
- Product or service explanation
- Process, statistics, testimonial, case study, and CTA
- Navigation and footer
- Sparse and dense content
- Wide, portrait, square, small, and large formats
- Mobile viewport
- Any required non-web channels

For each test, note which principles remain, which variables change, which optional devices disappear, and what preserves recognition.

Run an accessibility and resilience check covering contrast, legibility, reading order, zoom, reflow, reduced motion, touch, keyboard use, and cognitive load. Separate brand signature from information required for comprehension.

### 11. Distill the system

Remove rules that duplicate another principle, document a single mockup, lack a meaningful source, require constant exceptions, restrict useful variation, or are too complex to remember.

Finish with a memory-sized system:

```txt
1 system thesis
3-5 core principles
3-6 essential ingredients
3 expression levels
a short list of prohibitions
```

### 12. Explain the rationale and handoff

Connect every final principle to the project:

| Principle | Project source | Business or concept relevance | Expected effect |
|---|---|---|---|

State what is ready for layout exploration, what needs visual prototyping, which brand or accessibility questions remain, and which production dependencies must be resolved downstream.

## Output format

Return:

```md
## Visual System Brief

Project:
Approved concept:
Essential meaning:
Audience:
Desired visual character:
Existing identity constraints:
Primary channels:

## Source Inventory

| Source | Type | Concept relevance | Visual potential | Decision |
|---|---|---|---|---|

## System Foundation

Primary source:
Supporting sources:
System thesis:
Why this source is appropriate:

## Core Principles

### Principle 1 — <name>

Project origin:
Meaning:
Affects:
Do:
Do not:

## System Invariants and Variables

| Element | Invariant | Variable | Reason |
|---|---|---|---|

## Visual Ingredients

| Element | Source | Role | Requirement | Risk |
|---|---|---|---|---|

## Visual Grammar

Composition:
Shape:
Framing:
Typography:
Color:
Imagery:
Graphic devices:
Texture or material:
Iconography or illustration:

## Motion Grammar

Source verbs:
Functional motion:
Narrative motion:
Signature motion:
Decorative motion:
Reduced-motion principle:

## Expression Levels

| Dimension | Quiet | Standard | Expressive |
|---|---|---|---|

## Application Tests

| Context | Principles used | Variables changed | Expression level | Notes |
|---|---|---|---|---|

## Misuse Conditions

- ...

## Accessibility and Resilience

Contrast:
Typography:
Motion:
Responsive simplification:
Content order:

## Memory-Sized System

Thesis:
Core principles:
Essential ingredients:
Optional ingredients:
Never:

## Handoff

Ready for layout exploration:
Needs visual prototyping:
Open brand questions:
Production dependencies:
Accessibility questions:
Recommended next workflow:
```

Adapt the sections to the evidence. Mark unknowns instead of inventing certainty.

## Quality bar

The task is complete only when:

- An approved concept exists and the primary system source is explicit.
- The thesis connects authentic source, visual behavior, and meaning.
- Approximately three to five memorable principles describe behavior rather than aesthetic labels.
- Invariants and variables are separated.
- Required, optional, and experimental ingredients are distinguished.
- Typography, imagery, color, composition, graphic devices, and relevant motion form one coherent grammar.
- Exact typefaces, color values, grids, and implementation details are deferred unless explicitly requested.
- Quiet, standard, and expressive levels remain recognizably one system.
- The system works beyond the hero, across sparse and dense content, and on narrow screens.
- Recognition survives when most expressive devices are removed.
- Important decisions are traceable to project or business relevance.
- Accessibility risks and responsive simplifications are explicit.
- Weak or unnecessary rules have been removed.
- The output remains a compact visual grammar rather than becoming a component or token specification.

## Edge cases

- No established identity: derive from the approved concept, product, process, language, environment, or audience transformation; mark identity decisions as provisional.
- Strong brand guidelines: preserve mandatory rules and focus on digital behavior rather than redesigning the identity.
- Rebrand in scope: identify system hypotheses, but do not silently redefine the logo, naming, positioning, or brand architecture.
- Parent brand plus campaign: separate parent-brand invariants from campaign variables.
- Multiple audiences: vary content and intensity, not the core identity.
- Highly functional product UI: keep operational surfaces quiet or functional while using stronger expression on marketing surfaces.
- Accessibility conflict: constrain, replace, or make the expressive device optional while preserving its underlying principle.
- Source is too literal: abstract from the object's behavior or meaning rather than repeating its image.
- Too many strong sources: select one primary source and demote the rest to supporting or experimental.

## Related skills

Use before this skill when appropriate:

- `design-problem-framer`
- `graphic-universe-builder`
- `story-led-website-concept`
- `design-direction-decision`

Use after this skill when appropriate:

- `layout-principles-review`
- `ui-design-direction-builder`

