---
name: design-screenshot-spec
description: 'Inspect Figma links through MCP or browser computer use, or analyze screenshots and selected-layer properties. Produce frontend specs and clarify unresolved product behavior before implementation.'
id: 'agents.skills.design-screenshot-spec.skill'
title: 'Design Screenshot Spec'
doc_type: 'skill'
layer: 'skill'
status: 'active'
publishable: true
local_only: false
skill: 'design-screenshot-spec'
tags:
    - 'agents/skill-package'
    - 'frontend/design'
    - 'frontend/spec'
parent:
    - '[[AGENTS|Canonical Agent Policy]]'
related:
    - '[[skills/design-screenshot-spec/references/design-source-inspection|Design Source Inspection]]'
    - '[[skills/design-screenshot-spec/references/product-behavior-review|Product Behavior Review]]'
    - '[[skills/design-screenshot-spec/references/spec-extraction-checklist|Spec Extraction Checklist]]'
    - '[[skills/frontend-design-director/SKILL|Frontend Design Director]]'
    - '[[skills/frontend-layout-implementer/SKILL|Frontend Layout Implementer]]'
    - '[[skills/frontend-visual-qa/SKILL|Frontend Visual QA]]'
depends_on:
    - '[[AGENTS|Canonical Agent Policy]]'
---

# Design Screenshot Spec

## Purpose

Inspect live Figma designs or supplied screenshots, property panels, assets,
and notes to produce a traceable `Design Implementation Spec`. Review the
observed design as a product flow and resolve unspecified design and behavior
decisions with the user before handing affected work to an implementer.
The existing skill name remains stable for bundle compatibility.

## When To Use

- The user sends screenshots of Figma frames, components, screens, or inspect
  panels.
- The user asks to analyze a visual design before implementation.
- The user provides a Figma file, frame, component, or prototype link and asks
  to inspect it or implement its design.
- The next step is frontend layout work and the implementer needs a structured
  spec.

## When Not To Use

- The user asks to edit the design canvas, create files or whiteboards,
  generate a design system, or write Code Connect mappings.
- The user already provides a complete `Design Implementation Spec` and asks to
  implement it. Use `frontend-layout-implementer`.

## Required Context

1. Read `AGENTS.md`.
2. Confirm the classified task is `design-spec` or design intake for later
   frontend implementation.
3. Read `common/approved-patterns.md`.
4. Read `common/anti-patterns.md`.
5. Read `project/design-reference-profile.md` when present.
6. Read `references/spec-extraction-checklist.md`.
7. For live links, read `references/design-source-inspection.md`.
8. After extraction, read `references/product-behavior-review.md` before
   formulating product questions or an implementation handoff.

## Tool Contract

- Resolve `live_design_source` and `design_reference_files` through the current
  tool registry and `tool-capabilities-manifest.json` for the active source.
- A supplied link triggers scoped read-only inspection automatically: use a
  callable Figma MCP read tool first; if unavailable, failing, or incomplete,
  use permitted browser/computer use to inspect the same design visually.
- Browser fallback must support screenshots and pointer interaction with the
  canvas and property panel. Search results or an HTTP fetch are not inspection.
- With screenshots and no link, inspect those images directly; do not require
  a Figma connection. Never invent a tool, session, node, or successful read.
- Follow host tool instructions and permissions. Do not install tools, change
  access settings, edit the source canvas, or write mappings during intake.

## Workflow

1. Inventory links, screenshots, inspect panels, exports, notes, target screens,
   and existing user decisions. Identify the requested frame and state scope.
2. Inspect live links using `references/design-source-inspection.md`; use
   supplied screenshots directly when no link exists. If neither source can be
   inspected, request the smallest missing reference and report the limitation.
3. Group evidence by screen, component, variant, state, and viewport. Record
   source ID, node or selected-layer identity, frame size, image crop/zoom when
   known, access path, and inspection coverage. Match property panels to their
   selected elements before assigning values. Inspect every in-scope component;
   reuse proven identical instances while recording overrides and state changes.
4. Treat each screenshot or design-frame size as a reference coordinate system,
   not as a production container cap. Record whether containment is explicitly
   visible and capture desktop edge anchors plus expected behavior beyond the
   reference viewport.
5. Extract visible layout, hierarchy, typography, color, spacing, sizing,
   radius, shadow, assets, states, and responsive behavior.
6. For typography, prefer copied inspect values or selected-text properties for
   `font-family`, `font-size`, `font-weight`, `line-height`, color, alignment,
   max width, and wrapping. When properties are unavailable, estimate from the
   screenshot and mark each estimate as `screenshot-inferred`.
7. For spacing, separate outside margins, section rhythm, inter-component gaps,
   container padding, and internal control padding instead of merging them into
   one generic gap value.
8. Mark values `source-provided`, `screenshot-inferred`, or `unknown`, with the
   exact source/selection and units; keep user decisions separately traceable.
9. Prefer exact properties only for the same node, state, mode, and revision.
   Reinspect mismatches; ask the user which reference governs unresolved conflicts.
10. Apply `references/product-behavior-review.md`: map observed actions and
    states, inspect available prototype transitions, then ask about every
    unresolved product/design decision needed for the requested scope. Keep
    recommendations unaccepted until the user answers; do not invent defaults.
11. Produce a draft spec with a decision register. Mark affected slices blocked
    until answers settle their dependencies. Continue independent inspection;
    never treat silence or a question limit as approval.
12. Hand off the resolved scope only when implementation was requested. Use
    `frontend-design-director` for requested redesign or visual choices that need
    proposals; source-fidelity work does not itself authorize redesign.

## Output Contract

Final response: return only facts that affect the user's understanding, confidence, or next action. Omit empty fields and workflow narration.

Return a `Design Implementation Spec` with these sections:

- `Source Inventory`
- `Component Evidence And Coverage`
- `Screen And Component Scope`
- `Layout Structure`
- `Typography`
- `Color And Effects`
- `Spacing And Sizing`
- `Assets`
- `States And Interactions`
- `Product Questions And Decisions`
- `Responsive Behavior`
- `Accessibility Notes`
- `Implementation Acceptance Criteria`
- `Confidence And Unknowns`

Keep detailed per-component evidence in the spec; user-facing questions should
name the relevant component, observation, missing decision, and consequence.

## Validation Gates

- Every concrete value must cite its source, selection/state, and confidence.
- A link-only request must attempt an available read path before requesting
  screenshots. Missing MCP alone must not block an available browser fallback.
- Each in-scope component/state is inspected or explicitly marked missing,
  unreadable, or blocked; an overview image is not complete extraction.
- Mixed selections and parent properties must not be attributed to a child.
- `Source Inventory` must record each screenshot's viewport or frame size when
  visible or provided.
- `Spacing And Sizing` must distinguish measured or estimated margins, section
  rhythm, inter-component gaps, container padding, and internal control padding
  with confidence labels.
- `Typography` must distinguish inspect-provided text properties from inferred
  font family, size, weight, line height, color, alignment, and wrapping.
- `Responsive Behavior` must include viewport-aware notes based on supplied
  screenshot widths, desktop edge anchors, and behavior beyond each reference
  viewport, and must mark inferred intermediate behavior explicitly.
- Screenshot or design-frame dimensions must not become runtime `max-width`,
  fixed container dimensions, or equivalent caps without source evidence of a
  centered container and an explicit responsive rationale.
- Missing states, assets, breakpoints, and token names must be explicit.
- Unresolved product behavior, visual deviations, and inferred responsive or
  motion choices must be asked back and block their dependent implementation.
- A static screenshot does not establish transitions, timings, hidden forms,
  validation, persistence, or error recovery.
- The spec must be usable by `frontend-layout-implementer` without guessing the
  target layout intent.
- Report actual MCP/browser/image evidence and access gaps honestly; source
  inspection alone does not prove the implemented UI works.

## Trigger Evals

Should trigger:

- "Here are Figma screenshots with dimensions and colors; write the layout spec."
- "Read these frame screenshots and inspect panels before coding."
- "Create a frontend implementation spec from these design screenshots."
- "Open this Figma node and inspect its components before coding."
- "MCP is unavailable; inspect the linked design in the browser."
- "Which layer do these property-panel values belong to?"

Should not trigger:

- "Implement this existing Design Implementation Spec."
- "Create a new Figma whiteboard."

## Reference Map

- `references/spec-extraction-checklist.md`
- `references/design-source-inspection.md` - live MCP and browser acquisition.
- `references/product-behavior-review.md` - evidence-led product questions and
  decision gates after extraction.
- `skills/frontend-design-director/SKILL.md`
