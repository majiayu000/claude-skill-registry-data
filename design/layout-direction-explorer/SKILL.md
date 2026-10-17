---
name: layout-direction-explorer
description: Generate several structurally distinct layout directions from a defined design problem, content hierarchy, or existing page. Use when a user wants composition alternatives or thumbnail-style explorations before selecting and implementing a final direction.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to supplied briefs, screenshots, content, design documents, or repository files unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: generator
  audience: designers-frontend-developers-product-teams-and-creative-directors
  tags:
    - layout
    - composition
    - design-exploration
    - visual-hierarchy
    - art-direction
    - thumbnails
    - concept-generation
    - design-direction
  status: draft
  side_effects: none
---

# Layout Direction Explorer

## Purpose

Generate three to five plausible, meaningfully different layout directions before a team commits to one. Treat the work as thumbnail sketching: explore hierarchy, composition, sequence, and rhythm broadly enough that the next design decision is real.

This skill produces conceptual directions only. It does not select a winner, create a final mockup, write code, or make production specifications.

## When to use this skill

Use this skill when:

- A page, landing page, portfolio, or product surface needs multiple ways to organize the same message and content.
- The user asks for layout concepts, composition alternatives, structural hypotheses, or thumbnail-style explorations.
- An existing layout feels generic, conventional, or prematurely fixed, and the team wants wider options before refinement.
- The design frame is already clear enough to distinguish useful alternatives.

Do not use this skill when:

- The purpose, audience, primary message, or constraints are too unclear to evaluate directions; use `design-problem-framer` first.
- The user wants critique of one layout, a final art direction, a comparison and recommendation among existing options, or frontend implementation.
- The task is primarily brand identity, technical architecture, or accessibility compliance.

## Inputs to inspect

Inspect the smallest useful set of available inputs:

- Design brief, page purpose, audience, primary message, primary action, content inventory, and non-negotiables.
- Existing screenshots, wireframes, page copy, product visuals, brand guidance, references, and known constraints.
- A `design-problem-framer` result, when available.

At minimum, establish purpose, primary message, primary content, primary action, and major constraints. Infer conservatively and label assumptions; do not invent claims or requirements.

## Workflow

1. **Establish the design frame.** Record the audience, desired understanding or action, content priorities, desired perception, constraints, and non-negotiables. Preserve settled decisions rather than reopening them.
2. **Name the default pattern.** Describe the most obvious conventional structure the brief would produce. This creates a baseline and prevents cosmetic variations of one layout from masquerading as exploration.
3. **Choose meaningful variables.** Vary only assumptions that can legitimately change: entry point, focal point, hierarchy, composition, image and typography roles, density, rhythm, narrative sequence, or navigation model. Preserve fixed content and constraints.
4. **Form structural hypotheses.** Start with questions such as “What if the product is the evidence?” or “What if proof precedes explanation?” rather than visual-style labels. A style treatment is not a layout direction.
5. **Create 3–5 distinct directions.** Each direction needs one organizing idea and should state its entry point, dominant element, composition model, content sequence, image role, typography role, whitespace and rhythm, primary strength, and primary risk.
6. **Add a conceptual thumbnail.** Use a simple text diagram to communicate relationships and sequence. It must not imply pixel dimensions, exact components, or production CSS.
7. **Describe the visual pathway.** Explain the likely order of attention and how the composition extends beyond the hero into the page.
8. **Test diversity and tradeoffs.** For each direction, explain in one sentence what makes it structurally different. Merge concepts that share the same hierarchy, hero, grid, and flow. Make each direction optimize a different useful tradeoff.
9. **Summarize without choosing.** Compare options, identify what the exploration reveals, and route selection to `design-direction-decision` unless the user explicitly asks for a recommendation.

## Exploration rules

- Explore structure before style: hierarchy, focal point, composition, sequence, and rhythm come before colors, effects, or named aesthetics.
- A direction is distinct only when it changes a fundamental compositional assumption, such as message-first versus product-first versus evidence-first—not merely image placement or palette.
- Give every direction one dominant idea. Do not combine unrelated visual devices just to make it feel novel.
- Let directions make different tradeoffs. For example, one may optimize clarity, another distinction, and another product proof.
- Use content roles such as `[PRIMARY PROPOSITION]` when copy or assets are incomplete. Do not fabricate marketing claims.
- Discuss mobile or motion only as conceptual adaptations; do not write responsive CSS or animation specifications.
- Keep the directions intentionally incomplete. Avoid exact spacing, font sizes, grids, breakpoints, durations, and implementation details unless supplied as fixed constraints.

## Output format

Return:

````md
# Layout Direction Exploration

## Design frame

- **Purpose:** ...
- **Audience:** ...
- **Primary message:** ...
- **Primary action:** ...
- **Non-negotiables and assumptions:** ...

## Current/default pattern

...

## Exploration strategy

The directions vary: ...

## Direction A — <structural name>

- **Core idea:** ...
- **What makes it different:** ...
- **Entry point and dominant element:** ...
- **Composition:** ...
- **Content sequence:** 1. ... 2. ... 3. ...
- **Image and typography roles:** ...
- **Whitespace and rhythm:** ...

### Conceptual thumbnail

```text
...
```

### Visual pathway

1. ...
2. ...
3. ...

- **Strength:** ...
- **Risk:** ...

<Repeat for each direction.>

## Comparison snapshot

| Direction | Entry point | Optimizes for | Main risk |
|---|---|---|---|
| A | ... | ... | ... |

## What we learned

- ...

## Next step

Use `design-direction-decision` to select a direction, or a specialist design skill to develop one further.
````

For a small request, use a compact version with the core idea, text thumbnail, focal point, flow, strength, and risk for each of three directions.

## Quality bar

The task is complete only when:

- The design frame and consequential assumptions are clear.
- Three to five directions are provided unless the user requested a different number.
- Every direction has a distinct structural hypothesis, a clear focal point, content sequence, conceptual thumbnail, visual pathway, strength, and risk.
- The options are alternatives to the same communication problem, not cosmetic variants or unrelated redesigns.
- Each direction can plausibly develop into a whole-page experience rather than only a hero.
- No final selection, frontend code, or production-level specification is supplied unless explicitly requested.

## Edge cases

- **Existing layout is already strong:** include an evolutionary direction only when it offers a meaningful strategic alternative; do not change it for novelty.
- **Incomplete content:** use content roles and surface what would change the choice; do not fill gaps with invented copy.
- **One or no images:** vary imagery as evidence, interruption, background anchor, cropped detail, typography, data, product UI, diagram, or whitespace rather than assuming stock images.
- **Unconventional request:** test unusual composition, sequence, scale, or framing while preserving essential comprehension. Clearly label intentionally risky experimentation.
- **Strong brand constraints:** vary structure within them; do not treat a fixed identity as permission to ignore the brief.
- **Mobile or motion matters:** preserve the direction’s thesis and reading order conceptually; route deeper work to `responsive-behavior-planner` or `motion-experience-director`.

## Related skills

- `design-problem-framer` — frames purpose, message, priorities, constraints, and decision criteria before exploration.
- `design-direction-decision` — compares developed directions and recommends one.
- `layout-art-direction` — develops or reviews the composition of a selected direction.
- `provocative-concept-director` — expands creative exploration when initial alternatives are too predictable.
- `editorial-digital-designer`, `minimalist-brand-director`, and `conversion-creative-director` — develop specialized directions after a promising structure is identified.
- `creative-technologist` — evaluates feasibility once an ambitious direction is selected.
