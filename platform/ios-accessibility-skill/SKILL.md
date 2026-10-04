---
name: iOS Accessibility Skill
description: Use when iOS or iPadOS accessibility design, implementation, review, or testing involves VoiceOver, Voice Control, Switch Control, Full Keyboard Access, Dynamic Type, contrast, motion, focus, media alternatives, or Assistive Access. Do not use for generic visual styling or platform-neutral UI work with no accessibility requirement.
---

# iOS Accessibility Skill

Treat accessibility as part of the product contract, not a modifier pass at the end. Preserve the semantics of native controls, support user settings, and verify behavior with the actual assistive technologies in scope.

## Baseline and availability

Core guidance applies broadly. Copy-ready examples use Xcode 15, Swift 5.9, and iOS/iPadOS 17.

- Assistive Access exists as a system experience on iOS/iPadOS 17.
- `accessibilityAssistiveAccessEnabled` is available from iOS/iPadOS 18.
- The SwiftUI `AssistiveAccess` scene and `assistiveAccessNavigationIcon` are stable Xcode 26 APIs requiring iOS/iPadOS 26.
- OS 27-cycle material is beta relative to stable Xcode 26.6. Include it only on explicit request, label it beta, and gate it.

Always check the user's deployment target before emitting newer API code.

## Audit order

1. Identify essential tasks, content, and destructive actions.
2. Inspect the accessibility tree: roles, labels, values, hints, ordering, grouping, and hidden decoration.
3. Exercise VoiceOver, Voice Control, Switch Control, and Full Keyboard Access as relevant.
4. Test every Dynamic Type size, including accessibility categories.
5. Test Increase Contrast, Reduce Motion, Reduce Transparency, Differentiate Without Color, Bold Text, and button shapes.
6. Verify localization, right-to-left layouts, captions/transcripts, and audio descriptions where applicable.
7. Run Accessibility Inspector, then test on device and with disabled users when possible.

Automated checks can find omissions; they cannot prove that reading order, wording, focus, and task flow are usable.

## Semantics

- Prefer semantic controls such as `Button`, `Toggle`, `TextField`, `Slider`, and `Link` over tap gestures on generic views.
- Labels identify an element or action concisely. Values communicate current state. Hints describe the result when that result is not obvious.
- Do not put gestures in hints: avoid “Tap,” “Double-tap,” or “Swipe.” VoiceOver already teaches interaction mechanics.
- Do not repeat the control type in its label; the accessibility trait supplies it.
- Hide purely decorative images. For icon-only buttons, label the button rather than exposing the image separately.
- Add custom actions or rotors when they shorten a real workflow; retain an ordinary visible path to the action.

See [the complete favorite-button example](examples/example_voiceover.swift). A hint such as “Adds this item to Favorites” describes the result; omit it when the label already makes that result clear.

## Grouping and focus

- Use `.combine` for static fragments that should form one announcement, such as a title plus subtitle.
- Use `.contain` to create a navigable group while preserving its interactive children.
- Never combine multiple text fields, buttons, or other independently actionable controls into one accessibility element.
- Keep focus order aligned with visual and task order. Restore focus deliberately after modal transitions or major content replacement.
- Prefer state-driven updates. Post announcements only when important information would otherwise be missed; avoid interrupting speech for routine changes.

```swift
import SwiftUI

struct ContactForm: View {
    @State private var name = ""
    @State private var phone = ""

    var body: some View {
        VStack(alignment: .leading) {
            Text("Contact information")
                .font(.headline)
                .accessibilityAddTraits(.isHeader)
            TextField("Name", text: $name)
            TextField("Phone", text: $phone)
        }
        .accessibilityElement(children: .contain)
    }
}
```

Each field remains independently editable and focusable.

## Dynamic Type

- Prefer semantic fonts such as `.body`, `.headline`, and `.title`.
- For a custom face, use `Font.custom(_:size:relativeTo:)` in SwiftUI or `UIFontMetrics` in UIKit.
- Let user content wrap. Avoid fixed heights, single-line limits, and `minimumScaleFactor` as substitutes for layout that supports large text.
- Use `@ScaledMetric(relativeTo:)` for icons, spacing, or custom controls that should grow with a text style.
- At accessibility sizes, switch layout when needed—for example, place trailing actions below labels instead of squeezing them horizontally.

See [the Dynamic Type example](examples/example_dynamic_type.swift).

## Motor and input accessibility

- Prefer the platform's standard control sizes. On iOS/iPadOS, aim for the default 44-by-44-point target. If a compact design uses the documented 28-by-28-point minimum, provide sufficient spacing and verify it with real input.
- Do not require precision, simultaneous gestures, long holds, or motion when a simpler alternative can perform the same task.
- Give Voice Control users unique, visible names and avoid duplicate control labels.
- Ensure Switch Control scanning reaches every task and that custom controls expose adjustable or custom actions.
- Support keyboard focus, activation, dismissal, and visible focus indication on iPad when Full Keyboard Access is relevant.

## Visual, motion, and media access

- Never encode status using color alone; pair it with text, shape, or an icon.
- Check contrast in every state and appearance, including disabled and selected states.
- Honor `accessibilityReduceMotion`, `accessibilityReduceTransparency`, `accessibilityDifferentiateWithoutColor`, and `colorSchemeContrast`.
- Replace large motion or parallax with a meaningful low-motion transition; do not merely shorten a hazardous animation.
- Caption speech and meaningful sounds in video, provide transcripts for audio, and add audio descriptions when visuals carry essential information.
- Localize accessibility strings in context. Keep private values out of labels, announcements, logs, and screenshots.

## Cognitive accessibility and Assistive Access

- Keep pathways short, labels literal, decisions limited, and destructive operations recoverable.
- Pair symbols with clear text and keep navigation consistent.
- For iOS 26+, consider a dedicated `AssistiveAccess` scene only when the app benefits from a distilled experience. Add the required Info.plist support and test the entire scene on device.
- On iOS 18+, `accessibilityAssistiveAccessEnabled` can adapt an existing view, but it is not a substitute for designing the simplified flow.

## Copy-ready examples

- [Semantic VoiceOver button](examples/example_voiceover.swift)
- [Dynamic Type layout](examples/example_dynamic_type.swift)
- [Accessibility review prompts](examples/prompts.md)

Every recommendation must state relevant availability and include a fallback when the deployment target predates the API.
