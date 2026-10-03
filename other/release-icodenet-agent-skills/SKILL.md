---
name: release
description: >-
  Prepare a release: decide the semantic version bump, write the changelog /
  release notes from actual changes, and tag. Use when releasing or publishing
  a package or service version, cutting a release branch, or when asked "what
  version should this be" or to write release notes. Do not use for the deploy
  execution itself (use deploy-checklist).
---

# Release

A release is a statement to consumers: what changed, whether it's safe to upgrade, and what they must do if not.

## Workflow

### 1. Collect the actual changes

Work from evidence, not memory: `git log <last-release-tag>..HEAD` plus the diff. Group commits into user-facing changes; ignore internal noise (CI tweaks, formatting) unless it affects consumers.

### 2. Decide the version bump

Apply the contract-guard classification (see the `contract-guard` skill and its breaking-change taxonomy) to everything in the release:

- Any breaking change to a public surface → **major**
- Compatible new capability → **minor**
- Behavior-preserving fixes only → **patch**

If a breaking change is present without a migration path documented, **stop** — that's a contract-guard failure to resolve before releasing, not a notes problem.

### 3. Write the notes

Structure, plain language, consumer perspective:

```markdown
## <version> — <date>

### Breaking changes        <!-- omit section if none -->
- <what broke> — **Migration:** <exact steps for the consumer>

### Added
- <new capability, phrased as what the user can now do>

### Fixed
- <symptom that no longer occurs>

### Changed / Deprecated    <!-- include deprecation timelines -->
```

Rules: every breaking entry has a migration step; entries describe outcomes, not commit titles; link issues/PRs where they exist.

### 4. Tag and record

- Update the changelog file if the repo keeps one (`CHANGELOG.md`) — append, never rewrite history of prior releases.
- Bump the version where the project declares it (package manifest, plugin manifest, etc.).
- `git tag v<version>` after the release commit; push tags.

## Constraints

- Never publish a major bump silently as minor "to avoid alarm" — mislabeled breaking changes are the worst outcome for consumers.
- Notes are for consumers, not contributors: no internal refactor bragging unless it changes observable behavior or performance.
- If the project uses conventional commits or a release tool (changesets, semantic-release), follow that convention instead of hand-rolling.

## Verification

- [ ] Change list derived from git history since last tag
- [ ] Bump justified against the breaking-change taxonomy
- [ ] Every breaking change has a migration step
- [ ] Version bumped in the manifest + changelog updated + tag created
