---
name: glowup-ui
description: Build distinctive new web apps, transform existing frontends, or refine already-designed interfaces. Use when asked for app creation, full UI redesign, modernization, visual hierarchy, responsive layouts, or scoped visual polish. CREATE establishes composition and shared components on the first pass. TRANSFORM improves an existing app across affected pages while preserving routes, content, data, APIs, behavior and branding. REFINE preserves identity and composition while repairing observed weaknesses. Especially useful for React, Vite, Next.js and Tailwind; adapt to the existing stack. Skip backend-only work.
license: MIT
compatibility: Agent Skills-compatible coding agents including Claude Code and Codex. Helpers use Node.js 20+ built-ins. Browser review uses an available browser or optional Playwright; never installs silently. No paid service required by the skill.
metadata:
  version: "0.1.2"
  homepage: "https://github.com/avivgerz-hue/glowup-ui"
---

# Glowup UI

Turn the user's task into a deliberate composition, then implement it. `<skill-dir>` means this folder. Follow the request and existing brand over any recipe.

## Select scope
- **CREATE:** empty project/new standalone product. Read [create-mode.md](references/create-mode.md). Establish the design in the first implementation.
- **TRANSFORM:** existing product, including new pages within it. Read [transform-mode.md](references/transform-mode.md). **Polish** keeps composition and identity. **Full redesign** may change layout, type hierarchy and shared visual components; it preserves brand, product and behavior. Do not interpret every redesign as tiny polish. Rebranding requires explicit intent.
- **REFINE** (polish): an already-designed interface or a local improvement. Use TRANSFORM's polish scope; preserve identity and composition, fix observed weaknesses.
- One element or bug: fix that scope using the existing system; skip scaffolding and broad audit.

## Execute
1. In at most four lines state the user task, scope, strongest existing feature and main weakness (or intended focal point for CREATE). No planning document.
2. Read the selected mode and [design-quality.md](references/design-quality.md). For CREATE or substantial TRANSFORM, use [design-decisions.md](references/design-decisions.md): infer TRANSFORM depth (polish/recompose/reframe), compare distinct product-specific compositions, then choose one. Skip exploration for REFINE or an already-chosen user direction. Inspect shell, theme, representative page and existing checks once. For a new system, `scripts/direction.mjs` supplies contrast-checked tokens and a product composition brief; scaffolding includes it. For an existing app lacking a clear hierarchy, use `scripts/composition.mjs --product "..." --mode redesign` without generating a replacement theme. Recipes are suggestions, not requirements.
3. Decide the page's focal region, supporting context, type roles and one useful signature treatment. Prioritize composition/navigation, typography, shared components and responsive states before decorative details. For full redesign, fix the shared causes across affected pages; three priorities can represent many changes, not a three-edit ceiling.
4. Implement in the app, not just a proposal. Check one representative screen, then propagate shared primitives and adapt every requested screen/state, including tabs/dialogs without separate routes. Preserve handlers, state, content, routes, APIs, auth, tests, assets and unrelated work. Use one global navigation system. No dependency or framework changes solely for styling.
5. Verify to scope using [verification.md](references/verification.md). For full work inspect actual desktop/phone screenshots and exercise the primary flow. Compare TRANSFORM with the original against its stated design priorities. Critique actual hierarchy, product specificity, navigation, consistency and phone composition separately from mechanical checks. Correct the biggest evidenced unmet priority or regression within two review rounds. Report incomplete implementation and unverified views explicitly.

## Design contract
Account for every requested screen/state as implemented, intentionally preserved with an observed reason, or incomplete. A full redesign is complete only when its identified hierarchy/composition weaknesses are addressed across affected pages, shared controls agree, and phone layouts and primary interactions work. Color/shadow-only edits do not satisfy a composition problem. Preserve already-strong sections; do not chase diff size or force novelty.

## Tools and effort
- `scripts/inspect.mjs [dir] [--scope redesign|refine]`: one orientation pass with routes, shared files and project checks; scope follows the request, not detected styling.
- `scripts/checkpoint.mjs save|check [dir]`: original-state fingerprints; save before edits, never reset to hide a failure. Warnings require review, not blind rollback of authorized design changes.
- `scripts/composition.mjs`: compact product/layout/type/phone decisions; explicit `--profile finance|commerce|productivity|portfolio|booking|chat|general` overrides keyword matching. Read-only, no network.
- `scripts/scaffold.mjs` / `scripts/direction.mjs`: CREATE foundation; keep an existing stack and brand. Do not scaffold inside an existing app.
- `scripts/screenshot.mjs`, `scripts/review.mjs`, `scripts/compare.mjs`: capture and group rendered issues. Measurements are not aesthetic scores or proof of preserved behavior.
- `scripts/verify-flow.mjs`: optional browser outcome assertions when existing behavior tests do not cover an affected flow; see verification guidance.
- `scripts/palette.mjs`, `scripts/contrast.mjs`, `scripts/lint.mjs`: focused checks when relevant. Do not run every helper by habit.

Batch related reads; change shared components before repeating page edits. Small polish needs targeted checks, full redesign needs route/phone coverage. Reuse the browser and check results; no repeated analysis, mandatory planning files, decorative dependencies, invented content, silent commits or uploads. Never claim activation, visual improvement or testing without evidence.
