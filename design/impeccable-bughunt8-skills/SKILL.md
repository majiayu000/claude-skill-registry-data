---
name: impeccable
description: "Direct and improve frontend UX and visual design for websites, applications, and UI components."
disable-model-invocation: true
argument-hint: "[mode] [target]"
---

# Impeccable

> Portable edition adapted from [pbakaus/impeccable](https://github.com/pbakaus/impeccable).
> See [ATTRIBUTION.md](ATTRIBUTION.md) for source, version, and license details.

Use this skill when the user asks to design, redesign, critique, audit, polish, simplify, animate, or otherwise improve a frontend interface. It applies to websites, landing pages, dashboards, product UI, app shells, components, forms, settings, onboarding, and empty states. It does not apply to backend-only or non-UI work.

## Working principles

- Deliver complete, production-appropriate work; do not use a generic visual treatment when the product context supports a deliberate point of view.
- Preserve the existing identity, behavior, factual copy, and out-of-scope surfaces when refining. Ask before replacing factual copy or adding product claims.
- For a redesign, retain product truth, functionality, native affordances, and constraints, but intentionally replace the visual world rather than mixing the old and new directions.
- Prefer clear hierarchy, accessible contrast, readable typography, meaningful whitespace, and purposeful motion over decorative complexity.
- Verify in bounded passes: inspect desktop and mobile together, fix the findings as a batch, then confirm once. Do not enter an open-ended polish loop.

## Workflow

1. **Understand the surface.** Inspect the target and a representative source of visual truth, such as tokens, theme configuration, CSS, a component library, or existing assets. Identify the user, their task, the platform, and the constraints.
2. **Select the mode.** Choose the mode based on the surface, not the overall product:
   - **Persuade:** landing pages, marketing, campaigns, and pricing; optimize for attention and action.
   - **Operate:** dashboards, editors, settings, and tools; optimize for task completion, scanning, and native expectations.
   - **Read:** documentation, articles, guides, and help; optimize for comprehension and sustained reading.
   - **Experience:** portfolios, galleries, and showcases; let the work lead while the interface recedes.
3. **Set direction before implementation.** State the intended hierarchy, visual character, layout, typography, color, and interaction behavior. When the request is ambiguous, ask the smallest set of questions needed to make those choices.
4. **Implement at the right scope.** Reuse the project’s established components and tokens where they support the direction. Add reusable tokens or components when a visual decision recurs. Keep responsive, keyboard, touch, reduced-motion, and localization behavior in scope.
5. **Review the result.** Inspect the rendered interface at relevant device sizes and assess information hierarchy, accessibility, empty/error/loading states, performance-sensitive effects, and consistency with the selected mode.

## Modes

Use a named mode when it clarifies the request; otherwise apply the workflow directly.

| Mode | Goal |
|---|---|
| `shape` | Plan UX and visual direction before coding. |
| `critique` | Review usability, hierarchy, information architecture, and cognitive load. |
| `audit` | Check accessibility, responsive behavior, and UI performance. |
| `polish` | Run the final bounded quality pass before shipping. |
| `bolder` | Give a bland but sound design more distinct character. |
| `quieter` | Reduce visual aggression or overstimulation without losing hierarchy. |
| `distill` | Remove unnecessary complexity and preserve the essential task. |
| `harden` | Cover errors, empty states, edge cases, i18n, and production constraints. |
| `onboard` | Improve first-run, activation, and empty-state experiences. |
| `animate` | Add motion that explains state or strengthens feedback. |
| `colorize` | Use color strategically to clarify hierarchy and state. |
| `typeset` | Improve font choices, type scale, measure, and text hierarchy. |
| `layout` | Improve spacing, alignment, rhythm, and responsive composition. |
| `delight` | Add restrained, memorable details that support the product character. |
| `clarify` | Improve labels, instructions, UX copy, and error messages. |
| `adapt` | Adapt a surface across screen sizes and input methods. |
| `optimize` | Diagnose and reduce UI performance costs. |

## Quality floor

- Make the primary action and the current state obvious without relying on color alone.
- Maintain keyboard access, visible focus, semantic controls, sufficient contrast, and reduced-motion support.
- Design loading, empty, success, error, disabled, and overflow states rather than treating them as exceptions.
- Avoid placeholder imagery, invented product claims, inaccessible interactions, and novelty effects that compromise performance or usability.
- Use responsive layouts that reflow content instead of merely shrinking desktop UI.

For the complete upstream skill, including its optional CLI tooling, design detector, live-browser workflow, and detailed command playbooks, consult the [Impeccable repository](https://github.com/pbakaus/impeccable).
