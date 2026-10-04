---
name: frontend-design
description: Use when planning a specific frontend page, component, layout, responsive behavior, UI state, accessibility contract, or visual QA. Do not use for product-wide design-system generation, supplied brand governance, dependency selection, browser automation, implementation, or code review.
---

# Frontend Design

Produce a project-grounded UI design brief before implementation. Prioritize
clear hierarchy, accessible interaction, responsive behavior, and existing
design-system conventions over novelty.

## Craft and perceived quality

Small details compound. Users may not name a spacing inconsistency, unclear
label, delayed response, or missing state, but the accumulation changes whether
the product feels trustworthy and easy to use. Treat polish as functional
quality, not decoration.

- Study existing product patterns and explain why they work before introducing
  a new treatment.
- Make the important states feel immediate, predictable, and complete.
- Defend unusual spacing, type, color, motion, or hierarchy with a user or
  product reason; remove effects that only signal novelty.
- Use the brief and later QA to test assumptions. A design that looks correct
  in a static view may still fail in interaction, at another viewport, or with
  larger text.

## Precedence and boundaries

Apply guidance in this order:

1. Existing project brand assets, design tokens, components, accessibility
   conventions, and content guidelines.
2. Existing framework, dependencies, and repository constraints.
3. The user's explicit brief and acceptance criteria.
4. This skill's design and accessibility guidance.

- Do not invent or replace a brand identity. Ask for brand guidance or provide
  neutral, clearly labelled options when the project has none.
- Do not own product-wide visual-system generation, semantic token architecture,
  or reusable component-system rules; hand those requests to
  `ui-design-system` when available.
- Do not implement, refactor, install dependencies, start processes, open a
  browser, take screenshots, or run audits without explicit approval.
- Do not perform code review; hand completed changes to `review-diff` when it is
  available, or to an equivalent review capability exposed by the active
  harness.
- Do not claim visual, responsive, or accessibility verification without fresh
  evidence from the approved project tooling.

## Design workflow

Before proposing a direction, state a one-line **Design Read** covering the
page kind, audience, requested vibe or references, and the design system or
aesthetic family that fits. If the brief genuinely permits materially
different directions, ask one focused clarifying question; otherwise infer and
proceed. Supplied brand, accessibility, regulatory, and product constraints
override aesthetic preference.

When the user requests image-first design or image-to-code work, hand off to
[`image-to-code`](../image-to-code/SKILL.md) when the active harness has the
needed image-generation or image-inspection capability. That skill owns the
reference-image generation, extraction, and implementation sequence; this
skill remains the planning and accessibility contract. If the capability is
unavailable, use supplied references or continue with this brief and report
  the limitation rather than inventing generated-image evidence.

When the request concerns a product-wide visual language, design tokens,
typography or color system, reusable component rules, or UI anti-patterns,
hand off to [`ui-design-system`](../ui-design-system/SKILL.md). This skill then
owns the page-specific hierarchy, state, responsive, accessibility, and QA
brief that applies the approved system to the requested screen or component.

### 1. Frame the page or component

State the audience, user job, page or component purpose, primary action,
information hierarchy, content assumptions, and success condition. Identify the
existing design-system components and tokens to reuse before proposing anything
new.

For a redesign, first classify it as preserving the existing visual language or
an explicitly approved overhaul. Audit current tokens, information
architecture, content and copy voice, signature interactions, analytics or SEO
dependencies, and accessibility wins before proposing changes. Preserve those
contracts by default; do not change them merely to make the result look newer.

For requests such as “polished” or “distinctive,” identify the specific product
or audience quality to express. Avoid generic gradients, cards, rounded corners,
placeholder copy, or decorative effects unless the project system supports them
and they serve the hierarchy.

### 2. Define the visual and structural plan

Describe:

- Content hierarchy, key sections, and a compact wireframe or component tree.
- Existing or proposed token usage for color, typography, spacing, elevation,
  borders, and motion.
- Component composition, responsibilities, and state ownership at a level that
  respects the current framework rather than assuming React or a specific store.
- Realistic user-facing copy, labels, actions, and outcomes.

If the project has no visual system, offer restrained alternatives and wait for
approval before creating a new direction or signature visual treatment.

### 3. Specify interaction and state contracts

For every important interaction, define loading, success, empty, error,
disabled, permission-denied, and retry behavior where applicable. Error states
must explain what happened and provide a useful next action. Avoid optimistic
updates unless the data model, rollback behavior, and user impact justify them.

Specify responsive behavior at 320, 768, 1024, and 1440 px: reflow, visibility,
navigation, touch targets, density, and overflow behavior. Mobile is a first
class layout, not a scaled desktop view.

### 4. Define the accessibility contract

Include semantic HTML, heading order, labels and accessible names, keyboard
operation, visible focus, focus management, contrast, non-color state cues,
screen-reader announcements, reduced motion, text resizing, and form-error
handling as relevant. Use buttons for actions and links for navigation.

State any accessibility uncertainty instead of assuming a component is
accessible because of its visual appearance.

### 5. Plan approval-gated visual QA

Return the manual and automated checks appropriate to the existing project:

- Required states and viewport matrix.
- Keyboard and focus traversal.
- Screen-reader and semantic checks.
- Console, network, and visual/screenshot evidence.
- Existing accessibility or browser-test commands, if any.

Request approval before starting a server or browser, attaching to a profile,
installing audit tooling, or running tests. Use
`verification-before-completion` after implementation for fresh evidence when
that companion skill is available; otherwise apply the same evidence standard
directly.

## Design brief

```markdown
## User Goal and Hierarchy

## Existing System and Constraints

## Layout, Components, and Tokens

## Interaction and State Matrix

## Responsive Behavior

## Accessibility Contract

## Visual QA Plan

## Open Questions and Required Approval
```

Stop at the approved brief. Hand implementation to an approved engineering
workflow and completed-change review to `review-diff` when available, or to an
equivalent review capability exposed by the active harness.
