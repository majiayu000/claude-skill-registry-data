---
name: apple-swiftui-native-apps
description: "Build, review, or repair a SwiftUI feature. Start here for native UI semantics, task scoping, SDK verification, and selecting focused Apple-platform skills."
---

# SwiftUI engineering entry point

## Inputs

Read the current source and repository instructions. Record the requested outcome, edit authority, affected targets, deployment minimums, Swift language mode, and available tools. Ask only for a missing decision that blocks safe progress; otherwise state a reversible assumption.

## Rules

- **UI-001 — Semantics before decoration.** Use native controls for actions, choices, and navigation. Custom appearance is allowed; it must preserve interaction, accessibility, and platform behavior.
- **UI-002 — Evidence before modernization.** Check the exact SDK declaration, platform availability, compiler mode, and current Apple guidance. A newer SDK does not raise deployment minimums automatically.
- **UI-003 — Own the truth once.** Identify the owner of mutable state, persistent data, navigation, and side effects before splitting views.
- **UI-004 — Scope the change.** Preserve user edits and working behavior. A review does not authorize edits; preparation does not authorize release, deletion, or account changes.
- **UI-005 — Make uncertainty visible.** Separate documented facts, repository conventions, design recommendations, and untested hypotheses. Never manufacture build, screenshot, device, or benchmark evidence.

## Workflow

1. Trace the affected action from visible control through state, service, storage, and any system projection.
2. Load only relevant specialist skills: state, concurrency, navigation, layout, controls, accessibility, design, persistence, networking, testing, platforms, interop, system experiences, privacy, project governance, performance, device validation, or release.
3. Define the smallest complete behavior, including loading, empty, error, denied, cancelled, and restored states that actually apply.
4. Implement or recommend a coherent change. Prefer existing conventions unless a concrete defect justifies changing them.
5. Verify the claim at the required level and review the final diff.

## Verify

Use source inspection for structure, builds for compilation, tests for behavior, rendered UI for layout, and devices for hardware-dependent claims. Check accessibility, localization, and lifecycle risks in the edited scope.

## Output

Return the change or finding, exact files/symbols, rationale, verification performed, and remaining risks. For reviews: severity, reproduction, impact, correction, and regression test. Avoid a checklist dump for a small fix.

## References

Read the [playbook](references/correction-patterns.md) for decisions, failure cases, and source links.

For review and modernization decisions, read the [focused reference](references/review-and-modernization.md).
