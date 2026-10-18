---
name: forge-figma
description: "Forge: design-to-code: figma, design to code, mockup, design tokens, pixel-perfect, responsive, breakpoints, style guide, dev mode, handoff, accessibility."
---

# Forge playbook — Design → code (Figma / mockups)

`ui-boss` leads the translation under `build-boss`; a stack reviewer (`react-reviewer` **or** `vue-reviewer`) reviews the built components; `a11y-architect` guards accessibility. Design→code **is** website/frontend work, so the built result also runs under `forge-website` conventions (real content, responsive, a11y, no placeholders). The honesty rule here: state what you translated **from** — a live Figma read (MCP) or provided exports — and never invent measurements you couldn't see.

## Hard rules (non-negotiable)
- **Faithful translation, verified visually.** Rendered output is compared **side-by-side** against the source frame at the design's breakpoints (spacing, sizing, hierarchy, states) — "close enough" from memory is not translation. Screenshot evidence, not assertion.
- **Design tokens, not scattered magic values.** Colours, typography, spacing, radii, shadows are extracted into tokens/variables (CSS custom properties, a tokens file, or a theme object) and reused — the design's real scale, not a fresh hardcoded hex/px per component.
- **Responsive fidelity.** The design's breakpoints are honoured (Figma usually ships desktop + mobile frames); layout adapts. No fixed-pixel-only layout that breaks off-frame.
- **Accessibility is not optional.** Semantic HTML, WCAG **AA** contrast, visible focus states, keyboard navigation, alt text, ARIA where needed. A design can look right and still fail contrast — **flag the failure back**, don't silently ship it. a11y wins over exact pixel-match.
- **Component structure mirrors the design system.** A Figma variant set (e.g. a `Button` with variants) becomes **one** prop-driven component, not copy-pasted one-offs. Real content from the design, no Lorem where real copy exists.

## Team (conditional by stack/level)
Lead: `ui-boss` (design-led) or `build-boss`. Build review: `react-reviewer` **or** `vue-reviewer` (by stack). Accessibility: `a11y-architect`. Figma MCP wiring (opt-in): **`mcp-developer`**. Design critique of the translated result: the `design-is` skill. If it's a marketing/landing surface, `seo-boss` for meta/perf.

## Skills / commands / MCP
`design-is` (audit the translated UI against real design principles — see `~/.claude/rules/ecc/web/design-quality.md`), `browser` (screenshot loop: render → compare to the source frame at each breakpoint), `forge-website` (the built UI must be responsive + a11y + real-content), `/react-build` + `/react-review` (or the Vue equivalents). **Figma MCP is opt-in:** the Figma Dev-Mode MCP server / Figma API lets an agent read the file and pull tokens, measurements, and exports directly — it requires a **Figma access token + MCP wiring** (`mcp-developer` sets it up), and this session's `n8n`/other MCP auth state does not include it by default. **Native fallback (no MCP):** work from owner-provided exports — PNG/SVG frames + a measurement/redlines spec (or a shared style guide). Be explicit: **without the MCP or provided exports, Claude cannot see the Figma file** and any translation is approximate — request the assets rather than guessing.

## Fan-out & flow
L2 a single component or screen; L3 a full design-system / multi-screen translation.
**Serial:** ingest the design (MCP read **or** exported frames + specs) → extract tokens → build components → wire responsive breakpoints → a11y pass → visual diff vs source.
**Parallel:** independent components/screens translate in parallel **once** the token system is fixed (tokens are the shared contract).

## Domain gates
- Rendered output matches the source frame at the design's breakpoints — side-by-side screenshot evidence.
- Design tokens extracted to variables/theme and reused; no per-component hardcoded palette/spacing drift.
- Responsive at the design's declared breakpoints; no fixed-pixel-only layout.
- a11y: contrast meets AA, semantic HTML, visible focus, keyboard-navigable — any contrast failure **in the source** is flagged, not shipped silently.
- Components mirror the design's variant/component system (reusable, prop-driven), not copy-paste duplicates.
- The translation **source** is stated — Figma MCP read vs provided exports — and no measurements are invented.

## Ship-readiness (unique)
Side-by-side visual match at the design's breakpoints (screenshots attached); a tokens file/theme present and used; responsive verified; a11y (contrast AA / focus / keyboard) checked with any source-side a11y defects flagged back; component structure mirrors the design system; the translation source (MCP vs exports) stated honestly — and if neither was available, the output is labelled approximate. Defers to `forge-website` ship-readiness for the built page (real content, no test copy, secrets in env). Advisory checklist; optionally run `codex-reviewer` on component code — not a blocker.
