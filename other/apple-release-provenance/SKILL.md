---
name: apple-release-provenance
description: Audit source-to-installed provenance for Apple app releases. Use when proving a shipped build, signing state, or artifact chain; not for feature work.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# Apple Release Provenance

Prove the requested chain without collapsing distinct transformations:

`source -> archive -> export -> published -> downloaded -> installed -> running`

## Invariants

- Record exact source, dirty/generated inputs, dependencies, toolchain, CI/build identity, channel, and each artifact boundary. Filenames, versions, branches, valid signatures, or notarization alone do not prove a source revision.
- Inspect effective signing, entitlements, profiles, nested code, and notarization at the stages where they are observable. Apple re-signs App Store products; submitted and delivered signatures or bundle bytes need not match.
- Bind runtime evidence to the strongest observable build identity. On macOS, inspect the exact installed executable. Restricted platforms may expose only App Store Connect, app-reported, receipt, or diagnostic identifiers; mark inaccessible delivered-code claims `unproven`.
- Treat TCC state as a separate runtime observation. Never transfer permission conclusions between builds or reset permissions just to simplify diagnosis.
- Treat Sparkle archive, appcast, download, installed replacement, and relaunched executable as separate boundaries. Its signature proves neither source revision nor Apple signing state.

## Route

1. Freeze the precise claim and distribution channel.
2. Read [references/evidence-ledger.md](references/evidence-ledger.md) to collect source, artifact, signing, installed, and runtime evidence and classify every transition.
3. Read [references/distribution-channels.md](references/distribution-channels.md) for App Store/TestFlight, Developer ID, Development, Ad Hoc, or Sparkle checks.
4. Read [references/apple-documentation.md](references/apple-documentation.md) before changing Apple signing, entitlement, notarization, or distribution guidance.

Do not upload, notarize, publish, install, update, replace an app, or reset permissions without authorization. Report the strongest supported claim, the first contradicted or missing boundary, and the smallest next observation. A claim-critical `unproven` boundary prevents a “verified” conclusion.

## Review

- Last updated: **2026-08-30**
- Last reviewed: **2026-08-30**
- Apple documentation reviewed: **2026-08-30**
- Release signing, entitlement, notarization, and distribution guidance was reviewed with Xcode MCP `DocumentationSearch`; see [Apple documentation evidence](references/apple-documentation.md).
