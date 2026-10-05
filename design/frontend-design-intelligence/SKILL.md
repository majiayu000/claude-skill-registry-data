---
name: frontend-design-intelligence
description: 'Review inspected designs or briefs for product-flow gaps and ask evidence-based user questions. Ground UI direction in audience, patterns, and UX risks; excludes code and tool setup.'
id: 'agents.skills.frontend-design-intelligence.skill'
title: 'Frontend Design Intelligence'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'frontend-design-intelligence'
tags:
    - 'agents/skill-package'
    - 'agents/design'
    - 'workflow/design-intelligence'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/design-screenshot-spec/references/product-behavior-review|Product Behavior Review]]'
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[common/design-quality-rubric|Design Quality Rubric]]'
    - '[[common/anti-template-defaults|Anti-Template Defaults]]'
    - '[[common/ui-ux-priority-checklist|UI UX Priority Checklist]]'
    - '[[skills/frontend-design-intelligence/references/product-pattern-matrix|Product Pattern Matrix]]'
    - '[[skills/frontend-design-intelligence/references/design-dials|Design Dials]]'
    - '[[skills/frontend-design-intelligence/references/product-anti-patterns|Product Anti-Patterns]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Frontend Design Intelligence

## Purpose

Create a compact design intelligence brief before visual direction when a UI task needs product-category grounding, page-pattern choice, density decisions, or domain-specific anti-pattern checks.

This skill adapts design-system reasoning into the WebDev Agent Kit model without becoming a UI framework, CLI generator, or package installer.

## When To Use

Use after prompt intent routing when the task is `Standard Workflow` or `Deep Workflow` and one or more are true:

- product type, page type, audience, or user job is vague;
- the user asks for visual style, landing structure, dashboard structure, or distinctive UI direction;
- the page needs visual variance, motion, or density decisions;
- inspected designs leave transitions, forms, states, or product behavior unclear;
- `frontend-design-director` needs better grounding before writing a Design Direction Contract.

## When Not To Use

Do not use for Fast Lookup, tiny edits, purely technical bugfixes, code implementation, live Figma inspection, package installation, or new styling systems.

## Required Context

1. Read `AGENTS.md`.
2. Read `common/prompt-intent-routing-rules.md` when workflow level is unclear.
3. Read relevant project overlays when present.
4. Read only relevant references from this skill:
   - `references/product-pattern-matrix.md`;
   - `references/design-dials.md`;
   - `references/product-anti-patterns.md`.
5. Read supplied screenshots, briefs, inspect notes, or existing route files only when they materially affect the brief.
6. Read `skills/design-screenshot-spec/references/product-behavior-review.md`
   when reviewing flows or unresolved product/design decisions. If supplied
   visual sources have not been inspected, use `design-screenshot-spec` first.

## Tool Contract

- May read project overlays and relevant source files.
- Must not run design generators or external CLIs.
- Must not create or edit app source code.
- Must not create a global design system unless explicitly requested, and then only inside `.agents/project/**`.
- Delegate live source acquisition to `design-screenshot-spec`; consume its
  component evidence and report missing coverage before product review.

## Workflow

1. Identify product category, audience, page type, and single job.
2. Separate confirmed facts from unknowns. Inspect the available evidence before
   asking the user; never fill missing product intent with an assumed default.
3. Map the observed user journey and component states. Apply the product review
   reference to ask about unresolved transitions, forms, feedback, persistence,
   responsive behavior, and motion, with evidence and tradeoffs.
4. Propose a page pattern and design dials only where choices are needed. Keep
   proposals distinct from confirmed constraints and obtain the user's decisions.
5. Identify domain UX risks.
6. Identify product-specific anti-patterns and generic template risks.
7. Produce a compact Design Intelligence Brief.
8. Hand off to `frontend-design-director` when visual direction is needed.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

```text
Product Category
Audience
Page Type
Single Job
Recommended Page Pattern
Design Dials
Domain UX Risks
Product-Specific Anti-Patterns
Useful Subject Materials
Design Direction Handoff
Product Questions And Decisions
Blocked Dependent Scope
```

## Validation Gates

- The brief must not prescribe a UI library, styling system, package, or animation dependency.
- The recommendation must be a starting hypothesis, not a rigid template.
- The page pattern must connect to the user job.
- Design dials must explain restraint or intensity.
- Unspecified product/design choices remain open until answered; recommendations
  and existing-code behavior are not substitutes for a user decision.
- Every question identifies a real component/flow, the evidence gap, and user
  impact. Do not re-ask settled facts or stop at a fixed total question count.
- Durable records belong in local project overlays, not reusable bundle docs.

## Trigger Evals

Should trigger:

- "Ground this analytics dashboard before choosing its visual direction."
- "Choose product patterns and design dials for this AI workflow."
- "Review these inspected screens and ask what is missing from the form flow."

Should not trigger:

- "Change this button color."
- "Implement this completed Design Direction Contract."

## Reference Map

- `references/product-pattern-matrix.md`
- `skills/design-screenshot-spec/references/product-behavior-review.md`
- `references/design-dials.md`
- `references/product-anti-patterns.md`
- `skills/frontend-design-director/SKILL.md`
- `common/design-quality-rubric.md`
- `common/anti-template-defaults.md`
- `common/ui-ux-priority-checklist.md`
