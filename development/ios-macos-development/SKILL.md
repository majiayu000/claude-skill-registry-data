---
name: ios-macos-development
description: Build, debug, or release iOS and macOS apps with Swift and Apple platform tools.
---

# iOS and macOS Development

Preserve the project's UI framework, deployment targets, and architecture unless the task requires a change.
Use API availability checks only when supported deployment targets require them.
Do not re-sign an app or change its bundle ID as a debug fix without explicit approval.
A local build request does not authorize distribution, submission, or account changes.

## Task references

Read the guide that resolves the current task.
Do not load a stack of guides for an ordinary edit.

For Apple API guidance, read the relevant [Xcode reference](../programming/references/apple/guide.md) first.
The guides below provide supplementary examples and local tool workflows.

| Task | Guide |
| --- | --- |
| SwiftUI API or state design | [SwiftUI](swift-ui/guide.md) |
| Navigation, sheets, forms, or component examples | [UI patterns](swiftui-ui-patterns/guide.md) |
| Actor isolation or `Sendable` diagnostics | [Swift concurrency](swift-concurrency-expert/guide.md) |
| Liquid Glass adoption | [Liquid Glass](swiftui-liquid-glass/guide.md) |
| View structure or ownership refactor | [View refactor](swiftui-view-refactor/guide.md) |
| SwiftUI performance symptoms | [Performance audit](swiftui-performance-audit/guide.md) |
| Trace capture or analysis | [Native performance](native-app-performance/guide.md) or [Instruments](instruments-profiling/guide.md) |
| App Intents, entities, or Shortcuts | [App Intents](ios-app-intents/guide.md) |
| Live simulator inspection | [Simulator debugger](ios-debugger-agent/guide.md) |
| Repeatable simulator automation | [Simulator scripts](ios-simulator/guide.md) |
| Archives, certificates, TestFlight, App Store, or notarization | [Distribution](app-store-connect-cli/guide.md) |

Use available tools and repository commands.
If a referenced tool is absent, use an available equivalent and state the limitation.
Report the actual build, runtime, or distribution result that the user requested.
