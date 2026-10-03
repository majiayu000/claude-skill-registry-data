---
name: ls-automatic-versioning
description: Use and maintain automatic versioning from conventional commits; VERSION as source of truth; sync to READMEs and docs. Use when working on version bumps, release workflow, or when the user asks about versioning or conventional commits.
metadata:
  version: "1.1"
---

# Automatic versioning (framework)

**Purpose:** The framework uses semantic versioning with VERSION as source of truth. Use this skill when implementing, explaining, or changing versioning behavior so it stays consistent and framework-appropriate.

## Source of truth

- **VERSION** (repo root): single line, semantic version `MAJOR.MINOR.PATCH` (e.g. `2.0.0`). This is the only canonical version value.
- **Displayed version** must stay in sync: README and framework README show `**Version:** X.Y.Z`; framework docs use YAML front matter `version: X.Y` (major.minor). The repo tooling keeps these in sync when the release workflow runs.

## Patch-default release policy

- **Default:** normal development batches release as one PATCH increment, including commits that use `feat:` for readability.
- **Explicit release type:** add `Release-Type: major|minor|patch|none` in the commit body to request any non-default release impact or to document an intentional patch/no-bump decision.
- **Breaking markers:** `BREAKING CHANGE:` in the body or type followed by `!` (for example `feat!: new API`) are diagnostics only until paired with `Release-Type:`. `version-plan` fails when a breaking marker is present without the explicit trailer.
- **No bump:** Merge commits, version-sync commits, and fully canceled unreleased reverts.
- **Diagnostics:** `version-plan` keeps `raw_bump` as the Conventional Commit interpretation and `bump` as the effective patch-default release decision.

## Explicit sequential logical-slice policy

A valid `.localsetup-release.json` committed in the planned HEAD selects
`sequential-logical-slices` consistently across the planner, CLI, preflight,
pre-push and release CI. Repositories without this file retain `patch-default`.
Python callers can explicitly select sequential mode when unconfigured; they
cannot override a conflicting committed contract. Loose worktree policy changes
do not activate, replace or disable the selected commit's policy.

Use the [release policy schema](../../config/release-policy.schema.json).
Schema 1 contains `schema_version: 1`, `policy: "sequential-logical-slices"`,
an `anchor` containing full commit SHA, canonical version and matching version
tag, and `overrides`. Schema 2 is the repository's one-time 4.x correction: it
adds `major_line: 4` and exact `reconciliation` evidence for the original anchor,
the immutable pre-correction release anchor, the source and corrected cutoff
versions, and the breaking source SHAs reclassified from MAJOR to MINOR. Runtime
validation binds tags to commits, replays historical sync checks and arithmetic,
requires the committed cutoff and corrected version to match, and requires HEAD
to be version-synced even when no new slice adds a bump. Until the corrected 4.x
tag is published, arithmetic starts at the corrected cutoff; afterwards, it
starts at the newly verified 4.x release anchor while retaining the historical
reconciliation record and published baseline for release-document coverage.

The loader requires a regular committed blob of at most 64 KiB, exact fields and
types, and no duplicate keys or override SHAs. Each override has `commit`, `slice`
and `classification`; it identifies one unpublished source SHA and reviewed
logical ID/impact. It cannot target merges, generated receipts, reverts or
published work, or downgrade breaking changes. Actual messages and diagnostic
`raw_bump` remain intact; full and prefix folds use the same overrides.

Verify the published tag/commit independently before selecting or advancing the
anchor. The planner checks local committed VERSION and ancestry without network
access. When advancing to a verified published commit, clear already-published
overrides and commit the policy update; preserve exact source ancestry. The
repo-only file is export-excluded and must not be copied into converted projects.

- Each accepted logical source slice increments once: `feat:` defaults to MINOR and resets PATCH; other source commits default to PATCH. `Release-Type:` declares explicit impact.
- `Release-Slice: lowercase-id` groups unpublished members. Otherwise each source SHA is distinct. The first integrated source member anchors the slice; its highest final member classification determines the single increment. An interleaved later feature member upgrades that original slice without moving it or counting it twice.
- Integration traverses first-parent history, then newly introduced side ancestry in recorded parent order, never author/committer dates.
- Breaking markers require an explicit `Release-Type: major` compatibility decision. Lower/none overrides, duplicate or malformed metadata fail planning. An active 4.x major-line lock also rejects major classifications; restore compatibility or stop release work until the lock is explicitly amended.
- Actual merges and generated-only receipts are excluded using changed-path/owned-facts evidence, not subject resemblance. Sync commits must change only canonical version/generated content.
- Each sync's recorded and committed version must match its own ancestry-prefix target; the latest sync and HEAD must match the final target. Incorrect historical syncs require explicit reviewed reconciliation, not automatic exemptions.
- Exact native Git reverts cancel fully reverted unpublished slices only when single-parent raw path/blob/mode changes prove the complete inverse. Mixed changes, conflict-adjusted reverts or later changes to the same affected file require explicit reconciliation; later unrelated files remain untouched. Partial grouped reverts, ambiguous targets and revert-of-revert histories require explicit reconciliation. Reverting published work is a new maintenance outcome.
- Existing plan fields remain. `logical_slices` records anchors, members, classification and before/after versions; `excluded_commits` and `version_sync_checks` explain evidence. Aggregate `bump` is the highest category, not target arithmetic.
- With committed policy, comparison/upstream refs are diagnostic metadata; arithmetic always uses the anchor. Without configuration, explicit sequential bases must be ancestors. Invalid historical prefixes are nonrepairable and stop mutation; ordinary target drift is repairable. Explicit version targets cannot bypass canonical arithmetic. Do not guess historical aliases or use private ledgers as hidden CI configuration.

## In this repo (public framework)

The corrected 4.x release line is explicitly major-locked. Only MINOR and PATCH
increments are allowed while the lock is active; do not produce an automatic or
implicit MAJOR increment. Reject prospective MAJOR classifications, including
`Release-Type: major`, rather than silently downgrading them.

This one-time numbering reconciliation leaves the published pre-correction tag and
assets immutable and maps that content to corrected arithmetic 4.43.2 after the
exact historical issue-100 MAJOR-to-MINOR reconciliation. Branding maps to
4.44.0, and canonical repository-name policy maps to 4.44.1. The 4.44.1
corrected release established this numbering baseline. Its release guidance must
clearly disclose the existing SDK paging and Agent Q v2/envelope compatibility
breaks. Renumbering did not restore source or protocol compatibility.
This policy classifies the repository-only `reconciliation.published_anchor` as
`MISNUMBERED_HISTORICAL` for this actual publication; it must not be selected
as an active 4.x release candidate.

Version bump and doc sync are performed by deterministic repo tooling. Use `uv run --locked python ls/tools/localsetup.py --source-root . release-push` for normal release pushes. Raw `git push` is guarded: if a sync commit is needed, `.githooks/pre-push` creates it and stops the stale push so the next push sends the correct commit.

For read-only release preflight, run `uv run --locked python ls/tools/localsetup.py --source-root . version-plan` and `uv run --locked python ls/tools/localsetup.py --source-root . version-sync --check --target "$(cat VERSION)"`.

## Reference

- Versioning doc: [ls/docs/VERSIONING.md](../../docs/VERSIONING.md) is the public reference.

## Rule ownership

This skill owns versioning and release-sync behavior. Keep `VERSION`, generated docs, version-sync path lists, provenance, and release tooling aligned here before updating the public doc.

- `VERSION` is canonical.
- Release impact uses the explicitly selected repository policy; existing callers retain patch-default unless sequential mode is selected.
- Generated docs and generated taxonomy artifacts are part of release sync; do not leave them outside the versioning candidate/staging lists.

## Finalize before generating

Complete the accepted source slice, then bind its release record and generate
version/document outputs once. Preserve the owning generator's source commit
and tree provenance; never edit generated receipts to manufacture a clean check.
A docs-only receipt or unchanged integration does not itself require another
full suite. Use the publishing skill's exact-commit CI evidence path, focused
checks for follow-up changes, and the existing signed-tag/artifact checks.
