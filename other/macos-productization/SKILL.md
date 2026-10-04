---
name: macos-productization
description: "Prepare or inspect a macOS distribution artifact. Use for Developer ID or Mac App Store signing, hardened runtime, notarization, packaging, Gatekeeper, installation, and update integrity."
---

# macOS productization and distribution

## Inputs

Identify the authorized stage, distribution channel, candidate source/version, bundle and nested code, signing/entitlement requirements, packaging pipeline, update channel, and available artifact evidence.

## Rules

- **MAC-001 — Choose the channel.** Development, internal, direct distribution, and Mac App Store have different signing, sandbox, packaging, and review requirements.
- **MAC-002 — Inspect the artifact.** Project settings are intent; the signed app, package, receipts, and installed copy establish distribution facts.
- **MAC-003 — Preserve the trust chain.** Verify nested code and entitlements deliberately. Do not use blanket re-signing to hide an unexplained signing failure.
- **MAC-004 — Separate trust gates.** Signing, notarization acceptance, stapling, Gatekeeper assessment, installation, and launch are distinct checks.
- **MAC-005 — Respect release authority.** Private credentials, notarization/upload, installation, publication, deletion, and system-wide changes require the corresponding authorization.

## Workflow

1. Map channel requirements and inspect the exact bundle/packaging pipeline.
2. Fix the source owner of signing, entitlements, resources, or identity problems.
3. Build/export and inspect the authorized candidate and nested components.
4. Run applicable trust and installed-artifact checks without broad destructive workarounds.
5. Bind release notes, version, hashes, receipts, and update metadata to the same artifact.

## Verify

Verify distribution identity, embedded entitlements, nested code, hardened runtime/sandbox as applicable, notarization status, stapled ticket, Gatekeeper behavior, installed launch, icons, and update authenticity for the chosen channel.

## Output

Report the exact artifact and channel, checks performed, external actions taken, and remaining trust/install/release gates. Do not claim “notarized” or “Gatekeeper-clean” from a local build alone.

## References

Read the [playbook](references/macos-productization-patterns.md) for decisions, failure cases, and source links.

For reproducible distribution and installed-artifact proof, read the [focused reference](references/distribution-reproducibility.md).
