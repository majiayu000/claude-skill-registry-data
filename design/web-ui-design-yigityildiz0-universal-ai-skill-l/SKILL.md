---
name: web-ui-design
description: "Web/app UI: visual direction, layout polish, screenshot-to-code, UX copy, WCAG accessibility, browser testing, handoff. Site tasarla, arayüzü güzelleştir, responsive yap."
---

# Web UI Design

Build, restyle, review and verify web and app interfaces as one system. The ui-ux-pro-max family is installed as separate, upstream-maintained skills — use them for their specialties:

- `ui-ux-pro-max` — searchable styles, palettes, font pairings, stack rules, design-system generator.
- `ui-styling` — shadcn/ui + Tailwind implementation, themes, dark mode, canvas visuals.
- `design-system` — token architecture and component specs.
- `modern-web-guidance` / `site-seo-audit` (ChatGPT) or the Marketing plugin (Claude) — newer browser APIs, Baseline support, SEO.

## Choose the module

| Need | Module |
|---|---|
| New UI or new visual direction; avoid a templated look | `frontend-design` |
| Polish or review layout, spacing, typography, color, motion; "tasarım dengesiz/yamuk" | `web-design-guidelines-workflow` |
| Screenshot or reference image → code with visual comparison | `visual-reference-to-code` |
| Labels, buttons, errors, empty states, onboarding copy | `ux-copy` |
| Accessibility / WCAG audit | `accessibility-review` |
| Test in a real browser: console, network, responsive, interaction | `browser-testing-with-devtools` |
| Developer handoff and acceptance criteria | `design-handoff` |

## Shared rules

- Inspect the existing project, framework and design tokens first; change the smallest surface that solves the request.
- Accessibility is part of done: contrast, focus, keyboard, labels, reduced motion.
- Verify visually (screenshot or browser) before claiming the UI is finished.
- Do not install tooling or add dependencies unless the task needs them; ask before large restyles of working pages.

## Module map

Open only the module(s) the request needs and read the module file completely before acting. Several modules may combine in one task.

| Module | Use when | File |
|---|---|---|
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. | [MODULE.md](modules/frontend-design/MODULE.md) |
| `web-design-guidelines-workflow` | Build, improve, or review web and product interfaces as one coherent system across layout and optical balance, accessibility, UX writing, typography, color, surfaces, ic… | [MODULE.md](modules/web-design-guidelines-workflow/MODULE.md) |
| `visual-reference-to-code` | Turn a screenshot, generated design reference, or visual brief into a polished responsive interface through measurable visual analysis, implementation, and screenshot co… | [MODULE.md](modules/visual-reference-to-code/MODULE.md) |
| `ux-copy` | Write or review interface copy for labels, buttons, onboarding, forms, empty states, errors, confirmations, permissions, and help text. | [MODULE.md](modules/ux-copy/MODULE.md) |
| `accessibility-review` | Audit a web, mobile, desktop, document, or product flow for practical accessibility issues using current WCAG 2.2 AA-oriented checks, code, screenshots, and interaction … | [MODULE.md](modules/accessibility-review/MODULE.md) |
| `browser-testing-with-devtools` | Test and debug web interfaces in a real browser using whatever browser, DevTools, Playwright, or computer-use capability is already available. | [MODULE.md](modules/browser-testing-with-devtools/MODULE.md) |
| `design-handoff` | Create or review a design-to-engineering handoff with intent, responsive behavior, tokens, states, interaction rules, edge cases, assets, acceptance criteria, and open d… | [MODULE.md](modules/design-handoff/MODULE.md) |

Supporting files (open only when the module points to them):

- `web-design-guidelines-workflow`: [accessibility.md](modules/web-design-guidelines-workflow/references/accessibility.md), [color-and-theming.md](modules/web-design-guidelines-workflow/references/color-and-theming.md), [layout-and-balance.md](modules/web-design-guidelines-workflow/references/layout-and-balance.md), [typography.md](modules/web-design-guidelines-workflow/references/typography.md), [ui-polish-and-motion.md](modules/web-design-guidelines-workflow/references/ui-polish-and-motion.md), [ux-writing.md](modules/web-design-guidelines-workflow/references/ux-writing.md)
- `browser-testing-with-devtools`: [browser-debugging-playbooks.md](modules/browser-testing-with-devtools/references/browser-debugging-playbooks.md), [test-plan-template.md](modules/browser-testing-with-devtools/references/test-plan-template.md)
