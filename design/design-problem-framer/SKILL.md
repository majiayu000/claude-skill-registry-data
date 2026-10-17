---
name: design-problem-framer
description: Frames a design problem before layout, visual direction, or interface exploration begins. Use when a brief, redesign request, existing page, or set of requirements needs its purpose, audience, message, priorities, constraints, and success criteria clarified before solutions are proposed.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with access to supplied briefs, screenshots, design documents, content, or repository files unless stated otherwise.
metadata:
  category: ui-ux-polish
  task_type: planner
  audience: designers-frontend-developers-product-teams-creative-directors
  tags:
    - design-framing
    - design-brief
    - audience
    - messaging
    - content-priority
    - problem-definition
    - redesign
  status: draft
  side_effects: none
---

# Design Problem Framer

## Purpose

Turn an ambiguous design request into a concise, evidence-based frame for later creative work. Establish what the design must accomplish, for whom, what must be understood or done, what content matters most, and how later directions will be judged.

This is a problem-definition skill. It does not choose a final visual style, layout, component pattern, or implementation.

## When to use this skill

Use this skill when:

- A user wants to define a design problem, turn a vague idea into a brief, or prepare for a redesign.
- A page or product needs its audience, message, content hierarchy, or primary action clarified before visual exploration.
- Requirements conflict or proposed solutions may be disguising the underlying need.
- An existing page needs its communication gap identified before it is redesigned.
- A later art-direction, layout, conversion, or implementation workflow needs a shared decision frame.

Do not use this skill when:

- The problem is already well framed and the user wants design concepts, a visual direction, or implementation.
- The task is a detailed composition critique, technical architecture, code change, or accessibility compliance audit.
- The user only wants visual inspiration with no concrete communication problem.

## Inputs to inspect

Inspect the smallest useful set of supplied evidence:

- Briefs, product requirements, stakeholder comments, and business goals.
- Page copy, content inventories, brand guidance, or design-system documentation.
- Existing websites, screenshots, mockups, wireframes, or prototypes.
- User goals, audience research, analytics, competitor references, or portfolio context.

Do not require every input. Separate direct evidence from interpretation, and name consequential unknowns.

## Workflow

1. Read the available context without brainstorming a layout. Identify explicit requirements, strong implicit goals, contradictions, missing information, and proposed solutions presented as requirements.
2. Separate findings into **known**, **assumed**, and **preference**. Treat a preferred style or solution as a preference unless the evidence establishes it as a hard constraint.
3. State one primary purpose: the change the page or interface should create for its audience. Rank secondary purposes instead of combining unrelated goals.
4. Define the primary audience by situation: goals, relevant knowledge, decision role, questions, objections, context of use, and known access needs. Do not infer stereotypes.
5. Write one primary message that should be clear before detailed reading. Identify only the supporting messages that materially reinforce it.
6. Identify the primary intended action, which may be comprehension or exploration rather than a button click. Note a secondary action only when it affects the design.
7. Prioritize content as **primary**, **secondary**, **supporting**, **optional**, or **remove or reconsider**. Distinguish features from the user-relevant benefits or proof they provide.
8. Describe the communication sequence: the order in which the audience needs to understand ideas. This is not a page layout or component plan.
9. Select two to four strategic perception qualities, such as precise, credible, approachable, or experimental. Explain what each means for the experience without mapping it directly to colors, fonts, or effects.
10. Record hard constraints, soft constraints, preferences, and unknowns. Surface central tensions, non-goals, and the few non-negotiables every viable direction must preserve.
11. Identify specific opportunities and risks. When reviewing an existing design, state the gap between what it needs to communicate and what it currently communicates; do not expand into a full layout critique.
12. Write a solution-neutral problem statement and a single open design challenge beginning with “How might we…”.
13. Rank observable, implementation-independent success and decision criteria for comparing later directions.
14. Recommend the next design workflow, but do not perform it unless asked.

## Framing rules

- Start with “What must this accomplish?”, not “What should it look like?”
- Preserve contradictions rather than silently resolving them. For example, record “minimalism ↔ information density” when both are requested.
- Translate vague goals into observable intentions. “Make it more engaging” might mean creating a clear entry point, early product evidence, and a readable introduction rather than simply adding decoration.
- Keep the primary message short. If it needs a paragraph, the problem is probably still too broad.
- Separate business and user goals when relevant. A qualified demo request and a visitor’s need to assess product fit can both be true.
- Treat accessibility as a design constraint when known, but route detailed compliance work to a dedicated accessibility skill.
- Do not prescribe grids, colors, typefaces, animations, cards, or hero treatments unless they are confirmed constraints.

## Output format

Use the compact form for a simple request. Use the full form when the supplied context supports it.

```md
# Design Problem Frame

## Core problem

<one to three sentences>

## Problem statement

> We need to <design challenge> for <audience> so they can <understanding or action>, while <important constraint>.

## Design challenge

> How might we…

## Purpose

**Primary:** …

**Secondary:** …

## Audience

### Primary audience

…

### Needs, knowledge, and friction

- …

## Message

### Primary message

> …

### Supporting messages

1. …

## Intended action

**Primary:** …

**Secondary:** …

## Content priority

### Primary

- …

### Secondary

- …

### Supporting / optional / reconsider

- …

## Communication sequence

1. …
2. …

## Desired perception

- **…** — …

## Current gap

<Include only for an existing design.>

## Constraints and unknowns

### Hard constraints

- …

### Soft constraints and preferences

- …

### Unknowns and assumptions

- …

## Tensions, non-goals, and non-negotiables

- **Tension:** … ↔ …
- **Non-goal:** …
- **Every viable direction must:** …

## Opportunities and risks

- **Opportunity:** …
- **Risk:** …

## Success and decision criteria

### Critical

1. …

### Important

- …

## Recommended next step

…
```

## Quality bar

The task is complete only when:

- The core problem, primary purpose, audience, message, and intended action are explicit or clearly marked as assumptions.
- Content priority and communication order are clear enough to guide later hierarchy decisions.
- Desired perception is separated from a visual solution.
- Constraints, preferences, unknowns, tensions, non-goals, and non-negotiables are not conflated.
- The design challenge permits multiple solutions, and the success criteria can distinguish among them.
- No layout, style system, frontend code, or implementation plan has been prematurely produced.

## Edge cases

- **Vague idea:** Produce a provisional frame, infer conservatively, and name assumptions.
- **Client brief:** Classify each input as business requirement, user need, stakeholder preference, proposed solution, or constraint.
- **Screenshot with little context:** Use observed, likely, and unknown; do not invent business strategy from appearance alone.
- **Detailed brief:** Synthesize it into priorities, contradictions, and decision criteria rather than repeating it.
- **“Modern” or “unique”:** Offer evidence-based possible meanings and leave unresolved interpretations visible rather than choosing one arbitrarily.
- **Experimental work:** Treat exploration or memorability as a valid purpose, while retaining a clear audience, action, and evaluation standard.

## Related skills

- `ui-design-direction-builder` — creates an implementation-ready visual and interaction direction after framing.
- `layout-art-direction` — develops structural and compositional direction from the defined hierarchy.
- `conversion-creative-director` — develops a persuasion-focused direction when conversion is central.
- `provocative-concept-director` — explores distinctive concepts once the communication goals are clear.
- `editorial-digital-designer` and `minimalist-brand-director` — explore specialized visual approaches after framing.
