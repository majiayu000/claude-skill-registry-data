---
name: frontend-design-director
description: 'Set subject-grounded visual direction for standard or deep UI work, redesign, polish, critique, anti-template review, or design handoff. Skip technical micro-fixes and isolated code edits.'
id: 'agents.skills.frontend-design-director.skill'
title: 'Frontend Design Director'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-director'
tags:
    - 'agents/skill-package'
    - 'agents/design'
    - 'workflow/design-direction'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/design-screenshot-spec/references/product-behavior-review|Product Behavior Review]]'
    - '[[common/prompt-intent-routing-rules|Prompt Intent Routing Rules]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/interface-copy-rules|Interface Copy Rules]]'
    - '[[common/motion-rules|Motion Rules]]'
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[skills/frontend-design-intelligence/SKILL|Frontend Design Intelligence]]'
    - '[[skills/design-screenshot-spec/SKILL|Design Screenshot Spec]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
    - '[[templates/visual-memory|Visual Memory Template]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Design Director

## Purpose

Define a concrete, subject-grounded frontend design direction before implementation when a task requires visual judgment.

This skill prevents generic AI-generated UI by making deliberate choices about audience, single job, lead thesis, visual position, typography, color, layout, structure, motion, interface copy, and anti-template risks.

It does not implement code by default. It creates a Design Direction Contract that can be handed to `frontend-layout-implementer` and verified by `frontend-visual-qa` or `frontend-quality-reviewer`.

## Design Lead Stance

Act as a design lead, not a style randomizer.

For supplied designs, establish fidelity constraints through
`design-screenshot-spec` before critique. Read
`skills/design-screenshot-spec/references/product-behavior-review.md` for unresolved visual or behavior choices.
Preserve observed design intent; recommendations, polish, and accessibility
deviations require user resolution before entering the implementation contract.
Creative guidance below shapes proposals only where the user requests design work.

- The page needs a point of view that fits this subject and audience.
- Take one real visual risk only when it can be justified.
- Spend boldness in one place and keep the rest disciplined.
- The hero or lead section must express the page thesis.
- Typography, structure, motion, and copy are design material, not filler.
- Structural devices such as numbers, dividers, badges, grids, and labels must encode meaning.

## When To Use

Use this skill after prompt intent routing when the task is `Standard Workflow` or `Deep Workflow` and includes visual judgment.

Use this skill when the user asks to create, redesign, polish, critique, make distinctive, or define visual acceptance criteria for a rendered frontend surface.

## When Not To Use

Do not use this skill for one small bug, one obvious type error, one direct file-scope edit, one isolated code refactor, purely technical debugging, UI library selection, package installation, or testing workflows.

Do not use this skill as a required step for every frontend task. Use it only when design judgment affects the current slice.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read `common/design-quality-rubric.md`, `common/anti-template-defaults.md`, `common/interface-copy-rules.md`, and `common/motion-rules.md`.
4. Read `skills/frontend-design-intelligence/SKILL.md` only when product category, page pattern, design dials, or domain-specific anti-patterns need grounding.
5. Read only relevant project overlays:
   - `project/stack-profile.md`;
   - `project/styling-profile.md`;
   - `project/design-reference-profile.md`;
   - `project/visual-memory.md` when present;
   - `project/active-goals.md` or the compact goal contract when present.
6. Read supplied screenshots, design references, copied inspect values, or written brief.
7. Read affected route or component files only when existing project constraints are needed.
8. Do not read all source files, all skills, or all references for routing.

## Tool Contract

- May use filesystem access to read relevant project overlays and write design artifacts only when durable handoff is required.
- May use Browser or Playwright screenshots when a rendered UI already exists and screenshot critique is needed.
- May use MDN or official platform docs for CSS, accessibility, motion, or browser behavior details when needed.
- May use `context7` for framework-specific UI constraints when relevant.
- Route supplied live links and uninspected images through `design-screenshot-spec`;
  reuse its MCP/browser/image evidence instead of assuming visual properties.
- Must not install UI libraries, animation libraries, testing libraries, packages, or MCP servers.
- Must not implement code unless the user explicitly asked for implementation and the execution plan includes a separate implementation slice.

## Workflow

1. Confirm visual task scope.
   - If the task is lightweight and purely technical, stop and route to the direct technical skill.
   - If visual direction matters, continue.
2. Ground the design.
   Define subject, audience, single job, product context, and workflow level.
3. Use `frontend-design-intelligence` when the product/page pattern or design dials are not already clear.
4. Identify existing constraints: typography system, colors, tokens, layout patterns, components, accessibility, responsive constraints, visual memory, and rejected directions.
5. Draft a compact first-pass direction with color, type, layout, structure, motion, copy voice, and signature element.
6. Critique the draft against the brief.
   - If it could fit an unrelated product by swapping copy, revise it.
   - If structural devices do not encode meaning, remove or replace them.
   - If typography is neutral by habit, give it a role or keep it intentionally quiet.
7. Define the lead or hero thesis.
   - What must the first screen prove?
   - What subject-specific material opens the page?
   - Why is this not a generic hero?
8. Present the proposed direction and unresolved choices with evidence and
   tradeoffs. Ask the user to settle them; do not choose on the user's behalf.
9. Define the Design Direction Contract.
10. Run anti-template review.
11. Prepare implementation handoff to `frontend-layout-implementer` only for
    scope whose visual and product decisions are confirmed. Include decision IDs,
    source evidence, and any blocked dependent scope.
12. Prepare verification handoff with visual acceptance criteria for `frontend-visual-qa` or `frontend-quality-reviewer`.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return or write a Design Direction Contract with:

```text
Subject
Audience
Single Job
Product Context
Lead / Hero Thesis
Design Dials
Visual Position
Design Risk
Signature Element
Token System
Typography Roles
Structure As Information
Layout Concept
Motion Stance
Interface Copy Voice
Anti-Template Checks
Implementation Handoff Notes
Visual Acceptance Criteria
Next Skill Or Next Step
Product Questions And Decisions
```

Use `templates/design-direction-contract.md` for durable handoff when needed.

## Unresolved Experimental Questions

If a material UI or state choice remains unresolved after inspection, ask the
user. Propose `frontend-prototype-explorer` only when an experiment would help
them decide, and run it only when requested. Keep this planning skill read-only;
experimental observations do not themselves settle the product choice.

## Validation Gates

Before finishing, verify:

- the task actually needed design judgment;
- the direction is grounded in the subject and audience;
- unresolved design/product questions block dependent implementation, and no
  proposal or experiment result is presented as a user-approved decision;
- the screen has one primary job;
- the hero or lead section expresses a thesis when the surface has a lead section;
- design dials are explicit when visual intensity, motion, or density matters;
- at least one signature element is defined when creating or redesigning a major page;
- typography, color, layout, structure, and motion choices have reasons;
- structural devices encode real meaning;
- anti-template checks were applied;
- no UI component library skill was introduced;
- no testing workflow was introduced;
- no source code was changed by this skill unless a separate implementation slice was explicitly requested.

## Trigger Evals

Should trigger:

- "Make this dashboard look less generic before implementation."
- "Create a visual direction for this landing page."
- "Redesign this screen from the screenshot and make it distinctive."
- "Define the design contract before coding this UI."
- "Review this page for AI-template design issues."

Should not trigger:

- "Fix this TypeScript error."
- "Change this button color to #333."
- "Rename this prop in one component."
- "Run visual QA on the already implemented page."
- "Install a UI library."
- "Create tests."

## Reference Map

- `AGENTS.md` - canonical policy, routing, tool rules, and documentation rules.
- `skills/frontend-design-intelligence/SKILL.md` - product pattern, design dials, and product anti-pattern grounding.
- `common/prompt-intent-routing-rules.md` - workflow weight selection and escalation rules.
- `common/design-quality-rubric.md` - design review dimensions and verdicts.
- `common/anti-template-defaults.md` - suspicious generic UI defaults.
- `common/interface-copy-rules.md` - copy as part of interface design.
- `common/motion-rules.md` - motion restraint and reduced-motion rules.
- `common/ui-ux-priority-checklist.md` - user-impact priority model.
- `templates/design-direction-contract.md` - durable design direction artifact.
- `templates/visual-memory.md` - local-only project visual memory template.
- `skills/design-screenshot-spec/references/product-behavior-review.md` - user
  decisions, evidence-based questions, and implementation readiness.
