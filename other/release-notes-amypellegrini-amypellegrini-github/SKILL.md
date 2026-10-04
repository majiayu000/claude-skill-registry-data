---
name: release-notes
description: "Draft release notes from a verified release scope for the intended audience and distribution channel."
metadata:
  category: Delivery
---

# Release Notes

## Adapt to the target repository

Use the repository selected by the user or the current working directory. Read its applicable instructions and relevant project documentation. Discover the remote owner, default branch, package manager, build/test commands, issue tracker, and workflow conventions from that repository; do not assume any particular stack, hosting service, board, or directory layout. In a multi-repository workspace, resolve each issue or PR to its owning checkout before acting.

Use available authenticated tools for the configured service. For GitHub, resolve the repository with `gh repo view --json nameWithOwner,defaultBranchRef` and pass explicit repository context when working across checkouts. Project boards are optional: discover their owner, fields, and status values instead of assuming they match repository ownership or fixed names. Ask only when essential context is missing or ambiguous.

The user's request defines the authorized actions. This skill does not grant permission to publish messages, push, merge, or change project state. Preserve unrelated local changes. Use existing authorization without repeatedly asking. If a named companion skill or subagent is unavailable, follow the procedure here with the tools you have and report any capability that prevents completion.

## Procedure

1. Resolve the release scope: version/tag range, milestone, project, merged PRs, or an explicit list. Discover the repository's release history and template. Ask for the range when it cannot be inferred reliably; do not equate every closed issue with shipped work.
2. Collect changes in that scope, including pagination, and cross-check merge/release status. Exclude work not included in the release. Separate known limitations from delivered changes.
3. Write user-facing outcomes grouped appropriately, such as features, fixes, and improvements. Explain a technical change only when it affects users or integrators. Highlight breaking changes and migration steps with supporting evidence.
4. Follow the requested audience, language, and channel. Apply a store's length or formatting limit only when that store is the chosen destination and its current requirement is known. Do not assume mobile distribution or a universal character limit.
5. Validate names, version numbers, issue links, and any length constraints. Avoid claims not supported by the release contents.

## Deliverable

Return a release-notes draft and the included scope. Publishing a release, creating a tag, or uploading to a store requires authorization for that action; drafting notes alone does not grant it.
