---
name: iOS Animation Graphics Skill
description: Design, implement, debug, and review accessible Apple-platform animation and graphics with SwiftUI animation, Canvas, TimelineView, matched geometry, phase/keyframe animators, Core Animation, and Lottie. Use for motion design, custom drawing, transitions, particles, animated symbols, UIKit/AppKit bridging, Reduce Motion, and animation performance. Prefer native SwiftUI for app UI; use Core Animation or Lottie only when their capabilities are needed. Do not use this skill for SpriteKit/Metal game engines, video rendering, or image editing unless animation integration is the specific task.
---

# Apple UI Animation and Graphics

Choose the simplest rendering system that expresses the motion, then make accessibility and lifecycle behavior part of the design rather than a later patch.

## Compatibility baseline

- `Canvas` and `TimelineView` require iOS 15, macOS 12, tvOS 15, or watchOS 8.
- `matchedGeometryEffect` requires iOS 14 / macOS 11.
- `PhaseAnimator`, `KeyframeAnimator`, and the first symbol-effect APIs require iOS 17 / macOS 14.
- Zoom navigation transitions and SwiftUI animation bridging into UIKit/AppKit require iOS 18 / macOS 15 where documented.
- Lottie’s native SwiftUI `LottieView` was introduced in Lottie 4.3. Pin a tested package version and obey that release’s Xcode, Swift, and deployment requirements; Lottie 4.6 requires Xcode 16 / Swift 6.
- Gate newer APIs with `#available` and provide a meaningful lower-target result. Treat 27-cycle APIs as unavailable unless the project actually builds with that SDK.

State the exact minimum that the proposed implementation needs; do not assign one minimum to every animation technique.

## Select the rendering path

| Need | Preferred tool |
| --- | --- |
| Animate SwiftUI state, layout, or transitions | `withAnimation`, value-scoped `.animation`, `transition` |
| Several discrete or timed phases | `PhaseAnimator` / `KeyframeAnimator` on iOS 17+ |
| Draw many lightweight vector elements | `Canvas` |
| Redraw continuously from elapsed time | `TimelineView(.animation)` around `Canvas` |
| Synchronize two SwiftUI layouts | `matchedGeometryEffect` |
| Animate an SF Symbol | `symbolEffect` where available |
| Control a layer tree or UIKit view | Core Animation / `UIViewRepresentable` |
| Play designer-authored JSON or `.lottie` assets | Lottie |

Do not drive a `Canvas` by changing a captured scalar with `withAnimation`; a renderer closure is not itself animatable data. Derive each frame from a `TimelineView` date or expose explicit animatable values in a custom view.

## Workflow

1. Declare the before/after states and what event starts or stops motion.
2. Check the project’s deployment targets and third-party dependency version.
3. Define Reduce Motion behavior: static end state, dissolve, shortened travel, or no autoplay.
4. Pick the rendering path from the table above.
5. Keep animation state as the source of truth; avoid imperative controls that drift from SwiftUI state.
6. Test interruption, repeated taps, navigation, background/foreground, resizing, and device rotation.
7. Profile representative hardware with SwiftUI, Core Animation, and Time Profiler instruments when frames drop.

## SwiftUI rules

- Scope implicit animations with `.animation(_:value:)`.
- Use `withAnimation` for an explicit state mutation.
- Prefer opacity, scale, rotation, and offset for hot paths; animating frame constraints can trigger repeated layout.
- Keep stable identity across transitions. Do not use changing random IDs to force animation.
- Let interactive gestures update state continuously and choose a spring only when the gesture ends.
- Use animation completion APIs only at their documented availability; do not infer completion from a fixed sleep.

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion
@State private var isExpanded = false

Button("Details") {
    withAnimation(reduceMotion ? nil : .snappy) {
        isExpanded.toggle()
    }
}
.scaleEffect(isExpanded ? 1.08 : 1)
.opacity(isExpanded ? 1 : 0.85)
```

For multi-stage motion on iOS 17+, prefer phase or keyframe animators over chains of delayed tasks. Provide a simple state change for earlier targets.

## Canvas and continuous drawing

`Canvas` redraws when its surrounding view invalidates. For time-based graphics, wrap it in `TimelineView(.animation(paused:))` and derive phase from `context.date`. Pause the schedule for Reduce Motion and when the animation is not visible or active.

Read [examples/example_canvas_waveform.swift](examples/example_canvas_waveform.swift) for a complete iOS 15+ waveform. It uses time as the source of truth, has no accumulating phase drift, and renders a static frame for Reduce Motion.

Control work per frame:

- Step vector paths at the coarsest visually acceptable interval.
- Cache expensive geometry or resolved symbols when inputs are unchanged.
- Avoid allocating images, formatters, or large collections inside the renderer.
- Respect `TimelineView` cadence and pause offscreen work.

## Core Animation bridging

Layer geometry is invalid in `makeUIView` when the host view still has zero bounds. Put layer sizing and mask paths in a `UIView` subclass’s `layoutSubviews`; disable implicit actions for those layout updates. Make playback updates idempotent and never force-unwrap a stored animation.

Read [examples/example_gradient_border.swift](examples/example_gradient_border.swift) for a layout-safe, Reduce-Motion-aware border. Use the same pattern for emitter layers: update `frame` and `emitterPosition` from current bounds, set `birthRate` to zero when paused/reduced/offscreen, and remove animations during teardown.

## Lottie

Use Lottie’s native SwiftUI `LottieView` on Lottie 4.3+; do not create local types named `LottieView` or `LottieAnimationView`. Those names collide with library types and can make state declarations recursively refer to the wrong type.

Keep playback declarative with `LottiePlaybackMode`. For Reduce Motion, show a meaningful static progress frame or an asset-authored reduced-motion marker rather than autoplaying. Verify the animation asset exists in the intended bundle and test VoiceOver focus while it plays.

Read [examples/example_lottie_animation.swift](examples/example_lottie_animation.swift) after adding a compatible Lottie package. The example intentionally has an external dependency and is not part of dependency-free compiler validation.

## Accessibility

- Read `accessibilityReduceMotion` in every view that autoplays, loops, travels, parallax-scrolls, or emits particles.
- Preserve meaning when motion is removed; do not simply hide success/error state.
- Avoid rapid flashing and large involuntary motion.
- Do not make animation the only signal. Pair it with text, shape, sound, or haptics as appropriate.
- Keep controls operable while animation is interrupted or disabled.
- Decorative drawing should be accessibility-hidden; meaningful charts need labels or an accessible representation.

## Performance and correctness review

- Does the animation have one authoritative state and a deterministic stop condition?
- Does continuous work stop offscreen, in the background, and under Reduce Motion?
- Are Core Animation layer frames recalculated after nonzero layout and rotation?
- Are repeated SwiftUI updates idempotent rather than restarting the same CA animation?
- Does a Lottie view use the package’s types without name shadowing?
- Are availability and package-version requirements explicit?
- Has the effect been tested on a physical low-end supported device?
- Are render cost, layout passes, overdraw, and memory measured rather than guessed?

## Supporting material

- [README.md](README.md) summarizes minimums and resource selection.
- [examples/example_canvas_waveform.swift](examples/example_canvas_waveform.swift) demonstrates scheduled Canvas redraw.
- [examples/example_gradient_border.swift](examples/example_gradient_border.swift) demonstrates layout-safe Core Animation bridging.
- [examples/example_lottie_animation.swift](examples/example_lottie_animation.swift) demonstrates non-shadowing declarative Lottie playback.
- [examples/prompts.md](examples/prompts.md) contains representative activation prompts.
