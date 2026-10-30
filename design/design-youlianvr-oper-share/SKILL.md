---
name: design
description: >-
  UI, UX and visual design work: direction and brand language, layout and
  information architecture, components and states, data on screen, flows and
  accessibility, design systems and craft tooling. Use when building or reshaping
  an interface, a landing page, a brand language or a design system. One contract
  with the parts under parts/ — open the one the task needs.
---

# design — UI, UX and visual work

> Home branch in Memora: `root/skill/design`.
>
> Craft, not filter. The adjacent `antislop` skill is the filter (what to avoid);
> this skill is the craft (what to build and why). Read both when building or
> reshaping an interface.

## Choosing a part

**Direction and visual language**

| Part | What it covers |
|---|---|
| `parts/brand/` | Brand voice, visual identity, messaging frameworks, asset management, brand consistency |
| `parts/brand-visual-language/` | A brand's visual tone — playful or serious, rounded or angular — consistent across every UI element |
| `parts/dembrandt/` | Orchestrator for the full six-stage dembrandt UX pipeline: direction → tokens → layout → components → states |
| `parts/extract-design/` | Extract a complete design system — colours, typography, spacing, components, shadows and W3C tokens — from a live website |
| `parts/generate-ui-from-brand/` | Turn a URL or `DESIGN.md` into a concrete UI structure with the decisions already made |
| `parts/algorithmic-color-palette/` | Derive a full UI palette algorithmically from one or two brand colours |
| `parts/color-mode-and-theme/` | Choose light, dark or combined mode deliberately, from brand tone and user context |
| `parts/modular-scale-typography/` | Type feels intentional when sizes follow a ratio-based scale where each size relates to the next |
| `parts/visual-emphasis-and-hierarchy/` | The most important actions and content are prominent through size, colour, weight and position |
| `parts/real-world-metaphors/` | Patterns borrowed from the physical world — graspable cards, scrollable carousels, pullable drawers |
| `parts/gestalt-ui-organisation/` | Grouping and layout follow Gestalt principles so users see which controls belong together |
| `parts/frontend-design/` | Guidance for distinctive, intentional visual design when building or reshaping UI |
| `parts/epic-design/` | Immersive, cinematic 2.5D websites: scroll storytelling, parallax depth, text animation — no WebGL |

**Layout and structure**

| Part | What it covers |
|---|---|
| `parts/layout-paradigms-and-consistency/` | Choosing the paradigm — feed, board, table, canvas, master-detail, dashboard, gallery, timeline, map, single-focus, long-scroll — shapes how content is understood |
| `parts/information-architecture/` | In large applications, IA decides whether users can find, understand and act on data |
| `parts/responsive-paradigms/` | Mobile, tablet and desktop are different interaction paradigms, not one layout scaled |
| `parts/sticky-and-fixed-elements/` | Sticky and fixed positioning keeps critical UI in reach while the page scrolls |
| `parts/scroll-areas/` | Nested scroll areas should be avoided wherever possible |
| `parts/ui-density/` | How much information appears at once should match the platform and the user's task |
| `parts/global-toolbar-controls/` | Quick global settings — currency, language, region, units — in a persistent, low-profile place |
| `parts/tab-navigation/` | Tabs organise related content under one context and swap the view without leaving the page |
| `parts/semantic-html-and-seo/` | Semantic HTML5, SEO fundamentals, alt text, progressive enhancement, SPA and capability detection |

**Components and states**

| Part | What it covers |
|---|---|
| `parts/button-states/` | Every interactive element needs rest, hover, active, focus, disabled and loading states |
| `parts/component-family-consistency/` | Buttons, inputs, pills, badges and calendars share one border-radius, colour logic, shadow and state language |
| `parts/modal-and-overlay-patterns/` | Modals, drawers, bottom sheets and popovers: when to interrupt and when to augment the flow |
| `parts/form-design/` | Helper text, placeholder and validation as three layers; submit enabled only when the form is valid |
| `parts/status-colors-and-errors/` | Status and error colours stay minimal and consistent — too many semantic colours confuse |
| `parts/system-feedback/` | Make clear what happened after an action: confirmation, loading, error, empty state, progress |
| `parts/notifications-and-recovery/` | When something goes wrong the user must be able to recover or retry |
| `parts/loading-states-and-perceived-performance/` | Spinners, skeletons and staggered animation that keep perceived wait short |
| `parts/micro-interactions/` | Small purposeful animation that rewards the user and makes the interface feel alive |
| `parts/motion-and-storytelling/` | Animation principles and cinematic techniques, used subtly, make interfaces feel intentional |
| `parts/transitions-dev/` | Production-ready CSS transitions for web apps |
| `parts/elevation-and-depth/` | Subtle shadows and layering express hierarchy by lifting elements off the surface |
| `parts/repeated-component-alignment/` | A component rendered many times is a fixed slot model: same slots, same places, aligned across siblings |

**Data on screen**

| Part | What it covers |
|---|---|
| `parts/data-display-and-selection/` | Complex data deserves several view modes — grid, list, table — chosen by the user's task |
| `parts/coordinated-data-views/` | Show tabular and visual representations together and keep them synchronised |

**Flows and people**

| Part | What it covers |
|---|---|
| `parts/user-flows-and-guided-paths/` | Purchase, onboarding and multi-step configuration designed as natural guided paths |
| `parts/ux-navigation-context/` | Going back after an action, diagnosing why the wrong screen opened, reworking a crowded menu |
| `parts/ui-context-and-scope/` | Make clear where the user is, what context they act in, and what the action will affect |
| `parts/nielsen-usability-heuristics/` | Nielsen's ten heuristics as the review frame for usability |
| `parts/wcag-accessibility/` | WCAG 2.2 AA compliance, as the European Accessibility Act (EN 301 549) requires |
| `parts/a11y-audit/` | Scan, fix and verify WCAG 2.2 A/AA across React, Next.js, Vue, Angular and Svelte |
| `parts/domain-expert-configuration/` | Settings UIs for domain experts: their language, sensible defaults, grouping by professional concept |
| `parts/operational-expert-tool-ui/` | Tools used for hours daily: density, linear workflow and at-a-glance status over whitespace |

**Systems, craft and tooling**

| Part | What it covers |
|---|---|
| `parts/design-system/` | Capture the brand once through a short wizard and emit tokens, components and a style guide |
| `parts/impeccable/` | Design, redesign, critique, audit, polish, distill, harden, animate, colorize and extract a UI |
| `parts/ui-styling/` | Accessible interfaces with shadcn/ui (Radix + Tailwind), utility-first styling and canvas work |
| `parts/ui-ux-pro-max/` | UI/UX design intelligence for web and mobile |
| `parts/agent-designer/` | Multi-agent system design: orchestration pattern, tool schemas, role boundaries |
| `parts/web-design-guidelines/` | Review UI code against the Web Interface Guidelines |
| `parts/web-design-toolkit/` | Layout, colours, components, animation, `DESIGN.md` generation and style cloning |
| `parts/senior-frontend/` | React, Next.js, TypeScript and Tailwind application work |
| `parts/vercel-react-best-practices/` | React and Next.js performance rules from Vercel Engineering |
| `parts/performance-and-web-vitals/` | Lighthouse audits and Core Web Vitals fixes — LCP, CLS, INP |
| `parts/saas-scaffolder/` | Production-ready SaaS boilerplate: auth, schema, billing, routes, working shell |
| `parts/landing/` | A premium single-page landing with 3D CSS, GSAP scroll and mouse parallax, after an intake |
| `parts/banner-design/` | Banners for social, ads, heroes and print: art direction and platform presets |

## Rules

- **Loading every part is wrong by construction.** This router exists so a
  session loads one contract and opens one part — 59 contracts never travel
  together. Large parts are read by section, not end to end.
- **No brand direction → say so.** Without direction the output drifts to default
  taste; offer to capture it in the project's `DESIGN.md` (`brand`,
  `extract-design`, `generate-ui-from-brand`).
- **End-to-end interface work starts at `parts/dembrandt/`**, which orders the six
  stages and points back into the parts above.
- **Accessibility is checked, not claimed**: `wcag-accessibility`, `a11y-audit` and
  `impeccable` carry the checks; `antislop` has the contrast checker.
- **Forks worth `ask_questions`**: a new visual direction or rebrand, a design
  system change that affects other screens, a third-party UI dependency, and any
  accessibility trade-off that changes the layout.
- **Decisions and reusable findings** become Memora nodes under
  `root/skill/design`; the direction itself lives in the project's `DESIGN.md`.

## Related

`antislop` (the filter), `decks` (slides), `documents` (paper), `media`
(imagery), `dev` (`coding-style`, `simplify`).
