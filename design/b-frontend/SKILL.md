---
name: b-frontend
description: >
  Context-aware frontend/UI implementation for pages, layouts, components,
  styling, responsive behavior, interactions, and visual refreshes. Uses
  existing product tokens, components, assets, and design guidance without
  inventing a generic aesthetic, and hands browser/visual proof to
  b-browser. Routing signals: frontend implementation, UI implementation,
  page implementation, layout implementation, component implementation,
  component styling, responsive behavior, responsive layout, UI
  interaction, interaction state, visual refresh, landing page, landing-
  page.
metadata:
  phase: Build
  execution_mode: main
---

<!-- Generated from skills/registry.yaml and skills/b-frontend/prompt.md. Edit those sources, not this file. -->

# b-frontend

Implement clearly scoped frontend/UI code, visual refreshes, landing pages, and component styling in the existing application. Keep decisions contextual to the product and hand real-browser or visual proof to **b-browser**.

## When to use

- The user asks to build or change a frontend page, layout, component, styling, responsive behavior, interaction state, or landing/marketing surface.
- Existing product tokens, components, assets, or `docs/DESIGN.md` provide enough direction for code work now.

## When NOT to use

- The user wants reusable frontend standards or `docs/DESIGN.md` created or refreshed -> use **b-design**.
- The user wants browser sessions, screenshots, live UI checks, or e2e/visual evidence -> use **b-browser**.
- The request is broad or the implementation approach is unclear -> use **b-plan**; unresolved external framework/API facts belong to **b-research**.
- A confirmed runtime or rendering defect needing root-cause diagnosis -> use **b-debug**.
- The change is not frontend/UI work -> use **b-implement**.

## Tool guidance

- Use native repository reads and edits plus the existing project commands. Inspect the package manifest and relevant lockfile before adding imports; do not assume React, Tailwind, GSAP, an icon library, or any other framework/library.
- Per the kernel CodeGraph rule, before changing a shared component, hook, or token in an indexed project, use `codegraph_explore` to find its consumers; use native tools for styles, markup, and known-path local edits.
- Use the repository's existing tokens, components, assets, content, and `docs/DESIGN.md` when present as the visual authority. Do not generate or fetch external assets as a prerequisite; use real repo assets/data only.
- `shadcn_*` - optional native registry lookup, only when the project already has a shadcn stack (`components.json` present). Use read-only tools one at a time to find real registry components and usage before hand-rolling. The MCP never installs anything; adding a component goes through the project's package runner in shell with manifest review.

## Steps

1. Read the user's brief/intent, acceptance criteria, and existing UI context. Inspect the relevant layout/component files, tokens, assets, data, package manifest, and `docs/DESIGN.md` when present before choosing an approach.
2. Treat the existing visual system or design documentation as authoritative. When `docs/DESIGN.md` records Mobbin reference links, treat them as pattern references subordinate to repo tokens; do not open them in a browser unless **b-browser** is invoked. Before selecting composition or styling, make an explicit, task-conditional design read covering the surface, audience, brand/repository evidence, hierarchy, density, layout variance, and motion posture. State one product-appropriate art direction and its anti-default constraints. Ask one material question only when the requested design direction materially diverges from that authority; otherwise make the smallest contextual choice that fits the product. Treat marketing pages, product apps, dashboards, and trust/regulated surfaces differently rather than applying a rote landing-page formula. Where requirements and target support allow, prefer semantic HTML and native HTML/CSS/browser features before bespoke components or new dependencies. Keep repository UI/design authority primary; do not reduce accessible behavior or override product/design evidence for a smaller implementation.
3. Define the bounded UI slice: component structure and content, loading/empty/error/success states where applicable, responsive behavior, interaction states, semantic HTML, keyboard/focus behavior, contrast, and other relevant accessibility needs. Choose hierarchy, density, and composition from the product context.
4. Implement the smallest coherent change. Preserve existing information architecture, brand, behavior, and tracking in a redesign unless the user approved changing them. Avoid rote generic card grids, gratuitous gradients, fake product screenshots, invented social proof, and invented metrics.
5. Add motion only when it communicates a state or relationship. Use performance-safe mechanisms and provide a reduced-motion fallback; do not introduce an animation library or other dependency without repository evidence and manifest review.
6. Before delivery, self-audit the implementation against the chosen direction and product context: typography, palette, composition/layout repetition, surface/card restraint, meaningful interactions and states, truthful copy/assets, responsive behavior, and accessibility. Record any unresolved gap instead of substituting a generic default.
7. Verify with the narrowest useful existing repository checks for the changed surface, inspect the actual changed paths and diff, and report exact outcomes. Do not run browser work or claim visual proof; hand that evidence request to **b-browser**.

## Pre-delivery checklist

- [ ] Existing tokens, components, assets, content, and design guidance were inspected and followed.
- [ ] A product-appropriate design read, chosen art direction, and evidence-backed anti-default constraints are explicit.
- [ ] Component structure, states, responsive behavior, semantics, keyboard/focus behavior, and relevant accessibility needs are covered.
- [ ] The result is contextual rather than a generic card/gradient/marketing template, with no fabricated assets, data, social proof, or metrics.
- [ ] New imports and dependencies are supported by the manifest and existing stack; registry components were preferred over bespoke equivalents when the shadcn stack is present; no arbitrary package was installed.
- [ ] Motion is purposeful, performance-safe, and reduced-motion friendly when present.
- [ ] Relevant repository checks passed (or their exact gaps are reported), unrelated changes were preserved, and browser/visual proof is explicitly handed to **b-browser**.

## Output format

Report implemented behavior, changed paths, exact checks and outcomes, acceptance coverage, and deviations or gaps. Include a concise handoff when browser or visual evidence is still needed.

## Rules

- Stay within the approved or clearly scoped request; stop and ask the user about a material blocker or scope change before editing further.
- Prefer repository evidence over aesthetic defaults and do not add speculative abstractions, compatibility paths, or dependencies.
- Reject recognizable generic AI defaults such as unmotivated gradients, repeated centered heroes, three equal feature cards, or indiscriminate glass surfaces unless the brief or evidence explicitly calls for them; do not replace them with another fixed aesthetic.
- Also treat these concrete defects as defaults to justify, not bans: nested cards, zero-offset colored glow halos, hairline border plus wide diffuse shadow, animating layout properties (width/height/margin) instead of transform/opacity, functional text under ~11px, body measure well over ~75ch, and interactive targets under 44px. Repository evidence or the brief overrides them.
- Use real repo assets/data only. Do not make image generation or external asset fetching a task requirement.
- The design direction is contextual guidance, not a mandate for a particular font, icon library, dark mode, image-generation workflow, or heavy motion.
- Do not claim browser, screenshot, e2e, or visual proof from code inspection or non-browser checks; route it to **b-browser**.
- Route reusable design-standard authoring to **b-design** and unresolved external facts to **b-research**.
