---
name: project-release-maintainer
description: Project overlay for release and packaging maintenance across install layout, shipped assets, automation, license and notice alignment, and release docs. Not for content-only documentation or publishing without explicit authorization.
---

# Project Release Maintainer

This is a composable project overlay. Add matching implementation guidance when
source, build, or automation code changes. Compose with `documenter` when the
main artifact is durable release, install, or contributor documentation.

For review or planning, inspect and report without changing package contents,
manifests, notices, or release state. Apply the workflow as edit instructions
only when the user asks for those changes.

## When to use

The change affects the shipped or published contract: package contents, install
rules, release automation, shipped assets, license and notice files, release
checklists, or documentation that must match those artifacts.

## Not for

Use `documenter` alone for content-only edits that do not require reconciliation
with shipped artifacts. For internal code changes with no release impact, use
the matching principle skill and add `project-core-dev` only when repository-
specific completion evidence is not concrete. Use `project-config-and-tests`
for config contracts. Use `project-vendor-boundary` as primary for vendored
source ownership, and compose both overlays when a vendor change also alters
shipped metadata.

## Workflow

1. Inventory the existing release contract from package manifests, install
   rules, shipped assets, release automation, license and notice files,
   checklists, and public documentation. Identify the source of truth before
   editing.
2. Trace the requested change across only the affected artifacts. Keep package
   contents, install behavior, public commands, examples, and release notes
   mutually consistent.
3. Use the repo's existing dry-run, package-listing, hygiene, and verification
   commands. When install behavior changes, validate in a temporary install tree
   and clean it up; smoke-test the installed artifact when practical.
4. Inspect the produced package or staged tree rather than inferring contents
   from build configuration alone. Report unavailable signing, platform, or
   publication checks instead of implying they passed.
5. Keep documentation concise and grounded in the shipped build. Do not invent
   CI, packaging, signing, publishing, or release workflows that the repo does
   not contain or the user did not request.

Treat tagging, publishing, uploading, signing, credential use, and creating an
external release as separate consequential actions that require explicit
authorization. Limit license work to keeping declared license and notice files
consistent; do not make legal compatibility claims or change project licensing
without explicit direction.
