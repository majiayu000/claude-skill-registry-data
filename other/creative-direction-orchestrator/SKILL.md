---
name: creative-direction-orchestrator
description: Coordinate a stage-aware, evidence-led creative-direction workflow for broad or high-impact digital design work. Use when a user needs one coherent strategy for a new or redesigned website, landing page, product experience, campaign, or flagship interface; needs visual research turned into concepts; needs competing directions resolved; needs a chosen direction translated into a visual system or expressive layout; or needs an executed design checked for concept drift and coherence. Route to the smallest relevant workflow skills and convene a focused specialist council only when material creative tensions remain. Do not use for a small UI fix, approved-design implementation, isolated copywriting, a single accessibility audit, or purely technical debugging.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: planner
  audience: web-designers-creative-directors-product-teams
  tags:
    - creative-direction
    - orchestration
    - design-strategy
    - concept-development
    - visual-system
    - art-direction
    - design-review
  status: draft
  side_effects: none
---

# Creative Direction Orchestrator

## Purpose

Coordinate a coherent creative-direction process across research, concept development, visual-system definition, layout planning, specialist debate, and design review.

The orchestrator should not perform every possible design workflow on every project.

Its job is to determine:

```txt
Where is the project now?

What decision is actually unresolved?

Which evidence is missing?

Which specialist workflow can resolve it?

Which tensions require multiple perspectives?

What is the smallest sequence that can reach a defensible decision?
```

Use specialist workflow skills to generate structured evidence.

Use specialist creative-director perspectives to challenge important decisions.

Then synthesize those inputs into one coherent direction.

Do not produce seven disconnected redesign ideas or run every available specialist merely because they exist.

---

# Core orchestration model

Treat creative direction as a staged system:

```txt
UNDERSTAND
design-problem-framer
        ↓
DISCOVER
graphic-universe-builder
        ↓
CONCEPTUALIZE
story-led-website-concept
        ↓
DECIDE
design-direction-decision
        ↓
SYSTEMIZE
brand-derived-visual-system
        ↓
STRUCTURE
expressive-grid-planner
        ↓
DESIGN EXECUTION
        ↓
VERIFY CONCEPT
art-direction-coherence-review
        ↓
VERIFY CRAFT
layout-principles-review
```

This is a routing model, not a mandatory waterfall.

Start at the earliest unresolved stage relevant to the user's request.

Stop when the requested decision has been reached.

Do not automatically run downstream stages.

---

# Two kinds of specialists

The orchestrator uses two different types of specialist capability.

## Workflow skills

Workflow skills perform bounded jobs and return structured artifacts.

Examples:

* `design-problem-framer`
* `graphic-universe-builder`
* `story-led-website-concept`
* `design-direction-decision`
* `brand-derived-visual-system`
* `expressive-grid-planner`
* `art-direction-coherence-review`
* `layout-principles-review`
* `website-distinctiveness-review`

Use these to establish evidence, generate artifacts, or validate execution.

Do not treat them as fictional council personalities.

---

## Council perspectives

Council perspectives challenge the problem from different professional viewpoints.

Available perspectives:

* `provocative-concept-director` — premise, tension, cultural angle, surprise, and differentiation.
* `experimental-web-art-director` — visual expression, art direction, composition, atmosphere, and signature moments.
* `minimalist-brand-director` — restraint, recognition, system coherence, and unnecessary-element removal.
* `editorial-digital-designer` — hierarchy, typography, pacing, content relationships, and responsive composition.
* `conversion-creative-director` — decision path, proof, objections, trust, and calls to action.
* `motion-experience-director` — behavior, feedback, pacing, interaction character, and reduced motion.
* `creative-technologist` — browser feasibility, progressive enhancement, performance, fallback strategy, and production phasing.

Council perspectives debate decisions.

Workflow skills create or validate the material being debated.

Do not confuse the two.

---

# Start with project-state detection

Before convening a council or generating directions, inspect the smallest relevant set of:

* project material
* prior design artifacts
* research
* existing website or mockups
* technical constraints
* prior specialist outputs

Separate:

### Evidence

Known from supplied material or verified sources.

### Constraint

Something the direction must respect.

### Inference

A reasonable interpretation that has not been verified.

### Open question

Missing information that could materially change the direction.

Create a shared frame:

```txt
Project:
Audience:
Primary message:
Primary action:
Current state:
Current problem:
Desired outcome:
Fixed constraints:
Excluded work:
Available evidence:
Unverified assumptions:
Central design question:
```

Do not repeat work already supported by a strong upstream artifact.

---

# Determine the current creative-direction stage

Classify the project at the earliest unresolved stage.

## Stage 1 — Problem framing

Signals:

* audience is unclear
* business transformation is vague
* everyone is discussing aesthetics before purpose
* primary message is unresolved
* success criteria are unclear

Route to:

`design-problem-framer`

Expected result:

```txt
clear design problem
audience
transformation
communication objective
constraints
central design question
```

Do not proceed to visual research while the core problem remains materially ambiguous.

---

## Stage 2 — Graphic-universe discovery

Signals:

* project is understood
* visual language is not
* design feels generic or trend-led
* references are mostly competitor websites
* there is no authentic visual source
* project-specific metaphors have not been explored

Route to:

`graphic-universe-builder`

Expected result:

```txt
project vocabulary
research territories
reference clusters
category clichés
visual atoms
metaphor candidates
candidate graphic universes
```

Use this stage to expand the creative source material.

Do not choose the final visual direction here.

---

## Stage 3 — Story-led concept development

Signals:

* strategic problem is understood
* research exists
* the website still lacks a central idea
* sections feel like features rather than a coherent experience
* multiple narrative possibilities exist

Route to:

`story-led-website-concept`

Expected result:

```txt
essential meaning
audience transformation
narrative opportunities
2–3 coherent concepts
story spines
section narratives
evidence plans
directional visual implications
```

This is usually where council perspectives add the most value.

---

## Stage 4 — Direction decision

Signals:

* two or more credible concepts exist
* stakeholders disagree
* strengths and sacrifices need comparison
* no dominant direction has been selected

Route to:

`design-direction-decision`

Use council evidence when the trade-off is substantial.

Expected result:

```txt
selected direction
preserved strengths
accepted sacrifices
rejected alternatives
remaining validation
```

Do not create a Frankenstein hybrid merely to satisfy every preference.

---

## Stage 5 — Visual-system derivation

Signals:

* creative direction is selected
* screens still depend on individual designer taste
* visual rules are inconsistent
* the concept lacks a reusable visual grammar
* project-specific visual material needs distillation

Route to:

`brand-derived-visual-system`

Expected result:

```txt
system thesis
primary source
3–5 core principles
invariants
variables
visual grammar
motion grammar
quiet / standard / expressive modes
application logic
```

Do not turn this stage into a coded component design system.

---

## Stage 6 — Structural layout planning

Signals:

* visual system is clear
* page structure remains generic
* content does not fit standard layout patterns
* hierarchy needs spatial expression
* compound, modular, asymmetric, or editorial structures may help

Route to:

`expressive-grid-planner`

Expected result:

```txt
content hierarchy
structural requirements
2–3 grid directions when useful
composition behavior
whitespace strategy
intentional grid violations
responsive transformation
recommended structure
```

Do not write CSS during this stage.

---

## Stage 7 — Art-direction validation

Signals:

* a mockup, prototype, or website exists
* the concept may have drifted during execution
* sections feel disconnected
* the visual system is inconsistently applied
* motion, imagery, copy, and composition conflict
* the design is over-directed or under-directed

Route to:

`art-direction-coherence-review`

Expected result:

```txt
art-direction verdict
intended vs perceived meaning
coherence matrix
concept drift
contradictions
generic fallback zones
priority corrections
elements to preserve
```

---

## Stage 8 — Craft validation

Signals:

* concept is coherent
* remaining problems concern composition quality
* hierarchy, proportion, rhythm, spacing, balance, alignment, or flow need refinement

Route to:

`layout-principles-review`

This should normally occur after conceptual problems have been resolved.

Do not polish a structurally wrong idea.

---

# Optional specialist validation

Some projects require additional review outside the primary sequence.

## Distinctiveness

Use:

`website-distinctiveness-review`

when the dominant question is:

```txt
Could this design credibly belong to several competitors?
```

Distinctiveness and coherence are related but different.

A design may be:

```txt
coherent + generic
```

or:

```txt
distinctive + incoherent
```

---

## Accessibility

Use relevant accessibility skills when questions concern:

* semantics
* keyboard access
* focus
* screen readers
* WCAG
* contrast
* target size
* zoom
* reflow

The orchestrator should protect an accessible baseline but should not impersonate a full accessibility audit.

---

## Technical feasibility

Use `creative-technologist` when the proposed direction materially depends on:

* WebGL
* canvas
* complex motion
* real-time effects
* large media
* experimental browser APIs
* advanced responsive behavior
* difficult progressive enhancement

Do not burden simple designs with a technical feasibility council when standard frontend implementation is sufficient.

---

# Decide whether a council is actually needed

Do not convene a council automatically.

Use a council only when at least two material creative tensions exist.

Examples:

```txt
expression vs comprehension

brand restraint vs differentiation

storytelling vs conversion speed

editorial composition vs CMS flexibility

motion ambition vs accessibility

immersive experience vs performance

novel interaction vs familiar usability

brand consistency vs campaign distinction
```

If the problem is narrow and one workflow skill can resolve it, route directly to that skill.

---

# Select the smallest useful council

Use three or four council perspectives for a bounded problem.

Use the full council only when:

* the project is a flagship experience
* the concept is highly ambiguous
* several major design systems collide
* the user explicitly requests a broad council

Record:

```txt
Included perspectives:
Why each is needed:

Excluded perspectives:
Why they are unnecessary:

Decision expected from the council:
```

---

# Council selection signals

## Provocative concept director

Include when:

* concepts feel obvious
* differentiation is weak
* the central premise lacks tension
* the category is saturated
* an experimental wildcard is appropriate

---

## Experimental web art director

Include when:

* visual expression is strategically important
* signature moments are unresolved
* the concept needs stronger experiential form
* the website is a campaign, portfolio, cultural experience, or flagship brand site

---

## Minimalist brand director

Include when:

* the concept has too many ideas
* brand recognition is weak
* visual devices are accumulating
* system coherence and restraint are major concerns

---

## Editorial digital designer

Include when:

* content hierarchy is complex
* typography matters strongly
* the page is editorial or content-rich
* composition, pacing, and responsive structure are major concerns

---

## Conversion creative director

Include when:

* the primary action is commercially important
* user objections are substantial
* the experience risks hiding the offer behind storytelling
* proof, trust, pricing, lead generation, or purchase behavior matter strongly

---

## Motion experience director

Include when:

* motion carries concept or narrative
* interaction character is central
* the design relies on scrolling or transitions
* reduced-motion behavior requires strategic decisions

---

## Creative technologist

Include when:

* technical feasibility could materially constrain the direction
* fallback behavior affects the concept
* performance cost may be substantial
* the experience depends on advanced browser capabilities

---

# Read the council playbook

When council mode is selected, read the [council playbook](references/council-playbook.md).

Use it for:

* independent specialist positions
* position normalization
* conflict handling
* candidate comparison
* direction selection

Do not claim to have used the playbook when it is unavailable.

---

# Downstream orchestration

Once a direction is selected, determine what is still missing.

## If the visual language remains undefined

Run:

`brand-derived-visual-system`

---

## If the visual system exists but layout remains generic

Run:

`expressive-grid-planner`

---

## If design execution already exists

Do not regenerate upstream strategy automatically.

Run:

`art-direction-coherence-review`

Then use specialist reviews only for identified weaknesses.

---

## If conceptual coherence is strong but craft is weak

Run:

`layout-principles-review`

---

## If the design is coherent but generic

Run:

`website-distinctiveness-review`

Possible follow-up:

`graphic-universe-builder`

when the root problem is insufficient project-specific source material.

---

# Review loop

The orchestrator may use a bounded loop:

```txt
direction
→ execution
→ coherence review
→ targeted correction
→ re-review
```

Do not reopen the entire creative process for every local issue.

Escalate upstream only when the review identifies a foundational problem.

Example:

```txt
button spacing problem
→ do not reopen concept

generic testimonial section
→ reuse visual-system principles

entire execution contradicts concept
→ reconsider art direction

concept itself unsupported by business evidence
→ return to problem framing
```

---

# Test the synthesis before presenting it

## Coherence

Check whether:

* content structure
* narrative
* visual language
* composition
* conversion path
* interaction
* motion
* responsive behavior
* technical approach

imply the same overall experience.

When execution exists, prefer `art-direction-coherence-review` for the detailed pass.

---

## Subtraction

Remove:

* redundant sections
* redundant messages
* unnecessary graphic devices
* decorative effects
* duplicate calls to action
* unnecessary technical layers

Ask:

```txt
What can disappear without weakening the central idea?
```

---

## Accessible baseline

The essential meaning and primary action must survive:

* semantic linear reading
* keyboard use
* touch
* zoom and reflow
* reduced motion
* unavailable advanced rendering
* failed JavaScript where progressive enhancement is expected

Do not make spectacle a prerequisite for comprehension.

---

## Responsive concept survival

Ask:

```txt
What is the conceptual invariant?

How does it transform on narrow screens?

Which expressive devices can disappear?

What relationship must remain?
```

Do not preserve desktop composition at the expense of usability.

---

## Feasibility

Classify the direction as:

* `feasible`
* `feasible with constraints`
* `prototype required`
* `not production-feasible`
* `insufficient information`

When constrained, provide a simpler expression that preserves the premise.

Do not silently downgrade the concept without explaining the trade-off.

---

# Output modes

Choose the output based on the user's actual request.

## Discovery output

When the project is early:

```md
## Current stage

## Problem frame

## Missing evidence

## Skills routed

## Research or concept findings

## Next decision
```

---

## Concept council output

When concepts are being debated:

```md
## Decision question

## Evidence

## Council

## Candidate directions

## Conflict map

## Comparison

## Selected direction

## Sacrifices and rejected ideas

## Validation required
```

---

## Direction-to-system output

When a concept has already been chosen:

```md
## Approved direction

## Skills routed

## Visual-system implications

## Structural implications

## Remaining design decisions

## Validation gates
```

---

## Execution-review output

When design already exists:

```md
## Review baseline

## Art-direction verdict

## Concept drift

## Strongest preserved elements

## Priority corrections

## Specialist follow-ups

## Validation gates
```

---

# Final decision artifact

For broad creative-direction work, return one unified artifact containing:

## Project Frame

```txt
Project:
Audience:
Primary message:
Primary action:
Problem:
Desired outcome:
Constraints:
```

## Current Stage

```txt
Stage:
Why:
Previous stages already supported by:
Missing evidence:
```

## Skills Used

| Skill | Why it was needed | Artifact produced |
| ----- | ----------------- | ----------------- |

Do not claim a skill was invoked if it was unavailable or not actually used.

---

## Council

When used:

| Perspective | Why included | Key contribution |
| ----------- | ------------ | ---------------- |

Also list material exclusions.

---

## Selected Direction

```txt
Concept:
Essential meaning:
Audience transformation:
Narrative:
Visual-system thesis:
Composition principle:
Interaction character:
Conversion strategy:
```

Include only fields relevant to the current stage.

---

## What We Preserve

* ...

## What We Reject

* ...

## What We Sacrifice

* ...

## What Remains Unverified

* ...

---

## Next-Stage Plan

Organize only the work necessary to progress.

Possible phases:

```txt
1. semantic content and information structure
2. visual-system exploration
3. responsive structural design
4. interaction and motion
5. technical prototype where needed
6. accessibility validation
7. art-direction coherence review
8. layout craft review
```

Do not prescribe phases that are already complete.

---

## Validation Gates

Define specific checks before moving forward.

Examples:

```txt
concept explains business transformation clearly
graphic system remains recognizable in quiet mode
layout survives narrow viewport
primary CTA remains directly accessible
signature motion has reduced-motion behavior
execution passes art-direction coherence review
```

---

# Do not

Do not:

* invoke every available skill automatically
* convene a council for a narrow problem
* treat workflow skills as fictional personas
* produce fictional roleplay
* produce seven isolated redesigns
* hide disagreement behind false consensus
* combine every candidate into one compromise
* optimize aesthetics before understanding the problem
* create a visual system before selecting a concept
* create a complex grid before understanding content
* confuse visual-system work with coded component-system work
* polish layout while the concept is fundamentally incoherent
* use storytelling when direct utility is more appropriate
* use motion as a substitute for meaning
* sacrifice accessibility for spectacle
* fabricate customer evidence
* claim user testing that was not performed
* claim specialist invocation that did not occur
* write frontend code unless the user explicitly moves the task into implementation

---

# Quality bar

The orchestration is complete only when:

* The project's current creative-direction stage is explicit.
* Existing evidence is reused rather than recreated.
* Only the smallest relevant workflow sequence was used.
* Workflow skills and council perspectives are treated differently.
* Council mode was used only for meaningful tensions.
* Every selected specialist has a reason to be present.
* Material disagreements are visible.
* Candidate directions are internally coherent.
* One dominant decision is produced when decision-making is in scope.
* Trade-offs are explicit.
* The visual direction traces back to project evidence.
* Narrative, visual system, and layout are connected rather than developed independently.
* Accessibility is treated as a design constraint rather than a final compliance pass.
* Technical feasibility is considered only to the depth justified by the concept.
* Existing strong design decisions are preserved during review.
* Downstream reviews can route foundational problems back to the appropriate upstream stage.
* The result ends with a clear next decision or next-stage plan.
* No frontend implementation is produced unless explicitly requested.

---

# Related skills

Primary workflow:

* `design-problem-framer`
* `graphic-universe-builder`
* `story-led-website-concept`
* `design-direction-decision`
* `brand-derived-visual-system`
* `expressive-grid-planner`
* `art-direction-coherence-review`
* `layout-principles-review`

Optional validation:

* `website-distinctiveness-review`

Council perspectives:

* `provocative-concept-director`
* `experimental-web-art-director`
* `minimalist-brand-director`
* `editorial-digital-designer`
* `conversion-creative-director`
* `motion-experience-director`
* `creative-technologist`

The orchestrator owns routing and synthesis.

The specialist skills own their bounded jobs.
