---
name: ui-ux-pro-max
description: "UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, mobile app, .html, .tsx, .vue, .svelte. Elements: button, modal, navbar, sidebar, card, table, form, chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, flat design. Topics: color palette, accessibility, animation, layout, typography, font pairing, spacing, hover, shadow, gradient. Integrations: shadcn/ui MCP for component search and examples."
---

# UI/UX Pro Max - Design Intelligence

Operating contract for UI/UX planning, implementation, review, and repair across web and mobile interfaces. Use the searchable data and scripts when design direction, accessibility, layout, typography, color, chart, component, or stack guidance is needed.

## Invocation Triggers

Use this skill when the user asks to design, build, implement, review, fix, improve, optimize, enhance, or refactor UI/UX for:

- Websites, landing pages, dashboards, admin panels, SaaS, e-commerce, portfolios, blogs, and mobile apps.
- Components such as buttons, modals, navbars, sidebars, cards, tables, forms, and charts.
- Design decisions around style, palette, typography, accessibility, responsive layout, animation, spacing, hover states, shadows, or gradients.
- Stack-specific UI work in HTML/Tailwind, React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, shadcn/ui, or Jetpack Compose.

## When Not to Use

- Pure backend, data pipeline, DevOps, or API work with no user-facing interface.
- Product strategy without screen, flow, component, or interaction decisions.
- Brand-only work with no UI implementation or critique.
- Tasks where another more specific skill fully covers the request and UI is incidental.

## Required Input Contract

Collect or infer:

- Product type, audience, industry, goal, and conversion or task outcome.
- Screen or component scope.
- Stack; default to `html-tailwind` when unspecified.
- Style keywords and any existing brand constraints.
- Accessibility, responsive, and motion requirements.
- Data visualization needs and data shape when charts are involved.
- Existing code, screenshots, design system, or reference material when available.

If critical context is missing, proceed with explicit assumptions unless the choice changes accessibility, compliance, platform fit, or implementation feasibility.

## Core UI/UX Workflow

1. Analyze the request for product type, audience, style, industry, stack, and UI surface.
2. Generate or retrieve a design system before implementation or critique.
3. Supplement with focused searches only when needed: style, color, typography, landing, chart, UX, web, React, or stack.
4. Apply accessibility and interaction rules before visual polish.
5. Implement or review using the selected stack's conventions.
6. Validate responsive layout, keyboard/focus behavior, touch targets, contrast, reduced motion, loading states, and visual consistency.
7. Report design choices, files changed, checks performed, and remaining risks.

See [design-workflow.md](references/design-workflow.md) for detailed search commands, domain and stack catalogs, persistence, and output formats.

## Critical Rules

Accessibility and usability:

- Normal text contrast must meet at least 4.5:1.
- Interactive controls need visible focus states and 44x44px minimum touch targets.
- Icon-only buttons need accessible labels.
- Forms need labels, clear errors, and keyboard-friendly order.
- Color cannot be the only indicator.
- Respect `prefers-reduced-motion`.

Professional UI quality:

- Use SVG icon sets such as Lucide, Heroicons, or Simple Icons; do not use emojis as UI icons.
- Give clickable elements pointer cursors and clear hover/focus feedback.
- Avoid hover effects that shift layout.
- Keep transitions in the 150-300ms range for common micro-interactions.
- Preserve responsive layouts at mobile, tablet, laptop, and wide desktop widths.
- Avoid horizontal scroll on mobile.
- Ensure fixed or floating elements do not cover content.

See [ui-patterns.md](references/ui-patterns.md) for pattern catalogs and [accessibility-and-validation.md](references/accessibility-and-validation.md) for complete checks.

## Search and Implementation Rules

- Start design work with the design-system search when the script is available.
- Use focused domain searches after the initial system, not as a substitute for it.
- Resolve scripts relative to this skill directory; do not hard-code private local paths in tracked files.
- Use `--stack html-tailwind` when the user does not specify a stack.
- Use shadcn/ui MCP only when relevant to component search, examples, forms, theming, or shadcn implementation.
- Keep generated design systems and page overrides in project files only when the user asks for persistent design artifacts.

Minimal command shape:

```bash
python3 scripts/search.py "<product_type> <industry> <style keywords>" --design-system -p "<project-name>"
python3 scripts/search.py "<keyword>" --domain ux
python3 scripts/search.py "<keyword>" --stack html-tailwind
```

## Safety and Validation Rules

- Do not introduce secrets, private context, real local paths, credentials, tokens, session records, or personal identifiers.
- Do not claim visual or browser verification unless it was actually performed.
- Do not use fake logos, fake brand claims, fake screenshots, or unsupported accessibility claims.
- Preserve existing design-system conventions unless the user requests a redesign.
- For frontend changes, inspect the existing UI before editing and validate at realistic responsive widths.
- For reviews, prioritize user-impacting defects: accessibility, broken layout, unreadable text, unusable controls, performance, and data clarity.

## Output Expectations

Depending on the task, provide:

- Design system summary: style, palette, typography, spacing, interaction, and anti-patterns.
- Implementation notes or changed files.
- Accessibility and responsive checks performed.
- Screenshots, browser test notes, or command output when applicable.
- Open assumptions, limitations, and follow-up recommendations.

## Minimal Examples

```text
Design a professional SaaS dashboard in Next.js with accessible dark mode.
Review this landing page for conversion, accessibility, responsive layout, and visual polish.
Fix the mobile nav, table overflow, focus states, and button hover behavior.
```

## Reference Map

- Detailed workflow, search commands, domains, stacks, persistence, and output formats: [design-workflow.md](references/design-workflow.md)
- UI pattern catalogs, style selection, typography, color, chart, and professional UI rules: [ui-patterns.md](references/ui-patterns.md)
- Accessibility requirements and delivery validation checklist: [accessibility-and-validation.md](references/accessibility-and-validation.md)
- Critique rubric, troubleshooting, and common failure modes: [critique-and-troubleshooting.md](references/critique-and-troubleshooting.md)
- End-to-end public-safe examples: [examples.md](references/examples.md)
