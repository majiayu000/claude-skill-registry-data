---
name: release-semver
description: |
  Semantic versioning releases — version bumps, changelogs, tags, publishing. Use when preparing a new release: deciding the version bump, drafting the changelog, tagging the commit, and publishing to the project's distribution channel.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-release-semver
    version: "1.2.0"
    created: 2026-04-06T00:00:00Z
    category: devops
    layer: 3
    commands:
      - name: pk-release
        args: "bump-type (major, minor, patch, or version number)"
        description: "Prepare a release: bump version, draft changelog, create tag."
      - name: pk-publish
        args: ""
        description: "Execute the publish phase of the prepared release."
---

# Semantic Versioning Release Process

## Intro

Releases are routine, not heroic. Decide the version bump from the
nature of the changes, draft a changelog, update version files in
one commit, tag with `vX.Y.Z`, and publish. The goal is a release
anyone on the team can perform from the same checklist.

## Overview

### Determine the version bump

Semantic versioning has three numbers: MAJOR.MINOR.PATCH.

- **Patch** (0.1.0 → 0.1.1): bug fixes only, no API changes.
- **Minor** (0.1.0 → 0.2.0): new features, backward-compatible.
- **Major** (0.1.0 → 1.0.0): breaking changes.

Pre-1.0 projects bend the rules: minor bumps are allowed to break
compatibility, and patch bumps cover both features and fixes. Once
you ship 1.0, the rules become strict.

### Pre-release checklist

- All tests pass on the designated release-integration branch.
- No uncommitted changes in the working tree.
- Dependencies reviewed and up to date where appropriate.
- `CHANGELOG.md` has a curated, dated section for the exact release tag;
  it includes only user-visible changes, uses standard categories, and has
  correct comparison links.
- A root `LICENSE` file exists and matches the intended project
  license. If the project ships release archives, the archive build must
  include that `LICENSE` at the top level. For processkit,
  `scripts/build-release-tarball.sh` copies root `LICENSE` into
  `processkit-vX.Y.Z/`.

### Draft the changelog

Group entries under **Added**, **Changed**, **Fixed**, and
**Removed**. Reference issue and PR numbers. Note breaking changes
prominently — call them out in their own section if a major bump
is involved.

### The release flow (single turn, bulletproof)

A release is **one continuous sequence** — you do not stop halfway.
`/pk-release vX.Y.Z` runs every step below in order, in the same
turn, and is not considered done until the final verification
passes. See DEC-20260422_1348-SnowyWolf.

1. **Bump version** in every relevant file (`aibox.lock`,
   `Cargo.toml`, `pyproject.toml`, `package.json`, lockfiles).
2. **Finalize CHANGELOG** — rename the `[vX.Y.Z-candidate]` section
   to `[vX.Y.Z] — YYYY-MM-DD`; ensure Added/Changed/Fixed/Removed
   grouping; call out breaking changes if a major bump. Confirm the
   root `CHANGELOG.md` contains a `## [vX.Y.Z]` heading; the archive
   build rejects a release without it.
3. **Regenerate provenance / transitive artifacts** — for processkit,
   `scripts/stamp-provenance.sh vX.Y.Z`.
4. **Commit** the bump with message `chore(release): bump to vX.Y.Z`.
5. **Tag** the commit: `git tag -a vX.Y.Z -m "<tag summary>"`.
6. **Push** the release-integration branch then tag. For a stable release,
   merge that tagged branch into `main` immediately afterwards; for a v1
   prerelease, retain the tag on `v1.x-pre-release`.
   A tag push alone does **not** create a GitHub Release — it is a
   git ref, not a distribution-channel artifact.
7. **Create the GitHub Release** with notes extracted from the
   CHANGELOG and attach the release archive plus checksum when the
   project produces binary/archive assets. For processkit, build first
   with `scripts/build-release-tarball.sh vX.Y.Z`; the tarball must
   contain top-level `LICENSE` and `CHANGELOG.md`. The tag commit must
   also contain root `LICENSE`, so GitHub's generated source archives
   carry the license. The single canonical command:
   ```bash
   gh release create vX.Y.Z \
     dist/processkit-vX.Y.Z.tar.gz \
     dist/processkit-vX.Y.Z.tar.gz.sha256 \
     --repo <org>/<repo> \
     --title "vX.Y.Z — <one-line summary>" \
     --notes-file <(awk -v v=X.Y.Z '
       $0 ~ "^## \\[v" v "\\]"   { f=1; next }
       f && /^## \[/              { f=0 }
       f
     ' CHANGELOG.md) \
     --latest
   ```
8. **Verify** the Release is live. This is the release's
   completion gate. For archive-based releases, verify the Release has
   the expected tarball/checksum assets and that extracting the tarball
   shows a top-level `LICENSE`; also verify the tag itself contains
   root `LICENSE`:
   ```bash
   gh release view vX.Y.Z --repo <org>/<repo>
   tar -tzf dist/processkit-vX.Y.Z.tar.gz | grep '/LICENSE$'
   git show vX.Y.Z:LICENSE >/dev/null
   ```
   If this exits non-zero, the release is **incomplete** — return
   to step 7. Do not report the release as done until step 8
   succeeds.
9. **Other channels** (crates.io, PyPI, npm, container registry,
   homebrew tap, etc.) — run after step 8 so the GitHub Release
   remains the canonical artifact pointer.

**Recovery pattern** — if a tag was pushed in a prior session
without the Release, run `gh release create` and `gh release view`
for that tag directly; `/pk-publish` exists as an alias for this
recovery scenario.

**pk-doctor `release_integrity` check (detection layer)** — walks
every local `v*` git tag, probes GitHub for a matching Release, and
WARNs on any tag without one. Run `/pk-doctor --category=release_integrity`
after a release to confirm; run `/pk-doctor` routinely to catch any
historical gap. Requires `gh` CLI + auth; emits INFO when `gh` is
unavailable.

### Example

User says: "Let's release — we fixed two bugs and added a feature."
The agent recommends a minor bump (because of the new feature),
drafts changelog entries grouped Added/Fixed, updates version
files, creates the bump commit, and tags it.

This skill also provides the `/pk-release` and `/pk-publish` commands
for direct invocation — see `commands/pk-release.md` and
`commands/pk-publish.md`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Bundling a breaking change into a patch or minor release.** Consumers rely on semver guarantees to control when they take breaking changes. A breaking change in a patch release violates the contract and causes silent runtime failures in consumer code.
- **Skipping the changelog because "git log has it".** Git log is not a changelog. It lacks context, grouping, and the human judgment that makes a changelog useful. Every release needs a curated changelog with Added/Changed/Fixed/Removed sections.
- **Bumping all version files in separate commits.** A brief window where `Cargo.toml` says `1.2.0` but `pyproject.toml` still says `1.1.0` is a broken state. Update all version files in a single atomic commit.
- **Tagging before CI passes.** A tag should point to a commit that has been fully built and tested. Tagging a commit that later fails CI means the published artifact may not match what was verified.
- **Publishing from a developer machine without a clean checkout.** Uncommitted local changes — WIP files, debug flags, `console.log` statements — may sneak into the artifact. Publish from CI with a clean checkout or from a fresh clone.
- **Re-tagging a published version to fix a mistake.** Package registries (crates.io, PyPI, npm) prohibit or block re-publishing to an existing version. Cut a new patch version (e.g. `1.2.1`) to fix a mistake in `1.2.0`; never overwrite a tag.
- **Pre-1.0 projects that promise stability they cannot keep.** If the API is still moving, stay below 1.0 and say so. Cutting `1.0.0` too early creates a compatibility obligation that slows future improvements.
- **Treating `git push --tags` as "the release is out."** Pushing a tag creates a git ref; it does **not** create a GitHub Release, a crates.io release, a PyPI release, or any other distribution-channel artifact. Downstream consumers (package managers, `gh api`, the Releases page, auto-sync tools like aibox) read from the channel, not the tag. Until `gh release create` (or the equivalent channel publish command) has run, the release is not visible. The flow above bakes this in: the release is not complete until step 8 (`gh release view`) succeeds. See DEC-20260422_1348-SnowyWolf.
- **Stopping after `/pk-release` prepare-like work.** In an older split where `/pk-release` prepared and `/pk-publish` published, it was easy to do only half. The current flow is single-turn: /pk-release runs every step through GitHub-Release verification. /pk-publish remains only as a recovery alias for historical tags without Releases.

## Full reference

### When pre-1.0 ends

Cut 1.0 when the public API is something you are willing to
support without breaking. Until then, keep the version below 1.0
honestly — there is no shame in 0.17.0, and it signals to users
that the surface may still move.

### Version bumps for special changes

| Change | Bump |
|---|---|
| Bug fix that does not change behavior contract | patch |
| Performance improvement, no API change | patch |
| New feature behind a feature flag | minor |
| New optional parameter with a default | minor |
| Removing or renaming a public symbol | major |
| Changing default behavior of an existing API | major |
| Tightening input validation that rejects previously valid input | major |
| Dependency bump that surfaces in your public API | major |

### Anti-patterns

- Bundling breaking changes into a patch release
- Skipping the changelog "because git log has it"
- Tagging a commit that was not built and tested
- Publishing from a developer machine without a clean checkout
- Re-tagging a published version to fix a mistake (cut a new
  patch instead)
- Pre-1.0 projects that promise stability they cannot keep
