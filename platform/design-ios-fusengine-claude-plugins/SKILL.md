---
name: design-ios
description: "Use when designing a screen or flow for any Apple platform — iPhone (incl. iPhone Duo), iPad, Mac, Apple Watch, Apple TV or Vision Pro — deliverable is a device/window-framed HTML mockup and a handoff spec, never SwiftUI code."
when-to-use: "Designing an iOS, iPadOS, macOS, watchOS, tvOS or visionOS screen or flow — the deliverable is a framed HTML mockup and a handoff spec for swift-expert or an Apple-platform developer to implement, not working SwiftUI."
keywords: ios, ipados, macos, watchos, tvos, visionos, iphone-duo, hig, dynamic-type, liquid-glass, contrast, handoff, mockup
priority: critical
related: design-method, design-system, design-review
---

<objective>
Produces Apple-platform mockups and developer handoff specs: design tokens mapped to the
HIG text styles of the target platform, semantic colors with verified contrast, size-class
aware canvases, Liquid Glass used only in the functional layer, and platform conventions
(system window frame on macOS, focus on tvOS, glass windows and ornaments on visionOS,
glanceable screens on watchOS, vertical controls on iPhone Duo).

The deliverable is a framed HTML mockup plus a SwiftUI-ready handoff spec (named tokens,
text styles, semantic colors, sizing, states, spacing). This skill never writes SwiftUI —
implementation goes to `swift-expert` or an Apple-platform developer.
</objective>

## Design for Apple Platforms — Mockup and Handoff, Not Code

### When
After `design-system` tokens exist.

### Input
- `design-system.md` — OKLCH palette, typography direction, motion personality.
- The screen/flow and the target platform(s). Pick the platform reference first:

| Target | Read |
|---|---|
| iPhone | steps below + `references/dynamic-type.md` |
| iPad, resizable window, iPhone Duo | + `references/ipados-iphone-duo.md` |
| Mac | + `references/macos.md`, `references/type-scales-other.md` |
| Apple Watch, Apple TV, Vision Pro | + `references/watch-tv-vision.md`, `references/type-scales-other.md` |

### Steps
1. **Map tokens to platform roles.** Typography → the platform's HIG text styles by name
   (iOS/iPadOS Dynamic Type: Body 17 pt … Caption 2 11 pt; macOS fixed styles: Body 13 pt
   … Large Title 26 pt; tvOS/watchOS tables) — `dynamic-type.md`, `type-scales-other.md`.
   Colors → semantic roles, never raw hex — `semantic-colors.md`.
2. **Choose canvases by size class**, not by device: at least compact width, regular width,
   and the key screen at AX5 text size. The HIG no longer publishes device point sizes —
   take them from Xcode Device Hub and record the source — `viewports.md`.
3. **Build the HTML mockup**: frame at the recorded point size (1 pt = 1 CSS px),
   `viewport-fit=cover`, `env(safe-area-inset-*)` for Dynamic Island / home indicator —
   `mockup.md`. macOS: a standard system window frame, never custom chrome — `macos.md`.
4. **Liquid Glass only in the functional layer** (tab bars, toolbars, sidebars, key
   controls), never in content. Regular variant by default and for text-heavy surfaces;
   clear only over rich media, with a 35% dark dimming layer over bright content; accent
   color on the primary action's background, sparingly. No published corner radius —
   concentric nesting instead — `liquid-glass.md`.
5. **Verify targets and contrast**: platform control sizes (iOS 44×44 pt, macOS 28×28,
   tvOS 66×66, visionOS 60×60, watchOS 44×44) and spacing — `touch-targets.md`. Contrast
   **4.5:1 minimum** (3:1 for ≥18 pt or bold), **7:1 target** for custom colors and small
   text, checked in light, dark **and** Increase Contrast — `semantic-colors.md`.
   Sources: https://developer.apple.com/design/human-interface-guidelines/dark-mode and
   https://developer.apple.com/design/human-interface-guidelines/accessibility.
6. **Sidebar ≤ 2 levels.** Deeper hierarchy → a split view with a **content list between
   the sidebar and the detail view**, not a third disclosure tier. Consider a tab bar
   first on iPad. Source:
   https://developer.apple.com/design/human-interface-guidelines/sidebars.
7. **Platform pass** — apply the platform reference picked above (macOS desktop tinting
   only under the graphite accent; tvOS 60/80 pt safe area and focus growth; visionOS
   ornaments for controls only; watchOS ≤3 glyph buttons per row; iPhone Duo controls on
   the side and the fold reserved region).
8. **Look at the render** — screenshot each canvas (light, dark, AX5) and Read the PNGs
   before calling the mockup done; fix what you see, then hand off to `design-review`.
9. **Write the handoff spec** per `handoff-swiftui.md`: named tokens only, text styles by
   name, semantic colors, sizing (fixed/hug/fill), all states (disabled/pressed/focused,
   plus pointer style on macOS and focus on tvOS), spacing in pt, canvas sources.

### Failure Handling
- Screenshot tooling unavailable → say so in the report (`visual check: not run`) and
  describe the mockup with exact pt values; never claim a visual check that didn't run.
- A needed value isn't in the references or on the cited HIG page → mark it "to reconfirm
  on developer.apple.com"; never invent a number. Apple publishes **no numeric spacing or
  corner-radius grid** — don't impose an 8-pt grid; a chosen value is a project token.

### Output
- Framed HTML mockup(s) per canvas, plus their screenshots.
- `handoff.md` with named tokens, text styles, semantic colors, sizing, states, spacing,
  canvas sources — ready for `swift-expert`.

### Next → `design-review` (mockup-scoped: screenshot, contrast, no full site audit loop).

### References
| File | Purpose |
|------|---------|
| `references/dynamic-type.md` | iOS/iPadOS Dynamic Type (Large + AX5), default/min sizes — HIG Typography |
| `references/type-scales-other.md` | macOS, tvOS, watchOS text styles; visionOS notes — HIG Typography |
| `references/semantic-colors.md` | Semantic roles, contrast 4.5/3/7:1, increased contrast, base/elevated — HIG Color, Dark Mode |
| `references/viewports.md` | Size classes, safe areas, canvas sizing via Device Hub — HIG Layout |
| `references/liquid-glass.md` | Liquid Glass layering, variants, color, per platform — HIG Materials, Color |
| `references/touch-targets.md` | Control sizes for all platforms + spacing — HIG Accessibility |
| `references/macos.md` | Window frame, fixed type, desktop tinting, pointer, sidebars — HIG |
| `references/ipados-iphone-duo.md` | iPadOS + iPhone Duo poses, reserved regions, vertical controls — HIG |
| `references/watch-tv-vision.md` | watchOS, tvOS, visionOS basics — HIG |
| `references/mockup.md` | Device-frame HTML/CSS technique (safe areas, viewport-fit) |
| `references/handoff-swiftui.md` | SwiftUI-ready handoff spec format |
