---
name: cross-repo-project
description: "The private GitHub Project spanning open enhancement issues across the EISS and NetSec repos: its scope, its boundary against milestones, the single Effort field, the manual add step, and the retirement threshold. Use when asked about the cross-repo Project board."
---

# 13. Cross-repo Project

A private GitHub Project at <https://github.com/users/EISSeuropa/projects/1>
("NetSec + EISS websites") spans open enhancement issues from both this
repo and the NetSec sister site.

### Scope

Open `enhancement` issues from both repos. Bugs stay in their own
per-repo tracker unless they cross-cut both sites structurally.

### Boundary against milestones

Rule §10 milestones remain the source of truth for release planning. The
Project is a view across the two repos, not a replacement for milestones.
Avoid double-bookkeeping: milestone a release, don't version-track in the
Project.

### Single custom field

`Effort: S / M / L`. Adding more fields requires a recurring need; the
anti-creep clause keeps the Project from becoming a second backlog.

### Not part of the release-time §5 cross-check

The Project is ambient awareness between cycles, not a release gate.

### Auto-add limitation

GitHub Projects v2 auto-add workflows (automatically adding issues with
a given label) need UI configuration under each repo's *Projects* tab;
the CLI does not expose this. Issues are added manually via
`gh project item-add`.

### Retirement threshold

If more than ~20% of items in any view are `Done`, or new entries stop
getting Effort tags, archive the Project rather than letting it drift.
