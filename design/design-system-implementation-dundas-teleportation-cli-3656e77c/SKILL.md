---
name: design-system-implementation
description: Build or update frontend components and pages that strictly adhere to the project design system defined in design/design-system.json (and design/design.json when present).
license: Complete terms in LICENSE.txt
---

This skill ensures that all new or modified UI is implemented **in line with the project design system**, rather than inventing ad-hoc styles.

Use it when:
- Implementing a new component, page, or flow.
- Refactoring existing UI to match the design system.
- Extending the design system with carefully considered new patterns.

It is designed to be used **after** a design system has been created (for example via the `design-system-from-reference` workflow).

## Inputs and assumptions

- The project design system is defined in:
  - `design/design-system.json` (implementation-level source of truth).
  - Optionally `design/design.json` (higher-level style guide).
- The user can describe:
  - What they want to build or change (component/page/flow).
  - Any relevant constraints (framework, routing, data layer, accessibility).
- The codebase uses a consistent framework (e.g., React + Tailwind, or another typical web stack).

If `design/design-system.json` is missing, this skill should **not** free-style a new design system. Instead, it should:
- Ask the user to confirm whether a design system exists elsewhere.
- Suggest running the `design-system-from-reference` workflow first.

## Core responsibilities

When building or updating UI, this skill must:

1. **Load and understand the design system**
   - Ingest `design/design-system.json` (and `design/design.json` if present).
   - Identify:
     - Tokens (colors, spacing, radii, typography scales, shadows, etc.).
     - Component definitions and their variants.
     - Layout and spacing rules.
     - Interaction states and motion guidelines.
   - Summarize back to the user how the design system wants buttons, inputs, cards, navigation, etc. to look and behave.

2. **Map the request to existing patterns**
   - For a new request (e.g., "build a billing settings page"):
     - Break the UI into **sections and components**.
     - For each part, map it to existing component types or patterns in the design system.
   - If something genuinely new is needed:
     - Propose how it fits into existing patterns (e.g., "This is a variant of the card component with…").
     - Avoid inventing totally unrelated styling unless the user explicitly wants to extend the system.

3. **Implement using the design system**
   - Use **only** tokens, utility classes, and component recipes defined by the design system whenever possible.
   - Avoid arbitrary inline styles or one-off Tailwind utilities that conflict with the system.
   - Respect:
     - Typography hierarchy (headings, body, labels, etc.).
     - Spacing scale and layout rules.
     - Color usage rules for states (primary, secondary, error, warning, success, disabled, etc.).
     - Motion and interaction patterns.
   - Keep code production-quality: clear structure, accessible semantics (ARIA, labels, keyboard navigation), and sensible component boundaries.

4. **Handle extensions carefully**
   - When the design system does not explicitly cover a case:
     - First, try to express the new UI using **combinations or variants** of existing components.
     - If an extension is truly needed, propose an addition to `design/design-system.json`:
       - Describe new tokens, component variants, or layout rules.
       - Ensure they are consistent with the existing system.
     - Present the proposed JSON patch or snippet to the user for review before updating the design system.

5. **Validate adherence**
   - After generating code, briefly explain **how** it follows the design system:
     - Which tokens/variants were used.
     - How spacing/typography align with the rules.
   - If any deliberate deviations were made (e.g., an experimental component), call them out clearly.

## Suggested workflow when invoked

1. **Confirm context**
   - Ask the user:
     - What they want built or changed.
     - Where in the codebase it lives (paths, existing components).
     - Whether there is an existing design system JSON; if unsure, search for `design/design-system.json`.
2. **Load design system files**
   - Open `design/design-system.json` (and `design/design.json` if present) and summarize the relevant parts for this task.
3. **Plan the implementation**
   - Break the UI into logical components/sections.
   - For each, decide which design system components or patterns to use.
   - Share this plan with the user and pause for confirmation.
4. **Implement incrementally**
   - Update or create components in small, reviewable steps.
   - After each significant chunk (e.g., a component or page section), pause and:
     - Show the diff or the new code.
     - Explain how it adheres to the design system.
5. **Optional: update the design system**
   - If new patterns were introduced, propose JSON additions/changes for `design/design-system.json`.
   - Only modify the design system after explicit user approval.
6. **Summarize and hand off**
   - Recap what was built/changed and how it aligns with the design system.
   - List any follow-ups (e.g., applying the same patterns to other screens, updating docs).

## Interaction with other skills

- When combined with **`design-system-from-reference`**:
  - Run `design-system-from-reference` first to create or update the design system files.
  - Then use this `design-system-implementation` skill for all subsequent UI work.
- When combined with **`frontend-design-concept`**:
  - Use `frontend-design-concept` for exploring bold conceptual directions.
  - Once a direction is chosen and codified into the design system, use `design-system-implementation` to roll out consistent implementations across the app.
