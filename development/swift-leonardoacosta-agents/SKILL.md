---
name: swift
description: Swift project layout, XcodeGen, xcodebuild, testing, code signing, and device deployment conventions for native iOS, macOS, and watchOS applications.
metadata:
  category: Framework
  level: library
  engineer: ui-engineer
  gate: xcodegen generate && xcodebuild test CODE_SIGNING_ALLOWED=NO
  audit-rubric:
    - XcodeGen regenerates the project without unexplained output drift.
    - The selected scheme builds and its focused tests pass without code signing.
    - Signed remote builds use an explicitly configured GUI-session bridge.
allowed-tools: Read, Glob, Grep, Bash
---

# Swift

Use this skill for native Apple-platform work involving Swift, SwiftUI, XcodeGen,
`xcodebuild`, code signing, or device deployment. Repository instructions own the concrete
project path, schemes, destinations, signing team, and deployment host.

## XcodeGen projects

Treat `project.yml` as the source of truth. Do not hand-edit `project.pbxproj` in a generated
project.

```yaml
targets:
  ExampleApp:
    type: application
    platform: iOS
    sources:
      - path: ExampleApp/Sources
```

- Add source files below the configured source glob, then run `xcodegen generate`.
- Review and commit generated project changes when the repository tracks them.
- Treat changes outside documented generated paths as unexpected drift.
- Keep shared modules independent from application-only types so they remain easy to test.

## Verification

Run the repository's own scheme and destination when they are declared:

```bash
xcodegen generate
xcodebuild -scheme "$SCHEME" -destination "$DESTINATION" test CODE_SIGNING_ALLOWED=NO
```

For a self-contained file on a remote macOS builder, copy it to a temporary directory and use
the target SDK's compiler for a fast type-check. This is a focused preflight, not a replacement
for building the generated project and running its tests.

Validate plist and entitlement files with `plutil -lint` before a signed build.

## Signing and capabilities

- Store the development-team identifier and signing configuration in repository-local build
  settings or an ignored `.xcconfig`; do not bake personal account data into reusable guidance.
- Prefer automatic signing only when the repository has explicitly opted into it.
- Add capabilities through the target's entitlements and required usage-description keys, then
  regenerate the project before building.
- Keep App Store Connect credentials in an approved secret store. Never commit private keys or
  pass secret material through logs.

## Remote signed builds

Code signing can depend on the interactive macOS security session. A background SSH session may
therefore fail even when the login keychain is unlocked. If a repository supports remote signed
builds, use its documented GUI-session LaunchAgent bridge and marker protocol.

Load [references/codesign-bridge.md](references/codesign-bridge.md) before designing or debugging
that bridge. The repository must supply its own labels, paths, schemes, team settings, and device
selection.

## Never

- Never hand-edit a generated `project.pbxproj`.
- Never treat a focused `swiftc -typecheck` as the full project gate.
- Never assume code-signing identities work in a background SSH security session.
- Never publish signing-team identifiers, device identifiers, account names, host aliases, or
  private-key paths in a portable skill.
