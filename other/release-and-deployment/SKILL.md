---
name: release-and-deployment
description: Release and deployment guidance for versioning, changelogs, rollout safety, and rollback-aware delivery.
compatibility: opencode
metadata:
  audience: release
  purpose: release-guidance
---
## Core approach

- Treat releases as operational events, not just git events.
- Verify what is changing, how it will be deployed, and how it can be rolled back.
- Surface migration coupling, environment assumptions, and release sequencing risks.
- Prefer repeatable, documented release steps.

## Practical guidance

- Check versioning, release notes, deployment prerequisites, feature flags, migrations, and rollback constraints.
- Make sure release communication reflects user-visible or operator-visible changes.
