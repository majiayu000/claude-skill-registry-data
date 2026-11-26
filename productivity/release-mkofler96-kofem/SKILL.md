---
name: release
description: Assess whether KoFEM is ready for a release, or route an explicit request to prepare-release or create-release. Use for release advice, changes since the last version, and the legacy release command.
---

# Release

Releases are requested by the maintainer, never scheduled or started from a
routine or weekly update. Choose the workflow from the request:

- **Assess**, "should we release?", or "what changed?": read
  [the assessment procedure](references/assessment.md) and report the result.
  This is read-only: do not create issues, labels, branches, or PRs.
- **Prepare release** or "plan the release": follow
  [prepare-release](../prepare-release/SKILL.md). It writes the release plan
  and readiness tasks in Linear, without changing product versions.
- **Create release**, "cut the release", or "open the release PR": follow
  [create-release](../create-release/SKILL.md). It checks the plan and current
  evidence before opening the version/changelog PR into `develop`.

Agents never create tags or GitHub Releases, merge the release PR, or open or
merge a promotion. The maintainer promotes `develop` to `main`; CI tags the
tested promotion commit and publishes its GitHub Release.
