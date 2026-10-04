---
name: project-vendor-boundary
description: Project overlay for checked-in or submodule-managed third-party source, provenance, local patches, and the app-owned integration seam. Not for package-manager dependency changes without vendored source.
---

# Project Vendor Boundary

This is a composable project overlay. Add matching implementation guidance when
the work requires language-specific code judgment.

For review, inspect provenance, local patches, and integration behavior without
updating, fetching, or replacing the vendor tree. During implementation, preserve
pre-existing local changes and apply only the requested integration or update.

## When to use

The change involves checked-in third-party source, a subtree or submodule, a
vendor directory, copied sources, a local vendor patch, or the app-owned adapter
around that material.

## Not for

Do not use this for ordinary package-manager version or lockfile changes with no
checked-in third-party source, app-owned code unrelated to the integration seam,
or generated outputs that must be changed through their generator. Use
`project-release-maintainer` for release concerns and compose it only when a
vendor change also affects shipped metadata. Use `security` first when exploit
review is the primary job.

## Workflow

1. Classify the material before editing: app-owned source, checked-in vendor
   source, submodule, generated output, or package-managed dependency. Read the
   repository's update instructions, provenance record, patch convention, and
   license or notice files when they exist.
2. Prefer an adapter or wrapper change in app-owned code when the integration
   seam can reasonably absorb it. Patch vendor source only when the seam cannot
   solve the problem without distorting the app contract.
3. Keep vendor patches minimal. Avoid unrelated formatting, generated churn,
   mass mechanical rewrites, or local style normalization inside the vendor
   tree. Record the upstream source or base version and patch rationale using
   the repository's existing convention.
4. Validate the app-owned seam and the narrowest relevant vendor build or test
   path the repo supports. Inspect the final diff for accidental vendor churn.
5. Update notices, provenance, upstream version, local patch records, install
   rules, or shipped metadata only when the vendor change affects them; do not
   rewrite these files for an app-only adapter change.

Treat fetching or replacing upstream source, moving a submodule, and filing an
upstream issue or contribution as separate actions with their own network and
external side effects. Do not edit generated vendor artifacts manually when a
documented regeneration path owns them.
