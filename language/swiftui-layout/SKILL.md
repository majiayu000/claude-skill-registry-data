---
name: swiftui-layout
description: "Repair SwiftUI layout, safe areas, stacks, grids, lists, scrolling, custom Layout, GeometryReader, Dynamic Type, and right-to-left adaptation."
---

# Adaptive layout and scrolling

## Inputs

Identify the actual container proposal, safe areas, content size, supported windows/devices, text-size range, keyboard behavior, and right-to-left requirements.

## Rules

- **LAY-001 — Use container geometry.** Do not derive a resizable view from global screen bounds. Let content and the current proposal determine layout.
- **LAY-002 — Adapt before shrinking.** Reflow or prioritize content before clipping labels or capping Dynamic Type. Fixed sizes need an explicit component contract.
- **LAY-003 — Measure without feedback loops.** Transform geometry into the smallest meaningful value and update state only when that value changes.
- **LAY-004 — Respect safe areas and identity.** Separate edge-to-edge backgrounds from readable/interactive content. Preserve scroll and row identity across updates.
- **LAY-005 — Escalate deliberately.** Start with stacks, grids, alignment, layout priority, and fitting alternatives; use custom `Layout` or readers when the behavior needs them.

## Workflow

1. Reproduce the failure at the affected proposal and text size.
2. Remove conflicting frames, padding, overlays, and nested scrolling before adding constraints.
3. Choose eager versus lazy containers from semantics and measured content scale.
4. Handle keyboard, window resizing, localization, and scroll restoration explicitly.
5. Verify adjacent supported sizes rather than one fixed preview.

## Verify

Render smallest/largest supported containers, accessibility text sizes, long translations, right-to-left content, keyboard-visible states, empty lists, and large datasets. Profile measurement loops and heavy cells where relevant.

## Output

Return the layout decision, boundary cases, visual evidence, and any fixed-size rationale.

## References

Read the [playbook](references/layout-patterns.md) for decisions, failure cases, and source links.

For layout proposals, lists, and scroll state, read the [focused reference](references/layout-and-scroll-edge-cases.md).
