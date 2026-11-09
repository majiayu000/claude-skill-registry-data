---
name: standards
description: Index of official Apple/Swift/Xcode docs, Apple sample apps (Landmarks, Backyard Birds, Food Truck) and iOS house patterns (state, UI events).
user-invocable: false
---

# iOS standards reference

Use this to pick the authoritative source for a question. For a standard, quote its anchor in
`references/source-anchors.md` instead of fetching the page. Look up deadlines, deprecations, App Store
requirements and versions with WebFetch when you use them, because they change between anchor checks. Do not
answer those from memory.

| Question | Read |
|---|---|
| State ownership, @Observable vs ObservableObject, environment | `references/official-docs.md` §SwiftUI, then `references/apple-samples.md` |
| One-shot model → UI events (navigation, alerts, toasts) | `references/ui-events.md` (house pattern and how it differs from the Android rule) |
| Too many closures on a view | `references/ui-events.md` §Actions struct |
| Design system, tokens, component API, previews | `references/apple-samples.md` |
| Concurrency, @MainActor, Swift 6 language mode | `references/official-docs.md` §Swift |
| Testing (Swift Testing vs XCTest), accessibility | `references/official-docs.md` §Testing, §Accessibility |
| Xcode, SwiftPM, CocoaPods, App Store submission gates | `references/official-docs.md` §Build |
| Security controls, Keychain, ATS, privacy manifests | `references/official-docs.md` §Security |
| Starting a per-repo `CLAUDE.md` | `references/project-claude-md-template.md` |
| MCP servers, community skills, lint hooks, xcresulttool | `references/official-docs.md` §Community tooling |

Guardrails when applying any reference to this repo:
- Target repos are often hybrid legacy apps (UIKit + SwiftUI, CocoaPods + SwiftPM). Recommend the blueprint pattern for new
  code. Do not propose rewriting working UIKit screens unless the ticket is a migration.
- Apple publishes no architecture doctrine. Sample apps show `@Observable` models injected through the environment, model
  code in separate Swift packages and navigation as data. Treat that as consensus, not a rule. MV vs MVVM, a domain layer
  and a view model per view are choices. Grade consistency with the codebase, not the choice.
- A reference may need a newer deployment target or Xcode than the repo (`@Observable` iOS 17+, Swift Testing Xcode 16+,
  Liquid Glass iOS 26+). State the version the source targets and the repo's gap.
