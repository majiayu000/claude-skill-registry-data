---
name: release
description: "Drives a release through the repository's release tool, release-me by default or release-please where configured: verifies pending commits and the release pull request, merges it only after confirmation, and checks the resulting tag and changelog. Use when a version should be cut."
---

# Release

Cut a release through the repository's release tool, never around it.

## When to use

- A version should be published.
- A release pull request exists and needs review before merging.
- A release ran but the tag, changelog or artifacts are missing.

## Steps

1. Read `release` from the config. `false` means release automation is disabled for
   this repository. Report that and stop instead of releasing manually. `release.tool`
   names which tool, release-me by default, release-please where configured.
2. Determine the current state: the latest tag, and the commits since that tag on the
   default branch. release-please also carries state in
   `.release-please-manifest.json`; release-me reads the tags directly, with nothing
   else to check.
3. Check the commit subjects. They become the changelog. A wrong subject or an
   unmarked breaking change gets fixed before releasing, because the changelog cannot
   be fixed afterwards.
4. State the expected version from the commit types before doing anything.
5. Verify the repository is releasable: CI green on the default branch, tests and
   linters passing, migration notes present for breaking changes.
6. Find the release pull request by its pending label: `release: pending` for
   release-me, `autorelease: pending` for release-please, both the tool's own default,
   overridden in its config. If none exists, name why: no releasable commits, a failed
   workflow, or a configuration problem. Never tag manually to work around a missing
   release pull request.
7. Review the release pull request: version, changelog entries, every file the tool
   touched.
8. Ask for confirmation, then merge it.
9. Verify the result: tag created, release published, changelog updated, release
   artifacts built, the pull request's label swapped to tagged (`release: tagged` or
   `autorelease: tagged`).
10. Report the version, the release URL and anything that did not complete.

## Guardrails

- Commits since the last release reviewed, subjects fit for the changelog.
- Expected version stated before merging.
- CI green on the default branch before release.
- Merge confirmed before it happens. No manual tag, no `gh release` where the release
  tool is configured.
- Tag, release, changelog and artifacts verified afterwards.

## Config

- `release`: `false` disables release automation for the repository.
- `release.tool`: release tool. Default `release-me`.

## References

- `release-conventions` for versioning and changelog rules.
