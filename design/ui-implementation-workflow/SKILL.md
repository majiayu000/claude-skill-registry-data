---
name: ui-implementation-workflow
description: Implement project-consistent UI through page classification, bounded references, semantic tokens, skeleton-first delivery, and responsive screenshot QA. Use for frontend redesigns, dashboards, forms, settings, mobile pages, screenshot recreation, visual polish, or generic-looking generated UI.
---

# UI Implementation Workflow

Use this workflow before substantial UI code. Preserve the existing project system unless the task explicitly authorizes a redesign.

## 1. Classify And Audit

Choose one primary page type: `marketing`, `brand`, `portfolio`, `content`, `auth`, `dashboard`, `list`, `detail`, `form`, `settings`, or `mobile`.

Inspect the current stack, component library, routes, shared layout, tokens, typography, assets, and neighboring pages. For a redesign, record what must stay consistent and what is allowed to change.

Start with no inherited aesthetic preference. Do not use old `design-taste-frontend` defaults or earlier taste/review history as design authority. Existing brand rules, accessibility requirements, tokens, and current-task constraints still apply.

Task-size shortcut:

- `tiny`: no external inspiration search; reuse the current design system and verify the changed viewport.
- `small`: use at most one external reference only when the project has no usable pattern.
- `medium+`: use at most three references, each with one job: layout, visual language, component or motion.

## 2. Select References

Do not collect a mood-board pile. For every selected reference, record the exact pattern to borrow and what must not transfer.

- Product UI such as dashboards, lists, forms, details, and settings starts from the existing design system or a proven enterprise component library. Do not apply marketing-site motion or hero composition to operational screens.
- Marketing, portfolio, brand, and content pages may use curated inspiration and restrained motion libraries.
- Prefer code-compatible components over screenshot imitation. Check stack fit, license, accessibility, bundle cost, and maintenance before adoption.
- Never copy an entire page, brand identity, proprietary asset, or paid template without permission.

Read [references/source-catalog.md](references/source-catalog.md) only when external reference research is needed.

For `marketing`, `brand`, `portfolio`, or `content` pages that need a visual direction beyond the existing system, read [references/visual-direction.md](references/visual-direction.md). Do not read it for routine product UI or small corrections. The old `$design-taste-frontend` name is only a compatibility adapter into this reference; do not run it as a second workflow.

When the user or a designated reviewer comments on rendered UI, read [references/visual-review-signals.md](references/visual-review-signals.md) and append the explicit result to the project-local `.codex/ui-visual-review-signals.md`. New entries are raw review evidence only; they must not become persistent or cross-project preferences automatically.

Keep a reference ledger for every candidate inspected. Record `candidate`, `active`, `rejected`, or `replaced`; its role; the exact borrowed rule; screenshot result; rejection reason; and successor. The catalog is complete inventory, not permission to load every site into context.

## 3. Produce The UI Implementation Plan

Do not modify code until the plan is explicit. Include:

1. page type, purpose, audience, and primary workflow;
2. existing project constraints, selected foundation, and visual-direction brief when applicable;
3. layout hierarchy and sections/components;
4. typography levels;
5. semantic colors, borders, radii, shadows, spacing, and container widths;
6. hover, focus, disabled, loading, empty, error, and success states;
7. motion type, duration, trigger, reduced-motion fallback, or why motion is omitted;
8. desktop, tablet, and mobile behavior;
9. selected references, borrowed rules, and rejected patterns;
10. implementation order and screenshot acceptance criteria.

If the plan cannot explain why the result fits this product and audience, stop and revise it before coding.

## 4. Establish Semantic Tokens

Reuse existing tokens first. If the project has none, create the smallest coherent layer needed for the page:

```css
--radius-sm; --radius-md; --radius-lg;
--space-1; --space-2; --space-3; --space-4;
--color-background; --color-surface; --color-text; --color-muted;
--color-primary; --color-border; --color-danger;
--shadow-sm; --shadow-md;
```

Map component states to semantic tokens. Do not scatter arbitrary colors, radii, shadows, and spacing values across each page.

## 5. Implement In Order

Use this sequence:

```text
page structure
-> real data and interactions
-> responsive behavior
-> typography and color
-> borders, shadows, and assets
-> motion and decorative polish
```

Keep state behavior and real workflows working before decorative effects. Use one component/design system per surface. For operational UI, prioritize scanability, density, predictable navigation, form ergonomics, and clear status feedback.

## 6. Render, Compare, Repair

Load `$browser-automation-router`. Start the application and capture stable screenshots at:

- `1440px` desktop;
- `768px` tablet;
- `390px` mobile.

Check overflow, clipping, horizontal scroll, alignment, spacing rhythm, control heights, text fit, empty/loading/error states, focus visibility, image quality, motion readability, and performance. Compare against the implementation plan and selected references.

Fix visible defects and capture the affected widths again. Do not accept code inspection as visual evidence. Use `$playwright` when CI, deterministic traces, or repeatable screenshot tests are required.

### Dynamic Reference Switching

If the rendered result misses acceptance criteria, diagnose the failed dimension before changing references:

- hierarchy, section order, density, or spacing: replace only the `layout` reference;
- typography, color, imagery, or visual tone: replace only the `visual` reference;
- component fidelity, accessibility, stack fit, or maintenance: replace only the `component` reference;
- timing, motion clarity, or performance: replace the `motion` reference or remove motion.

Keep at most three active references. Replace one role per iteration, update the reference ledger and implementation plan, then make the smallest corresponding code change and recapture affected widths. Do not silently blend the old and new direction.

`tiny` does not switch to external sources. `small` allows one switch round. `medium+` allows two switch rounds by default; after that, return the remaining visual gap, attempted sources, and a decision request instead of browsing indefinitely. Do not revisit a rejected source unless the acceptance criteria changed.

## Completion Evidence

Return the page type, visual-direction brief when used, reference ledger and switch history, fresh visual-review signal entries when feedback occurred, design plan, token changes, implementation files, commands, screenshot paths for all required widths, defects fixed after the first render, residual differences, and skill-hit callback. A first-pass screenshot without a repair decision is not a closed visual loop.
