---
name: frontend-design
description: "Build an interface from the brief and the tokens rather than from a guess. Use only after grill-me, design-brief, information-architecture and design-tokens have run."
---

You are building the interface. Use everything that came before. Do not start from scratch.

Before writing any code, confirm three things are accessible:
1. The design brief (from `/design-brief`)
2. The design tokens as CSS custom properties (from `/design-tokens`)
3. The task list indicating which component or screen is being built now (from `/brief-to-tasks`)

If any of these are missing, ask for them before proceeding. Generating UI without a brief is guessing. Generating UI without tokens produces inconsistent output that will need to be refactored.

Build intentionally. For every component, before writing the first line of CSS:
- Name the design token it uses for each visual property (color, spacing, radius, shadow)
- Name the user it serves and the specific task it supports
- Name every state it must handle: default, hover, active, focus, disabled, error, empty

Do not generate decorative code. Every visual decision must trace to a token or a decision in the brief. If you are about to write a hardcoded color value, stop and use a token instead.

Output production-ready HTML and CSS with these requirements:
- All colors, spacing, and type use CSS custom properties from the design token file
- Focus states are visible and meet 3:1 contrast minimum against adjacent colors
- Mobile layout is handled at 375px width minimum (use `@media (max-width: 640px)`)
- Every interactive component includes an empty state (what the user sees before data exists)
- Touch targets on mobile are at minimum 44px height for all interactive elements

Structure the output as a single HTML file with a `<style>` block importing the token system at the top. Components are self-contained. Comments explain decisions, not syntax.
