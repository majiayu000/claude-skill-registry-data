---
name: design-tokens
description: "Establish color, typography, spacing, radius and motion as named role-based tokens. Use before building any interface."
---

You are establishing the design system foundation. Tokens defined here are used by every component in `/frontend-design`. Get this right before building anything.

First, check: does a design system already exist for this project? Ask the user to confirm. If yes, document the existing tokens rather than inventing new ones. Pull from Figma or existing CSS files if accessible.

If starting from scratch, create CSS custom properties across these five categories:

**Color**
Brand colors (primary, secondary, accent), semantic colors (action, destructive, success, warning), neutral scale (background, surface, border, text), feedback colors (error, warning, success, info). Name every token by its purpose, not its value. Use `--color-action` not `--color-blue`. Use `--color-text-primary` not `--color-gray-900`.

**Typography**
Font family (body, heading, mono if needed), type scale (xs, sm, base, lg, xl, 2xl, 3xl), font weights (regular, medium, semibold, bold), line heights (tight, normal, relaxed).

**Spacing**
A consistent scale, not arbitrary values. Use a base unit (4px or 8px) and name steps by feel: `--spacing-tight`, `--spacing-comfortable`, `--spacing-spacious`. At minimum: 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px.

**Border radius**
Small (input, button), medium (card), large (modal, sheet), full (pill, avatar).

**Motion**
A duration scale (fast, default, slow) and one easing curve. Justify the slow end against the slowest device your user is actually holding.

Output as a ready-to-paste CSS `:root` block. Include a brief comment above each category explaining the system logic. No inline documentation that pads length; every comment must earn its space.

Dark mode: structure the tokens so that dark mode requires only new token values, not new components. Use semantic names so a dark theme can override `--color-background` without touching component code.

**Token audit (use this when Figma and the frontend do not match)**

If a value looks correct in Figma but renders differently in the browser, run this audit before filing a bug. Paste your Figma token export and your CSS file and ask:

"I am going to paste two things: a Figma token export and a CSS file. Compare them. Tell me: (1) which tokens in the export are not referenced anywhere in the CSS, (2) which CSS values are hardcoded instead of using a token, and (3) whether there are any unit mismatches between the token values and the CSS values (for example, a px value in the token but a rem value in the CSS). List each issue with the specific token name and the line in the CSS where the problem appears."

The four most common causes of a mismatch: the token was never exported from Figma, the token was exported but the CSS references a hardcoded value instead, the units differ (px in Figma, rem in CSS), or the comparison is being made at different zoom levels. Confirm all four before concluding something is broken.
