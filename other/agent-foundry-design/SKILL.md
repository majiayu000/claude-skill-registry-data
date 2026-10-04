---
name: agent-foundry-design
description: "Create, redesign, or review AgentFoundry SwiftUI iOS product UI with the AgentFoundry iOS 26.1 target baseline, native iOS 26 Liquid Glass design, Apple-style design system, polished modern visuals, clickability checks, and shadow/clipping QA. Use when an AgentFoundry task touches app design, SwiftUI UI, target deployment version, Liquid Glass, glass/material surfaces, chat/artifact UI visuals, visual QA, tap targets, rounded corners, shadows, or full redesign."
---

# AgentFoundry Design

## Purpose

Use this skill as the single design authority for AgentFoundry iOS products.

Use TravelPlanner2 as the golden reference for composition and finish, distilled into the universal AgentFoundry product-workspace language. Reuse its hierarchy, atmosphere, continuity, soft geometry, selective glass, artifact-first detail, and floating agent presence; never copy travel-specific screens or colors by default.

The goal is a native iOS 26 product that feels current, tactile, and polished: Liquid Glass surfaces, layered depth, Apple-style typography, SF Symbols, smooth motion, generous radii, vivid product-specific color, readable hierarchy, and real workflow screens. Do not accept boxy prototype UI, web-dashboard styling, raw JSON/debug output, placeholder-only screens, or decorative screens that do not make the product more useful.

## Required References

Load only what is needed:

- Read `references/design-system.md` before creating a new AgentFoundry SwiftUI app, redesigning a screen, or building reusable UI components.
- Read `references/product-workspace-language.md` before defining a new product concept, primary workspace, palette, artifact surface, or agent/composer relationship.
- Read `references/visual-qa.md` before declaring an AgentFoundry UI redesign or visual pass complete.

When another AgentFoundry skill touches SwiftUI UI, target version, Liquid Glass, app surfaces, cards, sheets, navigation, tap targets, shadows, or visual QA, apply this skill before planning and again before final verification.

## Target Baseline

- New AgentFoundry SwiftUI iOS projects use iOS 26.1 as the minimum deployment target when the local Xcode/toolchain supports it.
- Persist the deployment target in the Tuist project graph, shared settings source, or project configuration that regenerates Xcode state. Do not rely only on manual generated `.xcodeproj` edits.
- If local tooling cannot build iOS 26.1, stop and ask before lowering the deployment target.
- Existing projects with a lower target may keep it only when the task is explicitly constrained to existing support. In that case, gate iOS 26-only APIs with `#available(iOS 26, *)` and provide a native material fallback.

## Design Direction

Start from a concept, not from repainting existing boxes.

1. Identify the core product object and user workflow: chat, plan, comparison, tracker, case, order, approval, document, or another durable artifact.
2. Define the three-layer hierarchy: navigation/continuity, durable product workspace, and agent presence.
3. Define the visual concept in one or two sentences: product mood, information density, primary surface, warm semantic signal, and how glass/depth helps the workflow.
4. Create or update a design system layer before scattering one-off modifiers through feature views.
5. Redesign the main screens as native app surfaces with clear hierarchy, useful states, and platform interactions.
6. Verify build, runtime UI, clickability, shadows, clipping, Dynamic Type, and dark/light appearance.

## iOS 26 Liquid Glass Rules

- Prefer native iOS 26 Liquid Glass APIs over custom blur stacks: `glassEffect`, `GlassEffectContainer`, and glass button styles.
- Use `GlassEffectContainer` where multiple glass elements coexist or visually interact.
- Apply glass modifiers after layout and appearance modifiers.
- Use interactive glass only for tappable, focusable, draggable, or otherwise interactive elements.
- Use consistent shapes across related controls. Favor soft Apple-like radii and capsules for prominent controls; avoid square cards and sharp rectangular chrome.
- Layer glass over meaningful background content or color fields. Avoid a blank gray stack of translucent rectangles.
- Use material depth sparingly for hierarchy: primary action, selected object, active surface, elevated card, or floating input. Not every list row needs glass.
- Provide graceful fallbacks for pre-iOS 26 support when an existing project requires it.

## Design System Requirements

Every new or redesigned AgentFoundry SwiftUI app should have a small `DesignSystem` module or folder that owns:

- Color roles: app background, elevated background, glass tint, text primary/secondary, accent, success, warning, danger, selection, separator.
- Typography roles using system text styles and Dynamic Type, not viewport-like scaling or fixed hero sizes inside compact UI.
- Surface styles: background scene, glass panel, glass card, elevated card, toolbar, floating input, sheet, inline artifact card, empty/error/loading states.
- Controls: primary/secondary/destructive buttons, icon buttons, segmented controls, search/input bars, toggles, chips, rows, cards, progress indicators.
- Reusable text rendering for assistant/agent Markdown where the app displays backend Markdown.
- Motion tokens for navigation, card reveal, selection, generation progress, and state changes.

Do not build card-in-card page layouts. Use cards for repeated domain objects, chat/artifact previews, sheets, and contained tools. Page sections should be real app surfaces, not generic floating panels.

## Surface Rules

- Design around the durable product artifact, not around the chat transcript. The detail screen must be useful without rereading the chat.
- Prefer an atmospheric workspace composition: ambient product-specific background fields, one visually primary durable object, selective elevated glass, and a floating agent composer. Do not turn every section into a translucent card.
- Use the universal radius rhythm from the product-workspace language: hero 32–36, panel 26–30, prominent controls 20–24, compact surfaces 16–18, adjusted only when the product concept calls for it.
- In products with stages, options, dates, versions, or comparable objects, use a stable selector or horizontal preview rail whose geometry does not jump as selection changes.
- Use SwiftUI-native navigation, sheets, full-screen covers, tabs, segmented controls, maps, charts, and lists where they match the workflow.
- Keep chat readable: assistant Markdown remains text-forward; rich cards live outside the text bubble chrome.
- In chat creation and chat composer screens, tapping free/non-interactive space must dismiss the keyboard without breaking message scrolling, card taps, text selection, or explicit controls.
- Use SF Symbols in controls and rows when a symbol improves scanning.
- Empty, loading, partial, stale, failed, and generating states must be designed, not left as debug text.
- Do not show fake affordances. If data is missing, represent the surface as `generating`, `needs_input`, `partial`, `stale`, or `failed`.

## Clickability And Shadows

These are hard gates:

- Tappable controls have at least a 44x44 pt hit area, either through layout or `.contentShape`.
- Text fields, send buttons, cards, chips, toolbar buttons, segmented controls, and sheet controls can be tapped reliably without overlapping transparent overlays.
- On chat creation/composer screens, a tap on free background space dismisses the keyboard. Implement this through the project's approved focus/dismiss pattern, and ensure the background tap gesture does not consume taps meant for messages, cards, links, scroll views, or controls.
- Card taps route through typed app state/reducer actions; renderer views should not mutate backend state directly.
- Shadows, glows, and glass highlights are not clipped by parent stacks, scroll views, masks, or over-aggressive `.clipShape`.
- If a component has an outer shadow, keep clipping inside the background shape and leave parent padding/scroll margins for the shadow. Use `.scrollClipDisabled()` where appropriate and available.
- Do not place important controls flush against safe areas or sheet edges.

## Verification Gate

Do not call an AgentFoundry UI/design pass complete until:

- The app builds with the required target baseline.
- The changed surfaces run on Simulator or device.
- At least the main happy path, loading, empty, failed, and restored states have been visually inspected.
- Tap targets are reachable and do not conflict with overlays or gestures.
- Shadows/materials are visible and not clipped.
- Text respects Dynamic Type enough not to clip in common larger sizes.
- Light and dark appearance remain readable.
- No raw JSON, debug labels, placeholder-only panels, or web/admin-looking screens are shipped as user-facing product UI.

## Output Shape

When using this skill for planning or implementation, state:

- Target baseline and whether iOS 26.1 is supported locally.
- Design concept.
- Design system components/tokens to add or change.
- Screen-by-screen redesign plan.
- Liquid Glass/API choices and any fallbacks.
- Clickability and shadow/clipping QA checks.
- Verification commands and remaining manual UI QA.
