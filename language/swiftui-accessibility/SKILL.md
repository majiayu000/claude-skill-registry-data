---
name: swiftui-accessibility
description: "Audit or implement VoiceOver, Dynamic Type, accessible controls, contrast, Reduce Motion, keyboard access, localization, and right-to-left SwiftUI behavior."
---

# Accessibility and localization

## Inputs

Identify the core user journeys, supported platforms/input methods, content meaning, largest supported text sizes, languages, and current accessibility settings.

## Rules

- **AX-001 — Preserve meaning and operability.** Every essential action and value needs an accessible representation, not merely a visible label.
- **AX-002 — Adapt to people.** Support larger text, contrast preferences, reduced motion, alternative input, and layout direction without removing core functionality.
- **AX-003 — Do not encode meaning only visually.** Provide alternatives to color, position, sound, motion, and gesture-only instructions.
- **AX-004 — Group intentionally.** Combine related static content, but do not hide independent controls inside an inaccessible combined element. Keep focus order meaningful.
- **AX-005 — Verify journeys.** Automated audits and labels alone do not prove accessibility. Test reading, editing, acting, error recovery, and dismissal.

## Workflow

1. Inspect the accessibility tree and complete the core journey with an assistive technology.
2. Correct semantics before adding hints or traits indiscriminately.
3. Reflow at accessibility text sizes and verify nonvisual state changes.
4. Localize user-facing strings, pluralization, formatting, and directional layout.
5. Record defects with affected users, reproduction, and validation evidence.

## Verify

Check VoiceOver reading and actions, Full Keyboard Access where relevant, contrast, Reduce Motion, Reduce Transparency, large text, mixed-direction content, longer translations, and error recovery. Use automated audits as an additional signal.

## Output

Return prioritized barriers, exact controls, corrections, and tested settings/journeys. Do not claim universal accessibility or store-label eligibility from a source scan.

## References

Read the [playbook](references/accessibility-patterns.md) for decisions, failure cases, and source links.

For assistive journeys and localized content, read the [focused reference](references/assistive-and-localized-flows.md).
