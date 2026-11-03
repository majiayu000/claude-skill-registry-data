---
name: ios-clean
description: 'Remove the DebugBridge SPM package and all #if DEBUG wiring from an iOS app. (gstack)'
category: mobile
sources:
- repository: gstack
  original_path: ios-clean/SKILL.md
  sha256: 2111cef7d268d546d57f1c5b3c63a0bf42059471d583f23b438bf5371c348f00
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

## When to invoke this skill

Cleans up StateServer, DebugOverlay, accessor codegen output, and
app-side hooks installed by /ios-qa. This is a convenience wrapper —
the structural Release-build guard (Package.swift conditional + CI
swift build -c release check) is the safety-critical path.
Use when asked to "clean the iOS debug bridge", "remove DebugBridge",
or "strip the gstack iOS instrumentation".

Voice triggers (speech-to-text aliases): "clean the iOS debug bridge", "remove DebugBridge", "strip the gstack iOS instrumentation".

# Strip the DebugBridge from an iOS app

This skill is a **convenience flow**, not a safety mechanism. The structural
guard against shipping DebugBridge in Release is in `Package.swift.template`
(`.when(configuration: .debug)`) plus the CI invariant test that runs
`swift build -c release` and asserts the DebugBridge symbol is absent. Both
ship as part of `/ios-qa`'s template installation.

This skill exists for developers who:

- Manually copied DebugBridge files (without using `/ios-qa`'s SPM install).
- Want a guided, reversible removal flow before a security audit.
- Are migrating away from gstack and want a clean exit.

## What it removes

Each item is reverted only after AskUserQuestion confirmation:

1. The `DebugBridge` SPM target from `Package.swift`.
2. The `#if DEBUG` block in the app's `@main` entry that calls
   `DebugBridgeManager.shared.start()`.
3. Any standalone `// @Snapshotable` generator marker comments on the
   canonical app state class.
4. Generated `StateAccessor.swift` files anywhere under the app source.
5. The `gstack-ios-qa.token` file under `NSTemporaryDirectory()` on the
   device (best-effort — only works if device is connected when /ios-clean
   runs).

## What it does NOT touch

- App business logic, view models, view code.
- Anything outside `#if DEBUG` blocks.
- Other test or QA infrastructure.

## Phase 1: Inventory

1. Glob for `import DebugBridge` across the app source.
2. Glob for `#if DEBUG ... DebugBridgeManager` blocks.
3. Glob for `// Auto-generated state accessor` headers in
   `StateAccessor.swift` files.
4. Parse `Package.swift` for the DebugBridge dependency entry.
5. Show the user what's about to be removed (file list + line counts).
   AskUserQuestion: proceed, dry-run, or abort.

## Phase 2: Remove

For each item the user approved:

1. Use Edit tool to strip the import + the `#if DEBUG` block (keep the
   surrounding code intact).
2. Use Edit tool to remove the `.package(url:...DebugBridge...)` entry
   from `Package.swift` and any `targets` referencing `"DebugBridge"`.
3. Delete generated `StateAccessor.swift` files.
4. Run `xcodebuild -scheme <SchemeName> -destination 'platform=iOS,id=<UDID>'
   build install -configuration Release` to verify Release builds without
   the bridge. If it fails on a missing DebugBridge symbol, the removal
   was incomplete — STOP and report.

## Phase 3: Verify

1. `! grep -r "DebugBridge" <app-source-dir>` (no matches).
2. `! grep -r "@Snapshotable" <app-source-dir>` (no matches).
3. `swift build -c release` succeeds.
4. `nm -j` on the built binary doesn't show DebugBridge symbols.

Report the cleanup result + a one-line summary of what got removed.

## Reversibility

Every Edit + delete is a git operation; the user can `git restore` to undo.
This skill never force-pushes, never amends, never deletes the SPM cache —
those are user choices.

## Runtime prerequisites

See [the dependency ledger](../../DEPENDENCIES.md) and this skill’s records in [dependencies.json](../../dependencies.json). Native gstack/ECC CLIs, browsers, hooks, model tools, credentials, and memory stores must be available before invoking their steps. No runtime installation or execution has been performed. CSO requires its trusted helper; do not emulate that helper on the host.

## Related skills and principles

- [core/goal-driven-execution](../../core/goal-driven-execution/SKILL.md)
- [core/gstack-operating-protocol](../../core/gstack-operating-protocol/SKILL.md)
- [core/simplicity-first](../../core/simplicity-first/SKILL.md)
- [core/surgical-changes](../../core/surgical-changes/SKILL.md)
- [core/think-before-coding](../../core/think-before-coding/SKILL.md)
- [developer-experience/plan-tune](../../developer-experience/plan-tune/SKILL.md)
- [documentation/document-generate](../../documentation/document-generate/SKILL.md)
- [engineering/codex](../../engineering/codex/SKILL.md)
- [engineering/review](../../engineering/review/SKILL.md)
- [memory/context-restore](../../memory/context-restore/SKILL.md)
- [memory/context-save](../../memory/context-save/SKILL.md)
- [memory/learn](../../memory/learn/SKILL.md)
- [mobile/ios-qa](../ios-qa/SKILL.md)
- [project-management/retro](../../project-management/retro/SKILL.md)
- [release/ship](../../release/ship/SKILL.md)
- [testing/qa-only](../../testing/qa-only/SKILL.md)

## Source provenance

- `gstack/ios-clean/SKILL.md`
