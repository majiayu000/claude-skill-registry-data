---
name: ui-design-system
description: >-
  Use when creating, extending, or auditing a project-grounded UI design system:
  visual direction, semantic design tokens, typography, color, spacing,
  component guidance, responsive rules, or UI anti-patterns. Do not use for a
  page-specific UI brief, supplied brand governance, generic frontend
  implementation, or visual QA alone.
license: MIT
metadata:
  source: nextlevelbuilder/ui-ux-pro-max-skill
  source_revision: 7f69fed
  source_url: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
  compatibility: harness-neutral; uses existing project evidence and capabilities
---

# UI Design System

Create a reusable, project-grounded visual and interaction system that makes
page and component decisions consistent without flattening legitimate context.
This skill owns system-level design guidance. `frontend-design` owns the
page-specific brief and accessibility contract; `brand-guidelines` owns
supplied identity rules; an approved engineering workflow owns implementation.

## Boundaries and precedence

Use this skill for requests such as:

- define or audit the product's visual language and design tokens;
- choose a coherent style, palette, typography system, spacing scale, or motion
  language for multiple screens;
- establish component states, resilient content rules, or stack-aware UI
  guidance that should be reused across a product;
- review a proposed design system for consistency, accessibility, and
  implementation risk.

Do not use it for a single page or component brief, which belongs to
`frontend-design`; for customer or market uncertainty, use `product-discovery`;
for repository architecture, use `technical-design`; for supplied identity
rules, use `brand-guidelines`.

Apply constraints in this order:

1. Existing project tokens, components, accessibility and content conventions.
2. Approved brand rules and assets, when supplied.
3. Existing framework, platform, dependency, and repository constraints.
4. The user's explicit brief and acceptance criteria.
5. This skill's neutral system guidance.

Never invent a brand identity, copy another organization's visual identity, or
turn one campaign example into a global rule. When brand evidence is absent,
propose a restrained neutral direction and label it as a proposal.

Do not edit files, generate a design-system artifact, install fonts or
dependencies, start a renderer, or run visual checks without explicit approval.

## Workflow

### 1. Establish the system boundary

State whether the request is to create, extend, audit, or migrate a design
system. Identify the products, platforms, pages, components, users, and
implementation stack in scope. Inspect existing tokens, components, examples,
brand material, and accessibility requirements before proposing new rules.

Separate confirmed rules, inferred patterns, assumptions, and missing evidence.
If there is no existing system, say so and keep the initial system deliberately
small. Do not build a catalog merely to make the output look complete.

### 2. Define the design language

Recommend one coherent direction unless the user asks for alternatives. State
the user or product quality it expresses and the evidence supporting it. Cover
only the visual dimensions that matter for the scope:

- surface, border, contrast, and depth treatment;
- color mode and semantic color roles;
- typography roles, hierarchy, readable measure, and fallback behavior;
- spacing, sizing, radius, elevation, and density;
- icon, illustration, imagery, and chart conventions;
- motion purpose, timing, interruption, and reduced-motion behavior.

Avoid aesthetic filler and trend labels without operational consequences. A
style recommendation is useful only when it leads to rules a page or component
can apply consistently.

### 3. Build semantic tokens

Prefer semantic roles over component-specific or raw-value names. Include only
the token families the project needs, such as:

- `background`, `foreground`, `surface`, `surface-muted`, and their content
  counterparts;
- `primary`, `secondary`, `accent`, `destructive`, and explicit on-colors;
- `border`, `focus-ring`, disabled, success, warning, and informational states;
- typography roles, spacing scale, control heights, radii, elevation, and motion
  durations or easing where those are part of the system.

For each proposed token, state its purpose, inheritance or override rules, and
where it is consumed. Preserve existing names and values when they are already
an approved contract. Do not prescribe a framework-specific syntax unless the
repository already uses it or the user explicitly requests it.

### 4. Specify reusable component guidance

Describe the components that are actually in scope and their states. For each
important interactive component, cover its semantic role, content constraints,
loading, success, empty, error, disabled, permission, retry, focus, and
keyboard behavior where applicable.

Include resilient rules for real content: long headings, translated labels,
URLs and identifiers, chips and badges, dense tables, text resizing, browser
zoom, and narrow screens. Prefer wrapping or an operable disclosure over
clipping. If truncation is unavoidable, define an accessible full-value path.

For charts, dashboards, and data-heavy interfaces, define legibility, non-color
distinctions, empty and loading states, and the smallest useful responsive
behavior instead of prescribing a chart type without context.

### 5. Check platform and stack fit

Inspect the repository's actual stack and existing component library. Adapt
terminology and examples to it; do not default to React, Tailwind, a specific
CSS system, or a font provider. Use `source-driven-development` when a
framework, platform, or library behavior is version-sensitive.

If the stack or target platform is unknown, keep the recommendation framework-
neutral and list the smallest question needed to specialize it. Do not install
packages or fetch a knowledge base to fill an evidence gap.

### 6. Define the quality gate

Return checks proportionate to the system's scope:

- semantic token coverage and absence of unexplained one-off values;
- readable contrast and visible focus for applicable states;
- keyboard operation, semantic names, and non-color status cues;
- responsive behavior at the project's supported widths, including 320, 768,
  1024, and 1440 px when no project matrix exists;
- text resizing, zoom, localization, overflow, and resilient content behavior;
- reduced-motion behavior and interruptible state transitions;
- component examples or repository-native tests when a runnable seam exists.

Treat visual or accessibility claims as unverified until the approved project
tooling produces fresh evidence. Hand page-specific validation to
`frontend-design` and final completion evidence to
`verification-before-completion` when available.

## Output contract

```markdown
## System Scope and Design Read

## Existing Evidence and Constraints

## Visual Direction

## Semantic Token Plan

## Component and Content Rules

## Platform and Stack Fit

## Accessibility, Responsive, and Motion Contract

## Validation and Adoption Plan

## Open Questions, Non-Goals, and Required Approval
```

Stop at the approved design-system brief. Persist or implement it only through
an explicitly approved project workflow, and never imply that a generated
system, visual audit, or accessibility result exists without fresh evidence.
