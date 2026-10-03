---
name: codex-frontend-design
description: Use when designing or redesigning a web UI; select fast, prototype, or studio from the requested scope.
load_priority: on-demand
version: "18.1.0"
---

## TL;DR

Keep one-page and one-component work fast. Route a multi-route product flow to `prototype`: define the user and UX contract, choose one visual thesis and token set, build a runnable prototype, then review it with complete responsive evidence. Use `studio` only when the user asks for multiple directions or a new brand identity. A previously approved design is implementation-only.

## Activation and routing

- Use for `$design`, `$ux`, `$direction`, `$refine`, or requests to create/redesign an interface or product flow.
- Choose `fast` for one page/component, a small visual refinement, or a narrow extension of an existing system.
- Choose `prototype` when the ask spans multiple routes/screens, a complete product flow, onboarding/checkout, or a product prototype whose important states must work together. `prototype` is an internal mode; keep the public `$design` alias.
- Choose `studio` only for explicit alternatives/multiple directions, `$direction`, or a new brand identity. It still produces one selected direction before build. Do not route every redesign to studio.
- If the design is approved and the user asks to implement it, skip design discovery and preserve the approved direction.
- When route scope is unclear, inspect the request and repository. Ask only for a missing fact that could change a consequential design decision; otherwise record the assumption.

## Fast path

1. Complete `references/design-brief-template.md` (audience, job, tone, memorable detail, constraints).
2. Inspect incumbent styles/components and product facts. For a new surface, compare two plausible layout structures with `references/layout-decision-framework.md` and choose the better content fit; skip this comparison for narrow refinements. State the composition thesis, type/color/spacing strategy, and any token changes before coding.
3. Implement with `codex-frontend-implementation` and working content/states, not an inert screenshot mock.
4. Apply the contextual audit in `references/anti-slop.md`, then run `$visual-gate` for substantial UI changes.

Do not demand a spec or design dossier for a small edit. Leave a short rationale in the handoff when a design decision has meaningful tradeoffs.

## Prototype pipeline

Follow `references/prototype-pipeline.md` in order. Do not skip directly to component generation.

1. **Understand the product and people.** Establish primary users, situation, task, success signal, product constraints, existing design authority, and credible content/proof. Separate known facts from assumptions; do not invent claims.
2. **Set the UX contract.** List routes/screens and their purpose, primary path, navigation, route transitions, realistic content bounds, interaction states, responsive reflow, keyboard/focus order, and accessibility needs. Save it under `.codex/design/surfaces/<slug>.md`.
3. **Choose one visual direction.** Compare structural layout hypotheses against the real content and user task using `references/layout-decision-framework.md`; write one product-specific composition thesis and document why that layout fits. Decide information hierarchy, density, type/color/material/motion tokens, image/icon strategy, and asset provenance. Persist a concise direction/tokens file in `.codex/design/`. Reuse incumbent tokens unless the contract calls for a change. Offer alternatives only when requested.
4. **Build a runnable prototype.** Implement the agreed routes, primary interactions, and critical empty/loading/error/success/permission states. Keep realistic, varied content. Verify navigation and controls actually work; do not label a static collage a functional prototype.
5. **Review and refine.** Run mechanical source checks and functional/a11y review. Capture every route and required state at the responsive profiles and breakpoint edges in `references/responsive-evidence.md`. Inspect every stitched image and its original slices; fix high-confidence defects and contextually proven slop. Allow at most two inspect/fix rounds, then record remaining issues honestly.
6. **Hand off with evidence.** Summarize implemented routes/states, chosen direction and assumptions, tests/checks actually run, capture manifest location, review status, and unresolved limitations. Store QA evidence under `.codex/design/reviews/`. Missing browser/screenshots/review means `DEGRADED`, never approved.

The prototype is ready for design handoff when its main flow works, important states have a visual treatment, no high-confidence issue remains unexplained, and each required route/state/viewport has reviewed capture evidence. A tool cannot prove absolute beauty; ground each visual judgment in a specific route, state, viewport, and image.

## Studio path

When the user requests options or a new identity:

1. Ask at most two material questions, only if repository/product evidence cannot resolve them.
2. Present three genuinely different directions with thesis, product fit, tradeoff, and implementation consequence. Avoid near-identical palette variations.
3. After selection, write the UX contract and direction/tokens, then build through fast or prototype according to scope.

## Design decision rules

- Product facts, accessibility, user task, and incumbent design authority constrain visual exploration.
- A visual device (gradient, glass, shadow, rounded container, animation, unusual cursor, illustration, or asymmetry) is neither automatically good nor bad. State what it communicates or enables, verify it works at target sizes, and remove it when it has no product job.
- Prefer one clear hierarchy and a coherent token system over piling on effects. Do not use an aesthetic preset as a substitute for a product-specific layout thesis.
- Keep source references and asset provenance with the direction notes. Do not copy reference layouts/assets wholesale.

## References

- `references/prototype-pipeline.md`
- `references/layout-decision-framework.md`
- `references/responsive-evidence.md`
- `references/anti-slop.md`
- `references/grammar.md`, `references/composition.md`
- `references/component-states.md`, `references/layout-adaptation.md`, `references/motion.md`
