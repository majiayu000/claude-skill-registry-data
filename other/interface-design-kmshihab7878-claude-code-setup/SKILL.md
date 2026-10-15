---
name: interface-design
description: This skill is for interface design — dashboards, admin panels, apps, tools, and interactive products. NOT for marketing design (landing pages, marketing sites, campaigns).
---

# Interface Design

Operating contract for crafted product interfaces: dashboards, admin panels, SaaS apps, tools, settings pages, data interfaces, and interactive products. This skill is not for marketing pages or campaigns; route those to `/frontend-design`.

## Invocation Triggers

Use this skill when the user asks to design, build, critique, improve, or systematize:

- Dashboards, admin panels, SaaS apps, internal tools, settings pages, data-heavy screens, and product workflows.
- Navigation, data surfaces, forms, tables, cards, panels, filters, charts, controls, and reusable interface systems.
- Interface craft: visual hierarchy, product-domain expression, typography, spacing, depth, surfaces, tokens, states, and consistency.
- `.interface-design/system.md` creation, use, audit, extraction, or update.

## When Not to Use

- Landing pages, marketing sites, campaigns, ads, or brand-only work with no product interface.
- Pure backend, API, data, DevOps, or CLI tasks with no screen or interaction surface.
- Generic frontend implementation when the user only wants mechanical code changes and no interface design judgment.
- Tasks better handled by a more specific skill, unless interface craft is central.

## Required Input Contract

Collect or infer:

- Human context: who uses the interface, when, and what they must accomplish.
- Product domain: concepts, vocabulary, materials, data, and operational realities.
- Interface scope: screens, flows, components, states, data density, and constraints.
- Existing design system, `.interface-design/system.md`, screenshots, code, or component library.
- Desired feel and product-specific direction, avoiding generic labels like "clean" without specifics.
- Stack and implementation constraints when code will be changed.
- Accessibility and usability requirements.

If intent, user, or task context is too vague to make non-generic choices, ask a focused question or propose a direction with explicit assumptions.

## Core Interface Design Workflow

1. Inspect existing interface code, screenshots, or `.interface-design/system.md` when present.
2. Define intent: who the human is, what they must do, and how the product should feel.
3. Explore the product domain before choosing visuals.
4. Produce the four direction inputs: domain concepts, color world, signature element, and defaults to reject.
5. Propose a direction that ties structure and expression back to those inputs.
6. Build or critique using a consistent token, spacing, typography, depth, surface, state, and navigation system.
7. Validate craft and usability before showing: swap test, squint test, signature test, token test, responsive check, and state check.
8. Offer to save durable interface patterns to `.interface-design/system.md` when useful.

See [design-workflow.md](references/design-workflow.md) for the full workflow, communication rules, system file behavior, and save criteria.

## Interface Quality Constraints

- Every visible choice must have a product-specific reason. "Common", "clean", or "modern" is not enough.
- Typography, navigation, data presentation, token names, colors, and spacing are design decisions, not neutral containers.
- Intent must be systemic: surfaces, text, borders, accents, motion, semantic colors, and component structure should reinforce the same direction.
- Avoid generic dashboard defaults unless the domain, user, and task justify them.
- Use one coherent depth strategy: borders-only, subtle shadows, layered shadows, or surface-color shifts.
- Use systematic tokens and spacing; avoid random hex values, random spacing, and mixed depth strategies.
- Design every state: default, hover, active, focus, disabled, loading, empty, and error.
- Navigation must ground the screen: where am I, where can I go, and what matters most.

See [layout-and-components.md](references/layout-and-components.md) for component, token, layout, state, and navigation guidance.

## Accessibility and Usability Constraints

- Keep text readable and hierarchy clear at a glance.
- Preserve keyboard focus visibility and logical interaction order.
- Do not rely on color alone to convey meaning.
- Keep controls usable in all relevant states.
- Ensure responsive layouts do not hide content, overlap controls, or create mobile horizontal scroll.
- Use data presentation that clarifies meaning and action, not decorative metrics.
- Respect existing accessibility, validation, and public-safety requirements in the repository.

See [accessibility-and-validation.md](references/accessibility-and-validation.md) for validation checks and delivery criteria.

## Validation Rules

Before presenting work:

- Run the swap test: replacing typeface, layout, palette, or component treatment with common defaults should change the product feel.
- Run the squint test: hierarchy should remain visible without harsh lines or jarring color jumps.
- Run the signature test: identify concrete components where the product-specific signature appears.
- Run the token test: token names and values should sound like they belong to this product's world.
- Check state coverage, responsive behavior, spacing consistency, and `.interface-design/system.md` consistency where applicable.
- If validation fails, iterate before showing the user.

See [critique-and-troubleshooting.md](references/critique-and-troubleshooting.md) for critique protocol and failure modes.

## Output Expectations

When proposing direction, include:

```text
Domain: [5+ product-world concepts]
Color world: [5+ domain-grounded colors/materials/light sources]
Signature: [one element unique to this product]
Rejecting: [default] -> [replacement], [default] -> [replacement], [default] -> [replacement]
Direction: [approach tied to the above]
```

When completing implementation or critique, report:

- Design intent and rationale.
- Files or components changed.
- Validation performed.
- Accessibility/usability risks.
- Whether durable patterns should be saved to `.interface-design/system.md`.

## Minimal Examples

```text
Design a dense operations dashboard for an incident commander.
Improve this settings page so hierarchy, states, and spacing feel intentional.
Audit this admin table against the current .interface-design/system.md.
Extract reusable interface patterns from these components.
```

## Reference Map

- Full workflow, product-domain exploration, communication, `system.md`, and saving rules: [design-workflow.md](references/design-workflow.md)
- Layout, component, token, surface, state, navigation, typography, icon, animation, and chart guidance: [layout-and-components.md](references/layout-and-components.md)
- Accessibility, usability, responsive validation, and pre-delivery checks: [accessibility-and-validation.md](references/accessibility-and-validation.md)
- Critique protocol, troubleshooting, generic-output failure modes, and repair patterns: [critique-and-troubleshooting.md](references/critique-and-troubleshooting.md)
- Worked public-safe examples and final report patterns: [examples.md](references/examples.md)

## Existing Deep Dives

- [craft-foundations.md](references/craft-foundations.md)
- [design-principles.md](references/design-principles.md)
- [principles.md](references/principles.md)
- [validation.md](references/validation.md)
- [critique.md](references/critique.md)
- [example.md](references/example.md)

## Commands

- `/interface-design:status` - current system state.
- `/interface-design:audit` - check code against system.
- `/interface-design:extract` - extract patterns from code.
