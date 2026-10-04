---
name: phase4-web-prototype-iteration
description: Use when a product manager needs to generate or iteratively refine a stage four web prototype from prior-stage product requirements, especially for stable B2B prototype webpages with a locked navigation/style/component framework, per-page requirement notes from phase three, target website or screenshot style extraction, field/button/flow/permission/state updates, high-fidelity icon/image asset handling, generated bitmap images when needed, motion/interaction restoration, browser visual regression checks, and prototype-to-PRD consistency.
---

# Phase 4 Web Prototype Iteration

Use this as the execution entry for product-manager stage four web prototype generation and stable iteration inside an established or newly locked web framework.

## Source Method

Read this method-library file before acting:

```text
$env:USERPROFILE\.codex\method-libraries\ai-product-manager\04_原型与PRD交付\07_动态网页原型稳定迭代Skill.md
```

That file is the source of truth. This entry file only adds routing and non-negotiable execution gates; do not let helper skills override the source method.

## Required Behavior

1. Identify the current project stage, module, page, and requested prototype goal.
2. Read only the relevant prior-stage materials for that module, usually phase three solution content or latest confirmation notes.
3. Inspect the prototype source of truth and the established framework rules, not only the rendered webpage.
4. If the global framework is not yet locked, extract and define it first: navigation, typography, colors, layout density, tables, filters, buttons, drawers, modals, and requirement-note behavior.
5. Lock the visual system before expanding pages: typography scale, spacing, density, color tokens, component states, icon style, image treatment, motion behavior, and responsive breakpoints.
6. Make small, scoped changes inside the existing framework. Do not casually change navigation, typography, page density, common layout, or shared components while editing a module.
7. Maintain a per-page prototype requirement note panel, usually in the page's upper-right corner, populated from phase three and updated with the user's latest confirmed wording.
8. When the user provides a target website, domain, screenshot, or Figma reference, extract and lock its style, asset, and interaction rules before expanding module pages.
9. Treat icons, images, illustrations, screenshots, and motion as first-class prototype assets. Reuse real project assets first; use existing icon libraries such as lucide when available; generate bitmap images only when a real visual asset is needed and no suitable source exists.
10. Refresh or rebuild the current prototype artifact only through the project’s existing workflow; do not create a new web framework for each change.
11. Validate the rendered page with browser checks when available, including desktop/mobile screenshots, overflow, text overlap, missing icons/images, incorrect image cropping, and core interactions.
12. Report changed content, source basis, asset/motion decisions, requirement-note updates, validation results, and remaining risks.

## Related Skill Routing

This skill may coordinate with other installed skills when the task requires their specialty:

- Use `figma-prototype-import` when the user needs editable Figma output, prototype JSON, design-context files, or a Figma import workflow.
- Use `frontend-design` when extracting or locking a visual system from a target website, existing product, or screenshot.
- Use `product-design:image-to-code` when the task depends on high-fidelity screenshot, target-image, or mockup restoration into frontend code.
- Use `product-design:audit` when the user needs a design/experience issue list before changing the prototype.
- Use `imagegen` when the prototype needs a missing bitmap image, product visual, illustration, texture, background, or cutout that cannot be sourced from project assets or the target reference.
- Use `figma:figma-implement-motion` or `figma:figma-use-motion` when the task references Figma motion, animations, transitions, or interactive prototype behavior.
- Use `frontend-testing-debugging` and the Browser skill for rendered validation, click checks, overflow checks, console errors, responsive screenshots, visual regression proof, and motion sanity checks.
- Use `frontend-app-builder` only for new builds or explicit redesigns, not for ordinary module-level iteration inside a locked framework.

Keep this skill as the orchestrator for phase four product-prototype work. Related skills are helpers; they should not override prior-stage requirements, locked framework rules, page requirement notes, or prototype-to-PRD consistency.

## Design And Asset Gates

- For target-site or screenshot matching, extract concrete visual rules before implementation: layout grid, density, type scale, spacing, colors, border/radius/shadow usage, component states, icon family, image crop behavior, and motion patterns.
- Do not leave generic placeholders where the reference clearly requires a meaningful image, product visual, logo-like mark, screenshot, avatar, chart preview, or scene.
- If exact assets are unavailable, state the fallback: reused project asset, icon-library substitute, generated bitmap, or intentionally neutral prototype placeholder.
- Prefer lucide or the project's existing icon system for functional UI icons. Keep icon stroke, size, optical alignment, hover/active/disabled states, and labels consistent.
- Implement expected interaction states for B2B prototypes: hover, selected, focused, disabled, loading, empty, error, drawer/modal open-close, tab switch, pagination, filter changes, and save/confirm feedback.
- Before final response, perform visual QA when a browser is available: at least one desktop viewport and one narrow/mobile viewport for affected pages, plus core click/transition checks.

## Trigger Examples

- “按照阶段三内容继续改这个网页原型。”
- “后面会频繁调整网页，需要稳定高效地改。”
- “根据上一个阶段的模块方案把页面字段和交互补齐。”
- “不要影响前面已经确认的页面，改完帮我回归检查。”
- “导航栏、字体这些基础规范已经定了，后续只在模块内调整。”
- “每个页面右上角都要有来自阶段三模块内容的原型需求说明。”
- “我发一个目标网站或截图，你先提取风格并固定成后续网页规范。”
