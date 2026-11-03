---
name: ios-sync
description: Regenerate the iOS debug bridge against the latest upstream gstack templates. (gstack)
category: mobile
sources:
- repository: gstack
  original_path: ios-sync/SKILL.md
  sha256: b4d371fcb028b1f6bec3c37c22a07c0fb0c4604e927a9ee2ffd364ff718f81b6
principles:
- core/think-before-coding
- core/simplicity-first
- core/surgical-changes
- core/goal-driven-execution
---

> **Library use:** Apply the [compatibility and execution contract](../../COMPATIBILITY.md). Source roles, memory claims, command names, hooks, and integrations are instructions or prerequisites—not installed capabilities.

## When to invoke this skill

Updates StateServer.swift, DebugOverlay.swift, Package.swift,
and the typed @Observable state accessors. Use after you upgrade gstack
or add new ViewModels/properties that need accessor coverage.
Use when asked to "resync the iOS debug bridge", "regenerate iOS
accessors", or "update the gstack iOS instrumentation".

Voice triggers (speech-to-text aliases): "resync the iOS debug bridge", "regenerate iOS accessors", "update the gstack iOS instrumentation".

# Resync the iOS debug bridge

After `/ios-qa` is installed in an app, the user may:

1. Add new `@Observable` classes or properties that need accessor coverage.
2. Upgrade gstack to a newer version with hardening fixes.
3. Move the `// @Snapshotable` generator marker comment to a different field.

This skill regenerates the relevant artifacts in place.

**Templates live in upstream gstack.** The installed
`gstack-ios-qa-regen` launcher resolves its own gstack root and copies only
the supported bridge files from `ios-qa/templates/`. The fork's HTTP-fetch
and wildcard-copy patterns are gone.

## Phase 1: Detect installed version

1. Read `<app>/DebugBridgeGenerated/.gstack-version` (written by /ios-qa
   during install). If missing, treat the install as "unknown old version".
2. Read upstream version from `$GSTACK_ROOT/VERSION`.
3. If versions match AND no new `@Observable` classes were added, exit
   early with "already up to date".

## Phase 2: Regenerate codegen output

Run the deterministic regenerator once. `--app-source` is the directory the
accessor scanner should inspect; `--bridge-dir` is the local Swift package
that the app links in Debug builds:

```bash
~/.claude/skills/gstack/bin/gstack-ios-qa-regen \
  --app-source "$APP_SOURCE_DIR" \
  --bridge-dir "$APP_SOURCE_DIR/DebugBridge"
```

The command removes only the known obsolete generated files from the former
flat `DebugBridgeGenerated/` layout before emitting the current accessor.
Generation accepts file-scope observable classes and JSON-native scalar,
array, String-keyed dictionary, and Optional field types. It rejects custom
types, implicitly unwrapped Optionals, nested observable classes, and duplicate
snapshot keys before writing a completion marker.

The composite-hash cache key handles whether anything actually needs
regenerating; if Swift version, generator git rev, lockfile, source content,
and platform triple all match the cache, this is a ~50ms no-op.

## Phase 3: Review the generated diff

1. Review changes under `<app>/DebugBridge/` and
   `<app>/DebugBridgeGenerated/StateAccessor.swift`.
2. Confirm the command did not modify the app's handwritten Swift files.
3. Keep app-specific wiring in the app target; canonical bridge package files
   are regenerated from upstream and should not be hand-edited.

## Phase 4: Verify

1. `swift build` succeeds against the app's package.
2. `xcodebuild -scheme <SchemeName>` succeeds.
3. Re-launch the app on the device; daemon connects + rotates token.
4. `GET /state/snapshot` returns the new accessor schema hash.

## Failure modes

| Symptom | Action |
|---|---|
| Swift compile fails after regen | Revert via `git restore` + AskUserQuestion: surface the compile error |
| Codegen reports an invalid marked declaration | Use a file-scope observable class and a writable instance `var` with an explicit JSON-native type, internal/public setter, and a key unique across models; otherwise remove the `// @Snapshotable` marker. |
| Schema hash unchanged after adding new @Observable | No field has the standalone `// @Snapshotable` marker comment — codegen excludes unmarked state correctly. Add the comment immediately above each field that should be snapshotted. |
| Scanner sees generated bridge sources | Pass the narrow app source directory; the regenerator automatically excludes `DebugBridgeGenerated` and `StateAccessor.swift`. |

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

- `gstack/ios-sync/SKILL.md`
