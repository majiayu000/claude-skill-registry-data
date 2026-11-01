---
name: figma-pixel-implement
version: "1.8.0"
user-invocable: true
description: "Implement Figma UI with export-faithful assets, a screen×state inventory, a control measured in its shipping parent, and a durable living spec in the target repo (state/mode/basis, required Assets subsection). With a component workbench (Storybook or similar), also deliver inventory-covering stories and Spec-locking tests. Use when implementing from Figma URLs/nodes or pixel-level restore / 按稿实现; light/dark is in scope when the file has modes or the project has theme switching. Same run measures laid-out frames via figma-pixel-verify until pass; no person between iterations. Triggers — 「像素级还原」「按稿实现」「Figma 对齐实现」「还原 Figma」「figma 保真实现」「暗黑模式还原」「多主题保真实现」 / implement from Figma, pixel restore, dark mode implement, multi-theme fidelity. Do NOT use for code→Figma canvas writes, no-design creative UI, or post-impl alignment checking alone (use figma-pixel-verify)."
---

# Figma Pixel Implement

Implement UI from a Figma node into the target codebase with **export-faithful assets**, a **screen × state inventory**, and a **durable living spec** in the target repo that `figma-pixel-verify` can measure against.

**Completion boundary:** this skill ends at “implemented + measurable contract” (code + **file path** to Inventory, Spec, and **Assets** sections). A session-only table is **not** complete. Missing Assets rows for implemented visible graphics means implement is incomplete. When the project has a component workbench, story coverage of the in-scope inventory (states × context) is also part of implement complete (Workflow 9). Pixel alignment is owned by `figma-pixel-verify`, which this run continues into. The user-facing result is that skill’s overall PASS. Iterations stay inside the run.

This skill is **platform-agnostic** (Claude Code / Cursor / OpenCode / others). It requires a **Figma design-context capability**, not a particular Agent’s skill id.

**Visual source of truth:** the named Figma node. Walkthrough or QA notes that conflict with the current node are recorded as notes/residuals; they do not replace `expected`.

## Prerequisites

1. **Figma design-context available (hard gate)** — Confirm the Agent can fetch structured design payload for a node (design context, metadata, screenshot, asset export as the environment provides). If that channel is missing or auth fails, **stop**: tell the user how to enable Figma MCP / plugin / equivalent for *their* Agent. Do **not** invent a single hard-coded install path as the only option. Do **not** invent UI from the URL alone.
2. **Optional: platform Figma→code guidance** — If this Agent already ships an official Figma design→code skill or guide (names vary by product; one Cursor plugin example is `figma-design-to-code`), load it when present and follow its URL parsing / Code Connect / adaptation rules. **Missing that named skill is not a blocker**—continue with Figma MCP (or equivalent) + this skill’s fidelity rules. Do not require a Cursor-only skill id on Claude Code, OpenCode, or other Agents.
3. **Figma URL or node** — Prefer a `figma.com` design/make URL or explicit `fileKey` + `nodeId`. If missing, ask once with clarifying-question discipline.

## Workflow (ordered)

1. **Parse target** — Extract `fileKey` / `nodeId` (convert `node-id=1-2` → `1:2`). Note frame name for the spec table.
2. **Fetch design context** — Call the environment’s design-context tool after step Prerequisites. Treat output as a **reference to adapt**, not paste-ready final code.
3. **Large frames** — If the payload is truncated or the frame is clearly multi-section: fetch **metadata/structure** first, then fetch and implement **every visible child section**. As each visible section is implemented, **append** its inventory and spec rows to the living artifact. Unfetched visible sections mean implement is **incomplete**. Prefer variables/tokens over guessed literals. On design-channel rate limits, pause and report the unfinished sections.
4. **Screen × state inventory** — Before the spec table, list screens/sections × visual states from the design (component variant names, prototype reactions that map to appearance, and **readable annotations / comments / adaptation notes**). Documented states such as default / hover / pressed / disabled / selected become inventory entries. Readable notes become inventory rows (`blocked`, visual state, or `out-of-scope: behavior` as they fit). Prototype or product **behaviors** that are not computed-style rows (window drag, auto-follow scroll, mouse-wheel paging) stay on the list as `out-of-scope: behavior`. If the design has no Hover (or equivalent) variant, record `no-variant-in-design` — do not invent hover colors or sizes from a note. When a note conflicts with the named node’s structured value, keep `expected` on the node and record the conflict. When the component’s host container can vary (resizable width, narrow squeeze), add a `context` axis to the inventory: the product width floor, preset checkpoints, and squeeze pressure become inventory rows or an optional `context` column.
5. **Detect theme structure** — Establish how the design expresses themes: variable collections with multiple modes (e.g. `light`/`dark`), or separate per-theme frames/variants. **Theme is in scope** when the file has multiple modes **or** the project already switches theme (`data-theme`, token files, `prefers-color-scheme`). Record the theme inventory (mode names or per-theme frame nodeIds). When neither the file nor the project has a second theme, stay on the requested frame/variant.
6. **Build the living spec** — Resolve a durable path in the **target repo**: prefer an existing Figma doc directory if the project already has one; otherwise `docs/figma/<safe-frame-name>.md`. Create Inventory, Spec, and a required **Assets** subsection there (leave Verify empty for `figma-pixel-verify`). After the inventory, write measurable rows — **mechanically expanded from the fetched node tree, never sampled**. Every fetched visible node yields rows for its position (x/y relative to its parent or section) and size; every text node additionally yields its full typography set (font-size, weight, line-height, color, alignment) and its line count when multi-line; every container additionally yields padding, gap, radius, shadow, and each child's cumulative absolute offset from the frame origin; sibling spacing is recorded with `basis` naming the relationship. A fetched node is either covered by spec rows or listed as `out-of-scope` with a reason — silent omission makes the spec incomplete. Minimum columns: `node` / role, `state`, `property`, `expected` (Figma exact), `unit`, `basis` (which parent or sibling the number is relative to), `token` / class in repo, `source` (variable, MCP field, metadata, or Code Connect component), `primitive` (`project-component` | `custom-layout` | `platform-control`). **Fill ownership:** if the node has no readable fill, Spec `expected` is transparent / `none` — a screenshot of surrounding color does not own that fill. **Text color:** use the text node’s own readable Figma variable as `token` / `source`; if none, record `raw-only`. Screenshots are visual reference only—not the sole source of numbers. When theme is in scope, add a `mode` column (or one row per mode) for theme-varying properties: resolve per-mode values from the design itself (variable `valuesByMode` when the channel exposes it, otherwise re-fetch with the file/frame mode switched or via the per-theme frame); shared values stay single-row. A session note is a draft only—implement is incomplete until the file exists (including Assets). **Reference exports:** export a raster image of every in-scope frame from the design source, store it in the target repo, and record node id, local path, and export scale in the living artifact. `figma-pixel-verify` uses these as its differential-sweep baseline; a missing reference export for an in-scope frame means implement is incomplete. Template: [reference.md](reference.md).
7. **Map to project** — Reuse existing components, tokens, and layout primitives. Prefer design-system variables over hard-coded values when the project already has them; flag unbound one-offs; when hard-coding is required for fidelity, record the expected value in the spec table. **Layout-measurable control:** when the node publishes an explicit width and height, the control that remains after layout inside the shipping parent (the container the screen uses) must have that box. A probe that lays out the control with no parent does not count. Prefer a project component whose laid-out size matches. When every stock platform control lays out to a different size, build a custom control and assign track, thumb, and label frames in that layout pass (`primitive: custom-layout`). `platform-control` is valid only after a layout probe of a stock instance matches the spec box. A flattened payload (outer box only) still binds that outer box to a matching project component or `custom-layout`. Inner sizes come from a structured child fetch or an existing spec row that cites a design node.
8. **Assets (hard rules)** — See [reference.md](reference.md) whitelist/blacklist. Export real image/SVG bytes into the project (or an approved dynamic source). Cut each visible icon/logo as **one file from the outer instance** (not stacked leaf paths). Reconstruct **that instance’s** width, height, and offsets — not a generic 16/20/24 shell unless the instance uses it. Restore overlap and floating layers from the readable instance hierarchy. Keep SVG aspect ratio unless the design requires stretch. Use `<img>` / framework image / export-preserving SVG. **Do not** use hand-authored path placeholders, CSS `mask` / `mask-image` + fill/`currentColor` recolor, or invent mask theming when only a light export exists (prefer a second export or record pending). When theme is in scope, export design-provided assets per theme (from each mode or per-theme frame)—one theme's export plus an invented recolor stays forbidden. Record every in-scope graphic in the Assets subsection (node, local path, format).
9. **Stories & component tests** — When the target project has Storybook or a similar component workbench (existing story setup, workbench config, or scripts): write **stories covering every in-scope Inventory row** (state × context), each exposing its state through a declarative entry the Agent can drive later (test id, knob, or auto-action), following the project’s existing story conventions. Add a **Stories** subsection to the living artifact mapping story → covered inventory rows → entry (template: [reference.md](reference.md)). Write **component tests locking the key Spec values** (geometry, color, token mapping) when the project has a test setup; when it does not, record the suggestion instead of scaffolding (advisory, not blocking). When no component workbench exists, record the adoption suggestion once (isolated, observable, agent-testable surface) — measurement falls back to the channel ladder in `figma-pixel-verify`.
10. **Theme mapping** — Stay **design-faithful** to the requested frame/variant colors. When theme is in scope, map theme-varying variables onto the project's theming mechanism (CSS custom properties / design tokens / `data-theme` or `prefers-color-scheme` switching) instead of duplicating hard-coded per-theme literals.
11. **Hand off** — Give the living-artifact **path** (Inventory + Spec + Assets present; + Stories when a workbench exists). In the same run, load `figma-pixel-verify` and follow it. On a non-pass row, that skill fixes and remeasures before the user sees a result. The user-facing result is overall PASS, or FAIL that names a measurement command that could not run. No path = implement incomplete.

## Tool intent (platform-agnostic)

Describe goals; let the Agent pick native tools:

| Intent | Examples of how Agents may satisfy it |
|--------|----------------------------------------|
| Structured design payload | Figma MCP design-context / metadata tools |
| Visual reference | Screenshot or canvas capture tools |
| Asset download | MCP asset download or export APIs |
| Code / living-spec edits | Native edit/write tools (spec file lives in the target repo) |

Do not require a named MCP server id or CLI as the only path.

## Relationship to other skills

| Capability | Boundary |
|------------|----------|
| Agent-native Figma→code guidance (optional, name varies) | When present, load for MCP hygiene; never a hard dependency on one product’s skill id |
| Figma MCP / design-context tools | Hard gate for structured fetch |
| `figma-pixel-verify` | Owns measured pass/fail; writes the Verify section on the same artifact (or Spec source sibling) |
| Host PDCA workflows | Incomplete implement if no durable path; missing Verify section fails their verification stage |
| `design-approval-gate` | Host workflow pre-impl approval — orthogonal |

## Pitfalls

- Treating a Cursor-only skill name as required on every Agent.
- Treating MCP code as final without project adaptation.
- Claiming “pixel perfect” without `figma-pixel-verify`.
- Using CSS mask recolor for icons that Figma exported as flat assets.
- Skipping the spec table so verify has nothing measurable.
- Treating a session-only table as implement complete (no durable path).
- Sampling a large frame’s chrome and calling implement complete.
- Inventing hover or dark values the design does not provide.
- When theme is in scope: implementing only the requested theme and hand-rolling the other themes' values or assets instead of resolving them from the design.
- Using the node’s own padding as `expected` when the design relationship is “distance to sibling X”.
- Claiming pixel PASS for `out-of-scope: behavior` items.
- Painting a solid fill because a screenshot looks filled when the node has no readable fill.
- Reassembling an icon from leaf-path fragments or a generic 16/24 wrapper.
- Replacing a readable Figma text variable with a self-invented semantic alias.
- Treating implement complete without an Assets subsection.
- Declaring implement complete when a component workbench exists but stories do not cover the in-scope inventory rows.
- Writing stories/tests that assert numbers from chat or walkthrough notes instead of the Spec table’s `expected`.
- Sampling “key values” into the spec table instead of mechanically expanding every fetched node — a missing row is unmeasurable downstream (unknown unknown).
- Handing off without per-frame reference exports — the differential sweep has no baseline.
