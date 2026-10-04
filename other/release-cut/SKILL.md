---
name: release-cut
version: 0.1.0
license: MIT
description: Use when the user asks to cut a release, tag a version, publish a release, or roll up the changelog. Not for routine merges; releases happen on request, not per feature.
---

# release-cut

Turn accumulated merged work into a clean tagged release: changelog roll-up, version bump, tag, GitHub release, and a drafted announcement. Drafts are drafts; nothing gets posted to social platforms by this skill.

## Preconditions

Check before touching anything; stop and report if any fail:
- On the default branch, clean tree, up to date with the remote
- CI green on the head commit
- Tests pass locally (run them, do not assume)

## Steps

1. **Scope the release.** `git log <last-tag>..HEAD --oneline` plus the CHANGELOG's Unreleased section. If the two disagree, reconcile first; the log is the truth, the changelog is the narrative.
2. **Pick the version.** Semver from the actual changes: breaking = major (or minor pre-1.0), features = minor, fixes only = patch. State the reasoning in one line.
3. **Roll the changelog.** Move Unreleased under the new version with today's date. Entries describe user-visible effects, not commit subjects. Start a fresh empty Unreleased section.
4. **Bump the version** everywhere the project declares it (package manifest, version constant, docs). Grep for the old version string to catch stragglers.
5. **Commit and tag.** `chore: release vX.Y.Z` then an annotated tag: `git tag -a vX.Y.Z -m "vX.Y.Z"`.
6. **Push, then release.** Push branch and tag, then `gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <(extracted changelog section)`.
7. **Draft the announcement.** Two or three sentences per platform the user actually publishes to: what shipped, why anyone should care, link. Hand the drafts to the user; do not post.

## Rules

- Never invent changelog entries. Every line traces to a commit or PR.
- Never release with failing or skipped tests "because the failure is unrelated". Fix or explicitly get the user's call.
- Version appears in code AND tag AND changelog AND release title. All four match or the release is wrong.
- If nothing user-visible changed since the last tag, say so and recommend not releasing.

## Common mistakes

- Tagging before pushing the release commit, leaving the tag pointing at an unpushed SHA.
- Release notes that are commit logs. Readers want effects, not plumbing.
- Bumping versions per merged feature. Accumulate, then release when there is a story to tell.
