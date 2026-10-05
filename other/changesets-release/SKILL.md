---
name: changesets-release
description: Records release intent with Changesets and guides semver, changelog, CI, and artifact-version checks for independently distributed packages. Use when a repository has `@changesets/cli`, `.changeset/`, a version-packages PR, publishable plugins, SDKs, libraries, or monorepos.
---

# Changesets Release

Use this for consumer-installed packages. Do not require Changesets for a single deployed application unless its owner chooses release versions.

## Decide Scope

- Use it for libraries, SDKs, CLIs, plugins, and packages published independently.
- In a monorepo, include every changed consumer package; let Changesets calculate internal dependency bumps.
- For internal-only work, use the repository's explicit `no-changeset` convention. Do not add an empty changeset merely to satisfy CI.
- Before first adoption, confirm the owner wants Changesets, then initialize it with the repository's package manager. Do not introduce a release dependency unilaterally.

## Add Release Intent

1. Read `.changeset/config.json`, package metadata, and the consumer contract before choosing a bump.
2. Use `patch` for compatible fixes, `minor` for compatible capabilities, and `major` for breaking behavior, removed APIs, or required consumer changes.
3. Run the configured `changeset` command and commit its generated `.changeset/<name>.md` with the implementation PR.
4. Write the entry for consumers: what changed, why it matters, and migration steps when needed. Never copy a commit subject as the release note.

## CI And Version PR

- Require a changeset or an approved `no-changeset` marker on releaseable PRs; `changeset status` is the non-interactive CI check.
- Use the Changesets GitHub Action to create/update a version-packages PR. Review generated versions and changelogs before merging.
- Keep publishing credentials in CI secrets. Never put registry tokens in a changeset, repository config, or commit.

## Supply-Chain Provenance

A CI secret and registry visibility are not proof of what was actually published. Every distributable artifact needs verifiable provenance before its release is considered complete.

- Prefer registry trusted publishing over a long-lived token for every package eligible for it — npm's trusted publishing issues short-lived OIDC-backed credentials per publish and automatically generates provenance for eligible public packages, replacing a standing `NPM_TOKEN` secret entirely. Check registry docs for the equivalent (PyPI Trusted Publishers, RubyGems Trusted Publishing) before assuming npm-only.
- When trusted publishing is unsupported by the registry (a private registry, a non-npm artifact, an internal package feed), generate a build provenance attestation for the distributable artifact instead — `actions/attest-build-provenance` for artifacts hosted with GitHub, or an equivalent SLSA-compliant attestation step, satisfying at minimum SLSA Build L1 (a provenance record identifying the output artifact by cryptographic digest and describing how it was built).
- Record the artifact's digest (sha256) in the release notes or version PR, not just its version string — a version tag can be recreated; a digest cannot.
- Verify the attestation after publish, not just generate it: `gh attestation verify <artifact> --repo <owner>/<repo>` (or the registry's equivalent) before declaring the release complete.
- State explicitly when a registry has no trusted-publishing or attestation support: document the fallback (long-lived token in CI secrets, manual digest recording) as a known gap, not a silent omission.

## Non-NPM Artifacts

Changesets records release intent; it does not automatically update every native manifest. The version PR must update and verify every public version surface.

- WordPress plugin: plugin header, `readme.txt` stable tag, ZIP filename/metadata, Git tag, and release notes.
- PHP/Composer package: package metadata, tag, generated artifact, and changelog.
- Application: only use Changesets when its release version is a real customer contract; otherwise keep deployment SHA and release notes separate.

## Release Check

1. Run the affected package tests and build.
2. Confirm generated changelog text is accurate and actionable.
3. Confirm the final tag and every distributable artifact report the same version.
4. Use `release-gate` for staging, rollout, rollback, and health checks.

## Verification

- `changeset status` succeeds in CI for a releaseable change.
- The version PR contains the expected bump and changelog entry.
- Artifact inspection proves all public version surfaces match the release tag.
- After publishing, follow `system-level/core.md` (Validation) and confirm the release appears in the intended package registry.
