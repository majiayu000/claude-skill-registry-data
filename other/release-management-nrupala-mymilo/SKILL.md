---
name: release-management
description: Ship releases safely — semver, changelogs, signed tags, rollout and rollback plans, sealed release provenance.
version: 1
triggers: release, semver, changelog, ship it, rollback, release process, versioning
category: Engineering & code
blurb: Ship releases safely — semver, changelogs, signed tags, rollout and rollback plans.
archetype: knowledge
example: Run this release with a proper changelog and rollback plan.
---

# Release Management — the release seat

Releases are events, not accidents: versioned, documented, sealed, and reversible.

## When to use
- Cutting any release, hotfix, or version bump.
- Preparing user-facing release notes.
- Post-release verification.

## Method
1. **Semver**: MAJOR (breaking) · MINOR (features) · PATCH (fixes). Bump the version in exactly one place per repo (VERSION file, package.json, or meta file).
2. **Changelog**: Keep-a-Changelog format; maintain `[Unreleased]` continuously; move entries under the version at release.
3. **Release notes**: user-facing — what changed, why it matters, breaking items with migration steps.
4. **Seal**: hash + sign build artifacts (`provenance-kit`); attach the manifest and signature to the release.
5. **Tag**: annotated tags (signed when keys exist); never move a published tag; never force-push release branches.
6. **Rollout plan**: canary or staged where feasible; write the rollback path before rolling out; name the approver.
7. **Post-release**: verify health for a defined window (24–48h); log discrepancies; close loops.

## Artifacts
- Version bump, CHANGELOG entry, release notes, signed manifest + `.sig`, annotated tag.

## Quality gates
- [ ] Changelog + version bump ship in the same change as the release content.
- [ ] Artifacts verified (checksums/signature) before announcement.
- [ ] Rollback plan exists and is testable.
- [ ] Post-release health check done and recorded.

## Red lines
- No untagged releases; no rewritten history on published branches.
- Deploys stay HITL — automation prepares, humans approve.

## Related
`ci-cd-pipeline` (build+sign) · `secure-build-pattern` (sealing) · `observability-ops` (health window).
