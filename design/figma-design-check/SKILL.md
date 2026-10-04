---
name: figma-design-check
description: Verify a planned or completed UI change against the Figma design via the Figma MCP before writing or editing component, layout, color, spacing, typography, sizing, or interaction-state code. Use when building or changing any visual surface and a Figma reference exists. Gated by capabilities.figma — skip with a capability-absent note when it is false.
---

# Figma Design Check

Verify every UI change against the Figma design **before** implementing it, using the
Figma MCP server. The Figma design is the source of truth for visuals; code must match
it (or the user must explicitly approve a deviation). A design match never waives the
accessibility or visual-regression gates that follow.

## Profile keys consumed

- `capabilities.figma`
- `framework.ui`
- `architecture.source_root`
- `architecture.component_prefix`

## Capability gate

This skill is gated by `capabilities.figma`. When it is `false` — or when the Figma MCP
server is not configured/reachable — record a capability-absent note and degrade:

- `SKIPPED: figma-design-check` when `capabilities.figma` is `false`. Note
  "Figma parity check not configured for this project", then proceed to the UI change
  without it — but **never invent the design intent from memory**. If no design reference
  exists, ask the user for the intended look (see "Prerequisite" below).
- The skip is bounded to the **visual-parity** check only. It does **not** waive the
  accessibility gate (route to the `accessibility-auditor` agent) or the visual-regression
  gate (the target mapped by `make.test_visual`, driven by the `qa-visual-tester` agent).
  Those run regardless of `capabilities.figma`, subject only to their own gates: the
  visual-regression lane is itself skipped with its own capability-absent note when
  `capabilities.visual_testing` is `false` or `make.test_visual` is `null`.

When `capabilities.figma` is `true`, this gate runs **before**
[frontend-component-development](../frontend-component-development/SKILL.md) and before any
UI edit.

## When to use (mandatory before UI changes)

Run this gate before ANY change that affects what the user sees: new or modified React
components (the project's `architecture.component_prefix` UI primitives, e.g. `UI*`),
layout, color/fill/border, spacing, typography, sizing, icons, or interaction states
(default / hover / focus-visible / active / disabled / loading / error).

It does NOT apply to pure logic, data-layer, test-only, or non-visual config changes.

## Prerequisite: a design reference

You need a Figma reference for the affected UI: a `figma.com` file/node URL, a node id,
or the user's current Figma desktop selection. **If no reference is available, ask the
user for the Figma link (or confirm there is no design for this surface) before
implementing the UI change** — do not silently guess the design intent.

## Workflow

1. **Identify the surface + its Figma node.** Map the component/screen you are about to
   change (under the source root, `architecture.source_root`) to the corresponding Figma
   frame/component.
2. **Pull the design via the Figma MCP tools**, exposed under whatever server alias the
   project has configured (load the tool schemas with `ToolSearch` first):
   - `get_design_context` — structured design + code context for the node.
   - `get_screenshot` — the rendered visual to compare against.
   - `get_variable_defs` — design tokens (colors, spacing, radii, type).
   - `get_metadata` — node structure/hierarchy when needed.
   - `get_code_connect_map` — existing component ↔ code mappings, if any.
3. **Compare the planned change to the design**, field by field: fill/background,
   text/label color, border + radius, spacing/padding, typography, size, and **every
   interaction state** the design defines (not just the default). Prefer the repo's design
   tokens (the theme / color modules under `architecture.source_root`, surfaced through the
   `framework.ui` theme) over raw literal values, and check they match the Figma variables.
4. **Decide** (see "Decision" below).
5. **After implementing**, re-verify the result against the Figma screenshot and report
   the comparison. The live-browser and visual-regression re-check belongs to the
   `qa-visual-tester` agent (the target mapped by `make.test_visual`).

## Decision

- **Match** → proceed with the implementation.
- **Divergence** → STOP. Surface the specific discrepancy (design value vs planned value)
  to the user and get a decision. The design wins unless the user explicitly overrides;
  record the override in your report.
- **No design exists for this surface** → tell the user and confirm the intended look
  before coding.

## Notes

- This is a lightweight **verification gate** — the "does my change match the design?"
  check before edits — distinct from any autonomous pixel-perfect Figma→code loop. Use
  this gate for every UI edit; reach for a full automated loop only when explicitly asked.
- A design match does **not** waive accessibility: still run the `accessibility-auditor`
  agent for UI code. If the Figma design itself fails a WCAG gate (e.g. contrast), flag it
  to the user — accessibility constraints can override the visual design.
- Keep evidence in your response: which Figma node you checked, the values compared, and
  the match/divergence outcome.

## Related skills

- [frontend-component-development](../frontend-component-development/SKILL.md) - The
  implementation skill this gate runs immediately before.
- [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) -
  Lighthouse and accessibility floors that a visual match must not regress.
