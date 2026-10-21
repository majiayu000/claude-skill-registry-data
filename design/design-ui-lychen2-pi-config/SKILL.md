---
name: design-ui
description: Build or improve user interfaces. Read the project's design system first, then select visual, component, motion, and browser checks for the task.
---

# Design UI

## Read the project before writing UI

1. Read applicable project instructions and the files affected by the request.
2. Inspect the package manifest, framework, component library, and existing dependencies.
3. Find and read the design documentation, token definitions, theme configuration, global styles, and relevant shared components.
4. Read the relevant page and adjacent components, including responsive and interaction states.
5. State the constraints you will reuse before choosing a direction or writing code.

Use the project's documented precedence. Check page-specific design rules when present.
Resolve conflicts between documents and active components before changing shared tokens.
For an existing interface, extend its typography, spacing, colors, surfaces, and interaction patterns.
For a new interface, choose a compact design direction based on audience, content, and the primary action.
Record only the decisions needed for the requested work. A small repair needs no new design document.

## Load only the guidance the task needs

Use skill discovery to find a candidate, then load its instructions explicitly.

| Need | Skill | Use |
| --- | --- | --- |
| New visual direction or substantial redesign | frontend-design | Establish hierarchy, typography, composition, imagery, and content specific to the brief. |
| Searchable design options or a new design-system draft | ui-ux-pro-max | Query local data; evaluate suggestions against the actual project. |
| Component feedback, transitions, gestures, or polish | emil-design-eng | Choose purposeful motion and implementation details. |
| User-requested animation audit | review-animations | Run explicitly with /skill:review-animations and a target. |
| Rendered UI and interaction acceptance | Existing browser tools or computer-use | Inspect the page and exercise its key path. |

Pass the concrete task and project constraints to each loaded skill.
Load frontend-design before committing to a new visual direction.
Load emil-design-eng when motion or component polish materially affects the task.
Use UI/UX Pro Max when a design choice needs research; skip database searches for routine fixes.

## Build with the project

Reuse shared components and semantic tokens. Add a token only when the design needs a reusable value.
Preserve the current framework and component library unless migration is requested.
Use CSS for ordinary state transitions. Consider existing Motion dependencies for React layout, exit, or gesture behavior.
Consider existing GSAP dependencies for coordinated timelines, scroll scenes, or complex SVG animation.
Choose any new dependency from a demonstrated requirement and the task's installation authority.
Keep content, assets, forms, loading, empty, error, and success states appropriate to the requested flow.
Use clear labels, visible focus, semantic controls, readable contrast, and comfortable touch targets.
Respect reduced motion and touch input. Keep essential actions usable during transitions.

## Inspect the result

Run the project's required checks for the affected behavior.
Use available browser tooling; discover computer-use if a visible browser workflow is needed.
Inspect actual screenshots at desktop and a narrow viewport, including approximately 390px when relevant.
Exercise the primary action, keyboard focus, and changed states. Check overflow, wrapping, and image cropping.
For motion, check interruption, repeated activation, and reduced-motion behavior.
Fix visible or functional defects before delivery.
Report the changed behavior, checks performed, and any browser access gap that prevented acceptance.
