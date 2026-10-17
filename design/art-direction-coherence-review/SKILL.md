---
name: art-direction-coherence-review
description: Reviews an existing website, mockup, prototype, or design execution for whether content, typography, imagery, composition, motion, interaction, responsiveness, and accessibility coherently express the intended creative concept. Use when a design feels fragmented, over-designed, generic despite a strong concept, inconsistent across sections, or drifted from its approved art direction.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: review
  audience: web-designers-product-designers-creative-directors-brand-teams
  tags:
    - art-direction
    - creative-direction
    - coherence
    - design-review
    - visual-system
    - storytelling
    - concept-drift
  status: draft
  side_effects: none
---

# Art Direction Coherence Review

## Purpose

Review whether an existing design communicates one clear creative idea through the combined behavior of its content, visual language, layout, imagery, typography, motion, interaction, and interface language.

Compare:

```txt
intended meaning
      ↕
actual execution
      ↕
likely perceived meaning
```

The goal is conceptual coherence, not perfect visual consistency. Different pages and sections may vary substantially when those differences serve the same underlying meaning.

## Core principle

Art direction should create a traceable relationship:

```txt
meaning → content → presentation → perception
```

For each major decision, ask:

- What is this trying to communicate?
- Why is it presented this way?
- Does that presentation strengthen the intended meaning?
- What is the audience likely to perceive instead?

A visually impressive decision that weakens meaning is not automatically successful.

Coherence is not sameness. Do not require identical layouts, typography, crops, density, animation, or decorative devices. Ask whether variation is a purposeful expression of one concept or an accumulation of unrelated ideas.

## When to use this skill

Use this skill when:

- A website, page, mockup, prototype, or design system has already been substantially designed.
- A strong concept existed earlier, but the execution now feels fragmented, generic, over-designed, or under-directed.
- Individual sections work in isolation but do not feel like one experience.
- Copy, imagery, typography, motion, and interaction appear to express different personalities.
- Several contributors or responsive adaptations may have introduced concept drift.
- A team wants an art-direction QA pass before implementation or launch.
- The user wants to know which ideas to preserve, strengthen, reduce, or remove.

Do not use this skill when:

- The project lacks a defined purpose or audience; use `design-problem-framer`.
- The user needs initial creative concepts; use `story-led-website-concept` or another concept-generation skill.
- The user wants to choose between unresolved directions; use `design-direction-decision`.
- The main question is whether the design unmistakably belongs to the brand; use `website-distinctiveness-review`.
- The main issue is detailed spacing, alignment, proportion, rhythm, or balance; use `layout-principles-review`.
- The task is a full accessibility, performance, or implementation audit.
- The user asks to redesign or code the interface rather than review it.

## Inputs to inspect

Inspect the smallest useful set of available evidence.

Execution evidence may include:

- Live websites, prototypes, screenshots, Figma frames, page mockups, or mobile designs
- Motion prototypes, recordings, and interaction specifications
- More than one page, section, state, or viewport when making system-wide claims

Intended-direction evidence may include:

- Approved concept, creative brief, narrative lens, or design rationale
- Essential meaning, audience transformation, story spine, and desired perception
- Visual-system thesis, core principles, invariants, variables, expression levels, and motion or layout principles
- Brand strategy, messaging, tone of voice, positioning, product goals, and business constraints

Content evidence may include:

- Headings, body copy, labels, CTAs, captions, testimonials, case studies, data, imagery, video, and product information

Art direction cannot be reviewed separately from content. If important evidence is unavailable, state the limitation and narrow the claims.

## Review modes

Choose the mode that matches the evidence:

- **Concept-to-execution:** Compare the design directly with approved concept or system documentation. This provides the strongest evidence.
- **Execution-only:** Infer the apparent art direction cautiously, label it as inferred, and review internal coherence only.
- **Section:** Limit conclusions to the supplied section or component. Do not infer site-wide inconsistency.
- **Cross-page:** Review continuity, purposeful variation, repeated signals, and concept survival across pages.
- **Responsive:** Review whether the same concept survives transformation across viewports rather than demanding desktop fidelity.

## Workflow

1. **Scope the evidence and mode.** Identify the artifact, available views and states, missing evidence, review mode, and confidence. Separate confirmed facts from inference.

2. **Establish the intended meaning.** Summarize the concept, essential meaning, audience, desired perception, narrative mechanism, visual-system thesis, and core principles. Condense the baseline to:

   ```txt
   The experience should make <audience>
   understand or feel <meaning>
   through <conceptual mechanism>.
   ```

3. **Infer the perceived meaning independently.** Temporarily set aside the written rationale and record the apparent personality, promise, emotional tone, trust level, narrative, and priorities. Do not invent a detailed brief from screenshots.

4. **Compare intention with perception.** For core idea, personality, tone, value proposition, audience relationship, and trust, classify alignment as `supports`, `partially supports`, `neutral`, `contradicts`, or `unverified`. Identify the strongest current signal and whether it deserves to dominate.

5. **Review the execution layers.** Evaluate content, voice, typography, imagery, visual-system behavior, composition, expression level, motion, interaction, responsiveness, accessibility, usability, and proportional expressive cost. Use [references/evaluation-framework.md](references/evaluation-framework.md) for the detailed questions and tests. Omit lenses unsupported by evidence.

6. **Locate drift and contradictions.** Identify where the concept remains strongest, begins to weaken, disappears, or is replaced by unrelated ideas. Run the substitution and generic-fallback tests locally. Record cross-layer contradictions explicitly rather than averaging them into a vague score.

7. **Preserve strengths.** Name the strongest concept expression, system application, content-form relationship, signature moment, and responsive adaptation. Mark effective decisions as `preserve` before recommending changes.

8. **Prioritize conceptual corrections.** Classify findings as `critical`, `high`, `medium`, or `low` by conceptual and user impact. Prefer the smallest correction that restores an existing principle: remove an unrelated effect, reuse a known system rule, change an image's role, or simplify an expression. Do not redesign by reflex.

9. **Choose a verdict and report.** Use one verdict: `coherent`, `mostly coherent`, `fragmented`, `concept drift`, `over-directed`, `under-directed`, or `insufficient evidence`. Follow [references/report-template.md](references/report-template.md), keeping the report proportional to the evidence and number of meaningful findings.

## Scope boundaries

### Distinctiveness

Coherence asks, “Do the design and content decisions reinforce the same intended idea?” Distinctiveness asks, “Could this identity unmistakably belong to this brand rather than its competitors?” A design may be coherent and generic, or distinctive and incoherent. Identify local generic fallback zones only when they cause concept drift; route an identity-wide ownership question to `website-distinctiveness-review`.

### Layout craft

This skill may find that composition does not support the narrative hierarchy. It does not perform a microscopic audit of spacing, alignment, proportion, rhythm, or grid execution; route those concerns to `layout-principles-review`.

### Accessibility and usability

Accessibility problems must not be defended as artistic expression. Identify tensions and propose an alternative treatment that preserves the underlying concept where possible. Do not replace WCAG, keyboard, screen-reader, focus, semantic, contrast, or usability testing.

### Performance

Ask whether costly media, 3D, canvas, font, or animation behavior is central enough to justify specialist optimization. Do not claim technical performance results without measurements.

### Implementation

Do not write HTML, CSS, JavaScript, final copy, a new visual system, or a new grid. This skill reviews and recommends only.

## Output format

Return:

- An art-direction verdict, confidence level, intended meaning, perceived meaning, and main gap
- Evidence-backed strengths to preserve
- A coherence matrix containing only supported layers
- Concept drift, contradictions, and generic fallback zones when present
- Expression balance and responsive findings when evidence exists
- Accessibility and usability tensions without presenting them as a full audit
- A short, prioritized set of conceptual corrections tied to existing principles
- The smallest useful specialist handoff, if one is needed

Use the detailed structure in [references/report-template.md](references/report-template.md). Do not fill empty sections with generic advice.

## Quality bar

The task is complete only when:

- Intended meaning is identified or explicitly marked unavailable.
- Intended and perceived meaning are compared using visible or supplied evidence.
- Content and presentation are reviewed together.
- Differences are tested for conceptual purpose rather than treated as inconsistency by default.
- Typography, imagery, composition, motion, and interaction are evaluated as meaning-bearing choices when evidence supports them.
- Invariants are distinguished from variables, and quiet moments from expressive peaks.
- Concept drift and cross-layer contradictions are named precisely.
- Responsive adaptations are judged by conceptual survival rather than desktop fidelity.
- Accessibility and usability take priority over a particular execution technique without making creative expression expendable.
- Strong existing decisions are explicitly preserved.
- Recommendations use existing project principles before inventing new visual ideas.
- Findings are prioritized by conceptual impact, not personal taste.
- Claims remain within the available evidence and specialist issues are routed rather than duplicated.

## Edge cases

- **One screenshot:** Review only visible meaning, hierarchy, typography, imagery, composition, and system signals. Do not claim cross-page, responsive, motion, interaction, or navigation coherence.
- **No approved concept:** Infer the apparent direction cautiously. If no organizing idea is visible, use `under-directed`; do not invent an intention after the fact.
- **Documentation conflicts with execution:** Treat the execution as evidence and state, “The documented concept says X; the design currently communicates Y.”
- **Several concepts are intentional:** Check whether they resolve into one higher-level direction. Alternating unrelated concepts is fragmentation.
- **Strong brand, weak page concept:** Separate brand coherence from page or story coherence.
- **Minimal design:** Review precision, editing, typography, imagery, pacing, and voice; restraint is not absence of direction.
- **Maximal design:** Do not penalize density automatically; test whether the density belongs to one coherent world.
- **Utility-heavy interface:** Permit quieter expression and prioritize clarity, hierarchy, tone, and recognizable identity.
- **Strong desktop, weak mobile:** Preserve essential conceptual signals through a simpler transformation rather than reproducing every desktop effect.

## Related skills

- `design-problem-framer` — establishes purpose, audience, constraints, and the communication problem.
- `graphic-universe-builder` — develops project-specific visual research territories.
- `story-led-website-concept` — defines the narrative concept and essential meaning.
- `design-direction-decision` — selects which developed concept should proceed.
- `brand-derived-visual-system` — defines the visual grammar, principles, invariants, and variables.
- `expressive-grid-planner` — translates an approved concept and visual system into responsive layout strategy.
- `website-distinctiveness-review` — evaluates brand ownership and category distinctiveness.
- `layout-principles-review` — reviews hierarchy, balance, proportion, alignment, repetition, and flow in detail.
- `motion-experience-director` — develops motion behavior when motion coherence is the dominant weakness.
- Accessibility specialist skills — review semantics, keyboard interaction, focus, announcements, contrast, motion, and WCAG-related concerns.
