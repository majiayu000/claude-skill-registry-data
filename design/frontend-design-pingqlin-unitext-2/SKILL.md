---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications; when they want critique, polish, or hardening passes for an existing frontend; or when they reference impeccable or impeccable.style as the desired design bar. Generates creative, polished code and UI design that avoids generic AI aesthetics and repetitive AI UI patterns.
license: Complete terms in LICENSE.txt
metadata:
  runtime_support_files: true
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details, critique discipline, and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

If you need the distilled upstream notes from `impeccable.style`, including anti-pattern clusters and the compatibility decision for this registry, read [references/impeccable-style-notes.md](./references/impeccable-style-notes.md).

## Context Gathering Protocol

Before coding, build a usable design brief from the request and repo context:

- **Purpose**: what problem does this interface solve and what action should it make easier?
- **Audience**: who is using it and what level of visual ambition can they tolerate?
- **Surface**: is this a marketing page, product UI, dashboard, internal tool, artifact, or experimental page?
- **Constraints**: framework, design system, performance envelope, accessibility expectations, mobile scope, and browser/runtime constraints
- **Existing language**: if the repo already has a visual system, list what must be preserved and what can be pushed further
- **Memorable move**: identify the one thing a user should remember after seeing the page

Do not jump straight into component assembly. Decide the content hierarchy and aesthetic thesis first.

## Anti-Attractor Preflight

Before implementation, explicitly list the reflex defaults you are refusing for this output. Use 3 to 6 concrete rejects, for example:

- `Inter` or other safe default sans by reflex
- purple/cyan gradient-on-white startup aesthetics
- centered hero with pill badge, headline, paragraph, two CTAs, and generic social proof strip
- identical feature-card grids with icon tile above heading
- nested cards, nested shadows, and indiscriminate glassmorphism
- mobile layout that just amputates density instead of redesigning the composition

If the current concept still sounds like a template, it is not ready yet.

## Design Direction

Commit to a BOLD aesthetic direction before building:

- **Tone**: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, or another clearly named direction
- **Contrast model**: sparse vs dense, quiet vs loud, precise vs expressive, geometric vs human, polished vs raw
- **Signature element**: define what makes the surface unforgettable: type treatment, composition logic, motion system, illustration style, framing device, or interaction pattern

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is production-grade, functional, visually striking, cohesive, and meticulously refined.

## Execution Workflow

Work in passes instead of trying to "get it right" in one draft:

1. **Frame the surface**
   - establish content hierarchy, layout skeleton, and responsive intent
   - decide where asymmetry, overlap, restraint, or density belong
2. **Establish the visual language**
   - select typography with character
   - define palette, contrast, spacing rhythm, borders, and background treatment
   - set CSS variables or tokens early so the surface feels authored rather than improvised
3. **Build the focal moments**
   - create one or two high-impact moments instead of sprinkling weak detail everywhere
   - examples: hero composition, navigation behavior, reveal sequence, editorial section transition, dramatic data framing
4. **Critique the result**
   - compare the output against the anti-attractor list
   - remove template-like patterns, repeated card logic, and low-signal ornament
   - strengthen weak typography, spacing, and hierarchy before adding more decoration
5. **Polish and harden**
   - verify empty/loading/error states when relevant
   - verify desktop and mobile layouts separately instead of assuming one scales into the other
   - keep accessibility, interaction clarity, and implementation integrity intact

For existing frontends, begin with critique and preservation:

- identify what already works and should be amplified
- identify what is generic, repetitive, or visually confused
- replace weak motifs with one coherent system instead of layering more effects on top

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic defaults like Arial and Inter by reflex. Pair a distinctive display voice with a refined body voice, and make the hierarchy visible without relying on huge font jumps alone.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Do not default to purple gradients, blue-glow SaaS chrome, or interchangeable dark mode.
- **Motion**: Use animation intentionally. Prioritize one orchestrated sequence or interaction family over scattered micro-motions. Use scroll-triggering, hover states, and reveal cadence that feel owned by the concept.
- **Spatial Composition**: Favor unexpected layouts, asymmetry, overlap, diagonal flow, grid-breaking elements, generous negative space, or controlled density when the concept calls for it.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Use textures, meshes, patterns, transparencies, shadows, borders, cursors, and grain only when they reinforce the chosen direction.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

## Strong Don'ts

- Do not hide weak layout thinking behind fancy gradients or animation noise
- Do not keep adding cards, badges, and separators when the hierarchy is unclear
- Do not use every accent everywhere; concentrate emphasis
- Do not let desktop and mobile share the exact same composition logic by default
- Do not preserve an existing design-system pattern when it is the reason the result feels generic

Remember: Claude is capable of extraordinary creative work. Don't hold back, but make the ambition legible, usable, and technically real.
