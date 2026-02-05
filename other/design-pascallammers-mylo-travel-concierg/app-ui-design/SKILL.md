---
name: app-ui-design
description: Design efficient, modern app interfaces with mature UI frameworks in React and cross-platform contexts. Use when asked to plan or create app UI/UX layouts, component structures, design tokens, interaction flows, or implementation-ready guidance for React web/mobile (e.g., React Native/Expo) with an emphasis on efficiency-first experiences.
---

# App UI Design

## Quick start

- Confirm goal, core flows, target platforms, and constraints.
- Prioritize efficiency-first interactions (short paths, reduced clicks, fast scanning).
- Choose a mature UI framework; see `references/frameworks.md` for options and selection notes.
- Use examples as templates when helpful; see `references/examples.md`.
- Produce a concrete UI plan: layout, component list, states, and interaction details.
- Provide implementation-ready guidance for React and cross-platform usage.

## Workflow

1. Gather inputs
   - Identify primary tasks, time-critical actions, and high-frequency flows.
   - Clarify platform targets (web, iOS, Android) and device sizes.
   - Capture constraints: data density, latency, offline, accessibility.

2. Define efficiency-first UX
   - Minimize steps for primary tasks; design for one-hand, keyboard, or quick actions where relevant.
   - Favor scanning: compact, consistent typography and alignment.
   - Use progressive disclosure for advanced actions.

3. Select framework and UI kit
   - Prefer mature, well-supported UI kits with design tokens and accessible defaults.
   - For cross-platform, favor React Native/Expo + a cross-platform UI system.
   - See `references/frameworks.md` for specific recommendations.

4. Design the UI structure
   - Provide a screen map and navigation model.
   - Specify layout grid, spacing scale, and typography hierarchy.
   - List components, variants, and empty/loading/error states.

5. Detail interactions
   - Document input validation, inline feedback, and shortcuts.
   - Define micro-interactions only when they aid speed or clarity.

6. Output deliverables
   - Present a UI spec or React component plan that can be implemented directly.
   - Include key design tokens and accessibility considerations.

## Output format

- Use concise sections: Goal, Screens, Layout, Components, States, Interactions, Tokens.
- Provide React-friendly component naming and props.
- Keep recommendations actionable and tied to efficiency metrics.
