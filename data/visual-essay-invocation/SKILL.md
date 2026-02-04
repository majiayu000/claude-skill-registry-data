---
name: visual-essay-invocation
description: Generate comprehensive invocation documents for scroll-driven visual essays. Use when the user wants to create a visual essay, immersive explainer, interactive documentary, scroll-driven narrative, or cinematic web experience. Produces detailed specifications including scroll-lock animations, parallax systems, chapter architecture, figure profiles, design systems, and implementation checklists. Supports both photorealistic (archival photography) and illustrated (SVG/generative) visual treatments.
license: Complete terms in LICENSE.txt
---

# Visual Essay Invocation Framework

This skill generates production-ready invocation documents that guide the development of immersive, scroll-driven visual essays. An invocation is a comprehensive specification—not the final artifact, but the blueprint that ensures consistent, high-quality execution.

## Framework Overview

Visual essays transform complex subjects into cinematic, scroll-driven experiences. They differ from articles-with-animations by treating scroll as narrative device, anchoring ideas in metaphor, and centering human faces and stories.

### Core Philosophy

1. **Metaphor-first storytelling** — Every chapter anchored by conceptual handle
2. **Human-centered narrative** — Ideas have faces; complexity becomes relatable through people
3. **Scroll as dramaturgy** — Not decoration but narrative control; scroll input drives revelation
4. **Emotional arc** — Information transforms the reader, not just informs them

## Invocation Architecture

Every invocation follows this six-layer structure. See `references/invocation-template.md` for the complete template.

### Layer 1: Strategic Foundation
- **Project Title** — Evocative name plus explanatory subtitle
- **Executive Brief** — Emotional throughline, stakes, transformation promise
- **Visual Treatment Philosophy** — Medium rules (photography vs. illustration, era treatments, source guidance)

### Layer 2: Technical Systems
- **Scroll-Lock Specification** — Viewport locking behavior, scroll-as-input mechanics
- **Parallax Depth System** — Layered depth (background, mid, subject, overlay, ambient)
- **Themed Progress Indicator** — Content-specific visualization of advancement

### Layer 3: Hero Architecture
- **Scroll-Lock Hero Sequence** — Always cinematic, tied to core thesis
- **Percentage-Based Choreography** — 0-20%, 20-40%, etc. breakpoints
- **Title Reveal Pattern** — Question or tension resolved into title card

### Layer 4: Chapter Schema
Each chapter includes:
- Title + temporal/contextual marker
- Central metaphor (one line)
- Visual assets specification
- Content focus (narrative beats)
- Key figure profile(s) with defining quotes
- Scroll-lock sequence (named, choreographed)
- Parallax treatment notes

### Layer 5: Design System
- Color palette with semantic meanings
- Typography scale (headlines, body, quotes, technical, captions)
- Animation principles (timing, easing, stagger values)
- Era/mood treatments for visual processing shifts

### Layer 6: Implementation
- Responsive adaptations
- Accessibility requirements
- Source attribution standards
- Deliverables checklist

## Workflow

### Step 1: Understand the Subject

Before writing, establish:
- **Scope**: What time period? What boundaries?
- **Audience**: Experts, beginners, or general curious?
- **Stakes**: Why does this matter now?
- **Arc**: What transformation should the reader experience?
- **Visual Medium**: Photography (archival/documentary) or illustration (generative/SVG)?

### Step 2: Identify Key Figures

Every visual essay needs human anchors. Identify 5-15 people who:
- Made pivotal contributions or decisions
- Have available photography or portraiture
- Represent different perspectives or eras
- Said memorable, quotable things

### Step 3: Map the Narrative Arc

Structure the essay with dramatic beats:
- **Opening hook**: Question, tension, or mystery
- **Rising action**: Building complexity, introducing figures
- **Climax**: The pivotal moment or revelation
- **Falling action**: Consequences, spread of impact
- **Resolution or open question**: Where we stand now

### Step 4: Design Scroll-Lock Sequences

For each major moment, define a scroll-lock animation. See `references/scroll-lock-patterns.md` for pattern library.

Key principles:
- Lock duration proportional to content importance
- Scroll input drives animation progress (not time)
- Always provide skip affordance
- Smooth easing on lock/unlock transitions

### Step 5: Specify Visual Treatment

For photorealistic essays:
- Identify archive sources
- Define era-based processing (B&W, color grading)
- Specify parallax separation techniques for photos

For illustrated essays:
- Define illustration style
- Specify generative/procedural elements
- Design metaphor visualizations

### Step 6: Write the Invocation

Follow the template in `references/invocation-template.md`. Be specific:
- Name exact scroll percentages
- Describe visual states at each breakpoint
- Specify figure profile format consistently
- Include actual quotes where possible

## Visual Medium Guidelines

### Photorealistic Treatment

Use for: Historical narratives, documentary subjects, biographical essays

Requirements:
- Source archives identified
- Era-based processing defined
- No illustrations mixed with photography
- Parallax achieved through photo masking/separation
- Grain, contrast, color grading specified per era

### Illustrated Treatment

Use for: Abstract concepts, technical explanations, future-focused topics

Requirements:
- Illustration style guide defined
- SVG/generative approach specified
- Metaphor visualizations designed
- Consistent visual language throughout

### Mythological Treatment

Use for: Sacred narratives, religious figures, cosmological concepts, living traditions

Requirements:
- Photography of historical art as primary (sculpture, painting, manuscripts)
- Custom illustration for cosmic/abstract sequences only
- Divine figure profile format (see `lenses/mythology.md`)
- Mythological arc types (Quest, War of Dharma, Cosmic Cycle, etc.)
- Cultural sensitivity guidelines followed
- Source attribution for both textual and visual sources

See `lenses/mythology.md` for complete guidance.

### Hybrid Treatment

Rarely recommended. If mixing:
- Clear separation between modes
- Photographs for people/history
- Illustrations for concepts/diagrams
- Never composite photos with illustrations

## Progress Bar Patterns

The progress indicator should reinforce the essay's central metaphor:

| Subject | Progress Concept |
|---------|------------------|
| Nuclear/Energy | Chain reaction particles |
| AI/Computing | Neural network building |
| Blockchain/Finance | Chain of blocks |
| Biology/Medicine | Cell division / DNA helix |
| Space/Physics | Orbital trajectory |
| History/Time | Timeline with era markers |
| Engineering | Blueprint completion |
| Music/Art | Waveform or composition |

## Chapter Schema Reference

See `references/chapter-schema.md` for the complete chapter template and examples.

Essential elements per chapter:
- Metaphor (required, one line)
- Central visuals (3-6 specific assets)
- Content focus (3-5 narrative beats)
- At least one key figure profile
- One scroll-lock sequence (named, with percentage choreography)

## Figure Profile Format

Consistent format for all historical/key figures:

```
**[Full Name]** — [Epithet/Role Descriptor]
- [Key contribution 1]
- [Key contribution 2]
- [Key contribution 3]
- [Optional: Defining quote]
- [Optional: Fate/legacy note]
- Photograph: [Description of ideal image]
```

## Design System Specifications

Every invocation must include:

### Color Palette (7-10 colors)
- Primary background
- Secondary/elevated background
- 2 accent colors (semantic meanings)
- Primary text (opacity noted)
- Secondary text
- Semantic colors (success, warning, era-specific)

### Typography (5 categories)
- Headlines: [Font family, weight, character]
- Body: [Font family, purpose]
- Quotes: [Font family, treatment]
- Technical/Code: [Monospace choice]
- Captions/Data: [Treatment]

### Animation Principles
- Scroll-lock zone depth (px range)
- Transition durations (by type)
- Easing curves
- Stagger values for sequences
- Parallax speed ratios per layer

## Common Patterns

### The Reveal
Scroll drives exposure of hidden content—black bars recede, fog lifts, blur clears.

### The Pan
Scroll moves viewport across large image, exploring details sequentially.

### The Zoom
Scroll pushes into image, focusing on specific detail, isolating significance.

### The Comparison
Scroll drives slider or crossfade between two states (before/after, then/now).

### The Sequence
Scroll advances through rapid series of related images (like flipbook).

### The Assembly
Scroll constructs something piece by piece—diagram builds, timeline populates.

### The Conversation
Scroll reveals dialogue line by line—human/AI, historical exchange, interview.

## Deliverables Checklist Template

Every invocation concludes with implementation checklist:

```
- [ ] Hero sequence with scroll-lock animation
- [ ] Themed progress bar component
- [ ] [N] chapters with scroll-lock sequences
- [ ] [N] historical figures profiled
- [ ] Parallax depth system implemented
- [ ] Design system with era treatments
- [ ] Mobile-responsive adaptations
- [ ] Accessibility: reduced motion, skip controls, alt text
- [ ] Source attribution system
- [ ] Content warnings (if applicable)
```

## Quality Standards

An invocation is complete when:
- Every chapter has a named metaphor
- Every scroll-lock sequence has percentage breakpoints
- Every figure has photograph description
- Design system is specific (not generic)
- Progress bar concept matches subject
- Arc moves from question to resolution/open question
- Emotional stakes are clear from executive brief

## References

- `references/invocation-template.md` — Complete template with all sections
- `references/scroll-lock-patterns.md` — Pattern library with implementation notes
- `references/chapter-schema.md` — Chapter structure with examples
- `references/topic-selection.md` — Topic evaluation and selection criteria
- `lenses/mythology.md` — Specialized guide for mythology, religious narratives, sacred traditions
- `examples/` — Condensed format references showing expected depth (see `examples/README.md`)
- `specs/` — Finished production-ready invocations (see `specs/README.md` for status levels)

## Anti-Patterns to Avoid

- Generic progress bars (simple lines or dots)
- Chapters without metaphors (just "Part 1, Part 2")
- Scroll-lock sequences without percentage choreography
- Figure profiles without photograph descriptions
- Design systems using only "clean" or "modern" as descriptors
- Missing skip affordances for locked sections
- Mixing photorealistic and illustrated without clear separation
- Essays without human anchors (all concept, no faces)

## Expanding the Framework

This skill documents known patterns, not all possible patterns. The framework is scaffolding, not a cage.

### When to Invent

Agents should create new patterns when:
- Existing scroll-lock patterns don't capture the narrative moment
- A subject suggests a novel progress bar metaphor
- The standard chapter arc doesn't fit the story's shape
- A new visual medium emerges (3D, interactive, generative)
- User feedback reveals gaps in current approach

### How to Invent Well

When creating new patterns, maintain core principles:
- **Metaphor-first**: New patterns should make abstract concrete
- **Human-centered**: Don't lose faces in pursuit of novelty
- **Scroll as dramaturgy**: New interactions must serve narrative, not decorate
- **Specific choreography**: Document with percentages and states, not vague descriptions
- **Accessibility**: New patterns need skip affordances and reduced-motion fallbacks

### Documenting Discoveries

When a new pattern proves successful:
1. Add it to the appropriate reference file
2. Include a concrete example from actual use
3. Note when to use it (and when not to)
4. Update this SKILL.md if it represents a fundamental addition

### Post-Invocation Learning Loop

After generating each invocation, the Visual Essay Invocation Agent should:

1. **Store** — Save the completed invocation to `specs/[topic-slug].md`
2. **Tag** — Mark as `[DRAFT]` in the file header
3. **Flag** — Notify for human review
4. **Await** — Do not reference as canonical until validated

**Review criteria:**
- Does it follow the six-layer structure?
- Are scroll-lock sequences specific (percentages, not vague)?
- Do figure profiles include photograph descriptions?
- Is the progress bar concept tied to subject matter?
- Would another agent produce quality output from this spec?

**Promotion path:**
```
specs/[DRAFT] → specs/[REVIEWED] → references/ (if canonical quality)
```

**Example storage format:**
```markdown
---
status: DRAFT
topic: [Topic Name]
generated: [ISO date]
visual_treatment: [photorealistic|illustrated|mixed]
chapters: [count]
figures: [count]
lens_applied: [lens name or "none"]
---

# Visual Essay Invocation: [Title]

[Full invocation content...]
```

This loop ensures the skill improves with use. Every invocation is potential training data for future quality.

### Areas Ripe for Expansion

Current gaps worth exploring:
- **Audio integration**: Sound design, narration, ambient audio
- **Branching narratives**: Non-linear story paths
- **Data-driven sequences**: Real-time data visualization
- **Generative visuals**: AI-generated imagery integration
- **Collaborative elements**: User contribution, annotation
- **Multi-device experiences**: Phone as controller, AR layers

### Evolution Philosophy

The best visual essays haven't been made yet. This framework captures what works today. Tomorrow's breakthrough will come from someone who understood these patterns well enough to know when to break them.

Document what you learn. The skill grows with use.